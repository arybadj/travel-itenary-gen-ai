# Import required libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Validate API Key
if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file. Please check your configuration.")
    st.stop()

# Configure the Gemini API
genai.configure(api_key=api_key)

# Function: Get response from image input
def get_response_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

# Function: Get response from text input
def get_response(prompt, input_text):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt, input_text])
    return response.text

# Function: Prepare image for Gemini
def prep_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File is uploaded!")

# Streamlit UI Setup
st.image('logo.jpg', width=70)
st.header("Planner: Discover and Plan your Culinary Adventures!")

# Radio menu for sections
section_choice = st.radio("Choose Section:", (
    "Location Finder", "Trip Planner", "Weather Forecasting", "Restaurant & Hotel Planner"
))

# ----------------------------- LOCATION FINDER -----------------------------
if section_choice == "Location Finder":
    upload_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    image = ""
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    input_prompt_loc = """
    You are an expert Tourist Guide. Your job is to provide:
    - A summary about the place shown in the image
    - The name of the place
    - State and Capital
    - Coordinates
    - Popular nearby destinations
    Return the response using markdown.
    """

    if st.button("Get Location!"):
        try:
            image_data = prep_image(upload_file)
            response = get_response_image(image_data, input_prompt_loc)
            st.subheader("Tour Bot:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {e}")

# ----------------------------- TRIP PLANNER -----------------------------
elif section_choice == "Trip Planner":
    input_prompt_planner = """
    You are an expert Tour Planner. Based on the location and number of days (if mentioned),
    - Suggest a complete travel itinerary
    - Include hidden gems, must-see places, hotels, and tips
    - Mention the best month to visit
    Return the response using markdown.
    """
    input_plan = st.text_area("Enter location and number of days for planning:")
    if st.button("Plan my Trip!"):
        try:
            response = get_response(input_prompt_planner, input_plan)
            st.subheader("Planner Bot:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {e}")

# ----------------------------- WEATHER FORECAST -----------------------------
elif section_choice == "Weather Forecasting":
    input_prompt_weather = """
    You are an expert weather forecaster. Provide a 7-day weather forecast from today for the given place:
    - Include Precipitation, Humidity, Wind, Air Quality, and Cloud Cover
    Return the response using markdown.
    """
    input_location = st.text_area("Enter location to forecast weather:")
    if st.button("Forecast Weather!"):
        try:
            response = get_response(input_prompt_weather, input_location)
            st.subheader("Weather Bot:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {e}")

# ----------------------------- HOTEL & RESTAURANT -----------------------------
elif section_choice == "Restaurant & Hotel Planner":
    input_prompt_accommodation = """
    You are an expert Restaurant & Hotel Planner. For the given place:
    - List Top 5 mid-range restaurants (with address, average cost per meal, and rating)
    - List Top 5 mid-range hotels (with address, average cost per night, and rating)
    Return the response using markdown.
    """
    input_location = st.text_area("Enter location to find Restaurants & Hotels:")
    if st.button("Find Restaurant & Hotel!"):
        try:
            response = get_response(input_prompt_accommodation, input_location)
            st.subheader("Accommodation Bot:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {e}")
