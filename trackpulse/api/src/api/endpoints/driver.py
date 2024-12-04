from typing import List
from fastapi import APIRouter
from src.schemas import Driver
from src.api.deps import SessionDeps

router = APIRouter()

@router.get("/driver/{driver_id}", status_code=200, response_model=Driver)
def get_driver(driver_id: int, db: SessionDeps) -> Driver:
  return db.query(Driver).filter(Driver.id == driver_id).first()

@router.get("/drivers", status_code=200, response_model=List[Driver])
def get_drivers(db: SessionDeps) -> List[Driver]:
  return db.query(Driver).all()

