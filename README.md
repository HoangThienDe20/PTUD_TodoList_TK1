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
