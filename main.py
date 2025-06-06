from uvicorn import run as run_app

from app import app

if __name__ == "__main__":
    run_app(app, host="0.0.0.0", port=3000)
