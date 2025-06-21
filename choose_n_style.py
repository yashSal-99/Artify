# Step 1: Install dependencies (run this once in your terminal)
# pip install tensorflow tensorflow_hub matplotlib pillow

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import Tk, filedialog

# Suppress TF logging
tf.get_logger().setLevel('ERROR')

# Step 2: Function to open file dialog and choose image
def choose_image(title="Select an image"):
    root = Tk()
    root.withdraw()  # Hide Tk window
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    return file_path

# Step 3: Image preprocessing
def load_and_process_image(img_path):
    img = Image.open(img_path).convert("RGB").resize((256, 256))
    img_array = np.array(img) / 255.0
    return tf.expand_dims(tf.convert_to_tensor(img_array, dtype=tf.float32), axis=0)

# Step 4: Load the TF Hub model
print("Loading model...")
model = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")

# Step 5: Choose images
print("Choose a CONTENT image")
content_path = choose_image("Choose content image")
print("Choose a STYLE image")
style_path = choose_image("Choose style image")

# Step 6: Process and transfer
content_image = load_and_process_image(content_path)
style_image = load_and_process_image(style_path)
stylized_image = model(content_image, style_image)[0]

# Step 7: Show results
def display_images(content, style, output):
    plt.figure(figsize=(15, 5))
    titles = ['Content', 'Style', 'Stylized']
    images = [content[0], style[0], output[0]]
    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.title(titles[i])
        plt.imshow(images[i])
        plt.axis('off')
    plt.tight_layout()
    plt.show()

display_images(content_image, style_image, stylized_image)
