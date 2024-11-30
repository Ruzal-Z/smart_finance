from fastapi import FastAPI

app = FastAPI(
    title = "",
    version = "0.1.0",
    description = "",
    openapi_url = "/api/v1/openapi.json"
) 

@app.get("/")
def read_root():
    return {"message": "Begin"}