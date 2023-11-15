import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.widget import Widget

# Create Task Object that will house all the information about a Task
# title: Task Title
# progressNum: # of times task has been done
# totalNum: total # of times task has to be done
class Task:
    def __init__(self, title, progressNum, totalNum):
        self.title = title
        self.progressNum = progressNum
        self.totalNum = totalNum

# Widget/Screen (will change to screen w/ ScreenManager)
class TaskScreen(Widget):
    # Create a list with any already existing Tasks (can be empty if we want
    # users to start with none like a new user)
    taskList = [Task("Call Mom", 1, 10), Task("Text Friend", 2, 5)]

    # Current task we're on starting at 0
    index = 0

    # Get the task we're on
    currentTask = taskList[0]

    # Function that is called when the button (made in kv file) is pressed
    def press(self):
        # increase the index of the Task we're on
        self.index += 1

        # get the new current task
        currentTask = self.taskList[self.index]

        # using the id of the label in the kv file, change label's text to the task's title
        self.ids.task_title_label.text = currentTask.title

class TaskApp(App):
    def build(self):
        return TaskScreen()
    
if __name__ == '__main__':
    TaskApp().run()