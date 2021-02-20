import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from wsb import main

sidebar = {
    "wallstreetbets": "Wall Street Bets",
    "bots": "Bots"
}

st.sidebar.title("Control Panel")

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)
option = st.sidebar.selectbox(
    'Which Dashboard',
    list(sidebar.keys()),
    format_func=sidebar.get
)

st.title(option)

if option == 'wallstreetbets':
    st.subheader('This is a scraper for WSB')
    kinds = st.multiselect('Multiselect', ['new', 'hot', 'top'])
    st.write(kinds)
    st.button('Hit me')
    st.checkbox('Check me out')
    x = st.slider('x')
    st.write(x, 'squared is', x * x)
    st.progress(x)
    st.spinner()
    with st.spinner(text='In progress'):
        time.sleep(5)
        st.success('Done')
    st.balloons()

if option == 'bots':
    st.subheader('This is a bot investing off WSB data')

    add_slider = st.sidebar.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0)
    )
    progress_bar = st.progress(0)
    status_text = st.empty()
    chart = st.line_chart(np.random.randn(10, 2))

    for i in range(100):
        # Update progress bar.
        progress_bar.progress(i + 1)

        new_rows = np.random.randn(10, 2)

        # Update status text.
        status_text.text(
            'The latest random number is: %s' % new_rows[-1, 1])

        # Append data to the chart.
        chart.add_rows(new_rows)

        # Pretend we're doing some computation that takes time.
        time.sleep(0.1)
    st.write("Yeet")
    status_text.text('Done!')
    st.balloons()
