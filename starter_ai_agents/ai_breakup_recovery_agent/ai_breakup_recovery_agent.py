from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()


# Configure logging for errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash", api_key=api_key)
        
        therapist_agent = Agent(
            model=model,
            name="Therapist Agent",
            description="Bạn là một chuyên gia trị liệu có khả năng đồng cảm và hỗ trợ tinh thần.",
            instructions=[
                "1. Lắng nghe câu chuyện của người dùng và đồng cảm với cảm xúc của họ.",
                "2. Sử dụng giọng điệu dịu dàng và một chút hài hước để xoa dịu tâm trạng của người dùng.",
                "3. Chia sẻ những kinh nghiệm giá trị về việc phục hồi sau chia tay.",
                "4. Đưa ra những lời khích lệ và lời khuyên hữu ích.",
                "5. Phân tích cả văn bản và hình ảnh để thấu hiểu cảm xúc của người dùng. Ưu tiên tìm kiếm thông tin bằng tiếng Việt.",
                "6. Hãy luôn thể hiện sự hỗ trợ và thấu hiểu trong mỗi phản hồi."
            ],
            markdown=True,
            debug_mode=True
        )

        closure_agent = Agent(
            model=model,
            name="Closure Agent",
            description="Bạn là một chuyên gia giúp khép lại quá khứ, có khả năng tạo ra những tin nhắn xúc cảm chưa gửi để giúp người dùng giải tỏa.",
            instructions=[
                "1. Soạn những thông điệp giàu cảm xúc cho những tâm tư chưa được gửi đi.",
                "2. Giúp người dùng bộc lộ những cảm xúc chân thật, nguyên sơ nhất.",
                "3. Định dạng các tin nhắn một cách rõ ràng, có tiêu đề.",
                "4. Đảm bảo giọng văn chân thành và giàu cảm xúc.",
                "5. Tập trung vào việc giải tỏa cảm xúc và giúp khép lại chuyện cũ."
            ],
            markdown=True,
            debug_mode=True
        )

        routine_planner_agent = Agent(
            model=model,
            name="Routine Planner Agent",
            description="Bạn là một chuyên gia lập kế hoạch phục hồi sau chia tay.",
            instructions=[
                "Bạn là một chuyên gia lập kế hoạch phục hồi, có nhiệm vụ:",
                "1. Thiết kế các thử thách phục hồi trong 7 ngày.",
                "2. Bao gồm các hoạt động vui vẻ và nhiệm vụ chăm sóc bản thân.",
                "3. Đề xuất các chiến lược 'cai' mạng xã hội (detox).",
                "4. Tạo các danh sách nhạc truyền cảm hứng và sức mạnh.",
                "5. Tập trung vào các bước phục hồi thiết thực và dễ thực hiện."
            ],
            markdown=True,
            debug_mode=True
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="Brutal Honesty Agent",
            tools=[DuckDuckGoTools()],
            description="Bạn là một chuyên gia đưa ra phản hồi thẳng thắn và không né tránh.",
            instructions=[
                "Bạn là một chuyên gia đưa ra phản hồi trực diện, có nhiệm vụ:",
                "1. Đưa ra phản hồi một cách khách quan, không tô vẽ về chuyện chia tay.",
                "2. Giải thích rõ ràng về những nguyên nhân thất bại trong mối quan hệ.",
                "3. Sử dụng ngôn ngữ thẳng thắn, dựa trên sự thật.",
                "4. Cung cấp những lý do thuyết phục để bước tiếp về phía trước.",
                "5. Tập trung vào những góc nhìn trung thực, không nói giảm nói tránh."
            ],
            markdown=True,
            debug_mode=True
        )
        
        return therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent
    except Exception as e:
        st.error(f"Lỗi khi khởi tạo các agent: {str(e)}")
        return None, None, None, None


# Set page config and UI elements
st.set_page_config(
    page_title="💔 Biệt Đội Chữa Lành Hậu Chia Tay",
    page_icon="💔",
    layout="wide"
)



with st.sidebar:
    st.header("🔑 Cấu hình API")

    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""
        
    api_key = st.text_input(
        "Nhập Khóa API Gemini của bạn",
        value=st.session_state.api_key_input,
        type="password",
        help="Lấy khóa API của bạn từ Google AI Studio",
        key="api_key_widget"
    )

    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
    
    if api_key:
        st.success("Đã cung cấp Khóa API! ✅")
    else:
        st.warning("Bạn đang sử dụng khoá API mặc định của ứng dụng")

        api_key = os.getenv("GEMINI_API_KEY")
        st.session_state.api_key_input = api_key


# Main content
st.title("💔 Biệt Đội Chữa Lành Hậu Chia Tay")
st.markdown("""
    ### Đội ngũ chữa lành hậu chia tay bằng AI của bạn đã ở đây để giúp đỡ!
    Chia sẻ cảm xúc và ảnh chụp màn hình cuộc trò chuyện, chúng tôi sẽ giúp bạn vượt qua giai đoạn khó khăn này.
""")

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Chia sẻ Cảm xúc của bạn")
    user_input = st.text_area(
        "Bạn đang cảm thấy thế nào? Chuyện gì đã xảy ra?",
        height=150,
        placeholder="Hãy kể cho chúng tôi câu chuyện của bạn..."
    )
    
