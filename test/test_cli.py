import logging
import test
from os.path import join
from subprocess import PIPE, STDOUT, CalledProcessError, Popen, check_output
from test.agenda_items import Valid
from unittest import TestCase

from src.helpers import get_default_khalorg_format, get_module_path


class TestNew(TestCase):

    def setUp(self) -> None:
        self.test_dir: str = get_module_path(test)
        return super().setUp()

    def test_new_item(self):
        """
        When feeding the org file valid.org into khalorg_tester
        through stdin, it expected to get the command line arguments from
        stdout as is described by MaximalValid.khal_new_args.
        """
        expected: str = 'khal new ' + ' '.join(Valid.khal_new_args)
        org_file: str = join(
            self.test_dir,
            'static',
            'agenda_items',
            'valid.org')
        cli_tester: str = join(self.test_dir, 'khalorg_tester')

        cat_args: tuple = ('cat', org_file)
        cli_tester_args: tuple = (cli_tester, 'new', 'Some_calendar')
        try:
            stdout: bytes = self._pipe_subproccesses(cat_args, cli_tester_args)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            message: str = f'\n\n{stdout}\n\n{expected.encode()}'
            logging.debug(stdout)
            self.assertTrue(expected.encode() in stdout, msg=message)

    def _pipe_subproccesses(self, first: tuple, second: tuple) -> bytes:
        with Popen(first, stdout=PIPE) as cat:
            stdout: bytes = check_output(
                second,
                stdin=cat.stdout,
                stderr=STDOUT
            )
            cat.wait()
            return stdout


class TestParentParser(TestCase):

    def setUp(self) -> None:
        self.test_dir: str = get_module_path(test)
        return super().setUp()

    def test_with_args(self):
        """
        Expected that the khalorg_cli_tester executable return the
        calendar and the log level.
        """
        cli_tester: str = join(self.test_dir, 'khalorg_cli_tester')
        args: list = [
            cli_tester,
            '--loglevel',
            'CRITICAL',
            'new',
            'calendar']
        try:
            stdout: bytes = check_output(args)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            expected: bytes = b"loglevel='CRITICAL', until='', calendar='calendar'"
            message: str = f"\n\nstdout:\n{stdout}\n\nexpected:\n{expected}"
            self.assertTrue(expected in stdout, msg=message)


class TestListParser(TestCase):

    def setUp(self) -> None:
        logging.basicConfig(level='DEBUG')
        self.test_dir: str = get_module_path(test)
        return super().setUp()

    def test_with_args(self):
        """
        Expected that the khalorg_cli_tester executable return the
        calendar, the loglevel, the start time, and stop time.
        """
        default_format: str = get_default_khalorg_format()

        cli_tester: str = join(self.test_dir, 'khalorg_cli_tester')
        args: list = [
            cli_tester,
            '--loglevel',
            'CRITICAL',
            'list',
            '--format',
            default_format,
            'calendar',
            'today',
            '2d']
        try:
            stdout: bytes = check_output(args)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            expected: str = (
                f"loglevel='CRITICAL', format='{default_format}', "
                "calendar='calendar', start='today', stop='2d'")
            expected_bytes: bytes = expected.encode('unicode_escape')

            message: str = f"\n\n{stdout}\n\n{expected_bytes}"
            self.assertTrue(expected_bytes in stdout, msg=message)

    def test_with_args_and_format(self):
        """
        Expected that the khalorg_cli_tester executable return the
        calendar, the loglevel, the start time, and stop time.
        """
        cli_tester: str = join(self.test_dir, 'khalorg_cli_tester')
        args: list = [
            cli_tester,
            '--loglevel',
            'CRITICAL',
            'list',
            '--format',
            '{org-dates}',
            'calendar',
            'today',
            '2d']
        try:
            stdout: bytes = check_output(args)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            expected: str = ("loglevel='CRITICAL', format='{org-dates}', "
                             "calendar='calendar', start='today', stop='2d'")
            expected_bytes: bytes = expected.encode('unicode_escape')

            message: str = f"\n\nstdout:\n{stdout}\n\nexpected:\n{expected_bytes}"
            self.assertTrue(expected_bytes in stdout, msg=message)
