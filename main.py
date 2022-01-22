import logging
from datetime import datetime

from cv2 import cv2
from numpy import ndarray
from skimage.metrics import structural_similarity
from strenum import StrEnum

import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.StreamHandler()])


class ImageFormat(StrEnum):
    JPG = "jpg"
    PNG = "png"


def resize_image(image: ndarray, percentage: float = 60.0) -> ndarray:
    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


class ImageDiff:
    def __init__(self, original: ndarray, changed: ndarray) -> None:
        self._original = resize_image(original)
        self._changed = resize_image(changed)

    @staticmethod
    def _convert_to_gray(image: ndarray) -> ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _calculate_contours(difference: ndarray) -> tuple:
        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(difference, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours[0] if len(contours) == 2 else contours[1]

    def find_difference(self) -> None:
        logging.info("Converting images to gray scale...")
        grayed_original, grayed_changed = [self._convert_to_gray(image) for image in (self._original, self._changed)]

        logging.info("Calculating difference and it's score...")
        score, difference = structural_similarity(grayed_original, grayed_changed, full=True)
        logging.info(f"Difference score: {round(score, 3)}.")

        logging.info("Calculating contours...")
        contours = self._calculate_contours((difference * 255).astype("uint8"))

        logging.info("Applying contours to the orginal image...")
        minimum_contour_area = 100  # I guess its 10 x 10 pixels
        red_colour = (0, 0, 255)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > minimum_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(self._original, (x, y), (x + w, y + h), red_colour, 10)
                cv2.rectangle(self._changed, (x, y), (x + w, y + h), red_colour, 10)

    def save_image(self, name: str, image_format: ImageFormat) -> None:
        for image_name, image in (("original", self._original), ("changed", self._changed)):
            date = datetime.now().strftime("%m%d%Y%H%M%S")
            image_name = f"{name}_{image_name}_{date}.{image_format}"
            logging.info(f"Saving image {image_name}")
            status = cv2.imwrite(image_name, image)
            logging.info(f"Image written to filesystem: {status}")


ENGINE_TYPES = {
    "123": "reference.png",
    "345": "reference_2.png"
}

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__name__))
    reference = str(input("Please specify engine type: "))
    reference = cv2.imread(ENGINE_TYPES[reference])

    changed = str(input("Please specify changed image: "))
    changed = cv2.imread(changed)

    image_diff = ImageDiff(reference, changed)
    image_diff.find_difference()
    image_diff.save_image(os.path.join(project_dir, "example"), ImageFormat.JPG)  # save in JPG
    image_diff.save_image(os.path.join(project_dir, "example"), ImageFormat.PNG)  # save in PNG
