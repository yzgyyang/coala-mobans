from unittest import TestCase

import pytest

from PEP440Version import PEP440Version
import egg_name_to_requirement

# Do manual import of dependency
egg_name_to_requirement.PEP440Version = PEP440Version  # noqa

from egg_name_to_requirement import egg_name_to_requirement


class EggNameTest(TestCase):

    def test_no_version(self):
        r = egg_name_to_requirement('abc')
        self.assertEqual(r, 'abc')

    def test_zero(self):
        r = egg_name_to_requirement('abc-0')
        self.assertEqual(r, 'abc==0')

    def test_no_previous_final(self):
        r = egg_name_to_requirement('abc-0.0.1')
        self.assertEqual(r, 'abc==0.0.1')

    def test_single_part_name(self):
        r = egg_name_to_requirement('abc-1.2.3')
        self.assertEqual(r, 'abc==1.2.3')

    def test_single_undercore_name(self):
        r = egg_name_to_requirement('ab_cd-1.2.3')
        self.assertEqual(r, 'ab_cd==1.2.3')

    def test_single_hyphen_name(self):
        r = egg_name_to_requirement('ab-cd-1.2.3')
        self.assertEqual(r, 'ab-cd==1.2.3')

    def test_dev0(self):
        r = egg_name_to_requirement('ab-cd-1.2dev0')
        self.assertEqual(r, 'ab-cd>1.1')

    def test_dot_dev0(self):
        r = egg_name_to_requirement('ab-cd-1.2.dev0')
        self.assertEqual(r, 'ab-cd>1.1')

    def test_dev_dot0(self):
        r = egg_name_to_requirement('ab-cd-1.2.dev0')
        self.assertEqual(r, 'ab-cd>1.1')

    def test_3to2(self):
        r = egg_name_to_requirement('3to2-1.2.dev0')
        self.assertEqual(r, '3to2>1.1')

    # TODO: this requires live lookup
    @pytest.mark.xfail
    def test_base_62(self):
        r = egg_name_to_requirement('base-62-1.2.dev0')
        self.assertEqual(r, 'base-62>1.1')


class EggNameInvalidDevVersionTest(TestCase):

    def test_zero(self):
        msg = 'version prior to 0.0 can not exist'
        with self.assertRaisesRegex(ValueError, msg):
            egg_name_to_requirement('abc-0-dev1')

    def test_no_previous_final(self):
        msg = 'Version 0.0.1-dev1 could not be decremented'
        with self.assertRaisesRegex(ValueError, msg):
            egg_name_to_requirement('abc-0.0.1-dev1')
