# Agentic Text-to-SQL System (ClassicModels)

This project is an AI-powered database assistant built with **FastAPI** and **PostgreSQL**. It uses an agentic workflow to translate natural language questions into valid SQL queries, executes them against a provided database schema, and provides human-readable summaries of the results.

## 🚀 Features
- **Query Decomposition:** Breaks down user questions into Intent, Tables, Columns, and Filters before writing SQL.
- **Agentic Self-Correction:** Automatically detects database errors and retries the query up to 3 times with feedback from the error message.
- **Security Guardrails:** Validates all queries to ensure only `SELECT` statements are executed, blocking destructive commands like `DROP` or `DELETE`.
- **Human-Readable Summaries:** Uses LLM (Gemini/Groq) to translate raw database rows into natural language answers.
- **Performance Logging:** Tracks execution time and attempt counts for every query.

---

## 🛠 Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (ClassicModels Schema)
- **ORMs/Tools:** SQLAlchemy, Pydantic
- **AI Models:** Google Gemini (1.5 Flash / 2.0 Flash) or Groq (Llama 3)
- **Environment:** Python 3.12+

---

## 📁 Project Structure
```text
Week_03/
├── app/
│   ├── main.py            # API Endpoints & Entry Point
│   ├── ml_model.py        # LLM SDK Integration (Gemini/Groq)
│   ├── sql_generator.py   # Decomposition & Summary Logic
│   ├── executor.py        # 3-Retry Execution Loop
│   ├── validator.py       # SQL Security Checks
│   ├── database.py        # DB Connection & Raw SQL Execution
│   └── routers/           # Standard CRUD Routes
├── .env                   # API Keys & DB Credentials (Hidden)
├── requirements.txt       # Dependencies
├── pyproject.toml         # Dependencies
├── Week03_sqlanswers.pdf  # SQL Queries Answers from Task 1
├── Week03Findings.pdf     # Benchmark Report & Findings
└── README.md              # Project Documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-link>
cd Week_03
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/classicmodels
GEMINI_API_KEY=your_gemini_api_key
# OR if using Groq
GROQ_API_KEY=your_groq_api_key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload --reload-include "*.py"
```

---

## 🤖 Agent Workflow (Task 4)
The system follows a 5-step agentic process:
1. **Understand:** The agent analyzes the question to identify the required schema components.
2. **Generate:** It writes a PostgreSQL-specific query (handling case-sensitive double quotes).
3. **Validate:** A security layer ensures the query is read-only.
4. **Act (Execute):** The query runs. If it fails, the agent reads the error and loops back to step 2 (Max 3 attempts).
5. **Summarize:** The final result set is transformed into a natural language sentence.

---

## 📊 Evaluation Benchmark (Task 1 & 2)
The agent was evaluated against a **50-question benchmark dataset** covering:
- Simple Data Retrieval
- Multi-table Joins
- Aggregations (`GROUP BY`, `SUM`, `COUNT`)
- Sorting and Filtering

**Key Results:**
- **SQL Accuracy:** ~X% (Update with your findings)
- **Self-Correction Rate:** X% of failed queries were fixed on Attempt 2.
- **Avg. Latency:** ~X.X seconds.

---

## 🛣 API Endpoints

### AI Agent Endpoints
- **`POST /agent/sql`**: (Task 4) The full agentic pipeline. Accepts JSON body.
- **`POST /agent/query`**: (Task 3) Basic Text-to-SQL pipeline.

### Example Request (Task 4)
**URL:** `http://localhost:8000/agent/sql`  
**Body:**
```json
{
  "question": "How many shipped orders are from USA customers?"
}
```

---

## 📝 Deliverables Checklist
- [x] Task 1: Ground Truth SQL queries for 50 questions.
- [x] Task 2: Structured Query Decomposition.
- [x] Task 3: Working Text-to-SQL pipeline with retry logic.
- [x] Task 4: Autonomous Mini SQL Agent with NL Summaries.
- [x] Full Query Execution Logs.

---

## 👨‍💻 Author  
AI Fellowship - Week 03 Assignment
