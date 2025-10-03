import pytest
from unittest.mock import patch, MagicMock

from src.controller.app_controller import AppController
from src.core.exceptions.exception import YTDLRuntimeError


@pytest.fixture
def controller():
    return AppController()


@patch("src.controller.app_controller.YTDLPRunner")
def test_setup_video_properties_success(mock_runner_class, controller):
    mock_runner = MagicMock()
    mock_runner.run.return_value = None
    mock_runner_class.return_value = mock_runner

    with (
        patch("src.controller.app_controller.has_error", return_value=False),
        patch("src.controller.app_controller.subtitles_parse_output", return_value=MagicMock()),
        patch("src.controller.app_controller.formats_parse_output", return_value=[{"id": "137"}]),
    ):
        controller.setup_video_properties("https://youtube.com/watch?v=abc", on_output=lambda x: None)

        assert controller.url == "https://youtube.com/watch?v=abc"
        assert controller.formats == [{"id": "137"}]
        assert controller.title == ""  # output_lines[-1] would be set in real run


@patch("src.controller.app_controller.YTDLPRunner")
def test_setup_video_properties_with_error(mock_runner_class, controller):
    mock_runner = MagicMock()
    mock_runner.run.side_effect = lambda url, on_output: on_output("ERROR: Invalid URL")
    mock_runner_class.return_value = mock_runner

    with patch("src.controller.app_controller.has_error", return_value=True):
        with pytest.raises(YTDLRuntimeError):
            controller.setup_video_properties("https://youtube.com/watch?v=abc")

        assert controller.formats == []
        assert controller.subtitles.subtitles == []


def test_start_downloading_when_already_running(controller):
    controller.is_running = True
    thread = controller.start_downloading()
    assert thread is None


@patch("src.controller.app_controller.threading.Thread")
def test_start_downloading_starts_thread(mock_thread_class, controller):
    controller.url = "https://youtube.com/watch?v=abc"
    controller.is_running = False

    mock_thread = MagicMock()
    mock_thread_class.return_value = mock_thread

    thread = controller.start_downloading()
    assert thread == mock_thread
    mock_thread.start.assert_called_once()