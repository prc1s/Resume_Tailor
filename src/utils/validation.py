"""
Validation utilities for CVTailor application.
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from config.settings import settings

@dataclass
class ValidationResult:
    """Result of validation operation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class FormValidator:
    """Handles validation for CV form data."""

    def __init__(self):
        self.min_lengths = {
            "job_description": settings.MIN_JOB_DESCRIPTION_LENGTH,
            "education": settings.MIN_EDUCATION_LENGTH
        }

    def validate_cv_form(self, form_data: dict) -> 'ValidationResult':
        """Validates the main CV form."""
        errors = []
        warnings = []
        
        # Check required fields
        for field in settings.REQUIRED_FIELDS:
            if not form_data.get(field):
                # This should be handled by form labels now, but as a fallback:
                errors.append(f"A required field is missing: {field.replace('_', ' ').title()}")
        
        # Validate email for delivery
        email_for_delivery = form_data.get('email_for_delivery')
        confirm_email = form_data.get('confirm_email')
        if email_for_delivery or confirm_email:
            if email_for_delivery != confirm_email:
                errors.append("The delivery emails do not match. Please re-enter them.")
            if email_for_delivery and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_for_delivery):
                errors.append("The delivery email address is not valid.")

        # Check field lengths
        if form_data.get("job_description") and len(form_data.get("job_description", "")) < self.min_lengths["job_description"]:
            warnings.append("The Job Description is short. For best results, provide more detail.")
        
        if form_data.get("education") and len(form_data.get("education", "")) < self.min_lengths["education"]:
            warnings.append("The Education section is short. For best results, provide more detail.")
            
        if form_data.get("experience") and len(form_data.get("experience", "")) < 20:
             warnings.append("The Work Experience section is very short.")
         
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def sanitize_input(self, text: str) -> str:
        """Sanitizes text input to prevent basic injection attacks."""
        return re.sub(r'[<>{}]', '', text)

    def validate_job_description(self, job_description: str) -> ValidationResult:
        """Validate job description specifically."""
        errors = []
        warnings = []
        
        if not job_description.strip():
            errors.append("Job description is required")
        elif len(job_description.strip()) < self.min_lengths["job_description"]:
            errors.append("Job description is too short")
        elif len(job_description.strip()) > 2000:
            warnings.append("Job description is very long")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

# Global validator instance
form_validator = FormValidator() 