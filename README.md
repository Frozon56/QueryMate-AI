# QueryMate AI

AI-powered multilingual document assistant built using Streamlit, Ollama, and Qwen2.5. QueryMate enables users to upload documents, ask questions in multiple languages, and receive intelligent responses through both text and voice.

## Features

* Upload and analyze PDF documents
* Ask questions directly from document content
* Multilingual support:

  * English
  * Hindi
  * Marathi
* Speech-to-Text for voice queries
* Text-to-Speech for voice responses
* Secure user authentication
* Query history tracking using SQLite
* Offline AI processing with Ollama
* Fast and lightweight local deployment

## Technologies Used

### Frontend

* Streamlit
* HTML
* CSS

### Backend

* Python

### AI & NLP

* Ollama
* Qwen2.5 (1.5B)
* SpeechRecognition
* pyttsx3

### Database

* SQLite

### Document Processing

* PyPDF2

## System Architecture

![Architecture](assets/architecture.png)

### Workflow

1. User uploads a PDF document
2. Text is extracted from the document
3. User asks a question using text or voice
4. Query is processed by Qwen2.5 through Ollama
5. AI generates an answer based on document content
6. Response is displayed and can be read aloud
7. Query and response are stored in history

## Application Screenshots

### Login Page

![Login](assets/screenshots/login.png)

### Dashboard

![Dashboard](assets/screenshots/dashboard.png)

### Upload PDF

![Upload PDF](assets/screenshots/upload.png)

### Ask Query

![Ask Query](assets/screenshots/query.png)

### Query History

![History](assets/screenshots/history.png)

## Installation

Clone the repository:

```bash
git clone https://github.com/Frozon56/QueryMate-AI.git
cd QueryMate-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install and run Ollama:

```bash
ollama run qwen2.5:1.5b
```

Start the application:

```bash
streamlit run app.py
```

## Future Enhancements

* Support for DOCX, PPTX, and TXT files
* Advanced RAG (Retrieval-Augmented Generation)
* Document summarization
* Cloud deployment
* User profile management
* OCR support for scanned PDFs

## Author

**Pranjali Tanaji Jadhav**

Final Year B.Tech Computer Science and Engineering

## License

This project is developed for educational and research purposes.
