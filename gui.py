import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()



def register():
    u = reg_user.get()
    p = reg_pass.get()

    if u == "" or p == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    cur.execute("""
    INSERT OR IGNORE INTO users(username, password, role)
    VALUES (?, ?, 'user')
    """, (u, p))

    conn.commit()
    messagebox.showinfo("Success", "Registered Successfully")



def login():
    u = username_entry.get()
    p = password_entry.get()

    cur.execute("""
    SELECT role FROM users WHERE username=? AND password=?
    """, (u, p))

    data = cur.fetchone()

    if data:
        login_window.destroy()
        open_main(u, data[0])
    else:
        messagebox.showerror("Error", "Wrong Username or Password")



def load_books():
    tree.delete(*tree.get_children())

    for row in cur.execute("SELECT * FROM books"):
        tree.insert("", "end", values=row)



def add_book():
    title = book_entry.get()

    if title == "":
        messagebox.showerror("Error", "Enter book name")
        return

    cur.execute("""
    INSERT INTO books(title,status,lender,issue_date,due_date,return_date,fine)
    VALUES (?,?,?,?,?,?,?)
    """, (title, "Available", "", "", "", "", 0))

    conn.commit()
    load_books()



def issue_book():
    sel = tree.focus()
    if not sel:
        messagebox.showerror("Error", "Select book")
        return

    data = tree.item(sel)['values']
    book_id = data[0]

    user = borrower_entry.get()

    if user == "":
        messagebox.showerror("Error", "Enter borrower name")
        return

    cur.execute("""
    UPDATE books
    SET status='Issued',
        lender=?,
        issue_date=datetime('now'),
        due_date=datetime('now','+7 day')
    WHERE id=?
    """, (user, book_id))

    conn.commit()
    load_books()



def return_book():
    sel = tree.focus()
    if not sel:
        messagebox.showerror("Error", "Select book")
        return

    data = tree.item(sel)['values']
    book_id = data[0]

    cur.execute("""
    UPDATE books
    SET status='Available',
        lender='',
        return_date=datetime('now')
    WHERE id=?
    """, (book_id,))

    conn.commit()
    load_books()



def dashboard():
    cur.execute("SELECT COUNT(*) FROM books")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM books WHERE status='Issued'")
    issued = cur.fetchone()[0]

    cur.execute("SELECT SUM(fine) FROM books")
    fine = cur.fetchone()[0] or 0

    messagebox.showinfo(
        "Dashboard",
        f"📚 Total Books: {total}\n📕 Issued: {issued}\n💰 Fine: {fine}"
    )



def history():
    win = tk.Toplevel(root)
    win.title("Report")
    win.geometry("600x400")

    t = ttk.Treeview(win,
        columns=("Book","User","Action","Date"),
        show="headings")

    for c in ("Book","User","Action","Date"):
        t.heading(c, text=c)

    t.pack(fill="both", expand=True)

    for row in cur.execute("SELECT book_title, username, action, date FROM history"):
        t.insert("", "end", values=row)



def open_main(user, role):
    global root, tree, book_entry, borrower_entry

    root = tk.Tk()
    root.title("Library Admin Panel")
    root.geometry("1100x700")
    root.configure(bg="#f4f6f9")

    
    header = tk.Frame(root, bg="#2c3e50", height=60)
    header.pack(fill="x")

    tk.Label(header,
             text=f"📚 Library System | {user} ({role})",
             bg="#2c3e50", fg="white",
             font=("Arial", 13, "bold")).pack(side="left", padx=15)

    def logout():
        root.destroy()
        main_login()

    tk.Button(header, text="Logout",
              bg="red", fg="white",
              command=logout).pack(side="right", padx=10)

    
    body = tk.Frame(root, bg="#f4f6f9")
    body.pack(fill="both", expand=True)

   
    side = tk.Frame(body, bg="#34495e", width=200)
    side.pack(side="left", fill="y")

    tk.Label(side, text="MENU",
             bg="#34495e", fg="white",
             font=("Arial", 12, "bold")).pack(pady=20)

    tk.Button(side, text="Dashboard",
              bg="#1abc9c", fg="white",
              command=dashboard).pack(pady=10)

    tk.Button(side, text="Report",
              bg="#3498db", fg="white",
              command=history).pack(pady=10)

   
    main = tk.Frame(body, bg="#f4f6f9")
    main.pack(side="left", fill="both", expand=True)

    tk.Label(main, text="Book Title", bg="#f4f6f9").pack()

    book_entry = tk.Entry(main, width=40)
    book_entry.pack()

    tk.Button(main, text="Add Book",
              bg="green", fg="white",
              command=add_book).pack(pady=5)

    tk.Label(main, text="Borrower", bg="#f4f6f9").pack()

    borrower_entry = tk.Entry(main, width=40)
    borrower_entry.pack()

    tk.Button(main, text="Issue Book",
              bg="orange", fg="white",
              command=issue_book).pack(pady=5)

    tk.Button(main, text="Return Book",
              bg="purple", fg="white",
              command=return_book).pack(pady=5)

  
    tree = ttk.Treeview(main,
        columns=("ID","Title","Status","Lender","Issue","Due","Return","Fine"),
        show="headings")

    for c in tree["columns"]:
        tree.heading(c, text=c)

    tree.pack(fill="both", expand=True)

    load_books()
    root.mainloop()



def main_login():
    global login_window, username_entry, password_entry, reg_user, reg_pass

    login_window = tk.Tk()
    login_window.title("Login System")
    login_window.geometry("400x500")
    login_window.configure(bg="#1e1e2f")

    tk.Label(login_window,
             text="LIBRARY LOGIN",
             bg="#1e1e2f", fg="white",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(login_window, text="Username", bg="#1e1e2f", fg="white").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password", bg="#1e1e2f", fg="white").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="LOGIN",
              bg="green", fg="white",
              command=login).pack(pady=10)

    tk.Label(login_window, text="Register", bg="#1e1e2f", fg="white").pack()

    reg_user = tk.Entry(login_window)
    reg_user.pack()

    reg_pass = tk.Entry(login_window, show="*")
    reg_pass.pack()

    tk.Button(login_window, text="REGISTER",
              bg="blue", fg="white",
              command=register).pack(pady=10)

    login_window.mainloop()



main_login()