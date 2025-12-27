from fastapi import FastAPI, Request
from pydantic import BaseModel
from pipeline.run import run_fest_scrape  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sponsor Scraper API is running!"}

class ScrapeRequest(BaseModel):
    url: str
    fest_name: str
    college: str
    year: int

from fastapi.concurrency import run_in_threadpool

@app.post("/api/scrape")
async def scrape_fest(data: ScrapeRequest):
    try:
        await run_in_threadpool(
            run_fest_scrape,
            data.url,
            data.fest_name,
            data.college,
            data.year
        )
        return {"message": "Scraping completed successfully!"}
    except Exception as e:
        return {"error": str(e)}
