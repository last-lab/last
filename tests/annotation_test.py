import unittest
from pydantic import ValidationError
from last.types.annotation import LabelStudioJSON, Annotations, AnnotationResult, AnnotationValue, Data, Meta  # 请替换为实际的导入路径

class TestLabelStudioJSON(unittest.TestCase):

    def test_valid_data(self):
        # 创建一个有效的LabelStudioJSON对象
        data = {
            'id': 1,
            'annotations': [
                {
                    'id': 1,
                    'completed_by': 1,
                    'result': [
                        {
                            'value': {'start': 0, 'end': 4, 'text': 'test'},
                            'id': 'some_id',
                            'from_name': 'label',
                            'to_name': 'text',
                            'type': 'labels',
                            'origin': 'manual'
                        }
                    ],
                    'was_cancelled': False,
                    'ground_truth': False,
                    'lead_time': 10.5
                }
            ],
            'file_upload': 'test.txt',
            'data': {'text': 'This is a test file.'},
            'meta': {},
            'created_at': '2023-09-06T12:20:25.640137Z',
            'updated_at': '2023-09-06T12:22:58.336359Z',
            'inner_id': 1,
            'total_annotations': 1,
            'cancelled_annotations': 0,
            'total_predictions': 0,
            'comment_count': 0,
            'unresolved_comment_count': 0,
            'project': 1,
            'updated_by': 1
        }
        
        # 验证数据是否有效
        label_studio_json = LabelStudioJSON(**data)
        self.assertEqual(label_studio_json.id, 1)
        
    def test_invalid_data(self):
        # 创建一个无效的LabelStudioJSON对象（缺少必需的字段）
        data = {
            'id': 1
        }
        
        # 验证数据是否无效
        with self.assertRaises(ValidationError):
            label_studio_json = LabelStudioJSON(**data)

if __name__ == '__main__':
    unittest.main()
