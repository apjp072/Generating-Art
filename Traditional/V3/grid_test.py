import cv2
import numpy as np
import cairo
import math

def create_grid(image, rows, cols):
    height, width, _ = image.shape
    grid = []
    for i in range(rows):
        for j in range(cols):
            grid.append((int(j * width / cols), int(i * height / rows)))
    return grid

def color_difference(color1, color2):
    return math.sqrt(sum([(float(a) - float(b)) ** 2 for a, b in zip(color1, color2)]))

def extend_until_color_change(image, drawn_grid, point, direction, threshold):
    height, width, _ = image.shape
    x, y = point
    dx, dy = direction

    while 0 <= x < width and 0 <= y < height:
        if drawn_grid[y, x] == 1:  # Check if the point is already drawn
            return (x - dx, y - dy)  # Return the last valid point before the drawn point

        if color_difference(image[y, x], image[point[1], point[0]]) > threshold:
            drawn_grid[y, x] = 1  # Mark the point as drawn
            return (x, y)

        x += dx
        y += dy

    return point

def draw_points_and_connect(surface, drawn_grid, points, color):
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(color[0], color[1], color[2])

    # Move to the first point
    ctx.move_to(points[0][0], points[0][1])

    # Draw lines to other points in the specific order and connect them
    order = [0, 1, 2, 3, 0]  # Indices for the directions
    for i in order:
        x, y = points[i]
        ctx.line_to(x, y)
        drawn_grid[y, x] = 1  # Mark the entire line as drawn
    ctx.stroke()

def main():
    image_path = 'V3/box-test.png' # the path to the input image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load the image")

    # Convert image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rows, cols = 50, 60
    color_change_threshold = 40  # A higher threshold means more leeway 

    grid = create_grid(image_rgb, rows, cols)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Cardinal directions (for now)

    height, width, _ = image_rgb.shape
    drawn_grid = np.zeros((height, width), dtype=int)  # Track drawn points

    # Create a Cairo surface and context
    surface_with_image = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx_with = cairo.Context(surface_with_image)

    surface_without_image = cairo.ImageSurface(cairo.FORMAT_ARGB32, image.shape[1], image.shape[0])
    ctx_without = cairo.Context(surface_without_image)

    # Draw the original image onto the surface
    for y in range(height):
        for x in range(width):
            pixel = image_rgb[y, x]
            ctx_with.set_source_rgb(pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0)
            ctx_with.rectangle(x, y, 1, 1)
            ctx_with.fill()

  
    for point in grid:
        extension_points = [extend_until_color_change(image_rgb, drawn_grid, point, direction, color_change_threshold) for direction in directions]
        color = [c / 255.0 for c in image_rgb[point[1], point[0]]]

        # Draw points and connect them on both surfaces
        draw_points_and_connect(surface_without_image, drawn_grid, extension_points, color)
        
                

    
    surface_with_image.write_to_png("boxes_with_image.png")  # Save to file
    surface_without_image.write_to_png("boxes_without_image.png")  # Save to file
    
if __name__ == "__main__":
    main()
