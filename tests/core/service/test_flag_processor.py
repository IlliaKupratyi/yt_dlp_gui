import pytest
from unittest.mock import patch
from src.core.flags.base_flag import BaseFlag
from src.core.service.flag_processor import FlagProcessor


# Dummy flag classes for testing
class MockFlagA(BaseFlag):
    name = "mock-a"
    conflicts = []
    requires = []

class MockFlagB(BaseFlag):
    name = "mock-b"
    conflicts = [MockFlagA]
    requires = []

class MockRequiredFlag(BaseFlag):
    name = "required"
    conflicts = []
    requires = []


@pytest.fixture
def processor():
    with patch("src.core.service.flag_processor.REQUIRED_FLAGS", []):  # avoid side effects
        return FlagProcessor()


def test_add_flag(processor):
    flag = MockFlagA()
    processor.add_flag(flag)
    assert flag in processor.flags


def test_add_duplicate_flag_ignored(processor):
    flag = MockFlagA()
    processor.add_flag(flag)
    processor.add_flag(flag)
    assert processor.flags.count(flag) == 1


def test_add_conflicting_flag_ignored(processor):
    flag_a = MockFlagA()
    flag_b = MockFlagB()  # conflicts with MockFlagA

    processor.add_flag(flag_a)
    processor.add_flag(flag_b)

    assert flag_b not in processor.flags
    assert flag_a in processor.flags


def test_remove_flag(processor):
    flag = MockFlagA()
    processor.add_flag(flag)
    processor.remove_flag(flag)
    assert flag not in processor.flags


def test_get_flags_includes_required():
    with patch("src.core.service.flag_processor.REQUIRED_FLAGS", [MockRequiredFlag]):
        proc = FlagProcessor()
        flags = proc.get_flags()
        assert any(isinstance(f, MockRequiredFlag) for f in flags)


def test_clear_flags(processor):
    flag = MockFlagA()
    processor.add_flag(flag)
    processor.clear_flags()
    assert processor.flags == []