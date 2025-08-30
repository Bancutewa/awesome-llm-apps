# 🛫 AI Travel Agent

Ứng dụng Streamlit này là một AI Travel Agent được hỗ trợ bởi AI, tạo ra các lịch trình du lịch cá nhân hóa bằng cách sử dụng Groq LLM. Nó tự động hóa quá trình nghiên cứu, lập kế hoạch và tổ chức kỳ nghỉ mơ ước của bạn, cho phép bạn khám phá các điểm đến thú vị một cách dễ dàng.

## 🎯 Kiến Thức Đã Học Được

### **1. Kiến Thức Tổng Quát**

#### **A. Multi-Agent Architecture Pattern**

- **Khái niệm**: Chia nhỏ task phức tạp thành nhiều agent chuyên biệt
- **Lợi ích**: Tăng hiệu quả, giảm độ phức tạp, dễ maintain
- **Pattern**: `Input → Agent 1 (Research) → Results → Agent 2 (Plan) → Output`

#### **B. Token Management & API Limits**

- **Vấn đề**: Mỗi LLM provider có giới hạn token khác nhau
- **Groq Free Tier**: 6000 tokens/phút
- **Giải pháp**: Chọn model phù hợp, tối ưu prompt, giảm context

#### **C. Error Handling & User Experience**

- **Graceful Degradation**: App vẫn hoạt động khi thiếu API keys
- **User Feedback**: Progress indicators, error messages rõ ràng
- **Input Validation**: Kiểm tra dữ liệu trước khi xử lý

#### **D. Internationalization (i18n)**

- **Localization**: Dịch UI và prompts sang tiếng Việt
- **Cultural Adaptation**: Điều chỉnh nội dung phù hợp văn hóa
- **User Experience**: Giao diện thân thiện với người dùng Việt Nam

### **2. Ví Dụ Từ Code**

#### **A. Multi-Agent System Implementation**

```python
# Agent 1: Researcher - Tìm kiếm thông tin
researcher = Agent(
    name="Researcher",
    role="Searches for travel destinations, activities, and accommodations",
    model=Groq(id="llama3-8b-8192", api_key=api_key),
    description="""Bạn là một nhà nghiên cứu du lịch hàng đầu thế giới...""",
    instructions=[
        "Khi nhận được điểm đến du lịch và số ngày...",
        "Đối với mỗi từ khóa tìm kiếm, hãy sử dụng `search_google`...",
        "Từ kết quả của tất cả các tìm kiếm, trả về 10 kết quả...",
    ],
    tools=[SerpApiTools(api_key=serp_api_key)],
)

# Agent 2: Planner - Tạo lịch trình
planner = Agent(
    name="Planner",
    role="Generates a draft itinerary based on research results",
    model=Groq(id="llama3-8b-8192", api_key=api_key),
    description="""Bạn là một nhà lập kế hoạch du lịch chuyên nghiệp...""",
    instructions=[
        "Tạo lịch trình du lịch chi tiết với các hoạt động...",
        "Đảm bảo lịch trình được cấu trúc tốt...",
        "Tất cả nội dung phải được viết bằng tiếng Việt...",
    ],
)
```

#### **B. Token Optimization Techniques**

```python
# ❌ Model lớn - tốn nhiều tokens
model=Groq(id="deepseek-r1-distill-llama-70b", api_key=api_key)

# ✅ Model nhỏ - tiết kiệm tokens
model=Groq(id="llama3-8b-8192", api_key=api_key)

# ❌ Prompt dài và phức tạp
description="""You are a world-class travel researcher. Given a travel destination and the number of days the user wants to travel for, generate a list of search terms for finding relevant travel activities and accommodations. Then search the web for each term, analyze the results, and return the 10 most relevant results."""

# ✅ Prompt ngắn gọn và hiệu quả
description="""Bạn là một nhà nghiên cứu du lịch hàng đầu thế giới. Khi nhận được điểm đến du lịch và số ngày du lịch của người dùng, hãy tạo ra danh sách các từ khóa tìm kiếm để tìm các hoạt động du lịch và chỗ ở phù hợp."""
```

