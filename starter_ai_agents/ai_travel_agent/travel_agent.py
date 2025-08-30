from textwrap import dedent
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
import streamlit as st
import re
from agno.models.groq import Groq
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_ics_content(plan_text:str, start_date: datetime = None) -> bytes:
    """
        Generate an ICS calendar file from a travel itinerary text.

        Args:
            plan_text: The travel itinerary text
            start_date: Optional start date for the itinerary (defaults to today)

        Returns:
            bytes: The ICS file content as bytes
        """
    cal = Calendar()
    cal.add('prodid','-//AI Travel Planner//github.com//' )
    cal.add('version', '2.0')

    if start_date is None:
        start_date = datetime.today()

    # Split the plan into days
    day_pattern = re.compile(r'Day (\d+)[:\s]+(.*?)(?=Day \d+|$)', re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days: # If no day pattern found, create a single all-day event with the entire content
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)  
    else:
        # Process each day
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)
            
            # Create a single event for the entire day
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())
            
            # Make it an all-day event
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()

# Set up the Streamlit app
st.title("🤖 AI Travel Planner")
st.caption("Lập kế hoạch chuyến đi mơ ước với AI Travel Planner - tự động nghiên cứu và tạo lịch trình cá nhân hóa bằng trí tuệ nhân tạo")

# Initialize session state to store the generated itinerary
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# Get OpenAI API key from user
openai_api_key = os.getenv("GROQ_API_KEY")

# Get SerpAPI key from the user
serp_api_key = os.getenv("SERPAPI_API_KEY")

if openai_api_key and serp_api_key:
    researcher = Agent(
        name="Researcher",
        role="Searches for travel destinations, activities, and accommodations based on user preferences",
        model=Groq(id="llama3-8b-8192", api_key=openai_api_key),
        description=dedent(
            """\
        Bạn là một nhà nghiên cứu du lịch hàng đầu thế giới. Khi nhận được điểm đến du lịch và số ngày du lịch của người dùng,
        hãy tạo ra danh sách các từ khóa tìm kiếm để tìm các hoạt động du lịch và chỗ ở phù hợp.
        Sau đó tìm kiếm trên web cho từng từ khóa, phân tích kết quả, và trả về 10 kết quả liên quan nhất.
        Tất cả thông tin phải được trình bày bằng tiếng Việt.
        """
        ),
        instructions=[
            "Khi nhận được điểm đến du lịch và số ngày du lịch của người dùng, trước tiên hãy tạo ra danh sách 3 từ khóa tìm kiếm liên quan đến điểm đến đó và số ngày.",
            "Đối với mỗi từ khóa tìm kiếm, hãy sử dụng `search_google` và phân tích kết quả. Ưu tiên tìm kiếm thông tin bằng tiếng Việt.",
            "Từ kết quả của tất cả các tìm kiếm, trả về 10 kết quả liên quan nhất với sở thích của người dùng.",
            "Hãy nhớ: chất lượng của kết quả rất quan trọng.",
            "Tất cả kết quả trả về phải được trình bày bằng tiếng Việt.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    planner = Agent(
        name="Planner",
        role="Generates a draft itinerary based on user preferences and research results",
        model=Groq(id="deepseek-r1-distill-llama-70b", api_key=openai_api_key),
        description=dedent(
            """\
        Bạn là một nhà lập kế hoạch du lịch chuyên nghiệp. Dựa trên điểm đến, số ngày du lịch và kết quả nghiên cứu,
        hãy tạo ra lịch trình du lịch chi tiết bao gồm các hoạt động và chỗ ở được đề xuất.
        Tất cả nội dung phải được trình bày bằng tiếng Việt một cách tự nhiên và hấp dẫn.
        """
        ),
        instructions=[
            "Tạo lịch trình du lịch chi tiết với các hoạt động và chỗ ở được đề xuất.",
            "Đảm bảo lịch trình được cấu trúc tốt, thông tin và hấp dẫn.",
            "Đảm bảo cung cấp lịch trình đa dạng và cân bằng, trích dẫn sự thật khi có thể.",
            "Hãy nhớ: chất lượng của lịch trình rất quan trọng.",
            "Tập trung vào sự rõ ràng, mạch lạc và chất lượng tổng thể.",
            "Không bao giờ bịa đặt sự thật hoặc đạo văn. Luôn trích dẫn nguồn gốc khi cần thiết.",
            "Tất cả nội dung phải được viết bằng tiếng Việt một cách tự nhiên và thân thiện.",
        ],
        add_datetime_to_instructions=True,
    )

    # Input fields for the user's destination and the number of days they want to travel for
    destination = st.text_input("Bạn muốn đi đâu?")
    num_days = st.number_input("Bạn muốn đi bao nhiêu ngày?", min_value=1, max_value=30, value=7)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Tạo lịch trình"):
            with st.spinner("🔍 Đang nghiên cứu điểm đến..."):
                # First get research results
                research_results = researcher.run(f"Nghiên cứu {destination} cho chuyến đi {num_days} ngày", stream=False)

                # Show research progress
                st.write("✅ Hoàn thành nghiên cứu")

            with st.spinner("📝 Đang tạo lịch trình cá nhân hóa..."):
                # Pass research results to planner
                prompt = f"""
                Điểm đến: {destination}
                Thời lượng: {num_days} ngày
                Kết quả nghiên cứu: {research_results.content}

                Hãy tạo lịch trình du lịch chi tiết bằng tiếng Việt dựa trên kết quả nghiên cứu này.
                Đảm bảo lịch trình hấp dẫn, thực tế và phù hợp với văn hóa Việt Nam.
                """
                response = planner.run(prompt, stream=False)
                # Store the response in session state
                st.session_state.itinerary = response.content
                st.write(response.content)
    
    # Only show download button if there's an itinerary
    with col2:
        if st.session_state.itinerary:
            # Generate the ICS file
            ics_content = generate_ics_content(st.session_state.itinerary)
            
            # Provide the file for download
            st.download_button(
                label="📅 Tải lịch trình (.ics)",
                data=ics_content,
                file_name="lich_trinh_du_lich.ics",
                mime="text/calendar"
            )