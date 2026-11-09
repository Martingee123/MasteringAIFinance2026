"""Structured outputs keep evidence separate from model judgments."""
from typing import Literal
from pydantic import BaseModel

class Evidence(BaseModel):
    file: str
    line_start: int
    line_end: int
    quote: str
    tag: str
    period: str
    value: float
    scale: float  # quoted value * scale = base USD, or 1 for EPS/percent

class Claim(BaseModel):
    label: str
    report_quote: str
    reported_value: float
    decimals: int
    kind: Literal['fact', 'line', 'ratio', 'unsupported']
    definition: str
    evidence: list[Evidence]
    expression: str  # ratio arithmetic on evidence values, + - * / only
    semantic_mark: Literal['correct', 'wrong', 'unsupported']
    semantic_reason: str
    corrected_text: str

class Audit(BaseModel):
    claims: list[Claim]
    excluded_thesis: str
    coverage_notes: str

class Review(BaseModel):
    report: str
    research_issues: list[str]
    financial_issues: list[str]
    advisor_issues: list[str]

class Calculation(BaseModel):
    id: str
    definition: str
    expression: str
    decimals: int
    evidence: list[Evidence]

class FinancialOutput(BaseModel):
    markdown: str
    calculations: list[Calculation]