#### **C. Error Handling & UX Patterns**

```python
# Graceful degradation - luôn hiển thị UI
st.title("🤖 AI Travel Planner")
st.caption("Lập kế hoạch chuyến đi mơ ước với AI Travel Planner...")

# Input validation
if st.button("🎯 Tạo lịch trình"):
    if destination:  # Kiểm tra input
        # Thực hiện logic
    else:
        st.error("Please enter a destination first!")

# Progress indicators
with st.spinner("🔍 Đang nghiên cứu điểm đến..."):
    research_results = researcher.run(prompt, stream=False)
```

#### **D. Internationalization Implementation**

```python
# UI localization
destination = st.text_input("Bạn muốn đi đâu?")
num_days = st.number_input("Bạn muốn đi bao nhiêu ngày?", min_value=1, max_value=30, value=7)

# Prompt localization
prompt = f"""
Điểm đến: {destination}
Thời lượng: {num_days} ngày
Kết quả nghiên cứu: {research_results.content}

Hãy tạo lịch trình du lịch chi tiết bằng tiếng Việt dựa trên kết quả nghiên cứu này.
Đảm bảo lịch trình hấp dẫn, thực tế và phù hợp với văn hóa Việt Nam.
"""

# Instructions localization
instructions=[
    "Tất cả kết quả trả về phải được trình bày bằng tiếng Việt.",
    "Tất cả nội dung phải được viết bằng tiếng Việt một cách tự nhiên và thân thiện.",
]
```

### **3. Tổng Hợp Cách Sử Dụng Cho Sau Này**

#### **A. Template Multi-Agent System**

```python
# Template cơ bản cho multi-agent system
def create_multi_agent_system():
    # Agent 1: Research/Extract
    researcher = Agent(
        name="Researcher",
        role="Brief role description",
        model=Groq(id="llama3-8b-8192", api_key=api_key),
        description="""You are a [ROLE]. Given [INPUT], [GOAL].""",
        instructions=[
            "Step 1: Do specific task...",
            "Step 2: Process results...",
            "Remember: [Quality constraint]...",
        ],
        tools=[...],
    )

    # Agent 2: Process/Create
    processor = Agent(
        name="Processor",
        role="Process research results",
        model=Groq(id="llama3-8b-8192", api_key=api_key),
        description="""You are a [ROLE]. Process [INPUT] to create [OUTPUT].""",
        instructions=[
            "Process the research results...",
            "Create structured output...",
            "Ensure quality and accuracy...",
        ],
    )

    return researcher, processor

# Usage pattern
def run_workflow(input_data):
    # Step 1: Research
    research_results = researcher.run(f"Research {input_data}")

    # Step 2: Process
    final_output = processor.run(f"""
    Input: {input_data}
    Research: {research_results.content}

    Process this information to create the final output.
    """)

    return final_output
```

#### **B. Token Optimization Checklist**

```python
# ✅ Token optimization checklist
def optimize_for_tokens():
    # 1. Choose appropriate model size
    model = Groq(id="llama3-8b-8192")  # Smaller model

    # 2. Keep prompts concise
    description = "Brief, clear description"
    instructions = [
        "Short, specific instruction 1",
        "Short, specific instruction 2",
    ]

    # 3. Limit context length
    max_context_length = 4000  # tokens

    # 4. Use streaming for long responses
    response = agent.run(prompt, stream=True)

    # 5. Implement retry logic
    try:
        result = agent.run(prompt)
    except TokenLimitError:
        # Reduce prompt size and retry
        simplified_prompt = simplify_prompt(prompt)
        result = agent.run(simplified_prompt)
```

#### **C. Error Handling Template**

```python
# Error handling template
def robust_agent_execution(agent, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            with st.spinner(f"Processing... (Attempt {attempt + 1})"):
                result = agent.run(prompt, stream=False)
                return result
        except TokenLimitError as e:
            st.warning(f"Token limit exceeded: {e}")
            # Reduce prompt size
            prompt = reduce_prompt_size(prompt)
        except APIError as e:
            st.error(f"API Error: {e}")
            if attempt == max_retries - 1:
                st.error("Failed after multiple attempts")
                return None
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return None
```

