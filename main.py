import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
import matplotlib.pyplot as plt

# 1. Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="🎬 Movie Review Sentiment Detector 🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for dark theme and color scheme
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
    }
    .stButton>button:hover {
        background-color: #104E8B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Title of the app
st.title("🎬 Movie Review Sentiment Detector 🍿")

# 4. Sidebar: Predefined Examples
st.sidebar.header("Example Reviews")
example_reviews = [
    "The movie was great!",
    "The movie was waste of time!",
    "Waste of money and time!"
]

review_choice = st.sidebar.selectbox("Choose an example review", example_reviews)
if st.sidebar.button("Use Example"):
    st.session_state['user_review'] = review_choice

# 5. About Section in Sidebar
st.sidebar.markdown("## About")
st.sidebar.markdown("""
    This app uses a pre-trained RNN model to classify movie reviews as **Positive** or **Negative**. 
    The model analyzes the words in the review and calculates a sentiment score that reflects the tone of the text.
""")

# 6. Display selected example in the main text area
if 'user_review' in st.session_state:
    user_review = st.text_area("Enter your review:", st.session_state['user_review'], height=150)
else:
    user_review = st.text_area("Enter your review:", height=150)

# 7. Load the pre-trained model with caching to improve performance
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('imdb_rnn_model_update.keras')

model = load_model()

# 8. For understanding the data, mapping words
word_index = tf.keras.datasets.imdb.get_word_index()
reverse_word_index = {value: key for (key, value) in word_index.items()}

# 9. Helper function to preprocess text
def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]  # Ensure consistent mapping
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review

# 10. Helper function to predict sentiment
def predict_sentiment(review):
    preprocessed_review = preprocess_text(review)
    prediction = model.predict(preprocessed_review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment, prediction[0][0]

# 11. Input Section
st.subheader("Input Your Movie Review")
st.markdown("Type or paste your movie review above and click **Analyze Sentiment**.")

# 12. Analyze Sentiment Button
if st.button("Analyze Sentiment"):
    if user_review.strip():
        with st.spinner("Analyzing sentiment..."):
            # Get sentiment prediction
            sentiment, score = predict_sentiment(user_review)
        
        # Display results
        st.markdown(f"### Sentiment: **{sentiment}**")
        st.markdown(f"### Confidence Score: **{score:.2f}**")
        
        # Sentiment Meter (Progress Bar)
        st.markdown("#### Sentiment Meter:")
        # Ensure the score is a native Python float between 0.0 and 1.0
        st.progress(float(score))
        
        # Brief Explanation
        explanation = (
            "The sentiment analysis model evaluates the words and phrases in your review to determine its overall sentiment. "
            "A confidence score closer to 1.0 indicates a stronger positive sentiment, while a score closer to 0.0 indicates a stronger negative sentiment."
        )
        st.markdown(f"#### Explanation:\n{explanation}")
    else:
        st.error("Please enter a review before analyzing sentiment.")
