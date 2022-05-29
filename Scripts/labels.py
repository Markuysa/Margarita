#from tkinter import *
# from main import main
# window = Tk()
# window.title("Голосовой помощник Маргарита")
# window.geometry("400x250")
# lb= Label(window,text="Запуск помощника",font=("Times",30))
# lb.grid(row=0,column=0)
# btn=Button(window,text="ЗАПУСК!",command=main)
# btn.grid(row=1,column=0)
# window.mainloop()
# for x in range(100):
#     label.configure(text=str(x))
#     window.update()
from main import main
from tkinter import *


def work():
    print('working')


root = Tk()

start = Button(root, text='start',command=lambda: main())
start.pack()

stop = Button(root, text='stop', command=lambda: exit())
stop.pack()
root.mainloop()