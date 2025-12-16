from sqlalchemy.orm import Session
from db.model import Fest, Company, Sponsorship, Source, ExtractedEntity

def get_or_create_fests(db: Session, name: str, college: str, year: int):
    fest = db.query(Fest).filter(Fest.name == name, Fest.college == college, Fest.year == year).first()
    if fest:
        return fest

    fest = Fest(name=name, college=college, year=year)
    db.add(fest)
    db.flush()
    return fest

def get_or_create_source(db: Session, fest_id: int, url: str):
    source = db.query(Source).filter(Source.fest_id == fest_id, Source.url == url).first()
    if source:
        return source

    source = Source(fest_id=fest_id, url=url)
    db.add(source)
    db.flush()
    return source

def save_extracted_entity(db: Session, source_id: int, raw_text: str, extracted_name: str | None,
    entity_type: str,confidence: float):
    
    entity = ExtractedEntity(
        source_id=source_id,
        raw_text=raw_text,
        extracted_name=extracted_name,
        entity_type=entity_type,
        confidence=confidence,
    )
    db.add(entity)
    db.flush()

    return entity

def get_or_create_company(db, name):
    company = (
        db.query(Company)
        .filter(Company.name.ilike(name))
        .first()
    )

    if company:
        return company

    company = Company(name=name.strip())
    db.add(company)
    db.flush()
    return company

def get_or_create_sponsorship(db: Session, fest_id: int, company_id: int, group_name: str | None,
    confidence: float | None):
    
    sponsorship = db.query(Sponsorship).filter(
        Sponsorship.fest_id == fest_id,
        Sponsorship.company_id == company_id
    ).first()

    if sponsorship:
            # enrich if better data arrives
            if not sponsorship.tier and group_name:
                sponsorship.tier = group_name
            if confidence and (sponsorship.confidence or 0) < confidence:
                sponsorship.confidence = confidence
            return sponsorship

    sponsorship = Sponsorship(
            fest_id=fest_id,
            company_id=company_id,
            tier=group_name,          # using tier column for now
            confidence=confidence,
        )
    db.add(sponsorship)
    db.flush()
    return sponsorship

def save_extracted_entity(
    db,
    source_id,
    raw_text,
    extracted_name,
    confidence,
    extraction_method,
):
    entity = ExtractedEntity(
        source_id=source_id,
        raw_text=raw_text,
        extracted_name=extracted_name,
        entity_type="SPONSOR",
        confidence=confidence,
    )
    db.add(entity)
    db.flush()
    return entity

from sqlalchemy import func


def count_sponsors_for_fest(db, fest_id: int) -> int:
    return (
        db.query(func.count(Sponsorship.id))
        .filter(Sponsorship.fest_id == fest_id)
        .scalar()
    )

 