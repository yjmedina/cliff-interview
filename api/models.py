from pydantic import BaseModel
from typing import Literal

Categories = Literal['Productivity', 'Design', 'Communication', 'Development', 'Finance', 'Marketing']

class License(BaseModel):
    license_id: int
    license_description: str
    category: Categories
    explanation: str
    manually_validated: bool = False


class LicenseClassificationRequest(BaseModel):
    license_id: int
    description: str

class LicenseUpdate(BaseModel):
    category: Categories
    explanation: str

class CategorySummary(BaseModel):
    category: str
    count: int
    validated_count: int 