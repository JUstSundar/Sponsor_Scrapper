from db.database import SessionLocal
from db.helpers import (
    get_or_create_fests,
    get_or_create_source,
    save_extracted_entity,
    get_or_create_company,
    get_or_create_sponsorship,
    count_sponsors_for_fest
)
from extractor.extract import (
    extract_sponsors_advanced
)

from extractor.fetch import fetch_html_js

def run_fest_scrape(
    fest_url: str,
    fest_name: str,
    college: str,
    year: int,
):
    db = SessionLocal()

    try:
        # create Fest
        fest = get_or_create_fests(
            db,
            name=fest_name,
            college=college,
            year=year,
        )
        print("Fest entry done")

        # create source page
        source = get_or_create_source(
            db,
            fest_id=fest.id,
            url=fest_url,
        )
        print("Source entry done")

        existing_count = count_sponsors_for_fest(db, fest.id) 

        if source.is_parsed:
            print("Source already parsed, Allowing re-parse.")

        # Skip if already parsed
        # if source.is_parsed and existing_count>10:  
            # print("Source already parsed, skipping.")
            # return

        # 3️⃣ Fetch HTML
        html = fetch_html_js(fest_url)

        # 4️⃣ Extract sponsors
        sponsors = extract_sponsors_advanced(
            html=html,
            base_url=fest_url,
        )
        print(f"Extracted {len(sponsors)} sponsors.")

        # 5️⃣ Persist results
        for s in sponsors:
            save_extracted_entity(
                db=db,
                source_id=source.id,
                raw_text=s["raw_text"],
                extracted_name=s["name"],
                confidence=s["confidence"],
                extraction_method=s.get("extraction_method","unknown"), 
            )

            company = get_or_create_company(
                db=db,
                name=s["name"],
            )

            get_or_create_sponsorship(
                db=db,
                fest_id=fest.id,
                company_id=company.id,
                group_name=s.get("tier"),
                confidence=s["confidence"],
            )

        # 6️⃣ Mark source as parsed
        source.is_parsed = True

        db.commit()
        print(f"Inserted {len(sponsors)} sponsors.")

    except Exception as e:
        print(f"Error during fest scrape: {e}")
        print("Rolling back DB session.")
        db.rollback()
        raise e

    finally:
        db.close()
