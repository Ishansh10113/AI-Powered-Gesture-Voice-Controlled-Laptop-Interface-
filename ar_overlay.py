import cv2
from assets import ar_image  # Load an AR image from assets

def display_ar_overlay(frame):
    frame[50:250, 50:250] = ar_image
