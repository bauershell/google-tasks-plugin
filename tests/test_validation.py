import unittest
from validation import task_body


class ValidationTests(unittest.TestCase):
    def test_patch_preserves_omitted_fields(self):
        self.assertEqual(task_body(title='Buy milk'), {'title': 'Buy milk'})

    def test_date_only_does_not_shift_timezone(self):
        self.assertEqual(task_body(due_date='2026-10-29')['due'], '2026-10-29T00:00:00.000Z')

    def test_clear_date_and_reopen(self):
        self.assertEqual(task_body(due_date='', status='needsAction'),
                         {'due': None, 'status': 'needsAction', 'completed': None})

    def test_reject_invalid_input(self):
        for kwargs in ({'title': ' '}, {'title': 'x' * 1025}, {'notes': 'x' * 8193},
                       {'status': 'done'}, {'due_date': '2026-02-30'},
                       {'due_date': '2026-10-29T12:00:00Z'}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    task_body(**kwargs)


if __name__ == '__main__':
    unittest.main()
