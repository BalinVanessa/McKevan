import kivy
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button
import random
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# setting the window at a fixed size of 400, 700 and making it so that it cannot be resized
_fixed_size = (400, 700)




def reSize(*args):
    Window.size = _fixed_size
    return True


Window.bind(on_resize=reSize)


# Create Task Object that will house all the information about a Task
# title: Task Title
# progressNum: # of times task has been done
# totalNum: total # of times task has to be done
class Task:
    def __init__(self, title, progressNum, totalNum, reminders, imagePath):
        self.title = title
        self.progressNum = progressNum
        self.totalNum = totalNum
        self.reminders = reminders
        self.imagePath = imagePath


# A list of fish images corresponding specific tasks defined
fish_images = {
    "Call Mom": "images/completed1.png",
    "Text Friend": "images/completed2.png",
    "Facetime Mom": "images/completed3.png",
    "Say happy birthday to Sam": "images/completed4.png",
    "Go get dinner with Laura": "images/completed5.png",
    "Ask how Jacob is feeling": "images/completed6.png",
    "Call MeMaw": "images/completed7.png",
    "Attend Basketball Practice": "images/completed8.png",
    "Call Dad": "images/completed9.png",
    "Call Friend": "images/completed10.png",
    "Attend Tennis Meeting": "images/completed11.png",
    "Attend Club Meeting": "images/completed7.png"
}

# Create a list with any already existing Tasks (can be empty if we want
# users to start with none like a new user)
taskList = [Task("Attend Club Meeting", 5, 10, "User will be reminded on Saturday at 4:24 PM",
                 fish_images["Attend Club Meeting"]),
            Task("Call Mom", 9, 10, "User will be reminded on Monday, Tuesday, at 7:0 AM", fish_images["Call Mom"]),
            Task("Text Friend", 2, 5, "User will be reminded on Friday at 12:10 PM", fish_images["Text Friend"])]

# Create list that houses completed tasks
completedTaskList = [
                    #Task("Attend Tennis Meeting", 6, 12, "User will be reminded on Saturday at 4:24 PM",
                    #      fish_images["Attend Tennis Meeting"]),
                    # Task("Call Dad", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM",
                    #      fish_images["Call Dad"]),
                    # Task("Call Friend", 2, 7, "User will be reminded on Friday at 12:10 PM",
                    #      fish_images["Call Friend"]),
                    # Task("Facetime Mom", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM",
                    #      fish_images["Facetime Mom"]),
                     #Task("Say happy birthday to Sam", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM", 10,
                     #     fish_images["Say happy birthday to Sam"]),
                     #Task("Go get dinner with Laura", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM", 10,
                     #     fish_images["Go get dinner with Laura"]),
                     #Task("Ask how Jacob is feeling", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM", 10,
                     #     fish_images["Ask how Jacob is feeling"]),
                     #Task("Attend Basketball Practice", 1, 5, "User will be reminded on Monday, Tuesday, at 7:0 AM", 10,
                     #     fish_images["Attend Basketball Practice"]),
                     ]

# Task which will be edited to add to task list
New_Task = Task(None, None, None, None, None)

# flag variable for displaying most recent goal when goal added
coming_from_add_goal = False


# Defining pop-up function
def show_popup(num):
    errors = ['Cannot proceed without a task!!',
              'Cannot have a goal with \n0 times of achievement!',
              'You must enter a positive integer!!',
              'You must select at least \none day to be reminded!!',
              'Are you sure you want to \nflush this fish??']

    # Create the label with white text color
    label = Label(text=errors[num], color=[1, 1, 1, 1])

    # Create the popup with the label as its content
    popup = Popup(title='Error',
                  content=label,
                  size_hint=(None, None), size=(500, 250))
    popup.open()


def show_popup_new():
    msg = 'You have completed this goal!\nSee your new fish on the home screen!'
    # Create the label with white text color
    label = Label(text=msg, color=[1, 1, 1, 1])

    # Create the popup with the label as its content
    popup = Popup(title='Congratualations!',
                  content=label,
                  size_hint=(None, None), size=(500, 250))
    popup.open()

