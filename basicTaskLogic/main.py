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

# Create a list with any already existing Tasks (can be empty if we want
# users to start with none like a new user)
taskList = [Task("Call Mom", 1, 10), Task("Text Friend", 2, 5), Task("Go to Club", 0, 20)]
completedTaskList = []

# Widget/Screen (will change to screen w/ ScreenManager)
class TaskScreen(Widget):
    # Current task we're on starting at 0
    index = 0

    # Get the task we're currently on
    currentTask = taskList[index]
    currentProgress = f'{currentTask.progressNum} / {currentTask.totalNum}'

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

    # Function that flushes the fish and updates the screen to a different goal afterwards
    def flushFish(self):
        taskList.remove(self.currentTask)
        self.updateIndex()
        self.updateLabels()
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

        # will disable the "next task" button if we are on the last task and hide it (minimal design)
        # or will re-enable the "previous task" button if we are no longer on the first task
        self.updateTaskButtons()


    # Function that is called when previous task button (made in kv file) is pressed
    def prevTask(self):
        # decrease the taskList index
        self.index = self.index - 1

        #get the new current task
        self.currentTask = taskList[self.index]

        # using the id of the label in the kv file, change label's text to the task's title
        self.updateLabels()

        # will re-enable the "next task" button if we are no longer on the last task
        # or will disable the "previous task" button if we are on the first task
        self.updateTaskButtons()


    # Function that updates the labels on the screen
    def updateLabels(self):
        if len(taskList) == 0:
            self.ids.task_title_label.text = "No active goals! Make a new one!"
            self.ids.task_progress_label.opacity = 0
        else:
            cTask = self.currentTask
            # Update Task Title
            self.ids.task_title_label.text = cTask.title
            # Update Progress Label
            self.ids.task_progress_label.text = f'{cTask.progressNum} / {cTask.totalNum}'


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


        # If there are no tasks, show none of the buttons
        if len(taskList) == 0:
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


class TaskApp(App):
    def build(self):
        return TaskScreen()
    
if __name__ == '__main__':
    TaskApp().run()