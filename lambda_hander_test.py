import unittest
from lambda_function import lambda_handler
from mock import mock_open, patch, Mock
import __builtin__ as builtins
import json


class LambdaHandlerBase(unittest.TestCase):

    def setUp(self):
        self.basic_types = ['', u'', 'a', 'hello-str',
                            u'hello-unicode',
                            1, -1, 0, 1L, 0.0, True, False]
        self.basic_collections = [[], {}, (), [1, 2, 3], {'': ''}, {'1': 'a'}, (1, 2, 3)]
        self.json_exclude = [1.0j]
        self.the_basics = self.basic_types + self.basic_collections
        self.valid_notification_event = {'Records': [{'s3': {'object': {'key': 'blah'}}}]}


class LambdaHandler(LambdaHandlerBase):

    def test_ensure_event_is_dict(self):
        self.assertEqual(lambda_handler('', ''), {})
        self.assertEqual(lambda_handler('blah', ''), {})
        self.assertEqual(lambda_handler(u'', ''), {})
        self.assertEqual(lambda_handler(u'blah', ''), {})
        self.assertEqual(lambda_handler([], ''), {})
        self.assertEqual(lambda_handler([1, 2, 3], ''), {})
        self.assertEqual(lambda_handler(1, ''), {})
        self.assertEqual(lambda_handler(-1, ''), {})
        self.assertEqual(lambda_handler(1L, ''), {})
        self.assertEqual(lambda_handler(0, ''), {})
        self.assertEqual(lambda_handler(0.0, ''), {})
        self.assertEqual(lambda_handler(1.0j, ''), {})
        self.assertEqual(lambda_handler(True, ''), {})
        self.assertEqual(lambda_handler(False, ''), {})
        self.assertEqual(lambda_handler((1, 2), ''), {})

    def test_validate_event_dict(self):
        self.assertEqual(lambda_handler({}, ''), {})
        notification_event = {'Records': 0}
        self.assertEqual(lambda_handler(notification_event, ''), {})
        notification_event = {'Records': []}
        self.assertEqual(lambda_handler(notification_event, ''), {})
        notification_event = {'Records': [{'s3': {}}]}
        self.assertEqual(lambda_handler(notification_event, ''), {})
        notification_event = {'Records': [{'s3': {'object': {}}}]}
        self.assertEqual(lambda_handler(notification_event, ''), {})
        notification_event = {'Records': [{'s3': {'object': {'key': ''}}}]}
        self.assertEqual(lambda_handler(notification_event, ''), {})

        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = False
            self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_s3_key_for_dir(self):
        notification_event = {'Records': [{'s3': {'object': {'key': 'blah/'}}}]}
        self.assertEqual(lambda_handler(notification_event, ''), {})

    def test_no_config(self):
        with patch('os.path.isfile') as isfile_mock:
            isfile_mock.return_value = False
            self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})


class LambdaConfigHandling(LambdaHandlerBase):

    def setUp(self):
        super(LambdaConfigHandling, self).setUp()
        # self.patcher = patch('os.path.isfile').start()
        # instance = self.patcher.return_value
        # instance.method.return_value = True

    # def tearDown(self):
    #     self.patcher.stop()

    def test_json_config_type_handling(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps(x)
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_domain_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps({'domains': x})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_api_key_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.the_basics:
                mock_data = json.dumps({'api_key': x})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_config_plain_text_handling(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.the_basics + self.json_exclude:
                with patch.object(builtins, 'open', mock_open(read_data=x)):
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_domains_dict_type_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.basic_types:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': 'example',
                                            'domains': {x: y}})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_imgix_domain_forward_lash_check_source_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'/sdafasdf/': ''}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_imgix_correct_domain_source_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'dsaf.not.imgix.net': ''}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_domain_and_api_key_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.the_basics:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': x,
                                            'domains': y})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_domain_url_dict_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for x in self.basic_types:
                for y in reversed(self.the_basics):
                    mock_data = json.dumps({'api_key': 'example',
                                            'domains': {'dsaf.not.imgix.net': {x: y}}})
                    with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                        self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_scheme_types_handling_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            for y in reversed(self.the_basics):
                mock_data = json.dumps({'api_key': 'example',
                                        'domains': {'dsaf.not.imgix.net': {'schemes': y}}})
                with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''), {})

    def test_correct_config(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'dsaf.not.imgix.net': {'schemes': ['http', 'https']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                with patch('requests.post') as req_post:
                    req_post.return_value = mock_response = Mock()
                    mock_response.status_code = 200
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''),
                                     {'http://dsaf.not.imgix.net/blah': 200,
                                      'https://dsaf.not.imgix.net/blah': 200})

    def test_correct_config_multi_domains(self):
        with patch('os.path.isfile') as isfile_mock:
            instance = isfile_mock.return_value
            instance.method.return_value = True

            mock_data = json.dumps({'api_key': 'example',
                                    'domains': {'dsaf.not.imgix.net': {'schemes': ['http', 'https']},
                                                '1234.imgix.net': {'schemes': ['https']}}})
            with patch.object(builtins, 'open', mock_open(read_data=mock_data)):
                with patch('requests.post') as req_post:
                    req_post.return_value = mock_response = Mock()
                    mock_response.status_code = 200
                    self.assertEqual(lambda_handler(self.valid_notification_event, ''),
                                     {'http://dsaf.not.imgix.net/blah': 200,
                                      'https://dsaf.not.imgix.net/blah': 200,
                                      'https://1234.imgix.net/blah': 200})


if __name__ == '__main__':
    unittest.main()
