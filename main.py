import sqlite3

# Connect to SQLite database (creates database if it doesn't exist)
def connect_db():
    return sqlite3.connect("database.db")

# Create users table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add a new user
def add_user(name, email, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Email already exists!")
    finally:
        conn.close()

# View all users
def view_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Delete a user by ID
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    print("User deleted successfully!")

# Update user (optional improvement)
def update_user(user_id, new_name, new_email):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (new_name, new_email, user_id)
        )
        conn.commit()
        print("User updated successfully!")
    except sqlite3.IntegrityError:
        print("Error: Email already exists!")
    finally:
        conn.close()

# Initialize table
create_table()

# Menu-driven interface
while True:
    print("\n==== User Management System ====")
    print("1. Add User")
    print("2. View Users")
    print("3. Delete User")
    print("4. Update User")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        add_user(name, email, password)

    elif choice == "2":
        users = view_users()
        if users:
            print("\nID | Name | Email")
            for user in users:
                print(user[0], "|", user[1], "|", user[2])
        else:
            print("No users found.")

    elif choice == "3":
        uid = input("Enter user ID to delete: ")
        delete_user(uid)

    elif choice == "4":
        uid = input("Enter user ID to update: ")
        new_name = input("Enter new name: ")
        new_email = input("Enter new email: ")
        update_user(uid, new_name, new_email)

    elif choice == "5":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please try again.")
