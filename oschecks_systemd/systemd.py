import dbus

DBUS_SYSTEMD_ID = 'org.freedesktop.systemd1'
DBUS_SYSTEMD_PATH = '/org/freedesktop/systemd1'

DBUS_PROP_ID = 'org.freedesktop.DBus.Properties'
DBUS_SYSTEMD_MANAGER_ID = '{}.Manager'.format(DBUS_SYSTEMD_ID)
DBUS_SYSTEMD_UNIT_ID = '{}.Unit'.format(DBUS_SYSTEMD_ID)

class Unit(object):
    def __init__(self, bus, path):
        self.bus = bus
        self.path = path
        self.proxy = self.bus.get_object(DBUS_SYSTEMD_ID, path)
        self.manager = dbus.Interface(self.proxy,
                                      dbus_interface=DBUS_SYSTEMD_UNIT_ID)

        self.properties = dbus.Interface(self.proxy,
                                         dbus_interface=DBUS_PROP_ID)

    def get(self, prop):
        return self.properties.Get(DBUS_SYSTEMD_UNIT_ID,
                                   prop)

class Systemd(object):
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.systemd = self.bus.get_object(DBUS_SYSTEMD_ID, DBUS_SYSTEMD_PATH)
        self.manager = dbus.Interface(self.systemd,
                                      dbus_interface=DBUS_SYSTEMD_MANAGER_ID)

    def get_unit(self, unit):
        path = self.manager.GetUnit(unit)
        return Unit(self.bus, path)

    def get_unit_file(self, unit):
        return str(self.manager.GetUnitFileState(unit))

if __name__ == '__main__':
    s = Systemd()
    u = s.get_unit('sshd.service')

