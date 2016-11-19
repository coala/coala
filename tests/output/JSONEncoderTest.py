import json
import re
import unittest
from datetime import datetime

from coalib.output.JSONEncoder import create_json_encoder


class TestClass1(object):

    def __init__(self):
        self.a = 0


class TestClass2(object):

    def __init__(self):
        self.a = 0
        self.b = TestClass1()


class TestClass3(object):

    def __init__(self):
        self.a = 0
        self.b = TestClass1()

    @staticmethod
    def __getitem__(key):
        return 'val'

    @staticmethod
    def keys():
        return ['key']


class PropertiedClass(object):

    def __init__(self):
        self._a = 5

    @property
    def prop(self):
        return self._a


class JSONAbleClass(object):

    @staticmethod
    def __json__():
        return ['dont', 'panic']


class JSONEncoderTest(unittest.TestCase):
    JSONEncoder = create_json_encoder(use_relpath=True)
    kw = {'cls': JSONEncoder, 'sort_keys': True}

    def test_builtins(self):
        self.assertEquals('"test"', json.dumps('test', **self.kw))
        self.assertEquals('1', json.dumps(1, **self.kw))
        self.assertEquals('true', json.dumps(True, **self.kw))
        self.assertEquals('null', json.dumps(None, **self.kw))

    def test_iter(self):
        self.assertEquals('[0, 1]', json.dumps([0, 1], **self.kw))
        self.assertEquals('[0, 1]', json.dumps((0, 1), **self.kw))
        self.assertEquals('[0, 1]', json.dumps(range(2), **self.kw))

    def test_dict(self):
        self.assertEquals('{"0": 1}', json.dumps({0: 1}, **self.kw))
        self.assertEquals('{"0": 1}', json.dumps({'0': 1}, **self.kw))
        self.assertEquals('{"0": "1"}', json.dumps({'0': '1'}, **self.kw))

    def test_time(self):
        tf = datetime.today()
        self.assertEquals('"' + tf.isoformat() + '"',
                          json.dumps(tf, **self.kw))

    def test_re_object(self):
        uut = re.compile('x')
        self.assertEqual('"' + uut.pattern + '"',
                         json.dumps(uut, **self.kw))

    def test_class1(self):
        tc1 = TestClass1()
        self.assertEquals('{"a": 0}', json.dumps(tc1, **self.kw))
        self.assertEquals('[{"a": 0}]', json.dumps([tc1], **self.kw))
        self.assertEquals('{"0": {"a": 0}}', json.dumps({0: tc1}, **self.kw))

    def test_class2(self):
        tc2 = TestClass2()
        self.assertEquals('{"a": 0, "b": {"a": 0}}',
                          json.dumps(tc2, **self.kw))

    def test_class3(self):
        tc3 = TestClass3()
        self.assertEquals('{"key": "val"}',
                          json.dumps(tc3, **self.kw))

    def test_propertied_class(self):
        uut = PropertiedClass()
        self.assertEqual('{"prop": 5}', json.dumps(uut, **self.kw))

    def test_jsonable_class(self):
        uut = JSONAbleClass()
        self.assertEqual('["dont", "panic"]', json.dumps(uut, **self.kw))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            json.dumps(1j, **self.kw)
