import cv2
import numpy as np

def load_and_process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load the image from the provided path.")

    # Convert to grayscale for contour detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth out the image
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Detect edges using Canny edge detector
    edged = cv2.Canny(blurred_image, 50, 50)

    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return image, contours

def main():
    image_path = 'V1/starry-night-test.jpg'  # Replace with your image path
    image, contours = load_and_process_image(image_path)

    # For visualization: draw contours on the original image
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Contours", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
