#extract schema
from sqlalchemy import create_engine,inspect
import json
import regex as re
db_url="sqlite:///amazon.db"

def extract_schema(db_url):
    engine=create_engine(db_url)
    inspector=inspect(engine)
    schema={}
    for table_name in inspector.get_table_names():
        columns  = inspector.get_columns(table_name)
        schema[table_name]=[col['name'] for col in columns]

    return json.dumps(schema)

#text to sql(deepseek with ollama)
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

def text_to_sql(schema,prompt):
    SYSTEM_PROMPT="""
    You are an expert SQL generator. Given a database schema and a user prompt,generate 
    a valid SQL query that answers the prompt. Only use the tables and columns provided in the schema.
    Ensure the SQL syntax is correct and avoid using any unsupported features.Output only the SQL.
    """

    prompt_template=ChatPromptTemplate.from_messages(
        [
            ("system",SYSTEM_PROMPT),
            ("user","Schema:\n{schema}\n Question:{user_prompt}\n\n Sql Query")
        ]
    )

    model = OllamaLLM(model="deepseek-r1:1.5b")

    chain = prompt_template | model
    raw =chain.invoke({"schema":schema,"user_prompt":prompt})
    cleaned_response=re.sub(r"<think>.*?</think>","",raw,flags=re.DOTALL)
    return cleaned_response


def run(prompt):
    schema=extract_schema(db_url)
    # prompt="tell me the top 5 names of all the customers"
    sql_query=text_to_sql(schema,prompt)
    print(sql_query)

    import sqlite3
    import pandas as pd

    db_path = "amazon.db"

    conn = sqlite3.connect(db_path)

    results = pd.read_sql_query(sql_query, conn)

    conn.close()

    return results
   
