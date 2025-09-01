## 📰 ➡️ 🎙️ AI Agent Chuyển Đổi Blog Thành Podcast

Đây là một ứng dụng Streamlit cho phép người dùng chuyển đổi bất kỳ bài blog nào thành podcast. Ứng dụng sử dụng Groq LLM để tóm tắt, Firecrawl để thu thập nội dung blog, và API ElevenLabs để tạo âm thanh. Người dùng chỉ cần nhập URL blog, và ứng dụng sẽ tạo ra một tập podcast dựa trên nội dung blog đó.

## 🎯 Kiến Thức Đã Học Được

### **1. Kiến Thức Tổng Quát**

#### **A. Single-Agent với Multi-Tools Architecture**

- **Khái niệm**: Một agent duy nhất sử dụng nhiều tools chuyên biệt
- **Lợi ích**: Đơn giản hóa workflow, dễ quản lý, phù hợp với tasks tuyến tính
- **Pattern**: `Input → Agent (with tools) → Multi-modal Output`

#### **B. Multi-Modal Output Processing**

- **Text Processing**: LLM tạo tóm tắt từ nội dung web
- **Audio Generation**: ElevenLabs chuyển text thành speech
- **File Management**: Xử lý file âm thanh, base64 encoding/decoding

#### **C. Voice Selection & Audio Quality**

- **ElevenLabs Models**: `eleven_turbo_v2_5`, `eleven_multilingual_v2`
- **Voice IDs**: Mỗi giọng có ID riêng, hỗ trợ đa ngôn ngữ
- **Audio Formats**: WAV, MP3 với chất lượng cao

#### **D. Web Scraping Integration**

- **Firecrawl API**: Thu thập nội dung từ URL
- **Content Processing**: Parse HTML, extract text
- **Error Handling**: Xử lý URL không hợp lệ, network issues

### **2. Ví Dụ Từ Code**

#### **A. Single-Agent với Multi-Tools Implementation**

```python
# Single Agent với nhiều tools
blog_to_podcast_agent = Agent(
    name="Blog to Podcast Agent",
    agent_id="blog_to_podcast_agent",
  model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
    tools=[
        ElevenLabsTools(
            voice_id=VOICE_OPTIONS[selected_voice],
            model_id="eleven_turbo_v2_5",
            target_directory="audio_generations",
            api_key=elevenlabs_api_key,
        ),
        FirecrawlTools(api_key=firecrawl_api_key),
    ],
    description="You are an AI agent that can generate audio using the ElevenLabs API.",
    instructions=[
        "When the user provides a blog URL:",
        "1. Use FirecrawlTools to scrape the blog content",
        "2. Create a concise summary of the blog content that is NO MORE than 3000 characters long",
        "3. The summary should capture the main points while being engaging and conversational",
        "4. Use the ElevenLabsTools to convert the summary to audio",
        "Ensure the summary is within the 3000 character limit to avoid ElevenLabs API limits",
    ],
    markdown=True,
    debug_mode=True,
)
```

#### **B. Voice Selection System**

```python
# Dictionary chứa các giọng nói
VOICE_OPTIONS = {
    # Vietnamese Voices
    "Nguyễn Ngân (Female, Vietnamese)": "DvG3I1kDzdBY3u4EzYh6",
    "Nhật Phong (Male, Vietnamese)": "RxhjHDfpO54FYotYtKpw",

    # International Voices
    "Rachel (Female, American)": "21m00Tcm4TlvDq8ikWAM",
    "Drew (Male, American)": "29vD33N1CtxCmqQRPOHJ",
}

# Streamlit selectbox
selected_voice = st.selectbox(
    "🎤 Choose Voice:",
    options=list(VOICE_OPTIONS.keys()),
    index=list(VOICE_OPTIONS.keys()).index("Nguyễn Ngân (Female, Vietnamese)"),
    help="Select the voice for your podcast"
)

# Sử dụng voice đã chọn
voice_id=VOICE_OPTIONS[selected_voice]
```

#### **C. Audio Processing & File Management**

```python
# Audio generation response
podcast: RunResponse = blog_to_podcast_agent.run(
    f"Convert the blog content to a podcast: {url}"
)

# File handling
if podcast.audio and len(podcast.audio) > 0:
    filename = f"{save_dir}/podcast_{uuid4()}.wav"
    write_audio_to_file(
        audio=podcast.audio[0].base64_audio,
        filename=filename
    )

    # Streamlit audio player
    audio_bytes = open(filename, "rb").read()
    st.audio(audio_bytes, format="audio/wav")

    # Download button
    st.download_button(
        label="Download Podcast",
        data=audio_bytes,
        file_name="generated_podcast.wav",
        mime="audio/wav"
    )
```

#### **D. Environment & API Key Management**

```python
# Load từ .env file
groq_api_key = os.getenv("GROQ_API_KEY")
elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

# Validation
keys_provided = all([groq_api_key, elevenlabs_api_key, firecrawl_api_key])

# Set environment variables cho Agno
os.environ["GROQ_API_KEY"] = groq_api_key
os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
```

