from unittest import TestCase

import pytest

from PEP440Version import PEP440Version


class PEP440VersionTest(TestCase):

    def test_PEP440(self):
        # All examples in PEP440 spec
        self.assertEqual(PEP440Version('1').version, [1])
        self.assertEqual(PEP440Version('1.2').version, [1, 2])
        self.assertEqual(PEP440Version('1.2.3').version, [1, 2, 3])

        self.assertEqual(PEP440Version('2012.04').version, [2012, 4])
        self.assertEqual(PEP440Version('2013.01').version, [2013, 1])

        self.assertEqual(PEP440Version('1.2a3').version, [1, 2, 'a', 3])
        self.assertEqual(PEP440Version('1.2b3').version, [1, 2, 'b', 3])
        self.assertEqual(PEP440Version('1.2rc3').version, [1, 2, 'rc', 3])

        self.assertGreater(PEP440Version('1.2rc3'), PEP440Version('1.2b3'))
        self.assertGreater(PEP440Version('1.2b3'), PEP440Version('1.2a3'))
        self.assertLess(PEP440Version('1.2a3'), PEP440Version('1.2b3'))
        self.assertEqual(PEP440Version('1.2a3'), PEP440Version('1.2a3'))

        self.assertEqual(PEP440Version('1.2.post3').version, [1, 2, 'post', 3])

        self.assertEqual(PEP440Version('1.2a3.post4').version,
                         [1, 2, 'a', 3, 'post', 4])
        self.assertEqual(PEP440Version('1.2b3.post4').version,
                         [1, 2, 'b', 3, 'post', 4])
        self.assertEqual(PEP440Version('1.2rc3.post4').version,
                         [1, 2, 'rc', 3, 'post', 4])

        self.assertEqual(PEP440Version('1.2.dev3').version, [1, 2, 'dev', 3])

        self.assertEqual(PEP440Version('1.2a3.dev4').version,
                         [1, 2, 'a', 3, 'dev', 4])

        self.assertEqual(PEP440Version('1.2.post3.dev4').version,
                         [1, 2, 'post', 3, 'dev', 4])

        self.assertEqual(PEP440Version('1!1.0').version, [1, '!', 1, 0])

        self.assertGreater(PEP440Version('1!1.1'), PEP440Version('1!1.0'))
        self.assertGreater(PEP440Version('2!1.1'), PEP440Version('1!0.9'))

        self.assertEqual(PEP440Version('1.1RC1'), PEP440Version('1.1rc1'))

        self.assertEqual(PEP440Version('1.2.a3').version, [1, 2, 'a', 3])
        self.assertEqual(PEP440Version('1.2-a3').version, [1, 2, 'a', 3])
        self.assertEqual(PEP440Version('1.2_a3').version, [1, 2, 'a', 3])

        self.assertEqual(PEP440Version('1.2.a3'), PEP440Version('1.2-a3'))

        self.assertEqual(PEP440Version('1.2.a'), PEP440Version('1.2-a0'))

        self.assertEqual(PEP440Version('1.2.post-3'),
                         PEP440Version('1.2.post3'))

        self.assertEqual(PEP440Version('1.2-3').version, [1, 2, 3])

        self.assertEqual(PEP440Version('1.2+u.3').version, [1, 2, '+', 'u', 3])
        self.assertEqual(PEP440Version('1.2+u-3').version, [1, 2, '+', 'u', 3])

        self.assertEqual(PEP440Version(' 1.2.3 ').version, [1, 2, 3])
        self.assertEqual(PEP440Version('\n1.2.3\n').version, [1, 2, 3])
        self.assertEqual(PEP440Version('\r1.2.3\r').version, [1, 2, 3])
        self.assertEqual(PEP440Version('\t1.2.3\t').version, [1, 2, 3])
        self.assertEqual(PEP440Version('\v1.2.3\v').version, [1, 2, 3])

    @pytest.mark.xfail
    def test_epoch_comparison(self):
        # TODO: This is quite essential to the purpose of PEP 440
        # but is rarely ever used.
        self.assertGreater(PEP440Version('1!1.0'), PEP440Version('2012.04'))

    @pytest.mark.xfail
    def test_implicit_post(self):
        # TODO: This is quite important to rewrite existing implicit post
        self.assertEqual(PEP440Version('1.2-3'), PEP440Version('1.2.post3'))
        self.assertNotEqual(PEP440Version('1.2-3'), PEP440Version('1.2.3'))

    @pytest.mark.xfail
    def test_non_final_unsupported_comparisons(self):
        # TODO: Ordering of these is not especially important
        self.assertEqual(PEP440Version('1.2a3'), PEP440Version('1.2alpha3'))
        self.assertEqual(PEP440Version('1.2b3'), PEP440Version('1.2beta3'))
        self.assertEqual(PEP440Version('1.2pre3'),
                         PEP440Version('1.2bpreview3'))
        self.assertEqual(PEP440Version('1.2rc3'), PEP440Version('1.2c3'))

    def test_final(self):
        v = PEP440Version('1.2.3')
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), '1.2.3')

    def test_invalid_epoch(self):
        with self.assertRaisesRegex(ValueError, 'Invalid use of epoch'):
            PEP440Version('a!1.2.3')

    def test_invalid_epoch_v(self):
        with self.assertRaisesRegex(ValueError, 'Invalid use of epoch'):
            PEP440Version('v!1.2.3')

    def test_epoch_not_implemented(self):
        # TODO: To be useful, final and previous need to ignore the epoch
        # until previous creates a new version identifier which should
        # be in the same epoch
        v = PEP440Version('5!1.2.3')
        with self.assertRaises(NotImplementedError):
            v.final

    def test_v_prefix(self):
        v = PEP440Version('v1.2.3')
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), 'v1.2.3')

    def test_v_prefix_disabled(self):
        v = PEP440Version('v1.2.3', v_prefix=False)
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), '1.2.3')

    def test_no_dots(self):
        v = PEP440Version('123')
        self.assertEqual(v.version, [123])

    def test_no_numbers(self):
        v = PEP440Version('abc')
        self.assertEqual(v.version, ['abc', 0])
        self.assertEqual(str(v), 'abc')

    def test_tuple(self):
        v = PEP440Version((1, 2, 3))
        self.assertEqual(v.version, (1, 2, 3))
        self.assertEqual(str(v), '1.2.3')

    def test_tuple_v(self):
        v = PEP440Version((1, 2, 3), v_prefix=True)
        self.assertEqual(v.version, (1, 2, 3))
        self.assertEqual(str(v), 'v1.2.3')

    def test_tuple_v_str(self):
        v = PEP440Version(('v1', 2, 3), v_prefix=True)
        self.assertEqual(v.version, (1, 2, 3))
        self.assertEqual(str(v), 'v1.2.3')

    def test_tuple_v_str_disabled(self):
        v = PEP440Version(('v1', 2, 3), v_prefix=False)
        self.assertEqual(v.version, (1, 2, 3))
        self.assertEqual(str(v), '1.2.3')

    def test_tuple_vv(self):
        v = PEP440Version(('vv', 2, 3), v_prefix=True)
        self.assertEqual(v.version, ('v', 2, 3))
        self.assertEqual(str(v), 'vv.2.3')
        self.assertEqual(repr(v), "PEP440Version('vv.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('vv.2.3')")

    def test_tuple_vv_auto(self):
        v = PEP440Version(('vv', 2, 3))
        self.assertEqual(v.version, ('v', 2, 3))
        self.assertEqual(str(v), 'vv.2.3')
        self.assertEqual(repr(v), "PEP440Version('vv.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('vv.2.3')")

    def test_tuple_vv_disabled(self):
        v = PEP440Version(('vv', 2, 3), v_prefix=False)
        self.assertEqual(v.version, ('v', 2, 3))
        self.assertEqual(str(v), 'v.2.3')
        self.assertEqual(repr(v), "PEP440Version('v.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('v.2.3')")

    def test_list(self):
        v = PEP440Version([1, 2, 3])
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), '1.2.3')

    def test_list_v(self):
        v = PEP440Version([1, 2, 3], v_prefix=True)
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), 'v1.2.3')

    def test_list_v_str(self):
        v = PEP440Version(['v1', 2, 3], v_prefix=True)
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), 'v1.2.3')

    def test_list_v_str_disabled(self):
        v = PEP440Version(['v1', 2, 3], v_prefix=False)
        self.assertEqual(v.version, [1, 2, 3])
        self.assertEqual(str(v), '1.2.3')

    def test_list_vv(self):
        v = PEP440Version(['vv', 2, 3], v_prefix=True)
        self.assertEqual(v.version, ['v', 2, 3])
        self.assertEqual(str(v), 'vv.2.3')
        self.assertEqual(repr(v), "PEP440Version('vv.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('vv.2.3')")

    def test_list_vv_auto(self):
        v = PEP440Version(['vv', 2, 3])
        self.assertEqual(v.version, ['v', 2, 3])
        self.assertEqual(str(v), 'vv.2.3')
        self.assertEqual(repr(v), "PEP440Version('vv.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('vv.2.3')")

    def test_list_vv_disabled(self):
        v = PEP440Version(['vv', 2, 3], v_prefix=False)
        self.assertEqual(v.version, ['v', 2, 3])
        self.assertEqual(str(v), 'v.2.3')
        self.assertEqual(repr(v), "PEP440Version('v.2.3')")
        self.assertEqual(repr(eval(repr(v))), "PEP440Version('v.2.3')")

    def test_list_v_str_mixed(self):
        v = PEP440Version(['v1', 2, '3'])
        self.assertEqual(v.version, [1, 2, 3])

    def test_list_v_str_with_dots(self):
        v = PEP440Version(['v1', 2, '3.4'])
        self.assertEqual(v.version, [1, 2, 3, 4])


