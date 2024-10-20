import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('images/liftingbody.png', cv2.IMREAD_GRAYSCALE)

# 1. Contrast Stretching (for Result 1)
def contrast_stretching(img):
    a = np.min(img)
    b = np.max(img)
    stretched = ((img - a) / (b - a)) * 255
    return stretched.astype(np.uint8)

# 2. Negative Transformation (for Result 2)
def negative_transformation(img):
    neg_img = 255 - img
    return neg_img

# 3. Gamma Correction (for Result 3)
def gamma_correction(img, gamma):
    invGamma = 1 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

# 4. Log Transformation (for Result 4)
def log_transformation(img):
    c = 255 / np.log(1 + np.max(img))
    log_img = c * (np.log(img + 1))
    return np.array(log_img, dtype=np.uint8)

# Apply transformations
result1 = negative_transformation(image)
result2 = gamma_correction(image, gamma=0.5)  # Gamma < 1 for darkening
result3 = log_transformation(image)
result4 = contrast_stretching(image)

# Display results
images = [image, result1, result2, result3, result4]
titles = ['Original', 'Result 1 (Negative)', 
          'Result 2 (Gamma Correction)', 'Result 3 (Log Transformation)', 'Result 4 (Contrast Stretching)']

plt.figure(figsize=(10,10))
for i in range(5):
    plt.subplot(2, 3, i+1), plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()
