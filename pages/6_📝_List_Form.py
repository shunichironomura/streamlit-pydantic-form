import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dynamic Form", page_icon="⚡")

st.header("Dynamic Form - Submit Multiple Items")

# Initialize an empty list to store the responses
if "responses" not in st.session_state:
    st.session_state.responses = []

# Define the form fields
fields = ["Name", "Age", "Email"]


@st.experimental_form
def dynamic_form():
    with st.form("dynamic_form"):
        st.subheader("Enter item details")

        # Create input fields for each item
        item = {}
        for field in fields:
            item[field] = st.text_input(field)

        # Add item button
        add_item = st.form_submit_button("Add Item")

        if add_item:
            st.session_state.responses.append(item)
            st.experimental_rerun()


# Call the dynamic form function
dynamic_form()

# Display the list of added items
st.subheader("Added Items")
if st.session_state.responses:
    df = pd.DataFrame(st.session_state.responses)
    st.table(df)
else:
    st.info("No items added yet.")

# Submit all items button
if st.button("Submit All Items"):
    if st.session_state.responses:
        st.success("All items submitted successfully!")
        st.write(st.session_state.responses)
        st.session_state.responses = []
    else:
        st.warning("No items to submit. Please add items first.")
