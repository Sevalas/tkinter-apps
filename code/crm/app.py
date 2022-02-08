from sqlite3.dbapi2 import Error
from tkinter import *
from tkinter import messagebox, ttk

import db as db
from client import Client

db.startDb()

root = Tk()
root.configure(background='#212121')
root.title('My CRM')
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)

ttk_style = ttk.Style()
ttk_style.theme_use('clam')

ttk_style.configure("TButton", foreground='#fff', background='#333333', relief ='flat')
ttk_style.map('TButton', background=[('active', '#4d4d4d')])
ttk_style.configure("Treeview", background='#333333', fieldbackground='#333333', foreground='#fff')
ttk_style.configure("Treeview.Heading", background='#333333', fieldbackground='#333333', foreground='#fff')
ttk_style.map('Treeview.Heading', background=[('active', '#4d4d4d')])
ttk_style.configure("TLabel", background='#212121', foreground='#fff')
ttk_style.configure("TEntry", background='#333333', fieldbackground='#333333', foreground='#fff')


def render_clients():
    client_tree.delete(*client_tree.get_children())
    clients = db.selectClients()
    for client in clients:
        client_tree.insert('', END, client.id, values=[client.names, client.phone, client.enterprise])

def add_client_window():
    add_window = Toplevel(background='#212121')
    add_window.title('Adding a new client')
    add_window.geometry('500x100')
    add_window.grid_columnconfigure(0, weight=0)
    add_window.grid_columnconfigure(1, weight=1)

    names_label = ttk.Label(add_window, text='Names*')
    names_entry = ttk.Entry(add_window)
    names_label.grid(row=0, column=0)
    names_entry.grid(row=0, column=1, sticky="nwe")

    phone_label = ttk.Label(add_window, text='Phone*')
    phone_entry = ttk.Entry(add_window)
    phone_label.grid(row=1, column=0)
    phone_entry.grid(row=1, column=1, sticky="nwe")

    enterprise_label = ttk.Label(add_window, text='Enterprise*')
    enterprise_entry = ttk.Entry(add_window)
    enterprise_label.grid(row=2, column=0)
    enterprise_entry.grid(row=2, column=1, sticky="nwe")

    def add_client():

        def missing_field_message(field_name):
            messagebox.showerror('Error', 'The {} field is requierd'.format(field_name), parent=add_window)

        if not names_entry.get(): missing_field_message('names'); return
        if not phone_entry.get(): missing_field_message('phone'); return
        if not enterprise_entry.get(): missing_field_message('enterprise'); return

        client = Client(
            names = names_entry.get(),
            phone = phone_entry.get(),
            enterprise = enterprise_entry.get()  
        )

        try:
            db.insertClient(client)
            add_window.destroy()
            render_clients()
        except Error:
            print(Error)

    save_client_btn = ttk.Button(add_window, text='Save', command=add_client)
    save_client_btn.grid(row=3, column=1, sticky="nswe")

    add_window.bind("<Return>", (lambda event: add_client()))
    add_window.grab_set()

def update_client_window():

    if not client_tree.selection() or len(client_tree.selection()) != 1:
        messagebox.showerror('Error', 'Only one client can be updated at a time')
    else:

        update_window = Toplevel(background='#212121')
        update_window.title('Upadate a client')
        update_window.geometry('500x100')
        update_window.grid_columnconfigure(0, weight=0)
        update_window.grid_columnconfigure(1, weight=1)

        client = db.selectClientsbyId(client_tree.selection())[0]

        print(db.selectClientsbyId(client_tree.selection()))

        names_label = ttk.Label(update_window, text='Names*')
        names_entry = ttk.Entry(update_window)
        names_entry.insert(0, client.names)
        names_label.grid(row=0, column=0)
        names_entry.grid(row=0, column=1, sticky="nwe",)

        phone_label = ttk.Label(update_window, text='Phone*')
        phone_entry = ttk.Entry(update_window)
        phone_entry.insert(0, client.phone)
        phone_label.grid(row=1, column=0)
        phone_entry.grid(row=1, column=1, sticky="nwe")

        enterprise_label = ttk.Label(update_window, text='Enterprise*')
        enterprise_entry = ttk.Entry(update_window)
        enterprise_entry.insert(0, client.enterprise)
        enterprise_label.grid(row=2, column=0)
        enterprise_entry.grid(row=2, column=1, sticky="nwe")

        def update_client():
            client_tree.grid_rowconfigure
            def missing_field_message(field_name):
                messagebox.showerror('Error', 'The {} field is requierd'.format(field_name), parent=update_window)        

            if not names_entry.get(): missing_field_message('names'); return
            if not phone_entry.get(): missing_field_message('phone'); return
            if not enterprise_entry.get(): missing_field_message('enterprise'); return

            updatedClient = Client(
                id = client.id,
                names = names_entry.get(),
                phone = phone_entry.get(),
                enterprise = enterprise_entry.get()  
            )

            try:
                db.updateClient(updatedClient)
                update_window.destroy()
                render_clients()
            except Error:
                print(Error)

        update_client_btn = ttk.Button(update_window, text='Update', command=update_client)
        update_client_btn.grid(row=3, column=1, sticky="nswe")

        update_window.bind("<Return>", (lambda event: update_client()))
        update_window.grab_set()

def remove_client():
    clients = db.selectClientsbyId(client_tree.selection())
    if clients and len(clients) != 0:
        confirmation = messagebox.askokcancel(
            'Sure?', 
            'You are going to delete the following user(s): {}'.format(', '.join(client.names for client in clients))
        )
        if confirmation:
            db.deleteClients(client_tree.selection())
            render_clients()

add_client_btn = ttk.Button(root, text="Add a new client", command=add_client_window)
add_client_btn.grid(column=0, row=0, sticky="nwe")

update_client_btn = ttk.Button(root, text="Update client", command=update_client_window)
update_client_btn.grid(column=1, row=0, sticky="nwe")

remove_client_btn = ttk.Button(root, text="Remove client(s)", command=remove_client)
remove_client_btn.grid(column=2, row=0, sticky="nwe")

client_tree_wrapper = Frame(root)
client_tree_wrapper.grid(column=0, row=1, columnspan=3, sticky="nsew")
client_tree_wrapper.grid_columnconfigure(0, weight= 3)
client_tree_wrapper.grid_columnconfigure(1, weight= 3)

client_tree = ttk.Treeview(client_tree_wrapper)
client_tree['columns'] = ('Names', 'Phone', 'Enterprise')
client_tree.column('#0', width=0, stretch=NO)
client_tree.column('Names')
client_tree.column('Phone')
client_tree.column('Enterprise')

client_tree.heading('Names', text='Names',)
client_tree.heading('Phone', text='Phone')
client_tree.heading('Enterprise', text='Enterprise')

client_tree.pack(side=LEFT, fill=BOTH, expand=TRUE)

scrollbar = ttk.Scrollbar(client_tree_wrapper, orient = "vertical", command = client_tree.yview)
scrollbar.pack(side=RIGHT, fill=Y)
client_tree.configure(yscrollcommand = scrollbar.set)

render_clients()

root.mainloop()
