# Hello To-Do - Cấp 0

Mục tiêu: tạo API FastAPI tối thiểu chạy được.

## Yêu cầu Cấp 0

- Tạo project FastAPI
- Endpoint:
	- `GET /health` -> `{ "status": "ok" }`
	- `GET /` -> message chào

## Các file liên quan

- `app/main.py`: định nghĩa FastAPI app và 2 endpoint
- `requirements.txt`: dependencies tối thiểu (`fastapi`, `uvicorn[standard]`)

## Cách chạy

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Chạy như trước (không dùng .venv)

Nếu terminal đang hiện `(.venv)`, thoát môi trường ảo trước:

```powershell
deactivate
```

Sau đó chạy lại lệnh ở trên bằng Python hệ thống.

Sau khi chạy, mở:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Test nhanh

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```

Kết quả mong đợi:

- `/health` trả về: `{ "status": "ok" }`
- `/` trả về JSON có trường `message`

---

# Cấp 1 - CRUD cơ bản (dữ liệu trong RAM)

Mục tiêu: làm CRUD với list/dict trong bộ nhớ (chưa dùng DB).

## Model ToDo

- `id: int`
- `title: str`
- `is_done: bool = False`

## Endpoints gợi ý

- `POST /todos` tạo todo
- `GET /todos` lấy danh sách
- `GET /todos/{id}` lấy chi tiết
- `PUT /todos/{id}` cập nhật toàn bộ
- `DELETE /todos/{id}` xóa

## Tiêu chí đạt

- Validate dữ liệu bằng Pydantic
- Trả lỗi đúng khi không tìm thấy (`404`)

## Test nhanh Cấp 1

```powershell
# Tạo mới
curl -X POST http://127.0.0.1:8000/api/v1/todos -H "Content-Type: application/json" -d '{"title":"Học FastAPI"}'

# Lấy danh sách
curl http://127.0.0.1:8000/api/v1/todos

# Lấy chi tiết
curl http://127.0.0.1:8000/api/v1/todos/1

# Cập nhật toàn bộ
curl -X PUT http://127.0.0.1:8000/api/v1/todos/1 -H "Content-Type: application/json" -d '{"title":"Học FastAPI kỹ hơn","is_done":true}'

# Xóa
curl -X DELETE http://127.0.0.1:8000/api/v1/todos/1
```

---

# Cấp 2 - Validation xịn + filter/sort/pagination

Mục tiêu: API giống thực tế hơn.

## Yêu cầu

- `title` không được rỗng, độ dài `3-100`
- `GET /todos` hỗ trợ:
	- filter: `is_done=true/false`
	- search: `q=keyword` (tìm theo title)
	- sort: `sort=created_at` hoặc `sort=-created_at`
	- pagination: `limit`, `offset`

## Tiêu chí đạt

- Response có cấu trúc:

```json
{
	"items": [],
	"total": 123,
	"limit": 10,
	"offset": 0
}
```

## Test nhanh Cấp 2

```powershell
# Filter theo trạng thái hoàn thành
curl "http://127.0.0.1:8000/api/v1/todos?is_done=true"

# Search theo title
curl "http://127.0.0.1:8000/api/v1/todos?q=fastapi"

# Sort theo thời gian tạo tăng dần
curl "http://127.0.0.1:8000/api/v1/todos?sort=created_at"

# Pagination
curl "http://127.0.0.1:8000/api/v1/todos?limit=5&offset=0"
```

---

# Cấp 3 - Tách tầng (router/service/repository) + cấu hình chuẩn

Mục tiêu: viết như dự án thật.

## Yêu cầu

- Tách thư mục:
	- `routers/`, `schemas/`, `services/`, `repositories/`, `core/`
- Dùng `APIRouter`, prefix `/api/v1`
- Config bằng `pydantic-settings` (env):
	- `APP_NAME`, `DEBUG`, ...

## Tiêu chí đạt

- Không viết logic DB trong router
- Có file `main.py` sạch

## Cấu trúc thư mục mẫu (Cấp 3)

```text
app/
	core/
	routers/
	schemas/
	services/
	repositories/
	main.py
