# AI-Driven Pharmaceutical Complaint Management Platform

An AI-powered full-stack application for managing pharmaceutical customer complaints.

The system converts unstructured complaint information from text, PDF, DOCX, TXT, and EML files into structured complaint records and assists users with complaint classification, completeness checking, risk assessment, summarization, and possible duplicate detection.

## 🔗 Live Demo & Project Links

- **Live Demo:**  https://gongatinaresh.github.io/Ai-pharmaceutical-complaint-management-platform/
- **GitHub Repository:** https://github.com/gongatinaresh/Ai-pharmaceutical-complaint-management-platform
- **Demo Video:** https://YOUR-DEMO-VIDEO-LINK
## 🚀 Project Overview

In pharmaceutical manufacturing, customer complaints may arrive through emails, documents, or unstructured text.

Manually reading these complaints, identifying important information, entering it into a complaint form, checking for missing information, assessing initial risk, and reviewing previous complaints can be time-consuming.

This project provides an **AI-assisted complaint intake and triage workflow**.

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

## ✨ Key Features

### 🤖 AI-Powered Complaint Extraction

Extracts structured information from unstructured complaint text, including:

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

The extracted information is automatically populated into the complaint form.

---

### 📋 Complaint Completeness Checking

Checks the extracted complaint information for missing fields.

The system is designed to avoid inventing unavailable information and identifies fields that require additional user input.

---

### 🏷️ Complaint Classification

The AI analyzes the complaint and determines an appropriate complaint category based on the information provided.

---

### ⚠️ AI-Assisted Risk Assessment

Generates an initial assessment containing:

- Risk level
- Severity
- Priority
- Assessment/reason
- Complaint category

The assessment is intended to support human review rather than replace the quality professional's decision.

---

### 🔎 Duplicate Complaint Detection

Checks existing complaint records for matching product and batch information and flags potential duplicates for human review.

---

### 📝 Complaint Summary

Generates a concise summary of the complaint to help users quickly understand the reported issue.

---

### 📄 Multi-Format Complaint Input

Supports:

- PDF
- DOCX
- TXT
- EML
- Directly pasted complaint text

Maximum uploaded file size: **10 MB**

---

### Add a Tech Stack section

I strongly recommend putting this **before the architecture** because recruiters scan README files quickly:

```markdown
## 🛠️ Tech Stack

### Frontend
- React.js
- Redux
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- REST APIs
- SQLAlchemy

### AI / GenAI
- LangGraph
- Groq
- LLM-based information extraction
- Prompt Engineering

### Database
- PostgreSQL

### Document Processing
- PyMuPDF
- python-docx
- TXT/EML processing

### Development Tools
- Git
- GitHub
- VS Code
- Docker

## 🏗️ System Architecture

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
