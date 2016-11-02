import dbus
import click
from oschecks_systemd.systemd import Systemd
import oschecks.common as common

@click.group('systemd')
@click.pass_context
def cli(ctx):
    '''Health checks for systemd units.'''

    ctx.obj = Systemd()


@cli.command()
@click.argument('unit')
@click.pass_context
def check_unit_active(ctx, unit):
    '''Check if the named unit is active.'''
    try:
        res = ctx.obj.get_unit(unit)
        state = res.get('ActiveState')
    except dbus.exceptions.DBusException:
        raise common.ExitCritical('Failed to query unit {} status'.format(
            unit))

    if state == 'failed':
        raise common.ExitCritical('Unit {} has failed'.format(unit))
    elif state == 'inactive':
        raise common.ExitWarning('Unit {} is inactive'.format(unit))
    elif state == 'active':
        raise common.ExitOkay('Unit {} is active'.format(unit))
    else:
        raise common.ExitWTF('Unit {} is in an unknown state'.format(unit))


@cli.command()
@click.argument('unit')
@click.pass_context
def check_unit_enabled(ctx, unit):
    '''Check if the named unit is enabled.'''

    try:
        state = ctx.obj.get_unit_file(unit)
    except dbus.exceptions.DBusException:
        raise common.ExitCritical('Failed to query unit {} status'.format(
            unit))

    if state in ['enabled']:
        raise common.ExitOkay('Unit {} is enabled'.format(unit))
    elif state in ['enabled-runtime']:
        raise common.ExitWarning('Unit {} is enabled temporarily'.format(unit))
    else:
        raise common.ExitCritical('Unit {} is not enabled'.format(unit))


@cli.command()
@click.argument('unit')
@click.pass_context
def check_unit_exists(ctx, unit):
    '''Check if the named unit exists.'''

    try:
        state = ctx.obj.get_unit_file(unit)
    except dbus.exceptions.DBusException:
        raise common.ExitCritical('Failed to query unit {} status'.format(
            unit))

    raise common.ExitOkay('Unit {} exists'.format(unit))

