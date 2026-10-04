# AI-Driven Pharmaceutical Complaint Management Platform

An AI-powered full-stack application for managing pharmaceutical customer complaints.

The system converts unstructured complaint information from text, PDF, DOCX, TXT, and EML files into structured complaint records and assists users with complaint classification, completeness checking, AI-assisted risk assessment, summarization, and possible duplicate detection.


## 🔗 Project Links

- **Frontend Demo:** https://gongatinaresh.github.io/Ai-pharmaceutical-complaint-management-platform/
- **GitHub Repository:** https://github.com/gongatinaresh/Ai-pharmaceutical-complaint-management-platform

> **Note:** The GitHub Pages link demonstrates the deployed frontend interface. The complete AI workflow requires the FastAPI backend, PostgreSQL database, and Groq API configuration.

---

## 🚀 Project Overview

In pharmaceutical manufacturing, customer complaints may arrive through emails, documents, or unstructured text.

Manually reading these complaints, identifying important information, entering it into a complaint form, checking for missing information, assessing initial risk, and reviewing previous complaints can be time-consuming.

This project provides an **AI-assisted complaint intake and triage workflow** that helps transform unstructured complaint information into structured complaint records.

A user can:

1. Paste complaint text or upload a complaint document.
2. Extract relevant complaint information using AI.
3. Automatically populate the complaint form.
4. Check whether important information is missing.
5. Classify the complaint.
6. Generate an AI-assisted risk assessment.
7. Generate a complaint summary.
8. Check for possible duplicate complaints.
9. Review the AI-generated information.
10. Save the complaint to PostgreSQL.

> **Important:** The AI provides assistance and recommendations. Final quality and regulatory decisions remain with the responsible human reviewer.

---

# ✨ Key Features

## 🤖 AI-Powered Complaint Extraction

The system extracts structured information from unstructured complaint text.

Extracted fields include:

- Complaint source
- Customer name
- Product name
- Product strength/grade
- Batch number
- Manufacturing date
- Expiry date
- Quantity affected
- Complaint type
- Complaint date
- Detailed complaint description
- Initial severity
- Priority

The extracted information is automatically populated into the complaint form for user review.

---

## 📋 Complaint Completeness Checking

The AI workflow checks the extracted complaint information for missing fields.

The system is designed to avoid inventing unavailable information and identifies fields that require additional user input.

This helps users identify incomplete complaint information before saving the record.

---

## 🏷️ Complaint Classification

The AI analyzes the complaint information and determines an appropriate complaint category based on the available information.

This supports the initial triage process and helps organize complaints for further review.

---

## ⚠️ AI-Assisted Risk Assessment

The system generates an initial AI-assisted assessment containing:

- Risk level
- Severity
- Priority
- Assessment reason
- Complaint category

The assessment is intended to support human review and does not replace the decision-making responsibility of a quality professional.

---

## 🔎 Duplicate Complaint Detection

The system checks existing complaint records for matching product and batch information.

When a possible match is found, the system flags the complaint for human review.

> The current implementation uses product and batch information to identify possible duplicates. It does not claim semantic or embedding-based duplicate detection.

---

## 📝 Complaint Summary

The AI generates a concise summary of the complaint so users can quickly understand the reported issue without reviewing the entire original complaint text.

---

## 📄 Multi-Format Complaint Input

The system supports:

- PDF
- DOCX
- TXT
- EML
- Directly pasted complaint text

Maximum uploaded file size:

**10 MB**

The application extracts text from supported documents before sending the complaint through the AI workflow.

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Redux
- JavaScript
- HTML5
- CSS3
- Vite

## Backend

- Python
- FastAPI
- REST APIs
- SQLAlchemy

## AI / Generative AI

- LangGraph
- Groq
- LLM-based information extraction
- Prompt Engineering
- AI-assisted classification
- AI-assisted risk assessment

## Database

- PostgreSQL

## Document Processing

- PyMuPDF
- python-docx
- Python email processing
- TXT processing

## Development & Deployment Tools

