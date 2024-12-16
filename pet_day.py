import streamlit as st
import pandas as pd

# Hardcoded users for demonstration purposes
USER_CREDENTIALS = {
    "admin": "password123",  # Admin user
    "suvi": "pass1",
    "nihi": "pass2",
    "varsha": "pass3"
}

# Initialize session state for customers and login
if 'customers' not in st.session_state:
    st.session_state.customers = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Constants
MAX_GLOBAL_SLOTS = 11  # Global pet limit across all customers
DOG_COST_PER_DAY = 20  # in USD
CAT_COST_PER_DAY = 15  # in USD
USD_TO_INR = 83  # Conversion rate from USD to INR

# Function to initialize customer profile in session state
def initialize_customer(username):
    # Initialize customer data with payment status
    if username not in st.session_state.customers:  # Prevent re-initialization
        st.session_state.customers[username] = {
            'pets': [],
            'total_cost': 0,
            'owner_details': {},  # Store owner details
            'payment_status': 'Pending',  # Default payment status
            'payment_method': None  # Track payment method
        }
    else:
        print(f"Customer data already exists for {username}")  # Debugging output

# Function to calculate the total number of pets across all customers
def calculate_total_pets():
    total_pets = 0
    for customer_data in st.session_state.customers.values():
        total_pets += len(customer_data['pets'])
    return total_pets

# Function to add a pet to the current customer
def add_pet(pet_type, pet_name, pet_days=1, pet_age=None, pet_breed=None, food_type=None, special_care=None, owner_name=None, contact_number=None, address=None, date_of_joining=None, timing=None, pet_photo=None, gender=None):
    current_user = st.session_state.current_user
    customer_data = st.session_state.customers[current_user]
    total_pets = calculate_total_pets()  # Calculate total pets globally

    # Check if adding a new pet exceeds the global limit
    if total_pets < MAX_GLOBAL_SLOTS:
        # Add owner details
        customer_data['owner_details'] = {
            'name': owner_name,
            'contact': contact_number,
            'address': address
        }

        # Add pet details including date of joining, timing, and other info
        customer_data['pets'].append({
            'type': pet_type,
            'name': pet_name,
            'days': pet_days,
            'age': pet_age,
            'breed': pet_breed,
            'food': food_type,
            'special_care': special_care,  # Add special care instructions
            'date_of_joining': date_of_joining,  # Date of joining
            'timing': timing,  # Timing for the pet's stay
            'photo': pet_photo,  # Store the pet's photo
            'gender': gender  # Add gender
        })
        st.success(f"Added {pet_name} to {current_user}'s pets with owner {owner_name}")
    else:
        st.error("Global maximum capacity reached! Cannot add more pets.")

# Function to delete a pet from the current customer
def delete_pet(pet_name):
    current_user = st.session_state.current_user
    customer_data = st.session_state.customers[current_user]
    customer_data['pets'] = [pet for pet in customer_data['pets'] if pet['name'] != pet_name]

# Function to calculate total cost based on the pets and days for the current customer
def calculate_cost(username):
    customer_data = st.session_state.customers.get(username, {})
    total_cost = 0
    if 'pets' in customer_data:
        for pet in customer_data['pets']:
            pet_days = pet.get('days', 1)
            if pet['type'] == 'Dog':
                total_cost += DOG_COST_PER_DAY * pet_days
            elif pet['type'] == 'Cat':
                total_cost += CAT_COST_PER_DAY * pet_days
    return total_cost

# Function to calculate total cost in INR
def calculate_cost_in_inr(username):
    total_cost_usd = calculate_cost(username)
    total_cost_inr = total_cost_usd * USD_TO_INR
    return total_cost_inr

# Function to log in a user
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.current_user = username
        if username != 'admin':
            initialize_customer(username)  # Initialize customer data for non-admins
        st.success(f"Successfully logged in as {username}!")
    else:
        st.error("Invalid username or password")

# Function to log out the current user
def logout():
    st.session_state.current_user = None  # Only clear the current user, leave customers intact
    st.info("You have been logged out.")

