# 📊 AI Data Analysis Agent

Ứng dụng AI Data Analysis Agent được xây dựng bằng Agno Agent framework và mô hình OpenAI GPT-4o. Agent này giúp người dùng phân tích dữ liệu từ file CSV, Excel thông qua các câu hỏi bằng ngôn ngữ tự nhiên, được hỗ trợ bởi các mô hình ngôn ngữ của OpenAI và DuckDB để xử lý dữ liệu hiệu quả - giúp việc phân tích dữ liệu trở nên dễ dàng với tất cả người dùng, bất kể họ có kiến thức SQL hay không.

## 🎯 Kiến Thức Đã Học Được

### **1. Kiến Thức Tổng Quát**

#### **Kiến Thức Chính Từ Dự Án Này:**

**A. Natural Language to SQL (NL2SQL) Pattern**

- **Khái niệm**: Sử dụng AI để chuyển đổi câu hỏi tự nhiên thành SQL queries
- **Lợi ích**: Cá nhân hóa việc phân tích dữ liệu, không cần chuyên môn SQL
- **Thách thức**: Đảm bảo AI hiểu đúng schema và intent của câu hỏi
- **Giải pháp**: Sử dụng GPT-4 với context về schema dữ liệu

**B. Data Processing Pipeline**

- **Input Processing**: Handle CSV/Excel files, detect data types automatically
- **Data Cleaning**: Xử lý missing values, type conversion, data validation
- **Schema Inference**: Tự động hiểu cấu trúc dữ liệu để tạo semantic model
- **Temporary Storage**: Sử dụng tempfile để DuckDB có thể query dữ liệu

**C. DuckDB Integration với AI**

- **DuckDB**: Database OLAP nhanh, in-process, không cần server
- **Semantic Models**: Cung cấp context về tables và columns cho AI
- **Query Generation**: AI tạo SQL queries dựa trên semantic model
- **Result Processing**: Xử lý kết quả và format output cho user

#### **So Sánh Với Các Dự Án Trước:**

| Dự Án                | Pattern                            | AI Role              | Output                 |
| -------------------- | ---------------------------------- | -------------------- | ---------------------- |
| **Travel Agent**     | Multi-Agent (Researcher + Planner) | 2 agents phối hợp    | Lịch trình du lịch     |
| **Blog to Podcast**  | Single-Agent + Multi-Tools         | 1 agent đa tools     | Audio content          |
| **Breakup Recovery** | Multi-Agent Emotional              | 4 specialized agents | Emotional support      |
| **Data Analysis**    | NL2SQL Agent                       | 1 agent + DuckDB     | SQL queries & insights |

### **2. Kiến Thức Tổng Quát**

#### **A. Data Analysis với AI Agents**

- **Khái niệm**: Sử dụng AI để chuyển đổi ngôn ngữ tự nhiên thành SQL queries
- **Lợi ích**: Cá nhân hóa việc phân tích dữ liệu, không cần chuyên môn SQL
- **Pattern**: `Natural Language → AI Agent → SQL Query → Data Analysis → Results`

#### **B. DuckDB Integration**

- **Vấn đề**: Cần engine database hiệu quả để xử lý dữ liệu lớn
- **DuckDB**: Database OLAP nhanh, in-process, không cần server
- **Giải pháp**: Tích hợp DuckDB với AI agents để query dữ liệu hiệu quả

#### **C. File Processing Pipeline**

- **Input Processing**: Xử lý CSV/Excel files, detect data types
- **Data Cleaning**: Handle missing values, type conversion
- **Schema Inference**: Tự động hiểu cấu trúc dữ liệu
- **Temporary Storage**: Tạo temporary files để DuckDB có thể query

#### **D. Natural Language to SQL Translation**

- **NL2SQL Challenge**: Chuyển đổi câu hỏi tự nhiên thành SQL queries chính xác
- **Context Awareness**: AI hiểu schema và relationships trong data
- **Query Optimization**: Tạo SQL queries hiệu quả và chính xác

