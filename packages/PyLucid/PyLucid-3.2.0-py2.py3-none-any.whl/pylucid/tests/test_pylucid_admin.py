
import subprocess
import unittest
from pathlib import Path

# PyLucid
import pylucid
from pylucid.admin_shell.path_helper import get_path_helper_instance
from pylucid.pylucid_boot import VerboseSubprocess




class TestPyLucidAdmin(unittest.TestCase):
    """
    Tests for pylucid/pylucid_admin.py
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.path_helper = get_path_helper_instance()

    def pylucid_admin_run(self, *args):
        args = ("pylucid_admin", ) + args
        try:
            return VerboseSubprocess(*args).verbose_output(check=False)
        except subprocess.CalledProcessError as err:
            self.fail("Subprocess error: %s" % err)

    def test_help(self):
        output = self.pylucid_admin_run("help")
        print(output)

        self.assertIn("pylucid_admin shell", output)
        self.assertIn("Available commands (type help <topic>):", output)

        self.assertIn("create_page_instance", output)
        self.assertIn("Create a PyLucid page instance.", output)

        self.assertIn("update_env", output)
        self.assertIn("Update all packages in virtualenv.", output)

        # If DocString is missing in do_<name>():
        self.assertNotIn("Undocumented", output)

    def test_unknown_command(self):
        output = self.pylucid_admin_run("foo bar is unknown ;)")
        print(output)

        self.assertIn("pylucid_admin shell", output)
        self.assertIn("*** Unknown command: 'foo bar is unknown ;)' ***", output)

    def test_path_helper(self):
        self.path_helper.print_path()
        self.path_helper.assert_all_path()

    @unittest.skipIf(get_path_helper_instance().normal_mode, "Only available in 'developer' mode.")
    def test_change_editable_address(self):
        """
        All test runs on Travis-CI install PyLucid as editable!
        See .travis.yml
        """
        self.assertFalse(self.path_helper.normal_mode)

        pylucid_src_path = self.path_helper.base.parent
        print("pylucid_src_path: %r" % pylucid_src_path)

        self.assertTrue(pylucid_src_path.is_dir())
        self.assertTrue(str(pylucid_src_path).endswith("/src/pylucid"))

        git_path = Path(pylucid_src_path, ".git")
        print("git_path: %r" % git_path)

        self.assertTrue(git_path.is_dir())

        # Needed while developing with github write access url ;)
        output = VerboseSubprocess(
            "git", "remote", "set-url", "origin", "https://github.com/jedie/PyLucid.git",
            cwd=str(pylucid_src_path)
        ).verbose_output(check=True)
        # print(output)

        # Check if change was ok:
        output = VerboseSubprocess(
            "git", "remote", "-v",
            cwd=str(pylucid_src_path)
        ).verbose_output(check=True)
        # print(output)
        self.assertIn("https://github.com/jedie/PyLucid.git", output)
        self.assertNotIn("git@github.com", output)

        output = self.pylucid_admin_run("change_editable_address")
        print(output)

        self.assertIn("git@github.com:jedie/PyLucid.git", output)
