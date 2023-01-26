import unittest
import copy

from shadowui import Section

class TestSection(unittest.TestCase):
    def setUp(self):
        self.test_dom = [
        Section('top',children=[
            Section('top_child1'),
            Section('top_child2')
            ]),
        Section('middle',children = [
            Section('middle_child1',children=[
                Section('middle_child1_1'),
                Section('middle_child1_2'),
                Section('middle_child1_3'),
                Section('middle_child1_4')
            ]),
            Section('middle_child2')
            ]),
        Section('bottom',children=[
            Section('middle_child1'),
            Section('middle_child2')
            ]),
        ]
        self.root =Section("main", children=self.test_dom)

    def test_children_creation_from_dom(self):
        self.assertEqual(len(self.root.children),3)
        self.assertEqual(self.root['top'].name,'top')
        self.assertEqual(len(self.root['middle.middle_child1'].children),4)
        self.assertEqual(self.root['middle.middle_child1.middle_child1_3'].name,'middle_child1_3')


    def test_children_add(self):
        additional_dom = [
            Section('foo'),
            Section('Bar')
        ]
        new_root = Section('new_root')
        self.assertEqual(len(new_root.children),0)
        new_root += additional_dom
        self.assertEqual(len(new_root.children),2)
        new_root += Section('baz')
        self.assertEqual(len(new_root.children),3)
        new_root += [Section('a'),Section('b')]
        self.assertEqual(len(new_root.children),5)

        self.assertRaises(TypeError, new_root.__iadd__, 10)
        self.assertRaises(TypeError, new_root.__iadd__, [10,20])
        self.assertRaises(TypeError, new_root.__iadd__, "aa")
        self.assertRaises(TypeError, new_root.__iadd__, {"bb","cc"})
        self.assertRaises(TypeError, new_root.__iadd__, {Section('ok'),"bb",10})
