#!/usr/bin/env python
#
# Author March 2019 Zhenxing Xu <xuzhenxing@canaan.creative.com>
#
# USBTORS485 connect PLC: Custom communication protocol in RPI and PLC
# protocol: start, function code, datas, end. All 4 bytes.
# start		    function code			        data0       end
# 'C'/0x43	    writing big fan: 0		        0/1/2		'N'/0x4E
#		        reading send wind temp: 1
#		        reading back wind temp: 2
#		        reading dry room temp1: 3
#		        reading dry room temp2: 4
#

import serial
import time
import sys


def rs485_open():
    global COM_Port

    try:
        # Opening the serial port
        COM_PortName = "/dev/ttyUSB0"
        COM_Port = serial.Serial(COM_PortName, timeout=1)

        # Set Baud rate, Number of data bits for 8, No parity, Number of Stop bits for 1
        COM_Port.baudrate = 9600
        COM_Port.bytesize = 8
        COM_Port.parity = 'N'
        COM_Port.stopbits = 1
    except:
        return False

    return True


def rs485_close():
    try:
        # Closed COM Port
        COM_Port.close()
    except:
        return False

    return True


# Read RS485 datas
def rs485_read(cnt):
    read_data = []

    try:
        for idx in range(cnt):
            rx_data = COM_Port.read()
            read_data.append(hex(ord(rx_data)))
    except:
        return None

    return read_data


# Write RS485 datas
def rs485_write(data):
    bytes_cnt = COM_Port.write(data)
    print("Write: write count = %d bytes, datas: %s" % (bytes_cnt, data))


# Setting big fan's speed
def set_fan_speed(level):
    print("\033[1;32m\nSet fan speed\033[0m")

    data = [67, 0, 0, 78]
    data[2] = level
    rs485_write(data)
    time.sleep(1)
    tmp = rs485_read(6)
    if tmp:
        if tmp[1] == '0x43' and tmp[2] == '0x0' and tmp[3] == '0x88' and tmp[4] == '0x4e':
            return True
        else:
            return False
    else:
        return False


# Get inlet tempurature
def get_inlet_temp():
    print("\033[1;32m\nGet inlet tempuratrue\033[0m")

    data = [67, 1, 0, 78]
    rs485_write(data)
    time.sleep(1)
    tmp = rs485_read(6)
    if tmp:
        if tmp[1] == '0x43' and tmp[2] == '0x1' and tmp[4] == '0x4e':
            return tmp[3]
        else:
            print(tmp)
            return None
    else:
        return None


# Get outlet tempurature
def get_outlet_temp():
    print("\033[1;32m\nGet outlet tempuratrue\033[0m")

    data = [67, 2, 0, 78]
    rs485_write(data)
    time.sleep(1)
    tmp = rs485_read(6)
    if tmp:
        if tmp[1] == '0x43' and tmp[2] == '0x2' and tmp[4] == '0x4e':
            return tmp[3]
        else:
            print(tmp)
            return None
    else:
        return None


def get_dry_room_temp1():
    data = [67, 3, 0, 78]
    rs485_write(data)
    time.sleep(1)
    tmp = rs485_read(6)
    if tmp:
        if tmp[1] == '0x43' and tmp[2] == '0x3' and tmp[4] == '0x4e':
            return tmp[3]
        else:
            print(tmp)
            return None
    else:
        return None


def get_dry_room_temp2():
    data = [67, 4, 0, 78]
    rs485_write(data)
    time.sleep(1)
    tmp = rs485_read(6)
    if tmp:
        if tmp[1] == '0x43' and tmp[2] == '0x4' and tmp[4] == '0x4e':
            return tmp[3]
        else:
            print(tmp)
            return None
    else:
        return None


# Get dry room tempurature1
def get_dry_room_temp(position):
    if position == 1 or position == 2:
        print("\033[1;32m\nGet dry room tempuratrue%d\033[0m" % position)
    else:
        print("\033[1;31m\nDry room position error\033[0m")
        sys.exit()

    if position == 1:
        return get_dry_room_temp1()
    elif position == 2:
        return get_dry_room_temp2()


if __name__ == '__main__':
    if not rs485_open():
        print("\033[1;31m\nOpen USB failed\033[0m")
        sys.exit()

    print(set_fan_speed(1))
    print(get_inlet_temp())
    print(get_outlet_temp())
    print(get_dry_room_temp(1))
    print(get_dry_room_temp(2))

    if not rs485_close():
        print("\033[1;31m\nFailed USB failed\033[0m")
        sys.exit()
