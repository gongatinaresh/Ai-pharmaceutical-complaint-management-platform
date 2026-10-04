# AI-Driven Pharmaceutical Complaint Management Platform

An AI-powered full-stack application for managing pharmaceutical customer complaints.

The system converts unstructured complaint information from text, PDF, DOCX, TXT, and EML files into structured complaint records and assists users with complaint classification, completeness checking, AI-assisted risk assessment, summarization, and possible duplicate detection.

> Developed as part of the AIVOA AI Product Engineer internship assignment.

---

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
