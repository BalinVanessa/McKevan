import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

class HomeScreen(Screen):
    pass

class ActiveGoalScreen(Screen):
    pass

class NewGoalScreen(Screen):
    pass
class MyFish(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return kv
if __name__ == '__main__':
    MyApp().run()
