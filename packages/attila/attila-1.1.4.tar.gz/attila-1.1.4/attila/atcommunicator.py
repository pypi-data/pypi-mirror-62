# ATtila
# Developed by Christian Visintin
#
# MIT License
# Copyright (c) 2019 Christian Visintin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from .exceptions import ATSerialPortError

from serial import Serial, SerialException, SerialTimeoutException
import re
from time import time
from time import sleep

class ATCommunicator(object):
  """
  ATCommunicator class provides an interface to communicate with an
  RF module using AT commands through a serial port
  """

  def __init__(self, serial_port, baud_rate, default_timeout = 10, line_break = "\r\n"):
    """
    Class constructor. Instantiates a new :class:`.ATCommunicator.` object with the provided parameters.

    :param serial_port: serial port to use in order to communicate with the RF module
    :param baud_rate: baud rate to set
    :param default_timeout (optional): the default timeout for command response read in seconds; it will be used if a timeout is not provided when executing a command         :param line_break (optional): specify line break to use when sending command; most of RF modules use CRLF
    :type serial_port: string
    :type baud_rate: int
    :type default_timeout: int > 0
    :type line_break: string
    """
    self._device = None
    self._serial_port = serial_port
    self._baud_rate = baud_rate
    self.default_timeout = default_timeout
    self._line_break = line_break

  @property
  def serial_port(self):
    return self._serial_port

  @serial_port.setter
  def serial_port(self, serial_port):
    self._serial_port = serial_port

  @property
  def baud_rate(self):
    return self._baud_rate

  @baud_rate.setter
  def baud_rate(self, baud_rate):
    self._baud_rate = baud_rate

  @property
  def default_timeout(self):
    return self._default_timeout

  @default_timeout.setter
  def default_timeout(self, timeout):
    if timeout:
      if timeout > 0:
        self._default_timeout = timeout
      else:
        self._default_timeout = 10
    else:
      self._default_timeout = 10

  @property
  def line_break(self):
    return self._line_break

  @line_break.setter
  def line_break(self, brk):
    self._line_break = brk

  def open(self):
    """
    Open serial port

    :raises ATSerialPortError
    """
    if not self._serial_port:
      raise ATSerialPortError("Serial port is not set")
    if self._device:
      self.close()
    try:
      self._device = Serial(self._serial_port, self._baud_rate, timeout = 0.1, write_timeout = self._default_timeout, rtscts=True, dsrdtr=True)
    except (OSError, SerialException) as error:
      raise ATSerialPortError(error)

  def close(self):
    """
    Close serial port

    :raises ATSerialPortError
    """
    if not self._device:
      raise ATSerialPortError("Serial port device is closed")
    try:
      self._device.close()
    except (OSError, SerialException) as error:
      raise ATSerialPortError(error)
    self._device = None

  def is_open(self):
    """
    Returns whether the serial port is open

    :returns bool
    """
    return self._device != None

  def exec(self, command, timeout = None):
    """
    Execute AT command

    :param command: command to execute
    :param timeout: timeout for command, if not set default will be used
    :type command: str
    :type timeout: int
    :returns tuple of (list of string, execution time ms); list: command response without line break; empty lines are ignored
    :raises ATSerialPortError
    """
    if not self._device:
      raise ATSerialPortError("Serial port device is closed")
    if not timeout:
      timeout = self.default_timeout
      self._device.write_timeout = self.default_timeout
    else: #Set write timeout to timeout
      self._device.write_timeout = timeout
    #Get start time
    t_start = int(time() * 1000)
    try:
      if self._line_break:
        self._device.write(b"%s%s" % (command.encode("utf-8"), self._line_break.encode("utf-8")))
      else:
        self._device.write(b"%s" % command.encode("utf-8"))
    except SerialTimeoutException as err:
      raise ATSerialPortError(str(err))
    data = ""
    #Set timeout to t_start + timeout seconds
    t_timeout = t_start + (timeout * 1000)
    t_now = t_start
    data_still_available = True
    sleep_time_based_on_baud = 1000 / self.baud_rate
    #Try to read until there are data available and t_now < t_timeout
    while t_now < t_timeout and data_still_available:
      t_now = int(time() * 1000)
      #Read one byte
      read_byte = self._device.read()
      if not read_byte:
        continue
      #Sleep for a while in order to give data the time to come
      if read_byte == "\n" or read_byte == "\r":
        sleep(sleep_time_based_on_baud)
      #Check if there are still data available
      if self._device.in_waiting > 0:
        data_still_available = True
      else:
        data_still_available = False
      data += read_byte.decode("utf-8")
    #lines = self._device.readlines()
    lines = data.splitlines()
    t_end = int(time() * 1000)
    for i in range(len(lines)):
      #lines[i] = lines[i].decode("utf-8")
      #Remove newline
      if re.search("(\\r|)\\n$", lines[i]):
        lines[i] = re.sub("(\\r|)\\n$", "", lines[i])
    #Flush input buffer
    self._device.reset_input_buffer()
    return (lines, t_end - t_start)
