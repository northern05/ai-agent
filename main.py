import uvicorn
from app import app


if __name__ == '__main__':
    uvicorn.run("main:app", port=6010, reload=True)