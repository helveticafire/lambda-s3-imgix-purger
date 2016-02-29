import unittest
from lambda_function import lambda_handler


class LambdaHandler(unittest.TestCase):

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
        notification_event = {'Records': [{'s3': {'object': {'key': 'blah'}}}]}
        # self.assertEqual(lambda_handler(notification_event, ''), {})

    def test_s3_key_for_dir(self):
        notification_event = {'Records': [{'s3': {'object': {'key': 'blah/'}}}]}
        self.assertEqual(lambda_handler(notification_event, ''), {})


if __name__ == '__main__':
    unittest.main()
