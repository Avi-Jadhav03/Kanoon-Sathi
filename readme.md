# ⚖️ KanoonSathi — AI Legal Document Auditor

## 🌍 Live Demo
Coming soon

---

## 🧠 Project Overview

KanoonSathi is a multi-agent AI system that audits Indian legal documents and gives plain-English feedback on what's wrong, what's missing, and what could get it rejected — no lawyer needed.

Built for common people — tenants, students, small shop owners, RTI filers — who receive legal documents but can't afford lawyers or don't know enough to use ChatGPT correctly.

Every existing tool (VakilSearch, Manupatra, BharatLaw) is built for lawyers. KanoonSathi is built for the person who doesn't even know what CPC means.

---

## 🔥 Features

### ✅ Core Features
- Upload any Indian legal document (PDF)
- Automatic document type detection
- Structured clause extraction
- Cross-check against real Indian law corpus
- Plain-English audit report with risk score

### 🤖 AI Pipeline Features
- 6-agent LangGraph state machine
- RAG on actual Indian legal acts (RTI Act, Transfer of Property Act, Maharashtra Rent Control Act, Indian Contract Act, Consumer Protection Act)
- Self-correcting hallucination guard loop — agents verify each other's outputs
- Conditional routing — system loops back and re-fetches laws if findings are unreliable

---

## 🛠 Tech Stack

- LangGraph
- LangChain
- Groq (Llama 3.3 70B)
- ChromaDB
- HuggingFace Embeddings
- FastAPI
- HTML, CSS, JavaScript

---

## ⚙️ How It Works

### The 6-Agent Pipeline

PDF Upload

↓

Type Identifier — detects document type

↓

Meaning Extractor — extracts structured data (parties, dates, amounts, clauses)

↓

Law Fetcher — semantic search on Indian legal corpus

↓

Cross Checker — flags issues against retrieved laws

↓

Hallucination Guard — verifies findings are law-backed

↓ (re-fetch loop if not verified)

Report Generator — plain English audit report

### The Self-Correcting Loop

Cross Checker → Hallucination Guard

|

verdict: re-fetch?

Yes ↓        No ↓

Law Fetcher    Report Generator


The Hallucination Guard can reject Cross Checker's findings and send the system back to Law Fetcher with a more targeted query. This loop is what makes the system reliable for legal use.

---

## 🚀 Setup & Run

### Installation

```bash
git clone git@github.com:Avi-Jadhav03/kanoon-sathi.git
cd kanoon-sathi

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

```bash
cp .env.example .env
# Add your GROQ_API_KEY
```

### Build Legal Corpus

```bash
# Add Indian legal PDFs to documents/ folder
python llm/ingest.py
```

### Run

```bash
uvicorn app:app --reload
```

Open `http://localhost:8000`

---

## 📊 Example Output

```json
{
  "overall_risk": "High",
  "summary": "Your rent agreement is missing some important clauses that could cause problems later.",
  "issues": [
    {
      "issue": "No dispute resolution clause",
      "why_it_matters": "If there is a conflict, you won't have a clear process to resolve it",
      "how_to_fix": "Add a clause specifying how disputes will be resolved"
    }
  ]
}
```

---

## 📁 Project Structure

kanoon-sathi/

├── app.py                 # FastAPI backend

├── requirements.txt

├── documents/             # Indian legal PDFs

├── vectorstore/           # ChromaDB (auto-generated)

├── static/

│   └── index.html         # Frontend

└── llm/

├── agents.py          # All 6 agents

├── main.py            # LangGraph graph

├── state.py           # Shared state

└── ingest.py          # RAG ingestion

---

## ⚠️ Notes

- Free tier Groq has daily token limits — production needs paid API
- Legal corpus covers major central acts — state-specific laws can be added
- Not a substitute for professional legal advice

---

## 📚 What I Learned

- Multi-agent orchestration with LangGraph
- Building RAG pipelines on domain-specific corpus
- Designing self-correcting AI systems with verification loops
- Prompt engineering for legal reasoning
- FastAPI async backend with file upload
- Thinking like a systems architect — state design, agent separation, conditional routing

---

## 👨‍💻 Author

Avishkar Jadhav