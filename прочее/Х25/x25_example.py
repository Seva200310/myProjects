import libscrc
byte_arr=bytearray( [0x57,0x2a,0x1] )
def calc_crc(byte_arr):
    crc16 = libscrc.x25(byte_arr)
    return (hex(crc16))
crc=calc_crc(byte_arr)
print(crc)

