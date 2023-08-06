# Python 3 SDK for the KUSANAGI(tm) framework (http://kusanagi.io)
# Copyright (c) 2016-2020 KUSANAGI S.L. All rights reserved.
#
# Distributed under the MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from .component import Component
from .runner import ComponentRunner
from ..service import ServiceServer


class Service(Component):
    """KUSANAGI SDK Service component."""

    def __init__(self):
        super().__init__()
        # Create a component runner for the service server
        help = 'Service component action to process application logic'
        self._runner = ComponentRunner(self, ServiceServer, help)

    def action(self, name, callback):
        """Set a callback for an action.

        :param name: Service action name.
        :type name: str
        :param callback: Callback to handle action calls.
        :type callback: callable

        """

        self._callbacks[name] = callback


def get_component():
    """Get global Service component instance.

    :rtype: Service

    """

    return Service.instance
