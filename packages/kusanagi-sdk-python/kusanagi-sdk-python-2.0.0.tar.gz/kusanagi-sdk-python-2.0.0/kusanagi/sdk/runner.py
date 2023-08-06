# Python 3 SDK for the KUSANAGI(tm) framework (http://kusanagi.io)
# Copyright (c) 2016-2020 KUSANAGI S.L. All rights reserved.
#
# Distributed under the MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import asyncio
import functools
import inspect
import json
import logging
import os

import click
import kusanagi.payload
import zmq.asyncio

from ..errors import KusanagiError
from ..logging import disable_logging
from ..logging import setup_kusanagi_logging
from ..logging import SYSLOG_NUMERIC
from ..utils import EXIT_ERROR
from ..utils import EXIT_OK
from ..utils import install_uvevent_loop
from ..utils import ipc
from ..utils import RunContext
from ..utils import tcp

LOG = logging.getLogger(__name__)


def key_value_strings_callback(ctx, param, values):
    """Option callback to validate a list of key/value arguments.

    Converts 'NAME=VALUE' cli parameters to a dictionary.

    :rtype: dict

    """

    params = {}
    if not values:
        return params

    for value in values:
        parts = value.split('=', 1)
        if len(parts) != 2:
            raise click.BadParameter('Invalid parameter format')

        param_name, param_value = parts
        params[param_name] = param_value

    return params


def apply_cli_options(run_method):
    """Decorator to apply command line options to `run` method.

    Run is called after all command line options are parsed and validated.

    """

    @functools.wraps(run_method)
    def wrapper(self):
        # Create a command object to run the SDK component.
        # Component caller source file name is used as command name.
        caller_frame = inspect.getouterframes(inspect.currentframe())[2]
        self.source_file = caller_frame[1]
        command = click.command(name=self.source_file, help=self.help)

        # Run method is called when command line options are valid
        start_component = command(functools.partial(run_method, self))

        # Apply CLI options to command
        for option in self.get_argument_options():
            start_component = option(start_component)

        if not os.environ.get('TESTING'):
            # Run SDK component
            start_component()
        else:
            # Allow unit tests to properly parse CLI arguments
            return start_component

    return wrapper