### **2. Ví Dụ Từ Code**

#### **A. File Upload & Preprocessing Pipeline**

```python
def preprocess_and_save(file):
    # Read uploaded file into DataFrame
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])

    # Data type inference and conversion
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass  # Keep as string if conversion fails

    # Save to temporary CSV for DuckDB
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

    return temp_path, df.columns.tolist(), df
```

#### **B. DuckDB Agent Configuration**

````python
# Semantic model for DuckDB
semantic_model = {
    "tables": [
        {
            "name": "uploaded_data",
            "description": "Contains the uploaded dataset.",
            "path": temp_path,
        }
    ]
}

# Initialize DuckDbAgent
duckdb_agent = DuckDbAgent(
    model=OpenAIChat(model="gpt-4", api_key=api_key),
    semantic_model=json.dumps(semantic_model),
    tools=[PandasTools()],
    markdown=True,
    system_prompt="You are an expert data analyst. Generate SQL queries to solve the user's query. Return only the SQL query, enclosed in ```sql ``` and give the final answer.",
)
````

#### **C. Query Processing Flow**

```python
# Natural language query processing
user_query = st.text_area("Ask a query about the data:")

if st.button("Submit Query"):
    with st.spinner('Processing your query...'):
        # AI converts natural language to SQL
        response = duckdb_agent.run(user_query)

        # Display results
        st.markdown(response.content)
```

### **3. Tổng Hợp Cách Sử Dụng Cho Sau Này**

#### **A. Data Analysis Agent Template**

````python
def create_data_analysis_agent(file_path, api_key):
    # 1. Preprocess data
    temp_path, columns, df = preprocess_and_save(uploaded_file)

    # 2. Create semantic model
    semantic_model = {
        "tables": [{
            "name": "data_table",
            "description": "User uploaded dataset",
            "path": temp_path,
        }]
    }

    # 3. Initialize agent
    agent = DuckDbAgent(
        model=OpenAIChat(model="gpt-4", api_key=api_key),
        semantic_model=json.dumps(semantic_model),
        tools=[PandasTools()],
        system_prompt="""You are an expert data analyst.
        Generate SQL queries to solve user queries.
        Return only the SQL query in ```sql``` blocks and final answer.""",
    )

    return agent, df

# Usage
agent, df = create_data_analysis_agent(file_path, api_key)
response = agent.run("What are the top 5 sales by region?")
````

#### **B. File Processing Best Practices**

```python
def robust_file_processing(file):
    try:
        # 1. Detect file type
        file_ext = file.name.split('.')[-1].lower()

        # 2. Read with appropriate method
        if file_ext == 'csv':
            df = pd.read_csv(file, encoding='utf-8')
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported format")

        # 3. Data cleaning
        df = df.dropna(how='all')  # Remove empty rows
        df.columns = df.columns.str.strip()  # Clean column names

        # 4. Type inference
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try date conversion
                if 'date' in col.lower():
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                # Try numeric conversion
                else:
                    df[col] = pd.to_numeric(df[col], errors='ignore')

        # 5. Create temp file for DuckDB
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp:
            df.to_csv(temp.name, index=False, quoting=csv.QUOTE_ALL)
            return temp.name, df

    except Exception as e:
        st.error(f"File processing error: {e}")
        return None, None
```

#### **C. Natural Language Query Optimization**

```python
def optimize_nl_query(user_query, df_schema):
    """Optimize natural language queries for better SQL generation"""

    # Add context about available columns
    context = f"""
    Dataset has these columns: {', '.join(df_schema)}
    Available data types: {df.dtypes.to_dict()}

    User query: {user_query}

    Generate SQL query to answer this question.
    """

    return context

# Usage
optimized_query = optimize_nl_query(
    "Show me sales by month",
    df.columns.tolist()
)
response = agent.run(optimized_query)
```

## 🎯 Hướng Dẫn Prompt Engineering Cho Data Analysis

### **1. System Prompt Optimization**

#### **A. Basic vs Advanced System Prompts**

