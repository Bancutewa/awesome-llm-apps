# 💔 Đội Ngũ Hỗ Trợ Phục Hồi Sau Chia Tay

Đây là một ứng dụng AI được thiết kế để giúp người dùng phục hồi cảm xúc sau khi chia tay bằng cách cung cấp sự hỗ trợ, hướng dẫn và tin nhắn giải tỏa cảm xúc từ một đội ngũ các AI agents chuyên biệt. Ứng dụng được xây dựng sử dụng **Streamlit** và **Agno**, tận dụng **Gemini 2.0 Flash (Google Vision Model)**.

## 🚀 Tính Năng

- 🧠 **Đội Ngũ Multi-Agent:**
  - **Therapist Agent:** Cung cấp sự hỗ trợ đồng cảm và chiến lược đối phó.
  - **Closure Agent:** Viết tin nhắn cảm xúc mà người dùng không nên gửi để giải tỏa.
  - **Routine Planner Agent:** Đề xuất lịch trình hàng ngày để phục hồi cảm xúc.
  - **Brutal Honesty Agent:** Cung cấp phản hồi trực tiếp, không vòng vo về việc chia tay.
- 📷 **Phân Tích Ảnh Chat Screenshot:**
  - Upload ảnh chụp màn hình chat để phân tích.
- 🔑 **Quản Lý API Key:**
  - Lưu trữ và quản lý API key Gemini một cách an toàn qua sidebar của Streamlit.
- ⚡ **Thực Thi Song Song:**
  - Các agents xử lý input theo chế độ phối hợp để có kết quả toàn diện.
- ✅ **Giao Diện Thân Thiện:**
  - Giao diện đơn giản, trực quan với tương tác dễ dàng và hiển thị phản hồi của agents.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **AI Models:** Gemini 2.0 Flash (Google Vision Model)
- **Image Processing:** PIL (để hiển thị screenshots)
- **Text Extraction:** Google's Gemini Vision model để phân tích ảnh chụp màn hình chat
- **Environment Variables:** API keys được quản lý với `st.session_state` trong Streamlit

---

## 📦 Cài Đặt

1. **Clone Repository:**

   ```bash
   git clone <repository_url>
   cd breakup-recovery-agent-team
   ```

2. **Tạo Virtual Environment (Khuyến nghị):**

   ```bash
   conda create --name <env_name> python=<version>
   conda activate <env_name>
   ```

3. **Cài Đặt Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy Streamlit App:**
   ```bash
   streamlit run ai_breakup_recovery_agent.py
   ```

---

## 🔑 Environment Variables

Đảm bảo cung cấp **Gemini API key** trong sidebar của Streamlit:

- GEMINI_API_KEY=your_google_gemini_api_key

---

## 🛠️ Cách Sử Dung

1. **Nhập Cảm Xúc Của Bạn:**
   - Mô tả cảm xúc của bạn trong text area.
2. **Upload Ảnh Screenshot (Tùy Chọn):**
   - Upload ảnh chụp màn hình chat (PNG, JPG, JPEG) để phân tích.
3. **Thực Thi Agents:**
   - Click **"Get Recovery Plan 💝"** để chạy đội ngũ multi-agent.
4. **Xem Kết Quả:**
   - Phản hồi của từng agent được hiển thị riêng biệt.
   - Tóm tắt cuối cùng được cung cấp bởi Team Leader.

---

## 🧑‍💻 Tổng Quan Về Các Agents

- **Therapist Agent**

  - Cung cấp sự hỗ trợ đồng cảm và chiến lược đối phó.
  - Sử dụng **Gemini 2.0 Flash (Google Vision Model)** và DuckDuckGo tools để có insights.

- **Closure Agent**

  - Tạo ra các tin nhắn cảm xúc chưa gửi để giải tỏa cảm xúc.
  - Đảm bảo giọng điệu chân thành và xác thực.

- **Routine Planner Agent**

  - Tạo lịch trình phục hồi hàng ngày với các hoạt động cân bằng.
  - Bao gồm tự suy ngẫm, tương tác xã hội và sự phân tâm lành mạnh.

- **Brutal Honesty Agent**
  - Cung cấp phản hồi trực tiếp, khách quan về việc chia tay.
  - Sử dụng ngôn ngữ thực tế không vòng vo.

---

## 📚 **GIẢI THÍCH CHI TIẾT DỰ ÁN**

### **🎯 Mục đích của dự án:**

Dự án này giúp người dùng xử lý cảm xúc sau khi chia tay thông qua AI, sử dụng 4 agents chuyên biệt với vai trò khác nhau để cung cấp sự hỗ trợ toàn diện.

### **🧠 Kiến trúc Multi-Agent:**

