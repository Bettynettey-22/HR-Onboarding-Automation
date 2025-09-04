import streamlit as st
import pandas as pd
import random
import os

# ======================
# Utility Functions
# ======================

def generate_employee_id(name, dept):
    """Generate a unique employee ID"""
    initials = "".join([n[0] for n in name.split()]).upper()
    number = random.randint(1000, 9999)
    return f"{dept[:3].upper()}-{initials}{number}"

def add_employee(name, dept, email, start_date):
    """Create employee record with welcome message"""
    emp_id = generate_employee_id(name, dept)
    welcome_msg = f"""
    🌟 Hello {name},

    Welcome to the {dept} team at Account Way Consult!  
    Your Employee ID is "{emp_id}".  
    Start Date: {start_date}  

    Best regards,  
    HR Team
    """
    return {
        "Employee ID": emp_id,
        "Name": name,
        "Department": dept,
        "Email": email,
        "Start Date": start_date,
        "Welcome Message": welcome_msg.strip()
    }

def load_data(file="new_hires.csv"):
    """Load or create new hires CSV file"""
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Employee ID", "Name", "Department", "Email", "Start Date", "Welcome Message"])

def save_data(df, file="new_hires.csv"):
    """Save data back to CSV"""
    df.to_csv(file, index=False)

# ======================
# Streamlit UI Styling
# ======================

st.set_page_config(
    page_title="HR Onboarding Automation",
    page_icon="🌟",
    layout="centered"
)

# Custom CSS for Yellow & White theme
st.markdown(
    """
    <style>
        /* Background color */
        .stApp {
            background-color: #fffbea; /* soft light yellow */
        }
        /* Titles */
        h1, h2, h3 {
            color: #d4a017; /* golden yellow */
        }
        /* Form labels */
        label {
            color: #b58900 !important;
            font-weight: 600 !important;
        }
        /* Buttons */
        .stButton>button {
            background-color: #ffcc00;
            color: black;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #e6b800;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================
# Streamlit UI
# ======================

st.title("🌟 HR Onboarding Automation System")
st.write("Add new employees and instantly generate onboarding messages.")

# Load existing data
df = load_data()

# Employee Input Form
with st.form("employee_form"):
    st.subheader("➕ Add New Employee")

    name = st.text_input("Full Name")
    dept = st.selectbox("Department", ["Sales", "Operations", "Finance", "HR", "IT"])
    email = st.text_input("Email")
    start_date = st.date_input("Start Date")

    submitted = st.form_submit_button("Add Employee")

    if submitted:
        if name and dept and email and start_date:
            new_emp = add_employee(name, dept, email, str(start_date))
            df = pd.concat([df, pd.DataFrame([new_emp])], ignore_index=True)
            save_data(df)
            st.success(f"✅ Employee {name} added successfully!")
            st.info(f"Generated Employee ID: {new_emp['Employee ID']}")
            st.markdown(new_emp["Welcome Message"])
        else:
            st.error("⚠️ Please fill all fields before submitting.")
