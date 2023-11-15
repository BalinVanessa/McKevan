import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.widget import Widget

class Task:
    def __init__(self, title, progressNum, totalNum):
        self.title = title
        self.progressNum = progressNum
        self.totalNum = totalNum

class TaskScreen(Widget):
    taskList = [Task("Call Mom", 1, 10), Task("Text Friend", 2, 5)]
    index = 0
    currentTask = taskList[0]

    def press(self):
        self.index += 1
        currentTask = self.taskList[self.index]
        self.ids.task_title_label.text = currentTask.title

class TaskApp(App):
    def build(self):
        return TaskScreen()
    
if __name__ == '__main__':
    TaskApp().run()