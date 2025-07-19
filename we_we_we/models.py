from pydantic import BaseModel, Field, ConfigDict
from typing import List

class VibeScanInput(BaseModel):
    """Input schema for vibe_scan tool."""

    model_config = ConfigDict(extra='forbid')

    text: str = Field(..., description="Text to analyse for vibes", min_length=1)


class SecurityInput(BaseModel):
    """Input schema for security_lock tool."""

    model_config = ConfigDict(extra='forbid')

    text: str = Field(..., description="Input to scan for hostile patterns", min_length=1)


class MeshDigest(BaseModel):
    """Schema for mesh heartbeat payloads."""

    model_config = ConfigDict(extra='forbid')

    hash: str = Field(..., min_length=6)
    tags: List[str] = Field(default_factory=list)
    ts: int = Field(..., description="Unix timestamp (secs)")