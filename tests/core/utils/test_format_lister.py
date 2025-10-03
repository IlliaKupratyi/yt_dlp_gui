from src.core.utils.format_util import formats_parse_output, presets_to_dict, formats_to_dict, filter_by_unique_values


def test_formats_parse_output_parses_valid_lines():
    output_lines = [
        "ID  EXT   RESOLUTION FPS CH |   FILESIZE    TBR PROTO | VCODEC           VBR ACODEC      ABR ASR MORE INFO",
        "------------------------------------------------------------------------------------------------------",
        "137 mp4   1920x1080   25    | 6.69MiB  3020k https    | avc1.640028 3020k video only 1080p, mp4_dash",
        "140 m4a   audio only      2 |    3.29MiB   130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash",
        "249 webm  audio only      2 |    1.17MiB    46k https | audio only opus 46k 48k [en] low, webm_dash",
    ]

    result = formats_parse_output(output_lines)

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


def test_formats_parse_output_ignores_header_and_empty_lines():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "",
        "137 mp4   1920x1080   25 | 76.69MiB  3020k https | avc1.640028 3020k video only 1080p, mp4_dash",
        "   ",
        "140 m4a   audio only      2 |    3.29MiB   130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash",
    ]
    result = formats_parse_output(lines)
    assert len(result) == 2
    assert result[0]["id"] == "137"
    assert result[1]["id"] == "140"


def test_formats_parse_output_handles_audio_only_resolution():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "140 m4a audio only 2 | 3.29MiB 130k https | audio only mp4a.40.2  130k 44k [en] medium, m4a_dash"
    ]
    result = formats_parse_output(lines)
    assert result[0]["resolution"] == "audio only"


def test_formats_parse_output_handles_missing_fields():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "137 mp4   1920x1080   25 | 76.69MiB  3020k https"
    ]
    result = formats_parse_output(lines)
    assert len(result) == 1
    assert result[0]["id"] == "137"
    assert result[0]["tbr"] == "3020k"


def test_formats_parse_output_handles_truncated_line():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "137 mp4",
        "137 mp4   1920x1080   25    |   76.69MiB  3020k https | avc1.640028    3020k video only"
    ]
    result = formats_parse_output(lines)
    assert len(result) == 1
    assert result[0]["id"] == "137"


def test_formats_parse_output_ignores_lines_with_invalid_id():
    lines = [
        "ID EXT RESOLUTION FPS CH | FILESIZE TBR PROTO | VCODEC VBR ACODEC ABR ASR MORE INFO",
        "invalid_id mp4 1920x1080 25 | 76.69MiB 3020k https | avc1.640028 3020k video only 1080p, mp4_dash"
    ]
    result = formats_parse_output(lines)
    assert len(result) == 0


def test_formats_parse_output_empty_input():
    result = formats_parse_output([])
    assert result == []

def test_presets_to_dict():
    presets = ["MP4 1080p", "MP3"]
    result = presets_to_dict(presets)
    expected = [
        {"id": "mp4 1080p", "value": "MP4 1080p"},
        {"id": "mp3", "value": "MP3"}
    ]
    assert result == expected

def test_formats_to_dict():
    formats = [
        {"id": "137", "ext": "mp4", "resolution": "1920x1080"},
        {"id": "140", "ext": "m4a", "resolution": "audio only"}
    ]
    result = formats_to_dict(formats)
    expected = [
        {"id": "137", "value": "mp4 1920x1080"},
        {"id": "140", "value": "m4a audio only"}
    ]
    assert result == expected

def test_filter_by_unique_values():
    items = [
        {"id": "1", "value": "mp4 1080p"},
        {"id": "2", "value": "mp4 720p"},
        {"id": "3", "value": "mp4 1080p"},  # duplicate
        {"id": "4", "value": "webm 1080p"}
    ]
    result = filter_by_unique_values(items)
    expected = [
        {"id": "1", "value": "mp4 1080p"},
        {"id": "2", "value": "mp4 720p"},
        {"id": "4", "value": "webm 1080p"}
    ]
    assert result == expected

def test_filter_by_unique_values_empty():
    assert filter_by_unique_values([]) == []
