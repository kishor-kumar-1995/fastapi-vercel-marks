from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from mangum import Mangum  # <-- important for Vercel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def root():
    return {"message": "Welcome to the marks API. Use /api?name=Alice&name=Bob"}

@app.get("/api")
def get_marks(name: list[str] = []):
    result = [marks_data.get(n, 0) for n in name]
    return {"marks": result}

# Create handler for Vercel
handler = Mangum(app)
