import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "Dashboard/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
change_policy = st.Page("TinyMDM/change_policy.py", title="Change Policy", icon=":material/bug_report:")
technikzuordnung = st.Page(
    "Jira_Assets/technikzuordnung.py", title="Technikzuordnung", icon=":material/notification_important:"
)

#search = st.Page("tools/search.py", title="Search", icon=":material/search:")
#history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "TinyMDM": [change_policy],
            "Jira Assetmanagement": [technikzuordnung],
            "Account": [logout_page]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()