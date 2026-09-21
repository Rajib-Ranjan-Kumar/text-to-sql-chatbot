# AI Data Analyst

An AI-powered data analyst that converts **natural language questions into SQL queries** and executes them on a local SQLite database.

The project uses **LangChain**, **Ollama**, **DeepSeek-R1**, **SQLAlchemy**, **Pandas**, and **Streamlit** to provide a simple natural-language interface for querying data.

## Features

- Ask questions about your database using natural language
- Automatically extract database schema using SQLAlchemy
- Convert natural-language questions into SQL using a local Ollama LLM
- Execute generated SQL queries on a local SQLite database
- Display query results in an interactive Streamlit table
- Uses Pandas for structured query results
- Runs completely with a local LLM through Ollama
- Simple Python API through the `run()` function
- Easy to extend with other Ollama models

## Tech Stack

- Python 3.11+
- SQLite
- SQLAlchemy
- LangChain
- LangChain Ollama
- Ollama
- DeepSeek-R1
- Pandas
- Streamlit

## Project Architecture

```text
User Question
      |
      v
Streamlit Frontend
      |
      v
run(prompt)
      |
      +----------------------+
      |                      |
      v                      v
extract_schema()       text_to_sql()
      |                      |
      |                      v
      |                Ollama LLM
      |                DeepSeek-R1
      |                      |
      |                      v
      |                  SQL Query
      |                      |
      +-----------> SQLite Database
                             |
                             v
                       Pandas DataFrame
                             |
                             v
                    Streamlit Data Table
```

## Project Structure

```text
AI-Data-Analyst/
│
├── amazon.db
├── main.py
├── app.py
├── README.md
└── requirements.txt
```

## How It Works

### 1. Extract Database Schema

The application uses SQLAlchemy's inspector to automatically read the tables and columns from `amazon.db`.

```python
def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)

    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col["name"] for col in columns]

    return json.dumps(schema)
```

The schema is then provided to the LLM so that it knows which tables and columns are available.

### 2. Convert Natural Language to SQL

The user enters a question such as:

```text
Show the first 5 customers
```

The LLM receives the database schema and user question and generates an SQL query.

Example:

```sql
SELECT *
FROM customers
LIMIT 5;
```

The project currently uses:

```python
model = OllamaLLM(model="deepseek-r1:1.5b")
```

You can switch to another Ollama model depending on your system and requirements.

### 3. Execute the SQL Query

The generated SQL is executed against the local SQLite database:

```python
conn = sqlite3.connect("amazon.db")

results = pd.read_sql_query(sql_query, conn)

conn.close()

return results
```

The result is returned as a Pandas DataFrame.

### 4. Display Results in Streamlit

The Streamlit frontend displays the DataFrame as an interactive table:

```python
st.dataframe(answer, use_container_width=True)
```

This makes query results easier to read than displaying the DataFrame as plain text.

## Example Questions

You can ask questions such as:

```text
Show the first 5 customers
```

```text
Show all customers from Ranchi
```

```text
What are the most expensive products?
```

```text
Show the top 5 customers
```

```text
How many products are available?
```

```text
Show products with price greater than 500
```

The exact questions you can ask depend on the tables and columns available in `amazon.db`.

## Prerequisites

Before running the project, install:

- Python 3.11 or later
- Ollama
- A compatible Ollama model
- SQLite database

### Install Ollama

Download Ollama from:

https://ollama.com/download

After installation, pull the model:

```bash
ollama pull deepseek-r1:1.5b
```

You can also use another model supported by your Ollama installation.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

```bash
cd YOUR_REPOSITORY
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
streamlit
pandas
sqlalchemy
langchain-core
langchain-ollama
regex
```

### 4. Make Sure Ollama Is Running

Check that Ollama is available:

```bash
ollama list
```

Make sure your model is installed:

```bash
ollama pull deepseek-r1:1.5b
```

### 5. Add the Database

Place your SQLite database in the project root:

```text
AI-Data-Analyst/
└── amazon.db
```

The current project expects:

```python
db_url = "sqlite:///amazon.db"
```

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

You can then enter a question and click:

```text
Analyze
```

The application will:

```text
Question
   ↓
Schema Extraction
   ↓
LLM SQL Generation
   ↓
SQL Execution
   ↓
Pandas DataFrame
   ↓
Interactive Table
```

## Example

### User Input

```text
Show all customer names
```

### Generated SQL

```sql
SELECT name
FROM customers;
```

### Streamlit Output

| name |
|---|
| Neha Sharma |
| Arjun Patel |
| Priya Sharma |
| Aditya Das |
| Aman Patel |

## Main Components

### `main.py`

Contains the core data-analysis pipeline:

- `extract_schema()`
- `text_to_sql()`
- `run()`

### `app.py`

Contains the Streamlit user interface:

- Question input
- Analyze button
- Loading spinner
- Success message
- Interactive result table

### `amazon.db`

Local SQLite database containing the data queried by the application.

## SQL Generation Prompt

The LLM is instructed to generate SQL using only the provided schema:

```text
You are an expert SQL generator. Given a database schema and a user prompt,
generate a valid SQL query that answers the prompt.

Only use the tables and columns provided in the schema.
Ensure the SQL syntax is correct and avoid using any unsupported features.
Output only the SQL.
```

## DeepSeek Thinking Output

Reasoning models may return `<think>` blocks before the SQL query.

The project removes these blocks before executing the query:

```python
cleaned_response = re.sub(
    r"<think>.*?</think>",
    "",
    raw,
    flags=re.DOTALL
)
```

## Model Switching

You can change the Ollama model in `main.py`.

For example:

```python
model = OllamaLLM(model="qwen2.5-coder:7b")
```

Then install the model:

```bash
ollama pull qwen2.5-coder:7b
```

Different models may provide different trade-offs between speed, reasoning ability, and SQL generation quality.

## Security Considerations

The application executes SQL generated by an LLM.

For a local learning project this is useful, but production applications should add safeguards.

For example, restrict queries to read-only operations:

```python
if not sql_query.lower().strip().startswith("select"):
    raise ValueError("Only SELECT queries are allowed.")
```

Additional validation should be implemented to prevent statements such as:

```sql
DROP
DELETE
UPDATE
INSERT
ALTER
CREATE
```

Do not connect an unrestricted LLM-generated SQL system to sensitive production databases without proper access controls and query validation.

## Future Improvements

- Add SQL query validation
- Restrict database access to read-only queries
- Add query history
- Display generated SQL in the UI
- Add charts and visualizations
- Add automatic chart generation based on query results
- Add support for multiple SQLite databases
- Add PostgreSQL support
- Add DuckDB support
- Cache database schema
- Add error handling for invalid SQL
- Add conversational follow-up questions
- Add downloadable CSV results
- Add authentication
- Add automated tests

## Learning Goals

This project demonstrates how to combine:

- Natural Language Processing
- Large Language Models
- LangChain
- Local LLMs
- Text-to-SQL
- SQL databases
- Pandas
- Streamlit
- AI-assisted data analysis

It is designed as a practical project for understanding how natural-language interfaces can be connected to structured databases.

## License

This project is for educational and development purposes.

You can add your preferred open-source license to the repository.

---

Built with Python, LangChain, Ollama, SQLite, Pandas, and Streamlit.
