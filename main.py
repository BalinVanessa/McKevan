import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout

class HomeScreen(Screen):
    pass

class ActiveGoalScreen(Screen):
    pass

class NewGoalScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv
if __name__ == '__main__':
    MyApp().run()
