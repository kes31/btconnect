from xml.etree import ElementTree

import dbus


class DbusWrapper:

    def __init__(self, bluetooth_device):
        self._system_bus = dbus.SystemBus()
        self._bluetooth_device = bluetooth_device

    def _get_bluetooth_device_interface(self, device_name):
        proxy_object = self._system_bus.get_object('org.bluez',
                                                   '/org/bluez/{}/{}'.format(self._bluetooth_device, device_name))
        dbus_interface = dbus.Interface(proxy_object, 'org.bluez.Device1')

        return dbus_interface

    def connect_to_device_by_name(self, device_name):
        dbus_interface = self._get_bluetooth_device_interface(device_name)
        dbus_interface.Connect()

    def disconnect_from_device_by_name(self, device_name):
        dbus_interface = self._get_bluetooth_device_interface(device_name)
        dbus_interface.Disconnect()

    def _get_device_list(self):
        result = {}
        xml = self._system_bus.get_object('org.bluez', '/org/bluez/{}'.format(self._bluetooth_device)).Introspect(
            dbus_interface='org.freedesktop.DBus.Introspectable')
        for child in ElementTree.fromstring(xml):
            if child.tag == 'node':
                dev = self._system_bus.get_object('org.bluez',
                                                  '/org/bluez/{}/{}'.format(self._bluetooth_device,
                                                                            child.attrib['name']))
                interfaces = dbus.Interface(dev, 'org.freedesktop.DBus.Properties')
                props = interfaces.GetAll('org.bluez.Device1')
                result[str(props['Alias'])] = {
                    'address': str(props['Address']),
                    'attribute': str(child.attrib['name']),
                    'name': str(props['Name']),
                    'connected': bool(props['Connected'])
                }
        return result

    def get_device_list(self):
        result = {}

        device_list = self._get_device_list()
        for device_name in device_list.keys():
            device_info = device_list[device_name]
            result[device_name] = (device_info['address'], device_info['attribute'], device_info['name'])

        return result

    def get_connected_devices(self):
        result = {}

        device_list = self._get_device_list()
        for device_name in device_list.keys():
            device_info = device_list[device_name]
            if not device_info['connected']:
                continue

            result[device_name] = (device_info['address'], device_info['attribute'], device_info['name'])

        return result
