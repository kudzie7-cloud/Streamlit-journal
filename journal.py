import streamlit as st
import sqlite3
from datetime import datetime

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ""
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'new_entry' not in st.session_state:
    st.session_state['new_entry'] = ""

# Database connection
db_path = r"C:\Users\PLEASE BUY ME\Documents\Journals\our_journal.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS entries
             (date TEXT, user TEXT, entry TEXT)''')
conn.commit()

# Function: Authentication
def authenticate(username, password):
    credentials = {
        'Kudzie': 'kudzie7',
        'Didi': 'dinga95',
    }
    return credentials.get(username) == password

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    body {
        background-image: url('https://www.wallpapertip.com/wmimgs/87-878200_heart-wallpaper-hd.jpg');
        background-size: cover;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #d63384;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login Page
def login_page():
    st.title("Kudzie and Dee's Journal 💌")
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.session_state['page'] = 'journal'  # Navigate to the journal page
        else:
            st.error("Invalid username or password")

# Journal Page
def journal_page():
    # Sidebar logout button
    with st.sidebar:
        st.write(f"Logged in as **{st.session_state['user']}**")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['page'] = 'login'  # Navigate back to the login page

    st.title("Kudzie and Dee's Journal 💌")
    st.subheader(f"Hello, {st.session_state['user']}!")

    # Input for new journal entry
    if 'clear_entry' not in st.session_state:
        st.session_state['clear_entry'] = False  # Initialize clearing state

    if st.session_state['clear_entry']:
        st.session_state['new_entry'] = ""  # Reset the input box if cleared
        st.session_state['clear_entry'] = False  # Reset the clear flag

    new_entry_input = st.text_area("Write your journal entry here...", key="new_entry")

    if st.button("Submit Entry"):
        if new_entry_input.strip():
            try:
                # Save entry to the database
                c.execute("INSERT INTO entries (date, user, entry) VALUES (?, ?, ?)",
                          (datetime.now().isoformat(), st.session_state['user'], new_entry_input))
                conn.commit()
                st.success("Entry submitted successfully!")
                st.session_state['clear_entry'] = True  # Trigger clearing input box
            except Exception as e:
                st.error(f"Error saving entry: {e}")
        else:
            st.error("Entry cannot be empty.")

    # Display past entries
    st.subheader("Past Entries")
    try:
        c.execute("SELECT date, user, entry FROM entries ORDER BY date DESC")
        rows = c.fetchall()
        for row in rows:
            formatted_date = datetime.fromisoformat(row[0]).strftime("%b %d, %Y %I:%M %p")
            st.markdown(f"**{row[1]}** on {formatted_date}")
            st.write(row[2])
            st.markdown("---")
    except Exception as e:
        st.error(f"Error loading entries: {e}")

# Main app navigation
if st.session_state['page'] == 'login':
    login_page()
elif st.session_state['page'] == 'journal' and st.session_state['logged_in']:
    journal_page()
else:
    st.warning("You need to log in first!")
    st.session_state['page'] = 'login'
