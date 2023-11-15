import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

#Screens -
#home screen
class HomeScreen(Screen):
    pass

#my fish screen
class MyFish(Screen):
    pass

#active goal screen
class ActiveGoalScreen(Screen):
    pass

#new goal page
class NewGoalScreen(Screen):
    pass

#new goal form
#name of goal
class NewGoal_Name(Screen):
    pass
#times to achive goal
class NewGoal_Times(Screen):
    pass
#reminders of goal
class NewGoal_Reminders(Screen):
    pass

#Screen Manager -
class WindowManager(ScreenManager):
    pass

#Line which builds the kv file
kv = Builder.load_file("my.kv")

#main function
class MyApp(App):
    def build(self):
        #makes the window white
        Window.clearcolor = (1, 1, 1, 1)
        return kv
if __name__ == '__main__':
    MyApp().run()
