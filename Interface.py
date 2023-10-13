from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import main

# Import the rest of your code here

class MangaDownloaderApp(App):
    def build(self):
        self.title = 'Manga Downloader'

        layout = BoxLayout(orientation='vertical')

        self.name_input = TextInput(hint_text='Enter the manga name')
        self.select_page_input = TextInput(hint_text='Enter the starting page')
        self.download_button = Button(text='Download Manga')
        self.download_button.bind(on_press=self.download_manga)

        layout.add_widget(self.name_input)
        layout.add_widget(self.select_page_input)
        layout.add_widget(self.download_button)
        return layout

    def download_manga(self, instance):
        main.download_images(self.name_input.text, self.select_page_input.text)
        # Call your download_images function here with name_manga and select_page as inputs


if __name__ == '__main__':
    MangaDownloaderApp().run()
