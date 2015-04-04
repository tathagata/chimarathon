__author__ = 't'

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_render_static_files(self):
        pass

    def render_index_file(self):
        pass

    def test_write_static_file(self):
        pass

    def test_load_data(self):
        pass

    def test_csv_to_jinja(self):
        pass


if __name__ == '__main__':
    unittest.main()





