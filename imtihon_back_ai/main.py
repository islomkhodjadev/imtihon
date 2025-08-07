from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.websocket_main import router as websocket_router

app = FastAPI()
app.include_router(websocket_router)


@app.get("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
