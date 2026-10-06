# 🏙️ AI-Based Smart City Complaint Management System

An AI-powered Smart City Complaint Management System that helps citizens submit complaints and enables administrators to analyze, categorize, prioritize, and manage them efficiently.

## 📌 Project Overview

The system allows citizens to submit complaints along with their name, location, description, and an optional image.

The complaint is analyzed using an AI model, which automatically identifies:

- Complaint Category
- Responsible Department
- Priority
- Severity
- Complaint Summary

The complaint is then stored in an SQLite database and displayed in the Admin Dashboard for further management.

## ✨ Features

- 👤 Complainant name
- 📝 Complaint submission
- 📍 Location details
- 📷 Complaint image upload
- 🤖 AI-based complaint analysis
- 🏷️ Automatic complaint categorization
- 🏢 Department assignment
- ⚡ Priority detection
- 📊 Severity detection
- 📄 Automatic complaint summary
- 🔢 Complaint ID generation
- 🔎 Search and filter complaints
- 📊 Complaint statistics
- 🔄 Complaint status management
- 💾 SQLite database storage

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Ollama
- Llama 3.2
- LangChain
- Hugging Face
- HTML/CSS through Streamlit

## 🧩 System Modules

### 1. Citizen Complaint Module
Citizens can enter their name, complaint description, location, and upload an optional image.

### 2. AI Analysis Module
The AI analyzes the complaint and identifies its category, department, priority, severity, and summary.

### 3. Database Module
Complaint information is stored in an SQLite database.

### 4. Admin Dashboard
Administrators can view complaints, search and filter them, view complaint images, and update complaint status.

## 🤖 AI Categories

The system can classify complaints into:

- Pothole
- Garbage
- Water Leakage
- Street Light
- Drainage
- Other

## 📊 Complaint Status

Complaints can have the following statuses:

- Pending
- In Progress
- Resolved

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd SmartCityComplaint