# Screens -
# home screen
class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        # Load the screen fully, then call populate_images method otherwise the app crashes
        Clock.schedule_once(self.populate_images)

    def populate_images(self, dt):
        container = self.ids.image_container
        container.clear_widgets()

        # Find the center xy coordinates
        center_x = Window.width / 2
        center_y = Window.height / 2
        scatter_radius = 275

        # Add fishes to screen
        for task in completedTaskList:
            # Initialize the image at the center
            #print(fish_images[task.title])
            #print(task.imagePath)
            img = Image(source=task.imagePath, size_hint=(None, None), size=('100dp', '100dp'))
            img.center_x = center_x
            img.center_y = center_y
            container.add_widget(img)

            # Calculate random offset coordinates
            scatter_x = random.uniform(-scatter_radius, scatter_radius)
            scatter_y = random.uniform(-scatter_radius, scatter_radius)

            # Make the fishes move to new coordinates
            Animation(center_x=img.center_x + scatter_x, center_y=img.center_y + scatter_y, t='out_quad').start(img)


# my fish screen
class MyFish(Screen):
    def on_pre_enter(self, *args):
        # Clear any existing widgets
        self.ids.fish_container.clear_widgets()

        # Add image widgets for each task
        for task in completedTaskList:
            # Create a horizontal BoxLayout for each task
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')

            # Add the image
            image = Image(source=task.imagePath, size_hint=(None, None), size=('100dp', '100dp'))
            task_box.add_widget(image)

            # Add the task description
            task_description = Label(text=task.title, size_hint=(1, None), height='100dp')
            task_box.add_widget(task_description)

            # Add the task box to the fish_container
            self.ids.fish_container.add_widget(task_box)

            # Create an instance of HorizontalLine that spans the full width
            line = HorizontalLine(size_hint_x=1, height='2dp')
            self.ids.fish_container.add_widget(line)


# Horizontal Line
class HorizontalLine(Label):
    pass


# active goal screen
class ActiveGoalScreen(Screen):
    # Current task we're on starting at 0
    index = 0

    # Get the task we're currently on
    currentTask = taskList[index]
    currentProgress = f'{currentTask.progressNum} / {currentTask.totalNum}'
    def on_pre_enter(self):
        global coming_from_add_goal
        if coming_from_add_goal:
            self.index = len(taskList) - 1
            coming_from_add_goal = False
        self.currentTask = taskList[self.index]
        self.updateLabels()
        self.updateTaskButtons()

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
            show_popup_new()
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

    def show_confirmation_popup(self):
        # Layout for buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height='50dp')

        # Yes button
        yes_button = Button(text='Yes', size_hint=(0.5, 1))
        yes_button.bind(on_release=self.flush_fish_confirmed)

        # No button
        no_button = Button(text='No', size_hint=(0.5, 1))
        no_button.bind(on_release=self.dismiss_popup)

        # Add buttons to the layout
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)

        # Button layout in pop up box
        content_layout = BoxLayout(orientation='vertical', padding=10)
        content_layout.add_widget(Label(text='', size_hint_y=None, height='50dp'))
        content_layout.add_widget(button_layout)

        # Create popup box
        self.confirmation_popup = Popup(title='Are you sure you want to flush this fish??',
                                        content=content_layout,
                                        size_hint=(None, None),
                                        size=('300dp', '200dp'),
                                        auto_dismiss=False)
        self.confirmation_popup.open()

    def flush_fish_confirmed(self, instance):
        self.flushFish()
        self.confirmation_popup.dismiss()

    def dismiss_popup(self, instance):
        self.confirmation_popup.dismiss()

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

        # get the new current task
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
                    # set other indexes to ·
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


# new goal page
class NewGoalScreen(Screen):
    pass


# new goal form
# name of goal
class NewGoal_Name(Screen):
    goal_name = ""

    def goal_name_preset(self, preset_name):
        self.goal_name = preset_name
        New_Task.title = self.goal_name
        self.goal_name = ""
        self.ids.goal_name_entry.text = ""

    def new_goal_next_name(self):
        if self.ids.goal_name_entry.text:
            self.goal_name = self.ids.goal_name_entry.text
        if not self.goal_name:
            show_popup(0)
            return False
        else:
            # add to new goal
            New_Task.title = self.goal_name
            # reset values
            self.goal_name = ""
            self.ids.goal_name_entry.text = ""
            return True


