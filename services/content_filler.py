"""Content filling service"""

from models.page_template import PageTemplate


class ContentFiller:
    """Fills templates with data"""

    def fill(self, template: PageTemplate, content: dict[str, str]) -> str:
        """Fills and formats HTML template with content"""
        return template.html.format(**{
            **content,
            "js": template.js,
            "css": template.css,
        })