with col2:
    st.subheader("Tải lên Ảnh chụp màn hình Cuộc trò chuyện")
    uploaded_files = st.file_uploader(
        "Tải lên ảnh chụp màn hình cuộc trò chuyện của bạn (không bắt buộc)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="screenshots"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)

# Process button and API key check
if st.button("Nhận Kế Hoạch Chữa Lành 💝", type="primary"):
    if not st.session_state.api_key_input:
        st.warning("Vui lòng nhập khóa API của bạn ở thanh bên trước!")
    else:
        therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent = initialize_agents(st.session_state.api_key_input)
        
        if all([therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent]):
            if user_input or uploaded_files:
                try:
                    st.header("Kế Hoạch Chữa Lành Dành Riêng Cho Bạn")
                    
                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")
                                
                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())
                                
                                agno_image = AgnoImage(filepath=Path(temp_path))
                                processed_images.append(agno_image)
                                
                            except Exception as e:
                                logger.error(f"Lỗi khi xử lý ảnh {file.name}: {str(e)}")
                                continue
                        return processed_images
                    
                    all_images = process_images(uploaded_files) if uploaded_files else []
                    
                    # Therapist Analysis
                    with st.spinner("🤗 Đang tìm kiếm sự đồng cảm và hỗ trợ..."):
                        therapist_prompt = f"""
                        Phân tích trạng thái cảm xúc và đưa ra sự hỗ trợ đồng cảm dựa trên:
                        Lời nhắn của người dùng: {user_input}
                        
                        Vui lòng đưa ra một phản hồi trắc ẩn bao gồm:
                        1. Công nhận cảm xúc của họ
                        2. Những lời an ủi nhẹ nhàng
                        3. Những trải nghiệm tương tự để họ thấy không đơn độc
                        4. Những lời động viên, khích lệ
                        Lưu ý, không cần liệt kê các bước, chỉ cần đưa ra phản hồi. Trả lời ngắn gọn và trực quan nhưng phải dễ hiểu.
                        """
                        
                        response = therapist_agent.run(
                            message=therapist_prompt,
                            images=all_images
                        )
                        
                        st.subheader("🤗 Hỗ trợ về mặt cảm xúc")
                        st.markdown(response.content)
                    
                    # Closure Messages
                    with st.spinner("✍️ Đang soạn những lời nhắn giúp bạn giải tỏa..."):
                        closure_prompt = f"""
                        Giúp người dùng tạo ra những thông điệp để khép lại chuyện cũ dựa trên:
                        Cảm xúc của người dùng: {user_input}
                        
                        Vui lòng cung cấp:
                        1. Mẫu cho những tin nhắn sẽ không gửi đi
                        2. Các bài tập để giải tỏa cảm xúc
                        3. Các nghi thức để khép lại quá khứ
                        4. Các chiến lược để bước tiếp
                        """
                        
                        response = closure_agent.run(
                            message=closure_prompt,
                            images=all_images
                        )
                        
                        st.subheader("✍️ Tìm cách để khép lại chuyện cũ")
                        st.markdown(response.content)
                    
                    # Recovery Plan
                    with st.spinner("📅 Đang tạo kế hoạch chữa lành cho bạn..."):
                        routine_prompt = f"""
                        Thiết kế một kế hoạch phục hồi trong 7 ngày dựa trên:
                        Tình trạng hiện tại: {user_input}
                        
                        Kế hoạch cần bao gồm:
                        1. Các hoạt động và thử thách hàng ngày
                        2. Lịch trình chăm sóc bản thân
                        3. Hướng dẫn sử dụng mạng xã hội
                        4. Gợi ý âm nhạc giúp cải thiện tâm trạng
                        """
                        
                        response = routine_planner_agent.run(
                            message=routine_prompt,
                            images=all_images
                        )
                        
                        st.subheader("📅 Kế hoạch chữa lành của bạn")
                        st.markdown(response.content)
                    
                    # Honest Feedback
                    with st.spinner("💪 Đang tìm kiếm một góc nhìn thẳng thắn..."):
                        honesty_prompt = f"""
                        Cung cấp phản hồi trung thực, mang tính xây dựng về:
                        Tình huống: {user_input}
                        
                        Phản hồi cần bao gồm:
                        1. Phân tích khách quan
                        2. Các cơ hội để phát triển bản thân
                        3. Triển vọng cho tương lai
                        4. Các bước hành động cụ thể
                        """
                        
                        response = brutal_honesty_agent.run(
                            message=honesty_prompt,
                            images=all_images
                        )
                        
                        st.subheader("💪 Một góc nhìn thẳng thắn")
                        st.markdown(response.content)
                                
                except Exception as e:
                    logger.error(f"Lỗi trong quá trình phân tích: {str(e)}")
                    st.error("Đã xảy ra lỗi trong quá trình phân tích. Vui lòng kiểm tra lại.")
            else:
                st.warning("Vui lòng chia sẻ cảm xúc của bạn hoặc tải ảnh lên để nhận được sự giúp đỡ.")
        else:
            st.error("Không thể khởi tạo các agent. Vui lòng kiểm tra lại khóa API của bạn.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Được tạo ra với ❤️ bởi Biệt Đội Chữa Lành Hậu Chia Tay</p>
        <p>Chia sẻ hành trình của bạn với hashtag #BietDoiChuaLanhHauChiaTay</p>
    </div>
""", unsafe_allow_html=True)