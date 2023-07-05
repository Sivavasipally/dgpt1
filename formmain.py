#import openai
import streamlit as st
#from streamlit_chat import message

# Setting page title and header
st.set_page_config(page_title="DCHAT", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>DGPT</h1>", unsafe_allow_html=True)

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    # Results Can be either form or outside
    if submit_button:
        st.success("user_input is {}".format(user_input))
        st.write(user_input.upper())
