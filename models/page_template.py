""""""

from dataclasses import dataclass


@dataclass
class PageTemplate:
    """HTML template page"""
    html: str
    js: str
    css: str
    elements: list[str]
