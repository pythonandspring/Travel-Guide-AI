import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database and create a table if it doesn't exist
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create Users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    place TEXT,
                    password TEXT)''')

# Admin credentials
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

# Function to update user details
def update_user(user_id, name, place):
    cursor.execute("UPDATE users SET name = ?, place = ? WHERE id = ?", (name, place, user_id))
    conn.commit()

# Streamlit page layout
st.title("User Authentication System")

# Initialize session state for admin login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

# Sidebar for navigation
option = st.sidebar.selectbox("Choose Option", ("Login", "Signup", "Admin Login"))

# Signup Page
if option == "Signup":
    st.subheader("Signup Form")
    name = st.text_input("Enter your Name")
    place = st.text_input("Enter your Place")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Sign Up"):
        if name and place and password:
            add_user(name, place, password)
            st.success("You have successfully signed up.")
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

    # Admin login form only appears if not already logged in
    if not st.session_state.admin_logged_in:
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin"):
            if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Logged in as Admin")
            else:
                st.error("Invalid admin credentials. Please try again.")
    else:
        # Display admin actions once logged in
        st.success("Logged in as Admin")
        
        # Show the user details table
        users = get_users()
        if users:
            df = pd.DataFrame(users, columns=["ID", "Name", "Place"])
            st.dataframe(df)

            # Select a user to update
            user_id = st.selectbox("Select User ID to Update", [user[0] for user in users])
            
            # Fetch current details of the selected user and store in session state
            selected_user = next((user for user in users if user[0] == user_id), None)
            if selected_user:
                st.session_state.selected_user = selected_user

            # Show update fields if a user is selected
            if st.session_state.selected_user:
                new_name = st.text_input("New Name", st.session_state.selected_user[1])
                new_place = st.text_input("New Place", st.session_state.selected_user[2])

                if st.button("Update User"):
                    if new_name and new_place:
                        update_user(st.session_state.selected_user[0], new_name, new_place)
                        st.success("User details updated successfully!")
                        st.experimental_rerun()  # Refresh page to show updated data
                    else:
                        st.warning("Please enter new details to update.")

        # Logout button for admin
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.session_state.selected_user = None
            st.experimental_rerun()
