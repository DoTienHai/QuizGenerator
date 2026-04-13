---
date: 2026-04-03 15:45
summary: Tóm tắt toàn bộ kiến thức về Cookie & Session - Cách Backend phân biệt các user, Multi-tab & Multi-device, Device Fingerprinting
---

## Mục Lục
- [Vấn Đề Cơ Bản](#van-de-co-ban)
- [Cookie Là Gì](#cookie-la-gi)
- [Session Là Gì](#session-la-gi)
- [Quy Trình Chi Tiết](#quy-trinh-chi-tiet)
- [Cookies vs SessionStorage](#cookies-vs-sessionstorage)
- [Session Lifecycle - Chu Kỳ Hành Động](#session-lifecycle---chu-ky-hanh-dong)
- [Multi-Tab vs Multi-Device](#multi-tab-vs-multi-device)
- [Device Fingerprinting - Lấy Thông Số Máy](#device-fingerprinting---lay-thong-so-may)
- [Browser Tự Động Gửi Thông Tin](#browser-tu-dong-gui-thong-tin)
- [Token (JWT) - Stateless Authentication](#token-jwt---stateless-authentication)

---

# Cookies & Sessions - Toàn Tập

## Vấn Đề Cơ Bản

**Câu hỏi:** Frontend gửi request `/api/quizzes` đối tượi đơn giản không có username. Vậy Backend làm sao biết data của việc ai gửi?

**Đáp Án:** Browser **tự động** gửi Cookie, Backend dùng Cookie để identify user.

```
Frontend:  await fetch('/api/quizzes')
           ↓ (KHÔNG gửi username)
           
Browser:   GET /api/quizzes
           Cookie: session_id=xyz789 ← Tự động gửi!
           
Backend:   ✓ Nhận cookie
           ✓ Dùng session_id để tìm user_id
           ✓ Trả về data của user đó
```

---

## Cookie Là Gì

**định nghĩa:** Cookie = Dữ liệu lưu trên **Browser**, được gửi lại server mỗi request.

**Đặc điểm:**
- Lưu trữ ở: Browser storage (trên máy user)
- Ai tạo: Backend tạo, gửi cho Browser
- Thời hạn: Backend quyết định (1 ngày, 7 ngày, vĩnh viễn, etc.)
- Auto gửi lại: Browser tự động thêm vào mỗi request (nếu `credentials: 'include'`)

**Ví dụ:**
```
Browser Storage:
┌─────────────────────────────┐
│ Cookies                      │
├─────────────────────────────┤
│ Name: session_id             │
│ Value: xyz789                │
│ Expires: 2026-04-10 (7 days)│
│ HttpOnly: true               │
│ Secure: true                 │
└─────────────────────────────┘
```

---

## Session Là Gì

**Định nghĩa:** Session = Dữ liệu lưu trên **Server** để nhớ thông tin về user.

**Đặc điểm:**
- Lưu trữ ở: Server memory hoặc database
- Ai tạo: Backend tạo khi user login
- Nội dung: user_id, username, permissions, login_time, etc.
- Frontend biết không: Không, Frontend chỉ nhận cookie (giá trị session_id)

**Ví dụ:**
```python
# Backend lưu session:
session['user_id'] = 42
session['username'] = 'john'
session['login_time'] = datetime.now()

# Tương ứng trên server:
Session Storage:
├─ session_id=xyz789
│  ├─ user_id: 42
│  ├─ username: "john"
│  └─ login_time: 2026-04-03 15:30
```

---

## Ai Cấp Cookie?

**✅ ĐÚNG:** Backend tạo + gửi Cookie

```
Backend                    Browser
  ↓
Create session_id=xyz789
Save session['user_id']=42
  ↓
response.set_cookie(
    'session_id',
    'xyz789',
    max_age=604800
)
  ↓
HTTP Response Header:
Set-Cookie: session_id=xyz789; Max-Age=604800
  ↓
                           Browser nhận
                           → Tự động lưu cookie
                           → Remember: session_id=xyz789
                           → Set timer 7 ngày → xóa auto
```

**❌ SAIIII:** Frontend gửi Cookie / Frontend tạo Cookie

Frontend chỉ gửi username + password. Mọi thứ còn lại (cookies, headers, IP) do Browser xử lý.

---

## Quy Trình Chi Tiết

### Request 1: LOGIN

```
Frontend Code:
  const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({username: 'john', password: '123'})
  });

Backend:
  ✓ Verify credentials
  ✓ Create session_id = "xyz789"
  ✓ Save session['user_id'] = 42
  ✓ Return: Set-Cookie: session_id=xyz789; Max-Age=604800

Browser:
  ✓ Nhận header Set-Cookie
  ✓ Lưu cookie vào storage
  ✓ Set timer: 7 ngày → xóa auto
```

### Request 2: GET QUIZZES (trong 7 ngày)

```
Frontend Code:
  await fetch('/api/quizzes');  // KHÔNG cần gửi username!

Browser (tự động):
  GET /api/quizzes
  Cookie: session_id=xyz789  ← Tự động thêm!

Backend:
  ✓ Nhận cookie
  ✓ Extract: session_id=xyz789
  ✓ Lookup session → user_id=42
  ✓ Return: Quizzes của user #42
  
✅ KHÔNG cần username/password!
```

### Request 3: GET QUIZZES (sau 7 ngày)

```
Frontend:
  await fetch('/api/quizzes');

Browser:
  Cookie đã hết hạn → Xóa auto
  GET /api/quizzes
  Cookie: [KHÔNG CÓ]  ← Cookie expired!

Backend:
  ✗ Không tìm thấy session_id
  ✗ session['user_id'] = None
  ✗ Return: 401 Unauthorized
  
🔐 PHẢI LOGIN LẠI!
```

---

## Cookies vs SessionStorage

| Tính Năng | Cookies | SessionStorage |
|-----------|---------|---|
| **Lưu ở đâu** | Browser + Server | Browser only |
| **Server biết không** | ✅ Được (Browser tự động gửi) | ❌ Không (Browser không gửi) |
| **Thời hạn** | Có thể set (1 ngày, 1 năm, etc.) | Tự động xóa khi close browser |
| **Dùng cho** | Authentication (login) | Temporary state (exam session) |
| **Security** | HttpOnly flag (JS không access) | JS có thể access → lộ dữ liệu |

**Ví dụ QuizGenerator:**
```javascript
// Login: Backend gửi Cookie → Browser lưu
// fetch('/api/login', ...) → Server set Cookie

// Lưu trạng thái exam: dùng SessionStorage
sessionStorage.setItem('sessionId', 123);        // Tạm thời
sessionStorage.setItem('currentQuestion', 1);    // Local state
sessionStorage.setItem('answers', JSON.stringify([...]));

// Mỗi request: Browser tự động gửi Cookie
// fetch('/api/results', {...})
// Cookie: session_id=xyz789 (tự động)
```

---

## Session Lifecycle - Chu Kỳ Hành Động

**Timeline:**

```
T=0s (Khởi đầu)
├─ ❌ Không có cookie
├─ Backend: "Not logged in" → 401
└─ Yêu cầu: "Vui lòng đăng nhập"

T=1s (User login: username + password)
├─ Backend verify ✓
├─ Backend tạo: session_id = "xyz789"
├─ Backend lưu: session['user_id'] = 42
├─ Backend gửi: Set-Cookie: session_id=xyz789; Max-Age=604800
├─ Browser lưu cookie
├─ ✅ LOGGED IN
└─ Timer: 7 ngày countdown

T=5 minutes (User click "View Quizzes")
├─ Browser tự động: Cookie: session_id=xyz789
├─ Backend: user_id=42 ✓
├─ ✅ SUCCESS (KHÔNG cần username!)
└─ Timer reset: 7 ngày countdown lại

T=6 days 23 hours 59 minutes (Sắp hết)
├─ Cookie vẫn còn 1 phút
├─ Mỗi request → Timer reset
└─ ✅ Vẫn dùng được

T=7 days (COOKIE HẾT HẠN)
├─ Browser tự động XÓA cookie
├─ ❌ Cookie biến mất
├─ Tất cả API requests → 401 Unauthorized
└─ 🔐 PHẢI LOGIN LẠI

T=7 days + 2 minutes (Login lại)
├─ User nhập username + password
├─ Backend verify ✓
├─ Backend tạo: NEW session_id = "abc999"
├─ Backend gửi: Set-Cookie: session_id=abc999; Max-Age=604800
├─ Browser lưu NEW cookie
├─ ✅ LOGGED IN AGAIN
└─ Timer: 7 ngày countdown (từ 0)
```

---

## Multi-Tab vs Multi-Device

### Scenario 1: 2 Tabs Trên Cùng 1 Máy

```
Machine A (Chrome Browser):

  Tab 1                  Tab 2                 Server
    |                      |                      |
    | POST /api/login      |                      |
    |──── (john/123) ──────────────────────────> |
    |                      |                      |
    |                      |  ✓ Create session_id=xyz789
    |                      |  ✓ Save user_id=42
    |                      |  ✓ Set-Cookie: xyz789
    |                      |                      |
    | <─── Cookie ────────────────────────────── |
    |                      |                      |
    | Browser Storage (SHARED):
    | session_id = "xyz789" → Shared giữa tabs!
    |                      |                      |
    | GET /api/quizzes     |                      |
    |──── Cookie: xyz789 ──────────────────────> |
    |                      | GET /api/results     |
    |                      |──── Cookie: xyz789 > |
    |                      |                      |
    |                      |  ✓ Cả 2 = user#42
    |                      |                      |
    | <─── quizzes ────────────────────────────  |
    |                      | <─ results ─────────

⭐ KEY: Cookies SHARED
⭐ Result: 1 session, 2 tabs
⭐ Logout ở Tab 1 → Session xóa → Tab 2 cũng logout
```

### Scenario 2: 2 Máy Khác Nhau

```
Machine A (Chrome)         Machine B (Firefox)        Server
  |                            |                         |
  | POST /api/login            |                         |
  |──── (john/123) ────────────────────────────────────> |
  |                            |                         |
  |                            |  ✓ Create session_id=aaa111
  |                            |  ✓ Set-Cookie: aaa111
  |                            |                         |
  | <─── Cookie ────────────────────────────────────    |
  |      session_id=aaa111      |                        |
  | Browser A lưu              |                        |
  |                            |                         |
  |                            | POST /api/login         |
  |                            |──── (john/123) ──────> |
  |                            |                         |
  |                            |  ✓ Create NEW session_id=bbb222
  |                            |  ✓ Set-Cookie: bbb222
  |                            |                         |
  |                            | <─ Cookie ────────────  |
  |                            |    session_id=bbb222    |
  |                            | Browser B lưu           |
  |                            |                         |
  | GET /api/quizzes           |                         |
  |──── Cookie: aaa111 ──────────────────────────────> |
  |                            | GET /api/quizzes        |
  |                            |──── Cookie: bbb222 ───> |
  |                            |                         |
  |                    Backend Server Storage:
  |                    ├─ session[aaa111] → user_id=42
  |                    ├─ session[bbb222] → user_id=42
  |                    └─ (2 SESSIONS khác nhau!)
  |                            |                         |
  | ✓ Lookup aaa111 → 42       | ✓ Lookup bbb222 → 42
  | ✓ Return quizzes           | ✓ Return quizzes
  |                            |                         |

⭐ KEY: Cookies KHÔNG SHARED
⭐ Result: 2 sessions, 2 devices
⭐ Logout ở Machine A → Không ảnh hưởng Machine B
```

### So Sánh

| Yếu Tố | 2 Tabs (Cùng Máy) | 2 Máy Khác |
|--------|------------------|-----------|
| **Browser Storage** | ✅ SHARED | ❌ KHÁC NHAU |
| **Session IDs** | ✅ 1 session_id | ❌ 2 session_ids |
| **Backend Sessions** | ✅ 1 entry | ❌ 2 entries |
| **Logout Tab 1** | ❌ Tab 2 cũng logout | ✅ Machine 2 vẫn ok |
| **Backend View** | "1 user, 1 session, 2 tabs" | "1 user, 2 sessions, 2 devices" |

---

## Device Fingerprinting - Lấy Thông Số Máy

### Vấn Đề: Device Hijacking

```
Legitimate User (Machine B)      Hacker (Machine A)
  |                                   |
  | GET /api/quizzes                  |
  | Cookie: xyz789 ──────────────> Backend
  |                                   |
  |                                   | GET /api/quizzes
  |                                   | Cookie: xyz789 (STOLEN!) ──> Backend
  |                                   |
  |                        ⚠️ Backend không biết
  |                        Cả 2 requests = user_id
  |                        Hacker lộ data!
```

### Giải Pháp: Device Fingerprinting

**Ý tưởng:** Backend lưu "dấu vân tay" (fingerprint) của device khi login. Mỗi request sau, kiểm tra xem fingerprint có khớp không.

**Frontend (KHÔNG cần code gì):**
```javascript
await fetch('/api/login', {
    body: JSON.stringify({username: 'john', password: '123'})
    // ❌ KHÔNG gửi fingerprint!
});
```

**Browser (tự động gửi headers):**
```
POST /api/login
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0
Accept-Language: vi-VN
Accept-Encoding: gzip, deflate
(IP: 192.168.1.100)
```

**Backend (tạo & lưu fingerprint):**
```python
def generate_device_fingerprint(request):
    user_agent = request.headers.get('User-Agent')
    language = request.headers.get('Accept-Language')
    ip_address = request.remote_addr
    encoding = request.headers.get('Accept-Encoding')
    
    # Combine + hash
    fingerprint_string = f"{user_agent}|{ip_address}|{language}|{encoding}"
    fingerprint = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    return fingerprint
    # Output: "abc123def456789abcdef0123456789..."

# Khi login: Lưu fingerprint
session['device_fingerprint'] = fingerprint  # "abc123..."

# Mỗi request: Kiểm tra
saved_fp = session.get('device_fingerprint')
current_fp = generate_device_fingerprint(request)

if saved_fp != current_fp:
    # ⚠️ Device khác!
    # Option 1: Block request
    # Option 2: Ask 2FA
    # Option 3: Log suspicious activity
    return {'success': False, 'message': 'Device mismatch'}, 403
```

---

## Browser Tự Động Gửi Thông Tin

### Ai Gửi Thông Tin Máy?

**❌ SAI:** Frontend gửi fingerprint / Frontend gửi device info

**✅ ĐÚNG:** Browser TỰ ĐỘNG gửi headers, Backend extract từ headers

```
Frontend Developer Code:
  await fetch('/api/login', {
      body: JSON.stringify({username, password})
      // ❌ KHÔNG code thông tin máy
  });

↓

Browser Tự Động Gửi:
  POST /api/login HTTP/1.1
  
  User-Agent: Mozilla/5.0 Windows Chrome
    └─ Browser tự detect OS + version
  
  Accept-Language: vi-VN
    └─ Browser đọc từ OS settings
  
  Accept-Encoding: gzip, deflate
    └─ Browser auto-detect capabilities
  
  (IP: 192.168.1.100)
    └─ Network layer auto-capture

↓

Backend Extract:
  user_agent = request.headers.get('User-Agent')
  language = request.headers.get('Accept-Language')
  ip_address = request.remote_addr
  
  fingerprint = SHA256(user_agent|ip|language|encoding)
```

### Thông Số Nào Được Gửi?

| Thông Số | Gửi? | Auto/Manual | Ví Dụ | Backend Access |
|---------|------|-----------|-------|---|
| **User-Agent** | ✅ | ✅ Auto | Mozilla/5.0 Windows | ✅ Có |
| **IP Address** | ✅ | ✅ Auto | 192.168.1.100 | ✅ Có |
| **Language** | ✅ | ✅ Auto | vi-VN,en-US | ✅ Có |
| **Encoding** | ✅ | ✅ Auto | gzip, deflate | ✅ Có |
| **Cookie** | ✅ | ✅ Auto | session_id=xyz | ✅ Có |
| **Screen Size** | ❌ | N/A | 1920x1080 | ❌ HTTP không gửi |
| **Device Memory** | ❌ | N/A | 16GB | ❌ HTTP không gửi |

### Cùng Code, Khác Machine = Khác Fingerprint

```
FRONTEND CODE (giống nhau trên 2 máy):
  await fetch('/api/login', {
      body: JSON.stringify({username: 'john', password: '123'})
  });

MACHINE A (Windows Chrome, IP 192.168.1.100):
  Browser gửi:
    User-Agent: Mozilla/5.0 (Windows...) Chrome/120.0
    IP: 192.168.1.100
    Language: vi-VN
  
  Fingerprint: SHA256("Windows|Chrome|192.168|vi") = "abc123..."

MACHINE B (Mac Firefox, IP 203.0.113.50):
  Browser gửi:
    User-Agent: Mozilla/5.0 (Macintosh...) Firefox/121.0
    IP: 203.0.113.50
    Language: en-US
  
  Fingerprint: SHA256("Mac|Firefox|203.0.113|en") = "xyz789..."

⭐ RESULT:
  - Cùng code
  - ❌ Khác fingerprint
  - ✅ Backend detect 2 devices khác
  - ✅ Có thể ask 2FA cho device mới
```

---

## Tóm Tắt Nhanh

```
1️⃣ USER LOGIN
   ├─ Frontend gửi: username + password
   ├─ Backend tạo: session + session_id
   ├─ Backend gửi: Set-Cookie: session_id
   └─ Browser lưu cookie

2️⃣ MỖI REQUEST SAU
   ├─ Browser tự động gửi: Cookie
   ├─ Frontend code: KHÔNG cần gửi username
   ├─ Backend nhận: Dùng session_id để lookup user
   └─ ✅ KHÔNG cần authentication mỗi request

3️⃣ 2 TABS CÙNG MÁYTHAI
   ├─ Cookies SHARED → CÙNG session_id
   ├─ Backend sees: 1 session, 2 tabs
   └─ Logout Tab 1 → Tab 2 cũng logout

4️⃣ 2 MÁY KHÁC NHAU
   ├─ Cookies KHÔNG shared → 2 session_ids
   ├─ Backend sees: 2 sessions, 2 devices
   └─ Logout Machine A → Machine B vẫn login

5️⃣ DEVICE HIJACKING DETECTION
   ├─ Browser gửi: User-Agent, IP, Language (auto)
   ├─ Backend tạo: fingerprint = SHA256(...)
   ├─ Backend kiểm tra: fingerprint khớp không?
   ├─ Nếu khác: Block hoặc ask 2FA
   └─ ✅ Phát hiện cookie bị đánh cắp
```

---

# Token (JWT) - Stateless Authentication

## Token Là Gì?

**Định nghĩa:** Token (JWT) = Chuỗi text được Backend tạo, Client lưu & gửi kèm mỗi request.

**So sánh với Cookie:**

| Tiêu Chí | Cookie | Token |
|--------|--------|-------|
| **Lưu ở đâu** | Browser cookie storage (tự động) | localStorage / biến (thủ công) |
| **Ai tạo** | Backend | Backend |
| **Ai gửi** | Browser tự động | Dev phải thêm header |
| **Ai quản lý** | Browser | Developer |
| **Cần database** | ✅ CÓ (có thể) | ❌ KHÔNG (stateless) |
| **Use case** | Web + Browser | Code, Mobile, Microservices |

---

## JWT Cấu Trúc

**Token = Header.Payload.Signature**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9obiIsImV4cCI6MTExMTExMTExMX0
.xyz1234567890...

├─ Header (định nghĩa)
│  {
│    "alg": "HS256" ← Algorithm
│    "typ": "JWT"    ← Type
│  }
│
├─ Payload (dữ liệu - dev custom)
│  {
│    "user_id": 123,
│    "username": "john",
│    "exp": 1111111111  ← Expiry time
│  }
│
└─ Signature (chữ ký - tạo từ secret key)
   HMACSHA256(Header + Payload, SECRET_KEY)
```

### Ví Dụ: Flask Tạo Token

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "my-secret-key-123"  # Dev giữ kín

def create_token(user_id):
    """Backend tạo token"""
    
    payload = {
        'user_id': user_id,
        'username': 'john',
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
    # Output: "eyJhbGc...xyz123..."

@app.route('/login', methods=['POST'])
def login():
    # Xác thực user
    user_id = 123
    
    # Tạo & trả token
    token = create_token(user_id)
    
    return {
        'message': 'Login success',
        'token': token  # ← Client phải lưu
    }
```

---

## ⚠️ PHÂN BIỆT: Web Login vs Developer API Token

### Trong Lý Thuyết (Simple Flow)

```python
# Mỗi lần code chạy, login để lấy token
response = requests.post('/login', json={...})
token = response.json()['token']
```

### Trong Thực Tế (Actual Flow)

```
BƯỚC 1: User Login qua WEB (Browser)
├─ Nhập username + password
├─ Server trả: Cookie (tự động)
└─ ❌ KHÔNG trả token ở đây!

BƯỚC 2: User Tạo API Token (Dashboard)
├─ Truy cập: https://example.com/settings/api-tokens
├─ Click: "Generate API Token"
├─ Server tạo: eyJhbGc...longtoken... (long-lived)
├─ User COPY token
└─ Token được dùng lâu dài (KHÔNG phải mỗi lần login)

BƯỚC 3: Developer Paste Token vào Code
├─ Lưu: .env hoặc environment variable
├─ KHÔNG hardcode trong source code
└─ Code dùng token này lâu dài (không login mỗi lần)
```

**Ví dụ:**
```python
# ❌ SAI: Mỗi lần login để nhận token (inefficient)
response = requests.post(
    'https://api.example.com/login',
    json={'username': 'john', 'password': '123'}
)
token = response.json()['token']  # ← Lấy mới mỗi lần

# ✅ ĐÚNG: Lấy token LẦN, dùng lâu dài
import os
token = os.getenv('API_TOKEN')  # eyJhbGc...
# ← Token được user copy từ dashboard, paste vào .env
```

---

## Cách Dùng Token (Frontend/Client)

### 1️⃣ Lấy/Copy Token (Một Lần)

```
BƯỚC A: User Login Web
└─ https://example.com/login

BƯỚC B: User Tạo Token ở Settings
├─ Truy cập: https://example.com/settings/api-tokens
├─ Click: "Generate New Token"
├─ Nhập: Token name = "My Script"
├─ Server trả: eyJhbGc...token...xyz
├─ ⚠️ One-time display! User phải copy ngay
└─ User copy token

BƯỚC C: Developer Paste vào Code
├─ Lưu vào .env:
│  API_TOKEN=eyJhbGc...token...xyz
│
├─ Read từ code:
│  import os
│  token = os.getenv('API_TOKEN')
└─ KHÔNG hardcode!
```

### 2️⃣ Dùng Token (Mỗi Request)

```python
# Python
import os
import requests

# Lấy token từ environment
token = os.getenv('API_TOKEN')

# ✅ Gửi request với token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.example.com/api/quizzes',
    headers=headers
)

quizzes = response.json()
```

### 3️⃣ Lưu Token An Toàn (Best Practice)

```bash
# File: .env (KHÔNG commit vào git!)
API_TOKEN=eyJhbGc...
ADMIN_USER=admin
QUIZ_API_URL=https://api.example.com

# File: .gitignore (bảo vệ .env)
.env
.env.local
token.txt
secrets/
```

```python
# Code: myapp.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv('API_TOKEN')
if not token:
    raise Exception("❌ API_TOKEN not found in .env!")

headers = {'Authorization': f'Bearer {token}'}
response = requests.get(
    f"{os.getenv('QUIZ_API_URL')}/api/quizzes",
    headers=headers
)
```

### 2️⃣ Gửi Request Với Token

```python
# PHẢI tự thêm token vào header!
headers = {
    'Authorization': f'Bearer {token}',  # ← Dev thêm
    'Content-Type': 'application/json'
}

response = requests.get(
    'http://api.example.com/api/quizzes',
    headers=headers
)

quizzes = response.json()
```

### 3️⃣ Helper Function (Best Practice)

```python
class APIClient:
    """Wrapper để tự động quản lý token"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        """Login & lưu token"""
        response = requests.post(
            f'{self.base_url}/login',
            json={'username': username, 'password': password}
        )
        self.token = response.json()['token']
        print(f"✅ Logged in, token: {self.token[:30]}...")
    
    def _get_headers(self):
        """Helper: Thêm token vào header"""
        if not self.token:
            raise Exception("❌ Not logged in!")
        
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def get_quizzes(self):
        """Tự động thêm token"""
        response = requests.get(
            f'{self.base_url}/api/quizzes',
            headers=self._get_headers()  # Token tự động kèm
        )
        return response.json()

# Sử dụng
client = APIClient('http://localhost:5000')
client.login('john', 'password123')
quizzes = client.get_quizzes()  # Token tự động được thêm
```

---

## Backend: Verify Token

### Stateless (KHÔNG lưu token)

```python
@app.route('/api/quizzes')
def get_quizzes():
    # Lấy token từ header
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    
    try:
        # Verify signature (KHÔNG cần database)
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # ✅ Signature hợp lệ = User đáng tin cậy
        return {'quizzes': get_user_quizzes(user_id)}, 200
    
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}, 401
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401

# ✅ Lợi ích:
# - Không cần database
# - Nhanh (chỉ verify signature)
# - Scalable (stateless)
# ❌ Nhược điểm:
# - Logout KHÔNG tức thì (phải chờ token hết hạn)
# - KHÔNG thể revoke token
```

### Stateful (CÓ lưu token - Token Blacklist)

```python
@app.route('/api/quizzes')
def get_quizzes():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    
    try:
        # 1. Verify signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # 2. TRA CỨU DATABASE - Token có bị revoke không?
        token_record = db.session.query(UserToken).filter_by(
            token_value=token
        ).first()
        
        if not token_record or token_record.status == 'revoked':
            return {'error': 'Token revoked'}, 401
        
        # ✅ Token hợp lệ
        return {'quizzes': get_user_quizzes(user_id)}, 200
    
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401

# ✅ Lợi ích:
# - Logout TỨC THỜ
# - Có thể revoke token
# - An toàn hơn
# ❌ Nhược điểm:
# - Cần database
# - Chậm hơn (phải query DB)
# - Có state (không pure stateless)
```

### Logout - Tùy Vào Kiểu

```python
# STATELESS: Không cần làm gì
@app.route('/logout', methods=['POST'])
def logout_stateless():
    # Token sẽ tự hết hạn sau 24h
    return {'message': 'Token will expire'}, 200

# STATEFUL: Revoke token
@app.route('/logout', methods=['POST'])
def logout_stateful():
    token = request.headers['Authorization'].split(' ')[1]
    
    token_record = db.session.query(UserToken).filter_by(
        token_value=token
    ).first()
    
    if token_record:
        token_record.status = 'revoked'
        db.commit()
    
    return {'message': 'Logged out'}, 200
```

---

## Cookie vs Token

```
┌─────────────────────────────────────────┐
│           BROWSER (Web)                 │
├─────────────────────────────────────────┤
│ ✅ Cookie: Tự động, dễ, bảo mật        │
│ ✅ Token: Phức tạp, thủ công            │
│ Khuyên: Dùng COOKIE                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      CODE / MOBILE / AUTOMATION         │
├─────────────────────────────────────────┤
│ ❌ Cookie: Không thể (không browser)    │
│ ✅ Token: Hoàn hảo, tự động hóa được    │
│ Khuyên: PHẢI dùng TOKEN                 │
└─────────────────────────────────────────┘
```

---

## Automation + Token (Stateless) - Thực Tế

**Điểm Mạnh:** Token cho phép tự động hóa 100% mà không cần Browser!

### Ví Dụ: Cron Job Tự Động Sync Dữ Liệu (Đúng Cách)

```bash
# File: .env (developer paste token vào đây - LẦN)
QUIZ_API_TOKEN=eyJhbGc...xyz789...
QUIZ_API_URL=http://api.quizgenerator.com
```

```python
# auto_sync.py - Chạy mỗi giờ tự động (KHÔNG login mỗi lần)

import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AutoSync:
    BASE_URL = os.getenv('QUIZ_API_URL')
    API_TOKEN = os.getenv('QUIZ_API_TOKEN')  # ← LẤY token từ .env (KHÔNG login!)
    
    def __init__(self):
        if not self.API_TOKEN:
            raise Exception("❌ QUIZ_API_TOKEN not found in .env!")
        
        print(f"[{datetime.now()}] ✅ Token loaded from .env")
    
    def sync_quizzes(self):
        """Tự động FETCH dữ liệu (dùng token có sẵn)"""
        headers = {
            'Authorization': f'Bearer {self.API_TOKEN}'  # ← Token từ .env
        }
        
        response = requests.get(
            f'{self.BASE_URL}/api/quizzes',
            headers=headers
        )
        
        quizzes = response.json()['quizzes']
        print(f"[{datetime.now()}] 📥 Got {len(quizzes)} quizzes")
        
        return quizzes
    
    def save_report(self, quizzes):
        """Tự động LƯU báo cáo"""
        import json
        
        filename = f"quizzes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(quizzes, f)
        
        print(f"[{datetime.now()}] 💾 Saved to {filename}")
    
    def run(self):
        """Quy trình tự động - KHÔNG cần login mỗi lần!"""
        quizzes = self.sync_quizzes()
        self.save_report(quizzes)

# Chạy tự động lặp lại (⚠️ KHÔNG login mỗi lần!)
if __name__ == '__main__':
    syncer = AutoSync()
    
    while True:
        syncer.run()
        time.sleep(3600)  # Đợi 1 giờ

# OUTPUT:
# [2026-04-10 10:00:00] ✅ Token loaded from .env
# [2026-04-10 10:00:00] 📥 Got 15 quizzes
# [2026-04-10 10:00:01] 💾 Saved to quizzes_20260410_100000.json
# [2026-04-10 11:00:00] 📥 Got 15 quizzes
# [2026-04-10 11:00:01] 💾 Saved to quizzes_20260410_110000.json
# ...
```

### Cách Setup (Thực Tế)

```bash
# BƯỚC 1: User Login Web & Copy Token
# ├─ Mở http://localhost:5000
# ├─ Login: admin/password123
# ├─ Vào: http://localhost:5000/settings/api-tokens
# ├─ Click: "Generate Token"
# └─ Copy: eyJhbGc...xyz789...

# BƯỚC 2: Developer Paste vào .env
# File: .env
QUIZ_API_TOKEN=eyJhbGc...xyz789...
QUIZ_API_URL=http://localhost:5000

# BƯỚC 3: Chạy script tự động
python auto_sync.py

# BƯỚC 4: Setup cron job (chạy mỗi giờ)
0 * * * * /usr/bin/python3 /home/user/auto_sync.py

# ✅ XONG! Token được dùng lâu dài, KHÔNG login mỗi lần!
```

### ❌ SAI CÁCH (Vừa login vừa lấy token mỗi lần)

```python
# ❌ KHÔNG NÊN: Login mỗi lần script chạy
class AutoSyncWrong:
    BASE_URL = 'http://api.quizgenerator.com'
    USERNAME = 'admin'
    PASSWORD = 'secret123'  # ❌ Hardcode password = risks!
    
    def __init__(self):
        self.token = None
    
    def login(self):
        """❌ Mỗi lần run = login lại (inefficient!)"""
        response = requests.post(
            f'{self.BASE_URL}/login',
            json={'username': self.USERNAME, 'password': self.PASSWORD}
        )
        self.token = response.json()['token']
        print(f"🔐 Logged in, took time...")
    
    def sync_quizzes(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(.....)
    
    def run(self):
        self.login()  # ❌ Login lại mỗi lần!
        self.sync_quizzes()

# ❌ Vấn đề:
# - Mỗi giờ login 1 lần (tối ra viết logs)
# - Hardcode password trong code (security risk)
# - Chậm (phải wait auth server)
# - Nếu server reject → script fail
```

### ✅ ĐÚNG CÁCH (Dùng token từ .env)

```python
# ✅ ĐÚNG: Dùng token từ .env, KHÔNG login
class AutoSyncCorrect:
    BASE_URL = os.getenv('QUIZ_API_URL')
    API_TOKEN = os.getenv('API_TOKEN')  # ← Load từ .env (SET LẦN)
    
    def sync_quizzes(self):
        """Dùng token từ .env, KHÔNG login!"""
        headers = {'Authorization': f'Bearer {self.API_TOKEN}'}
        response = requests.get(
            f'{self.BASE_URL}/api/quizzes',
            headers=headers
        )
        return response.json()
    
    def run(self):
        self.sync_quizzes()  # ✅ KHÔNG gọi login!

# ✅ Lợi ích:
# - Nhanh (skip auth step)
# - An toàn (KHÔNG hardcode password)
# - Đơn giản (1 dòng load token)
# - Scalable (token có thể là 90 days, vài tháng, ...)
```

---

## So Sánh: Stateless vs Stateful Token

| Khía Cạnh | Stateless (JWT Thơm) | Stateful (JWT + DB) |
|----------|--------|---------|
| **Lưu token** | ❌ KHÔNG | ✅ CÓ (blacklist) |
| **Verify** | Chỉ check signature | Check signature + DB |
| **Logout** | ❌ KHÔNG tức thì | ✅ TỨC THỜ |
| **Revoke** | ❌ KHÔNG thể | ✅ CÓ thể |
| **Database** | ❌ KHÔNG cần | ✅ CẦN |
| **Performance** | ✅ Nhanh | ⚠️ Chậm hơn |
| **Scalability** | ✅ Cao | ⚠️ Thấp hơn |
| **Use case** | Microservices, API | Enterprise, Security |

**Khuyên cho QuizGenerator:** Dùng **Stateful** vì:
- Exam/Quiz cần bảo mật cao
- Logout phải tức thì
- Cần trace user hoạt động
- Có thể revoke token nếu cheating

---

## Tóm Tắt Token (Đúng Cách)

```
THỰC TẾ - BƯỚC TỪ ĐẦU ĐẾN CUỐI:

1️⃣ USER LOGIN WEB (Browser)
   ├─ Mở website
   ├─ Nhập username + password
   ├─ Server set: Cookie (tự động)
   └─ ❌ KHÔNG trả token ở đây!

2️⃣ USER TẠO API TOKEN (Dashboard)
   ├─ Truy cập: /settings/api-tokens
   ├─ Click: "Generate New Token"
   ├─ Server tạo: eyJhbGc...longtoken... (long-lived)
   ├─ User COPY token
   └─ ⚠️ One-time display!

3️⃣ DEVELOPER PASTE TOKEN VÀO .env
   ├─ Tạo file: .env
   │  API_TOKEN=eyJhbGc...longtoken...
   │  API_URL=http://api.example.com
   │
   ├─ Thêm .env vào .gitignore
   └─ ✅ KHÔNG commit vào git!

4️⃣ CODE LOAD TOKEN TỪ .env
   ├─ import os
   │  from dotenv import load_dotenv
   │
   ├─ load_dotenv()
   │  token = os.getenv('API_TOKEN')
   │
   └─ ✅ KHÔNG hardcode token!

5️⃣ DÙNG TOKEN MỖI REQUEST
   ├─ headers = {'Authorization': f'Bearer {token}'}
   ├─ requests.get('/api/...', headers=headers)
   └─ ✅ Token được dùng lâu dài (KHÔNG login mỗi lần)

6️⃣ AUTOMATION / CRON JOB
   ├─ Script chạy định kỳ
   ├─ Load token từ .env
   ├─ Gửi request (token từ env)
   └─ ✅ 100% tự động, KHÔNG cần user

⭐ KEY POINTS:
- Token tạo LẦN, dùng lâu dài
- Lưu ở .env hoặc environment variable
- KHÔNG lưu ở source code
- KHÔNG login mỗi lần script chạy
- Mỗi request tự động kèm token từ environment
```
