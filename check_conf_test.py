import unittest
from check_conf import validate_config
from mock import mock_open, patch
import __builtin__ as builtins
import json


class CheckConfTest(unittest.TestCase):

    def setUp(self):
        self.basic_types = ['', u'', 'a', 'hello-str',
                            u'hello-unicode',
                            1, -1, 0, 1L, 0.0, True, False]
        self.basic_collections = [[], {}, (), [1, 2, 3], {'': ''}, {'1': 'a'}, (1, 2, 3)]
        self.json_exclude = [1.0j]
        self.the_basics = self.basic_types + self.basic_collections
        # self.patcher = patch('os.path.isfile').start()
        # instance = self.patcher.return_value
        # instance.method.return_value = True

    # def tearDown(self):
    #     self.patcher.stop()

    def test_no_config(self):
        self.assertEqual(validate_config(''), False)

    def test_json_config_type_handling(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps(x)
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(validate_config(mock_data), False)

    def test_domain_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps({'domains': x})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(validate_config(mock_data), False)

    def test_api_key_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps({'api_key': x})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(validate_config(mock_data), False)

    def test_config_plain_text_handling(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.the_basics + self.json_exclude:
                with patch.object(builtins, 'open', mock_open(read_data=x)):
                    self.assertEqual(validate_config(x), False)

    def test_domains_dict_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.basic_types:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': 'example',
                                            'domains': {x: y}})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(validate_config(mock_data), False)

    def test_imgix_domain_forward_lash_check_source_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'/sdafasdf/': ''}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), False)

    def test_imgix_correct_domain_source_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'dsaf.not.imgix.net': ''}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), False)

    def test_domain_and_api_key_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.the_basics:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': x,
                                            'domains': y})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(validate_config(mock_data), False)

    def test_domain_url_dict_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for x in self.basic_types:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': 'example',
                                            'domains': {'dsaf.not.imgix.net': {x: y}}})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(validate_config(mock_data), False)

    def test_scheme_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            for y in reversed(self.the_basics):
                mock_data = json.dumps({'api_key': 'example',
                                        'domains': {'dsaf.not.imgix.net': {'schemes': y}}})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(validate_config(mock_data), False)

    def test_too_many_schemes_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'example.imgix.net': {'schemes': ['http', 'https', 'ftp']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), False)

    def test_incorrect_schemes_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'example.imgix.net': {'schemes': ['http', 'htt']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), False)

    def test_correct_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'example.imgix.net': {'schemes': ['http', 'https']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), True)

    def test_correct_config_multi_domains(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'xxx.imgix.net': {'schemes': ['http', 'https']},
                                                '1234.imgix.net': {'schemes': ['https']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), True)

    def test_correct_validate_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = True

            mock_data = json.dumps({"api_key": "somealphanumericvalue",
                                    "domains": {"blah.imgix.net": {"schemes": ["http", "https"]}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(validate_config(mock_data), True)


if __name__ == '__main__':
    unittest.main()
