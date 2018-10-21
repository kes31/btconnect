from .DbusWrapper import DbusWrapper

_dbus_wrapper = DbusWrapper('hci0')


def connect_to_device_by_name(device_name):
    _dbus_wrapper.connect_to_device_by_name(device_name)


def disconnect_from_device_by_name(device_name):
    _dbus_wrapper.disconnect_from_device_by_name(device_name)


def get_associated_devices():
    return _dbus_wrapper.get_device_list()


def get_connected_devices():
    return _dbus_wrapper.get_connected_devices()
