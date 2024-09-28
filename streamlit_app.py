import streamlit as st
import google.generativeai as genai

# Page layout - wide mode to give more space
st.set_page_config(page_title="Netflix Movie Recommender", layout="wide")

# Header Section with styling
st.markdown("<h1 style='text-align: center; color: #FF6347;'>🍿 Netflix Thailand Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4682B4;'>Find your next favorite movie!</h3>", unsafe_allow_html=True)

# Capture Gemini API Key
st.sidebar.subheader("🔑 API Configuration")
gemini_api_key = st.sidebar.text_input("Gemini API Key: ", placeholder="Enter your API Key", type="password")

# Initialize model to None
model = None

# Agent description - specialized in Netflix Thailand movie recommendations
agent_description = """
You are an expert in recommending movies from Netflix Thailand. 
Your expertise includes knowing the latest and most popular movies, various genres, and their ratings. 
You can help users by recommending movies based on their preferences for genre, release year, and popularity. 
You are also familiar with movie trends and can provide personalized suggestions.

If the user asks about anything outside of movies, politely inform them that you do not have enough information to answer that, and kindly ask them to only inquire about movies.
"""

# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.sidebar.success("Gemini API Key successfully configured.")
        
        # Store agent expertise in session state
        st.session_state.agent_expertise = agent_description
        #st.info("Agent expertise successfully set.")
    except Exception as e:
        st.sidebar.error(f"An error occurred while setting up the Gemini model: {e}")

# Movie preferences section with better layout
st.subheader("🎬 Select your movie preferences")
col1, col2, col3 = st.columns([2, 1, 2])

# Movie genres with icon
with col1:
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Documentary']
    selected_genre = st.selectbox("Choose a genre", genres)

# Movie release years with icon
with col2:
    years = [str(year) for year in range(2000, 2024)]
    selected_year = st.selectbox("Choose a release year", years)

# Movie type with icon
with col3:
    movie_type = st.radio("Choose movie type", ['Latest', 'Popular'], index=0)

# Recommendation section
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🍿 Get Movie Recommendations")

# Movie recommendation generation with a centered button
if st.button("Recommend a movie"):
    user_input = f"Recommend a {movie_type.lower()} {selected_genre.lower()} movie from {selected_year}"
    if model:
        try:
            # Send the request to the model
            response = model.generate_content(f"{agent_description}\n\n{user_input}")
            bot_response = response.text
            st.markdown(f"<div style='padding:10px; background-color:#f0f0f0; border-radius:10px;'><strong>{bot_response}</strong></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.warning("Please configure your API key to start getting recommendations.")

# Chatbot for additional questions or recommendations with chat history
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("💬 Chat with the Movie Bot")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Initialize with an empty list

# Display previous chat history using st.chat_message
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_chat_input := st.chat_input("Ask me anything about movies or recommendations!"):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_chat_input))
    st.chat_message("user").markdown(user_chat_input)
    
    # Use Gemini AI to generate a bot response
    if model:
        try:
            response = model.generate_content(f"{agent_description}\n\n{user_chat_input}")
            bot_response = response.text
            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.warning("Please configure your API key to start chatting.")
