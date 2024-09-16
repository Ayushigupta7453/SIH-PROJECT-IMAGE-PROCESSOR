# app/utils.py
import cv2
import numpy as np
import os

def calculate_snr(image):
    """
    Calculate the Signal-to-Noise Ratio (SNR) of a grayscale image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    signal = np.mean(gray)
    noise = np.std(gray)
    snr = signal / noise if noise != 0 else float('inf')
    return snr

def adjust_shadows(image):
    """
    Adjust shadows in the image to reduce shadow effect.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    shadow_threshold = 50
    white_threshold = 200

    shadow_mask = gray < shadow_threshold
    white_mask = gray > white_threshold

    kernel = np.ones((15, 15), np.uint8)
    expanded_white_mask = cv2.dilate(white_mask.astype(np.uint8), kernel)

    result_image = image.copy()

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if shadow_mask[y, x] and expanded_white_mask[y, x]:
                result_image[y, x] = [255, 255, 255]

    return result_image

def process_image(image_path):
    """
    Process the image by calculating SNR and adjusting shadows.
    Save the enhanced image and return the SNR values.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    # Calculate SNR before enhancement
    snr_before = calculate_snr(image)
    
    # Adjust shadows
    enhanced_image = adjust_shadows(image)
    
    # Calculate SNR after enhancement
    snr_after = calculate_snr(enhanced_image)
    
    # Define the enhanced image path
    enhanced_image_path = os.path.join('app/static/processed', os.path.basename(image_path))
    
    # Save the enhanced image
    cv2.imwrite(enhanced_image_path, enhanced_image)
    
    return snr_before, snr_after, enhanced_image_path
