from tkinter import *

root = Tk()
root.configure(background='#333333')
root.title('Calculator')
root.geometry('320x180')

equation = StringVar()

def press(key):
    equa = equation.get()
    keyIsDgt = key.isdigit()
    if equa == None or equa == '':
        if keyIsDgt:
            equation.set(equation.get() + str(key))
    else:
        if equa == "ERROR":
            clear()
        equaLstCharIsDgt = equa[len(equa)-1].isdigit()
        if keyIsDgt:
            equation.set(equation.get() + str(key))
        elif equaLstCharIsDgt and decimalRule(equa,key):
            equation.set(equation.get() + str(key))

def equalPress(*args):
    try:
        equa = equation.get()
        if equa != None and equa != '':
            if equa[len(equa)-1].isdigit():
                equation.set(str(eval(equation.get())))
    except:
        equation.set('ERROR')

def clear(*args):
    equation.set('')

def decimalRule(string,char):
    operators = ['+','-','*','/']
    decimal='.'
    if char == decimal:
        if decimal not in string:
            return True
        else:
            splitIndex = listFinder(string,operators)
            if splitIndex <= 0:
                return False
            else:
                left, right = string[:splitIndex], string[splitIndex:]
                return decimal not in right
    return True

def listFinder(string,list):
    lastIndexFind = -1
    for item in list:
        if string.rfind(item) > lastIndexFind:
            lastIndexFind = string.rfind(item)
    return lastIndexFind



expression_entry = Label(root, textvariable=equation,bg='black',fg="white",anchor="w")
expression_entry.grid(row=0,columnspan=4,sticky='nswe')
## Botons definitions, order by row up to down and columnd left to right

Button(root,text=' 7 ',fg='#fff',background='#666',command=lambda: press('7')).grid(row=1,column=0,sticky='nswe')
Button(root,text=' 8 ',fg='#fff',background='#666',command=lambda: press('8')).grid(row=1,column=1,sticky='nswe')
Button(root,text=' 9 ',fg='#fff',background='#666',command=lambda: press('9')).grid(row=1,column=2,sticky='nswe')
Button(root,text=' + ',fg='#fff',background='#fe9727',command=lambda: press('+')).grid(row=1,column=3,sticky='nswe')

Button(root,text=' 4 ',fg='#fff',background='#666',command=lambda: press('4')).grid(row=2,column=0,sticky='nswe')
Button(root,text=' 5 ',fg='#fff',background='#666',command=lambda: press('5')).grid(row=2,column=1,sticky='nswe')
Button(root,text=' 6 ',fg='#fff',background='#666',command=lambda: press('6')).grid(row=2,column=2,sticky='nswe')
Button(root,text=' - ',fg='#fff',background='#fe9727',command=lambda: press('-')).grid(row=2,column=3,sticky='nswe')

Button(root,text=' 1 ',fg='#fff',background='#666',command=lambda: press('1')).grid(row=3,column=0,sticky='nswe')
Button(root,text=' 2 ',fg='#fff',background='#666',command=lambda: press('2')).grid(row=3,column=1,sticky='nswe')
Button(root,text=' 3 ',fg='#fff',background='#666',command=lambda: press('3')).grid(row=3,column=2,sticky='nswe')
Button(root,text=' * ',fg='#fff',background='#fe9727',command=lambda: press('*')).grid(row=3,column=3,sticky='nswe')


Button(root,text=' 0 ',fg='#fff',background='#666',command=lambda: press('0')).grid(row=4,columnspan=2,sticky='nswe')
Button(root,text=' . ',fg='#fff',background='#666',command=lambda: press('.')).grid(row=4,column=2,sticky='nswe')
Button(root,text=' / ',fg='#fff',background='#fe9727',command=lambda: press('/')).grid(row=4,column=3,sticky='nswe')

Button(root,text=' Clear ',fg='#fff',background='#999',command=clear).grid(row=5,column=2,sticky='nswe')
Button(root,text=' = ',fg='#fff',background='#fe9727',command=equalPress).grid(row=5,column=3,sticky='nswe')


for col_num in range(root.grid_size()[0]): root.grid_columnconfigure(col_num,minsize=80)
for row_num in range(root.grid_size()[1]): root.grid_rowconfigure(row_num,minsize=30)

root.bind("<Return>",equalPress)
root.bind("<BackSpace>",clear)
root.bind('7', lambda event=None: press('7'))
root.bind('8', lambda event=None: press('8'))
root.bind('9', lambda event=None: press('9'))
root.bind('+', lambda event=None: press('+'))
root.bind('4', lambda event=None: press('4'))
root.bind('5', lambda event=None: press('5'))
root.bind('6', lambda event=None: press('6'))
root.bind('-', lambda event=None: press('-'))
root.bind('1', lambda event=None: press('1'))
root.bind('2', lambda event=None: press('2'))
root.bind('3', lambda event=None: press('3'))
root.bind('*', lambda event=None: press('*'))
root.bind('0', lambda event=None: press('0'))
root.bind('.', lambda event=None: press('.'))
root.bind('/', lambda event=None: press('/'))
root.mainloop()