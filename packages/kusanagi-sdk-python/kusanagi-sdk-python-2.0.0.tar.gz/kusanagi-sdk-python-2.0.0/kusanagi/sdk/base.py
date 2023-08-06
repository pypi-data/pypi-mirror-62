# Python 3 SDK for the KUSANAGI(tm) framework (http://kusanagi.io)
# Copyright (c) 2016-2020 KUSANAGI S.L. All rights reserved.
#
# Distributed under the MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from .schema.service import ServiceSchema
from ..errors import KusanagiError
from ..logging import INFO
from ..logging import value_to_log_string
from ..schema import get_schema_registry
from ..versions import VersionString


class ApiError(KusanagiError):
    """Exception class for API errors."""


class Api(object):
    """Base API class for SDK components."""

    def __init__(self, component, path, name, version, framework_version, **kw):
        self.__path = path
        self.__name = name
        self.__version = version
        self.__framework_version = framework_version
        self.__variables = kw.get('variables') or {}
        self.__debug = kw.get('debug', False)
        self._registry = get_schema_registry()
        self._component = component
        # Logger must be initialized by child classes
        self._logger = None

    def is_debug(self):
        """Determine if component is running in debug mode.

        :rtype: bool

        """

        return self.__debug

    def get_framework_version(self):
        """Get KUSANAGI framework version.

        :rtype: str

        """

        return self.__framework_version

    def get_path(self):
        """Get source file path.

        Returns the path to the endpoint userland source file.

        :returns: Source path file.
        :rtype: str

        """

        return self.__path

    def get_name(self):
        """Get component name.

        :rtype: str

        """

        return self.__name

    def get_version(self):
        """Get component version.

        :rtype: str

        """

        return self.__version

    def has_variable(self, name):
        """Checks if a variable exists.

        :param name: Variable name.
        :type name: str

        :rtype: bool

        """

        return name in self.__variables

    def get_variables(self):
        """Gets all component variables.

        :rtype: dict

        """

        return self.__variables

    def get_variable(self, name):
        """Get a single component variable.

        :param name: Variable name.
        :type name: str

        :rtype: str

        """

        return self.__variables.get(name, '')

    def has_resource(self, name):
        """Check if a resource name exist.

        :param name: Name of the resource.
        :type name: str

        :rtype: bool

        """

        return self._component.has_resource(name)

    def get_resource(self, name):
        """Get a resource.

        :param name: Name of the resource.
        :type name: str

        :raises: ComponentError

        :rtype: object

        """

        return self._component.get_resource(name)

    def get_services(self):
        """Get service names and versions.

        :rtype: list

        """

        services = []
        for name in self._registry.get_service_names():
            for version in self._registry.get(name).keys():
                services.append({'name': name, 'version': version})

        return services

    def get_service_schema(self, name, version):
        """Get service schema.

        Service version string may contain many `*` that will be
        resolved to the higher version available. For example: `1.*.*`.

        :param name: Service name.
        :type name: str
        :param version: Service version string.
        :type version: str

        :raises: ApiError

        :rtype: ServiceSchema

        """

        # Resolve service version when wildcards are used
        if '*' in version:
            try:
                version = VersionString(version).resolve(
                    self._registry.get(name, {}).keys()
                    )
                # NOTE: Space is uses ad separator because service names allow
                #       any character except spaces, \t or \n.
                path = '{} {}'.format(name, version)
                payload = self._registry.get(path, None, delimiter=" ")
            except KusanagiError:
                payload = None
        else:
            path = '{} {}'.format(name, version)
            payload = self._registry.get(path, None, delimiter=" ")

        if not payload:
            error = 'Cannot resolve schema for Service: "{}" ({})'
            raise ApiError(error.format(name, version))

        return ServiceSchema(name, version, payload)

    def log(self, value, level=INFO):
        """Write a value to KUSANAGI logs.

        Given value is converted to string before being logged.

        Output is truncated to have a maximum of 100000 characters.

        """

        if self._logger:
            self._logger.log(level, value_to_log_string(value))

    def done(self):
        """This is a dummy method that only raises an exception.

        It is implemented to comply with KUSANAGI SDK specifications.

        :raises: ApiError

        """

        msg = 'SDK does not support async call to end action: Api.done()'
        raise ApiError(msg)
