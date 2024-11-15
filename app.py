import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import time

# Load environment variables
load_dotenv()

# Retrieve credentials paths from .env file
serpapi_key = os.getenv("SERPAPI_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
firebase_credentials_path = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "C:/Users/AADI/OneDrive/Desktop/New folder (5)/AI_Agent_Project/ai-agent-39362-firebase-adminsdk-kcec2-c8d52150c8.json"
)

# Set up Google service account with correct scope for Generative Language API
google_credentials_path = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "C:/Users/AADI/OneDrive/Desktop/New folder (5)/AI_Agent_Project/mythic-reach-441020-s1-cd2ec16edee7.json"

)
SCOPE = "https://www.googleapis.com/auth/generative-language"
google_credentials = service_account.Credentials.from_service_account_file(
    google_credentials_path, scopes=[SCOPE]
)

# Refresh credentials to obtain access token
google_credentials.refresh(Request())
access_token = google_credentials.token

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    firebase_credentials = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(firebase_credentials)
else:
    st.warning("Firebase app is already initialized.")

# Initialize Firestore
db = firestore.client()

# In-memory "user database" for demonstration
user_db = {"admin@example.com": "password"}  # Use email as the key

# Function to search for query using SerpApi
def search_query(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": serpapi_key
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: Unable to fetch results from SerpApi. Details: {response.text}")
        return "Error fetching results."

    data = response.json()
    return data.get("organic_results", [{}])[0].get("link", "No result found")

# Function to process text with Google Generative Language API
def process_with_gemini(text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": text
            }]
        }]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        content = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No summary available.")
        return content if content else "No summary available."
    else:
        return f"Error: {response.status_code}. Details: {response.text}"

# Function to write results to Firebase Firestore
def write_to_firestore(results_df):
    try:
        collection_ref = db.collection('search_results')
        for _, row in results_df.iterrows():
            collection_ref.add({
                "Entity": row["Entity"],
                "Query": row["Query"],
                "Result": row["Result"],
                "Summarized Result": row["Summarized Result"]
            })
        st.success("Results successfully written to Firebase Firestore.")
    except Exception as e:
        st.error(f"Failed to write data to Firebase Firestore: {e}")

# Function to write results to Google Sheets
def write_to_google_sheets(results_df, google_sheets_id, google_sheets_range):
    try:
        service = build('sheets', 'v4', credentials=google_credentials)
        sheet = service.spreadsheets()

        values = results_df.values.tolist()
        body = {'values': values}

        sheet.values().update(
            spreadsheetId=google_sheets_id,
            range=google_sheets_range,
            valueInputOption="RAW",
            body=body
        ).execute()
        st.success(f"Results successfully written to Google Sheets (Range: {google_sheets_range}).")
    except HttpError as err:
        st.error(f"Failed to write data to Google Sheets: {err}")

def fetch_news(query):
    if not news_api_key:
        return "API Key not found. Please ensure the NEWS_API_KEY is set in your environment."
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": news_api_key,
        "pageSize": 15,  # Increased to fetch more articles
        "sortBy": "relevance",  # Sort by relevance
        "language": "en"  # Specify language
    }
    
    # Retry logic with delay for rate-limiting errors
    for attempt in range(5):  # Retry up to 5 times
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if not articles:
                return "No news found for your query."
            news_list = [{"title": article["title"], "description": article["description"], "url": article["url"]} for article in articles]
            return news_list
        elif response.status_code == 426:  # Rate limit exceeded
            time.sleep(30)  # Wait for 30 seconds before retrying
        else:
            return f"Error fetching news: {response.status_code}"

    return "Failed to fetch news after multiple attempts."

def display_news(news_list):
    if isinstance(news_list, list) and news_list:
        for idx, article in enumerate(news_list):
            st.write(f"**{idx + 1}. {article['title']}**")
            st.write(f"{article['description']}")
            st.write(f"[Read more]({article['url']})")
    else:
        st.error(news_list)  # This will show errors or no articles message

# Function for login/signup
def login_signup():
    """Login and Signup mechanism with persistent session state."""
    if "user_db" not in st.session_state:
        st.session_state.user_db = {"test_user@example.com": "password123"}  # Store email as key

    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = False
        st.session_state["current_user"] = None

    auth_action = st.radio("Select Action", ("Login", "Sign Up"))

    if auth_action == "Login":
        st.title("Login")
        email = st.text_input("Email").strip()
        password = st.text_input("Password", type="password").strip()

        if st.button("Login"):
            if email in st.session_state.user_db:
                if st.session_state.user_db[email] == password:
                    st.session_state["authentication_status"] = True
                    st.session_state["current_user"] = email
                    st.success("Logged in successfully!")
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.error("Email not found. Please sign up first or check for typos.")

    elif auth_action == "Sign Up":
        st.title("Sign Up")
        new_email = st.text_input("New Email").strip()
        new_password = st.text_input("New Password", type="password").strip()

        if st.button("Sign Up"):
            if new_email in st.session_state.user_db:
                st.warning("Email already exists. Please choose a different one.")
            elif new_email and new_password:
                st.session_state.user_db[new_email] = new_password
                st.success("Account created successfully! You can now log in.")
            else:
                st.error("Email and password cannot be empty.")

# Main app structure
def main():
    # Only display login page if not authenticated
    if not st.session_state.get("authentication_status", False):
        login_signup()
        return  # Stop here if user is not authenticated

    # Display AI Agent functionality after login
    st.title("AI Search Agent")
    st.write("Upload a CSV file, define a query to retrieve information for each entity, and extract data.")

    # Step 1: File Upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Step 2: Google Sheets ID and Range Input
    google_sheets_id = st.text_input("Enter Google Sheets ID (if applicable)")
    google_sheets_range = st.text_input("Enter the range for Google Sheets (e.g., 'Sheet1!A1:B10')")

    if uploaded_file is not None:
        # Step 3: Load CSV and display columns
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.write(data.head())

        # Step 4: Choose Column for Entity Names
        column = st.selectbox("Select the primary column for entities", data.columns)

        # Step 5: Define Query
        query = st.text_area("Enter query", "Please input a query to search for entities.")

        # Button to Execute Search and Summarization
        if st.button("Search and Summarize"):
            result_data = []
            for _, row in data.iterrows():
                entity_name = row[column]
                result_link = search_query(query)
                summarized_result = process_with_gemini(result_link)
                result_data.append({"Entity": entity_name, "Query": query, "Result": result_link, "Summarized Result": summarized_result})

            # Convert results to DataFrame
            result_df = pd.DataFrame(result_data)

            # Display results
            st.write("Search and Summarization Results:")
            st.write(result_df)

            # Step 6: Write to Firestore or Google Sheets
            write_to_firestore(result_df)
            if google_sheets_id and google_sheets_range:
                write_to_google_sheets(result_df, google_sheets_id, google_sheets_range)

    # Fetch and display related news
    news_query = st.text_input("Enter query for related news")
    if news_query:
        news_list = fetch_news(news_query)
        display_news(news_list)

if __name__ == "__main__":
    main()
