from typing import Optional
from pydantic import BaseModel, Field


class LessonDraft(BaseModel):
    """Generated lesson content structure."""
    topic: str = Field(description="Lesson topic (e.g., Introduction to RAG)")
    title: str = Field(description="Catchy, simple title for beginners")
    what_is_it: str = Field(description="Simple explanation of what the technology is using an everyday analogy.")
    why_it_matters: str = Field(description="Real-world problem it solves in plain terms.")
    how_it_works: str = Field(description="Step-by-step breakdown using relatable terms.")
    summary: str = Field(description="1-2 sentence recap or takeaway.")