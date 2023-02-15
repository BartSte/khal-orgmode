import logging
import test
from os.path import join
from subprocess import PIPE, STDOUT, CalledProcessError, Popen, check_output
from test.static.agenda_items import MaximalValid
from unittest import TestCase

from src.helpers import get_module_path


class TestCLI(TestCase):

    def setUp(self) -> None:
        self.test_dir: str = get_module_path(test)
        return super().setUp()

    def test_with_args(self):
        """ Expected that the khalorg_cli_tester executable return the
        calendar and the log level.
        """
        cli_tester: str = join(self.test_dir, 'khalorg_cli_tester')
        args: list = [cli_tester, 'new', 'calendar', '--logging', 'CRITICAL']
        try:
            stdout: bytes = check_output(args, stderr=STDOUT)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            self.assertEqual(stdout, b'calendar\nCRITICAL\n')

    def test_new(self):
        """ When feeding the org file maximal_valid.org into khalorg_tester
        through stdin, it expected to get the command line arguments from
        stdout as is described by MaximalValid.khal_new_args.
        """
        expected: str = 'khal new ' + ' '.join(MaximalValid.khal_new_args)
        org_file: str = join(self.test_dir, 'static', 'agenda_items', 'maximal_valid.org')
        cli_tester: str = join(self.test_dir, 'khalorg_tester')

        cat_args: tuple = ('cat', org_file)
        cli_tester_args: tuple = (cli_tester,'new', 'Some_calendar')
        try:
            stdout: bytes = self._pipe_subproccesses(cat_args, cli_tester_args)
        except CalledProcessError as error:
            logging.critical(error.output.decode())
            self.fail(error.output.decode())
        else:
            message: str = f'\n\n{stdout}\n\n{expected.encode()}'
            self.assertEqual(stdout, expected.encode(), msg=message)

    def _pipe_subproccesses(self, first: tuple, second: tuple) -> bytes:
        with Popen(first, stdout=PIPE) as cat:
            stdout: bytes = check_output(second, stdin=cat.stdout, stderr=STDOUT)
            cat.wait()
            return stdout

