from __future__ import annotations
import math
import string
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator
from pydantic.types import StringConstraints

def calculate_entropy(password: str) -> float:
    """
    Calculate the information-theoretic entropy of a password in bits.
    
    Formula: E = L * log2(R)
    Where L is the length of the password and R is the size of the pool 
    of unique characters used.
    
    Parameters:
        password (str): The plaintext password to evaluate.
        
    Returns:
        float: The calculated entropy rounded to two decimal places.
    """
    if not password:
        return 0.0
        
    pool_size = 0
    # Define characteristic character pools with their respective sizes
    character_pools = [
        (string.ascii_lowercase, 26),
        (string.ascii_uppercase, 26),
        (string.digits, 10),
        (string.punctuation + " ", 32),  # Combined standard punctuation and space
    ]
    
    # Deduplicate password characters into a set for O(1) lookups in the loop
    password_chars = set(password)
    for char_set, size in character_pools:
        if any(char in password_chars for char in char_set):
            pool_size += size

    if pool_size == 0:
        return 0.0
        
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


# Reusable domain constraint for trimmed, non-empty strings
TrimmedStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class PasswordEntry(BaseModel):
    """
    Pydantic V2 data model representing a single secure vault entry.
    
    Enforces domain-level data integrity and automatically computes cryptographic 
    metrics before data is passed down to the encryption layer.
    """
    website: TrimmedStr = Field(..., description="The target website or service URL")
    email: EmailStr = Field(..., description="The registered email address")
    username: Optional[str] = Field(default="", description="Optional account username")
    password: str = Field(..., min_length=8, description="The plaintext password (minimum 8 characters)")
    entropy: float = Field(default=0.0, description="Cryptographic strength of the password in bits")

    # Strict configuration to prevent unexpected payload injections
    model_config = ConfigDict(extra="forbid", frozen=False)

    @model_validator(mode="before")
    @classmethod
    def auto_calculate_entropy(cls, data: dict) -> dict:
        """
        Pre-validator hook to automatically inject the computed password entropy.
        
        Ensures that 'entropy' is consistently calculated regardless of how 
        the instance is initialized, eliminating the need for a manual factory.
        """
        if isinstance(data, dict) and "password" in data:
            data["entropy"] = calculate_entropy(data["password"])
        return data