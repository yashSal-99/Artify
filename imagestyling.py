import tensorflow_hub as hub
import tensorflow as tf
import matplotlib.pyplot as plt

# Load model
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.resize(img, [256, 256])
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, axis=0)
    return img

def run_style_transfer(content_path, style_path):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    # Display
    plt.figure(figsize=(10,5))
    images = [content_image[0], style_image[0], stylized_image[0]]
    titles = ['Content', 'Style', 'Stylized']
    for i in range(3):
        plt.subplot(1, 3, i+1)
        plt.title(titles[i])
        plt.imshow(images[i])
        plt.axis('off')
    plt.show()

run_style_transfer('2.jpg', 'picasso2.jpg')
