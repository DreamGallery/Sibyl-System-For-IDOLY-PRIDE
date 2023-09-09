import cv2
import numpy as np
from src.read_ini import config
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

_half_split_length = config.getint("Arg", "half_split_length")


def to_binary(img: cv2.UMat, thresh: float) -> cv2.UMat:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary


def to_binary_adaptive(img: cv2.UMat, blocksize: int, C: float) -> cv2.UMat:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, C)
    return binary


def draw_text(
    text: str, font_path: list[str], fontsize: list[int], strokewidth: int, kerning: int
) -> tuple[list[cv2.UMat], list[cv2.UMat]]:
    font_japan = ImageFont.truetype(font_path[0], fontsize[0])
    font_alpha = ImageFont.truetype(font_path[1], fontsize[1])
    font_digit = ImageFont.truetype(font_path[2], fontsize[2])

    char_info: list[tuple[FreeTypeFont, int]] = []
    text_height = int(0)
    for char in text:
        if char.encode("utf-8").isalpha():
            font = font_alpha
        elif char.encode("utf-8").isdigit():
            font = font_digit
        else:
            font = font_japan
        char_bbox = font.getbbox(char, stroke_width=strokewidth)
        char_width = char_bbox[2] - char_bbox[0] - strokewidth
        text_height = max((char_bbox[3] - char_bbox[1]), text_height)
        char_info.append([font, char_width])

    text_width = int(0)
    for info in char_info:
        text_width += info[1]
    text_size = ((text_width + (len(text) - 1) * kerning), text_height)
    text_img = Image.new("RGBA", text_size)
    draw = ImageDraw.Draw(text_img)

    tmp_width = int(0)
    for index, char in enumerate(text):
        draw.text(
            (((char_info[index][1]) // 2 + tmp_width), (text_size[1] // 2)),
            char,
            anchor="mm",
            font=char_info[index][0],
            stroke_width=strokewidth,
            stroke_fill=(32, 32, 32),
        )
        tmp_width = tmp_width + char_info[index][1] + kerning
    binary: list[cv2.UMat] = []
    mask: list[cv2.UMat] = []
    kernel = cv2.UMat(cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    if len(text) >= _half_split_length:
        spilt_pixel = sum(
            list(item[1] for item in char_info[: len(text) // 2]),
            kerning * (len(text) // 2),
        )
        image_part = [
            cv2.UMat(np.asarray(text_img)[:, :spilt_pixel]),
            cv2.UMat(np.asarray(text_img)[:, spilt_pixel:]),
        ]
        for part in image_part:
            binary.append(to_binary(part, 127))
            mask.append(cv2.erode(to_binary(part, 30), kernel, iterations=1))
    else:
        binary.append(to_binary(np.asarray(text_img), 127))
        mask.append(cv2.erode(to_binary(np.asarray(text_img), 30), kernel, iterations=1))

    return (binary, mask)


def compare(frame_img: cv2.UMat, binary: list[cv2.UMat], threshold: float, mask: list[cv2.UMat]) -> bool:
    white_pixels = cv2.countNonZero(frame_img)
    if white_pixels < 300:
        return False
    part_max: list[float] = []
    for image in zip(binary, mask):
        res = cv2.matchTemplate(frame_img, image[0], cv2.TM_CCORR_NORMED, mask=image[1]).get()
        res[np.isinf(res)] = 0
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        part_max.append(max_val)
    max_avg = sum(part_max) / len(part_max)
    if max_avg > threshold:
        return True
    else:
        return False
