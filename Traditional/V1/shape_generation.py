import cv2
import numpy as np
import cairo
from image_processing import load_and_process_image

def generate_shapes(image, contours):
    # Initialize a Pycairo surface
    height, width, _ = image.shape
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Set line width for shapes
    line_width = 4  # Adjust as needed
    ctx.set_line_width(line_width)
    
    drawn_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    for contour in contours:
        # Increase epsilon for smoother shapes
        epsilon = 0.05 * cv2.arcLength(contour, True)  # Adjust this value as needed
        approx = cv2.approxPolyDP(contour, epsilon, True)


        # Create a mask for the contour
        test_mask = np.zeros_like(drawn_mask)
        cv2.drawContours(test_mask, [approx], -1, 255, -1)
        if np.any(np.bitwise_and(drawn_mask, test_mask)):
            continue  # Skip this contour if it overlaps
        
        # Get the color from the contour area in the original image
        mean_color = cv2.mean(image, mask=test_mask)[:3]

        # Convert color to RGB (OpenCV uses BGR format)
        mean_color = mean_color[::-1]

        # Draw hollow shapes
        ctx.set_source_rgb(mean_color[0]/255, mean_color[1]/255, mean_color[2]/255)
        for i in range(len(approx)):
            if i == 0:
                ctx.move_to(approx[i][0][0], approx[i][0][1])
            else:
                # Using bezier curves for smoother transitions
                p1 = approx[i - 1][0]
                p2 = approx[i][0]
                cx, cy = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
                ctx.curve_to(p1[0], p1[1], cx, cy, p2[0], p2[1])
                
        ctx.close_path()
        ctx.stroke()  # Only stroke the path, do not fill

        # Update the drawn mask 
        cv2.drawContours(drawn_mask, [approx], -1, 255, -1)
        
    # Save the result to a file
    surface.write_to_png("output4.png")


def main():
    # Load the image and contours from the previous step
    image_path = 'starry-night-test.jpg'  # Replace with your image path
    image, contours = load_and_process_image(image_path)

    # Generate and render shapes
    generate_shapes(image, contours)

if __name__ == "__main__":
    main()
