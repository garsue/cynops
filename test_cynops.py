#!/usr/bin/python
# vim: fileencoding=utf-8

from cynops import Relation
from unittest import TestCase, TestLoader, TextTestRunner
import pickle


class TestRelation(TestCase):

    def setUp(self):
        self.s = Relation(frozenset(['SNO', 'SNAME', 'STATUS', 'CITY']))
        self.s.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'CITY': 'London'})
        self.s.add({'SNO': 'S2',
                    'SNAME': 'Jones',
                    'STATUS': 10,
                    'CITY': 'Paris'})
        self.s.add({'SNO': 'S3',
                    'SNAME': 'Blake',
                    'STATUS': 30,
                    'CITY': 'Paris'})
        self.s.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'CITY': 'London'})
        self.s.add({'SNO': 'S5',
                    'SNAME': 'Adams',
                    'STATUS': 30,
                    'CITY': 'Athens'})
        self.p = Relation(frozenset(['PNO', 'PNAME', 'COLOR',
                                     'WEIGHT', 'CITY']))
        self.p.add({'PNO': 'P1',
                    'PNAME': 'Nut',
                    'COLOR': 'Red',
                    'WEIGHT': 12.0,
                    'CITY': 'London'})
        self.p.add({'PNO': 'P2',
                    'PNAME': 'Bolt',
                    'COLOR': 'Green',
                    'WEIGHT': 17.0,
                    'CITY': 'Paris'})
        self.p.add({'PNO': 'P3',
                    'PNAME': 'Screw',
                    'COLOR': 'Blue',
                    'WEIGHT': 17.0,
                    'CITY': 'Oslo'})
        self.p.add({'PNO': 'P4',
                    'PNAME': 'Screw',
                    'COLOR': 'Red',
                    'WEIGHT': 14.0,
                    'CITY': 'London'})
        self.p.add({'PNO': 'P5',
                    'PNAME': 'Cam',
                    'COLOR': 'Blue',
                    'WEIGHT': 12.0,
                    'CITY': 'Paris'})
        self.p.add({'PNO': 'P6',
                    'PNAME': 'Cog',
                    'COLOR': 'Red',
                    'WEIGHT': 19.0,
                    'CITY': 'London'})
        self.sp = Relation(frozenset(['SNO', 'PNO', 'QTY']))
        for sno in xrange(1, 5):
            for pno in xrange(1, 7):
                ruple = {'SNO': 'S' + str(sno),
                         'PNO': 'P' + str(pno),
                         'QTY': None}
                if sno == 1:
                    if pno == 1:
                        ruple['QTY'] = 300
                        self.sp.add(ruple)
                    elif pno == 2:
                        ruple['QTY'] = 200
                        self.sp.add(ruple)
                    elif pno == 3:
                        ruple['QTY'] = 400
                        self.sp.add(ruple)
                    elif pno == 4:
                        ruple['QTY'] = 200
                        self.sp.add(ruple)
                    elif pno == 5:
                        ruple['QTY'] = 100
                        self.sp.add(ruple)
                    elif pno == 6:
                        ruple['QTY'] = 100
                        self.sp.add(ruple)
                if sno == 2:
                    if pno == 1:
                        ruple['QTY'] = 300
                        self.sp.add(ruple)
                    elif pno == 2:
                        ruple['QTY'] = 400
                        self.sp.add(ruple)
                if sno == 3:
                    if pno == 2:
                        ruple['QTY'] = 200
                        self.sp.add(ruple)
                if sno == 4:
                    if pno == 2:
                        ruple['QTY'] = 200
                        self.sp.add(ruple)
                    elif pno == 4:
                        ruple['QTY'] = 300
                        self.sp.add(ruple)
                    elif pno == 5:
                        ruple['QTY'] = 400
                        self.sp.add(ruple)
        with open('rel_s.dump', 'w') as f:
            pickle.dump(self.s, f)

        with open('rel_p.dump', 'w') as f:
            pickle.dump(self.p, f)

        with open('rel_sp.dump', 'w') as f:
            pickle.dump(self.sp, f)

    def test_restrict(self):
        psd = Relation(frozenset(['SNO', 'SNAME', 'STATUS', 'CITY']))
        psd.add({'SNO': 'S1',
                 'SNAME': 'Smith',
                 'STATUS': 20,
                 'CITY': 'London'})
        psd.add({'SNO': 'S4',
                 'SNAME': 'Clark',
                 'STATUS': 20,
                 'CITY': 'London'})
        target = {'CITY': 'London'}
        self.assertEqual(self.s.restrict(target), psd)

    def test_project(self):
        psd = Relation(frozenset(['SNAME', 'CITY', 'STATUS']))
        psd.add({'SNAME': 'Smith',
                 'STATUS': 20,
                 'CITY': 'London'})
        psd.add({'SNAME': 'Jones',
                 'STATUS': 10,
                 'CITY': 'Paris'})
        psd.add({'SNAME': 'Blake',
                 'STATUS': 30,
                 'CITY': 'Paris'})
        psd.add({'SNAME': 'Clark',
                 'STATUS': 20,
                 'CITY': 'London'})
        psd.add({'SNAME': 'Adams',
                 'STATUS': 30,
                 'CITY': 'Athens'})
        self.assertEqual(self.s.project(frozenset(['SNAME',
                                                   'CITY',
                                                   'STATUS'])), psd)

    def test_join(self):
        psd = Relation(frozenset(['SNO', 'SNAME', 'STATUS',
                                  'PNO', 'PNAME', 'COLOR', 'WEIGHT', 'CITY']))
        psd.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'PNO': 'P1',
                    'PNAME': 'Nut',
                    'COLOR': 'Red',
                    'WEIGHT': 12.0,
                    'CITY': 'London'})
        psd.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'PNO': 'P4',
                    'PNAME': 'Screw',
                    'COLOR': 'Red',
                    'WEIGHT': 14.0,
                    'CITY': 'London'})
        psd.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'PNO': 'P6',
                    'PNAME': 'Cog',
                    'COLOR': 'Red',
                    'WEIGHT': 19.0,
                    'CITY': 'London'})
        psd.add({'SNO': 'S2',
                    'SNAME': 'Jones',
                    'STATUS': 10,
                    'PNO': 'P2',
                    'PNAME': 'Bolt',
                    'COLOR': 'Green',
                    'WEIGHT': 17.0,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S2',
                    'SNAME': 'Jones',
                    'STATUS': 10,
                    'PNO': 'P5',
                    'PNAME': 'Cam',
                    'COLOR': 'Blue',
                    'WEIGHT': 12.0,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S3',
                    'SNAME': 'Blake',
                    'STATUS': 30,
                    'PNO': 'P2',
                    'PNAME': 'Bolt',
                    'COLOR': 'Green',
                    'WEIGHT': 17.0,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S3',
                    'SNAME': 'Blake',
                    'STATUS': 30,
                    'PNO': 'P5',
                    'PNAME': 'Cam',
                    'COLOR': 'Blue',
                    'WEIGHT': 12.0,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'PNO': 'P1',
                    'PNAME': 'Nut',
                    'COLOR': 'Red',
                    'WEIGHT': 12.0,
                    'CITY': 'London'})
        psd.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'PNO': 'P4',
                    'PNAME': 'Screw',
                    'COLOR': 'Red',
                    'WEIGHT': 14.0,
                    'CITY': 'London'})
        psd.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'PNO': 'P6',
                    'PNAME': 'Cog',
                    'COLOR': 'Red',
                    'WEIGHT': 19.0,
                    'CITY': 'London'})
        self.assertEqual(self.s.join(self.p), psd)

    def test_union(self):
        psd = Relation(frozenset(['CITY']))
        psd.add({'CITY': 'London'})
        psd.add({'CITY': 'Paris'})
        psd.add({'CITY': 'Athens'})
        psd.add({'CITY': 'Oslo'})
        attr = frozenset(['CITY'])
        self.assertEqual(self.s.project(attr).union(self.p.project(attr)),
                         psd)

    def test_difference(self):
        psd = Relation(frozenset(['CITY']))
        psd.add({'CITY': 'Athens'})
        attr = frozenset(['CITY'])
        self.assertEqual(self.s.project(attr).difference(self.p.project(attr)),
                         psd)

    def test_semijoin(self):
        psd = Relation(frozenset(['SNO', 'SNAME', 'STATUS', 'CITY']))
        psd.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'CITY': 'London'})
        psd.add({'SNO': 'S2',
                    'SNAME': 'Jones',
                    'STATUS': 10,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S3',
                    'SNAME': 'Blake',
                    'STATUS': 30,
                    'CITY': 'Paris'})
        psd.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'CITY': 'London'})
        self.assertEqual(self.s.semijoin(self.p), psd)

    def test_semidifference(self):
        psd = Relation(frozenset(['SNO', 'SNAME', 'STATUS', 'CITY']))
        psd.add({'SNO': 'S5',
                    'SNAME': 'Adams',
                    'STATUS': 30,
                    'CITY': 'Athens'})
        self.assertEqual(self.s.semidifference(self.p), psd)

    def test_rename(self):
        psd = Relation(frozenset(['SNO', 'SNAME', 'STATUS', 'SCITY']))
        psd.add({'SNO': 'S1',
                    'SNAME': 'Smith',
                    'STATUS': 20,
                    'SCITY': 'London'})
        psd.add({'SNO': 'S2',
                    'SNAME': 'Jones',
                    'STATUS': 10,
                    'SCITY': 'Paris'})
        psd.add({'SNO': 'S3',
                    'SNAME': 'Blake',
                    'STATUS': 30,
                    'SCITY': 'Paris'})
        psd.add({'SNO': 'S4',
                    'SNAME': 'Clark',
                    'STATUS': 20,
                    'SCITY': 'London'})
        psd.add({'SNO': 'S5',
                    'SNAME': 'Adams',
                    'STATUS': 30,
                    'SCITY': 'Athens'})
        test = self.s.rename({'CITY': 'SCITY'})
        self.assertEqual(test, psd)
        print '\n'
        test.display()

    def test_display(self):
        print '\n'
        self.s.display()


if __name__ == '__main__':
    suite = TestLoader().loadTestsFromTestCase(TestRelation)
    TextTestRunner(verbosity=2).run(suite)