# Inject custom CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E6E6FA; /* Light Lavender */
    }
    h1, h2, h3 {
        color: #454556; /* Dark Gray */
    }
    .stButton button {
        background-color: #C67171; /* Darker Rose */
        color: white;
        border-radius: 10px;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .stButton button:hover {
        background-color: #454556; /* Dark Gray */
        color: white;
        transform: scale(1.05);
    }
    .stTextInput, .stSelectbox, .stTextArea {
        border: none; /* No border */
        padding: 5px;
    }
    .stTextInput:focus, .stSelectbox:focus, .stTextArea:focus {
        border: none; /* No border on focus */
        outline: none; /* No outline on focus */
    }
    .stContainer {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        border-radius: 10px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #E6E6FA; /* Light Lavender */
#     }
#     h1, h2, h3 {
#         color: #454556; /* Dark Gray */
#     }
#     .stButton button {
#         background-color: #C67171; /* Darker Rose */
#         color: white;
#         border-radius: 10px;
#         transition: background-color 0.3s ease, transform 0.3s ease;
#     }
#     .stButton button:hover {
#         background-color: #454556; /* Dark Gray */
#         color: white;
#         transform: scale(1.05);
#     }
#     .stTextInput, .stSelectbox, .stTextArea {
#         border: none; /* No border */
#         padding: 5px;
#     }
#     .stTextInput:focus, .stSelectbox:focus, .stTextArea:focus {
#         border: none; /* No border on focus */
#         outline: 2px solid #FF69B4; /* Hot Pink outline on focus */
#     }
#     .stContainer {
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
#         border-radius: 10px;
#         padding: 15px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Streamlit app
if not st.session_state.current_user:
    # Display login page
    st.title("🐾 Pet Day Care Center Login")
    
    # Removed the image section here

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login(username, password)

    # Bold contact details at the bottom of the login page
    st.markdown("---")
    st.markdown("**Managed by the Pet Day Care Center © 2024**")
    st.markdown("**3, Bharathi Salai, Opposite to SRM University, Ramapuram, Chennai-600089**")
    st.markdown("**Contact details: +91 94444 84444**")
    st.markdown("**Shop Timings: 7:00 AM - 9:00 PM**")
    st.markdown('**"Available 24/7/365"**')

else:
    # Admin dashboard
    if st.session_state.current_user == 'admin':
        st.title("🐾 Admin Dashboard")
        st.header("📋 All Customers and Pets")
        
        # Global capacity display
        total_pets = calculate_total_pets()
        st.write(f"Global Pet Capacity: {total_pets}/{MAX_GLOBAL_SLOTS}")
        
        if not st.session_state.customers:
            st.write("No customers or pets found.")
        else:
            for customer, data in st.session_state.customers.items():
                st.subheader(f"Customer: {customer}")
                if data['pets']:
                    st.write(f"Owner Details:")
                    st.write(f"Name: {data['owner_details'].get('name', 'N/A')}")
                    st.write(f"Contact: {data['owner_details'].get('contact', 'N/A')}")
                    st.write(f"Address: {data['owner_details'].get('address', 'N/A')}")
                    st.write("Pets:")
                    for pet in data['pets']:
                        st.write(f"{pet['name']} - {pet['type']} - {pet['age']} months - {pet['breed']} - {pet['days']} day(s) - Food: {pet['food']} - Date of Joining: {pet.get('date_of_joining', 'N/A')} - Timing: {pet.get('timing', 'N/A')} - Gender: {pet.get('gender', 'N/A')}")
                        if pet.get('special_care'):
                            st.write(f"Special Care Instructions: {pet['special_care']}")
                        if pet.get('photo'):
                            st.image(pet['photo'], caption=f"{pet['name']}'s photo", width=150)
                    total_cost_inr = calculate_cost_in_inr(customer)
                    st.write(f"Total cost for {customer}: ₹{total_cost_inr}")
                    
                else:
                    st.write(f"No pets currently registered for {customer}.")
                
                st.write(f"Payment Status for {customer}: {data.get('payment_status', 'Not available')}")
                if data['payment_status'] == 'Paid':
                    st.write(f"Paid via: {data.get('payment_method', 'Not available')}")

        if st.button("Logout"):
            logout()
    else:
        # Main app content for non-admin users (customers)
        st.title(f"🐾 Welcome, {st.session_state.current_user}")

        with st.sidebar:
            st.header("💡 Quick Actions")
            current_user_data = st.session_state.customers[st.session_state.current_user]
            total_pets = calculate_total_pets()
            st.write(f"📊 Global Capacity: {total_pets}/{MAX_GLOBAL_SLOTS}")
            st.write(f"🧮 Total cost: ₹{calculate_cost_in_inr(st.session_state.current_user)}")
            if st.button("Logout"):
                logout()

        with st.expander("🐶 Current Pets", expanded=True):
            if current_user_data['pets']:
                for pet in current_user_data['pets']:
                    st.write(f"{pet['name']} - {pet['type']} - {pet['age']} months - {pet['breed']} - {pet['days']} day(s) - Date of Joining: {pet.get('date_of_joining', 'N/A')} - Timing: {pet.get('timing', 'N/A')} - Food: {pet['food']} - Gender: {pet.get('gender', 'N/A')}")
                    if pet.get('special_care'):
                        st.write(f"Special Care Instructions: {pet['special_care']}")
                    if pet.get('photo'):
                        st.image(pet['photo'], caption=f"{pet['name']}'s photo", width=150)
            else:
                st.write("No pets currently in daycare.")

        st.header("➕ Add a Pet")
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            pet_type = st.selectbox("Select Pet Type", ["Dog", "Cat"])
        with col2:
            pet_name = st.text_input("Enter Pet Name")
        with col3:
            pet_days = st.number_input("Number of Days", min_value=1, value=1)

        col4, col5 = st.columns(2)
        with col4:
            pet_age = st.number_input("Pet Age (in months)", min_value=1, value=1)
        with col5:
            pet_breed = st.text_input("Pet Breed")

        food_type = st.selectbox("Select Food Type", ["Wet Food", "Dry Food"])
        special_care = st.text_area("Special Care Instructions")

        # New fields for date of joining, timing, gender, and photo upload
        date_of_joining = st.date_input("Date of Joining")
        timing = st.text_input("Preferred Timing (e.g., 9 AM - 5 PM)")

        # Add gender field
        gender = st.selectbox("Select Gender", ["Male", "Female", "Unknown"])

        # Upload a pet photo
        pet_photo = st.file_uploader("Upload a Pet Photo", type=['jpg', 'jpeg', 'png'])

        st.header("🧑‍💼 Owner Details")
        col6, col7 = st.columns([2, 3])
        with col6:
            owner_name = st.text_input("Enter Owner Name")
        with col7:
            contact_number = st.text_input("Enter Contact Number")
        address = st.text_area("Enter Address")

        if st.button("Add Pet"):
            if pet_name and owner_name and contact_number:  # Ensure necessary details are provided
                add_pet(pet_type, pet_name, pet_days, pet_age, pet_breed, food_type, special_care, owner_name, contact_number, address, date_of_joining, timing, pet_photo, gender)
                st.session_state['pet_name'] = ""
                st.session_state['owner_name'] = ""
                st.session_state['contact_number'] = ""
            else:
                st.warning("Please fill in all required fields for pet and owner details.")
        if current_user_data['pets']:
            st.header("🗑 Delete a Pet")
            pet_to_delete = st.selectbox("Select Pet to Delete", [pet['name'] for pet in current_user_data['pets']])
    
            if st.button("Delete Pet"):
                delete_pet(pet_to_delete)  # Call the delete function
                 # Instead of rerunning, just provide feedback
                st.success(f"Successfully deleted {pet_to_delete}. Refreshing the list...")

                # Update the session state to refresh the app without using experimental_rerun
                st.session_state.customers[st.session_state.current_user] = current_user_data


        with st.expander("💰 Cost Calculation & Payment", expanded=True):
            total_cost_inr = calculate_cost_in_inr(st.session_state.current_user)
            st.write(f"Total cost for {len(current_user_data['pets'])} pet(s): ₹{total_cost_inr}")

            payment_method = st.selectbox("Select Payment Method", ["Credit Card 💳", "PayPal 🅿", "Cash 💵"])
            if st.button("Make Payment"):
                if total_cost_inr > 0:
                    current_user_data['payment_status'] = 'Paid'
                    current_user_data['payment_method'] = payment_method
                    st.success(f"Payment of ₹{total_cost_inr} received via {payment_method}")
                else:
                    st.warning("No pets in daycare. Total cost is ₹0.")

        # st.header("🐕 Pet Images")
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.image("images/dog.png", caption="Dog", width=150)
        # with col2:
        #     st.image("images/cat.png", caption="Cat", width=150)

# Footer
st.markdown("---")
st.caption("Managed by the Pet Day Care Center © 2024")
st.caption("3, Bharathi Salai, Opposite to SRM University, Ramapuram, Chennai-600089")
st.caption("Contact details: +91 94444 84444")
st.caption("Shop Timings: 7:00 AM - 9:00 PM")
st.caption('"Available 24/7/365"')