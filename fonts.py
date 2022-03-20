base = 700
from tkinter import *
from tkinter import font

root = Tk()
canvas = Canvas(root, bg='black')
frame = Frame(root)
frame.pack(side=LEFT, fill='y')
scroll = Scrollbar(frame, command=canvas.yview)
scroll.pack(fill='both', expand=True)
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side=LEFT)

text = "COMMAND UTILITY ACCESS/RETRIEVAL SYSTEM"
label1 = Label(canvas, text=text, font="NotoSansDisplay", anchor='w')
label2 = Label(canvas, text=text, font="FreeHelvetianCondensed", anchor='w')
label3 = Label(canvas, text=text, font="Keraleeyam", anchor='w')
label4 = Label(canvas, text=text, font="NotoSans", anchor='w')
label5 = Label(canvas, text=text, font="Meera", anchor='w')
label1.pack(fill='x')
label2.pack(fill='x')
label3.pack(fill='x')
label4.pack(fill='x')
label5.pack(fill='x')
print(len(font.families()))
for i in range(base, base + 25):
    thisfont = font.families()[i]
    xtext = ": ".join([text, thisfont.upper()])
    label = Label(canvas, text=xtext, font=(thisfont,), anchor='w')
    label.pack(side=TOP, fill='x')

root.mainloop()
