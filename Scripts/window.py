from funcitions import *
from main import main
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
class Myclass(App):
    def build(self):
        return Launch()

class Launch(BoxLayout):
    def start(self):
        main()

