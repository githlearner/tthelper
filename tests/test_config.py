import unittest
from flask_testing import TestCase

from manage import app


class TestDevConfig(TestCase):
    def create_app(self):
        app.config.from_object("main.config.DevConfig")
        return app

    def test_app_is_dev(self):
        self.assertTrue(
            app.config["SECRET_KEY"], "e82b9cda-db62-44ec-b6b2-b5b14de697dd"
        )

    def test_debug_flag(self):
        self.assertTrue(app.config["DEBUG"], True)


if __name__ == "__main__":
    unittest.main()
