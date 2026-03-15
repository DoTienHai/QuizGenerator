# Render.com - Web Deployment Platform

**Ngày tạo**: 2026-03-15  
**Mục đích**: Ghi chép về Render.com - nền tảng deploy web miễn phí

---

## 1. Render.com là gì?

**Render.com** là một **cloud platform** để deploy & host web applications.

**Định nghĩa**:
- Nền tảng đám mây cho phép bạn **upload code lên server**
- Server sẽ **chạy code 24/7**
- Mọi người trên internet có thể **truy cập website**
- **Miễn phí** cho mức sử dụng cơ bản

### Ví Dụ Thực Tế:

**Trước khi deploy (Local)**:
```
Bạn chạy: python app.py
↓
Server chạy ở máy tính bạn: http://localhost:5000
↓
Chỉ bạn hoặc máy bạn mới truy cập được
↓
Tắt máy tính → Web tắt
```

**Sau khi deploy (Render.com)**:
```
Bạn push code lên GitHub
↓
Render.com nhận & build code
↓
Server chạy ở cloud: https://quizgenerator.onrender.com
↓
Ai cũng truy cập được từ internet
↓
24/7 chạy (trừ plan Free auto-pause)
```

---

## 2. Các Alternatives (So Sánh)

| Platform | Giá | Dễ Dùng | Limitations |
|----------|-----|---------|------------|
| **Render.com** | 🆓 Free | ⭐⭐⭐⭐⭐ | Auto-pause free tier |
| **Heroku** | 💰 Paid | ⭐⭐⭐⭐⭐ | Ngừng free tier (2022) |
| **Vercel** | 🆓 Free | ⭐⭐⭐⭐ | Dành cho Next.js/Frontend |
| **Railway** | 🆓 Free | ⭐⭐⭐⭐ | $5/month trial |
| **PythonAnywhere** | 🆓 Free | ⭐⭐⭐ | Hạn chế hơn |
| **AWS** | 💰 Paid | ⭐⭐ | Phức tạp, đắt |

**Render.com tốt nhất cho**:
- ✅ Python/Flask/Django
- ✅ Node.js
- ✅ Mới bắt đầu
- ✅ Không có budget

---

## 3. Free Plan - Chi Tiết

### 3.1 Ưu Điểm

✅ **Miễn phí hoàn toàn**
- Không tính phí hàng tháng
- Không cần credit card

✅ **Public URL**
- Mọi người trên internet có thể truy cập
- Ví dụ: `https://quizgenerator.onrender.com`
- Có thể chia sẻ link cho bạn bè

✅ **Automatic Deployment**
- Push code lên GitHub → Render tự động build & deploy
- Không cần manual deploy

✅ **SSL Certificate**
- HTTPS support miễn phí
- Kết nối an toàn

✅ **Build & Runtime**
- Có sẵn Python, Node.js, Ruby, Go, etc
- Cài packages từ requirements.txt/package.json

### 3.2 Nhược Điểm

❌ **Auto-pause sau 15 phút**
- Nếu không ai truy cập 15 phút → Server tạm dừng
- Truy cập tiếp theo sẽ chậm (~30 giây) khi "wake up"

```
Timeline:
[00:00] User truy cập → Server active
[15:00] Không activity → Auto-pause
[15:01] User truy cập lại → Server restart (~30s)
```

❌ **Giới hạn RAM & CPU**
- Ram: 512MB (free tier)
- CPU: Limited (1 core)

❌ **Database**
- SQLite database sẽ bị xóa mỗi lần deploy
- Cần dùng PostgreSQL/MySQL ngoài (hoặc setup trong Render)

❌ **Bandwidth & Storage**
- Giới hạn (nhưng đủ cho app nhỏ)

---

## 4. Deployment Steps (Chi Tiết)

### 4.1 Chuẩn Bị Code

**Tệp cần có**:

1. **requirements.txt** (Python dependencies)
```
Flask==2.3.3
gunicorn==20.1.0
```