class PEP440FinalVersionTest(TestCase):

    def test_final(self):
        v = PEP440Version('1.2.3')
        self.assertEqual(v.version, [1, 2, 3])
        self.assertIsInstance(v.final, PEP440Version)
        self.assertNotEqual(v.final, PEP440Version([124]))
        self.assertIs(v.final, v)
        self.assertEqual(str(v), '1.2.3')

    def test_v_prefix(self):
        v = PEP440Version('v1.2.3')
        self.assertEqual(v.version, [1, 2, 3])
        self.assertNotEqual(v.final, PEP440Version([1, 2, 4]))
        self.assertNotEqual(v.final, PEP440Version([124]))
        self.assertIs(v.final, v)
        self.assertEqual(str(v), 'v1.2.3')
        self.assertEqual(str(v.final), 'v1.2.3')


class PEP440PreviousFinalVersionTest(TestCase):

    def test_final(self):
        v = PEP440Version('1.2.3')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [1, 2, 2])
        self.assertEqual(str(p), '1.2.2')

        p2 = v._estimate_previous()
        self.assertIs(p, p2)

    def test_not_final(self):
        v = PEP440Version('1.2.3dev0')
        with self.assertRaisesRegex(AssertionError, 'is not final'):
            v._estimate_previous()

    def test_epoch_not_implemented(self):
        # TODO: To be useful, final and previous need to ignore the epoch
        # until previous creates a new version identifier which should
        # be in the same epoch
        v = PEP440Version('5!1.2.3')
        with self.assertRaises(NotImplementedError):
            v._estimate_previous()

    def test_v_prefix(self):
        v = PEP440Version('v1.2.3')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [1, 2, 2])
        self.assertEqual(str(p), 'v1.2.2')

    def test_one(self):
        v = PEP440Version('1.2.1')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [1, 2, 0])
        self.assertEqual(str(p), '1.2.0')

    def test_zeros(self):
        v = PEP440Version('v1.2.0')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [1, 1, '*'])
        self.assertEqual(str(p), 'v1.1.*')

    def test_multiple_zeros(self):
        v = PEP440Version('1.0.0')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [0, 0, '*'])
        self.assertEqual(str(p), '0.0.*')

        v = PEP440Version('1.0.0.0')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [0, 0, 0, '*'])
        self.assertEqual(str(p), '0.0.0.*')

        v = PEP440Version('1.0.0.1.0')
        p = v._estimate_previous()
        self.assertIsInstance(p, PEP440Version)
        self.assertEqual(p.version, [1, 0, 0, 0, '*'])
        self.assertEqual(str(p), '1.0.0.0.*')

    def test_all_zeros(self):
        v = PEP440Version('0.0.0')
        msg = 'version prior to 0.0 can not exist'
        with self.assertRaisesRegex(ValueError, msg):
            v._estimate_previous()


class PEP440PreviousNonFinalVersionTest(TestCase):

    def test_zero_algorithm_non_final(self):
        v = (0, 0, 0, 'dev', 1)
        p = PEP440Version._decrement(v)
        self.assertIsInstance(p, tuple)
        self.assertEqual(p, (0, 0, 0, 'dev', 0))

    def test_skip_non_int(self):
        v = (0, 0, 1, 'dev', 0)
        p = PEP440Version._decrement(v)
        self.assertIsInstance(p, tuple)
        self.assertEqual(p, (0, 0, 0, 'dev', '*'))
