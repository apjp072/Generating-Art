import cairo
import numpy as np
import random
import cv2

# Parameters
line_thickness = 1
grid_spacing = 2.5 * line_thickness
grid_size = 21  # An odd number
# Create the grid
grid = np.zeros((grid_size, grid_size), dtype=int)

def create_grid_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load the image")

    height, width, _ = image.shape
    grid_rows = int(np.ceil(height / grid_spacing))
    grid_cols = int(np.ceil(width / grid_spacing))

    return np.zeros((grid_rows, grid_cols), dtype=int), image

def select_random_point(center, min_dist, max_dist, grid_size_x, grid_size_y):
    while True:
        angle = random.uniform(0, 2 * np.pi)
        r = random.uniform(min_dist, max_dist)
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        if 0 <= x < grid_size_x and 0 <= y < grid_size_y:
            return (x, y)

# Select the initial points
center_point = (grid_size // 2, grid_size // 2)
# Inside the main function loop
random_point = select_random_point(center_point, 2, 10, len(grid[0]), len(grid))


print("Initial Point:", center_point)
print("Random Point:", random_point)

def color_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def is_similar_color(image, point1, point2, threshold=30):
    color1 = image[point1[1]][point1[0]]  # Note: OpenCV uses y, x format
    color2 = image[point2[1]][point2[0]]
    return color_distance(color1, color2) < threshold

def find_path(image, start, end ,grid_size_x, grid_size_y):
    # Basic pathfinding implementation
    # A more sophisticated algorithm may be needed for complex images
    path = [start]
    current = start
    while current != end:
        # Placeholder for actual pathfinding logic
        # For now, move one step towards 'end'
        step = (np.sign(end[0] - current[0]), np.sign(end[1] - current[1]))
        next_step = (current[0] + step[0], current[1] + step[1])
        if not is_similar_color(image, current, next_step):
            break
        current = next_step
        path.append(current)
    return path

def draw_path(grid, path):
    for point in path:
        grid[point[0]][point[1]] = 1  # Mark the path on the grid

def visualize_grid(grid, image, line_thickness):
    # Create an empty image with the same dimensions as the original
    visualization = np.zeros_like(image)

    # Set the color for the lines
    line_color = (0, 255, 0)  # Green color

    # Iterate over the grid and draw lines where the grid is marked
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y][x] == 1:
                cv2.circle(visualization, (int(x * grid_spacing), int(y * grid_spacing)), line_thickness, line_color, -1)

    # Display the image
    cv2.imshow('Grid Visualization', visualization)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optionally, save the visualization
    cv2.imwrite('grid_visualization.jpg', visualization)

def find_extension_points(grid):
    # Find points on the grid that are part of existing paths
    extension_points = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                extension_points.append((x, y))
    return extension_points

def render_with_cairo(grid, image):
    height, width, _ = image.shape
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                color = image[y * grid_spacing][x * grid_spacing] / 255.0
                ctx.set_source_rgb(color[2], color[1], color[0])  # Convert BGR to RGB
                ctx.rectangle(x * grid_spacing, y * grid_spacing, line_thickness, line_thickness)
                ctx.fill()

    surface.write_to_png("output.png")  # Save to file


def main():
    image_path = 'V2/starry-night-test.jpg'  # Replace with your image path
    grid, image = create_grid_from_image(image_path)

    num_paths = 10  # Number of paths to create

    for _ in range(num_paths):
        extension_points = find_extension_points(grid)
        if extension_points:
            start_point = random.choice(extension_points)
        else:
            # Select a completely new point if no extensions are available
            center_x = random.randint(0, len(grid[0]) - 1)
            center_y = random.randint(0, len(grid) - 1)
            start_point = (center_x, center_y)

        random_point = select_random_point(start_point, 2, 10, len(grid[0]), len(grid))

        if is_similar_color(image, start_point, random_point):
            path = find_path(image, start_point, random_point, len(grid[0]), len(grid))
            draw_path(grid, path)

    render_with_cairo(grid, image)

if __name__ == "__main__":
    main()
