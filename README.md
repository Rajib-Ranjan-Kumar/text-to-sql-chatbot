# AI Data Analyst

An AI-powered **Text-to-SQL** application that converts natural-language questions into SQL queries and displays the results from a SQLite database.


- Ask questions about your data in natural language
- Automatically extracts the SQLite database schema
- Generates SQL using a local Ollama LLM
- Executes SQL queries on SQLite
- Displays results in an interactive Streamlit table
- Uses Pandas for structured results

## 🛠️ Tech Stack

- Python
- LangChain
- Ollama
- DeepSeek-R1
- SQLite
- SQLAlchemy
- Pandas
- Streamlit

## 🔄 How It Works

```text
User Question
      ↓
Extract Database Schema
      ↓
LLM generates SQL
      ↓
Execute SQL on SQLite
      ↓
Pandas DataFrame
      ↓
Streamlit Table
```

## 📁 Project Structure

```text
text-to-sql-chatbot/
│
├── create_database.py
├── main.py
├── frontend.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Rajib-Ranjan-Kumar/text-to-sql-chatbot.git
cd text-to-sql-chatbot
```

### 2. Create and activate virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama model

```bash
ollama pull deepseek-r1:1.5b
```

Make sure Ollama is running.

### 5. Create the database

```bash
python create_database.py
```

### 6. Run Streamlit

```bash
streamlit run frontend.py
```

## 💬 Example Questions

```text
Show the first 5 customers
```

```text
Show all customer names
```

```text
Show customers from Ranchi
```

```text
Show products with price greater than 500
```

## 🔑 Main Components

**`main.py`**
- Extracts database schema
- Converts natural language to SQL
- Executes SQL and returns a Pandas DataFrame

**`frontend.py`**
- Streamlit user interface
- Displays query results as a table

**`create_database.py`**
- Creates the sample SQLite database

## 🔒 Security

The application is designed for a local/educational environment. In production, generated SQL should be validated and restricted to read-only operations.

## 📌 Future Improvements

- SQL query validation
- Query history
- Data visualization
- CSV export
- Multiple database support
- Conversational follow-up questions

---

Built with Python, LangChain, Ollama, SQLite, Pandas, and Streamlit.
