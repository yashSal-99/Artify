import tensorflow as tf
import tensorflow_hub as hub

# Load TF Hub style transfer model
hub_model = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")

# Wrapper module to fix input shapes
class StyleTransferWrapper(tf.Module):
    def __init__(self):
        super().__init__()
        self.model = hub_model

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[1, 256, 256, 3], dtype=tf.float32, name='content_image'),
        tf.TensorSpec(shape=[1, 256, 256, 3], dtype=tf.float32, name='style_image'),
    ])
    def stylize(self, content_image, style_image):
        outputs = self.model(content_image, style_image)
        return {'stylized_image': outputs[0]}

model = StyleTransferWrapper()

# Save with correct function signature
tf.saved_model.save(model, "style_saved_model",
                    signatures=model.stylize.get_concrete_function())
converter = tf.lite.TFLiteConverter.from_saved_model("style_saved_model")
tflite_model = converter.convert()

with open("stylization_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Model converted successfully!")



interpreter = tf.lite.Interpreter(model_path="stylization_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
for i, d in enumerate(input_details):
    print(f"Input {i}: shape = {d['shape']}, dtype = {d['dtype']}")
