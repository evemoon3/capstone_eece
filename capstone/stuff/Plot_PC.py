import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import re  # Regular expression for parsing matrices


def plot_points():
    # Load the point cloud data from the text file
    file_path = "downloaded_file.txt"  # FILENAME

    # Read the entire file and remove header
    with open(file_path, "r") as f:
        file_content = f.read().strip()

    # Extract all matrix blocks using regex
    matrix_blocks = re.findall(r"\[\s*([\s\S]+?)\s*\]", file_content)

    # Convert extracted matrices into NumPy arrays
    point_cloud_data = []
    for block in matrix_blocks:
        try:
            # Clean up the block: remove any non-numeric characters except for digits, periods, minus signs, and 'e' for scientific notation
            cleaned_block = re.sub(r'[^\d\s\.\-e]', '', block)

            # Convert multiline text block into a NumPy array
            matrix = np.array(
                [[float(num) for num in line.split()] for line in cleaned_block.split("\n") if line.strip()])
            point_cloud_data.append(matrix)
        except Exception as e:
            print(f"Error processing matrix block:\n{block}\n{e}")

    # Flatten list of matrices into a single NumPy array
    if point_cloud_data:
        point_cloud_data = np.vstack(point_cloud_data)
    else:
        raise ValueError("No valid point cloud data found.")

    # Extract X, Y, Z coordinates
    X = point_cloud_data[:, 0]
    Y = point_cloud_data[:, 1]
    Z = point_cloud_data[:, 2]

    # Limit number of points
    X = X[:]
    Y = Y[:]
    Z = Z[:]

    # Find the min and max values across all axes
    min_value = min(X.min(), Y.min(), Z.min())
    max_value = max(X.max(), Y.max(), Z.max())

    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D scatter
    ax.scatter(X, Y, Z, c=Z, cmap='viridis', s=5)  # Adjust size 's' for visibility

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set axis limits to the same range
    ax.set_xlim([min_value, max_value])
    ax.set_ylim([min_value, max_value])
    ax.set_zlim([min_value, max_value])

    # Title
    ax.set_title('3D Point Cloud Plot')

    # Save the figure instead of showing it
    output_filename = "point_cloud_plot.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # Save as high-quality PNG

    return output_filename
    # Show plot
    # plt.show()
