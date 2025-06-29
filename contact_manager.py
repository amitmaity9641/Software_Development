import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File path for storing contacts
CONTACTS_FILE = "contacts.csv"

# Initialize contacts dataframe
def init_contacts():
    if os.path.exists(CONTACTS_FILE):
        return pd.read_csv(CONTACTS_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Phone", "Email", "Date Added"])

def save_contacts(df):
    df.to_csv(CONTACTS_FILE, index=False)

def add_contact(name, phone, email):
    new_contact = pd.DataFrame({
        "Name": [name],
        "Phone": [phone],
        "Email": [email],
        "Date Added": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    return pd.concat([st.session_state.contacts, new_contact], ignore_index=True)

def delete_contact(index):
    return st.session_state.contacts.drop(index).reset_index(drop=True)

def main():
    st.title("📒 Contact Management System")
    
    # Initialize session state
    if 'contacts' not in st.session_state:
        st.session_state.contacts = init_contacts()
    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = None
    
    # Sidebar for actions
    with st.sidebar:
        st.header("Actions")
        action = st.radio("Choose an action:", 
                         ["View Contacts", "Add Contact", "Edit Contact", "Delete Contact"])
    
    # Main content area
    if action == "View Contacts":
        st.header("Your Contacts")
        if len(st.session_state.contacts) > 0:
            st.dataframe(st.session_state.contacts, hide_index=True)
        else:
            st.info("No contacts found. Add your first contact!")
    
    elif action == "Add Contact":
        st.header("Add New Contact")
        with st.form("add_contact_form"):
            name = st.text_input("Name", max_chars=50)
            phone = st.text_input("Phone Number", max_chars=20)
            email = st.text_input("Email", max_chars=50)
            
            if st.form_submit_button("Save Contact"):
                if name and (phone or email):
                    st.session_state.contacts = add_contact(name, phone, email)
                    save_contacts(st.session_state.contacts)
                    st.success("Contact added successfully!")
                else:
                    st.error("Please provide at least a name and either phone or email")
    
    elif action == "Edit Contact":
        st.header("Edit Contact")
        if len(st.session_state.contacts) > 0:
            contact_index = st.selectbox(
                "Select contact to edit:",
                range(len(st.session_state.contacts)),
                format_func=lambda x: st.session_state.contacts.iloc[x]["Name"]
            )
            
            contact = st.session_state.contacts.iloc[contact_index]
            with st.form("edit_contact_form"):
                name = st.text_input("Name", value=contact["Name"], max_chars=50)
                phone = st.text_input("Phone Number", value=contact["Phone"], max_chars=20)
                email = st.text_input("Email", value=contact["Email"], max_chars=50)
                
                if st.form_submit_button("Update Contact"):
                    st.session_state.contacts.at[contact_index, "Name"] = name
                    st.session_state.contacts.at[contact_index, "Phone"] = phone
                    st.session_state.contacts.at[contact_index, "Email"] = email
                    save_contacts(st.session_state.contacts)
                    st.success("Contact updated successfully!")
        else:
            st.info("No contacts available to edit")
    
    elif action == "Delete Contact":
        st.header("Delete Contact")
        if len(st.session_state.contacts) > 0:
            contact_index = st.selectbox(
                "Select contact to delete:",
                range(len(st.session_state.contacts)),
                format_func=lambda x: st.session_state.contacts.iloc[x]["Name"]
            )
            
            contact = st.session_state.contacts.iloc[contact_index]
            st.warning(f"Are you sure you want to delete {contact['Name']}?")
            
            if st.button("Confirm Delete"):
                st.session_state.contacts = delete_contact(contact_index)
                save_contacts(st.session_state.contacts)
                st.success("Contact deleted successfully!")
        else:
            st.info("No contacts available to delete")

if __name__ == "__main__":
    main()