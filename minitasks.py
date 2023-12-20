import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

COLOUR_ACCENT = "#00ADB5"
COLOUR_DARK = "#EEEEEE"
COLOUR_LIGHT = "#222831"
COLOUR_WHITE = "#222831"
FONT = ("Times", 10)

def clear_children():
    for child in scroll.winfo_children():
        child.destroy()

connection = sqlite3.connect('./database.db')
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS minitasks(minitask text, minitask_state integer)")
connection.commit()
connection.close()


def minitask_done(m_id, m_state):
    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE minitasks SET minitask_state=? where rowid={m_id}", (m_state,))
    connection.commit()
    connection.close()


def db_minitask_edit(m_id, m_text):
    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE minitasks SET minitask=? where rowid={m_id}", (m_text,))
    connection.commit()
    connection.close()


def minitask_delete(m_id):
    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM minitasks WHERE rowid={m_id}")
    connection.commit()
    connection.close()


def minitask_add(e):
    if len(e.get()) > 0:
        m_text = e.get()
        m_state = 0
        connection = sqlite3.connect('./database.db')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO minitasks VALUES(?, ?)", (m_text.capitalize(), m_state))
            connection.commit()
        except:
            pass
        minitasks_show()
        e.delete(0, 'end')


def minitask_edit(minitask):
    def minitask_edit_save(e):
        if len(e.get("1.0", "end-1c")) > 0:
            db_minitask_edit(minitask[2], e.get("1.0", "end-1c"))
            minitasks_show()
            edit_window.destroy()

    edit_window = tk.Toplevel()
    edit_window.config(bg=COLOUR_WHITE)
    edit_window.geometry('900x900')
    edit_window.title(f'Edit {minitask[0]}')
    edit_window.columnconfigure(0, weight=1)
    edit_window.rowconfigure(0, weight=1)
    minitask_edit_entry = tk.Text(edit_window, font=("Times", 12), relief='flat', height=10, fg=COLOUR_DARK, bg=COLOUR_WHITE)
    minitask_edit_entry.grid(row=0, column=0, sticky='NEWS', padx=10, pady=10)
    minitask_edit_entry.focus()
    minitask_edit_entry.insert("1.0", minitask[0])
    tk.Button(edit_window, text='U P D A T E', foreground=COLOUR_WHITE, background=COLOUR_ACCENT, width=2, relief='flat', font=("Calibri", 10), command=lambda: minitask_edit_save(minitask_edit_entry)).grid(row=1, column=0, sticky='EW', padx=0, pady=0)


def minitasks_show():
    def create_minitask_labels(i, each_minitask):
        separator_frame = tk.Frame(scroll, bg=COLOUR_WHITE)
        separator_frame.grid(row=i, column=0, sticky="NEWS")
        separator_frame.columnconfigure(1, weight=1)
        tk.Button(separator_frame, text=f"✅", foreground=COLOUR_ACCENT, relief='flat', background=COLOUR_WHITE, font=("Times", 14), activebackground=COLOUR_WHITE, activeforeground=COLOUR_ACCENT, borderwidth=0, command=lambda: [minitask_done(each_minitask[2], 1), minitasks_show()]).grid(row=0, column=0, sticky='NSW', padx=(0, 10), pady=1)
        minitask_label = tk.Label(separator_frame, text=each_minitask[0], font=("Times", 12), wraplength=930, foreground=COLOUR_DARK, background=COLOUR_WHITE, justify='left', anchor='w')
        minitask_label.grid(row=0, column=1, sticky='WE', padx=2, pady=2)
        minitask_label.bind("<Button-1>", lambda x: minitask_edit(each_minitask))
    display_button['text'] = '💾'
    display_button['command'] = lambda: minitasks_show_completed()
    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT *, rowid FROM minitasks WHERE minitask_state=0 ORDER BY minitask ASC")
    minitasks_list = cursor.fetchall()
    connection.close()
    clear_children()
    for i, each_active in enumerate(minitasks_list):
        create_minitask_labels(i, each_active)


def confirm_delete(each_minitask):
    if messagebox.askokcancel(title='Delete task',
                              message=f'Are you sure you want to delete {each_minitask[0]}?'):
        minitask_delete(each_minitask[2])
        minitasks_show_completed()


def minitasks_show_completed():
    def create_minitask_labels(i, each_minitask):
        separator_f = tk.Frame(scroll, bg=COLOUR_WHITE)
        separator_f.grid(row=i, column=0, sticky="NEWS")
        separator_f.columnconfigure(1, weight=1)
        tk.Button(separator_f, text='❌', foreground=COLOUR_ACCENT, relief='flat', background=COLOUR_WHITE, font=("Times", 10), activebackground=COLOUR_WHITE, activeforeground=COLOUR_ACCENT, borderwidth=0, command=lambda: confirm_delete(each_minitask)).grid(row=int(i), column=0, sticky='NSW', pady=2)
        minitask_label = tk.Label(separator_f, text=each_minitask[0], font=("Times", 10), wraplength=930, foreground=COLOUR_DARK, background=COLOUR_WHITE, justify='left', anchor='w')
        minitask_label.grid(row=int(i), column=1, sticky='EW', padx=2)
    display_button['text'] = '💾'
    display_button['command'] = lambda: minitasks_show()
    connection = sqlite3.connect('./database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT *, rowid FROM minitasks WHERE minitask_state=1 ORDER BY minitask ASC")
    minitasks_list = cursor.fetchall()
    connection.close()
    clear_children()
    for i, each_minitask in enumerate(minitasks_list):
        if each_minitask[1] == 1:
            create_minitask_labels(i, each_minitask)


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid(row=0, column=0, sticky="NEWS")
        self.columnconfigure(1, weight=1)
        self.configure(relief='flat')
        self.canvas = tk.Canvas(self, bg=COLOUR_WHITE, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=1)
        self.scb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scb.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scb.set)
        self.canvas.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame_to_scroll = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_to_scroll, anchor="nw")
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))


root = tk.Tk()
root.geometry("1000x1500")
root.resizable(False, True)
root.title('MiniTask')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

scroll = ScrollableFrame(root).frame_to_scroll

ttk.Separator(root).grid(row=1, column=0, sticky="EW")

buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, sticky="EW")
buttons_frame.columnconfigure(0, weight=1)

minitask_entry = tk.Entry(buttons_frame, font=("Times", 14), relief='flat', bg=COLOUR_WHITE, fg=COLOUR_ACCENT)
minitask_entry.grid(row=0, column=0, sticky='NEWS')
minitask_entry.focus()
minitask_entry.bind("<Return>", lambda x: minitask_add(minitask_entry))

tk.Button(buttons_frame, text='➕', background=COLOUR_WHITE, foreground=COLOUR_ACCENT, relief='flat', font=("Times", 14), command=lambda: minitask_add(minitask_entry)).grid(row=0, column=2, sticky="e")
display_button = tk.Button(buttons_frame, text='💾', relief="flat", background=COLOUR_WHITE, foreground=COLOUR_ACCENT, font=("Times", 14), command=lambda: minitasks_show_completed())
display_button.grid(row=0, column=3, sticky='E', padx=(0, 1))

minitasks_show()
root.mainloop()
