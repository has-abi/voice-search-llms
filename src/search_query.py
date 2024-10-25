from typing import Optional

from pydantic import BaseModel, Field


class Experience(BaseModel):
    """Expérience requise"""
    min: Optional[int] = Field(default=None, description="Minimum d'expérience en années.")
    max: Optional[int] = Field(default=None, description="Maximum d'expérience en années.")


class SearchQuery(BaseModel):
    """La requête de recherche"""
    localisation: Optional[str] = Field(default=None, description="Localisation souhaitée.")
    niveau_etudes: Optional[str] = Field(default=None, description="Niveau d'étude souhaité.")
    experience: Optional[Experience] = Field(default=None, description="Expérience souhaité.")
    competences: Optional[list[str]] = Field(default=[], description="Compétences requises.")
    langues_parlees: Optional[list[str]] = Field(default=[], description="Langues parlées requises.")
