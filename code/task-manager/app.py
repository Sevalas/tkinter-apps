from tkinter import (Tk, ttk, Frame, Canvas, Checkbutton, Button, Label, Entry, messagebox, LEFT, BOTH, RIGHT, Y, X, END, YES, NW, W, NSEW, VERTICAL, ALL)
import db as db
from task import Task

db.startDb()

root = Tk()
root.title('Task Manager')
root.geometry('500x500')
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

style = ttk.Style(root)

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=NW, tags='scrollable_frame')
        canvas.configure(yscrollcommand=scrollbar.set)
       
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(
                scrollregion=canvas.bbox(ALL)
            )
        )
        canvas.bind(
            '<Configure>',
            lambda e: canvas.itemconfig(
                'scrollable_frame', width=canvas.winfo_width()
            )
        )
        canvas.bind_all(
            '<MouseWheel>',
            lambda event: canvas.yview_scroll(
                int(-1*(event.delta/120)), "units"
            )
        )

def updateStatus(task):
    def _updateStatus():
        status = 1 if task.status == 0 else 0;
        db.updateStatus(task.id, status)
        renderTasks()
    return _updateStatus


def removeTask(task):
    def _removeTask():
        db.deleteTask(task.id)
        renderTasks()
    return _removeTask


def renderTasks():

    for widget in task_list.scrollable_frame.winfo_children():
        widget.destroy()

    tasks: list(Task) = db.selectTasks()

    for index in range(0, len(tasks)):
        task = tasks[index]
        frame = Frame(task_list.scrollable_frame, padx=10, pady=3)
        frame.grid(column=0, row=index, columnspan=3, sticky=NSEW)

        completed = task.status
        color = '#555555' if task.status else '#000000'

        taskTitle = Checkbutton(frame, text=task.description, fg=color, anchor=W,command=updateStatus(task), variable=tasks[index])
        taskTitle.pack(side=LEFT)
        taskTitle.select() if completed else taskTitle.deselect()

        deleteButton = Button(frame, text='Remove',command=removeTask(task))
        deleteButton.pack(side=RIGHT)
  

def addTask():
    if e.get() and len(e.get()) >= 1:
            db.insertTask(e.get())
            e.delete(0, END)
            renderTasks()

header = Frame(root)
header.grid(column=0, row=0, columnspan=3, sticky=NSEW)

l = Label(header, text='Task Title')
l.pack(side=LEFT)

def validate(P):
    if len(P) == 0 or len(P) <= 50:
        return True
    else:
        return False

vcmd = (root.register(validate), '%P')

e = Entry(header, validate="key", validatecommand=vcmd)
e.pack(side=LEFT, fill=X, expand=YES)

btn = Button(header, text='Add', command=addTask, width = 20)
btn.pack(side=RIGHT)

task_list = ScrollableFrame(root)
task_list.grid(column=0, row=1, columnspan=3, sticky=NSEW)
task_list.scrollable_frame.grid_columnconfigure(0, weight=1)

e.focus()

root.bind('<Return>', lambda event: addTask())

renderTasks()

root.mainloop()
