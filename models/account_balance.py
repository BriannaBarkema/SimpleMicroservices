from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date, datetime

class AccountBalanceBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Family History ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    account_balance: float = Field(
        None,
        description="Balanced owed at facility",
        json_schema_extra={"example": 42.50 },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "account_balance": 120.21,
                }
            ]
        }
    }

class AccountBalanceCreate(AccountBalanceBase):
    """Creation payload for account balance."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "account_balance": 120.21,
                }
            ]
        }
    }

class AccountBalanceUpdate(AccountBalanceBase):
    """Partial update for account balance; supply only fields to change. ID comes from the path, not the body"""
    account_balance: Optional[float] = Field(None, json_schema_extra={"example": 192.43})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "account_balance": 192.43,
                }
            ]
        }
    }

class AccountBalanceRead(AccountBalanceBase):
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
                    "account_balance": 192.43,
                }
            ]
        }
    }