# 📊 AI Data Visualization Agent

Ứng dụng Streamlit này là một AI Data Visualization Agent được hỗ trợ bởi AI, hoạt động như chuyên gia trực quan hóa dữ liệu cá nhân của bạn. Chỉ cần tải lên dataset và đặt câu hỏi bằng ngôn ngữ tự nhiên - AI agent sẽ phân tích dữ liệu, tạo ra các biểu đồ phù hợp và cung cấp insights thông qua sự kết hợp của biểu đồ, thống kê và giải thích.

## 🎯 Kiến Thức Đã Học Được

### **1. Kiến Thức Tổng Quát**

#### **A. AI-Powered Data Analysis Pattern**

- **Khái niệm**: Sử dụng LLM để phân tích dữ liệu và tạo visualizations tự động
- **Lợi ích**: Tự động hóa quá trình phân tích, giảm thời gian xử lý, insights thông minh
- **Pattern**: `Data Upload → Natural Language Query → AI Analysis → Code Generation → Visualization`

#### **B. Code Interpreter Integration**

- **Vấn đề**: Cần môi trường an toàn để thực thi code Python
- **Giải pháp**: E2B Sandbox - môi trường sandbox đám mây
- **Lợi ích**: Bảo mật, scalability, không cần setup local environment

#### **C. Multi-Model AI Support**

- **Meta-Llama 3.1 405B**: Cho phân tích phức tạp
- **DeepSeek V3**: Cho insights chi tiết
- **Qwen 2.5 7B**: Cho phân tích nhanh
- **Meta-Llama 3.3 70B**: Cho queries nâng cao

#### **D. Natural Language to Code (NL2Code)**

- **Khái niệm**: Chuyển đổi câu hỏi tự nhiên thành Python code
- **Ứng dụng**: Tự động tạo visualizations, statistical analysis
- **Pattern**: `User Query → LLM → Python Code → Execution → Results`

### **2. Ví Dụ Từ Code**

#### **A. Code Interpreter Integration**

```python
# E2B Sandbox setup
with Sandbox(api_key=st.session_state.e2b_api_key) as code_interpreter:
    # Upload dataset
    dataset_path = upload_dataset(code_interpreter, uploaded_file)

    # Execute AI-generated code
    code_results, llm_response = chat_with_llm(code_interpreter, query, dataset_path)
```

#### **B. Natural Language Processing**

```python
def chat_with_llm(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str):
    system_prompt = f"""You're a Python data scientist and data visualization expert.
    You are given a dataset at path '{dataset_path}' and also the user's query.
    You need to analyze the dataset and answer the user's query with a response
    and you run Python code to solve them.
    IMPORTANT: Always use the dataset path variable '{dataset_path}' in your code
    when reading the CSV file."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    # Get AI response with code
    response = client.chat.completions.create(
        model=st.session_state.model_name,
        messages=messages,
    )
```

#### **C. Code Extraction & Execution**

````python
def match_code_blocks(llm_response: str) -> str:
    pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    match = pattern.search(llm_response)
    if match:
        code = match.group(1)
        return code
    return ""

def code_interpret(e2b_code_interpreter: Sandbox, code: str):
    with st.spinner('Executing code in E2B sandbox...'):
        exec = e2b_code_interpreter.run_code(code)

        if exec.error:
            print(f"[Code Interpreter ERROR] {exec.error}")
            return None
        return exec.results
````

#### **D. Multi-Model Selection**

```python
# Model selection dropdown
model_options = {
    "Meta-Llama 3.1 405B": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "DeepSeek V3": "deepseek-ai/DeepSeek-V3",
    "Qwen 2.5 7B": "Qwen/Qwen2.5-7B-Instruct-Turbo",
    "Meta-Llama 3.3 70B": "meta-llama/Llama-3.3-70B-Instruct-Turbo"
}

st.session_state.model_name = st.selectbox(
    "Select Model",
    options=list(model_options.keys()),
    index=0
)
```

#### **E. Result Visualization**

```python
# Display different types of results
if code_results:
    for result in code_results:
        if hasattr(result, 'png') and result.png:
            # Decode base64 PNG data
            png_data = base64.b64decode(result.png)
            image = Image.open(BytesIO(png_data))
            st.image(image, caption="Generated Visualization")
        elif hasattr(result, 'figure'):
            # Matplotlib figures
            fig = result.figure
            st.pyplot(fig)
        elif hasattr(result, 'show'):
            # Plotly figures
            st.plotly_chart(result)
        elif isinstance(result, (pd.DataFrame, pd.Series)):
            # DataFrames
            st.dataframe(result)
        else:
            st.write(result)
```

### **3. Tổng Hợp Cách Sử Dụng Cho Sau Này**

#### **A. Template AI Data Analysis System**

```python
# Template cơ bản cho AI data analysis system
def create_ai_data_analysis_system():
    # 1. Setup code interpreter
    with Sandbox(api_key=e2b_api_key) as code_interpreter:
        # 2. Upload dataset
        dataset_path = upload_dataset(code_interpreter, uploaded_file)

        # 3. Process user query
        code_results, llm_response = chat_with_llm(
            code_interpreter,
            user_query,
            dataset_path
        )

        # 4. Display results
        display_results(code_results, llm_response)
```

#### **B. Code Interpreter Best Practices**

```python
# Best practices for code interpreter
def robust_code_execution():
    # ✅ 1. Error handling
    try:
        exec = code_interpreter.run_code(code)
        if exec.error:
            st.error(f"Code execution error: {exec.error}")
            return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

    # ✅ 2. Output capture
    with contextlib.redirect_stdout(stdout_capture):
        with contextlib.redirect_stderr(stderr_capture):
            exec = code_interpreter.run_code(code)

    # ✅ 3. Result processing
    if exec.results:
        for result in exec.results:
            process_result(result)
```

#### **C. Multi-Model Strategy**

```python
# Model selection strategy
def select_appropriate_model(task_type):
    model_mapping = {
        "simple_analysis": "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "complex_analysis": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "detailed_insights": "deepseek-ai/DeepSeek-V3",
        "advanced_queries": "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    }
    return model_mapping.get(task_type, "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo")
```

#### **D. Natural Language to Code Template**

```python
# NL2Code template
def create_nl2code_system():
    system_prompt = """You're a Python data scientist and visualization expert.
    Given a dataset and user query, generate Python code to:
    1. Load and analyze the data
    2. Create appropriate visualizations
    3. Provide statistical insights
    4. Answer the user's question

    Always use the provided dataset path and ensure code is executable."""

    def process_query(user_query, dataset_path):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Dataset: {dataset_path}\nQuery: {user_query}"}
        ]

        response = llm_client.chat.completions.create(
            model=selected_model,
            messages=messages
        )

        # Extract and execute code
        code = extract_code_blocks(response.choices[0].message.content)
        results = execute_code(code)

        return results, response.choices[0].message.content
```

#### **E. Result Processing Template**

```python
# Result processing template
def process_visualization_results(results):
    for result in results:
        if hasattr(result, 'png'):
            # Handle PNG images
            display_image(result.png)
        elif hasattr(result, 'figure'):
            # Handle matplotlib figures
            display_matplotlib_figure(result.figure)
        elif hasattr(result, 'show'):
            # Handle plotly figures
            display_plotly_chart(result)
        elif isinstance(result, pd.DataFrame):
            # Handle DataFrames
            display_dataframe(result)
        else:
            # Handle other results
            display_text_result(result)
```

### **4. Best Practices Summary**

```python
# Best practices checklist
def apply_data_visualization_best_practices():
    # ✅ 1. Code interpreter integration
    # - Use secure sandbox environment
    # - Handle errors gracefully
    # - Capture all outputs

    # ✅ 2. Multi-model support
    # - Select appropriate model for task
    # - Provide model selection UI
    # - Handle model-specific features

    # ✅ 3. Natural language processing
    # - Clear system prompts
    # - Context-aware responses
    # - Code extraction reliability

    # ✅ 4. Result visualization
    # - Support multiple output types
    # - Handle different visualization libraries
    # - Provide fallback options

    # ✅ 5. User experience
    # - Progress indicators
    # - Error messages
    # - Interactive model selection

    # ✅ 6. Security
    # - Sandboxed code execution
    # - Input validation
    # - Safe file handling
```

## 🎯 Hướng dẫn Prompt Engineering

### Kiến thức tổng quát

#### **1. System Prompt Design**

- **Role Definition**: "You're a Python data scientist and visualization expert"
- **Context Injection**: Provide dataset path and user query
- **Task Specification**: Clear instructions for code generation
- **Quality Constraints**: Ensure executable, well-formatted code

#### **2. Code Generation Patterns**

```python
# Effective system prompt structure
system_prompt = f"""You're a Python data scientist and data visualization expert.
You are given a dataset at path '{dataset_path}' and also the user's query.

You need to analyze the dataset and answer the user's query with a response
and you run Python code to solve them.

IMPORTANT: Always use the dataset path variable '{dataset_path}' in your code
when reading the CSV file.

Guidelines:
1. Load the dataset using pandas
2. Perform necessary data analysis
3. Create appropriate visualizations
4. Provide statistical insights
5. Answer the user's specific question
6. Ensure all code is executable and well-formatted"""
```

