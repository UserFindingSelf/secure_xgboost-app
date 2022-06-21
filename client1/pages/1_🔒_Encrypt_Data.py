import os
import sys
import time
import subprocess
import streamlit as st
import securexgboost as xgb
from Utils import *

client = st.session_state.client_name

# Streamlit app
st.sidebar.title('CLIENT APP')
st.sidebar.markdown('#####') # Just for adding whitespace

st.subheader("Keys and certificates")
st.markdown('#####') # Just for adding whitespace

if st.button('Generate'):
     generate_certificate(client)
