from fastapi import FastAPI

app = FastAPI(title="Onde Alaga API")


@app.get("/healthz")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
