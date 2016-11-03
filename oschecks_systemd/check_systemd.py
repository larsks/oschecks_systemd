import dbus
from oschecks_systemd.systemd import Systemd
import oschecks.common as common


class SystemdCommand (common.CheckCommand):
    def take_action(self, parsed_args):
        self.systemd = Systemd()


class CheckUnitActive(SystemdCommand):
    def get_parser(self, prog_name):
        p = super(CheckUnitActive, self).get_parser(prog_name)
        p.add_argument('unit_name')
        return p

    def take_action(self, parsed_args):
        '''Check if the named unit is active.'''

        super(CheckUnitActive, self).take_action(parsed_args)

        try:
            res = self.systemd.get_unit(parsed_args.unit_name)
            state = res.get('ActiveState')
        except dbus.exceptions.DBusException:
            return (common.RET_CRIT,
                    'Failed to query unit {} status'.format(
                        parsed_args.unit_name))

        if state == 'failed':
            exitcode = common.RET_CRIT
            msg = 'Unit {} has failed'.format(parsed_args.unit_name)
        elif state == 'inactive':
            exitcode = common.RET_WARN
            msg = 'Unit {} is inactive'.format(parsed_args.unit_name)
        elif state == 'active':
            exitcode = common.RET_OKAY
            msg = 'Unit {} is active'.format(parsed_args.unit_name)
        else:
            exitcode = common.RET_WTF
            msg = 'Unit {} is in an unknown state'.format(parsed_args.unit_name)

        return (exitcode, msg)


class CheckUnitEnabled(SystemdCommand):
    def get_parser(self, prog_name):
        p = super(CheckUnitEnabled, self).get_parser(prog_name)
        p.add_argument('unit_name')
        return p

    def take_action(self, parsed_args):
        '''Check if the named unit is active.'''

        super(CheckUnitEnabled, self).take_action(parsed_args)

        try:
            state = self.systemd.get_unit_file(parsed_args.unit_name)
        except dbus.exceptions.DBusException:
            return (common.RET_CRIT,
                    'Failed to query unit {} status'.format(
                        parsed_args.unit_name))

        if state == 'enabled':
            exitcode = common.RET_OKAY
            msg = 'Unit {} is enabled'.format(parsed_args.unit_name)
        elif state == 'enabled-runtime':
            exitcode = common.RET_WARN
            msg = 'Unit {} is enabled temporarily'.format(parsed_args.unit_name)
        else:
            exitcode = common.RET_CRIT
            msg = 'Unit {} is not enabled'.format(parsed_args.unit_name)

        return (exitcode, msg)


class CheckUnitExists(SystemdCommand):
    def get_parser(self, prog_name):
        p = super(CheckUnitExists, self).get_parser(prog_name)
        p.add_argument('unit_name')
        return p

    def take_action(self, parsed_args):
        '''Check if the named unit exists.'''

        super(CheckUnitExists, self).take_action(parsed_args)

        try:
            state = self.systemd.get_unit_file(parsed_args.unit_name)
        except dbus.exceptions.DBusException:
            return (common.RET_CRIT,
                    'Failed to query unit {} status'.format(
                        parsed_args.unit_name))

        msg = 'Unit {} exists'.format(parsed_args.unit_name)

        return (common.RET_OKAY, msg)
