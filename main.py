from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

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

# Root route: welcome message or redirect
@app.get("/")
def root():
    return {"message": "Welcome to the marks API. Use /api?name=Alice&name=Bob"}

# Or use redirect instead:
# @app.get("/")
# def redirect_to_api():
#     return RedirectResponse(url="/api")

@app.get("/api")
def get_marks(name: list[str] = []):
    result = [marks_data.get(n, 0) for n in name]
    return {"marks": result}
