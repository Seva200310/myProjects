import libscrc
def calc_crc(byte_arr):
    crc16 = libscrc.x25(byte_arr)
    return (hex(crc16))


