# 🛫 AI Travel Agent

Ứng dụng Streamlit này là một AI Travel Agent được hỗ trợ bởi AI, tạo ra các lịch trình du lịch cá nhân hóa bằng cách sử dụng OpenAI GPT-4o. Nó tự động hóa quá trình nghiên cứu, lập kế hoạch và tổ chức kỳ nghỉ mơ ước của bạn, cho phép bạn khám phá các điểm đến thú vị một cách dễ dàng.

## Tính năng

- Nghiên cứu và khám phá các điểm đến du lịch, hoạt động và chỗ ở thú vị
- Tùy chỉnh lịch trình của bạn dựa trên số ngày bạn muốn đi du lịch
- Sử dụng sức mạnh của GPT-4o để tạo ra các kế hoạch du lịch thông minh và cá nhân hóa
- Tải xuống lịch trình của bạn dưới dạng file lịch (.ics) để nhập vào Google Calendar, Apple Calendar, hoặc các ứng dụng lịch khác

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

3. Lấy OpenAI API Key của bạn

- Đăng ký tài khoản [OpenAI](https://platform.openai.com/) (hoặc nhà cung cấp LLM mà bạn chọn) và lấy API key của bạn.

4. Lấy SerpAPI Key của bạn

- Đăng ký tài khoản [SerpAPI](https://serpapi.com/) và lấy API key của bạn.

5. Chạy ứng dụng Streamlit

```bash
streamlit run travel_agent.py
```

Đối với việc sử dụng LLM cục bộ (với Ollama):

```bash
streamlit run local_travel_agent.py
```

## Cách hoạt động?

AI Travel Agent có hai thành phần chính:

- **Researcher (Người Nghiên Cứu)**: Chịu trách nhiệm tạo ra các từ khóa tìm kiếm dựa trên điểm đến và thời gian du lịch của người dùng, và tìm kiếm trên web các hoạt động và chỗ ở liên quan bằng cách sử dụng SerpAPI.

- **Planner (Người Lập Kế Hoạch)**: Lấy kết quả nghiên cứu và sở thích của người dùng để tạo ra bản nháp lịch trình cá nhân hóa bao gồm các hoạt động được đề xuất, lựa chọn ăn uống và chỗ ở.

## Sử dụng tính năng tải xuống lịch

Sau khi tạo lịch trình du lịch của bạn:

1. Nhấp vào nút "Download Itinerary as Calendar (.ics)" xuất hiện bên cạnh nút "Generate Itinerary"
2. Lưu file .ics vào máy tính của bạn
3. Nhập file vào ứng dụng lịch ưa thích của bạn (Google Calendar, Apple Calendar, Outlook, v.v.)
4. Mỗi ngày của lịch trình sẽ xuất hiện dưới dạng sự kiện cả ngày trong lịch của bạn
5. Chi tiết hoàn chỉnh cho các hoạt động trong ngày được bao gồm trong mô tả sự kiện

Tính năng này giúp dễ dàng theo dõi kế hoạch du lịch của bạn và có lịch trình có sẵn trên tất cả thiết bị của bạn, ngay cả khi offline.

## Phiên bản cục bộ vs đám mây

- **travel_agent.py**: Sử dụng OpenAI's GPT-4o để có các lịch trình chất lượng cao (yêu cầu OpenAI API key)
- **local_travel_agent.py**: Sử dụng Ollama để suy luận LLM cục bộ mà không gửi dữ liệu đến các API bên ngoài (yêu cầu Ollama được cài đặt và chạy)
