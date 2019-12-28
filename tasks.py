# -*- coding: utf-8 -*-
# ############################################################################
#
#    Copyright Eezee-It (C) 2016
#    Author: Eezee-It <info@eezee-it.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import os
import shutil

from os.path import normpath, basename
from colorama import init, Fore, Style
from invoke import task

init()
# Utility task(s)


@task
def clean(c, database_name=''):
    info('• Cleaning Database')
    c.run("dropdb %s --if-exists" % _get_database_name(c, database_name))

    info('• Cleaning coverage data')
    if os.path.exists('.coverage'):
        os.remove('.coverage')

    if os.path.exists('htmlcov'):
        shutil.rmtree('htmlcov')


def info(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


def warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)


def debug(message):
    print(Fore.MAGENTA + message + Style.RESET_ALL)

# Linter task(s)


@task
def lint_flake8(c, addons=''):
    info('• Flake8')
    paths = ['.']

    if addons:
        paths = _find_addons_path(c, addons.split(','))

    for path in paths:
        command = "flake8 %s --config=.flakerc" % path
        if c.debug:
            debug(command)

        c.run(command)


@task
def lint_odoo_lint(c, addons=''):
    info('• pyLinter')

    if addons:
        addons = _find_addons_path(c, addons.split(','))
    else:
        addons = _find_addons_path(c, _get_odoo_addons(c))

    command = "pylint --errors-only --load-plugins=pylint_odoo -d all -e odoolint" + \
        " %s --disable=%s "

    if c.debug:
        debug('Addon list')
        debug(str(addons))

    for addon in addons:
        addon_name = basename(normpath(addon))
        info("Pylint check addon: %s" % addon_name)
        if c.debug:
            debug(command % (addon, c.odoo_lint_disable))

        c.run(command % (addon, c.odoo_lint_disable))


@task
def lint_xml(c, addons=''):
    info('• XMl Linter')
    c.run('find . -maxdepth 4 -type f -iname "*.xml" '
          '| xargs -I \'{}\' xmllint -noout \'{}\'')


@task()
def lint(c, addons=''):
    lint_xml(c, addons)
    lint_flake8(c, addons)
    lint_odoo_lint(c, addons)

# Unit tests task(s)


@task()
def unittest(c, with_coverage=False, addons='', build=False,
             database_name=''):
    info('• Unittest')

    if not addons:
        addons = ",".join(_get_odoo_addons(c))

    if not with_coverage:
        with_coverage = c.with_coverage

    if build:
        clean(c, database_name)
        _prepare_odoo(c, addons, database_name)

    info('• Launch test(s)')

    command = _unittest_odoo_command(c, addons, database_name)

    if with_coverage:
        _run_coverage(c, command)

    else:
        c.run(command)


@task()
def test(c, with_coverage=False, addons='', build=False, database_name=''):
    lint(c, addons)
    unittest(c, with_coverage, addons, build, database_name)


def _unittest_odoo_command(c, addons, database_name):

    command = _get_odoo_base_command(c, database_name)
    command += " --test-enable --log-level=%s" % c.test_log_level
    command += " --workers=0 --smtp=nosmtp"
    command += "%s" % _get_lang_handler_command_arg(c)
    command += " --stop-after-init -u %s" % addons

    if c.debug:
        debug("Unittest Command")
        debug(command)
    return command


def _get_lang_handler_command_arg(c):
    command_arg = ''
    log_handlers = c.test_log_handlers.split(",")
    for handler in log_handlers:
        command_arg += " --log-handler=%s " % handler
    return command_arg
# Debug tasks


@task()
def show_addons(c, addons=''):
    if not addons:
        addons = _get_odoo_addons(c)

    for addon in addons:
        print(addon)


@task()
def show_addons_directories(c, addons=''):
    _get_addons_from_directories(c, c.custom_addons_directories, debug=True)


def _prepare_odoo(c, addons, database_name):
    info('    • Preparing Odoo for test')
    command = _get_odoo_base_command(c, database_name)
    command += " --log-level=error --log-handler=odoo.modules.loading:INFO "
    command += "--workers=0 --smtp=nosmtp"
    command += " --stop-after-init -i %s" % addons
    c.run(command)


def _run_coverage(c, odoo_command):
    command = "coverage run %s && coverage html && coverage report -i " % odoo_command
    c.run(command)


def _get_odoo_base_command(c, database_name=''):
    if c.debug:
        debug("Addons path")
        debug(_get_addons_path(c))

    if c.debug and c.odoo_languages:
        debug("Lang to install:")
        debug(",".join(c.odoo_languages))

    languages_command = ''
    if c.odoo_languages:
        languages_command = '--load-language=%s' % (",".join(c.odoo_languages))
    db = _get_database_name(c, database_name)
    db_command = "-d %s --db-filter %s" % (db, db)
    odoo_base_command = "%s/odoo-bin --addons-path=%s %s %s" % (
        c.odoo_bin_directory, _get_addons_path(c), db_command,
        languages_command)

    if c.debug:
        debug("Odoo base command")
        debug(odoo_base_command)
    return odoo_base_command


def _get_database_name(c, database_name=''):
    if database_name:
        return database_name

    return c.database_name


def _get_odoo_addons(c):
    addons = []

    if c.custom_addons:
        addons += c.custom_addons

    if c.custom_addons_directories:
        addons += _get_addons_from_directories(c, c.custom_addons_directories)

    return addons


def _get_addons_from_directories(c, directories):

    addons = []
    for directory in directories:
        if c.debug:
            debug("Directory to fetch Odoo addons")
            debug(directory)
        addons += _get_addons_from_directory(get_project_base(c) + directory)
    return addons


def _get_addons_from_directory(directory):
    addons = []
    for item in os.listdir(directory):
        if not os.path.isfile(directory + "/" + item) and not item[0] == '.':
            addons.append(item)

    return addons


def _get_addons_path(c):
    if not c.custom_addons_directories:
        return []

    addons_path = []

    for addon_directory in c.odoo_addons_directories:
        addons_path.append(get_project_base(c) + addon_directory)

    for addon_directory in c.custom_addons_directories:
        addons_path.append(get_project_base(c) + addon_directory)

    return ",".join(addons_path)


def _find_addons_path(c, addons):

    addons_path = []
    for addon in addons:
        addons_path.append(_find_addon_path(c, addon))
    return addons_path


def _find_addon_path(c, addon):
    directories = _get_addons_path(c).split(',')
    for directory in directories:
        if not os.path.exists(directory):
            warning("Directory %s doesn\'t exists!" % directory)
            continue

        if not os.path.isdir(directory):
            warning("Directory %s is not a directory!" % directory)
            continue

        for item in os.listdir(directory):
            if item == addon:
                return directory + '/' + addon

    raise Exception("Module %s not found!" % addon)


def get_project_base(c):
    return os.getcwd() + c.odoo_bin_relative_path

# ns = Collection(clean, lint_flake8, lint_odoo_lint, lint_xml, lint, unittest,
#                 show_addons, show_addons_directories)
# ns.configure({'sphinx': {'target': "docs/_build"}})