2. **Procfile** (chỉ dẫn cho Render)
```
web: gunicorn app:app
```

3. **app.py** (Flask app)
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
```

4. **Push lên GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 4.2 Tạo Render Account

1. Truy cập **https://render.com**
2. Click **Sign up**
3. Chọn **Sign up with GitHub** (dễ nhất)
4. Authorize Render để access GitHub repo

### 4.3 Connect GitHub Repository

1. Sau đăng nhập, homepage tại **https://dashboard.render.com**
2. Click **New +** (góc trên phải)
3. Chọn **Web Service**
4. Click **Connect a repository**
5. Tìm repo `QuizGenerator`
6. Click **Connect**

### 4.4 Configure Web Service

**Form sẽ hiện, điền như sau**:

| Setting | Value | Ghi Chú |
|---------|-------|---------|
| **Name** | `quizgenerator` | Tên service (sẽ thành part của URL) |
| **Region** | `Singapore` hoặc `Ohio` | Chọn gần bạn |
| **Branch** | `main` | Branch GitHub deploy |
| **Runtime** | `Python 3` | Auto-detect |
| **Build Command** | `pip install -r requirements.txt` | Cài dependencies |
| **Start Command** | `gunicorn app:app` | Chạy app |
| **Plan** | `Free` | Miễn phí |

### 4.5 Deploy

1. **Review** tất cả settings
2. Click **Create Web Service** (nút xanh)
3. **Chờ build** (1-3 phút)
4. Khi thấy ✅ **Live** → Deploy thành công!

### 4.6 Truy Cập

```
URL: https://quizgenerator.onrender.com
(hoặc tên service bạn chọn)
```

---

## 5. Cấu Trúc File Deploy

```
QuizGenerator/
├── app.py                    ← Main Flask app
├── requirements.txt          ← Python dependencies
├── Procfile                  ← Instructions cho Render
├── templates/
│   └── index.html           ← HTML files
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── docs/                     ← Documentation
├── note/                     ← Notes
└── .gitignore               ← Files to ignore
```

**Render.com sẽ**:
1. Clone repo từ GitHub
2. Chạy `pip install -r requirements.txt`
3. Chạy `gunicorn app:app` (từ Procfile)
4. Expose port 10000 (auto)
5. URL: https://service-name.onrender.com

---

## 6. Auto-Deploy & Updates

### Cách Hoạt Động

```
GitHub (bạn push code)
    ↓
Render.com (webhook tự động trigger)
    ↓
Build lại app
    ↓
Redeploy live
```

**Không cần làm gì cả**:
- Push → Render auto build & deploy
- ~2-5 phút cập nhật trên web

### Cách Trigger Manual Deploy

1. Vào **https://dashboard.render.com**
2. Chọn service
3. Click **Manual Deploy** → **Deploy latest commit**
4. Chờ build xong

---

## 7. Logs & Debugging

### Xem Logs

1. Vào service page
2. Click **Logs** tab
3. Xem real-time logs

**Ví dụ logs**:
```
Mar 15 10:30:22 - Building...
Mar 15 10:30:45 - Installing dependencies...
Mar 15 10:31:00 - pip install -r requirements.txt
Mar 15 10:31:30 - Starting server...
Mar 15 10:31:45 - Server listening on port 10000
Mar 15 10:31:50 - Deployment successful ✓
```

### Common Errors

| Error | Nguyên Nhân | Fix |
|-------|-----------|-----|
| `ModuleNotFoundError` | Thiếu package | Thêm vào requirements.txt |
| `Procfile not found` | Chưa tạo Procfile | Tạo file `Procfile` |
| `Port 10000` | Flask mặc định port 5000 | Render tự quản port |
| `Build failed` | Syntax error | Kiểm tra GitHub code |

---

## 8. Environment Variables

### Thêm Secret Keys

**Khi có nhạy cảm** (API keys, passwords):

1. Vào **Environment** tab
2. Click **Add Environment Variable**
3. Thêm key-value pairs:
   ```
   DATABASE_URL = postgresql://...
   SECRET_KEY = your-secret-key
   API_KEY = abc123def456
   ```

### Trong Code

```python
import os

