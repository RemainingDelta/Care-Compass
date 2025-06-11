# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🧭"
    )


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠"
    )

#### ------------------------ Examples for Role of Resident ------------------------
def ResidentHomeNav():
    st.sidebar.page_link(
        "pages/00_Resident_Home.py", label="Resident Home", icon="🏠"
    )


def CustomizeMoveNav():
    st.sidebar.page_link(
        "pages/01_Customize_Move.py", label="Customize Your Move", icon="✈️"
    )


def CountryProfNav():
    st.sidebar.page_link("pages/02_Country_Profile.py", label="Country Profile", icon="🗺️"
    )


## ------------------------ Examples for Role of Student ------------------------
def StudentHomeNav():
    st.sidebar.page_link("pages/10_Student_Home.py", label="Student Home", icon="📚"
    )


def CountryComparatorNav():
    st.sidebar.page_link(
        "pages/11_Country_Comparator.py", label="Country Comparator", icon="📊"
    )


def SuggestedArticlesNav():
    st.sidebar.page_link(
        "pages/12_Suggested_Articles.py", label="Suggested Articles", icon="➕"
    )



#### ------------------------ Policymaker Role ------------------------
def PolicymakerHomeNav():
    st.sidebar.page_link("pages/20_Policymaker_Home.py", label="Policymaker Home", icon="👤")
    

def FeatOverTimeNav():
    st.sidebar.page_link("pages/21_Features_Over_Time.py", label="Features Over Time", icon="📈")


def TargetScoresNav():
    st.sidebar.page_link("pages/22_Target_Scores.py", label="Target Scores", icon="🎯")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "resident":
            ResidentHomeNav()
            CustomizeMoveNav()
            CountryProfNav()
                

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "student":
            StudentHomeNav()
            CountryComparatorNav()
            SuggestedArticlesNav()
            CountryProfNav()


        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "policymaker":
            PolicymakerHomeNav()
            FeatOverTimeNav()
            TargetScoresNav()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    # Always show a logout button if there is a logged in user
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")