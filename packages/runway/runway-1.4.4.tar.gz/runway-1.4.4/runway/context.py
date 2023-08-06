"""Runway context module."""
import logging
# needed for python2 cpu_count, can be replace with python3 os.cpu_count()
import multiprocessing
import os
import sys

LOGGER = logging.getLogger('runway')


def echo_detected_environment(env_name, env_vars):
    """Print a helper note about how the environment was determined."""
    env_override_name = 'DEPLOY_ENVIRONMENT'
    LOGGER.info("")
    if env_override_name in env_vars:
        LOGGER.info("Environment \"%s\" was determined from the %s environment variable.",
                    env_name,
                    env_override_name)
        LOGGER.info("If this is not correct, update "
                    "the value (or unset it to fall back to the name of "
                    "the current git branch or parent directory).")
    else:
        LOGGER.info("Environment \"%s\" was determined from the current "
                    "git branch or parent directory.",
                    env_name)
        LOGGER.info("If this is not the environment name, update the branch/folder name or "
                    "set an override value via the %s environment variable",
                    env_override_name)
    LOGGER.info("")


class Context(object):
    """Runway execution context."""

    env_override_name = 'DEPLOY_ENVIRONMENT'

    def __init__(self, env_name,  # pylint: disable=too-many-arguments
                 env_region, env_root, env_vars=None,
                 command=None):
        """Initialize base class."""
        self.env_name = env_name
        self.env_region = env_region
        self.env_root = env_root
        self.command = command
        self.env_vars = env_vars or os.environ.copy()
        self._env_name_from_env = bool(self.env_vars.get(self.env_override_name))

        self.echo_detected_environment()

        if not self._env_name_from_env:
            self.env_vars.update({'DEPLOY_ENVIRONMENT': self.env_name})

    @property
    def is_interactive(self):
        """Wether the user should be prompted or not.

        Determined by the existed of ``CI`` in the environment.

        Returns:
            bool

        """
        return not bool(self.env_vars.get('CI'))

    @property
    def is_noninteractive(self):
        """Wether the user should be prompted or not.

        Determined by the existed of ``CI`` in the environment.
        Inverse of ``is_interactive`` property.

        Returns:
            bool

        """
        return bool(self.env_vars.get('CI'))

    @property
    def is_python3(self):
        """Wether running in Python 3 or not.

        Used for Python compatability decisions.

        Returns:
            bool

        """
        return sys.version_info[0] > 2

    @property
    def max_concurrent_modules(self):
        """Max number of modules that can be deployed to concurrently.

        This property can be set by exporting ``RUNWAY_MAX_CONCURRENT_MODULES``.
        If no value is specified, ``min(61, os.cpu_count())`` is used.

        On Windows, this must be equal to or lower than ``61``.

        **IMPORTANT:** When using ``parallel_regions`` and ``child_modules``
        together, please consider the nature of their relationship when
        manually setting this value. (``parallel_regions * child_modules``)

        Returns:
            int: Value from environment variable or ``min(61, os.cpu_count())``

        """
        value = os.getenv('RUNWAY_MAX_CONCURRENT_MODULES')

        if value:
            return int(value)
        # TODO update to `os.cpu_count()` when dropping python2
        return min(61, multiprocessing.cpu_count())

    @property
    def max_concurrent_regions(self):
        """Max number of regions that can be deployed to concurrently.

        This property can be set by exporting ``RUNWAY_MAX_CONCURRENT_REGIONS``.
        If no value is specified, ``min(61, os.cpu_count())`` is used.

        On Windows, this must be equal to or lower than ``61``.

        **IMPORTANT:** When using ``parallel_regions`` and ``child_modules``
        together, please consider the nature of their relationship when
        manually setting this value. (``parallel_regions * child_modules``)

        Returns:
            int: Value from environment variable or ``min(61, os.cpu_count())``

        """
        value = os.getenv('RUNWAY_MAX_CONCURRENT_REGIONS')

        if value:
            return int(value)
        # TODO update to `os.cpu_count()` when dropping python2
        return min(61, multiprocessing.cpu_count())

    @property
    def use_concurrent(self):
        """Wether to use concurrent.futures or not.

        Noninteractive is required for concurrent execution to prevent weird
        user-input behavior.

        Python 3 is required because backported futures has issues with
        ProcessPoolExecutor.

        Returns:
            bool

        """
        if self.is_noninteractive and self.is_python3:
            return True
        return False

    def echo_detected_environment(self):
        """Print a helper note about how the environment was determined."""
        LOGGER.info("")
        if self._env_name_from_env:
            LOGGER.info("Environment \"%s\" was determined from the %s "
                        "environment variable.", self.env_name,
                        self.env_override_name)
            LOGGER.info("If this is not correct, update "
                        "the value (or unset it to fall back to the name of "
                        "the current git branch or parent directory).")
        else:
            LOGGER.info("Environment \"%s\" was determined from the current "
                        "git branch or parent directory.",
                        self.env_name)
            LOGGER.info("If this is not the environment name, update the "
                        "branch/folder name or set an override value via "
                        "the %s environment variable", self.env_override_name)
        LOGGER.info("")

    def save_existing_iam_env_vars(self):
        """Backup IAM environment variables for later restoration."""
        for i in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                  'AWS_SESSION_TOKEN']:
            if i in self.env_vars:
                self.env_vars['OLD_' + i] = self.env_vars[i]

    def restore_existing_iam_env_vars(self):
        """Restore backed up IAM environment variables."""
        for i in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                  'AWS_SESSION_TOKEN']:
            if 'OLD_' + i in self.env_vars:
                self.env_vars[i] = self.env_vars['OLD_' + i]
            elif i in self.env_vars:
                self.env_vars.pop(i)