````python
# ❌ Too basic
system_prompt = "You are a data analyst."

# ✅ Context-aware and specific
system_prompt = """You are an expert data analyst specializing in SQL query generation.

Given a user query about their dataset, generate precise SQL queries that:
1. Use correct table and column names
2. Apply appropriate aggregations and filters
3. Handle date formatting and data types properly
4. Return results in readable format

Dataset context: {table_schema}
Available columns: {columns_list}
Data types: {data_types}

Return only the SQL query in ```sql``` blocks followed by the final answer."""
````

### **2. Query Enhancement Techniques**

#### **A. Few-Shot Examples**

```python
few_shot_examples = """
Example 1:
User: "What are the total sales by region?"
SQL: SELECT region, SUM(sales) as total_sales FROM uploaded_data GROUP BY region ORDER BY total_sales DESC;

Example 2:
User: "Show me customers who spent more than $1000"
SQL: SELECT customer_name, total_spent FROM uploaded_data WHERE total_spent > 1000 ORDER BY total_spent DESC;

Example 3:
User: "What's the average order value by month?"
SQL: SELECT strftime('%Y-%m', order_date) as month, AVG(order_value) as avg_value FROM uploaded_data GROUP BY month ORDER BY month;
"""

enhanced_prompt = f"{few_shot_examples}\n\nNow, for this query: {user_query}"
```

## Tính năng

- 📤 **Hỗ trợ Upload File**:

  - Upload file CSV và Excel
  - Tự động phát hiện kiểu dữ liệu và schema
  - Hỗ trợ nhiều định dạng file

- 💬 **Truy vấn Ngôn ngữ Tự nhiên**:

  - Chuyển đổi câu hỏi tự nhiên thành SQL queries
  - Nhận câu trả lời tức thì về dữ liệu
  - Không cần kiến thức SQL

- 🔍 **Phân tích Nâng cao**:

  - Thực hiện các phép tổng hợp dữ liệu phức tạp
  - Lọc và sắp xếp dữ liệu
  - Tạo báo cáo thống kê
  - Tạo biểu đồ và visualizations

- 🎯 **Giao diện Tương tác**:
  - Giao diện Streamlit thân thiện với người dùng
  - Xử lý truy vấn theo thời gian thực
  - Trình bày kết quả rõ ràng

## Cách bắt đầu?

1. Clone kho lưu trữ GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/starter_ai_agents/ai_data_analysis_agent
```

2. Cài đặt các dependencies cần thiết:

```bash
pip install -r requirements.txt
```

3. Lấy GEMINI API Key của bạn

4. Chạy ứng dụng Streamlit

```bash
streamlit run ai_data_analyst.py
```

## Cách hoạt động?

AI Data Analysis Agent hoạt động theo quy trình sau:

### **1. Data Ingestion & Preprocessing**

```python
def preprocess_and_save(file):
    # Đọc file và detect format
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])

    # Data cleaning và type inference
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass  # Keep as string

    # Lưu temporary file cho DuckDB
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
        df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

    return temp_path, df.columns.tolist(), df
```

### **2. Semantic Model Creation**

```python
semantic_model = {
    "tables": [{
        "name": "uploaded_data",
        "description": "Contains the uploaded dataset.",
        "path": temp_path,
    }]
}
```

### **3. AI Agent Initialization**

```python
duckdb_agent = DuckDbAgent(
    model=OpenAIChat(model="gpt-4", api_key=api_key),
    semantic_model=json.dumps(semantic_model),
    tools=[PandasTools()],
    system_prompt="You are an expert data analyst. Generate SQL queries to solve the user's query.",
)
```

### **4. Query Processing Flow**

```python
# Natural language → SQL → Results
user_query = "What are the top 5 products by sales?"
response = duckdb_agent.run(user_query)
st.markdown(response.content)
```

## Kiến trúc kỹ thuật chi tiết

### **Core Components:**

1. **Frontend Layer (Streamlit)**

   - File upload interface
   - Query input textarea
   - Results display
   - API key management

2. **Data Processing Layer**

   - File format detection (CSV/Excel)
   - Data type inference
   - Schema extraction
   - Temporary file management

3. **AI Processing Layer**

   - OpenAI GPT-4 integration
   - Natural language understanding
   - SQL query generation
   - Context management

4. **Database Layer (DuckDB)**
   - In-memory data processing
   - SQL query execution
   - Result formatting
   - Performance optimization

### **Data Flow:**

```
User Upload → File Processing → Schema Inference → Semantic Model
                                        ↓