### **3. Tổng Hợp Cách Sử Dụng Cho Sau Này**

#### **A. Template Single-Agent với Multi-Tools**

```python
def create_content_processor_agent():
    # Single agent với multiple tools
    agent = Agent(
        name="Content Processor",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        tools=[
            # Tool 1: Content extraction
            WebScrapingTool(api_key=scraping_key),

            # Tool 2: Content processing
            ProcessingTool(api_key=processing_key),

            # Tool 3: Output generation
            OutputTool(api_key=output_key),
        ],
        description="""You are a content processor that extracts, processes, and generates outputs.""",
        instructions=[
            "Step 1: Extract content from input source",
            "Step 2: Process and transform content",
            "Step 3: Generate final output",
            "Quality constraint: Ensure output meets requirements",
        ],
        markdown=True,
        debug_mode=True,
    )
    return agent
```

#### **B. Voice Selection Template**

```python
def create_voice_selector():
    # Voice options dictionary
    VOICE_OPTIONS = {
        "Language_Group": {
            "Voice1": "voice_id_1",
            "Voice2": "voice_id_2",
        }
    }

    # Streamlit UI
    selected_voice = st.selectbox(
        "Select Voice:",
        options=list(VOICE_OPTIONS.keys()),
        index=0,
        help="Choose appropriate voice for content"
    )

    return VOICE_OPTIONS[selected_voice]

# Usage
voice_id = create_voice_selector()
audio_tool = AudioTool(voice_id=voice_id)
```

#### **C. Audio Processing Template**

```python
def process_audio_response(response, output_dir="audio_outputs"):
    """Template for handling audio generation responses"""

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    if response.audio and len(response.audio) > 0:
        # Generate unique filename
        filename = f"{output_dir}/audio_{uuid4()}.wav"

        # Save audio file
        write_audio_to_file(
            audio=response.audio[0].base64_audio,
            filename=filename
        )

        # Read for streaming
        audio_bytes = open(filename, "rb").read()

        # Streamlit components
        st.audio(audio_bytes, format="audio/wav")

        st.download_button(
            label="Download Audio",
            data=audio_bytes,
            file_name=f"generated_audio_{uuid4().hex[:8]}.wav",
            mime="audio/wav"
        )

        return filename
    else:
        st.error("No audio was generated")
        return None
```

#### **D. Error Handling Template**

```python
def robust_audio_generation(agent, prompt, voice_id, max_retries=3):
    """Robust audio generation with error handling"""

    for attempt in range(max_retries):
        try:
            with st.spinner(f"Generating audio... (Attempt {attempt + 1})"):

                # Ensure voice_id is valid
                if not voice_id:
                    raise ValueError("Invalid voice selection")

                # Run agent
                response = agent.run(prompt, stream=False)

                # Process audio
                audio_file = process_audio_response(response)

                if audio_file:
                    st.success("Audio generated successfully! 🎵")
                    return audio_file
                else:
                    raise Exception("Audio processing failed")

        except Exception as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt == max_retries - 1:
                st.error("Failed to generate audio after multiple attempts")
                return None

            # Wait before retry
            time.sleep(2)

    return None
```

## Cài Đặt

### Yêu Cầu

1. **API Keys**:

   - **Groq API Key**: Đăng ký tại Groq để lấy API key.

   - **ElevenLabs API Key**: Lấy API key ElevenLabs từ ElevenLabs.

   - **Firecrawl API Key**: Lấy API key Firecrawl từ Firecrawl.

2. **Python 3.8+**: Đảm bảo bạn đã cài đặt Python 3.8 trở lên.

### Cài Đặt

1. Clone repository này:

   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps
   cd ai_agent_tutorials/ai_blog_to_podcast_agent
   ```

2. Cài đặt các gói Python cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

### Chạy Ứng Dụng

1. Khởi động ứng dụng Streamlit:

   ```bash
   streamlit run blog_to_podcast_agent.py
   ```

2. Trong giao diện ứng dụng:

   - Nhập các API key OpenAI, ElevenLabs và Firecrawl vào sidebar.

   - Nhập URL blog bạn muốn chuyển đổi.

   - Nhấn "🎙️ Generate Podcast".

   - Nghe podcast đã tạo hoặc tải xuống.

## Cách Hoạt Động

1. **Thu thập nội dung**: Sử dụng Firecrawl để lấy toàn bộ nội dung từ URL blog
2. **Tóm tắt thông minh**: GEMINI LLM phân tích và tạo bản tóm tắt hấp dẫn
3. **Chuyển đổi âm thanh**: ElevenLabs chuyển văn bản thành giọng nói tự nhiên
4. **Tải xuống**: Người dùng có thể nghe trực tiếp hoặc tải file âm thanh

## Lưu Ý Quan Trọng

- Bản tóm tắt được giới hạn 3000 ký tự để tránh vượt quá giới hạn API ElevenLabs
- Cần có kết nối internet để truy cập các API
- File âm thanh được lưu trong thư mục `audio_generations`
- Sử dụng model `eleven_turbo_v2_5` cho chất lượng âm thanh tốt nhất
