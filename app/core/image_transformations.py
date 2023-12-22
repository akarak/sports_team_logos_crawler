from pathlib import Path
from PIL import Image


def convert_to_tga_without_transparent_margins(filepath: Path) -> Path:
    img_src: Image.Image = Image.open(filepath)
    img_dest = crop_transparent_margins(img_src)

    filepath_dest = Path(filepath).with_suffix(".tga")
    img_dest.save(str(filepath_dest), compression="tga_rle")

    return filepath_dest


def crop_transparent_margins(img: Image.Image, border: int = 0) -> Image.Image:
    bbox = img.getbbox()

    if not (bbox):
        return img

    if (bbox == (0, 0, img.width - 1, img.height - 1)) and (border == 0):
        return img

    img = img.crop(bbox)
    cropped_img = Image.new("RGBA", (img.width + border * 2, img.height + border * 2), (0, 0, 0, 0))
    cropped_img.paste(img, (border, border))

    return cropped_img
