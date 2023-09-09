import sys
import json
import cv2.typing
from src.read_ini import config
from src.frame import FrameProcess
from src.events import AssEvents
from src.adv_text import to_time
from src.match import draw_text, compare


_FONT_PATH = json.loads(config.get("File PATH", "FONT_PATH"))
_fontsize = json.loads(config.get("Font Config", "fontsize"))
_strokewidth = config.getint("Font Config", "strokewidth")
_kerning = config.getint("Font Config", "kerning")
_threshold = config.getfloat("Arg", "threshold")


def time_fix(
    event: AssEvents,
    image_list: list[tuple[str, cv2.typing.MatLike]],
    start_file_index: int,
    target: str,
    stream: FrameProcess,
) -> int:
    text = event.Text
    binary, mask = draw_text(text, _FONT_PATH, _fontsize, _strokewidth, _kerning)
    for frame_pack in image_list[start_file_index:]:
        if compare(frame_pack[1], binary, _threshold, mask=mask):
            start_time = float(frame_pack[0][:-1])
            event.Start = to_time(start_time)
            break
        else:
            start_file_index = start_file_index + 1

    if start_file_index >= len(image_list):
        print("can't find subtitle text in target files, please check or adjust parameter")
        sys.exit(1)

    index_plus = int(event.Duration * stream.fps - 2)
    start_file_index = start_file_index + index_plus

    try:
        for frame_pack in image_list[start_file_index:]:
            if compare(frame_pack[1], binary, _threshold, mask=mask):
                start_file_index = start_file_index + 1
            else:
                end_time = float(frame_pack[0][:-1])
                event.End = to_time(end_time)
                break
    except IndexError:
        print(
            IndexError,
            "\nfile start index plus index convert by time duration exceeds the number of all files",
        )
        sys.exit(1)

    end_file_index = start_file_index
    return end_file_index