# Lấy từ environment variable
db_url = os.getenv('DATABASE_URL')
secret_key = os.getenv('SECRET_KEY')

# Nếu không có → giá trị default
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
```

---

## 9. Database Deployment

### Vấn Đề SQLite

```python
# ❌ Hiện tại (SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///quizgenerator.db'
# → Mỗi deploy, file bị xóa (Render là ephemeral filesystem)
```

### Giải Pháp

**Tùy chọn 1: PostgreSQL trên Render** (Khuyến nghị)
```python
import os
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizgenerator.db'
```

1. Tạo PostgreSQL database trên Render (free tier)
2. Copy connection string
3. Add vào Environment Variables
4. Update code

**Tùy chọn 2: Firebase (NoSQL)**
- Google Cloud hosted
- Dễ setup
- Free tier đủ dùng

---

## 10. Lifecycle - Khi Deploy Xong

### Lần Đầu

```
[Push code] → [Render detect] → [Build (2-3 min)] → [Live ✓]
```

### Updates Tiếp Theo

```
[Push code] → [Auto trigger] → [Rebuild (1-2 min)] → [Live ✓]
```

### Auto-Pause (Free Tier)

```
[15 min no traffic] → [Pause]
                ↓
[User access] → [Wake up & restart (~30s)]
                ↓
[Page loads slow lần đầu] → [Normal speed sau đó]
```

---

## 11. Paid Plans & Upgrades

### Nếu Muốn Bỏ Auto-Pause

**Pro Plan** (~$7/month):
- ✅ No auto-pause
- ✅ More RAM & CPU
- ✅ Higher limits

### Nếu Muốn More Power

**Advanced Plans** (~$20+/month):
- ✅ 2GB RAM
- ✅ 2vCPU
- ✅ Priority support
- ✅ Custom domain

---

## 12. QuizGenerator Deployment Checklist

```
Code Preparation:
  ☐ app.py (Flask main file)
  ☐ requirements.txt (Flask, gunicorn)
  ☐ Procfile (web: gunicorn app:app)
  ☐ templates/index.html
  ☐ Push to GitHub main branch

Render Setup:
  ☐ Create Render.com account
  ☐ Connect GitHub
  ☐ Create Web Service
  ☐ Set Name: quizgenerator
  ☐ Set Runtime: Python 3
  ☐ Set Start Command: gunicorn app:app
  ☐ Select Plan: Free
  ☐ Click Create

Verify Deployment:
  ☐ Wait for build complete (✓ Live indicator)
  ☐ Check logs for errors
  ☐ Visit https://quizgenerator.onrender.com
  ☐ Test / button
  ☐ Test /api/quizzes

Post-Deploy:
  ☐ Share URL with team
  ☐ Test on mobile
  ☐ Monitor logs
  ☐ Update code & push (auto-redeploy)
```

---

## 13. Tóm Tắt

| Aspect | Chi Tiết |
|--------|----------|
| **Giá** | 🆓 Miễn phí (free tier) |
| **Thích hợp cho** | Prototype, side project, learning |
| **Setup time** | ~10 phút |
| **Deploy time** | ~2-3 phút (first), ~1 min (updates) |
| **URL** | `https://service-name.onrender.com` |
| **Auto-pause** | Sau 15 phút không activity |
| **Database** | SQLite xóa mỗi deploy → cần PostgreSQL |
| **Support** | Community + docs |
| **Upgrade path** | Dễ upgrade sang Pro/Advanced |

---

## 14. ⚠️ CRITICAL: Flask Host & Port Configuration

### Vấn Đề (Problem)

