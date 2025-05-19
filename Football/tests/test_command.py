import os

from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from Football import models


class TestFeedTableCommandMixin:
    """Base test class for the "feed_table" custom commands."""

    def __init__(self, table_model, feed_table_command, original_file_path_constant_name, test_file):
        """Initialize the class."""

        self.table_model = table_model
        self.feed_table_command = feed_table_command
        self.original_file_path_constant_name = original_file_path_constant_name
        self.test_file_path = "/".join([os.getcwd(), "Football", "tests", "tests_data", test_file])

    def mixin_setup(self):
        """Initialize the context of each test."""

        self.model_count = self.table_model.objects.count()

    def test_command_fails(self):
        """Check if exception is handled when command fails."""

        # Arrange.
        with patch(
            f"Football.management.commands.{self.feed_table_command}.{self.original_file_path_constant_name}",
            "fake/file/path",
        ):
            # Act.
            call_command(self.feed_table_command)

        # Assert.
        self.assertEqual(self.model_count, self.table_model.objects.count())

    def test_command_succeeds(self):
        """Check if table is populated as expected when command succeeds."""

        # Arrange.
        with patch(
            f"Football.management.commands.{self.feed_table_command}.{self.original_file_path_constant_name}",
            self.test_file_path,
        ):
            # On insère d'abord les entraîneurs nécessaires à la création des équipes
            call_command("feed_table_entraineur")
            # Act.
            call_command(self.feed_table_command)

        # Assert.
        self.assertEqual(self.model_count + 1, self.table_model.objects.count())

    def test_command_with_flush_succeeds(self):
        """Check if table is populated as expected when command is called with flush option, and succeeds."""

        # Arrange.
        with patch(
            f"Football.management.commands.{self.feed_table_command}.{self.original_file_path_constant_name}",
            self.test_file_path,
        ):
            # On insère d'abord les entraîneurs nécessaires à la création des équipes
            call_command("feed_table_entraineur")
            # Act.
            call_command(self.feed_table_command, "--flush")

        # Assert.
        self.assertEqual(self.model_count + 1, self.table_model.objects.count())


@patch("Football.management.commands.feed_all_tables.call_command")
class TestFeedAllTables(TestCase):
    """Test class for custom feed_all_tables command."""

    def test_command(self, mock_call_command):
        """Check calling command runs all table feeding commands as expected."""

        call_command("feed_all_tables")

        # We can check only the last call of our mock object.
        mock_call_command.assert_called_with("feed_table_equipe")

    def test_command_flush(self, mock_call_command):
        """Check calling command with "--flush" argument runs all table feeding commands as expected."""

        call_command("feed_all_tables", "--flush")

        # We can check only the last call of our mock object.
        mock_call_command.assert_called_with("feed_table_equipe", "--flush")


class TestFeedTableEntraineurCommand(TestCase, TestFeedTableCommandMixin):
    """Test class for custom feed_table1dot1 command."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""

        TestCase.__init__(self, *args, **kwargs)
        TestFeedTableCommandMixin.__init__(
            self,
            table_model=models.Entraineur,
            feed_table_command="feed_table_entraineur",
            original_file_path_constant_name="TABLE_ENTRAINEUR_FILE_PATH",
            test_file="Entraineur_test.csv",
        )

        self.setUp = self.mixin_setup


class TestFeedTableJoueurCommand(TestCase, TestFeedTableCommandMixin):
    """Test class for custom feed_table1dot1 command."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""

        TestCase.__init__(self, *args, **kwargs)
        TestFeedTableCommandMixin.__init__(
            self,
            table_model=models.Joueur,
            feed_table_command="feed_table_joueur",
            original_file_path_constant_name="TABLE_JOUEUR_FILE_PATH",
            test_file="Joueur_test.csv",
        )

        self.setUp = self.mixin_setup


class TestFeedTableEquipeCommand(TestCase, TestFeedTableCommandMixin):
    """Test class for custom feed_table1dot1 command."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""

        TestCase.__init__(self, *args, **kwargs)
        TestFeedTableCommandMixin.__init__(
            self,
            table_model=models.Equipe,
            feed_table_command="feed_table_equipe",
            original_file_path_constant_name="TABLE_EQUIPE_FILE_PATH",
            test_file="Equipe_test.csv",
        )

        self.setUp = self.mixin_setup
