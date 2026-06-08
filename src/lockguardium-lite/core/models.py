from __future__ import annotations
import math
import string
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, AfterValidator, ConfigDict
from pydantic.types import StringConstraints

def calculate_entropy(password: str) -> float:
    """
    Calculates the mathematical entropy of the password in the model. 
    Formula: E = L * log2(R)
    Args: L = Length und R = Size of the character set used.
    """
    if not password:
        return 0.0
        
    pool_size = 0
    if any(char in string.ascii_lowercase for char in password):
        pool_size += 26
    if any(char in string.ascii_uppercase for char in password):
        pool_size += 26
    if any(char in string.digits for char in password):
        pool_size += 10
    if any(char in string.punctuation or char in " !@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
        pool_size += 32

    if pool_size == 0:
        return 0.0
        
    # Entropy = Length * log2(char set)
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


# Common string restrictions (trimming of whitespace, minimum 1 character)
TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class PasswordEntry(BaseModel):
    """
    Ensures data quality at the domain level before encryption takes effect.
    """
    website: TrimmedStr = Field(..., description="Website or service")
    email: EmailStr = Field(..., description="Email address")
    username: Optional[str] = Field(default="", description="Username (optional)")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    
    # In-memory metadata for the GUI (not stored in the password table)
    entropy: float = Field(default=0.0, description="Cryptographic strength of the password in bits")

    @classmethod
    def create_validated_entry(cls, website: str, email: str, password: str, username: str = "") -> PasswordEntry:
        """
        Factory method: Creates an instance and automatically 
        calculates the entropy for later display in the GUI.
        """
        entropy_val = calculate_entropy(password)
        return cls(
            website=website,
            email=email,
            username=username,
            password=password,
            entropy=entropy_val
        )

    # Pydantic configuration: Prevents unwanted additional fields from being injected.
    model_config = ConfigDict(extra="forbid", frozen=False)