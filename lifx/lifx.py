from .enums import *
from .packet import *
from .network import Network
from .light import Light

# Wraps network providing a simpler API.
class Lifx:

    network = Network()

    def __init__(self):
        pass

    def on(self):
        self.set_on(True)

    def off(self):
        self.set_on(False)

    def set_on(self, on):
        self.network.send(PacketType.SET_POWER_STATE, Power.ON if on else Power.OFF)

    def is_on(self):
        self.network.send(PacketType.GET_POWER_STATE)
        header, payload = self.network.listen_sync(PacketType.POWER_STATE, 100).get_data()

        if payload is not None:
            return payload.onoff 
        return None

    def set_colour(self, hue, saturation = 30000, brightness = 30000, kelvin = 1000, duration = 500):
        self.network.send(PacketType.SET_LIGHT_COLOUR, 0, hue, saturation, brightness, kelvin, duration)

    def get_colours(self):
        self.network.send(PacketType.GET_LIGHT_STATE)
        header, payload = self.network.listen_sync(PacketType.LIGHT_STATUS, 100).get_data()

        if payload is not None:
            return payload.hue, payload.saturation, payload.brightness, payload.kelvin, payload.dim, payload.power, payload.build_label, payload.tags
        return None, None, None, None, None, None, None, None

    def get_wifi_info(self):
        self.network.send(PacketType.GET_WIFI_INFO)
        header, payload = self.network.listen_sync(PacketType.WIFI_INFO, 100).get_data()

        if payload is not None:
            return payload.signal, payload.tx, payload.rx, payload.mcu_temperature 
        return None, None, None, None

    def get_labels(self):
        self.network.send(PacketType.GET_BULB_LABEL)
        header, payload = self.network.listen_sync(PacketType.BULB_LABEL, 100).get_data()

        if payload is not None:
            return payload.label.decode("utf-8")
        return None

    def get_access_points(self):
        self.network.send(PacketType.GET_ACCESS_POINTS)
        header, payload = self.network.listen_sync(PacketType.ACCESS_POINT, 100).get_data()

        if payload is not None:
            return payload.interface, payload.ssid.split(b'\0',1)[0].decode("utf-8"), payload.security_protocol, payload.strength, payload.channel
        return None, None, None, None, None

    def get_time(self):
        self.network.send(PacketType.GET_TIME)
        header, payload = self.network.listen_sync(PacketType.TIME_STATE, 100).get_data()

        if payload is not None:
            return payload.time / 1000000000
        return None

    def get_version(self):
        self.network.send(PacketType.GET_VERSION)
        header, payload = self.network.listen_sync(PacketType.VERSION_STATE, 100).get_data()

        if payload is not None:
            return payload.vendor, payload.product, payload.version
        return None, None, None

    def reboot(self):
        self.network.send(PacketType.REBOOT)

    # Get the wrapped network object to perform lower level calls
    def get_network(self):
        return network 

    # Monitors packets calling func when packet received
    def monitor(self, func):
        self.network.listen_async(func)

    def print_packet(self, packet):
        if packet is None:
            print('Packet could not be parsed.\n')
        else:
            print(str(packet) + '\n')