class ComponentRunner(object):
    """Component runner.

    This class allows to isolate Component implementation details and
    keep the Component itself consisten with KUSANAGI SDK specifications.

    """

    def __init__(self, component, server_cls, help):
        """Constructor.

        :param component: The component to run.
        :type component: Component
        :param server_cls: Class for the component server.
        :param server_cls: ComponentServer
        :param help: Help text for the CLI command.
        :type help: str

        """

        self.__component = component
        self.__startup_callback = None
        self.__shutdown_callback = None
        self.__error_callback = None
        self._args = {}
        self.source_file = None
        self.loop = None
        self.callbacks = None
        self.server_cls = server_cls
        self.help = help

    @property
    def args(self):
        """Command line arguments.

        Command line arguments are initialized during `run`
        with the values used to run the component.

        :rtype: dict

        """

        return self._args

    @property
    def socket_name(self):
        """IPC socket name.

        :rtype: str

        """

        return self._args.get('socket') or self.get_default_socket_name()

    @property
    def tcp_port(self):
        """TCP port number.

        :rtype: str or None

        """

        return self._args.get('tcp')

    @property
    def name(self):
        """Component name.

        :rtype: str

        """

        return self._args['name']

    @property
    def version(self):
        """Component version.

        :rtype: str

        """

        return self._args['version']

    @property
    def component_type(self):
        """Component type.

        :rtype: str

        """

        return self._args['component']

    @property
    def debug(self):
        """Check if debug is enabled for current component.

        :rtype: bool

        """

        return self._args.get('debug', False)

    @property
    def compact_names(self):
        """Check if payloads should use compact names.

        :rtype: bool

        """

        return not self._args.get('disable_compact_names', False)

    def get_default_socket_name(self):
        """Get a default socket name to use when socket name is missing.

        :rtype: str

        """

        # Remove 'ipc://' from string to get socket name
        return ipc(self.component_type, self.name, self.version)[6:]

    def get_argument_options(self):
        """Get command line argument options.

        :rtype: list.

        """

        return [
            click.option(
                '-A', '--action',
                help=(
                    'Name of the action to call when request message '
                    'is given as JSON through stdin.'
                    ),
                ),
            click.option(
                '-c', '--component',
                type=click.Choice(['service', 'middleware']),
                help='Component type.',
                required=True,
                ),
            click.option(
                '-d', '--disable-compact-names',
                is_flag=True,
                help='Use full property names in payloads.',
                ),
            click.option(
                '-D', '--debug',
                is_flag=True,
                help='Enable component debug.',
                ),
            click.option(
                '-L', '--log-level',
                help=(
                    'Enable a logging using a numeric Syslog severity '
                    'value to set the level.'
                    ),
                type=click.IntRange(0, 7, clamp=True),
                ),
            click.option(
                '-n', '--name',
                required=True,
                help='Component name.',
                ),
            click.option(
                '-p', '--framework-version',
                required=True,
                help='KUSANAGI framework version.',
                ),
            click.option(
                '-s', '--socket',
                help='IPC socket name.',
                ),
            click.option(
                '-t', '--tcp',
                help='TCP port to use when IPC socket is not used.',
                type=click.INT,
                ),
            click.option(
                '-T', '--timeout',
                help='Process execution timeout per request in milliseconds.',
                type=click.INT,
                default=30000,
                ),
            click.option(
                '-v', '--version',
                required=True,
                help='Component version.',
                ),
            click.option(
                '-V', '--var',
                multiple=True,
                callback=key_value_strings_callback,
                help='Component variables.',
                ),
            ]

    def set_startup_callback(self, callback):
        """Set a callback to be run during startup.

        :param callback: A callback to run on startup.
        :type callback: function

        """

        self.__startup_callback = callback

    def set_shutdown_callback(self, callback):
        """Set a callback to be run during shutdown.

        :param callback: A callback to run on shutdown.
        :type callback: function

        """

        self.__shutdown_callback = callback

    def set_error_callback(self, callback):
        """Set a callback to be run on message callback errors.

        :param callback: A callback to run on message callback errors.
        :type callback: function

        """

        self.__error_callback = callback

    def set_callbacks(self, callbacks):
        """Set message callbacks for each component action.

        :params callbacks: Callbacks for each action.
        :type callbacks: dict

        """

        self.callbacks = callbacks

    @apply_cli_options
    def run(self, **kwargs):
        """Run SDK component server.

        Calling this method checks command line arguments before
        component server starts, and then blocks the caller script
        until component server finishes.

        """

        # Initialize component logging
        log_level = kwargs.get('log_level')
        if log_level in SYSLOG_NUMERIC:
            setup_kusanagi_logging(
                self.server_cls.get_type(),
                kwargs['name'],
                kwargs['version'],
                kwargs['framework_version'],
                SYSLOG_NUMERIC[log_level],
                )
        else:
            # No logs are printed when log-level is not available
            disable_logging()

        # Standard input is read only when action name is given
        message = {}
        if kwargs.get('action'):
            contents = click.get_text_stream('stdin', encoding='utf8').read()

            # Add JSON file contents to message
            try:
                message['payload'] = json.loads(contents)
            except:
                LOG.exception('Stdin input value is not valid JSON')
                os._exit(EXIT_ERROR)

            # Add action name to message
            message['action'] = kwargs['action']

        # Skip zeromq initialization when transport payload is given
        # as an input file in the CLI.
        if message:
            # Use standard event loop to run component server without zeromq
            self.loop = asyncio.get_event_loop()
        else:
            # Set zeromq event loop when component is run as server
            install_uvevent_loop()
            self.loop = zmq.asyncio.ZMQEventLoop()
            asyncio.set_event_loop(self.loop)

        self._args = kwargs

        # When compact mode is enabled use long payload field names
        if not self.compact_names:
            kusanagi.payload.DISABLE_FIELD_MAPPINGS = True

        # Create a run context
        ctx = RunContext(self.loop)

        # Create component server and run it as a task
        server = self.server_cls(
            self.callbacks,
            self.args,
            debug=self.debug,
            source_file=self.source_file,
            error_callback=self.__error_callback,
            )

        LOG.debug('Using PID: "%s"', os.getpid())

        if message:
            server_task = self.loop.create_task(server.process_input(message))
        else:
            # Create channel for TCP or IPC conections
            if self.tcp_port:
                channel = tcp('127.0.0.1:{}'.format(self.tcp_port))
            else:
                # Abstract domain unix socket
                channel = 'ipc://{}'.format(self.socket_name)

            server_task = self.loop.create_task(server.listen(channel))

        ctx.tasks.append(server_task)

        # By default exit successfully
        exit_code = EXIT_OK

        # Call startup callback
        if self.__startup_callback:
            LOG.info('Running startup callback ...')
            try:
                self.__startup_callback(self.__component)
            except:
                LOG.exception('Startup callback failed')
                LOG.error('Component failed')
                exit_code = EXIT_ERROR

        # Run component server
        if exit_code != EXIT_ERROR:
            try:
                self.loop.run_until_complete(ctx.run())
            except zmq.error.ZMQError as err:
                exit_code = EXIT_ERROR
                if err.errno == 98:
                    LOG.error('Address unavailable: "%s"', self.socket_name)
                else:
                    LOG.error(err.strerror)

                LOG.error('Component failed')
            except KusanagiError as err:
                exit_code = EXIT_ERROR
                LOG.error(err)
                LOG.error('Component failed')
            except Exception:
                exit_code = EXIT_ERROR
                LOG.exception('Component failed')
            finally:
                # Finally close the event loop
                self.loop.close()

        # Call shutdown callback
        if self.__shutdown_callback:
            LOG.info('Running shutdown callback ...')
            try:
                self.__shutdown_callback(self.__component)
            except:
                LOG.exception('Shutdown callback failed')
                LOG.error('Component failed')
                exit_code = EXIT_ERROR

        if exit_code == EXIT_OK:
            LOG.info('Operation complete')

        os._exit(exit_code)
