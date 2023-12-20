import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import webbrowser
import random

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

buttons_size = 14

def create_databases():
    connection = sqlite3.connect("./passwords_database.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS passwords("
        "password_title text, "
        "password_login text, "
        "password_password text, "
        "password_website text, "
        "password_notes text)")
    connection.commit()
    connection.close()

def password_add(p_title, p_login, p_password, p_website, p_notes):
    connection = sqlite3.connect("./passwords_database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO passwords VALUES(?, ?, ?, ?, ?)",
                        (p_title, p_login, p_password, p_website, p_notes))
        connection.commit()
    except:
        statusbar.set('Database error')
    connection.close()

def password_update(tit, log, pas, web, notes, idnumber):
    connection = sqlite3.connect("./passwords_database.db")
    cursor = connection.cursor()
    cursor.execute(f'UPDATE passwords SET password_title=? WHERE rowid={idnumber}', (tit,))
    cursor.execute(f'UPDATE passwords SET password_login=? WHERE rowid={idnumber}', (log,))
    cursor.execute(f'UPDATE passwords SET password_password=? WHERE rowid={idnumber}', (pas,))
    cursor.execute(f'UPDATE passwords SET password_website=? WHERE rowid={idnumber}', (web,))
    cursor.execute(f'UPDATE passwords SET password_notes=? WHERE rowid={idnumber}', (notes,))
    connection.commit()
    connection.close()

def passwords_select_all():
    connection = sqlite3.connect("./passwords_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM passwords ORDER BY password_title")
    all_passwords = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in cursor.fetchall()]
    connection.close()
    return all_passwords

def password_delete(p_id):
    connection = sqlite3.connect("./passwords_database.db")
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM passwords WHERE rowid={p_id}')
    connection.commit()
    connection.close()

def start_app():
    if len(passwords_select_all()) == 0:
        FrameAddUpdate(root, password_details='add')
    else:
        list_button['state'] = 'normal'
        main_frame = FrameMain(root)

def copy_to_clipboard(source):
    root.clipboard_clear()
    root.clipboard_append(source)
    statusbar.set(f'{source} copied to clipboard')

def generate_password():
    return ''.join([random.choice(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f',
        'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I',
        'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '!', '£',
        '$', '%', '^', '&', '*', '(', ')', '[', ']', ';', '\'', '#', ',', '.', '/', '{', '}', ':', '@', '<', '>', '?']
            ) for x in range(16)])

