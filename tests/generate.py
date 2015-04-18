__author__ = 't'

import unittest
from app.generate import render_index_page, write_templates_to_file
from mock import patch


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.all_data_list = ['3/25/2015 0:33:55', 'TestFirst', 'TestLast',
                             'TestAddress', 'TestCity', 'TestState', 'TestZip',
                             'TestCell', '03/15/2015', 'Male','TestTshirtSize', 'TestReasonForAsha'
                             'email@id', 'channelid']

        self.all_data_list_without_channelid = ['3/25/2015 0:33:55', 'TestFirst', 'TestLast',
                             'TestAddress', 'TestCity', 'TestState', 'TestZip',
                             'TestCell', '03/15/2015', 'Male','TestTshirtSize', 'TestReasonForAsha'
                             'email@id', None]
        self.runners_data_list_with_channelid = [('TestFirst TestLast', 'users/TestFirstTestLast/profile.html')]
        self.runners_data_list_without_channelid = [('TestFirst1 TestLast1', 'users/TestFirst1TestLast1/profile.html', 'TestChannelid1'),
                                               ('TestFirst2 TestLast2', 'users/TestFirst1TestLast1/profile.html', None)]


    @patch('app.generate.write_templates_to_file')
    def test_render_index_page(self, write_static_file_fn):
        render_index_page(self.runners_data_list_with_channelid)


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