1. **Therapist Agent:** Tập trung vào sự đồng cảm và hỗ trợ cảm xúc
2. **Closure Agent:** Giúp giải tỏa cảm xúc qua việc viết tin nhắn
3. **Routine Planner Agent:** Tạo kế hoạch phục hồi hàng ngày
4. **Brutal Honesty Agent:** Cung cấp góc nhìn thực tế và thẳng thắn

### **🔧 Công nghệ chính:**

- **Agno Framework:** Framework để xây dựng multi-agent system
- **Gemini 2.0 Flash:** Model AI mạnh mẽ hỗ trợ vision và text
- **Streamlit:** Framework UI nhanh cho web app
- **PIL:** Xử lý ảnh cho screenshots

### **⚡ Điểm mạnh của dự án:**

- **Multi-Modal Input:** Hỗ trợ cả text và image analysis
- **Parallel Processing:** Các agents chạy song song
- **Error Handling:** Xử lý lỗi tốt với logging
- **User Experience:** Giao diện thân thiện và intuitive
- **Emotional Intelligence:** AI có khả năng đồng cảm và xử lý cảm xúc

### **📝 Các tính năng nổi bật:**

1. **Emotional Analysis:** Phân tích cảm xúc từ text và hình ảnh
2. **Personalized Support:** Hỗ trợ được cá nhân hóa dựa trên input
3. **Closure Exercises:** Bài tập giúp tìm kiếm sự kết thúc
4. **Recovery Planning:** Lập kế hoạch phục hồi chi tiết
5. **Honest Feedback:** Phản hồi thẳng thắn và xây dựng

### **🎯 PROMPT ENGINEERING - Kiến Thức Chi Tiết**

#### **1. Prompt Architecture Tổng Quan**

##### **A. Two-Level Prompt System**

- **Level 1 - Agent Instructions:** Hướng dẫn cơ bản, định hình tính cách agent
- **Level 2 - Runtime Prompts:** Prompts cụ thể cho từng tác vụ khi chạy

##### **B. Emotional Intelligence Integration**

- **Context Awareness:** Các prompt tích hợp thông tin cảm xúc từ input
- **Multi-Modal Processing:** Xử lý cả text và image trong cùng prompt
- **Personalization:** Tùy chỉnh phản hồi dựa trên trạng thái người dùng

#### **2. Chi Tiết Instructions Mỗi Agent**

##### **A. Therapist Agent - Instructions**

```python
instructions=[
    "You are an empathetic therapist that:",
    "1. Listens with empathy and validates feelings",
    "2. Uses gentle humor to lighten the mood",
    "3. Shares relatable breakup experiences",
    "4. Offers comforting words and encouragement",
    "5. Analyzes both text and image inputs for emotional context",
    "Be supportive and understanding in your responses"
]
```

**📋 Dịch sang tiếng Việt:**

- Bạn là một chuyên gia trị liệu giàu sự đồng cảm:
  1. Lắng nghe với sự đồng cảm và xác nhận cảm xúc
  2. Dùng chút hài hước nhẹ nhàng để giảm căng thẳng
  3. Chia sẻ những trải nghiệm chia tay có thể đồng cảm
  4. Đưa ra lời an ủi và khích lệ
  5. Phân tích cả văn bản và hình ảnh để hiểu bối cảnh cảm xúc
     Hãy hỗ trợ và thấu hiểu trong mọi phản hồi

##### **B. Closure Agent - Instructions**

```python
instructions=[
    "You are a closure specialist that:",
    "1. Creates emotional messages for unsent feelings",
    "2. Helps express raw, honest emotions",
    "3. Formats messages clearly with headers",
    "4. Ensures tone is heartfelt and authentic",
    "Focus on emotional release and closure"
]
```

**📋 Dịch sang tiếng Việt:**

- Bạn là chuyên gia giúp khép lại cảm xúc:
  1. Tạo các tin nhắn cảm xúc để giải tỏa (nhưng không gửi)
  2. Giúp thể hiện cảm xúc chân thật, nguyên vẹn
  3. Định dạng thông điệp rõ ràng với tiêu đề
  4. Đảm bảo giọng điệu chân thành và xác thực
     Tập trung vào giải tỏa cảm xúc và tìm sự khép lại

##### **C. Routine Planner Agent - Instructions**

```python
instructions=[
    "You are a recovery routine planner that:",
    "1. Designs 7-day recovery challenges",
    "2. Includes fun activities and self-care tasks",
    "3. Suggests social media detox strategies",
    "4. Creates empowering playlists",
    "Focus on practical recovery steps"
]
```

**📋 Dịch sang tiếng Việt:**

