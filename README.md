# README: AI Chatbot Application with Python Django, Google Gemini API, and RAG

## Introduction
This project involves the development of an AI-powered chatbot application using Django, Google Gemini API for generating responses, and Retrieval-Augmented Generation (RAG) with embeddings generated by `sentence-transformers/all-MiniLM-L6-v2`. The chatbot provides personalized responses by retrieving relevant information from user-provided documents and generating context-aware answers.

## Features
1. **Generative AI with Google Gemini**: Utilizes Google Gemini API to generate conversational responses.
2. **RAG-based Information Retrieval**: Implements Retrieval-Augmented Generation using embeddings created by `sentence-transformers/all-MiniLM-L6-v2` to enhance response relevance.
3. **Document Upload via Dashboard**: Users can upload documents for RAG processing through a web-based dashboard.
4. **Real-Time Chat Interface**: Provides an interactive chat interface for users.

## Installation Guide

### Prerequisites
- Python 3.12 or higher
- Django framework
- PostgreSQL database with `pgvector` extension enabled
- Google Gemini API key

### Steps to Install

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Django Project**
   - Create a `.env` file in the root directory and add the following:
     ```
     GENERATIVE_AI_KEY=your_google_gemini_api_key_here
     DATABASE_URL=postgres://user:password@localhost:5432/your_database_name
     ```
   - Ensure `pgvector` extension is enabled in your PostgreSQL database:
     ```sql
     CREATE EXTENSION IF NOT EXISTS vector;
     ```

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

## Usage Guide

### Uploading Documents for RAG
1. Navigate to the dashboard.
2. Enter the URL of the document you want to upload.
3. Click the "Upload" button. The document will be processed, and embeddings will be generated using `sentence-transformers/all-MiniLM-L6-v2`.

### Chatting with the AI Chatbot
1. Access the chat interface.
2. Type your query in the input box and press Enter.
3. The chatbot will retrieve relevant information from the uploaded documents and generate a response using Google Gemini API.

## Key Components

### 1. Google Gemini API Integration
   The chatbot uses the Google Gemini API to generate responses based on the context provided by RAG. The API key is securely stored in an environment variable and accessed in the Django settings.

### 2. RAG with `sentence-transformers/all-MiniLM-L6-v2`
   - Embeddings are created using `sentence-transformers/all-MiniLM-L6-v2`.
   - Relevant document chunks are retrieved using cosine similarity.

### 3. PostgreSQL and `pgvector`
   - The `pgvector` extension is used for efficient vector similarity search.
   - Embeddings are stored as vector data in PostgreSQL.

## Environment Variables
- `GENERATIVE_AI_KEY`: Your Google Gemini API key.
- `DATABASE_URL`: Connection string for the PostgreSQL database.

## Requirements
The project dependencies are listed in `requirements.txt`. Key packages include:
- `Django`
- `psycopg2-binary`
- `sentence-transformers`
- `google-generativeai`

## Future Improvements
1. **Enhanced Document Management**: Add features for document deletion and editing.
2. **Improved UI/UX**: Enhance the chat interface for better user experience.
3. **Scalability**: Implement caching and load balancing for handling a larger number of users.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request.


## Contact
For questions or support, please contact [estopangaribuan@gmail.com].

