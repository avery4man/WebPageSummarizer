# Import necessary libraries
import streamlit as st
import time
# Import the summarize function from main.py
from main import summarize

# Set the layout of the Streamlit app to wide
st.set_page_config(layout='wide')

# Set the title of the Streamlit app
st.title('Web Page Summarizer')

# Create a text input for the user to enter a URL
url = st.text_input('Enter a URL')

# Set the title of the sidebar
st.sidebar.title('Summary Details')

# Function to fetch summary details
def fetch_summary_details(url):
    # Record the start time
    start_time = time.time()
    # Call the summarize function and get the summary, tokens used, cost, and model
    summary, tokens, cost, model = summarize(url)
    # Record the end time
    end_time = time.time()
    # Calculate the duration
    duration = end_time - start_time
    return summary, tokens, cost, model, duration

# Function to display summary details
def display_summary_details(summary, tokens, cost, model, duration):
    # Display the summary
    st.subheader('Summary')
    st.write(summary)
    # Display the model used in the sidebar
    st.sidebar.subheader('Model')
    st.sidebar.write(model)
    # Display the number of tokens used in the sidebar
    st.sidebar.subheader('Tokens used')
    st.sidebar.write(f'{tokens} tokens')
    # Display the cost in the sidebar
    st.sidebar.subheader('Cost')
    st.sidebar.write(f'${cost:.2f}')
    # Display the time taken in the sidebar
    st.sidebar.subheader('Time taken')
    st.sidebar.write(f'{duration:.2f} seconds')

# Create a button that triggers the summarization when a user clicks it
if st.button('Summarize'):
    # Show a spinner while the summarization is in progress
    with st.spinner('Summarizing...'):
        summary, tokens, cost, model, duration = fetch_summary_details(url)
    display_summary_details(summary, tokens, cost, model, duration)
