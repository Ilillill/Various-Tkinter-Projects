import tkinter as tk
from tkinter import ttk
from random import choice

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

click = 0
list_icons = ['🚗', '🏡', '🌈', '⛄', '🐸', '🐬', '🍓', '🍰', '🍩', '🌲', '💻', '📷', '📚', '🎮', '👻', '🦘', '🦎']
list_buttons = []
clicked_buttons = []
blocked = []
list_final = []

def action(button_clicked):
    def hide():
        global click
        clicked_buttons[0].configure(fg='white', state='normal')
        clicked_buttons[1].configure(fg='white', state='normal')
        click = 0
        clicked_buttons.clear()
        for each_blocked_button in blocked:
            each_blocked_button['state'] = 'normal'
        blocked.clear()

    global click
    click += 1
    if click == 1:
        button_clicked.configure(disabledforeground='black', state='disabled')
        clicked_buttons.append(button_clicked)
    else:
        button_clicked.configure(fg='black')
        clicked_buttons.append(button_clicked)
        if clicked_buttons[0]['text'] == clicked_buttons[1]['text']:
            clicked_buttons[0].configure(disabledforeground='green', state='disabled')
            clicked_buttons[1].configure(disabledforeground='green', state='disabled')
            click = 0
            clicked_buttons.clear()
        else:
            clicked_buttons[0].configure(disabledforeground='black', state='disabled')
            clicked_buttons[1].configure(disabledforeground='black', state='disabled')
            for each_selected_button in list_final:
                if each_selected_button[1]['state'] != 'disabled':
                    blocked.append(each_selected_button[1])
                if each_selected_button[2]['state'] != 'disabled':
                    blocked.append(each_selected_button[2])
            for each_appended in blocked:
                each_appended.configure(disabledforeground='white', state='disabled')
            root.after(1000, hide)

def create_buttons(selected_button):
    selected_button.configure(command=lambda: action(selected_button))

root = tk.Tk()
root.title('Game')
root.columnconfigure((0, 1, 2, 3), minsize=150, weight=1)
root.rowconfigure((0, 1, 2, 3), minsize=150, weight=1)




for i in range(16):
    list_buttons.append(tk.Button(root, bg='white', fg='white', text='', font=("Calibri Light", 40)))

for each_button in list_buttons:
    create_buttons(each_button)


list_buttons[0].grid(row=0, column=0, sticky="NEWS")
list_buttons[1].grid(row=0, column=1, sticky="NEWS")
list_buttons[2].grid(row=0, column=2, sticky="NEWS")
list_buttons[3].grid(row=0, column=3, sticky="NEWS")
list_buttons[4].grid(row=1, column=0, sticky="NEWS")
list_buttons[5].grid(row=1, column=1, sticky="NEWS")
list_buttons[6].grid(row=1, column=2, sticky="NEWS")
list_buttons[7].grid(row=1, column=3, sticky="NEWS")
list_buttons[8].grid(row=2, column=0, sticky="NEWS")
list_buttons[9].grid(row=2, column=1, sticky="NEWS")
list_buttons[10].grid(row=2, column=2, sticky="NEWS")
list_buttons[11].grid(row=2, column=3, sticky="NEWS")
list_buttons[12].grid(row=3, column=0, sticky="NEWS")
list_buttons[13].grid(row=3, column=1, sticky="NEWS")
list_buttons[14].grid(row=3, column=2, sticky="NEWS")
list_buttons[15].grid(row=3, column=3, sticky="NEWS")

menu_frame = tk.Frame(root, bg='white')
menu_frame.grid(row=0, column=4, rowspan=4, sticky="NEWS")
menu_frame.columnconfigure(0, weight=1)





for i in range(8):
    selected_icon = choice(list_icons)
    list_icons.remove(selected_icon)
    selected_button_01 = choice(list_buttons)
    list_buttons.remove(selected_button_01)
    selected_button_02 = choice(list_buttons)
    list_buttons.remove(selected_button_02)
    list_final.append([selected_icon, selected_button_01, selected_button_02])

for each_item in list_final:
    each_item[1].configure(text=each_item[0])
    each_item[2].configure(text=each_item[0])

root.mainloop()