#### **D. Internationalization Template**

```python
# i18n template
class LocalizedAgent:
    def __init__(self, language="vi"):
        self.language = language
        self.translations = {
            "vi": {
                "title": "🤖 AI Travel Planner",
                "destination": "Bạn muốn đi đâu?",
                "days": "Bạn muốn đi bao nhiêu ngày?",
                "generate": "🎯 Tạo lịch trình",
                "researching": "🔍 Đang nghiên cứu điểm đến...",
                "planning": "📝 Đang tạo lịch trình cá nhân hóa...",
            },
            "en": {
                "title": "🤖 AI Travel Planner",
                "destination": "Where do you want to go?",
                "days": "How many days do you want to travel?",
                "generate": "🎯 Generate Itinerary",
                "researching": "🔍 Researching destination...",
                "planning": "📝 Creating personalized itinerary...",
            }
        }

    def get_text(self, key):
        return self.translations.get(self.language, {}).get(key, key)

    def create_localized_prompt(self, base_prompt, **kwargs):
        if self.language == "vi":
            return f"""
            {base_prompt}

            Yêu cầu: Tất cả nội dung phải được viết bằng tiếng Việt.
            Văn hóa: Phù hợp với văn hóa và phong tục Việt Nam.
            """
        return base_prompt
```

#### **E. Best Practices Summary**

```python
# Best practices checklist
def apply_best_practices():
    # ✅ 1. Multi-agent architecture
    # - Separate concerns
    # - Clear input/output between agents
    # - Modular design

    # ✅ 2. Token management
    # - Choose appropriate model size
    # - Optimize prompts
    # - Implement retry logic

    # ✅ 3. Error handling
    # - Graceful degradation
    # - User-friendly error messages
    # - Input validation

    # ✅ 4. Internationalization
    # - Localize UI elements
    # - Adapt content for culture
    # - Support multiple languages

    # ✅ 5. User experience
    # - Progress indicators
    # - Clear instructions
    # - Responsive design

    # ✅ 6. Code organization
    # - Clean, readable code
    # - Proper documentation
    # - Reusable components
```

## 🎯 Hướng dẫn Prompt Engineering

### Kiến thức tổng quát

#### **1. Các cấp độ Prompt**

- **Level 0**: Basic prompt - "Tell me about Paris"
- **Level 1**: Context - "Tell me about Paris as a travel destination for 5 days"
- **Level 2**: Role - "You are a travel expert. Tell me about Paris..."
- **Level 3**: Instructions - "Step by step guide for Paris trip"
- **Level 4**: Multi-step - "Research → Plan → Optimize"
- **Level 5**: Meta-cognitive - "Think about how to approach this task"

#### **2. Các kỹ thuật cơ bản**

- **Role-based**: "You are a [ROLE]"
- **Task-specific**: "Given [INPUT], do [TASK]"
- **Step-by-step**: "First do X, then Y, finally Z"
- **Quality constraints**: "Ensure [QUALITY], never [BAD]"
- **Context injection**: Provide relevant data
- **Output formatting**: Specify format/structure

#### **3. Best Practices**

- **Clear & Specific**: Avoid ambiguity
- **Structured**: Use bullet points, numbered lists
- **Context-aware**: Include relevant information
- **Quality-focused**: Add constraints and guardrails
- **Iterative**: Test and refine prompts
- **Modular**: Break complex tasks into steps

#### **4. Common Patterns**

```
"You are a [EXPERT]. Given [CONTEXT], [TASK].
Follow these steps:
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]

Constraints:
- [QUALITY RULE 1]
- [QUALITY RULE 2]
- Never [PROHIBITED ACTION]

Output format: [SPECIFY FORMAT]
```

### Áp dụng trong AI Travel Agent

#### **Description vs Instructions**

