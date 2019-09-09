''' range of red in the picture '''

import numpy as np
import cv2

RED_RANGE = [([0, 0, 30], [60, 60, 255])]


async def encoded_image(bin_img):
    ''' decoding from bytearray to NumPY array '''
    image = bin_img
    decoded = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    return await found_red_image(decoded, RED_RANGE)


async def found_red_image(image, list_range):
    ''' break the array into a search range and return the result in float format '''
    for (lower, upper) in list_range:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(image, lower, upper)

        result = round(cv2.countNonZero(mask) * 100 / (image.size / 3), 2)
        return result
