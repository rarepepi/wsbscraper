import asyncio
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from wsb import get_data_frame

sidebar = {
    "wallstreetbets": "r/WallStreetBets",
    "investing": "r/Investing"
}
st.sidebar.title("Control Panel")
option = st.sidebar.selectbox(
    'Which Dashboard',
    list(sidebar.keys()),
    format_func=sidebar.get
)
st.title(option)

# @st.cache
async def watch(test):
    articles_df, comments_df = await get_data_frame()
    return (articles_df, comments_df)

test = st.empty()

if option == 'wallstreetbets':
    # st.subheader('This is a scraper for WSB')

    # Sidebar
    kinds = st.sidebar.multiselect('Multiselect', ['new', 'hot', 'top'])

    # Content
    articles_df = None
    comments_df = None

    st.spinner()
    if st.button("Run"):
        with st.spinner(text='In progress'):
            tic = time.perf_counter()
            articles_df, comments_df = asyncio.run(watch(test))
            st.success('Done')
            st.balloons()
            st.dataframe(articles_df)
            st.dataframe(comments_df)
            toc = time.perf_counter()
            st.write(f"Scraped {articles_df.size} articles, or {comments_df.size} total comments :D")
            st.write(f"Comments a second: {comments_df.size/(toc - tic)}")


async def watch2():
    pass
if option == 'investing':
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

if option == 'test':
    st.button('Hit me')
    st.checkbox('Check me out')
    st.radio('Radio', [1,2,3])
    st.selectbox('Select', [1,2,3])
    st.multiselect('Multiselect', [1,2,3])
    st.slider('Slide me', min_value=0, max_value=10)
    st.select_slider('Slide to select', options=[1,'2'])
    st.text_input('Enter some text')
    st.number_input('Enter a number')
    st.text_area('Area for textual entry')
    st.date_input('Date input')
    st.time_input('Time entry')
    st.file_uploader('File uploader')
    st.color_picker('Pick a color')
