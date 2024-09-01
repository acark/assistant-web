from pydantic import BaseModel
from typing import List, Optional


## These are JSON format like objects in python. 
class TranscriberConfig(BaseModel):
    provider: str
    model: str
    language: str
    smartFormat: bool
    keywords: Optional[List[str]]
    endpointing: int

class ModelConfig(BaseModel):
    provider: str
    model: str
    temperature: float
    maxTokens: int
    emotionRecognitionEnabled: bool
    numFastTurns: int
