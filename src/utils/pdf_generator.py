"""
PDF generation utilities for CVTailor using HTML/CSS templates.
"""
import logging
import markdown2
from typing import Dict, Any
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Handles PDF generation for CVs using HTML/CSS templates."""

    def __init__(self):
        self.template_dir = Path(__file__).parent / 'templates'
        self.env = Environment(loader=FileSystemLoader(self.template_dir), autoescape=True)
        self.env.filters['markdown'] = lambda text: markdown2.markdown(text, extras=["break-on-newline"])

    def generate_cv_pdf(self, cv_data: Dict[str, Any], user_info: Dict[str, Any]) -> BytesIO:
        """Generate a professional CV PDF from an HTML template."""
        try:
            template = self.env.get_template('cv_template.html')
            
            # Combine all skills into one field for the template if they exist
            all_skills = ""
            if cv_data.get('technical_skills'):
                all_skills += cv_data['technical_skills'] + "\n\n"
            if cv_data.get('soft_skills'):
                all_skills += cv_data['soft_skills']
            
            # Add combined skills to cv_data if it's not empty
            if all_skills:
                cv_data['skills'] = all_skills.strip()
            
            # Combine data for template
            template_data = {
                'cv_data': cv_data,
                'user_info': user_info
            }
            
            rendered_html = template.render(template_data)
            
            css_path = self.template_dir / 'style.css'
            
            html = HTML(string=rendered_html, base_url=str(self.template_dir))
            
            pdf_buffer = html.write_pdf(stylesheets=[CSS(css_path)])
            
            logger.info("PDF generated successfully from HTML template.")
            return BytesIO(pdf_buffer)

        except Exception as e:
            logger.error(f"Error generating PDF from HTML: {e}")
            raise

# Global PDF generator instance
pdf_generator = PDFGenerator() 