- Git
- GitHub
- VS Code
- Docker
- GitHub Pages

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                    Paste Text / Upload File
                               │
                               ▼
                    ┌──────────────────────┐
                    │     React + Redux    │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                         REST API Calls
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                      Document Extraction
                               │
                               ▼
                    ┌──────────────────────┐
                    │      LangGraph       │
                    │    AI Workflow       │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        Extraction       Classification    Risk Assessment
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         Groq LLM
                               │
                               ▼
                    Structured AI Result
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Redux Store      │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
             Complaint Form        AI Assessment
                    │
                    ▼
               Human Review
                    │
                    ▼
             ┌───────────────┐
             │  PostgreSQL   │
             └───────────────┘

🔄 AI Workflow
The complaint processing workflow is orchestrated using LangGraph.

Complaint Text / Document
          │
          ▼
   Text Extraction
          │
          ▼
  Complaint Extraction
          │
          ▼
Completeness Checking
          │
          ▼
     Classification
          │
          ▼
    Risk Assessment
          │
          ▼
      Summarization
          │
          ▼
  Duplicate Detection
          │
          ▼
   Structured AI Result
          │
          ▼
      Human Review
          │
          ▼
     Save to Database

LangGraph Workflow Nodes
The AI workflow contains the following processing stages:
1. Complaint Extraction
2. Completeness Checking
3. Complaint Classification
4. Risk Assessment
5. Complaint Summarization
6. Duplicate Detection
Groq provides the LLM capabilities used by the AI workflow, while LangGraph manages the sequence and state of the processing steps.

🔌 API Endpoints
Health Check
GET /api/health

Returns the health status of the backend.
AI Complaint Processing
POST /api/ai/process

Processes directly submitted complaint text through the LangGraph AI workflow.
Example request
{
  "complaint_text": "Customer reported damaged packaging for Paracetamol 500 mg from batch PCM24015."
}

Complaint Document Upload
POST /api/upload/complaint

Accepts supported complaint documents:
- PDF
- DOCX
- TXT
- EML
The endpoint extracts the document text and sends it through the AI complaint workflow.
Complaint Management
Create Complaint
POST /api/complaints/

Get All Complaints
GET /api/complaints/

Get Complaint
GET /api/complaints/{complaint_id}

Update Complaint
PUT /api/complaints/{complaint_id}

Delete Complaint
DELETE /api/complaints/{complaint_id}

📁 Project Structure
ai-pharmaceutical-complaint-management-platform/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── graph.py
│   │   │   ├── nodes.py
│   │   │   ├── prompts.py
│   │   │   └── state.py
│   │   │
│   │   ├── api/
│   │   │   ├── ai.py
│   │   │   ├── complaints.py
│   │   │   └── upload.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   └── complaint.py
│   │   │
│   │   ├── schemas/
│   │   │   └── complaint.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   └── groq_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env.example
│   ├── compose.yaml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── store/
│   │   │   ├── complaintSlice.js
│   │   │   └── store.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── complaint-dashboard.png
│
├── .gitignore
└── README.md

🖥️ Application Workflow
1. User opens the complaint management interface
                    ↓
2. User enters complaint text or uploads a document
                    ↓
3. FastAPI receives the request
                    ↓
4. Document text is extracted when required
                    ↓
5. LangGraph starts the AI workflow
                    ↓
6. Complaint information is extracted
                    ↓
7. Missing information is identified
                    ↓
8. Complaint is classified
                    ↓
9. Initial risk assessment is generated
                    ↓
10. Complaint summary is generated
                    ↓
11. Possible duplicates are checked
                    ↓
12. AI results are returned to React
                    ↓
13. Redux updates the complaint state
                    ↓
14. Complaint form is automatically populated
                    ↓
15. User reviews the AI-generated information
                    ↓
16. Complaint is saved to PostgreSQL

🖼️ Application Preview
Add a screenshot of the working application to:
docs/complaint-dashboard.png

Then display it here:
![AI Complaint Management Dashboard](docs/complaint-dashboard.png)