class FrameMain(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid(row=1, column=0, sticky="NEWS")
        self.bg = "white"
        self.buttons_size = 18
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.DISPLAY_FRAME = tk.Frame(self, bg='white')
        self.DISPLAY_FRAME.grid(row=1, column=1, sticky='NEWS')
        self.DISPLAY_FRAME.columnconfigure(0, weight=1)
        self.DISPLAY_FRAME.rowconfigure(0, weight=1)

        ''' IMAGE '''
        password_img = tk.PhotoImage(file='pass_image.png')
        self.welcome_label = tk.Label(self.DISPLAY_FRAME, image=password_img)
        self.welcome_label.image = password_img
        self.welcome_label.grid(row=0, column=0, sticky="news")

        ''' LISTBOX '''
        self.listbox_password_list = passwords_select_all()
        self.listbox_just_titles = [entry[1] for entry in self.listbox_password_list]
        self.passwords = tk.StringVar(value=self.listbox_just_titles)
        self.listbox_frame = tk.Frame(self, bg='white')
        self.listbox_frame.grid(row=1, column=0, sticky='NEWS')
        self.listbox_frame.columnconfigure(0, weight=1)
        self.listbox_frame.rowconfigure(0, weight=1)
        self.passwords_listbox = tk.Listbox(self.listbox_frame, listvariable=self.passwords, height=10)
        self.passwords_listbox['selectmode'] = "single"
        self.passwords_listbox.grid(row=0, column=0, sticky='NEWS')
        self.passwords_listbox.bind("<<ListboxSelect>>", lambda event: DetailsFrame(self))
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.passwords_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.passwords_listbox["yscrollcommand"] = scrollbar.set

        def DetailsFrame(self):
            import _tkinter
            try:

                selected_item = self.passwords_listbox.curselection()
            except _tkinter.TclError:
                selected_item = []

            statusbar.set(self.passwords_listbox.get(selected_item))
            password_details = self.listbox_password_list[self.listbox_just_titles.index(self.passwords_listbox.get(selected_item))]

            main_frame = tk.Frame(self.DISPLAY_FRAME, bg='white', padx=20, pady=5)
            main_frame.grid(row=0, column=0, sticky="news")
            main_frame.columnconfigure(1, weight=1)

            label_title = tk.Label(main_frame, bg="white", padx=10, pady=20, text=f'{password_details[1]}', font=("Calibri", 24))
            label_title.grid(row=0, column=0, columnspan=2, sticky="ew")

            tk.Label(main_frame, text="Title", width=10, bg="white").grid(row=1, column=0, pady=5)
            details_title_label = tk.Label(main_frame, text=f"{password_details[1]}", width=10, bg="white", anchor='w')
            details_title_label.grid(row=1, column=1, pady=5, sticky='ew')
            details_title_label.bind("<Button-1>", lambda *args: copy_to_clipboard(details_title_label['text']))

            tk.Label(main_frame, text="Login", width=10, bg="white").grid(row=2, column=0, pady=5)
            details_login_label = tk.Label(main_frame, text=f"{password_details[2]}", width=10, bg="white", anchor='w')
            details_login_label.grid(row=2, column=1, pady=5, sticky='ew')
            details_login_label.bind("<Button-1>", lambda *args: copy_to_clipboard(details_login_label['text']))

            tk.Label(main_frame, text="Password", width=10, bg="white").grid(row=3, column=0, pady=5)
            details_password_label = tk.Label(main_frame, text=f"{password_details[3]}", width=10, bg="white", anchor='w')
            details_password_label.grid(row=3, column=1, pady=5, sticky='ew')
            details_password_label.bind("<Button-1>", lambda *args: copy_to_clipboard(details_password_label['text']))

            tk.Label(main_frame, text="Website", width=10, bg="white").grid(row=4, column=0, pady=5)
            details_website_label = tk.Label(main_frame, text=f"{password_details[4]}", width=10, bg="white", anchor='w')
            details_website_label.grid(row=4, column=1, pady=5, sticky='ew')
            details_website_label.bind("<Button-1>", lambda *args: webbrowser.open(password_details[4]))

            details_notes_label = tk.Label(main_frame, text=f"{password_details[5]}", width=10, bg="white", anchor='w')
            details_notes_label.grid(row=5, column=0, columnspan=2, sticky='ew', pady=30)
            details_notes_label.bind("<Button-1>", lambda *args: copy_to_clipboard(details_notes_label['text']))

            buttons_frame = tk.Frame(self.DISPLAY_FRAME, bg='white')
            buttons_frame.grid(row=1, column=0, sticky="EW", padx=20)
            buttons_frame.columnconfigure(0, weight=1)

            tk.Label(buttons_frame, text='Click on Login or Password to copy to clipboard. Click on website to open.', font=("Calibri", 8, 'italic'), bg='white').grid(row=0, column=0, sticky='ew')

            def confirm_delete(self):
                if messagebox.askyesno(title=f'Delete {password_details[1]}?', message=f'Are you sure you want to delete {password_details[1]}?', icon='question'):
                    password_delete(password_details[0])
                    self.destroy()
                    start_app()

            button_delete = ttk.Button(buttons_frame, text='❌', width=3, command=lambda: confirm_delete(self))
            button_delete.grid(row=0, column=1, sticky='e')

            button_edit = ttk.Button(buttons_frame, text='Edit', command=lambda: [self.destroy(), FrameAddUpdate(root, password_details=password_details)])
            button_edit.grid(row=0, column=2, sticky='e')

class FrameAddUpdate(tk.Frame):
    def __init__(self, container, password_details, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid(row=1, column=0, sticky='NEWS')
        self.password_details = password_details
        self.configure(bg='white')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        def check_entry_and_add(self, tit, log, pas, web, notes, addorupdate, idnumber=''):
            tit_ok, log_ok, pas_ok = False, False, False
            if len(tit) > 20:
                statusbar.set("Title can not be longer than 20 characters.")
            elif len(tit) == 0:
                statusbar.set("Title field can not be empty. Please add a title.")
            else:
                tit_ok = True
            if len(log) == 0:
                statusbar.set("Login field can not be empty. Please add login.")    
            else:
                log_ok = True
            if len(pas) == 0:
                statusbar.set("Password field can not be empty. Please add password.")    
            else:
                pas_ok = True
            if len(web) == 0:
                web = ''
            if len(notes) == 0:
                notes = ''

            if tit_ok and log_ok and pas_ok:
                if addorupdate == 'add':
                    statusbar.set("New entry added successfuly!")
                    password_add(tit, log, pas, web, notes)
                    self.destroy()
                    start_app()
                elif addorupdate == 'update':
                    statusbar.set("Entry updated")
                    password_update(tit, log, pas, web, notes, idnumber)
                    self.destroy()
                    start_app()

        label_title = tk.Label(self, bg="white", padx=10, pady=20, font=("Calibri", 24))
        label_title.grid(row=0, column=0, columnspan=3, sticky="ew")

        tk.Label(self, text="Title", width=10, bg="white").grid(row=1, column=0, pady=5)
        entry_title = ttk.Entry(self)
        entry_title.grid(row=1, column=1, columnspan=2, pady=5, sticky='ew')

        tk.Label(self, text="Login", width=10, bg="white").grid(row=2, column=0, pady=5)
        entry_login = ttk.Entry(self)
        entry_login.grid(row=2, column=1, columnspan=2, pady=5, sticky='ew')

        tk.Label(self, text="Password", width=10, bg="white").grid(row=3, column=0, pady=5)
        entry_password = ttk.Entry(self)
        entry_password.grid(row=3, column=1, pady=5, sticky='ew')

        generate_password_button = tk.Button(self, text="Generate", bg="white", borderwidth=0, command=lambda: [entry_password.delete(0, 'end'), entry_password.insert(0, generate_password())])
        generate_password_button.grid(row=3, column=2, sticky='e', pady=5)

        tk.Label(self, text="Website", width=10, bg="white").grid(row=4, column=0, pady=5)
        entry_website = ttk.Entry(self)
        entry_website.grid(row=4, column=1, columnspan=2, pady=5, sticky='ew')

        entry_notes = tk.Text(self, height=5, border=1, borderwidth=1, font=('Calibri', 10))
        entry_notes.grid(row=5, column=0, columnspan=3, sticky='news', pady=30)

        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.grid(row=6, column=0, sticky="EW", padx=20, columnspan=3)
        buttons_frame.columnconfigure(0, weight=1)

        button_add_update = ttk.Button(buttons_frame)
        button_add_update.grid(row=0, column=1, sticky='e')

        button_cancel = ttk.Button(buttons_frame, text="Cancel", command=lambda: [self.destroy(), start_app()])
        button_cancel.grid(row=0, column=2, sticky="e")

        if self.password_details == 'add':
            label_title['text'] = 'Add new entry'
            button_add_update['command'] = lambda: check_entry_and_add(self, entry_title.get(), entry_login.get(), entry_password.get(), entry_website.get(), entry_notes.get("1.0", "end-1c"), 'add')
            button_add_update['text'] = 'Add'

        else:
            label_title['text'] = f"Update {password_details[1]}"
            button_add_update['command'] = lambda: check_entry_and_add(self, entry_title.get(), entry_login.get(), entry_password.get(), entry_website.get(), entry_notes.get("1.0", "end-1c"), 'update', idnumber=password_details[0])
            button_add_update['text'] = 'Update'
            entry_title.insert(0, password_details[1])
            entry_login.insert(0, password_details[2])
            entry_password.insert(0, password_details[3])
            entry_website.insert(0, password_details[4])
            entry_notes.insert("1.0", password_details[5])

class FrameLocked(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid(row=0, column=0, sticky='NEWS', rowspan=2)
        self.configure(bg='white')
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 3), weight=1)

        def check_password(self):
            if entry_password.get() == ' ':
                self.destroy()
                start_app()
                statusbar.set('')
            else:
                statusbar.set('Wrong password, try again...')
                entry_password.delete(0, 'end')
                entry_password.focus()

        entry_password = ttk.Entry(self, width=30, show="*")
        entry_password.grid(row=1, column=0)
        entry_password.focus()
        entry_password.bind("<Return>", lambda event: check_password(self))

        password_button = ttk.Button(self, text='Enter password', width=30, command=lambda: check_password(self))
        password_button.grid(row=2, column=0)

root = tk.Tk()
root.title("Password Manager")
root.geometry("1000x700")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

''' TOP MENU '''
frame_buttons = tk.Frame(root, bg="white")
frame_buttons.grid(row=0, column=0, sticky='ew', columnspan=2)
frame_buttons.columnconfigure(8, weight=1)
add_button = tk.Button(frame_buttons, text='➕', font=('Calibri', buttons_size), borderwidth=0, fg='green', padx=2, bg='white', command=lambda: FrameAddUpdate(root, password_details='add'))
add_button.grid(row=0, column=0, sticky='w')

list_button = tk.Button(frame_buttons, text='📄', font=('Calibri', buttons_size), borderwidth=0, fg='blue', padx=2, bg='white', command=lambda: FrameMain(root), state='disabled')
list_button.grid(row=0, column=1, sticky='w')

lock_button = tk.Button(frame_buttons, text='🔒', font=('Calibri', buttons_size), borderwidth=0, fg='red', command=lambda: FrameLocked(root), padx=2, bg='white')
lock_button.grid(row=0, column=9, sticky='e')

statusbar = tk.StringVar()
statusbar_label = tk.Label(root, bg="white", textvariable=statusbar)
statusbar_label.grid(row=2, column=0, sticky="ew")

create_databases()
locked_frame = FrameLocked(root)

root.mainloop()