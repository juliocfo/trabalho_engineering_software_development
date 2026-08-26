"""
API minima (FastAPI) que expoe o Config Validator como microsservico.
"""
from fastapi import FastAPI
from pydantic import BaseModel

from .validator import validate_config

app = FastAPI(title="Config Validator", version="1.0.0")


class ConfigInput(BaseModel):
    config: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/validate")
def validate(payload: ConfigInput):
    return validate_config(payload.config)
