# app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from db.database import Base


class Fest(Base):
    __tablename__ = "fests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    college = Column(String(500), nullable=False)
    year = Column(Integer, nullable=False)

    sponsorships = relationship("Sponsorship", back_populates="fest")
    sources = relationship("Source", back_populates="fest")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), unique=True, nullable=False)
    website = Column(String(200))

    sponsorships = relationship("Sponsorship", back_populates="company")


class Sponsorship(Base):
    __tablename__ = "sponsorships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fest_id = Column(Integer, ForeignKey("fests.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    tier = Column(String(100))
    confidence = Column(Float)

    fest = relationship("Fest", back_populates="sponsorships")
    company = relationship("Company", back_populates="sponsorships")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fest_id = Column(Integer, ForeignKey("fests.id"), nullable=False)

    url = Column(String(1000), nullable=False)
    is_parsed = Column(Boolean, default=False)

    fest = relationship("Fest", back_populates="sources")
    extracted_entities = relationship("ExtractedEntity", back_populates="source")


class ExtractedEntity(Base):
    __tablename__ = "extracted_entities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    raw_text = Column(String(2000), nullable=False)
    extracted_name = Column(String(300))
    entity_type = Column(String(100))
    confidence = Column(Float)

    source = relationship("Source", back_populates="extracted_entities")