| Aspect       | Description                     | Instructions                   |
| ------------ | ------------------------------- | ------------------------------ |
| **Mục đích** | Định hình personality & vai trò | Hướng dẫn cụ thể cách làm việc |
| **Độ dài**   | Ngắn gọn (2-3 câu)              | Chi tiết, step-by-step         |
| **Nội dung** | "Bạn là ai?"                    | "Bạn làm gì?"                  |
| **Style**    | Narrative, descriptive          | Directive, prescriptive        |
| **Focus**    | Role & expertise                | Process & quality              |

#### **Ví dụ thực tế trong code:**

**Researcher Agent:**

```python
description="""Bạn là một nhà nghiên cứu du lịch hàng đầu thế giới. Khi nhận được điểm đến du lịch và số ngày du lịch của người dùng, hãy tạo ra danh sách các từ khóa tìm kiếm để tìm các hoạt động du lịch và chỗ ở phù hợp. Sau đó tìm kiếm trên web cho từng từ khóa, phân tích kết quả, và trả về 10 kết quả liên quan nhất. Tất cả thông tin phải được trình bày bằng tiếng Việt."""

instructions=[
    "Khi nhận được điểm đến du lịch và số ngày du lịch của người dùng, trước tiên hãy tạo ra danh sách 3 từ khóa tìm kiếm liên quan đến điểm đến đó và số ngày.",
    "Đối với mỗi từ khóa tìm kiếm, hãy sử dụng `search_google` và phân tích kết quả. Ưu tiên tìm kiếm thông tin bằng tiếng Việt.",
    "Từ kết quả của tất cả các tìm kiếm, trả về 10 kết quả liên quan nhất với sở thích của người dùng.",
    "Hãy nhớ: chất lượng của kết quả rất quan trọng.",
    "Tất cả kết quả trả về phải được trình bày bằng tiếng Việt.",
]
```

**Planner Agent:**

```python
description="""Bạn là một nhà lập kế hoạch du lịch chuyên nghiệp. Dựa trên điểm đến, số ngày du lịch và kết quả nghiên cứu, hãy tạo ra lịch trình du lịch chi tiết bao gồm các hoạt động và chỗ ở được đề xuất. Tất cả nội dung phải được trình bày bằng tiếng Việt một cách tự nhiên và hấp dẫn."""

instructions=[
    "Tạo lịch trình du lịch chi tiết với các hoạt động và chỗ ở được đề xuất.",
    "Đảm bảo lịch trình được cấu trúc tốt, thông tin và hấp dẫn.",
    "Đảm bảo cung cấp lịch trình đa dạng và cân bằng, trích dẫn sự thật khi có thể.",
    "Hãy nhớ: chất lượng của lịch trình rất quan trọng.",
    "Tập trung vào sự rõ ràng, mạch lạc và chất lượng tổng thể.",
    "Không bao giờ bịa đặt sự thật hoặc đạo văn. Luôn trích dẫn nguồn gốc khi cần thiết.",
    "Tất cả nội dung phải được viết bằng tiếng Việt một cách tự nhiên và thân thiện.",
]
```

#### **Context Injection Pattern:**

```python
prompt = f"""
Điểm đến: {destination}
Thời lượng: {num_days} ngày
Kết quả nghiên cứu: {research_results.content}

Hãy tạo lịch trình du lịch chi tiết bằng tiếng Việt dựa trên kết quả nghiên cứu này.
Đảm bảo lịch trình hấp dẫn, thực tế và phù hợp với văn hóa Việt Nam.
"""
```

### Template để tái sử dụng

#### **Template cơ bản cho Agent:**

```python
agent = Agent(
    name="AgentName",
    role="Brief role description",
    description="""You are a [ROLE]. Given [INPUT], [GOAL].""",
    instructions=[
        "Step 1: Do something specific...",
        "Step 2: Process the results...",
        "Remember: [Quality constraint]...",
        "Never [Prohibited action]..."
    ],
    tools=[...],
)
```

#### **Template cho Multi-Agent System:**

```
User Input → Agent 1 (Research/Extract) → Results → Agent 2 (Process/Create) → Final Output
```

#### **Template cho Quality Guardrails:**

