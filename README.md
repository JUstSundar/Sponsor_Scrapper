# Sponsor Scrapper
## About 
This is a robust, production-grade web application with a scraping pipeline to automatically discover, extract, and structure sponsor information from college fest websites. This project is designed to handle real-world, messy websites, with different strucutres(e.g. Mood Indigo, IIT fests, cultural & technical festivals) where sponsor data is presented visually rather than semantically. 

## Design Flow
Users feed URL, Fest name, College name, Fest year to the React website -> HTTP request to Backend -> Scrapping pipeline switched on -> Scrape website -> Insert information on DB -> Inform frontend "Scraping completed"

## Tech stack
Frontend :- React JS
Backend :- Python, FastAPI
Hosting :- Render(Backend), Vercel(Frontend)
Scraping :- Playwright(Chromium)
Production :- Docker

## Usage
This application has been deployeed and is in use currently for official purposes of the Festember Marketing team 2026. This was done on a short duration of 1 week by me to simplify sponsor collection process. Incase you have any improvements to this application, feel free to raise pull requests

## Frontend View
<img width="1865" height="929" alt="Screenshot From 2025-12-31 10-53-18" src="https://github.com/user-attachments/assets/5806d09b-c1b8-47f6-83c1-0b69d9d808b3" />