# times to achive goal
class NewGoal_Times(Screen):
    times_achieved = None

    def new_goal_next(self):
        self.times_achieved = self.ids.goal_achieve_number.text

        if self.times_achieved.isdigit():
            self.times_achieved = int(self.times_achieved)
            if self.times_achieved == 0:
                show_popup(1)  # Show popup if the condition is met
                return False
            else:
                # add to goal
                New_Task.totalNum = self.times_achieved
                # reset numbers
                self.ids.goal_achieve_number.text = "10"
                self.times_achieved = None
                return True
        else:
            show_popup(2)
            return False


# reminders of goal
class NewGoal_Reminders(Screen):
    am_pm_index = 1
    am_pm_options = ["AM", "PM"]

    minuets_index = 9
    minuets_options = range(0, 60, 5)

    hours_index = 2
    hours_options = range(1, 13)

    def am_pm_increase(self):
        self.am_pm_index += 1
        if self.am_pm_index == 2:
            self.am_pm_index = 0

        self.ids.am_pm_label.text = self.am_pm_options[self.am_pm_index]

    def am_pm_decrease(self):
        self.am_pm_index -= 1
        if self.am_pm_index == -1:
            self.am_pm_index = 1

        self.ids.am_pm_label.text = self.am_pm_options[self.am_pm_index]

    def minuets_increase(self):
        self.minuets_index += 1
        if self.minuets_index == len(self.minuets_options):
            self.minuets_index = 0

        self.ids.minuets_label.text = str(self.minuets_options[self.minuets_index])

    def minuets_decrease(self):
        self.minuets_index -= 1
        if self.minuets_index == -1:
            self.minuets_index = len(self.minuets_options)-1

        self.ids.minuets_label.text = str(self.minuets_options[self.minuets_index])

    def hours_increase(self):
        self.hours_index += 1
        if self.hours_index == 12:
            self.hours_index = 0

        self.ids.hours_label.text = str(self.hours_options[self.hours_index])

    def hours_decrease(self):
        self.hours_index -= 1
        if self.hours_index == -1:
            self.hours_index = 11

        self.ids.hours_label.text = str(self.hours_options[self.hours_index])

    checked_weekdays = []

    def reminder_check_click(self, instance, value, weekday):
        if value:
            self.checked_weekdays.append(weekday)
            # print(MyApp.checked_weekdays)
        else:
            self.checked_weekdays.remove(weekday)

    def new_goal_next_reminders(self):
        if not self.checked_weekdays:
            # popup saying you need to select a day
            show_popup(3)
            return False
        else:
            # add reminders to goal
            New_Task.reminders = "User will be reminded "
            for i in self.checked_weekdays:
                New_Task.reminders += i + ", "
            New_Task.reminders += "at " + str(self.hours_options[self.hours_index])
            New_Task.reminders += ":" + str(self.minuets_options[self.minuets_index])
            New_Task.reminders += " " + str(self.am_pm_options[self.am_pm_index])

            print("New Task reminder:", New_Task.reminders)

            # user has done task 0 times
            New_Task.progressNum = 0

            # add fish number for image source path

            key_random, val_random = random.choice(list(fish_images.items()))
            val_random = str(val_random)
            New_Task.imagePath = val_random

            # add new goal to active goals
            to_add_task = Task(New_Task.title, New_Task.progressNum, New_Task.totalNum, New_Task.reminders, New_Task.imagePath)
            taskList.append(to_add_task)

            #flag varible for pre screen active goals
            global coming_from_add_goal
            coming_from_add_goal = True


            # resetting the reminders screen
            # reset checkboxes and labels
            for x in list([self.ids.check_mon, self.ids.check_tue, self.ids.check_wed, self.ids.check_thurs,
                           self.ids.check_fri, self.ids.check_sat, self.ids.check_sun]):
                if x.active:
                    x.active = False

            self.am_pm_index = 1
            self.minuets_index = 9
            self.hours_index = 2
            self.ids.am_pm_label.text = self.am_pm_options[self.am_pm_index]
            self.ids.minuets_label.text = str(self.minuets_options[self.minuets_index])
            self.ids.hours_label.text = str(self.hours_options[self.hours_index])

            return True


# Screen Manager -
class WindowManager(ScreenManager):
    pass


# Line which builds the kv file
kv = Builder.load_file("FinFriends.kv")


# main function
class FinFriends(App):
    

    def build(self):
        # makes the window white
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 700)

        return kv


if __name__ == '__main__':
    FinFriends().run()
