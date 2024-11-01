import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.measure import regionprops

# Step 1: Read the image
image = cv2.imread('input.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Convert to binary image
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Step 3: Remove small objects (area < 30 pixels)
binary_cleaned = morphology.remove_small_objects(binary.astype(bool), min_size=30)
binary_cleaned = binary_cleaned.astype(np.uint8) * 255  # Convert to uint8 image

# Step 4: Perform morphological closing with a disk structuring element
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
closed = cv2.morphologyEx(binary_cleaned, cv2.MORPH_CLOSE, kernel)

# Step 5: Fill the holes in binary image
filled = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel)

# Step 6: Label connected components
label_image = measure.label(filled)

# Step 7: Measure properties of each region (area, perimeter, circularity)
props = regionprops(label_image)

# Initialize variables for storing the largest round object
max_area = 0
largest_round_object = None

# Display the original image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Round Objects with Circularity')
plt.axis('off')

# Step 8: Loop through each region to calculate and display circularity for each object
for prop in props:
    area = prop.area
    perimeter = prop.perimeter
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

    # Mark the centroid of the object
    centroid = prop.centroid
    plt.plot(centroid[1], centroid[0], 'ro', markersize=5)  # Mark the centroid

    # Display the circularity value next to each object
    plt.text(centroid[1], centroid[0] + 25, f'{circularity:.2f}', color='yellow', fontsize=10, fontweight='bold')

    # Check if the object is round based on circularity
    if circularity > 0.9:
        # Find the largest round object
        if area > max_area:
            max_area = area
            largest_round_object = prop

# Step 9: Highlight the largest round object if found
if largest_round_object:
    largest_centroid = largest_round_object.centroid
    plt.plot(largest_centroid[1], largest_centroid[0], 'go', markersize=15)  # Highlight the largest round object in green
    circularity = (4 * np.pi * max_area) / (largest_round_object.perimeter ** 2)
    print(f'Largest round object found with area = {max_area}, circularity = {circularity:.2f}')
else:
    print('No round object found')

# Show the final image with circularity values for all objects
plt.show()
