from tkinter import *

root = Tk()

e = Entry(root, width=50, bg="blue", fg="white", borderwidth=5)
e.grid(row=1, column=3)
e.insert(0, "texttttt here")


def onClick():
    hello = "Hello " + e.get()
    myLabel = Label(root, text=hello).grid(row=1, column=1)


myLabel = Label(root, text="HEY BITCH").grid(row=0, column=0)
myLabel2 = Label(root, text="AAAAAAAAAHH").grid(row=1, column=0)
# myLabel.grid(row=0, column=0)
# myLabel2.grid(row=1, column=0)

myButton = Button(root, text="CLICKY", padx=50, pady=20,
                  command=onClick, fg="blue", bg="white").grid(row=2, column=0)

root.mainloop()
