# main.py
import os
import numpy as np
import tensorflow as tf
from PIL import Image as PILImage
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')

class HomeScreen(Screen):
    pass

class StyleScreen(Screen):
    def select_content_image(self):
        self._open_file_chooser(is_style=False)

    def select_style_image(self):
        self._open_file_chooser(is_style=True)

    def _open_file_chooser(self, is_style):
        layout = BoxLayout(orientation='vertical', spacing=10)
        chooser = FileChooserIconView()
        layout.add_widget(chooser)

        def load_file(instance):
            if chooser.selection:
                path = chooser.selection[0]
                if is_style:
                    App.get_running_app().style_image = path
                    if App.get_running_app().content_image:
                        self.manager.current = 'displayscreen'
                else:
                    App.get_running_app().content_image = path

                popup.dismiss()

        select_btn = Button(text="Select", size_hint_y=None, height=50)
        select_btn.bind(on_release=load_file)
        layout.add_widget(select_btn)

        popup = Popup(title="Select Image", content=layout, size_hint=(0.9, 0.9))
        popup.open()

    def set_style(self, path):
        App.get_running_app().style_image = path
        if App.get_running_app().content_image:
            self.manager.current = 'displayscreen'

class DisplayScreen(Screen):
    def on_enter(self):
        content_path = App.get_running_app().content_image
        style_path = App.get_running_app().style_image

        if content_path and style_path:
            content_image = self.load_and_process_image(content_path)
            style_image = self.load_and_process_image(style_path)

            interpreter = tf.lite.Interpreter(model_path="stylization_model.tflite")
            interpreter.allocate_tensors()

            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            interpreter.set_tensor(input_details[0]['index'], content_image)
            interpreter.set_tensor(input_details[1]['index'], style_image)

            interpreter.invoke()

            stylized_image = interpreter.get_tensor(output_details[0]['index'])[0]
            output_image = (np.clip(stylized_image, 0, 1) * 255).astype(np.uint8)
            img = PILImage.fromarray(output_image)

            save_path = os.path.join(os.getcwd(), 'styled_result.jpg')
            img.save(save_path)

            # Force reload to avoid caching
            self.ids.result_image.source = ''
            self.ids.result_image.source = save_path
            self.ids.result_image.reload()

    def load_and_process_image(self, path):
        img = PILImage.open(path).convert('RGB').resize((256, 256))
        img = np.array(img).astype(np.float32) / 255.0
        return np.expand_dims(img, axis=0)

    def download_image(self):
        src = os.path.join(os.getcwd(), 'styled_result.jpg')
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "styled_image"
        ext = ".jpg"
        count = 1
        dest = os.path.join(download_dir, base_name + ext)

        while os.path.exists(dest):
            dest = os.path.join(download_dir, f"{base_name}({count}){ext}")
            count += 1

        if os.path.exists(src):
            from shutil import copyfile
            copyfile(src, dest)
            print(f"✅ Saved to: {dest}")

class ClickableImage(ButtonBehavior, Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    content_image = ''
    style_image = ''

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()
