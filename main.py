import pysine
import sys
import os
import binascii
from bitstring import BitArray
from alive_progress import alive_bar

FREQUENCIES = [
    400,
    600,
    800,
    1000,
    1200,
    1400,
    1600,
    1800
]

OUTPUT = []
TIME = 0.1
TIME = float(sys.argv[2])

def ConvertByte(byte):
    global OUTPUT

    hex_string = str(binascii.hexlify(byte)).split("'")[1]
    bin_string = BitArray(hex=hex_string).bin

    for i in range(0, 8):
        if bin_string[i] == '0':
            OUTPUT.append(0)
        else:
            OUTPUT.append(FREQUENCIES[i])
    return

head = '''Python Audio/Data Converter
Mitchell Blaser, 2021.
github.com/mitchellblaser
'''
print(head)

TARGET = sys.argv[1]
FILESIZE = os.path.getsize(TARGET)

print("Input File:     " + TARGET)
print("File Size:      " + str(FILESIZE) + " bytes.")
print("Estimated Time: " + str(FILESIZE*8*TIME) + " seconds.")
print("")
c = input("Continue? (y/n): ")
if c == "n":
    exit()

print("")
print("Reading File...")

with alive_bar(FILESIZE) as bar:
    FILE = open(TARGET, "rb")
    BYTE = FILE.read(1)
    while BYTE:
        ConvertByte(BYTE)
        BYTE = FILE.read(1)
        bar()
    FILE.close()
print("")
print("Playing Output...")
with alive_bar(len(OUTPUT)) as bar:
    for i in range(0, len(OUTPUT)):
        pysine.sine(frequency=OUTPUT[i], duration=TIME)
        bar()
print("")