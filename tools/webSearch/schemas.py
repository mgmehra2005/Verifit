from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Source(BaseModel):
    title: str
    url: str
    source_type: Literal[
        "web",
        "social",
        "competitor"
    ]


class Evidence(BaseModel):
    claim: str
    source: Source
    strength: Literal[
        "high",
        "medium",
        "low"
    ]


class Competitor(BaseModel):
    name: str
    description: str
    strengths: List[str]
    weaknesses: List[str]
    pricing: Optional[str] = None
    target_customer: Optional[str] = None
    source: Optional[Source] = None


class ResearchReport(BaseModel):

    # Core
    idea: str

    # Market
    market_summary: str
    market_signals: List[str]

    # Demand
    demand_signals: List[str]
    pain_points: List[str]

    # Competition
    competitors: List[Competitor]
    competitive_intensity: Literal[
        "low",
        "medium",
        "high"
    ]
    market_gaps: List[str]

    # Analysis
    opportunities: List[str]
    risks: List[str]

    # Evidence
    evidence: List[Evidence]

    # Metadata
    source_count: int
    evidence_count: int
    research_confidence: int = Field(
        ge=0,
        le=100
    )