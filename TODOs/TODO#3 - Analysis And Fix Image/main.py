import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_image_type(image):
    """Determine if the image is binary, grayscale or RGB."""
    if len(image.shape) == 2:
        # It's a grayscale image
        return 'Grayscale'
    elif len(image.shape) == 3 and image.shape[2] == 3:
        # It's an RGB image
        return 'RGB'
    else:
        return 'Unknown'

def analyze_histogram(image):
    """Analyze the image histogram to find if it's over dark, over bright, low contrast, or normal."""
    if len(image.shape) == 3:
        # Convert RGB to grayscale for histogram analysis
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    # Calculate histogram
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    # Determine if the image is over dark, over bright, or low contrast
    total_pixels = gray_image.size
    darkness_threshold = total_pixels * 0.9  # 90% of pixels too dark 
    brightness_threshold = total_pixels * 0.7  # 70% of pixels too bright 
    low_contrast_threshold = total_pixels * 0.9  # 90% of pixels concentrated in middle range
    print(total_pixels)
    print(brightness_threshold)
    print(np.sum(hist[190:]))
    if np.sum(hist[:50]) > darkness_threshold:
        return 'Over Dark'
    elif np.sum(hist[180:]) > brightness_threshold:
        return 'Over Bright'
    elif np.sum(hist[50:200]) > low_contrast_threshold:
        return 'Low Contrast'
    else:
        return 'Normal'

def enhance_image(image, issue):
    """Enhance the image depending on the detected issue."""
    if issue == 'Over Dark':
        # Apply brightness and contrast enhancement
        enhanced_image = cv2.convertScaleAbs(image, alpha=1.5, beta=30)  # Increase brightness and contrast
    elif issue == 'Over Bright':
        # Reduce brightness
        enhanced_image = cv2.convertScaleAbs(image, alpha=0.8, beta=-30)
    elif issue == 'Low Contrast':
        # Apply histogram equalization for grayscale images
        if len(image.shape) == 2:
            enhanced_image = cv2.equalizeHist(image)
        else:
            # For RGB, apply histogram equalization on each channel separately
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            enhanced_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        # If the image is normal, no enhancement is applied
        enhanced_image = image

    return enhanced_image


def display_results(original_image, enhanced_image, image_type, issue):
    """Display the original and enhanced images along with their histograms, and show image type and issue on side."""
    # Convert to grayscale if needed for histogram comparison
    if len(original_image.shape) == 3:
        gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        gray_enhanced = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    else:
        gray_original = original_image
        gray_enhanced = enhanced_image

    # Calculate histograms
    hist_original = cv2.calcHist([gray_original], [0], None, [256], [0, 256])
    hist_enhanced = cv2.calcHist([gray_enhanced], [0], None, [256], [0, 256])

    # Create figure with space for additional info
    plt.figure(figsize=(14, 8))  # Wider figure to accommodate text on the side

    # Plot original and enhanced images with their histograms
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(2, 3, 2)
    plt.imshow(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))
    plt.title('Enhanced Image')

    plt.subplot(2, 3, 4)
    plt.plot(hist_original, color='gray')
    plt.title('Original Histogram')

    plt.subplot(2, 3, 5)
    plt.plot(hist_enhanced, color='gray')
    plt.title('Enhanced Histogram')

    # Display text information in a separate subplot
    plt.subplot(2, 3, 3)
    plt.axis('off')  # Turn off axis for the text box
    plt.text(0.5, 0.5, f"Image Type: {image_type}\nIssue: {issue}",
             fontsize=24, ha='center', va='center', wrap=True)
    plt.title("Image Info")

    # Show the final figure with images, histograms, and info
    plt.tight_layout()
    plt.show()
# Sample usage of the updated function
def process_image(image_path):
    """Process the image from the given path."""
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image {image_path}.")
        return

    # Step 1: Identify image type
    image_type = find_image_type(image)
    print(f"Image Type: {image_type}")

    # Step 2: Analyze histogram and find issues
    issue = analyze_histogram(image)
    print(f"Image Issue: {issue}")

    # Step 3: Enhance the image if there's an issue
    enhanced_image = enhance_image(image, issue)

    # Step 4: Display the results with image type and issue
    display_results(image, enhanced_image, image_type, issue)
# Test the program on an image
image_path = 'images/3.png' 
process_image(image_path)
