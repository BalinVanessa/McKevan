import kivy
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config

#setting the window at a fixed size of 400, 700 and making it so that it cannot be resized
_fixed_size = (400, 700)
def reSize(*args):
   Window.size = _fixed_size
   return True
Window.bind(on_resize = reSize)

# Create Task Object that will house all the information about a Task
# title: Task Title
# progressNum: # of times task has been done
# totalNum: total # of times task has to be done
class Task:
    def __init__(self, title, progressNum, totalNum):
        self.title = title
        self.progressNum = progressNum
        self.totalNum = totalNum

# Create a list with any already existing Tasks (can be empty if we want
# users to start with none like a new user)
taskList = [Task("Attend Club Meeting", 5, 10), Task("Call Mom", 1, 10), Task("Text Friend", 2, 5)]
# Create list that houses completed tasks
completedTaskList = []

#Screens -
#home screen
class HomeScreen(Screen):
    pass

#my fish screen
class MyFish(Screen):
    pass

#active goal screen
class ActiveGoalScreen(Screen):
    # Current task we're on starting at 0
    index = 0

    # Get the task we're currently on
    currentTask = taskList[index]
    currentProgress = f'{currentTask.progressNum} / {currentTask.totalNum}'

    # Function that updates the fish image based on the current task's progress
    def getFishImage(self):
        # calculate the number of progress (percentage of progress rounded down to nearest int)
        imgNum = math.floor((self.currentTask.progressNum / self.currentTask.totalNum) * 10)
        # if number is 0 or there are no tasks available, set it to the empty fish image
        if (imgNum == 0) or (len(taskList) == 0):
            self.ids.goal_fish_img.source = "images/fish/1.png"
        else:
            # Get the image corresponding to the progress percentage
            self.ids.goal_fish_img.source = f'images/fish/{imgNum}.png'

    # Function that logs the progress for the current Task
    def logProgress(self):
        # Adds 1 to the progress number and updates the labels
        self.currentTask.progressNum += 1

        # If the goal is completed, add it to completed tasks and remove it from current tasks
        # and refreshes the screen (may move to a different goal if this one if completed)
        if self.currentTask.progressNum == self.currentTask.totalNum:
            completedTaskList.append(self.currentTask)
            taskList.remove(self.currentTask)
            self.updateIndex()
            self.updateTaskButtons()

        # Update Labels
        self.updateLabels()
        self.getFishImage()

    # Function that flushes the fish and updates the screen to a different goal afterwards
    def flushFish(self):
        taskList.remove(self.currentTask)
        self.updateIndex()
        self.updateLabels()
        self.getFishImage()
        self.updateTaskButtons()

    # Function to update index after a task is removed/completed
    def updateIndex(self):
        # If the current goal was deleted/completed, show the previous goal now
        if (self.index > 0) & (len(taskList) > 0):
            self.index -= 1
            self.currentTask = taskList[self.index]
        elif len(taskList) > 0:
            self.currentTask = taskList[self.index]

    # Function that is called when the next task button (made in kv file) is pressed
    def nextTask(self):
        # increase the index of the Task we're on
        self.index = self.index + 1

        # get the new current task
        self.currentTask = taskList[self.index]

        # using the id of the label in the kv file, change label's text to the task's title
        self.updateLabels()

        self.getFishImage()

        # will disable the "next task" button if we are on the last task and hide it (minimal design)
        # or will re-enable the "previous task" button if we are no longer on the first task
        self.updateTaskButtons()

    # Function that is called when previous task button (made in kv file) is pressed
    def prevTask(self):
        # decrease the taskList index
        self.index = self.index - 1

        #get the new current task
        self.currentTask = taskList[self.index]

        # update the fish image
        self.getFishImage()

        # using the id of the label in the kv file, change label's text to the task's title
        self.updateLabels()

        # will re-enable the "next task" button if we are no longer on the last task
        # or will disable the "previous task" button if we are on the first task
        self.updateTaskButtons()

    # Function that updates the labels on the screen
    def updateLabels(self):
        if len(taskList) == 0:
            self.ids.goal_title_label.text = "No active goals!"
            self.ids.goal_progress_label.text = "Go to Add Goal!"
            self.ids.active_goal_index.text = ""
        else:
            cTask = self.currentTask
            # Update Task Title
            self.ids.goal_title_label.text = cTask.title
            # Update Progress Label
            self.ids.goal_progress_label.text = f'{cTask.progressNum} / {cTask.totalNum}'

            # Update Active Goal Index
            # Initialize an empty String
            indexString = ""
            # for the amount of active tasks available...
            for x in range(len(taskList)):
                # if we are on the active task, set index to a "o"
                if x == self.index:
                    indexString += "o"
                else:
                    # set other indexes to x
                    indexString += "·"

                # Adds a space between the index symbols (unless it's the last task index)
                if x != (len(taskList) - 1):
                    indexString += " "
            # Set active goal index to the indexString
            self.ids.active_goal_index.text = indexString
                


    # Function that updates the state of the buttons:
    # If we are on the first task, the "previous task" button disappears
    # If we are on the last task, the "next task" button disappears
    def updateTaskButtons(self):
        if len(taskList) == 0:
            # Make Log Progress Button and Flush Fish Button disabled and invisible
            self.ids.log_progress_button.disabled = True
            self.ids.log_progress_button.opacity = 0
            self.ids.flush_fish_button.disabled = True
            self.ids.flush_fish_button.opacity = 0
        else:
            self.ids.log_progress_button.disabled = False
            self.ids.log_progress_button.opacity = 1
            self.ids.flush_fish_button.disabled = False
            self.ids.flush_fish_button.opacity = 1


        # If there are no tasks or only one task, show none of the prev/next buttons
        if len(taskList) == 0 or len(taskList) == 1:
            self.ids.prev_task_button.disabled = True
            self.ids.prev_task_button.opacity = 0

            self.ids.next_task_button.disabled = True
            self.ids.next_task_button.opacity = 0
        # If we're on the first task
        elif self.index == 0:
            # Disable the previous task button and make it invisible
            self.ids.prev_task_button.disabled = True
            self.ids.prev_task_button.opacity = 0

            # Enable the next task button and make it visible
            self.ids.next_task_button.disabled = False
            self.ids.next_task_button.opacity = 1

        # If we're on the last task
        elif self.index == (len(taskList) - 1):
            # Enable the previous task button and make it visible
            self.ids.prev_task_button.disabled = False
            self.ids.prev_task_button.opacity = 1

            # Disable the next task button and make it invisible
            self.ids.next_task_button.disabled = True
            self.ids.next_task_button.opacity = 0
        else:
            # Makes both buttons visible
            self.ids.prev_task_button.disabled = False
            self.ids.prev_task_button.opacity = 1

            self.ids.next_task_button.disabled = False
            self.ids.next_task_button.opacity = 1



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
    checked_weekdays = []
    def reminder_check_click(self, instance, value, weekday):
        if value:
            MyApp.checked_weekdays.append(weekday)
            #print(MyApp.checked_weekdays)
        else:
            MyApp.checked_weekdays.remove(weekday)

    def new_goal_next(self):
        if not MyApp.checked_weekdays:
            return False
        else:
            return True

    def build(self):
        #makes the window white
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 700)
        return kv
if __name__ == '__main__':
    MyApp().run()
