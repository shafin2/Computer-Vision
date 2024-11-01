import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_multiotsu

# Step 1: Load the image
image = cv2.imread('tt.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Multi-level thresholding (equivalent to multithresh in MATLAB)
# Use threshold_multiotsu to get two threshold levels (3 regions in total)
thresholds = threshold_multiotsu(gray_image, classes=3)
t1, t2 = thresholds  # Get the two threshold values

# Step 3: Binary thresholding with two levels (equivalent to im2bw in MATLAB)
bL = np.where(gray_image > t1, 1, 0)  # Threshold for Liquid White (lower)
bH = np.where(gray_image > t2, 1, 0)  # Threshold for Liquid Black (higher)

# Step 4: Subtract the binary images to isolate the liquid (Liquid with Noise)
L = bL - bH

# Step 5: Apply median filtering (equivalent to medfilt2 in MATLAB)
L1 = cv2.medianBlur((L * 255).astype(np.uint8), 9)  # Median filter with 9x9 window

# Step 6: Display the results
plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Bottles')

plt.subplot(2, 3, 2)
plt.imshow(bL, cmap='gray')
plt.title('Liquid White')

plt.subplot(2, 3, 3)
plt.imshow(bH, cmap='gray')
plt.title('Liquid Black')

plt.subplot(2, 3, 4)
plt.imshow(L, cmap='gray')
plt.title('Liquid with Noise')

plt.subplot(2, 3, 5)
plt.imshow(L1, cmap='gray')
plt.title('Pure Liquid')

plt.show()