#### **3. Code Extraction Techniques**

````python
# Robust code extraction
def extract_code_blocks(response_text):
    # Multiple patterns for different code block formats
    patterns = [
        r"```python\n(.*?)\n```",
        r"```\n(.*?)\n```",
        r"```py\n(.*?)\n```"
    ]

    for pattern in patterns:
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            return match.group(1).strip()

    return ""
````

#### **4. Error Handling in Code Generation**

```python
# Error handling for AI-generated code
def safe_code_execution(code, code_interpreter):
    try:
        # Validate code before execution
        if not code.strip():
            return None, "No code generated"

        # Execute in sandbox
        exec_result = code_interpreter.run_code(code)

        if exec_result.error:
            return None, f"Execution error: {exec_result.error}"

        return exec_result.results, None

    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
```

## Tính năng

#### **Phân Tích Dữ Liệu Bằng Ngôn Ngữ Tự Nhiên**

- Đặt câu hỏi về dữ liệu bằng tiếng Anh đơn giản
- Nhận visualizations và phân tích thống kê tức thì
- Nhận giải thích về findings và insights
- Hỏi đáp tương tác theo dõi

#### **Lựa Chọn Visualization Thông Minh**

- Tự động chọn loại biểu đồ phù hợp
- Tạo visualization động
- Hỗ trợ visualization thống kê
- Định dạng và styling biểu đồ tùy chỉnh

#### **Hỗ Trợ AI Đa Model**

- Meta-Llama 3.1 405B cho phân tích phức tạp
- DeepSeek V3 cho insights chi tiết
- Qwen 2.5 7B cho phân tích nhanh
- Meta-Llama 3.3 70B cho queries nâng cao

## Cách bắt đầu?

1. **Clone kho lưu trữ GitHub**

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/starter_ai_agents/ai_data_visualisation_agent
```

2. **Cài đặt các dependencies cần thiết:**

```bash
pip install -r requirements.txt
```

3. **Lấy Together AI API Key**

- Đăng ký tài khoản [Together AI](https://api.together.ai/signin) và lấy API key của bạn.
- Mọi người đều nhận được $1 credit miễn phí từ Together AI - AI Acceleration Cloud platform

4. **Lấy E2B API Key**

- Đăng ký tài khoản [E2B](https://e2b.dev/) và lấy API key của bạn.
- Xem hướng dẫn: [E2B Getting Started](https://e2b.dev/docs/legacy/getting-started/api-key)

5. **Chạy ứng dụng Streamlit**

```bash
streamlit run ai_data_visualisation_agent.py
```

## Cách hoạt động?

AI Data Visualization Agent có các thành phần chính:

1. **Data Upload**: Tải lên file CSV và hiển thị preview
2. **Natural Language Query**: Người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên
3. **AI Analysis**: LLM phân tích câu hỏi và tạo Python code
4. **Code Execution**: Code được thực thi trong E2B sandbox
5. **Result Display**: Hiển thị visualizations, charts và insights

## Workflow chi tiết

```
User Upload CSV → Preview Data → Enter Query → AI Generates Code →
Execute in Sandbox → Display Results (Charts/Stats/Insights)
```

## Sử dụng tính năng

1. **Tải lên dataset**: Chọn file CSV từ máy tính
2. **Xem preview**: Kiểm tra dữ liệu trước khi phân tích
3. **Đặt câu hỏi**: Sử dụng ngôn ngữ tự nhiên để hỏi về dữ liệu
4. **Chọn model**: Lựa chọn AI model phù hợp với task
5. **Phân tích**: Nhấn "Analyze" để bắt đầu quá trình
6. **Xem kết quả**: Nhận visualizations, charts và insights

## Ví dụ câu hỏi

- "Can you compare the average cost for two people between different categories?"
- "Show me the distribution of ratings"
- "What are the top 10 most expensive items?"
- "Create a correlation matrix for numerical columns"
- "Show trends over time if there's a date column"

## Lưu ý quan trọng

- **API Keys**: Cần cả Together AI và E2B API keys
- **File Format**: Chỉ hỗ trợ file CSV
- **Code Execution**: Tất cả code được thực thi trong sandbox an toàn
- **Model Selection**: Chọn model phù hợp với độ phức tạp của task
- **Error Handling**: App sẽ hiển thị lỗi nếu có vấn đề với code generation hoặc execution
