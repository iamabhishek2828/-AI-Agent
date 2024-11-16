
# **AI Agent: An Intelligent Data Search and Summarization Tool**

## **Overview**

The **AI Agent** is a cutting-edge solution designed to assist in data search, summarization, and storage through seamless integration with modern technologies. Leveraging powerful APIs like **SerpApi**, **Google Generative Language API**, and **Firebase Firestore**, this project allows users to perform intelligent searches, summarize results, and store the findings in both **Google Sheets** and **Firebase Firestore**. Additionally, it provides features for uploading CSV files, performing entity-based searches, and fetching relevant news articles.
This project showcases the use of AI-driven tools to facilitate decision-making processes by summarizing web data, enhancing productivity, and simplifying information storage in a highly automated manner.
You can also try the deployed version of the app here: [Live Demo on Streamlit](https://abhishekchoudhary.streamlit.app/)

## **Features**

### 1. **Intelligent Web Search and Summarization**
   - Use **SerpApi** to conduct web searches based on user-defined queries.
   - Automatically generate summaries of search results using **Google's Generative Language API**, ensuring efficient content extraction.

### 2. **CSV Data Processing**
   - Upload and process CSV files containing entities for which data is to be searched.
   - Perform searches on these entities, retrieve relevant data, and generate summaries.

### 3. **Data Storage and Management**
   - Seamlessly store search results in **Firebase Firestore** for efficient data management.
   - Alternatively, store the results in **Google Sheets** for easy sharing and collaboration.

### 4. **User Authentication and Management**
   - In-built authentication system to manage users (with session management in memory).
   - Easily extendable for production use, such as integrating third-party authentication providers.

### 5. **News Fetching**
   - Fetch and display real-time news articles related to user queries, using the **News API**.

---

## **Technology Stack**

The AI Agent leverages an array of powerful technologies and APIs to deliver a seamless and efficient user experience:

- **Streamlit**: For developing the interactive web-based application, enabling fast, dynamic UI development.
- **SerpApi**: For web scraping and search results gathering, offering real-time web data.
- **Google Generative Language API**: For AI-powered content summarization, providing concise summaries of search results.
- **Firebase Firestore**: For real-time NoSQL database storage of search results and user data.
- **Google Sheets API**: For writing results directly to Google Sheets for collaborative and easy sharing.
- **News API**: To fetch the latest news articles related to the user’s query.
  
---

## **Getting Started**

### **Pre-requisites**

1. **Python 3.7+**
2. **Google Cloud Credentials** for accessing Google APIs (Firestore, Sheets API).
3. **Firebase Project Credentials** for Firestore access.

### **Setting Up the Environment**

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd ai-agent-project
   ```

2. **Install Dependencies**:
   
   Install required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:

   Create a `.env` file at the root of the project and add the following variables:

   ```bash
   SERPAPI_KEY=<your-serpapi-key>
   NEWS_API_KEY=<your-news-api-key>
   GOOGLE_APPLICATION_CREDENTIALS=<path-to-google-credentials-json>
   FIREBASE_CREDENTIALS_PATH=<path-to-firebase-credentials-json>
   ```

   Replace `<your-serpapi-key>`, `<your-news-api-key>`, and the paths with your actual API keys and credentials.

4. **Run the Application**:

   After setting up your environment variables, launch the application by running:

   ```bash
   streamlit run app.py
   ```

   This will start the application locally, accessible through your browser at `http://localhost:8501`.

---

## **How It Works**

### 1. **User Login/Sign-Up**:
   Upon launching the app, users are prompted to log in or sign up. The authentication system is extendable and can be customized for production environments.

### 2. **CSV File Upload**:
   Users can upload CSV files containing entities (e.g., company names, products, etc.) for which data will be searched.

### 3. **Search and Summarization**:
   After uploading the CSV, users define a search query. The app uses **SerpApi** to search the web and then summarizes the results using the **Google Generative Language API**.

### 4. **Storing Results**:
   Summarized results can be stored either in **Firebase Firestore** for easy querying or in **Google Sheets** for easy sharing.

### 5. **News Fetching**:
   In addition to web searches, the app allows users to retrieve related news articles in real-time based on their search queries.

---

## **Technological Highlights**

- **Real-Time Data Search**: Powered by SerpApi, this tool extracts up-to-date information from the web, giving users access to relevant, real-time data.
- **AI-Driven Summaries**: Leverages the Google Generative Language API to generate meaningful summaries of large volumes of web data, providing concise and actionable insights.
- **Flexible Data Storage**: Users can choose whether they prefer to store results in a **cloud-based database** (Firestore) or a **collaborative document** (Google Sheets).
- **Seamless User Experience**: The app offers a clean, user-friendly interface via **Streamlit**, making it easy for non-technical users to interact with advanced AI-driven tools.

---

## **Firebase Setup**

To enable Firebase integration:

1. Go to [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Set up Firebase Admin SDK, and generate a service account key (JSON).
3. Update the `.env` file with the path to your Firebase credentials file.

---

## **Contributing**

We welcome contributions to enhance the functionality and scalability of this project:

- **Fork the repository**.
- **Make changes** or add features (e.g., adding new data storage options or supporting additional APIs).
- **Submit a pull request**.

Feel free to create **issues** for bugs or feature requests, and we’ll prioritize them accordingly.

---

## **License**

This project is licensed under the **MIT License**, granting you the freedom to modify, distribute, and use the code as you wish.

---

## **Acknowledgments**

- **SerpApi** for providing an efficient web scraping API.
- **Google** for the powerful APIs like Generative Language API and Firestore.
- **Firebase** for providing real-time NoSQL database solutions.
- **Streamlit** for simplifying the development of web applications.
  
