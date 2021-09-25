import os
from PIL import Image


def detect_color_image(file_name, thumb_size=40, MSE_cutoff=22):
    """
    takes in input filename which should be in the same directory as of
    this file and returns a whether the image is colored or greyscale.

    :param file_name: image file name
    :param thumb_size: size of the resized image
    :param MSE_cutoff: THe minimum Mean Squared Error threshold
    :return: A string predicting whether the image is colored or greyscale
    """
    pil_img = Image.open(file_name)
    bands = pil_img.getbands()

    # if image is coloured
    if bands == ('R', 'G', 'B') or bands == ('R', 'G', 'B', 'A'):
        # resize the image for easier processing
        thumb = pil_img.resize((thumb_size, thumb_size))
        # SSE: squared error
        SSE, bias = 0, [0, 0, 0]
        # loop over every pixel
        for pixel in thumb.getdata():
            # we take the average value of each pixel's RGB values
            mu = sum(pixel) / 3
            SSE += sum((pixel[i] - mu - bias[i]) * (pixel[i] - mu - bias[i]) for i in [0, 1, 2])

        # calculate the mean squared error
        MSE = float(SSE) / (thumb_size * thumb_size)
        if MSE <= MSE_cutoff:
            return f"grayscale {100 - MSE}"
        else:
            return f"color"
    elif len(bands) == 1:
        return "black_white"
    else:
        return "not sure"
