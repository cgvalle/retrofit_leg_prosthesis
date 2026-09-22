import os
from smbus2 import SMBus
from time import sleep

DEVICE_AS5600 = 0x36 # Default device I2C address
bus = SMBus(1)

ESTIRADA = 230
CONTRAIDA = 170
def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x

def normalizar(valor, cero, uno):
    return clamp((valor - cero) / (uno - cero))

def ReadRawAngle(): # Read angle (0-360 represented as 0-4096)
    read_bytes = bus.read_i2c_block_data(DEVICE_AS5600, 0x0C, 2)
    angle = (read_bytes[0]<<8) | read_bytes[1];
    # to degress
    raw_deg = angle * 360 / 4096

    # goes from 0 to 90 knee flexion. 0 is fully extended
    angle = normalizar(raw_deg, ESTIRADA, CONTRAIDA) * 90
    return raw_deg, angle


while True:
    os.system('clear')
    raw_deg, angle = ReadRawAngle()
    # Use raw_deg at full extension / full flexion to set ESTIRADA / CONTRAIDA in leg/models/motor_pid.py
    print(f"raw: {raw_deg:6.1f} deg   knee: {angle:5.1f} deg")
    sleep(0.1)
