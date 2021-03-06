# ----- Info ------------------------------------------------------------------

__author__ = 'Michael Montero <mcmontero@gmail.com>'

# ----- Imports ---------------------------------------------------------------

from tinyAPI.base.context import Context
from tinyAPI.base.exception import ContextException

import os
import tinyAPI
import unittest

# ----- Tests -----------------------------------------------------------------

class ContextTestCase(unittest.TestCase):

    def tearDown(self):
        try:
            del os.environ['APP_SERVER_ENV']
        except KeyError:
            pass

        Context().reset()

    def test_context_exceptions(self):
        try:
            Context().get_server_env()

            this.fail('Was able to get server environment even though one was '
                      + 'not set.')
        except ContextException as e:
            self.assertEqual(
                'could not find environment variable called "APP_SERVER_ENV"',
                e.get_message())

        os.environ['APP_SERVER_ENV'] = 'invalid'

        try:
            Context().get_server_env()

            this.fail('Was able to get server environment even though the '
                      + 'value that was set was invalid.')
        except ContextException as e:
            self.assertEqual(
                'application server environment "invalid" is not valid',
                e.get_message())

    def test_getting_server_env(self):
        os.environ['APP_SERVER_ENV'] = Context.LOCAL
        self.assertEqual(Context.LOCAL, Context().get_server_env())

    def test_server_env_local(self):
        os.environ['APP_SERVER_ENV'] = Context.LOCAL
        self.assertTrue(tinyAPI.env_local())

    def test_server_env_staging(self):
        os.environ['APP_SERVER_ENV'] = Context.STAGING
        self.assertTrue(tinyAPI.env_staging())

    def test_server_env_qa(self):
        os.environ['APP_SERVER_ENV'] = Context.QA
        self.assertTrue(tinyAPI.env_qa())

    def test_server_env_prod(self):
        os.environ['APP_SERVER_ENV'] = Context.PRODUCTION
        self.assertTrue(tinyAPI.env_prod())

    def test_server_env_not_prod(self):
        os.environ['APP_SERVER_ENV'] = Context.LOCAL
        self.assertTrue(tinyAPI.env_not_prod())

        Context().reset()

        os.environ['APP_SERVER_ENV'] = Context.STAGING
        self.assertTrue(tinyAPI.env_not_prod())

        Context().reset()

        os.environ['APP_SERVER_ENV'] = Context.QA
        self.assertTrue(tinyAPI.env_not_prod())

        Context().reset()

        os.environ['APP_SERVER_ENV'] = Context.PRODUCTION
        self.assertFalse(tinyAPI.env_not_prod())

    def test_cli(self):
        Context().set_cli()
        self.assertTrue(Context().is_cli())

    def test_web(self):
        Context().set_web()
        self.assertTrue(Context().is_web())

    def test_unit_test(self):
        Context().set_unit_test()
        self.assertTrue(Context().is_unit_test())

# ----- Main ------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
