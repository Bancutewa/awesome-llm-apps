# 🚀 Hướng Dẫn Thiết Lập API Keys

## 1. Tạo File .env

Tạo một file có tên `.env` trong thư mục gốc của dự án và sao chép nội dung sau:

```bash
# API Keys cho các Model Providers
# Điền các API keys thực tế của bạn vào đây

# OpenAI API Key (https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (https://console.anthropic.com/)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google AI API Key (https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=your_google_api_key_here

# Hugging Face Token (tùy chọn - cho các model mã nguồn mở)
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

## 2. Cách Lấy API Keys

### 🔑 OpenAI API Key

1. Truy cập: https://platform.openai.com/api-keys
2. Đăng nhập tài khoản OpenAI
3. Tạo API key mới
4. Copy và paste vào file .env

### 🤖 Anthropic API Key

1. Truy cập: https://console.anthropic.com/
2. Đăng nhập tài khoản Anthropic
3. Tạo API key mới
4. Copy và paste vào file .env

### 🌐 Google AI API Key

1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập tài khoản Google
3. Tạo API key mới
4. Copy và paste vào file .env

### 🤗 Hugging Face Token (Tùy Chọn)

1. Truy cập: https://huggingface.co/settings/tokens
2. Tạo token mới
3. Copy và paste vào file .env

## 3. ⚠️ Lưu Ý Quan Trọng

### 🔒 Bảo Mật

- **KHÔNG** commit file `.env` vào Git
- Thêm `.env` vào file `.gitignore`
- KHÔNG chia sẻ API keys với ai khác

### 💰 Credits và Chi Phí

- OpenAI: Có phí sử dụng dựa trên tokens
- Anthropic: Có phí sử dụng dựa trên tokens
- Google AI: Một số credits miễn phí ban đầu
- Hugging Face: Miễn phí cho hầu hết các model

### 🔄 Best Practices

- Sử dụng API keys với quyền hạn tối thiểu cần thiết
- Rotate (đổi) API keys định kỳ
- Monitor usage để tránh vượt quá giới hạn

## 4. 🧪 Test API Keys

Sau khi thiết lập xong, bạn có thể test bằng script Python đơn giản:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test OpenAI
if os.getenv('OPENAI_API_KEY'):
    print("✅ OpenAI API Key loaded successfully")
else:
    print("❌ OpenAI API Key not found")

# Test Anthropic
if os.getenv('ANTHROPIC_API_KEY'):
    print("✅ Anthropic API Key loaded successfully")
else:
    print("❌ Anthropic API Key not found")

# Test Google AI
if os.getenv('GOOGLE_API_KEY'):
    print("✅ Google AI API Key loaded successfully")
else:
    print("❌ Google AI API Key not found")
```

## 5. 🚨 Troubleshooting

### Lỗi thường gặp:

- **API Key Invalid**: Kiểm tra lại API key đã copy đúng chưa
- **Rate Limit Exceeded**: Đã vượt quá giới hạn sử dụng, đợi một thời gian
- **Permission Denied**: API key không có quyền truy cập service đó
- **Network Error**: Kiểm tra kết nối internet

### Hỗ trợ:

- OpenAI: https://help.openai.com/
- Anthropic: https://docs.anthropic.com/
- Google AI: https://ai.google.dev/support