```

## Cách chạy (Cấp 3)

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Nếu dùng prefix `/api/v1`, endpoint sẽ thành:

- `GET /api/v1/todos`
- `POST /api/v1/todos`
- ...

---

# Cấp 4 - Dùng Database (SQLite/PostgreSQL) + ORM

Mục tiêu: lưu dữ liệu thật.

## Yêu cầu

- Dùng `SQLModel` (trên nền SQLAlchemy)
- Bảng `todos` có các cột:
	- `id`, `title`, `description`, `is_done`, `created_at`, `updated_at`
- Migration bằng `Alembic`

## Endpoints thêm

- `PATCH /api/v1/todos/{id}` cập nhật một phần
- `POST /api/v1/todos/{id}/complete` đánh dấu hoàn thành

## Tiêu chí đạt

- `created_at` và `updated_at` được set tự động khi tạo/cập nhật
- Pagination thực sự từ DB qua `offset/limit`

## Cấu hình DB

File `.env` (tùy chọn):

```env
APP_NAME=Hello To-Do
DEBUG=false
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///./todos.db
```

Bạn có thể đổi sang PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/tododb
```

## Migration với Alembic

```powershell
pip install -r requirements.txt
alembic upgrade head
```

Nếu DB đã tồn tại từ bản chạy thử trước đó (table `todos` đã được tạo sẵn), dùng lệnh sau 1 lần để đồng bộ version:

```powershell
alembic stamp head
```

Nếu muốn tạo revision mới:

```powershell
alembic revision --autogenerate -m "your message"
alembic upgrade head
```

## Chạy ứng dụng

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Test nhanh Cấp 4

```powershell
# Tạo todo
curl -X POST http://127.0.0.1:8000/api/v1/todos -H "Content-Type: application/json" -d '{"title":"Học SQLModel","description":"Bài Cấp 4"}'

# List có pagination/filter/search/sort từ DB
curl "http://127.0.0.1:8000/api/v1/todos?limit=10&offset=0"
curl "http://127.0.0.1:8000/api/v1/todos?is_done=false"
curl "http://127.0.0.1:8000/api/v1/todos?q=sql"
curl "http://127.0.0.1:8000/api/v1/todos?sort=-created_at"

# Cập nhật một phần
curl -X PATCH http://127.0.0.1:8000/api/v1/todos/1 -H "Content-Type: application/json" -d '{"is_done":true}'

# Đánh dấu hoàn thành
curl -X POST http://127.0.0.1:8000/api/v1/todos/1/complete
```

---

# Cấp 5 - Authentication + User riêng

Mục tiêu: mỗi user có to-do riêng.

## Yêu cầu

- Bảng `users`: `id`, `email`, `hashed_password`, `is_active`, `created_at`
- JWT login:
	- `POST /api/v1/auth/register`
	- `POST /api/v1/auth/login`
	- `GET /api/v1/auth/me`
- Todo gắn `owner_id`

## Tiêu chí đạt

- User A không xem/xóa todo của User B
- Password hash bằng `passlib/bcrypt`

## Cấu hình thêm cho JWT

Trong `.env` (tuỳ chọn):

```env
JWT_SECRET_KEY=change-this-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

## Migration Cấp 5

```powershell
alembic upgrade head
```

## Luồng test nhanh Cấp 5

```powershell
# 1) Đăng ký
curl -X POST http://127.0.0.1:8000/api/v1/auth/register -H "Content-Type: application/json" -d '{"email":"usera@example.com","password":"secret123"}'

# 2) Đăng nhập lấy token
curl -X POST http://127.0.0.1:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{"email":"usera@example.com","password":"secret123"}'

# 3) Gọi /auth/me
curl http://127.0.0.1:8000/api/v1/auth/me -H "Authorization: Bearer <TOKEN>"

# 4) Tạo todo của user hiện tại
curl -X POST http://127.0.0.1:8000/api/v1/todos -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"title":"Todo cua user A"}'
```

Ghi chú bảo mật:

- Tất cả endpoint Todo yêu cầu token hợp lệ.
- Truy vấn Todo luôn lọc theo `owner_id = current_user.id`, nên không thể xem/sửa/xóa chéo user.
