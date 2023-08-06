import glob
import logging
import sys
import threading
import time

import serial

from hardware_communicator.abstract_communicator import AbstractCommunicator


def get_avalable_serial_ports(ignore=None):
    if ignore is None:
        ignore = []
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    ports = set(ports)

    result = []
    for port in ports.difference(ignore):
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return set(result)


PORT_READ_TIME = 0.01


class SerialCommunicator(AbstractCommunicator):
    POSSIBLE_BAUD_RATES = [
        460800,
        230400,
        115200,
        57600,
        38400,
        19200,
        14400,
        9600,
        4800,
        2400,
        1200,
    ]

    def __init__(self,interpreter, port=None, auto_port=True,**kwargs):
        super().__init__(interpreter=interpreter,**kwargs)
        self.connection_checks = []
        self.port = port
        self.connected = False
        self.serial_connection = None
        self.is_open = False
        self.read_buffer = []
        self._work_port_task=None
        self._in_finding = False
        if not hasattr(self, "logger"):
            self.logger = logging.getLogger(self.__class__.__name__)
        if not hasattr(self, "on_connect"):
            self.on_connect = None
        if self.port:
            self.connect_to_port(port)

        if not self.connected:
            if auto_port and self.interpreter:
                def ap():
                    time.sleep(0.5)
                    self.find_port()
                threading.Thread(target=ap,daemon=True).start()


    def find_port(self, excluded_ports=None, retries=3):
        if self.connected:
            return self.port
        if self._in_finding:
            return None
        self._in_finding=True

        if excluded_ports is None:
            excluded_ports = []

        self.logger.info("Check ports"+str(get_avalable_serial_ports(ignore=excluded_ports)))
        for port in get_avalable_serial_ports(ignore=excluded_ports):
            self.connect_to_port(port, retries=retries)
            if self.connected:
                self._in_finding=False
                return self.port
        self._in_finding = False

    def add_connection_check(self, function):
        self.connection_checks.append(function)

    def connect_to_port(self, port, retries=3):
        for i in range(retries):
            self.logger.debug(f'try connecting to port "{port} try {i + 1}/{retries}"')
            for baud in self.POSSIBLE_BAUD_RATES:
                self.logger.debug(f'try connecting to port "{port} with baud {baud}"')
                try:
                    self._open_port(port=port, baud=baud)
                    time.sleep(0.1)
                    check = True
                    for func in self.connection_checks:
                        r = func()
                        if not r:
                            check = False
                            break
                    if check:
                        time.sleep(0.5)
                        self.connected = True
                        break
                    else:
                        self.stop_read(permanently=True)
                except serial.serialutil.SerialException:
                    time.sleep(0.5)
            if self.connected:
                self.port = port
                self.logger.info(f'successfully connected to "{port} with baud {baud}"')
                if self.on_connect:
                    self.on_connect()
                return port

    def _close_port(self):
        self.port = None
        port = None
        if self.serial_connection:
            port = self.serial_connection.port
            self.serial_connection.close()
        if self.is_open:
            self.logger.info("port closed " + port)
        self.serial_connection = None
        self.is_open = False

    def _open_port(self, port, baud):
        self.port = port
        if self.serial_connection or self.is_open:
            self._close_port()
        self.serial_connection = serial.Serial(port, baudrate=baud, timeout=0)
        self.is_open = True
        self._work_port_task = threading.Thread(target=self.work_port,daemon=True)
        self._work_port_task.start()

    def work_port(self):
        while self.is_open:
            try:
                if self.is_open:
                    self._write_to_port()
                    try:
                        c = self.serial_connection.read()
                    except AttributeError as e:
                        c = ""
                    while len(c) > 0:
                        #print(ord(c),c)
                        self.read_buffer.append(c)
                        self.validate_buffer()
                        if not self.is_open:
                            break
                        try:
                            c = self.serial_connection.read()
                        except AttributeError as e:
                            c = ""
                time.sleep(PORT_READ_TIME)
            except Exception as e:
                self.logger.exception(e)
                self.stop_read()
        self.logger.error("work_port stopped")
        self.stop_read()

    def stop_read(self, permanently=False):
        port = None
        baud = None
        if self.serial_connection:
            port = self.serial_connection.port
            baud = self.serial_connection.baudrate
        self._close_port()
        if not permanently and port:
            self._open_port(port=port, baud=baud)

    def detatch(self):
        self.stop_read(permanently=True)

    def write_to_port(self, send_item):
        return self.send_queue.append(send_item)

    def _write_to_port(self):
        #   if(len(self.send_queue)>0):
        # print(self.port, self.send_queue)
        for item in self.send_queue:
            try:
                self.serial_connection.write(list(item.data))
            except Exception as e:
                self.logger.error(f"cannot write {item}")
                raise e
            item.sended(self)

    def validate_buffer(self):
        self.read_buffer = self.interpreter.decode_data(self.read_buffer, self)
