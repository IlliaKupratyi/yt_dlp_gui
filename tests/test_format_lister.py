from unittest.mock import patch

import pytest

from src.core.runner import YTDLPRunner
from src.utils.format_lister import FormatLister

lister = FormatLister()

@patch.object(YTDLPRunner, 'run')
def test_get_formats_calls_runner_and_parses_output(mock_run):
    mock_output_lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "------------------------------------------------------------------------------------------------------",
        "137 mp4   1920x1080   25    | 6.69MiB  3020k https    | avc1.640028 3020k video only 1080p, mp4_dash",
        "140 m4a   audio only      2 |    3.29MiB   130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash",
        "249 webm  audio only      2 |    1.17MiB    46k https | audio only opus 46k 48k [en] low, webm_dash",
    ]

    mock_run.return_value = {
        'return_code': 1,
        'stderr': [],
        'stdout': mock_output_lines
    }

    lister.output_formats = mock_output_lines

    result = lister.get_formats("https://youtube.com/watch?v=abc")

    print(result)
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert kwargs['on_output'] is not None

    assert len(result) == 3
    assert result[0]["id"] == "137"
    assert result[0]["ext"] == "mp4"
    assert result[0]["resolution"] == "1920x1080"
    assert result[0]["tbr"] == "3020k"

    assert result[1]["id"] == "140"
    assert result[1]["ext"] == "m4a"
    assert result[1]["resolution"] == "audio only"
    assert result[1]["tbr"] == "130k"

    assert result[2]["id"] == "249"
    assert result[2]["ext"] == "webm"
    assert result[2]["resolution"] == "audio only"
    assert result[2]["tbr"] == "46k"


@patch.object(YTDLPRunner, 'run')
def test_get_formats_raises_error_on_nonzero_exit_code(mock_run):
    mock_run.return_value = {
        'return_code': 2,
        'stderr': ['ERROR: Network timeout'],
        'stdout': []
    }

    with pytest.raises(RuntimeError, match=r"yt-dlp failed: ERROR: Network timeout"):
        lister.get_formats("https://example.com")


def test_parse_output_handles_empty_input():
    lister.output_formats = []
    result = lister._parse_output()
    assert result == []


def test_parse_output_ignores_header_and_empty_lines():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "",
        "137 mp4   1920x1080   25    |   76.69MiB  3020k https | avc1.640028 3020k video only 1080p, mp4_dash",
        "   ",
        "140 m4a   audio only      2 |    3.29MiB   130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash",
    ]
    lister.output_formats = lines
    result = lister._parse_output()
    assert len(result) == 2
    assert result[0]["id"] == "137"
    assert result[1]["id"] == "140"


def test_parse_output_handles_audio_only_resolution():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "140 m4a audio only 2 | 3.29MiB 130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash"
    ]
    lister.output_formats = lines
    result = lister._parse_output()
    assert result[0]["resolution"] == "audio only"


def test_parse_output_handles_missing_fields():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "137 mp4   1920x1080   25 | 76.69MiB  3020k https"
    ]
    lister.output_formats = lines
    result = lister._parse_output()
    assert len(result) == 1
    assert result[0]["id"] == "137"
    assert result[0]["tbr"] == "3020k"

def test_parse_output_handles_truncated_line():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "137 mp4",
        "137 mp4   1920x1080   25    |   76.69MiB  3020k https | avc1.640028    3020k video only"
    ]
    lister.output_formats = lines
    result = lister._parse_output()
    assert len(result) == 1
    assert result[0]["id"] == "137"

def test_parse_output_ignores_lines_with_invalid_id():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "invalid_id mp4 1920x1080 25 | 76.69MiB 3020k https | avc1.640028 3020k video only 1080p, mp4_dash"
    ]
    lister.output_formats = lines
    result = lister._parse_output()
    assert len(result) == 0