import pytest
from unittest.mock import patch, MagicMock
from src.core.flags.base_flag import BaseFlag
from src.core.service.runner import YTDLPRunner


# Dummy flag for testing
class TestFlag(BaseFlag):
    name = "test-flag"

    def to_args(self) -> list[str]:
        return ["--test-flag"]


@pytest.fixture
def runner():
    return YTDLPRunner(yt_dlp_path="/mock/yt-dlp")


def test_init_uses_default_path():
    with patch("src.core.service.runner.YT_DLP_PATH", "/default/yt-dlp"):
        runner = YTDLPRunner()
        assert runner.yt_dlp_path == "/default/yt-dlp"


def test_add_flag_accepts_list_of_baseflag(runner):
    flag1 = TestFlag()
    flag2 = TestFlag()
    runner.add_flag([flag1, flag2])
    assert len(runner.flags) == 2
    assert flag1 in runner.flags
    assert flag2 in runner.flags


def test_add_flag_rejects_non_baseflag(runner):
    with pytest.raises(TypeError, match="flag must be of type BaseFlag"):
        runner.add_flag(["not-a-flag"])  # type: ignore


def test_build_command_with_flags(runner):
    runner.add_flag([TestFlag()])
    cmd = runner.build_command("https://youtube.com/watch?v=abc")
    assert cmd == ["/mock/yt-dlp", "--test-flag", "https://youtube.com/watch?v=abc"]


def test_build_command_rejects_empty_url(runner):
    with pytest.raises(ValueError, match="url cannot be empty"):
        runner.build_command("")


@patch("src.core.service.runner.subprocess.Popen")
def test_run_executes_subprocess_and_streams_output(mock_popen, runner):
    # Mock subprocess
    mock_process = MagicMock()
    mock_process.stdout = [
        "Downloading...\n",
        "100% complete\n"
    ]
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    output_lines = []

    def on_output(line):
        output_lines.append(line)

    result = runner.run("https://youtube.com/watch?v=abc", on_output=on_output)

    # Assertions
    assert result["return_code"] == 0
    assert result["stdout"] == ["Downloading...", "100% complete"]
    assert output_lines == ["Downloading...", "100% complete"]
    mock_popen.assert_called_once()


@patch("src.core.service.runner.subprocess.Popen")
def test_run_raises_error_if_stdout_is_none(mock_popen, runner):
    mock_process = MagicMock()
    mock_process.stdout = None
    mock_popen.return_value = mock_process

    with pytest.raises(RuntimeError, match="Stdout cannot be None"):
        runner.run("https://youtube.com/watch?v=abc")


def test_clear_flags(runner):
    runner.add_flag([TestFlag()])
    assert len(runner.flags) == 1
    runner.clear_flags()
    assert runner.flags == []