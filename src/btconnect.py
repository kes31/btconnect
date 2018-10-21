#!env python
import argparse

import dbus_wrapper


def parse_arguments():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', help="list of subcommands")

    sub_parser = subparsers.add_parser('connect', help='try to connect via bluetooth')
    sub_parser.add_argument('device', metavar='ALIAS', type=str,
                            help='alias of the device to connect to')

    sub_parser = subparsers.add_parser('disconnect', help='disconnect from device')
    sub_parser.add_argument('device', metavar='ALIAS', type=str,
                            help='alias of the device to connect to')

    parser.add_argument('-l', '--list', action="store_true", help="list paired devices")
    parser.add_argument('-c', '--get-connected', action="store_true", help="list connected devices")

    args = parser.parse_args()

    return args


def print_device_list(devices):
    if len(devices) <= 0:
        print('  None\n')
        return

    for key in devices.keys():
        print('  {:12s} --> {} {}'.format(key, devices[key][0], '({})'.format(devices[key][2])))
    print('\n')


if __name__ == '__main__':
    parsed_arguments = parse_arguments()
    devices = {}
    if parsed_arguments.list or parsed_arguments.command in ('connect', 'disconnect'):
        devices = dbus_wrapper.get_associated_devices()

    if parsed_arguments.list:
        print('registered devices:\n')
        print_device_list(devices)
    if parsed_arguments.get_connected:
        print('connected device:\n')
        connected_devices = dbus_wrapper.get_connected_devices()
        print_device_list(connected_devices)
    if parsed_arguments.command == 'connect':
        print('connecting: {}'.format(parsed_arguments.device))
        try:
            dbus_wrapper.connect_to_device_by_name(devices[parsed_arguments.device][1])
        except:
            print('could not connect to device')
            exit(1)
    elif parsed_arguments.command == 'disconnect':
        print('disconnecting: {}'.format(parsed_arguments.device))
        try:
            dbus_wrapper.disconnect_from_device_by_name(devices[parsed_arguments.device][1])
        except:
            print('could not disconnect from device')
            exit(1)
