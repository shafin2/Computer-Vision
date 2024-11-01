import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Open a simple image from the specified file
img = cv2.imread("d.png")

# Step 2: Convert the image from BGR (Blue, Green, Red) to HSV (Hue, Saturation, Value) color space
# The HSV color space is often more effective for color-based segmentation as it separates color information (hue) from intensity (value).
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Step 3: Create a skin color mask in the HSV color space
# a. Define the skin color range in the HSV color space and create a mask
HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17, 170, 255))

# b. Apply morphological opening to remove small noise in the HSV mask
HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

# Step 4: Convert the original image from BGR to YCbCr color space
# The YCbCr color space separates luminance from chrominance, which can enhance skin detection in certain lighting conditions.
img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# Step 5: Create a skin color mask in the YCbCr color space
# a. Define the skin color range in the YCbCr color space and create a mask
YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255, 180, 135))

# b. Apply morphological opening to the YCbCr mask to remove small noise
YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

# Step 6: Merge the two skin detection masks (from YCbCr and HSV color spaces) using bitwise AND
# This step combines the strengths of both color spaces to improve skin detection accuracy.
global_mask = cv2.bitwise_and(YCrCb_mask, HSV_mask)

# Step 7: Apply median blur to smooth the global mask
global_mask = cv2.medianBlur(global_mask, 3)

# Step 8: Apply morphological opening to the global mask to remove small noise
global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))

# Step 9: Invert the masks to highlight skin areas in white
HSV_result = cv2.bitwise_not(HSV_mask)
YCrCb_result = cv2.bitwise_not(YCrCb_mask)
global_result = cv2.bitwise_not(global_mask)

# Step 10: Convert the original BGR image to RGB for displaying with Matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Step 11: Create a subplot to display multiple images
fig, axs = plt.subplots(1, 4, figsize=(20, 5))

# Step 12: Display the original image in the first subplot
axs[0].imshow(img_rgb)
axs[0].set_title("Original Image")
axs[0].axis('off')  # Hide the axes for a cleaner look

# Step 13: Display the HSV mask result in the second subplot
axs[1].imshow(HSV_result, cmap='gray')  # Use a grayscale colormap
axs[1].set_title("HSV Mask Result")
axs[1].axis('off')

# Step 14: Display the YCbCr mask result in the third subplot
axs[2].imshow(YCrCb_result, cmap='gray')  # Use a grayscale colormap
axs[2].set_title("YCbCr Mask Result")
axs[2].axis('off')

# Step 15: Display the global mask result in the fourth subplot
axs[3].imshow(global_result, cmap='gray')  # Use a grayscale colormap
axs[3].set_title("Combine Result")
axs[3].axis('off')

# Step 16: Show all the plots
plt.show()
