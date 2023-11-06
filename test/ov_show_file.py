import numpy as np
import struct
from matplotlib import pyplot as plt

# Generate file names for the three txt files: received_data_1.txt, received_data_2.txt, received_data_3.txt
file_names = [f"serial_data/received_data_{i}.txt" for i in range(1, 4)]

# Create a list to store the images
images = []

# Iterate over each txt file
for txt_file in file_names:
    HEXADECIMAL_BYTES = []

    # Open the current txt file and read each line, then split each line into hexadecimal values
    with open(txt_file, "r") as file:
        for line in file:
            hex_values = line.strip().split(',')
            for hex_value in hex_values:
                HEXADECIMAL_BYTES.append(hex_value.strip())

    # Reformat the bytes into an image
    raw_bytes = np.array([int(x, 16) for x in HEXADECIMAL_BYTES if x], dtype="i2")
    image = np.zeros((len(raw_bytes), 3), dtype=int)

    for j in range(len(raw_bytes)):
        pixel = struct.unpack('>h', raw_bytes[j])[0]
        r = ((pixel >> 11) & 0x1F) << 3
        g = ((pixel >> 5) & 0x3F) << 2
        b = (pixel & 0x1F) << 3
        image[j] = [r, g, b]

    image = np.reshape(image, (144, 176, 3))
    image = np.uint8(image)

    images.append(image)

# Display or save the images
for i, image in enumerate(images):
    # Save each image with a different output file name
    output_path = f"SVMImageClassification/test_photo/output_image_{i + 1}.png"
    plt.imsave(output_path, image, format='png')

    # If you want to display the images, uncomment the following line
    # plt.imshow(image)
    # plt.show()