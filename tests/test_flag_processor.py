from src.core.flags.base_flag import BaseFlag
from src.core.flag_processor import FlagProcessor

"""
Mock flags for testing
"""

class FlagA(BaseFlag):
    name = "flag-a"
    requires = []
    conflicts = []

class FlagB(BaseFlag):
    name = "flag-b"
    requires = [FlagA]
    conflicts = []

class FlagC(BaseFlag):
    name = "flag-c"
    requires = []
    conflicts = [FlagA]

class FlagD(BaseFlag):
    name = "flag-d"
    requires = [FlagA]
    conflicts = []


"""
Mock REQUIRED_FLAGS
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

"""
Tests
"""

"""Test adding a single flag without dependencies or conflicts."""
def test_add_single_flag():
    processor = FlagProcessor()
    flag_a = FlagA()
    processor.add_flag(flag_a)
    assert len(processor.flags) == 1
    assert processor.flags[0] is flag_a

"""Test that required flags are automatically added."""
def test_add_flag_with_required_dependency():
    processor = FlagProcessor()
    flag_b = FlagB()
    processor.add_flag(flag_b)
    assert len(processor.flags) == 2
    assert isinstance(processor.flags[0], FlagA)
    assert processor.flags[1] is flag_b

"""Test that flag is not added if a conflicting flag is already present."""
def test_conflict_prevention():
    processor = FlagProcessor()
    flag_a = FlagA()
    flag_c = FlagC()

    processor.add_flag(flag_a)
    processor.add_flag(flag_c)
    assert len(processor.flags) == 1
    assert isinstance(processor.flags[0], FlagA)

"""Test that adding the same flag instance twice does nothing."""
def test_no_duplicate_flags():
    processor = FlagProcessor()
    flag_a = FlagA()
    processor.add_flag(flag_a)
    processor.add_flag(flag_a)
    assert len(processor.flags) == 1

"""Test flag that requires a flag which itself requires another."""
def test_add_flag_that_requires_multiple():
    processor = FlagProcessor()
    flag_d = FlagD()
    processor.add_flag(flag_d)
    assert len(processor.flags) == 2
    assert isinstance(processor.flags[0], FlagA)

"""Test that get_flags() doesn't duplicate flags already added."""
def test_get_flags_does_not_duplicate_existing():
    processor = FlagProcessor()
    flag_a = FlagA()
    processor.add_flag(flag_a)
    processor.get_flags()
    assert len(processor.flags) == 2
    assert sum(1 for f in processor.flags if isinstance(f, FlagA)) == 1

"""Test that get_flags() returns the same list instance."""
def test_get_flags_returns_same_list():
    processor = FlagProcessor()
    flags1 = processor.get_flags()
    flags2 = processor.get_flags()
    assert flags1 is flags2

"""Test that conflict is triggered if ANY conflicting flag is present."""
def test_conflict_with_multiple_flags():
    processor = FlagProcessor()
    flag_a = FlagA()
    flag_c = FlagC()
    flag_e = FlagA()

    processor.add_flag(flag_c)
    processor.add_flag(flag_a)
    processor.add_flag(flag_e)
    processor.add_flag(flag_c)
    assert len(processor.flags) == 2