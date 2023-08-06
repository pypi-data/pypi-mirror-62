"""Cloudformation module."""
import logging
import os
import re
import sys

import yaml

from . import RunwayModule, run_module_command
from ..util import change_dir

LOGGER = logging.getLogger('runway')


def ensure_stacker_compat_config(config_filename):
    """Ensure config file can be loaded by Stacker."""
    try:
        with open(config_filename, 'r') as stream:
            yaml.safe_load(stream)
    except yaml.constructor.ConstructorError as yaml_error:
        if yaml_error.problem.startswith(
                'could not determine a constructor for the tag \'!'):
            LOGGER.error('"%s" appears to be a CloudFormation template, '
                         'but is located in the top level of a module '
                         'alongside the CloudFormation config files (i.e. '
                         'the file or files indicating the stack names & '
                         'parameters). Please move the template to a '
                         'subdirectory.',
                         config_filename)
            sys.exit(1)


def gen_stacker_env_files(environment, region):
    """Generate possible Stacker environment filenames."""
    return [
        # Give preference to explicit environment-region files
        "%s-%s.env" % (environment, region),
        # Fallback to environment name only
        "%s.env" % environment
    ]


def get_stacker_env_file(path, environment, region):
    """Determine Stacker environment file name."""
    for name in gen_stacker_env_files(environment, region):
        if os.path.isfile(os.path.join(path, name)):
            return name
    return "%s-%s.env" % (environment, region)  # fallback to env & region


def make_stacker_cmd_string(args):
    """Generate stacker invocation script from command line arg list.

    This is the standard stacker invocation script, with the following changes:
    * Adding our explicit arguments to parse_args (instead of leaving it empty)
    * Overriding sys.argv

    """
    # This same code is duplicated in the base Runway command `run-stacker`
    return ("import sys;"
            "from runway.cfngin.logger import setup_logging;"
            "from runway.cfngin.commands import Stacker;"
            "sys.argv = ['stacker'] + {args};"
            "stacker = Stacker(setup_logging=setup_logging);"
            "args = stacker.parse_args({args});"
            "stacker.configure(args);args.run(args)".format(args=str(args)))


class CloudFormation(RunwayModule):
    """CloudFormation (Stacker) Runway Module."""

    def execute_stacker_cmd(self, cmd_list):
        """Run Stacker in child process."""
        if getattr(sys, 'frozen', False):
            # running in pyinstaller single-exe, so sys.executable will
            # be the all-in-one Runway binary
            executable_cmd_list = [sys.executable, 'run-stacker', '--']
            LOGGER.debug(
                "Stacker command being executed: runway-cli %s %s",
                ' '.join(executable_cmd_list[1:]),
                ' '.join(cmd_list)
            )
            run_module_command(
                cmd_list=executable_cmd_list + cmd_list,
                env_vars=self.context.env_vars
            )
        else:
            # traditional python execution
            stacker_cmd_str = make_stacker_cmd_string(cmd_list)
            executable_cmd_list = [sys.executable, '-c']
            LOGGER.debug(
                "Stacker command being executed: %s \"%s\"",
                ' '.join(executable_cmd_list),
                stacker_cmd_str
            )
            run_module_command(
                cmd_list=executable_cmd_list + [stacker_cmd_str],
                env_vars=self.context.env_vars
            )

    def run_stacker(self, command='diff'):  # pylint: disable=too-many-branches,too-many-locals
        """Process config files and run Stacker."""
        response = {'skipped_configs': False}
        stacker_cmd = [command, "--region=%s" % self.context.env_region]

        if command == 'destroy':
            stacker_cmd.append('--force')
        elif command == 'build':
            if 'CI' in self.context.env_vars:
                stacker_cmd.append('--recreate-failed')
            else:
                stacker_cmd.append('--interactive')

        if 'DEBUG' in self.context.env_vars:
            stacker_cmd.append('--verbose')  # Increase logging if requested

        stacker_env_file = get_stacker_env_file(self.path,
                                                self.context.env_name,
                                                self.context.env_region)
        stacker_env_file_present = os.path.isfile(
            os.path.join(self.path, stacker_env_file)
        )

        for key, val in self.options['parameters'].items():
            stacker_cmd.extend(['-e', "%s=%s" % (key, val)])

        if stacker_env_file_present:
            stacker_cmd.append(stacker_env_file)

        if not (stacker_env_file_present or self.options['environment']):
            response['skipped_configs'] = True
            LOGGER.info(
                "Skipping stacker %s; no environment "
                "file found for this environment/region "
                "(looking for one of \"%s\")",
                command,
                ', '.join(
                    gen_stacker_env_files(self.context.env_name,  # noqa
                                          self.context.env_region))  # noqa
            )
        else:
            with change_dir(self.path):
                # Iterate through any stacker yaml configs to deploy them in order
                # or destroy them in reverse order
                for _root, _dirs, files in os.walk(self.path):
                    sorted_files = sorted(files)
                    if command == 'destroy':
                        sorted_files = reversed(sorted_files)
                    for name in sorted_files:
                        if re.match(r"runway(\..*)?\.(yml|yaml)", name) or (
                                name.startswith('.') or
                                name == 'docker-compose.yml'):
                            # Hidden files (e.g. .gitlab-ci.yml), Runway configs,
                            # and docker-compose files definitely aren't stacker
                            # config files
                            continue
                        if os.path.splitext(name)[1] in ['.yaml', '.yml']:
                            ensure_stacker_compat_config(
                                os.path.join(self.path, name)
                            )
                            LOGGER.info("Running stacker %s on %s in region %s",
                                        command,
                                        name,
                                        self.context.env_region)
                            self.execute_stacker_cmd(stacker_cmd + [name])
                    break  # only need top level files
        return response

    def plan(self):
        """Run stacker diff."""
        self.run_stacker(command='diff')

    def deploy(self):
        """Run stacker build."""
        self.run_stacker(command='build')

    def destroy(self):
        """Run stacker destroy."""
        self.run_stacker(command='destroy')
