from pydantic import BaseModel
from typing import List, Dict, Any


class TwinObject(BaseModel):
    id: str
    name: str
    ifc_class: str
    position: List[float] = [0.0, 0.0, 0.0]
    bbox: List[float] = [0, 0, 0, 1, 1, 1]


class TwinRelation(BaseModel):
    subject: str
    predicate: str
    object: str


class TwinState(BaseModel):
    objects: List[TwinObject]
    relations: List[TwinRelation]
    geometry: Dict[str, Any]
    constraints: List[Dict]
    confidence: Dict[str, float]