Khi deploy lên Render.com, Flask phải được cấu hình **đúng cách** để nghe các request từ internet.

**Lỗi nếu config sai**:
```
ERROR: No open ports detected on 0.0.0.0, continuing to scan...
↓
Render.com không thể truy cập Flask app
↓
Deploy fails ❌
```

### Nguyên Nhân

Render.com là **cloud server**:
- Flask chạy trên một **container** (virtual machine)
- Người dùng truy cập từ **internet** (external network)
- Flask cần nghe trên **tất cả network interfaces** (không chỉ localhost)

### Giải Pháp: 2 Thay Đổi Bắt Buộc

#### ❌ SAI (Local development only):
```python
if __name__ == '__main__':
    app.run(debug=True)  # ← Chỉ nghe localhost
```

**Khi chạy**:
```
* Running on http://127.0.0.1:5000
* Chỉ máy bạn truy cập được
```

#### ✅ ĐÚNG (Production on Render):
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # ← Cần bắt buộc
    app.run(host='0.0.0.0', port=port, debug=False)  # ← Cần bắt buộc
```

**Khi chạy**:
```
* Running on http://0.0.0.0:5000 (locally)
* Hoặc 0.0.0.0:10000 (on Render)
* Ai cũng từ internet truy cập được
```

### Chi Tiết: Localhost vs 0.0.0.0

| Config | Nghe Trên | Ai Truy Cập Được | Dùng Cho |
|--------|-----------|------------------|----------|
| `127.0.0.1` | localhost | Chỉ máy local | Local dev |
| `localhost` | localhost | Chỉ máy local | Local dev |
| `0.0.0.0` | Tất cả interfaces | Ai từ internet | Production |

**Visual**:
```
Local Dev:
    app.run(debug=True)  →  127.0.0.1:5000  →  Chỉ bạn
                             ↓
                        http://localhost:5000

Render Production:
    app.run(host='0.0.0.0', port=10000)  →  0.0.0.0:10000  →  Ai cũng được
                                              ↓
                                    https://quizgenerator.onrender.com
```

### Port Binding: Dynamic Environment Variable

**Render.com quy định**:
- Render tự động gán **dynamic port** (thường 10000)
- Flask phải **đọc** từ environment variable `PORT`
- Nếu chạy local → default về 5000

**Code**:
```python
import os
port = int(os.environ.get('PORT', 5000))
#     ↑                       ↑              ↑
#     Đọc từ OS        lấy từ PORT    default=5000
app.run(host='0.0.0.0', port=port, debug=False)
```

**Khi chạy**:
```bash
# Local (PORT không set)
$ python app.py
Running on http://0.0.0.0:5000

# Render (PORT=10000)
$ PORT=10000 python app.py
Running on http://0.0.0.0:10000
```

### Tóm Tắt 2 Thay Đổi Bắt Buộc

```python
# REQUIREMENT 1: host='0.0.0.0'
# Lý do: Render.com là cloud → cần nghe tất cả network interfaces
app.run(host='0.0.0.0', ...)

# REQUIREMENT 2: Đọc PORT từ environment variable
# Lý do: Render tự động gán port → Flask cần flexible
port = int(os.environ.get('PORT', 5000))
app.run(..., port=port, ...)
```

### QuizGenerator: Đã Fix ✅

**File**: `app.py` (lines 84-86)
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Status**: ✅ Config chính xác → Ready for Render.com

**Commit**: `cc387f7` - "Fix Flask port binding for Render.com deployment"

---

## 15. Next Steps

1. ✅ Deploy QuizGenerator lên Render.com
2. ✅ Test endpoints từ URL public
3. ✅ Chia sẻ URL với team
4. ✅ Implement database models (Phase 3 tiếp)
5. ✅ Add real logic & data persistence
6. ✅ Setup PostgreSQL nếu cần production

---

**Tài Liệu Tham Khảo**:
- https://render.com/docs
- https://render.com/docs/deploy-flask
- https://render.com/blog

