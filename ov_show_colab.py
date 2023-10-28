# Import the needed libraries
from matplotlib import pyplot as plt
import numpy as np
import struct

# Copy the output of the Serial Monitor to the variable below
HEXADECIMAL_BYTES = []

# Reformat the bytes into an image
raw_bytes = np.array(HEXADECIMAL_BYTES, dtype="i2")
image = np.zeros((len(raw_bytes),3), dtype=int)

# Loop through all of the pixels and form the image
for i in range(len(raw_bytes)):
    #Read 16-bit pixel
    pixel = struct.unpack('>h', raw_bytes[i])[0]

    #Convert RGB565 to RGB 24-bit
    r = ((pixel >> 11) & 0x1f) << 3;
    g = ((pixel >> 5) & 0x3f) << 2;
    b = ((pixel >> 0) & 0x1f) << 3;
    image[i] = [r,g,b]

image = np.reshape(image,(240, 320, 3)) #QCIF resolution

# Show the image
plt.imshow(image)
plt.show()