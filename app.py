import streamlit as st

st.title('title of your application')
st.markdown('for example here is a **bold text**')

st.sidebar.title('title of the sidebar')

agree = st.checkbox('I agree')

if agree:
    st.write('Great!')

side_check = st.sidebar.checkbox('Click me!')

if side_check:
    st.sidebar.write('Side bar has been clicked.')