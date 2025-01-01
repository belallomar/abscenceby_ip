import streamlit as st
import pandas as pd
import socket
from datetime import datetime

# Initialize CSV file
CSV_FILE = "students_data.csv"
MONTH_COLUMN = datetime.now().strftime("%B")  # Get current month

# Function to initialize the CSV file if it doesn't exist
def initialize_csv():
    if not pd.io.common.file_exists(CSV_FILE):
        df = pd.DataFrame(columns=["Name", "Device_IP", "Phone_IP", MONTH_COLUMN])
        df.to_csv(CSV_FILE, index=False)

# Function to get the client's IP address
def get_client_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Function to check attendance and update the CSV file
def mark_attendance(ip):
    df = pd.read_csv(CSV_FILE)

    # Check if the IP exists in Device_IP or Phone_IP
    if ip in df["Device_IP"].values or ip in df["Phone_IP"].values:
        user_index = df.index[(df["Device_IP"] == ip) | (df["Phone_IP"] == ip)].tolist()[0]
        df.at[user_index, MONTH_COLUMN] = 1  # Mark as attended
        df.to_csv(CSV_FILE, index=False)
        return "Your attendance has been recorded."
    else:
        return "Your device is not registered for attendance."

# Function to register a new student
def register_student(name):
    df = pd.read_csv(CSV_FILE)
    client_ip = get_client_ip()

    # Check if IP is already registered
    if client_ip in df["Device_IP"].values or client_ip in df["Phone_IP"].values:
        return "This device is already registered."

    # Add new student with the current IP
    new_entry = {
        "Name": name,
        "Device_IP": client_ip,
        "Phone_IP": "",  # Placeholder for phone IP
        MONTH_COLUMN: 0  # Default attendance for the month
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return "Student registered successfully."

# Streamlit app setup
initialize_csv()
st.title("College Attendance System")

menu = st.sidebar.radio("Menu", ["Mark Attendance", "Register Student"])

if menu == "Mark Attendance":
    st.write("Scan the QR code and open the link to mark your attendance.")

    # Get user's IP address
    client_ip = get_client_ip()

    # Mark attendance
    message = mark_attendance(client_ip)
    st.success(message)

elif menu == "Register Student":
    st.write("Register a new student by filling the form below.")

    name = st.text_input("Enter your name")

    if st.button("Register"):
        if name.strip():
            message = register_student(name.strip())
            st.success(message)
        else:
            st.error("Name cannot be empty.")

# Debugging and display current data (for admin purposes, optional)
if st.checkbox("Show Current Attendance Data"):
    st.write(pd.read_csv(CSV_FILE))
