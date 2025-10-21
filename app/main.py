from fastapi import FastAPI

app = FastAPI(title="EduMatch API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao EduMatch API 🚀"}
