from datetime import datetime

from PIL import Image
from PIL import ImageChops


class ImageDiff:
    def __init__(self, original: Image, changed: Image) -> None:
        self._original = original
        self._changed = changed

    @staticmethod
    def _add_transparent_fields(pixels_sequences) -> list:
        pixel_image_with_difference = []
        transparent_value = (255, 255, 255, 0)

        for pixel_sequence in pixels_sequences:
            if not any(pixel_sequence[:-1]):
                pixel_image_with_difference.append(transparent_value)
            else:
                pixel_image_with_difference.append(pixel_sequence)
        return pixel_image_with_difference

    def find_difference(self) -> None:
        differance = ImageChops.difference(self._original, self._changed).convert("RGBA")
        pixels_sequences = differance.getdata()

        transparent_fields = self._add_transparent_fields(pixels_sequences)

        differance.putdata(transparent_fields)
        copied_original = self._original.copy()
        copied_original.paste(differance, (0, 0), differance)

        date = datetime.now().strftime("%m-%d-%Y%H:%M:%S")
        copied_original.save(f"result_{date}.png")


if __name__ == "__main__":
    reference = Image.open("reference.png")
    photo_1 = Image.open("photo1.png")

    image_diff = ImageDiff(reference, photo_1)
    image_diff.find_difference()
