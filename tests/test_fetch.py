import unittest
import pdb
import sys
from mock import mock_open, patch, Mock

from referralmanager.cli.fetch import fetch, download_files, setup_local_dir, recursive_list, get_login_details
from referralmanager.cli.base import base

from click.testing import CliRunner

class TestFetch(unittest.TestCase):
    # Just test that the "base" click function can be run without producing an error:
    @patch('referralmanager.cli.base.raven')
    def test_base(self, mock_raven):
        # Mock the raven Client class constructor:
        mock_raven.Client = Mock()

        # Create mock objects to be passed as arguments to base:
        with patch('referralmanager.cli.base.open', mock_open(read_data='{"public_key":"na", "secret":"na", "project":"na"}'), create=True):
            runner = CliRunner()
            result = runner.invoke(base, ["--sentry-login", "dummyFilename.txt", "--loglevel", "INFO", "fetch", "--help"])
            self.assertEqual(result.exit_code, 0)

    def test_get_login_details_real_file(self):
        with patch('test_fetch.open', mock_open(read_data='{"username":"testuser", "password":"testpassword"}'), create=True):
            with open('FakeFile.txt') as test_file:
                (username, password) = get_login_details(test_file)
                self.assertEqual(username, "testuser")
                self.assertEqual(password, "testpassword")

    def test_get_login_details_broken_file(self):
        with patch('test_fetch.open', mock_open(read_data='{"username":"testuser"}'), create=True):
            with open('FakeFile.txt') as test_file:
                self.assertRaises(Exception, lambda: get_login_details(test_file))

#    def test_recursive_list(self):
#        # XXX FIXME: I do not know how to mock the "walktree" method. Perhaps I need to use the "side_effect"
#        # argument of "patch()" or "mock()" somehow? It's a tricky case as the user sends callbacks to the
#        # method and in my case walktree has an effect by modifying a list in those callbacks - so it's not a
#        # simple matter of obtaining a return value.
#        with patch("pysftp.Connection") as mock_connection:
#            with pysftp.Connection("1.2.3.4", "user", "pwd", 12345) as sftp:
#                #sftp.walktree = Mock(side_effect=)
#                sftp.get("filename")
#        mock_connection.assert_called_with("1.2.3.4", "user", "pwd", 12345)
#        sftp.get.assert_called_with("filename")

    # XXX FIXME: Need to add more tests for setup_local_dir once I figure out how to deal with
    # the case of a directory not existing when it should - e.g. should we expect and exception
    # in this case and if so what type?

    @patch('referralmanager.cli.fetch.os.path')
    @patch('referralmanager.cli.fetch.os')
    def test_setup_local_dir(self, mock_os, mock_os_path):
        def curr_side_effect(arg):
            return arg

        mock_os_path.exists = Mock()
        mock_os_path.exists.side_effect = [True, True, False]

        mock_os_path.join = Mock()
        mock_os_path.join.side_effect = ["testdir/csv", "testdir/pdf"]

        mock_os.mkdir = Mock()

        (csv_dir, pdf_dir) = setup_local_dir("testdir")

        self.assertEqual(csv_dir, "testdir/csv")
        self.assertEqual(pdf_dir, "testdir/pdf")

        # FIXME: When I figure out how, I should also add assertions on the call outcomes
        # of mock_os_path.exists

    # XXX FIXME: I need to test the "download_files" function. However, I do not know how
    # to test the outcome of this function. The outcome is a "side effect" of
    # sftp.Connection.get(), as a specified set of files are downloaded and should exist
    # locally once the function has run. This seems kind of complicated so I'm not sure
    # how to do it with mocking objects yet.
#    @patch('referralmanager.cli.fetch.pysftp.Connection')
#    def test_download_files(self, mock_conn):
#        mock_conn.get = Mock()
#        mock_conn.get.return_value =

    # XXX FIXME: A fetch unit test will look vaguely like this - rethink this if/when I
    # one day understand unit testing and mock objects better:
#    @patch("referralmanager.cli.fetch.pysftp.Connection")
#    @patch('referralmanager.cli.fetch.os.path')
#    @patch('referralmanager.cli.fetch.os')
#    def test_fetch(self, mock_os, mock_os_path, mock_conn):
#        with patch('test_fetch.open', mock_open(read_data='{"username":"testuser", "password":"testpassword"}'),
#                   create=True):
#            mock_conn.get = Mock()
#            mock_conn.walktree = Mock()
#            mock_os.mkdir = Mock()
#            mock_os_path.exists = Mock()
#            mock_os_path.exists.return_value = True
#            mock_os_path.join = Mock()
#            mock_os_path.join.side_effect = ["test_local_dir/csv", "test_local_dir/pdf"]
#
#            fetch("dummy_login_file.txt", "test_local_dir", "test_remote_dir")
#            mock_conn.get.assert_called_with('kundftp.biobank.ki.se', username="testuser",
#                                             password="testpassword")
