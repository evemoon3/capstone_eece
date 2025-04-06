from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests

server_start = "18.188.244.245"


def indexView(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def outputView(request):
    template = loader.get_template('output.html')
    server_url = f"http://{server_start}:80/get"
    response = requests.get(server_url)
    print("Received number:", response.json())
    output = response.json()['numb_preset']
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def plot_page(request):
    template = loader.get_template('output.html')
    # stop all things for first
    url = f"http://{server_start}:80/set_start"
    response1 = requests.post(url, json={"start": False})
    url = f"http://{server_start}:80/set_start_video"
    response2 = requests.post(url, json={"start": False})
    url = f"http://{server_start}:80/set_start_radar"
    response3 = requests.post(url, json={"start": False})
    print(f"STARTING, {response1.status_code}, {response2.status_code}, {response3.status_code}")

    output = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))




def downloaded_file(request):
    template = loader.get_template('output.html')
    url = f"http://{server_start}:80/download/point_cloud.txt"
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        with open("downloaded_file.txt", "wb") as f:
            f.write(response.content)
        print("File downloaded successfully!")
    else:
        print("Error:", response.json())
    img_file = plot_points()

    output = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))



# get it to display the img

# # file upload
# url = "http://3.142.77.213:80/upload"
# file_path = "point_cloud2.txt"
#
# with open(file_path, "rb") as file:
#     files = {"file": file}
#     response = requests.post(url, files=files)
#
# print("done")
# print(response.status_code)
# print(response.text)
#
#
# # file download
# url = "http://13.59.189.77:80/download/point_cloud.txt"  # Replace with actual file name
# response = requests.get(url)
# print(response.status_code)
#
# if response.status_code == 200:
#     with open("downloaded_file.txt", "wb") as f:
#         f.write(response.content)
#     print("File downloaded successfully!")
# else:
#     print("Error:", response.json())







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
    output_filename = "./stuff/static/point_cloud_plot.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # Save as high-quality PNG

    return output_filename
    # Show plot
    # plt.show()


from django.http import JsonResponse


def start_button(request):
    print("SENDING START REQ")
    server_url = f"http://{server_start}:80/set_start"
    response = requests.post(server_url, json={"start": True})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def stop_button(request):
    print("SENDING STOP REQ")
    server_url = f"http://{server_start}:80/set_start"
    response = requests.post(server_url, json={"start": False})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def start_video_button(request):
    print("SENDING START VIDEO REQ")
    server_url = f"http://{server_start}:80/set_start_video"
    response = requests.post(server_url, json={"start": True})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def stop_video_button(request):
    print("SENDING STOP VIDEO REQ")
    server_url = f"http://{server_start}:80/set_start_video"
    response = requests.post(server_url, json={"start": False})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

def start_radar_button(request):
    print("SENDING START RADAR REQ")
    server_url = f"http://{server_start}:80/set_start_radar"
    response = requests.post(server_url, json={"start": True})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def stop_radar_button(request):
    print("SENDING STOP RADAR REQ")
    server_url = f"http://{server_start}:80/set_start_radar"
    response = requests.post(server_url, json={"start": False})
    print("Recieved: ", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def new_img(request):
    url = f"http://{server_start}:80/download/point_cloud.txt"
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        with open("downloaded_file.txt", "wb") as f:
            f.write(response.content)
        print("File downloaded successfully!")
    else:
        print("Error:", response.json())
    img_file = plot_points()
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})



def video_stream(request):
    template = loader.get_template('video_stuff.html')
    url = "http://<YOUR_FLASK_SERVER_IP>:5000/video_feed"
    context = {
        'output': server_start,
    }
    return HttpResponse(template.render(context, request))


def radar_img(request):
    url = f"http://{server_start}:80/download_img"
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        with open("./stuff/static/radar_plot.png", "wb") as f:
            f.write(response.content)
        print("Radar Img downloaded successfully!")
    else:
        print("Error:", response.json())
    return JsonResponse({"message": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

def get_radar_room_state(request):
    print("RADAR ROOM STATE")
    server_url = f"http://{server_start}:80/is_radar_room"
    response = requests.get(server_url)
    print("Recieved: ", response.json())
    return JsonResponse({"message": response.json()["radar"]})