import os
import sys
import time
import subprocess
import streamlit as st
import securexgboost as xgb

# Streamlit app
st.set_page_config(
    page_title="Homepage",
)
st.sidebar.title('CLIENT APP')
st.sidebar.markdown('#####') # Just for adding whitespace

if 'client_name' not in st.session_state:
    st.session_state.client_name = ''

st.subheader("Client Configuration")
client = st.text_input("Enter your client name")

# After client name added
if st.button('Enter'):
    if client:
        st.session_state.client_name = client
        st.success("Name saved as '" + client + "'")
