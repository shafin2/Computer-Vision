import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_multiotsu

# Step 1: Load the image (replace 'main4.png' with your actual image)
image = cv2.imread('main5.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Apply multi-level Otsu thresholding to get two threshold values
thresholds = threshold_multiotsu(gray_image, classes=3)
t1, t2 = thresholds

# Step 3: Binary thresholding for bottle and liquid detection
bL = np.where(gray_image > t1, 1, 0)  # Lower threshold for bottles
bH = np.where(gray_image > t2, 1, 0)  # Higher threshold for liquid
liquid_mask = bL - bH  # Liquid region
liquid_mask = (liquid_mask * 255).astype(np.uint8)  # Convert to binary mask

# Step 4: Create bottle mask
bottel_mask = np.where(gray_image > t1, 1, 0)
bottel_mask = (bottel_mask * 255).astype(np.uint8)

# Step 5: Morphological closing to reduce noise in the liquid region
kernel = np.ones((5, 5), np.uint8)
liquid_clean = cv2.morphologyEx(liquid_mask, cv2.MORPH_CLOSE, kernel)  # Clean the liquid mask
refined_mask = cv2.erode(liquid_clean, kernel, iterations=2)

# Step 6: Find contours for all bottles in the bottle mask
contours, _ = cv2.findContours(bottel_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize counters for total bottles and bottles with liquid
total_bottles = 0
bottles_with_liquid = 0

# Step 7: Loop over bottle contours to count total bottles
for contour in contours:
    # Calculate contour area and filter out small contours (e.g., noise)
    area = cv2.contourArea(contour)
    if area < 1000:
        continue
    # Increment total bottle count
    total_bottles += 1

# Step 8: Find contours for liquid-filled regions using the refined mask
contours_liquid, _ = cv2.findContours(refined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 9: Loop over liquid contours to detect and label bottles
for contour in contours_liquid:
    # Calculate contour area and filter out small contours (e.g., noise)
    area = cv2.contourArea(contour)
    if area < 1000:
        continue

    # Get bounding box for each liquid-filled region
    x, y, w, h = cv2.boundingRect(contour)

    # Extract bottle region from the liquid_clean binary image
    bottle_region = liquid_clean[y:y+h, x:x+w]

    # Calculate the height of the liquid by finding non-zero rows in the region
    non_zero_rows = np.any(bottle_region > 0, axis=1)
    
    # If there are non-zero rows (indicating liquid), calculate liquid height
    if np.any(non_zero_rows):
        highest_liquid_level = np.argmax(non_zero_rows)  # First row with liquid
        lowest_liquid_level = len(non_zero_rows) - np.argmax(non_zero_rows[::-1])  # Last row with liquid
        liquid_height = lowest_liquid_level - highest_liquid_level

        # Calculate the percentage of the bottle filled with liquid
        fill_percentage = (liquid_height / 520) * 100

        # Increment count for bottles with liquid
        bottles_with_liquid += 1

        # Label the bottle as partially or fully filled
        if fill_percentage < 90:
            label = f"Partially Filled ({fill_percentage:.1f}%)"
        else:
            label = f"Full ({fill_percentage:.1f}%)"
    else:
        # If no liquid is detected, the bottle is empty
        fill_percentage = 0
        label = "Empty"

    # Draw bounding box and label the bottle
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Step 10: Print results and show the labeled image
print(f"Total bottles detected: {total_bottles}")
print(f"Bottles with liquid detected: {bottles_with_liquid}")

# Display the image with labels
plt.figure(figsize=(10, 8))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Bottles with Liquid Levels')
plt.axis('off')
plt.show()
