import cv2
import matplotlib.pyplot as plt
import numpy as np

# Convert image to grayscale
def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display image using matplotlib
def show_image(image, is_gray=False):
    plt.figure(figsize=(6, 6))
    if is_gray:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Sharpen the image to enhance edges
def sharpen_image(image):
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    return cv2.filter2D(image, -1, sharpening_kernel)

# Apply fixed thresholding for segmentation
def apply_threshold(image, threshold_value=110):
    _, thresh_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    return thresh_image

# Apply Canny edge detection
def find_edges_canny(image, low_threshold=50, high_threshold=150):
    return cv2.Canny(image, low_threshold, high_threshold)

# Apply morphological operations (closing gaps)
def apply_morphology(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# Detect and label partially filled glasses
def detect_and_label_glasses(original_image, thresh_image):
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    glass_count = 0
    partially_filled_count = 0

    # Loop over each contour (each glass)
    for contour in contours:
        # Get the bounding rectangle for the current contour
        x, y, w, h = cv2.boundingRect(contour)

        # Extract the glass region from the thresholded image
        glass_region = thresh_image[y:y+h, x:x+w]

        # Calculate total area and filled area (white pixels in thresholded image)
        total_area = w * h
        filled_area = cv2.countNonZero(glass_region)  # Count non-zero pixels (white)

        # If the filled area is less than 80% of the total area, classify as "Partially Filled"
        if filled_area < total_area * 0.8:
            label = "Partially Filled"
            partially_filled_count += 1
        else:
            label = "Fully Filled"

        glass_count += 1

        # Draw the bounding rectangle and label on the original image
        cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(original_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the final image with labels
    show_image(original_image)

    # Print the counts of glasses
    print(f"Total Glasses Detected: {glass_count}")
    print(f"Partially Filled Glasses: {partially_filled_count}")

# Main processing function
def process_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # 1. Convert to grayscale
    grayscale_image = convert_to_grayscale(image)

    # 2. Sharpen the image
    sharpened_image = sharpen_image(grayscale_image)

    # 3. Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(sharpened_image, (3, 3), 0)

    # 4. Apply fixed thresholding to segment glasses
    threshold_value = 120  # You can experiment with this value
    thresh_image = apply_threshold(blurred, threshold_value)
    show_image(thresh_image, True)

    # 5. Apply morphology to close gaps and smoothen
    morphed_image = apply_morphology(thresh_image)
    show_image(morphed_image, True)

    # 6. Detect and label the glasses
    detect_and_label_glasses(image, morphed_image)

# Run the function on your image
process_image('main.jpg')
