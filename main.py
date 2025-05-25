# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example student marks data
marks_data = {
    "Alice": 10,
    "Bob": 20,
    "Charlie": 30
}

@app.get("/api")
def get_marks(name: list[str] = []):
    result = [marks_data.get(n, 0) for n in name]
    return {"marks": result}