⚙️ Local Setup
Prerequisites
Make sure the following are installed:
- Python 3.10+
- Node.js
- npm
- Docker Desktop
- Git
- PostgreSQL through Docker
1. Clone the Repository
git clone https://github.com/gongatinaresh/Ai-pharmaceutical-complaint-management-platform.git

cd Ai-pharmaceutical-complaint-management-platform

🐍 Backend Setup
2. Navigate to Backend
cd backend

3. Create Virtual Environment
Windows:
python -m venv .venv

Activate:
.venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

🗄️ PostgreSQL Setup
5. Start PostgreSQL Using Docker
From the backend directory:
docker compose up -d

Check the container:
docker compose ps

The PostgreSQL database is configured through the Docker Compose file.
🔑 Environment Configuration
6. Create .env
Create:
backend/.env

Add:
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

Never commit your actual .env file or API key to GitHub.

A sample configuration is provided in:
backend/.env.example

🚀 Run the Backend
From the backend directory:
uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

⚛️ Frontend Setup
Open another terminal.
Navigate to:
cd frontend

Install dependencies:
npm install

Start the development server:
npm run dev

Frontend:
http://localhost:5173

🔐 Security
The project follows basic security practices for local development:
- API keys are stored in environment variables.
- .env files are excluded from Git.
- .env.example is provided without secrets.
- AI-generated assessments are presented as recommendations.
- Final quality and regulatory decisions remain with human reviewers.

🧪 Testing the Application
The application can be tested using:
Text Input
Paste a realistic customer complaint into the AI assistant.
PDF
Upload a text-based PDF complaint.
DOCX
Upload a Microsoft Word complaint document.
TXT
Upload a plain-text complaint.
EML
Upload an email complaint file.

The expected workflow is:
Input
  ↓
Text Extraction
  ↓
AI Processing
  ↓
Structured Data
  ↓
Form Population
  ↓
AI Risk Assessment
  ↓
Human Review
  ↓
Database Save

🧠 Design Decisions
Why React?
React provides a component-based frontend for building the complaint management interface.
Why Redux?
Redux provides centralized state management for complaint form data and AI-generated results.
Why FastAPI?
FastAPI provides lightweight Python REST APIs and integrates naturally with the AI processing layer.
Why LangGraph?
LangGraph is used to organize the complaint-processing steps into a structured AI workflow.
Why Groq?
Groq provides access to the LLM used for complaint extraction, classification, risk assessment, and summarization.
Why PostgreSQL?
PostgreSQL provides persistent relational storage for structured complaint records.
Why Docker?
Docker provides a consistent local PostgreSQL environment without requiring a separate PostgreSQL installation.

⚠️ Current Limitations
This project is a portfolio/internship demonstration and is not intended to be used as a production pharmaceutical quality management system.
Current limitations include:
- No production authentication or role-based access control
- No audit trail
- No production OCR for scanned documents
- Duplicate detection currently relies on matching product and batch information
- AI assessments require human review
- Backend and database require local/cloud deployment for public live usage
- No production monitoring or observability

🚀 Future Improvements
Potential future improvements include:
- Root Cause Recommendation
- CAPA Recommendation
- Semantic duplicate detection using embeddings
- OCR support for scanned complaint documents
- Authentication and role-based access control
- Audit logging
- Automated unit and integration testing
- Production cloud deployment
- Enhanced pharmaceutical quality workflows
- Monitoring and observability
- Improved validation and error handling

📌 Project Highlights
This project demonstrates practical experience with:
- Full-stack web application development
- AI/LLM application development
- LangGraph workflow orchestration
- Groq LLM integration
- REST API development
- React and Redux state management
- PostgreSQL database integration
- Document processing
- AI-assisted information extraction
- AI-assisted risk assessment
- Computer-to-AI-to-database workflow design


👨‍💻 Author
Gongati Naresh
- GitHub: https://github.com/gongatinaresh
- LinkedIn: https://www.linkedin.com/in/gongati-naresh-33b172334
