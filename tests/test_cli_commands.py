"""
CLI Command Extensions for Flask
"""
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
from service import app
from service.common.cli_commands import db_create


class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = app.test_cli_runner()

    @patch('service.common.cli_commands.db')
    def test_db_create(self, db_mock):
        """It should call the db-create command"""
        db_mock.return_value = MagicMock()
        result = self.runner.invoke(db_create)
        self.assertEqual(result.exit_code, 0)
