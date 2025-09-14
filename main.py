from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.family_history import FamilyHistoryCreate, FamilyHistoryRead, FamilyHistoryUpdate
from models.account_balance import AccountBalanceCreate, AccountBalanceRead, AccountBalanceUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
family_histories: Dict[UUID, FamilyHistoryRead] = {}
account_balances: Dict[UUID, AccountBalanceRead] = {}
addresses: Dict[UUID, AddressRead] = {}

app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Family History endpoints
# -----------------------------------------------------------------------------
@app.post("/family-histories", response_model=FamilyHistoryRead, status_code=201)
def create_family_history(family_history: FamilyHistoryCreate) -> FamilyHistoryRead:
    if family_history.id in family_histories:
        raise HTTPException(status_code=400, detail="Family History with this ID already exists")
    history_read = FamilyHistoryRead(**family_history.model_dump())
    family_histories[history_read.id] = history_read
    return family_histories[history_read.id]

@app.get("/family-histories", response_model=List[FamilyHistoryRead])
def get_family_histories(
    father: Optional[str] = Query(None, description="Filter by father's health history"),
    mother: Optional[str] = Query(None, description="Filter by mother's health history"),
    sister: Optional[str] = Query(None, description="Filter by sister's health history"),
    brother: Optional[str] = Query(None, description="Filter by brother's health history"),
):
    results = list(family_histories.values())

    if father is not None:
        results = [p for p in results if p.father == father]
    if mother is not None:
        results = [p for p in results if p.mother == mother]
    if sister is not None:
        results = [p for p in results if p.sister == sister]
    if brother is not None:
        results = [p for p in results if p.brother == brother]

    return results

@app.get("/family-histories/{history_id}", response_model=FamilyHistoryRead)
def get_family_history(history_id: UUID):
    if history_id not in family_histories:
        raise HTTPException(status_code=404, detail="Family history not found")
    return family_histories[history_id]

@app.patch("/family-histories/{history_id}", response_model=FamilyHistoryRead)
def update_family_history(history_id: UUID, update: FamilyHistoryUpdate):
    if history_id not in family_histories:
        raise HTTPException(status_code=404, detail="Family history not found")
    stored = family_histories[history_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    family_histories[history_id] = FamilyHistoryRead(**stored)
    return family_histories[history_id]

# -----------------------------------------------------------------------------
# Account Balance endpoints
# -----------------------------------------------------------------------------
@app.post("/account-balances", response_model=AccountBalanceRead, status_code=201)
def create_account_balance(account_balance: AccountBalanceCreate) -> AccountBalanceRead:
    # Each person gets its own UUID; stored as PersonRead
    balance_read = AccountBalanceRead(**account_balance.model_dump())
    account_balances[balance_read.id] = balance_read
    return account_balances[balance_read.id]

@app.get("/account-balances", response_model=List[AccountBalanceRead])
def get_account_balance(
    account_balance: float = Query(None, description="Filter by balance"),
):
    results = list(account_balances.values())

    if account_balance is not None:
        results = [p for p in results if p.account_balance == account_balance]

    return results

@app.get("/account-balances/{account_id}", response_model=AccountBalanceRead)
def get_account_balances(account_id: UUID):
    if account_id not in account_balances:
        raise HTTPException(status_code=404, detail="Account balance not found")
    return account_balances[account_id]

@app.patch("/account-balances/{account_id}", response_model=AccountBalanceRead)
def update_account_balance(account_id: UUID, update: AccountBalanceUpdate):
    if account_id not in account_balances:
        raise HTTPException(status_code=404, detail="Account balance not found")
    stored = account_balances[account_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    account_balances[account_id] = AccountBalanceRead(**stored)
    return account_balances[account_id]

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
