from charms.reactive import (
    clear_flag,
    set_flag,
    when,
    when_not,
)
from charmhelpers.contrib.python.packages import pip_install
from charmhelpers.core import (
    hookenv,
)
from charmhelpers.core.hookenv import (
    charm_dir,
    charm_name,
    close_port,
    config,
    open_port,
    status_set,
    log,
)
from charmhelpers.core.host import (
    service_restart,
    service_start,
    service_stop,
)

from jinja2 import Template


@when_not('cherrypy-helloworld.installed')
def install_cherrypy_helloworld():
    """Install the cherrypy helloworld service."""
    # Install dependencies for our helloworld service
    for pkg in ['CherryPy', 'jinja2']:
        pip_install(pkg)

    # When we first run, generate the systemd service file
    with open('{}/templates/helloworld.service.j2'.format(charm_dir())) as f:
        t = Template(f.read())

        # Render the new configuration
        rendered = t.render(
            charm_dir=charm_dir(),
        )

        status_set('maintenance', 'Creating helloworld service...')
        service_file = "/etc/systemd/system/{}.service".format(charm_name())
        with open(service_file, "w") as svc:
            svc.write(rendered)

        # Render the initial configuration
        render_config()

        status_set('maintenance', 'Starting helloworld service...')
        service_start(charm_name())

        # Make sure the port is open
        update_http_port()

        status_set('active', 'Ready!')

    set_flag('cherrypy-helloworld.installed')


@when('config.changed.http-port')
def update_http_port():
    """Change the exposed http port.

    If the http port has changed, make sure the previous port is unexposed
    and expose the new port.
    """
    cfg = config()
    old_port = cfg.previous('http-port')
    if old_port and int(old_port) > 0:
        close_port(old_port)

    # Open the port for our service
    open_port(cfg['http-port'])


@when('config.changed')
def config_changed():
    """Update the helloworld configuration and restart the service."""
    render_config()
    set_flag('helloworld.restart')


def render_config():
    """Render the cherrypy configuration."""
    with open('{}/templates/helloworld.cfg.j2'.format(charm_dir())) as f:
        t = Template(f.read())

        # Render the new configuration
        rendered = t.render(
            http_port=config('http-port'),
        )
        conf_file = "{}/helloworld/helloworld.conf".format(charm_dir())
        with open(conf_file, "w") as svc:
            svc.write(rendered)


@when('helloworld.restart')
def restart_service():
    """Restart the helloworld service."""
    status_set('maintenance', 'Restarting helloworld service...')
    service_restart(charm_name())
    status_set('active', 'Ready!')

    clear_flag('helloworld.restart')
