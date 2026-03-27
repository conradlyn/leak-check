from typing import Optional, List

from pydantic import BaseModel


class ModelResponseSource(BaseModel):
    id: int
    source: Optional[str]

class ModelResponsePerson(BaseModel):
    id: Optional[str]
    name: Optional[str]
    receiver: Optional[str]
    nickname: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    car: Optional[str]
    email: Optional[str]
    qq: Optional[int]
    weibo: Optional[int]
    contact:Optional[str]
    company: Optional[str]
    source: Optional[str]

class ModelResponsePersonAggregated(BaseModel):
    id: List[Optional[str]]
    name: List[Optional[str]]
    receiver: List[Optional[str]]
    nickname: List[Optional[str]]
    phone: List[Optional[str]]
    address: List[Optional[str]]
    car: List[Optional[str]]
    email: List[Optional[str]]
    qq: List[Optional[int]]
    weibo: List[Optional[int]]
    contact: List[Optional[str]]
    company: List[Optional[str]]
    source: List[Optional[str]]