from pydantic import BaseModel
from typing import Optional, List

class HATEOASLinkObject(BaseModel):
    name: str
    method: str
    href: str

class HATEOASLinks(BaseModel):
    self: HATEOASLinkObject
    actions: Optional[List[HATEOASLinkObject]] = None
    related: Optional[List[HATEOASLinkObject]] = None