Natural Language Query → GPT-4 → SQL Generation → DuckDB → Results → UI Display
```

## Ví dụ sử dụng

### **Dữ liệu mẫu**: File CSV nhân viên với các cột: name, age, city, salary, department

### **Các câu hỏi có thể hỏi**:

- "Tuổi trung bình của nhân viên theo phòng ban?"
- "Thành phố nào có nhiều nhân viên nhất?"
- "Top 3 phòng ban có lương cao nhất?"
- "Phân bố lương theo độ tuổi?"
- "Tổng lương theo khu vực địa lý?"

### **Kết quả mẫu**:

**Query**: "Tuổi trung bình theo phòng ban?"

```sql
SELECT department, AVG(age) as avg_age
FROM uploaded_data
GROUP BY department
ORDER BY avg_age DESC;
```

**Kết quả**:
| department | avg_age |
|------------|---------|
| Sales | 40.0 |
| HR | 36.0 |
| Marketing | 29.5 |
| Engineering| 28.5 |

## Debug và Troubleshooting

### **Các lỗi thường gặp:**

1. **API Key Issues**

   ```python
   # Error: "Please enter your OpenAI API key to proceed."
   # Solution: Enter valid OpenAI API key in sidebar
   ```

2. **File Processing Errors**

   ```python
   # Error: "Unsupported file format"
   # Solution: Only upload CSV or Excel files
   ```

3. **Data Type Issues**

   ```python
   # Error: "Error processing file: ..."
   # Solution: Check file encoding, missing values, column names
   ```

4. **Query Generation Issues**
   ```python
   # Error: "No results found"
   # Solution: Rephrase query, check column names, verify data
   ```

### **Best Practices cho Debugging:**

1. **Check Data First**: Luôn xem preview data trước khi query
2. **Simple Queries First**: Bắt đầu với queries đơn giản
3. **Verify Column Names**: Đảm bảo tên cột chính xác
4. **Check Data Types**: Verify numeric/date columns được detect đúng
5. **Monitor Terminal**: Xem output trong terminal cho debugging info

## Kiến trúc kỹ thuật

- **Frontend**: Streamlit cho giao diện web
- **AI Engine**: OpenAI GPT-4o cho NL2SQL conversion
- **Database**: DuckDB cho data processing và querying
- **Data Processing**: Pandas cho file I/O và preprocessing
- **Tools**: Agno framework cho agent orchestration

## Best Practices đã học

1. **Data Validation**: Luôn validate input data trước khi xử lý
2. **Error Handling**: Implement comprehensive error handling cho user experience tốt
3. **Type Inference**: Tự động detect và convert data types
4. **Query Optimization**: Sử dụng semantic models để cải thiện accuracy
5. **User Feedback**: Cung cấp progress indicators và clear error messages
6. **Security**: Handle API keys an toàn, validate file uploads
7. **Performance**: Sử dụng temporary files và efficient data structures

---

## 📚 **TỔNG KẾT KIẾN THỨC ĐÃ HỌC**

### **1. AI Data Analysis Agent - Kiến Thức Mới**

#### **A. Natural Language to SQL (NL2SQL)**

- **Pattern mới**: Single-Agent với DuckDB integration
- **Thách thức**: Chuyển đổi ngôn ngữ tự nhiên thành SQL queries chính xác
- **Giải pháp**: GPT-4 + semantic models + context injection

#### **B. Data Processing Pipeline**

- **File Handling**: CSV/Excel auto-detection
- **Data Cleaning**: Missing values, type conversion, schema inference
- **Temporary Storage**: tempfile management cho DuckDB

#### **C. DuckDB Integration**

- **In-Process Database**: Không cần server setup
- **High Performance**: OLAP queries trên large datasets
- **SQL Generation**: AI tạo queries dựa trên user intent

### **2. Pattern Comparison với Dự Án Trước**

| Aspect           | Travel Agent       | Blog→Podcast          | Breakup Recovery       | **Data Analysis**          |
| ---------------- | ------------------ | --------------------- | ---------------------- | -------------------------- |
| **Architecture** | Multi-Agent        | Single + Tools        | Multi-Agent Emotional  | **NL2SQL Agent**           |
| **AI Focus**     | Content Generation | Multi-Modal           | Emotional Intelligence | **Data Intelligence**      |
| **Tools**        | SerpAPI, Groq      | Firecrawl, ElevenLabs | Gemini Vision          | **DuckDB, Pandas**         |
| **Output**       | Travel Itinerary   | Audio Content         | Emotional Support      | **SQL Queries & Insights** |
| **Complexity**   | Medium             | Medium                | High                   | **Medium-High**            |

### **3. Technical Skills Acquired**

#### **A. Data Engineering Skills**

- **File Processing**: CSV/Excel handling với pandas
- **Data Type Inference**: Automatic column type detection
- **Schema Management**: Semantic model creation
- **Temporary File Management**: Secure temp file handling

#### **B. AI Integration Skills**

- **NL2SQL**: Natural language to SQL conversion
- **Context Management**: Providing schema context to AI
- **Prompt Engineering**: System prompts cho data analysis
- **Error Handling**: Robust error handling cho AI responses

#### **C. Database Skills**

- **DuckDB**: In-memory analytical database
- **SQL Generation**: AI-powered SQL query creation
- **Result Processing**: Formatting và displaying results
- **Performance Optimization**: Efficient data processing

### **4. Best Practices Learned**

#### **A. Data Analysis Best Practices**

```python
# ✅ Good: Comprehensive data preprocessing
def preprocess_data(file):
    df = load_file(file)
    df = clean_data(df)
    df = infer_types(df)
    return df

