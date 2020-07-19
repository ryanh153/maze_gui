import numpy as np
from PIL import Image


im_array = np.zeros([100, 100, 3], dtype=np.uint8)
im_array[0, 0, :] = 255
im_array[50, 0, :] = 255
im = Image.fromarray(im_array)
im.save("image.png")
