"""
Prompt management utilities for CVTailor.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages prompt templates and versions."""
    
    def __init__(self, prompts_file: str = "data/prompts.json"):
        self.prompts_file = Path(prompts_file)
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from JSON file."""
        try:
            if self.prompts_file.exists():
                with open(self.prompts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                logger.warning(f"Prompts file not found: {self.prompts_file}")
                return self._get_default_prompts()
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
            return self._get_default_prompts()
    
    def _get_default_prompts(self) -> Dict[str, Any]:
        """Return default prompts if file is not found."""
        return {
            "version": "1.1",
            "cv_generation": {
                "en_formal": "You are an expert CV writer specializing in creating professional, ATS-friendly resumes. Focus on quantifiable achievements, relevant keywords, and clear formatting. Use action verbs and the STAR method for experience descriptions. Always generate CVs in English regardless of user input language.",
                "en_friendly": "You are a friendly CV consultant who creates approachable yet professional resumes. Balance professionalism with warmth, use engaging language, and focus on cultural fit and soft skills alongside technical abilities. Always generate CVs in English regardless of user input language."
            },
            "improvement_suggestions": {
                "en": "Provide 3 specific, actionable suggestions to improve the CV. Focus on: 1) Missing certifications or skills that would strengthen the application, 2) Better phrasing or keywords to improve ATS compatibility, 3) Format or structure improvements for better readability and impact."
            },
            "interview_prep": {
                "en": "Generate relevant technical and behavioral questions based on the job description and candidate profile. Include company-specific insights when possible. Questions should be tailored to the role and industry."
            },
            "cover_letter_generation": {
                "en_formal": "You are an expert career consultant writing a professional and persuasive cover letter. The tone should be formal, confident, and tailored to the company's industry and values. The cover letter must be concise, structured, and highlight the candidate's most relevant skills and experiences from their profile that match the job description. Address it to the 'Hiring Manager' unless a specific contact is available. The letter should express genuine interest and a strong call to action.",
                "en_friendly": "You are a helpful career coach drafting a warm and engaging cover letter. The tone should be approachable, enthusiastic, and authentic. The letter should connect the candidate's personal story and passion to the role and company culture. It should be easy to read, highlight key personality traits and skills, and end with a friendly and proactive closing."
            }
        }
    
    def get_cv_prompt(self, tone: str = "formal") -> str:
        """Get CV generation prompt for specified tone."""
        prompt_key = f"en_{tone}"
        return self.prompts.get("cv_generation", {}).get(prompt_key, self.prompts["cv_generation"]["en_formal"])
    
    def get_suggestions_prompt(self, language: str = "en") -> str:
        """Get improvement suggestions prompt."""
        return self.prompts.get("improvement_suggestions", {}).get(language, self.prompts["improvement_suggestions"]["en"])
    
    def get_interview_prompt(self, language: str = "en") -> str:
        """Get interview preparation prompt."""
        return self.prompts.get("interview_prep", {}).get(language, self.prompts["interview_prep"]["en"])
    
    def get_cover_letter_prompt(self, tone: str = "formal") -> str:
        """Get cover letter generation prompt for specified tone."""
        prompt_key = f"en_{tone}"
        default_prompt = self.prompts.get("cover_letter_generation", {}).get("en_formal", "")
        return self.prompts.get("cover_letter_generation", {}).get(prompt_key, default_prompt)
    
    def get_version(self) -> str:
        """Get current prompt version."""
        return self.prompts.get("version", "1.0")
    
    def reload_prompts(self) -> None:
        """Reload prompts from file."""
        self.prompts = self._load_prompts()
        logger.info("Prompts reloaded successfully")

# Global prompt manager instance
prompt_manager = PromptManager() 