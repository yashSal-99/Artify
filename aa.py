import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt

# Load and preprocess image
def load_and_process_image(path):
    img = Image.open(path).convert('RGB').resize((256, 256))
    img = np.array(img).astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)

# Load images
content_image = load_and_process_image("1.jpg")  # your content image
style_image = load_and_process_image("Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg")      # your style image

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="stylization_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set inputs
interpreter.set_tensor(input_details[0]['index'], content_image)
interpreter.set_tensor(input_details[1]['index'], style_image)

# Run inference
interpreter.invoke()

# Get output
stylized_image = interpreter.get_tensor(output_details[0]['index'])[0]

# Show result
plt.imshow(np.clip(stylized_image, 0, 1))
plt.title("Stylized Output")
plt.axis('off')
plt.show()
