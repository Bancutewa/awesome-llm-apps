import json
import tempfile
import csv
import streamlit as st
import pandas as pd
from agno.models.google import Gemini
from agno.agent import Agent
import duckdb
import re
import os
from dotenv import load_dotenv
load_dotenv()

# Function to preprocess and save the uploaded file
def preprocess_and_save(file):
    try:
        # Read the uploaded file into a DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None, None, None
        
        # Data cleaning
        df = df.dropna(how='all')  # Remove empty rows
        df.columns = df.columns.str.strip()  # Clean column names

        # Ensure string columns are properly quoted
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)
        
        # Parse dates and numeric columns
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # Keep as is if conversion fails
                    pass
        
        # Create a temporary file to save the preprocessed data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            # Save the DataFrame to the temporary CSV file with quotes around string fields
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)
        
        return temp_path, df.columns.tolist(), df  # Return the DataFrame as well
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None

def optimize_nl_query(user_query, df):
    """Optimize natural language queries for better SQL generation"""

    # Add context about available columns
    context = f"""
    Dataset has these columns: {', '.join(df.columns)}
    Available data types: {df.dtypes.to_dict()}

    User query: {user_query}

    Generate SQL query to answer this question.
    """

    return context
# Streamlit app
st.title("📊 Data Analyst Agent")

# Sidebar for API keys
with st.sidebar:
    st.header("API Keys")
    gemini_key = st.text_input("Enter your Gemini API key:", type="password")
    if gemini_key:
        st.session_state.gemini_key = gemini_key
        st.success("API key saved!")
    else:
        st.warning("Using default Gemini API key.")
        gemini_key = os.getenv("GEMINI_API_KEY")
        st.session_state.gemini_key = gemini_key

# File upload widget
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None and "gemini_key" in st.session_state:
    # Preprocess and save the uploaded file
    temp_path, columns, df = preprocess_and_save(uploaded_file)
    
    if temp_path and columns and df is not None:
        # Display the uploaded data as a table
        st.write("Uploaded Data:")
        st.dataframe(df)  # Use st.dataframe for an interactive table
        
        # Display the columns of the uploaded data
        st.write("Uploaded columns:", columns)
        
        # Configure the semantic model with the temporary file path
        semantic_model = {
            "tables": [
                {
                    "name": "uploaded_data",
                    "description": "Contains the uploaded dataset.",
                    "path": temp_path,
                }
            ]
        }
        
        # Initialize the Data Analysis Agent with Gemini
        data_agent = Agent(
            name="DataAnalyst",
            role="Expert data analyst specializing in SQL query generation",
            model=Gemini(id="gemini-2.0-flash", api_key=st.session_state.gemini_key),
            description="""
            You are an expert data analyst. Given a user query about their dataset, 
            generate precise SQL queries that use correct table and column names, 
            apply appropriate aggregations and filters, and return results in readable format.
            """,
            instructions=[
                "Analyze the user's natural language query about the dataset",
                "Generate appropriate SQL query using the uploaded_data table",
                "Execute the query using DuckDB and return results",
                "Format results in a clear, readable manner",
                "Always include the SQL query in ```sql``` blocks",
                "Provide insights and explanations for the results"
            ],
        )
        
        # Initialize code storage in session state
        if "generated_code" not in st.session_state:
            st.session_state.generated_code = None
        
        # Main query input widget
        user_query = st.text_area("Ask a query about the data:")
        
        # Add info message about terminal output
        st.info("💡 Check your terminal for a clearer output of the agent's response")
        
        if st.button("Submit Query"):
            if user_query.strip() == "":
                st.warning("Please enter a query.")
            else:
                try:
                    # Show loading spinner while processing
                    with st.spinner('Processing your query...'):
                        # Create context for the agent
                        context = f"""
                        Dataset Information:
                        - File: {uploaded_file.name}
                        - Columns: {', '.join(df.columns.tolist())}
                        - Data types: {df.dtypes.to_dict()}
                        - Sample data: {df.head(3).to_dict('records')}
                        - Total rows: {len(df)}
                        
                        User Query: {user_query}
                        
                        Please generate a SQL query to answer this question using the uploaded_data table.
                        The data is stored in a CSV file at: {temp_path}
                        """
                        
                        # Get response from the agent
                        response = data_agent.run(context)
                        
                        # Extract SQL query from response
                        sql_query = None
                        if hasattr(response, 'content'):
                            content = response.content
                        else:
                            content = str(response)
                        
                        # Try to extract SQL query from the response
                        import re
                        sql_match = re.search(r'```sql\s*(.*?)\s*```', content, re.DOTALL | re.IGNORECASE)
                        if sql_match:
                            sql_query = sql_match.group(1).strip()
                            
                            # Execute SQL query with DuckDB
                            try:
                                conn = duckdb.connect()
                                # Load the CSV file into DuckDB
                                conn.execute(f"CREATE OR REPLACE TABLE uploaded_data AS SELECT * FROM read_csv_auto('{temp_path}')")
                                result = conn.execute(sql_query).fetchdf()
                                conn.close()
                                
                                # Display results
                                st.markdown("### 📊 Query Results:")
                                st.dataframe(result)
                                
                                st.markdown("### 🔍 Generated SQL Query:")
                                st.code(sql_query, language='sql')
                                
                            except Exception as sql_error:
                                st.error(f"SQL Execution Error: {sql_error}")
                                st.markdown("### 🤖 AI Response:")
                                st.markdown(content)
                        else:
                            st.markdown("### 🤖 AI Response:")
                            st.markdown(content)
                
                    
                except Exception as e:
                    st.error(f"Error generating response from the Data Analysis Agent: {e}")
                    st.error("Please try rephrasing your query or check if the data format is correct.")