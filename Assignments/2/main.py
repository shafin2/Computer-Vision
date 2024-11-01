import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the image
img = cv2.imread("a.png")

# Step 2: Convert the image from BGR to YCbCr color space
img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# Step 3: Define the skin color range in YCbCr color space
# Cr: 135-180, Cb: 85-135
lower_skin = np.array([0, 135, 85], dtype=np.uint8)  # Lower bound for skin color
upper_skin = np.array([255, 180, 135], dtype=np.uint8)  # Upper bound for skin color

# Step 4: Create a binary mask for skin colors
skin_mask = cv2.inRange(img_YCrCb, lower_skin, upper_skin)

# Step 5: Apply morphological operations to reduce noise
# Applying morphological opening to remove small noise in the mask
kernel = np.ones((3, 3), np.uint8)
skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)

# Step 6: Apply morphological closing to fill small holes
skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)

# Step 7: Segment the skin area from the original image using the mask
skin_segmented = cv2.bitwise_and(img, img, mask=skin_mask)

# Step 8: Convert the original BGR image to RGB for displaying with Matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_YCrCb_rgb = cv2.cvtColor(img_YCrCb, cv2.COLOR_YCrCb2RGB)  # Convert YCbCr to RGB
skin_segmented_rgb = cv2.cvtColor(skin_segmented, cv2.COLOR_BGR2RGB)

# Step 9: Create subplots to display the original image, YCbCr image, mask, and segmented skin image
fig, axs = plt.subplots(1, 4, figsize=(20, 5))

# Step 10: Display the original image
axs[0].imshow(img_rgb)
axs[0].set_title("Original Image")
axs[0].axis('off')  # Hide the axes for a cleaner look

# Step 11: Display the YCbCr image
axs[1].imshow(img_YCrCb_rgb)
axs[1].set_title("YCbCr Image")
axs[1].axis('off')

# Step 12: Display the skin mask result
axs[2].imshow(skin_mask, cmap='gray')  # Use a grayscale colormap
axs[2].set_title("Skin Mask")
axs[2].axis('off')

# Step 13: Display the segmented skin image
axs[3].imshow(skin_segmented_rgb)
axs[3].set_title("Segmented Skin Image")
axs[3].axis('off')

# Step 14: Show all plots
plt.show()
