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

class ScrapeRequest(BaseModel):
    url: str
    fest_name: str
    college: str
    year: int

@app.post("/api/scrape")
async def scrape_fest(data: ScrapeRequest):
    try:
        run_fest_scrape(
            fest_url=data.url,
            fest_name=data.fest_name,
            college=data.college,
            year=data.year
        )
        return {"message": "Scraping completed successfully!"}
    except Exception as e:
        return {"error": str(e)}
