import fastapi
import uvicorn

from service import login_service

app = fastapi.FastAPI()

app.include_router(login_service.router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
