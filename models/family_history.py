from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date, datetime

class FamilyHistoryBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Family History ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    father: Optional[str] = Field(
        None,
        description="Father's health history",
        json_schema_extra={"example": "alzheimer's disease"},
    )
    mother: Optional[str] = Field(
        None,
        description="Mother's health history",
        json_schema_extra={"example": "endometriosis"},
    )
    sister: Optional[str] = Field(
        None,
        description="Sister's health history",
        json_schema_extra={"example": "Diabetes"},
    )
    brother: Optional[str] = Field(
        None,
        description="Brother's health history",
        json_schema_extra={"example": "Diabetes"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "father": "IBS",
                    "mother": "diabetes",
                    "sister": "diabetes",
                }
            ]
        }
    }

class FamilyHistoryCreate(FamilyHistoryBase):
    """Creation payload for Family History."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "father": "IBS",
                    "mother": "diabetes",
                    "sister": "diabetes",
                    "brother": "blood clots"
                }
            ]
        }
    }

class FamilyHistoryUpdate(FamilyHistoryBase):
    """Partial update for health history; supply only fields to change. ID comes from the path, not the body"""
    father: Optional[str] = Field(None, json_schema_extra={"example": "alzheimer's disease"})
    mother: Optional[str] = Field(None, json_schema_extra={"example": "endometriosis"})
    sister: Optional[str] = Field(None, json_schema_extra={"example": "Diabetes"})
    brother: Optional[str] = Field(None, json_schema_extra={"example": "Diabetes"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                 {
                    "father": "IBS",
                    "mother": "diabetes",
                    "sister": "diabetes",
                    "brother": "blood clots",
                }
             ]
        }
     }

class FamilyHistoryRead(FamilyHistoryBase):
    """Server representation returned to clients."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "father": "IBS",
                    "mother": "diabetes",
                    "sister": "diabetes",
                    "brother": "blood clots",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }