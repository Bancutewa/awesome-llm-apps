
# Hướng dẫn làm việc với Fork Repo và Repo Gốc

## 📌 Phân tích hiện tại
1. **Fork repo gốc** (`upstream` = `https://github.com/Shubhamsaboo/awesome-llm-apps.git`) về GitHub của bạn (`origin` = `https://github.com/Bancutewa/awesome-llm-apps`).
2. Ban đầu `main` của bạn giống `upstream/main`.
3. Bạn code → tạo branch `start/ai_travel_agent` → push lên fork → merge vào `main` (local), rồi push `main` lên fork.  
   👉 Kết quả: `origin/main` **đi trước** `upstream/main` với các commit của bạn.
4. Hiện giờ:
   - `upstream/main`: repo gốc (liên tục được cập nhật bởi tác giả).
   - `origin/main`: repo fork của bạn (chứa cả commit của bạn).
   - `main` local: tracking `origin/main`.

---

## ✅ Mục tiêu
- **Luôn học tập / code trên repo fork (`origin`).**
- **Luôn có thể đồng bộ code mới từ repo gốc (`upstream`).**

---

## 🚀 Quy trình chuẩn bạn nên dùng từ giờ

### 1. Đồng bộ fork của bạn với repo gốc
Khi tác giả update code mới, bạn muốn lấy về:

```bash
# Đảm bảo bạn đang ở nhánh main local
git checkout main

# Lấy code mới nhất từ repo gốc
git fetch upstream

# Merge code gốc vào main của bạn
git merge upstream/main
```

👉 Lúc này `main` của bạn sẽ có cả code gốc mới + code của bạn.  
Nếu có conflict thì bạn resolve rồi commit.  

Sau đó push lên repo fork của bạn:
```bash
git push origin main
```

---

### 2. Cách bạn làm việc (để học tập, code thử)
- **Không code trực tiếp trên `main`** nữa.  
- Mỗi khi muốn làm gì đó, hãy tạo branch mới từ `main`:
  ```bash
  git checkout main
  git pull        # đảm bảo main đã mới nhất
  git checkout -b feature/something
  ```
- Code → commit → push:
  ```bash
  git push origin feature/something
  ```
- Nếu muốn gộp vào `main` thì merge ở local hoặc mở Pull Request trên GitHub của bạn.

---

### 3. Tóm gọn quy trình
- Cập nhật code mới từ repo gốc:
  ```bash
  git fetch upstream
  git merge upstream/main
  git push origin main
  ```
- Bắt đầu một tính năng mới:
  ```bash
  git checkout main
  git pull
  git checkout -b feature/ten-tinh-nang
  ```
- Code & commit bình thường, push branch đó lên fork:
  ```bash
  git push origin feature/ten-tinh-nang
  ```

---

## 📖 Kết luận
- **Repo fork của bạn (`origin`)** = nơi bạn học tập, lưu commit riêng.  
- **Repo gốc (`upstream`)** = luôn đồng bộ về khi bạn cần update.  
