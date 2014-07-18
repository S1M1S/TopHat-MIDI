__author__ = 'Celery'
import unittest

from midi.objects.key import Key

class TestKey(unittest.TestCase):
    cls = Key('name', 0, 'toggle')

    def test_set_name(self):
        func = self.cls.set_name
        func('a')
        func('1')
        self.assertRaises(NameError, func, 'over10chars')

    def test_set_midi_loc(self):
        func = self.cls.set_midi_loc
        self.assertTrue(func('0'))
        self.assertTrue(func('1'))
        self.assertTrue(func('0xF10'))
        self.assertFalse(func('string'))
        self.assertFalse(func('0xG0'))

    def test_set_func(self):
        func = self.cls.set_func
        self.assertTrue(func('toggle'))
        self.assertTrue(func('hold'))
        self.assertFalse(func('notafunction'))
        self.assertFalse(func(0))

    def test_set_colour(self):
        func = self.cls.set_colour
        self.assertTrue(func('(0,0,0)'))
        self.assertTrue(func('[0,0,0]'))
        self.assertTrue(func('[1,1,1]'))
        self.assertTrue(func('(255,0,0)'))
        self.assertTrue(func('yellow'))
        self.assertTrue(func('blue'))
        self.assertFalse(func('[256,0,0]'))
        self.assertFalse(func('{0,0,0}'))
        self.assertFalse(func('foo colour'))
        self.assertFalse(func('("blue",0,0)'))