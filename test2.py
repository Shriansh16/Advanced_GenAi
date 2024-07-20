import streamlit as st

# Function to display the main page
def main_page():
    st.title("Main Page")
    st.write("Welcome to the main page")
    if st.button("Go to Page 1"):
        st.experimental_set_query_params(page="page1")
    if st.button("Go to Page 2"):
        st.experimental_set_query_params(page="page2")

# Function to display Page 1
def page1():
    st.title("Page 1")
    st.write("Welcome to Page 1")
    if st.button("Go to Main Page"):
        st.experimental_set_query_params(page="main")
    if st.button("Go to Page 2"):
        st.experimental_set_query_params(page="page2")

# Function to display Page 2
def page2():
    st.title("Page 2")
    st.write("Welcome to Page 2")
    if st.button("Go to Main Page"):
        st.experimental_set_query_params(page="main")
    if st.button("Go to Page 1"):
        st.experimental_set_query_params(page="page1")

# Main function to control the navigation
def main():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    if page == "main":
        main_page()
    elif page == "page1":
        page1()
    elif page == "page2":
        page2()

if __name__ == "__main__":
    main()