from pydantic import BaseModel, Field
from typing import List, Dict


class ObjectNode(BaseModel):
    id: str
    name: str
    attributes: Dict[str, str] = {}


class Relation(BaseModel):
    subject: str
    predicate: str
    object: str


class SceneGraph(BaseModel):
    objects: List[ObjectNode]
    relations: List[Relation]
    confidence: Dict[str, float]