- Bạn là người lập kế hoạch phục hồi:
  1. Thiết kế thử thách phục hồi 7 ngày
  2. Bao gồm hoạt động vui vẻ và chăm sóc bản thân
  3. Gợi ý chiến lược "detox" mạng xã hội
  4. Tạo danh sách phát (playlist) truyền cảm hứng
     Tập trung vào các bước phục hồi thực tiễn

##### **D. Brutal Honesty Agent - Instructions**

```python
instructions=[
    "You are a direct feedback specialist that:",
    "1. Gives raw, objective feedback about breakups",
    "2. Explains relationship failures clearly",
    "3. Uses blunt, factual language",
    "4. Provides reasons to move forward",
    "Focus on honest insights without sugar-coating"
]
```

**📋 Dịch sang tiếng Việt:**

- Bạn là chuyên gia phản hồi thẳng thắn:
  1. Đưa ra phản hồi thẳng, khách quan về việc chia tay
  2. Giải thích rõ ràng vì sao mối quan hệ đổ vỡ
  3. Dùng ngôn ngữ trực diện, dựa trên sự thật
  4. Đưa ra lý do để bước tiếp
     Tập trung vào góc nhìn trung thực, không "đường mật"

#### **3. Runtime Prompts - Phân Tích Chi Tiết**

##### **A. Therapist Analysis Prompt**

```python
therapist_prompt = f"""
Analyze the emotional state and provide empathetic support based on:
User's message: {user_input}

Please provide a compassionate response with:
1. Validation of feelings
2. Gentle words of comfort
3. Relatable experiences
4. Words of encouragement
"""
```

**🔍 Phân tích ý nghĩa:**

- **Context Integration:** Sử dụng {user_input} để cá nhân hóa
- **Structured Response:** 4 điểm yêu cầu cụ thể
- **Emotional Focus:** Tập trung vào validation và comfort
- **Therapeutic Approach:** Áp dụng phương pháp trị liệu chuyên nghiệp

##### **B. Closure Messages Prompt**

```python
closure_prompt = f"""
Help create emotional closure based on:
User's feelings: {user_input}

Please provide:
1. Template for unsent messages
2. Emotional release exercises
3. Closure rituals
4. Moving forward strategies
"""
```

**🔍 Phân tích ý nghĩa:**

- **Emotional Release:** Tập trung giải tỏa cảm xúc
- **Practical Tools:** Cung cấp template và bài tập
- **Closure Process:** Hướng dẫn từng bước khép lại
- **Future Orientation:** Chiến lược để bước tiếp

##### **C. Recovery Plan Prompt**

```python
routine_prompt = f"""
Design a 7-day recovery plan based on:
Current state: {user_input}

Include:
1. Daily activities and challenges
2. Self-care routines
3. Social media guidelines
4. Mood-lifting music suggestions
"""
```

**🔍 Phân tích ý nghĩa:**

- **Time-Bound:** Kế hoạch 7 ngày cụ thể
- **Comprehensive:** Bao quát nhiều khía cạnh phục hồi
- **Practical:** Hoạt động và thói quen thực tế
- **Engaging:** Gợi ý âm nhạc để nâng tâm trạng

##### **D. Honest Feedback Prompt**

```python
honesty_prompt = f"""
Provide honest, constructive feedback about:
Situation: {user_input}

Include:
1. Objective analysis
2. Growth opportunities
3. Future outlook
4. Actionable steps
"""
```

**🔍 Phân tích ý nghĩa:**

- **Honesty First:** Ưu tiên trung thực
- **Constructive:** Kết hợp với tính xây dựng
- **Forward-Looking:** Tập trung vào tương lai
- **Action-Oriented:** Đề xuất bước cụ thể

#### **4. Cách Các Prompts Kết Hợp Với Nhau**

##### **A. Sequential Processing Logic**

```
Input User → Parallel Processing → Coordinated Output
    ↓              ↓                      ↓
[user_input] → [4 Agents] → [4 Responses]
```

##### **B. Information Flow**

1. **Input Processing:** User input được truyền vào tất cả agents
2. **Parallel Execution:** 4 agents xử lý đồng thời
3. **Context Sharing:** Tất cả agents nhận cùng context
4. **Independent Output:** Mỗi agent tạo response riêng
5. **Final Display:** Hiển thị tất cả responses cùng lúc

##### **C. Emotional Context Preservation**

```python
# Tất cả agents nhận cùng input
all_agents_input = user_input

# Mỗi agent xử lý từ góc nhìn khác nhau
therapist_response = therapist_agent.run(therapist_prompt)
closure_response = closure_agent.run(closure_prompt)
routine_response = routine_planner_agent.run(routine_prompt)
honesty_response = brutal_honesty_agent.run(honesty_prompt)
```

