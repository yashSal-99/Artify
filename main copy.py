
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
import shutil
import os
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

Builder.load_file('design.kv')
class HomeScreen(Screen):
    pass

class StyleScreen(Screen):
    def select_content(self):
        self.open_file_chooser('content')

    def select_style(self):
        self.open_file_chooser('style')

    def open_file_chooser(self, image_type):
        layout = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
        layout.add_widget(filechooser)
        def load_file(instance):
            selected = filechooser.selection[0]
            if image_type == 'content':
                App.get_running_app().content_image = selected
            else:
                App.get_running_app().style_image = selected
            popup.dismiss()
            if App.get_running_app().content_image and App.get_running_app().style_image:
                self.manager.current = "result"
        load_btn = Button(text="Load", size_hint_y=None, height=50)
        load_btn.bind(on_release=load_file)
        layout.add_widget(load_btn)
        popup = Popup(title='Choose Image', content=layout, size_hint=(0.9, 0.9))
        popup.open()

    def set_style(self, style_path):
        App.get_running_app().style_image = style_path
        if App.get_running_app().content_image:
            self.manager.current = "result"

class ResultScreen(Screen):
    def on_enter(self):
        self.ids.result_image.source = App.get_running_app().content_image

    def download_image(self):
        src = App.get_running_app().content_image
        dst = os.path.join(os.path.expanduser("~"), "Downloads", "styled_image.jpg")
        shutil.copy(src, dst)

class ArtifyApp(App):
    content_image = ''
    style_image = ''

    def build(self):
        return ScreenManager()

if __name__ == '__main__':
    ArtifyApp().run()
