import streamlit as st
import sqlite3
import pandas as pd

# Create a SQLite database and a table to store user data
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create Users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    place TEXT,
                    password TEXT)''')

# Admin credentials (these can be stored in the database too)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Function to add user to the database
def add_user(name, place, password):
    cursor.execute("INSERT INTO users (name, place, password) VALUES (?, ?, ?)", (name, place, password))
    conn.commit()

# Function to get all users
def get_users():
    cursor.execute("SELECT id, name, place FROM users")
    users = cursor.fetchall()
    return users

# Function to check admin login
def admin_login(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    else:
        return False

# Streamlit page layout
st.title("User Authentication System")

# Sidebar for navigation
option = st.sidebar.selectbox("Choose Option", ("Login", "Signup", "Admin Login"))

# Signup Page
if option == "Signup":
    st.subheader("Signup Form")

    # Collect user input
    name = st.text_input("Enter your Name")
    place = st.text_input("Enter your Place")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Sign Up"):
        if name and place and password:
            add_user(name, place, password)
            st.success("YOU HAVE SUCCESSFULLY SIGNED UP")
        else:
            st.warning("Please fill in all the details.")

# Login Page
elif option == "Login":
    st.subheader("Login Form")

    username = st.text_input("Enter your Name")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid credentials. Please try again.")

# Admin Login
elif option == "Admin Login":
    st.subheader("Admin Login")

    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if admin_login(admin_username, admin_password):
            st.success("Logged in as Admin")
            
            # Show the user details table
            users = get_users()
            if users:
                df = pd.DataFrame(users, columns=["ID", "Name", "Place"])
                st.dataframe(df)

            # Admin can update user details (name or place)
            user_id = st.selectbox("Select User to Update", [user[0] for user in users])
            user_name = st.text_input("New Name")
            user_place = st.text_input("New Place")

            if st.button("Update User"):
                if user_name or user_place:
                    if user_name:
                        cursor.execute("UPDATE users SET name=? WHERE id=?", (user_name, user_id))
                    if user_place:
                        cursor.execute("UPDATE users SET place=? WHERE id=?", (user_place, user_id))
                    conn.commit()
                    st.success("User details updated successfully!")
                else:
                    st.warning("Please enter new details to update.")
        else:
            st.error("Invalid admin credentials. Please try again.")