```python
instructions=[
    "Remember: the quality of the results is important.",
    "Never make up facts or plagiarize.",
    "Always provide proper attribution.",
    "Focus on clarity, coherence, and overall quality.",
    "Ensure output is well-structured and informative."
]
```

### Các kỹ thuật nâng cao

#### **1. Task Decomposition**

- Chia nhỏ task phức tạp thành các bước đơn giản
- Mỗi step có input/output rõ ràng
- Chain các steps lại với nhau

#### **2. Chain-of-Thought**

```python
"Think step-by-step:
1. Understand the user's requirements
2. Break down the task into components
3. Execute each component systematically
4. Validate results
5. Present final output"
```

#### **3. Self-Reflection**

```python
"After completing the task, review your work:
- Did you follow all instructions?
- Is the quality satisfactory?
- Are there any improvements needed?"
```

#### **4. Output Formatting**

```python
"Format your response as:
## Section 1
- Point 1
- Point 2

## Section 2
- Point 1
- Point 2"
```

## Tính năng

- Nghiên cứu và khám phá các điểm đến du lịch, hoạt động và chỗ ở thú vị
- Tùy chỉnh lịch trình của bạn dựa trên số ngày bạn muốn đi du lịch
- Sử dụng sức mạnh của Groq LLM để tạo ra các kế hoạch du lịch thông minh và cá nhân hóa
- Tải xuống lịch trình của bạn dưới dạng file lịch (.ics) để nhập vào Google Calendar, Apple Calendar, hoặc các ứng dụng lịch khác
- Giao diện hoàn toàn bằng tiếng Việt, phù hợp với văn hóa Việt Nam

## Cách bắt đầu?

1. Clone kho lưu trữ GitHub

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/starter_ai_agents/ai_travel_agent
```

2. Cài đặt các dependencies cần thiết:

```bash
pip install -r requirements.txt
```

3. Lấy Groq API Key của bạn

- Đăng ký tài khoản [Groq](https://console.groq.com/) và lấy API key của bạn.

4. Lấy SerpAPI Key của bạn

- Đăng ký tài khoản [SerpAPI](https://serpapi.com/) và lấy API key của bạn.

5. Chạy ứng dụng Streamlit

```bash
streamlit run travel_agent.py
```

## Cách hoạt động?

AI Travel Agent có hai thành phần chính:

- **Researcher (Người Nghiên Cứu)**: Chịu trách nhiệm tạo ra các từ khóa tìm kiếm dựa trên điểm đến và thời gian du lịch của người dùng, và tìm kiếm trên web các hoạt động và chỗ ở liên quan bằng cách sử dụng SerpAPI.

- **Planner (Người Lập Kế Hoạch)**: Lấy kết quả nghiên cứu và sở thích của người dùng để tạo ra bản nháp lịch trình cá nhân hóa bao gồm các hoạt động được đề xuất, lựa chọn ăn uống và chỗ ở.

## Sử dụng tính năng tải xuống lịch

Sau khi tạo lịch trình du lịch của bạn:

1. Nhấp vào nút "📅 Tải lịch trình (.ics)" xuất hiện bên cạnh nút "🎯 Tạo lịch trình"
2. Lưu file .ics vào máy tính của bạn
3. Nhập file vào ứng dụng lịch ưa thích của bạn (Google Calendar, Apple Calendar, Outlook, v.v.)
4. Mỗi ngày của lịch trình sẽ xuất hiện dưới dạng sự kiện cả ngày trong lịch của bạn
5. Chi tiết hoàn chỉnh cho các hoạt động trong ngày được bao gồm trong mô tả sự kiện

Tính năng này giúp dễ dàng theo dõi kế hoạch du lịch của bạn và có lịch trình có sẵn trên tất cả thiết bị của bạn, ngay cả khi offline.

## Phiên bản cục bộ vs đám mây

- **travel_agent.py**: Sử dụng Groq LLM để có các lịch trình chất lượng cao (yêu cầu Groq API key)
- **local_travel_agent.py**: Sử dụng Ollama để suy luận LLM cục bộ mà không gửi dữ liệu đến các API bên ngoài (yêu cầu Ollama được cài đặt và chạy)