#### **5. Best Practices Học Được**

##### **A. Prompt Design Patterns**

1. **Context-First:** Luôn đặt context người dùng lên đầu
2. **Structured Output:** Sử dụng danh sách để định dạng response
3. **Emotional Intelligence:** Cân bằng giữa đồng cảm và thực tế
4. **Actionable Results:** Cung cấp bước cụ thể để thực hiện

##### **B. Multi-Agent Coordination**

1. **Role Specialization:** Mỗi agent có vai trò riêng biệt
2. **Complementary Perspectives:** Các góc nhìn bổ sung nhau
3. **Parallel Processing:** Tăng hiệu quả và tốc độ
4. **Consistent Context:** Đảm bảo tất cả agents hiểu vấn đề giống nhau

##### **C. Error Handling in Prompts**

```python
# Graceful degradation
try:
    response = agent.run(prompt, images=all_images)
except Exception as e:
    logger.error(f"Agent error: {e}")
    st.error("Unable to process request. Please try again.")
```

#### **6. Template Cho Dự Án Tương Lai**

##### **A. Emotional Support Agent Template**

```python
def create_emotional_support_agent():
    agent = Agent(
        name="Emotional Support Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=[
            "You are a supportive AI assistant that:",
            "1. Validates user emotions",
            "2. Provides gentle guidance",
            "3. Suggests healthy coping strategies",
            "4. Maintains professional boundaries",
            "Focus on empathy and practical help"
        ],
        markdown=True
    )
    return agent
```

##### **B. Multi-Perspective Analysis Template**

```python
def analyze_with_multiple_perspectives(user_input):
    """Template for multi-agent emotional analysis"""

    # Define different perspectives
    perspectives = {
        "empathetic": create_empathetic_agent(),
        "practical": create_practical_agent(),
        "honest": create_honest_agent(),
        "creative": create_creative_agent()
    }

    results = {}
    for perspective, agent in perspectives.items():
        prompt = f"Analyze from {perspective} perspective: {user_input}"
        response = agent.run(prompt)
        results[perspective] = response

    return results
```

#### **7. Performance Optimization**

##### **A. Token Management**

- **Input Limits:** Giới hạn độ dài input để tránh vượt token
- **Response Structure:** Định dạng response để tối ưu token usage
- **Context Preservation:** Giữ context quan trọng, loại bỏ không cần thiết

##### **B. Processing Efficiency**

- **Parallel Execution:** Chạy agents song song thay vì tuần tự
- **Batch Processing:** Xử lý multiple images cùng lúc
- **Caching:** Cache responses cho inputs tương tự

##### **C. User Experience**

- **Progress Indicators:** Hiển thị tiến trình với st.spinner
- **Error Messages:** Thông báo lỗi thân thiện và actionable
- **Fallback Options:** Có kế hoạch dự phòng khi agent thất bại

### **🚀 Cách chạy dự án:**

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run ai_breakup_recovery_agent.py
```

### **🔑 API Keys cần thiết:**

- **Gemini API Key:** Từ Google AI Studio

### **📚 Tổng Kết Kiến Thức Prompt Engineering**

#### **🎯 Những Bài Học Chính:**

1. **Two-Level Prompt System:** Instructions cơ bản + Runtime prompts cụ thể
2. **Emotional Intelligence:** AI có thể xử lý cảm xúc với sự tinh tế
3. **Multi-Agent Coordination:** Các agents bổ sung nhau tạo ra góc nhìn toàn diện
4. **Context Preservation:** Duy trì context cảm xúc xuyên suốt quá trình
5. **Structured Output:** Định dạng response để dễ đọc và actionable

#### **🛠️ Template Sử Dụng Lại:**

```python
# Template cho Multi-Agent Emotional Support System
def create_multi_agent_emotional_support():
    agents = {
        "therapist": create_emotional_agent(),
        "planner": create_practical_agent(),
        "advisor": create_honest_agent(),
        "coach": create_motivational_agent()
    }

    def process_emotional_request(user_input, images=None):
        results = {}
        for role, agent in agents.items():
            prompt = create_role_specific_prompt(role, user_input)
            response = agent.run(prompt, images=images)
            results[role] = response
        return results

    return process_emotional_request
```

#### **🚀 Ứng Dụng Thực Tế:**

- **Mental Health Support:** Hỗ trợ sức khỏe tinh thần
- **Crisis Intervention:** Can thiệp khủng hoảng cảm xúc
- **Personal Development:** Phát triển EQ cá nhân
- **Relationship Counseling:** Tư vấn mối quan hệ

---

## 📄 License

Dự án này được cấp phép theo **MIT License**.

---