# ✅ Good: Semantic model for AI context
semantic_model = {
    "tables": [{
        "name": "data",
        "description": "User dataset",
        "path": temp_path
    }]
}
```

#### **B. User Experience Best Practices**

```python
# ✅ Good: Clear user feedback
with st.spinner('Processing your query...'):
    result = agent.run(query)

# ✅ Good: Data preview before analysis
st.write("Uploaded Data:")
st.dataframe(df.head())

# ✅ Good: Error handling with user-friendly messages
try:
    result = process_data(data)
except Exception as e:
    st.error(f"Processing failed: {str(e)}")
```

### **5. Template Patterns Cho Dự Án Tương Lai**

#### **A. Data Analysis Agent Template**

```python
def create_data_agent_template():
    return {
        "components": {
            "data_processor": "Pandas-based file processing",
            "ai_engine": "GPT-4 with semantic models",
            "database": "DuckDB for querying",
            "frontend": "Streamlit for UI"
        },
        "patterns": {
            "nl2sql": "Natural language to SQL conversion",
            "semantic_model": "Context provision for AI",
            "error_handling": "Comprehensive exception handling"
        }
    }
```

#### **B. Reusable Components**

```python
class DataAnalysisAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.semantic_model = None

    def process_file(self, file):
        # File processing logic
        pass

    def create_semantic_model(self, df, temp_path):
        # Semantic model creation
        pass

    def query_data(self, natural_language_query):
        # NL2SQL processing
        pass
```

**Kiến thức tích lũy:**

1. Multi-Agent Architecture (Travel Agent)
2. Single-Agent Multi-Tools (Blog→Podcast)
3. Emotional AI & Vision (Breakup Recovery)
4. **NL2SQL & Data Processing (Data Analysis)**
