from fastapi import FastAPI

app = FastAPI(title="Hello To-Do")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Xin chao from FastAPI Hello To-Do"}
