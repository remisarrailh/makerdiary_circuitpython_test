# CircuitPython NeoPixel Color Picker Example
import board
import pulseio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

led_red = pulseio.PWMOut(board.LED_RED, frequency=5000, duty_cycle=0)
led_green = pulseio.PWMOut(board.LED_GREEN, frequency=5000, duty_cycle=0)
led_blue = pulseio.PWMOut(board.LED_BLUE, frequency=5000, duty_cycle=0)

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            print(packet.color)
            led_red.duty_cycle = int(map(packet.color[0], 0, 255, 65535, 0))
            led_green.duty_cycle = int(map(packet.color[1], 0, 255, 65535, 0))
            led_blue.duty_cycle = int(map(packet.color[2], 0, 255, 65535, 0))

