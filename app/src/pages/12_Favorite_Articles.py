import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.style import style_sidebar, set_background

style_sidebar()
SideBarLinks()

st.title("FAVORITE HEALTHCARE ARTICLES")

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("You must be logged in to access this page.")
    st.stop()

# Get user ID
userID = st.session_state.get("user_id")

if not userID:
    st.error("Could not find user ID in session. Please log in again.")
    st.stop()

# API endpoint
fav_articles_URL = f"http://host.docker.internal:4000/country/articles/favorite?userID={userID}"

try:
    # Fetch Articles details
    response = requests.get(fav_articles_URL, timeout=10)
    
    if response.status_code == 200:
        favorites = response.json()
        
        if not favorites:
            st.info("You haven't favorited any articles yet.")
            st.write("Browse the country pages to find and favorite articles!")
        else:
            st.success(f"You have {len(favorites)} favorite articles:")
            
            # Display articles in a 3-column grid
            for idx in range(0, len(favorites), 3):
                cols = st.columns(3)
                
                for col_idx in range(3):
                    if idx + col_idx < len(favorites):
                        article = favorites[idx + col_idx]
                        
                        with cols[col_idx]:
                            # Create a container for each article
                            with st.container(border=True):
                                # Display thumbnail from database
                                image_name = article.get('image_name', 'Book-Blue.png')  # Default image if none specified
                                st.image(f"assets/{image_name}", use_container_width=True)
                                
                                # Article title
                                st.markdown(f"**{article.get('article_title', 'No Title')}**")
                                
                                # Source
                                st.markdown(f"*{article.get('source', 'Unknown Source')}*")
                                
                                # Country code (if you want to show it)
                                if article.get('country_code'):
                                    st.caption(f"Country: {article['country_code']}")
                                
                                # Read more link
                                if article.get('article_link'):
                                    st.markdown(f"[Read article →]({article['article_link']})")
                                
                                # Unfavorite button - use index to make key unique
                                if st.button(
                                    "Remove from Favorites", 
                                    key=f"remove_{article['id']}_{idx + col_idx}",
                                    type="secondary",
                                    use_container_width=True
                                ):
                                    # Call unfavorite API
                                    unfav_url = f"http://host.docker.internal:4000/country/articles/favorite/{article['id']}?userID={userID}"
                                    unfav_response = requests.delete(unfav_url)
                                    
                                    if unfav_response.status_code == 200:
                                        st.success("Article removed from favorites!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to remove article from favorites")
                                
                                # Add spacing between articles
                                st.divider()
                                
    else:
        st.error(f"Error fetching favorites: Status {response.status_code}")
        
except Exception as e:
    st.error(f"Error connecting to the API: {str(e)}")