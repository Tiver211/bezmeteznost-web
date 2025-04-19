import os
from uuid import uuid4

import bcrypt
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

@app.get("/api/ping")
def ping():
    return JSONResponse(status_code=200, content="PROOOOOOOOOOD")

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:443")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))