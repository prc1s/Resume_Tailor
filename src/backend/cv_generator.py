"""
CV generation backend module.
"""
import json
import logging
from typing import Dict, Any, Optional
import openai
from openai import OpenAI

# Use absolute imports for Streamlit compatibility
from config.settings import settings
from utils.prompts import prompt_manager

logger = logging.getLogger(__name__)

class CVGenerator:
    """Handles CV generation using OpenAI API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    def generate_cv(self, job_description: str, user_profile: str, tone: str = "formal") -> Dict[str, Any]:
        """Generate CV using OpenAI API."""
        try:
            # Get system prompt for the specified tone
            system_prompt = prompt_manager.get_cv_prompt(tone)
            
            # Build user prompt
            user_prompt = self._build_user_prompt(job_description, user_profile)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse response
            content = response.choices[0].message.content
            result = self._parse_response(content)
            
            # Log successful generation
            logger.info(f"CV generated successfully for tone: {tone}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating CV: {e}")
            return {"error": str(e)}
    
    def generate_cover_letter(self, job_description: str, user_profile: str, tone: str = "formal") -> str:
        """Generate a cover letter using OpenAI API."""
        try:
            system_prompt = prompt_manager.get_cover_letter_prompt(tone)
            
            user_prompt = f"""
Job Description: {job_description}

User Profile:
{user_profile}

Based on the user's profile and the job description, write a compelling and personalized cover letter.
Ensure the output is a clean, well-formatted string ready for display.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=1000  # Cover letters are shorter
            )
            
            content = response.choices[0].message.content
            logger.info(f"Cover letter generated successfully for tone: {tone}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            return "Error: Could not generate the cover letter."
    
    def _build_user_prompt(self, job_description: str, user_profile: str) -> str:
        """Build the user prompt for CV generation."""
        return f"""
Job Description: {job_description}

User Profile:
{user_profile}

Create a professional CV in English with the following structure and format:

## PROFESSIONAL SUMMARY
[Write a compelling 2-3 sentence summary highlighting key strengths and career objectives relevant to the job]

## WORK EXPERIENCE
[Format each role as:]
**Job Title** | Company Name | Date Range
- [Achievement 1 with quantifiable results - use numbers, percentages, metrics]
- [Achievement 2 with quantifiable results - focus on impact and outcomes]
- [Achievement 3 with quantifiable results - highlight leadership or technical skills]

## EDUCATION
[Format as:]
**Degree Name** | Institution Name | Graduation Year
- GPA: [if applicable and good]
- Relevant coursework: [if applicable to the job]

## TECHNICAL SKILLS
[Organize by category:]
- Programming Languages: [list relevant languages]
- Tools & Technologies: [list frameworks, databases, tools]
- Software & Platforms: [list relevant software]

## SOFT SKILLS
[list relevant soft skills for the role]

## PROJECTS
[If provided, format as:]
**Project Name** | Technologies Used
- [Description and outcomes with quantifiable results]
- [Technical challenges solved]
- [Business impact or user adoption]

## LANGUAGES
[If provided, list with proficiency levels]

## CERTIFICATIONS
[If provided, list with issuing organizations and dates]

## ACHIEVEMENTS & AWARDS
[If provided, list with dates and context]

---

Also provide these additional sections:

## IMPROVEMENT SUGGESTIONS
1. [Specific suggestion 1 - focus on missing skills or certifications]
2. [Specific suggestion 2 - focus on better phrasing or keywords] 
3. [Specific suggestion 3 - focus on format or structure improvements]

## INTERVIEW PREPARATION
**Technical Questions:**
1. [Question 1 - specific to the role and technologies]
2. [Question 2 - problem-solving or technical challenge]
3. [Question 3 - system design or architecture]

**Behavioral Questions:**
1. [Question 1 - leadership or teamwork scenario]
2. [Question 2 - problem-solving or conflict resolution]

**Company Tip:**
[One specific insight about the company culture, values, or role requirements]

Focus on:
- Quantifiable achievements (numbers, percentages, metrics, team sizes, budget amounts)
- Action verbs and strong language (led, developed, implemented, optimized, increased, reduced)
- Relevance to the job description and industry
- Professional formatting with clear sections
- ATS-friendly keywords from the job description
- STAR method for experience descriptions (Situation, Task, Action, Result)
"""
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse the API response and extract sections."""
        try:
            # Split content into sections
            sections = self._extract_sections(content)
            return sections
        except Exception as e:
            logger.warning(f"Failed to parse response properly: {e}")
            return {"raw_response": content}
    
    def _extract_sections(self, content: str) -> Dict[str, Any]:
        """Extract different sections from the CV content."""
        sections = {
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "languages": "",
            "certifications": "",
            "achievements": "",
            "suggestions": [],
            "technical_questions": [],
            "behavioral_questions": [],
            "company_tip": ""
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if line.upper().startswith('## PROFESSIONAL SUMMARY'):
                current_section = 'summary'
                continue
            elif line.upper().startswith('## WORK EXPERIENCE'):
                current_section = 'experience'
                continue
            elif line.upper().startswith('## EDUCATION'):
                current_section = 'education'
                continue
            elif line.upper().startswith('## TECHNICAL SKILLS'):
                current_section = 'skills'
                continue
            elif line.upper().startswith('## SOFT SKILLS'):
                current_section = 'skills'
                continue
            elif line.upper().startswith('## PROJECTS'):
                current_section = 'projects'
                continue
            elif line.upper().startswith('## LANGUAGES'):
                current_section = 'languages'
                continue
            elif line.upper().startswith('## CERTIFICATIONS'):
                current_section = 'certifications'
                continue
            elif line.upper().startswith('## ACHIEVEMENTS'):
                current_section = 'achievements'
                continue
            elif line.upper().startswith('## IMPROVEMENT SUGGESTIONS'):
                current_section = 'suggestions'
                continue
            elif line.upper().startswith('## INTERVIEW PREPARATION'):
                current_section = 'interview_prep'
                continue
            elif line.upper().startswith('**TECHNICAL QUESTIONS:**'):
                current_section = 'technical_questions'
                continue
            elif line.upper().startswith('**BEHAVIORAL QUESTIONS:**'):
                current_section = 'behavioral_questions'
                continue
            elif line.upper().startswith('**COMPANY TIP:**'):
                current_section = 'company_tip'
                continue
            
            # Add content to current section
            if current_section:
                if current_section in ['suggestions', 'technical_questions', 'behavioral_questions']:
                    if line.startswith(('1.', '2.', '3.', '-', '•')):
                        sections[current_section].append(line)
                elif current_section == 'company_tip':
                    sections[current_section] = line
                else:
                    if sections[current_section]:
                        sections[current_section] += '\n' + line
                    else:
                        sections[current_section] = line
        
        return sections
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key."""
        try:
            # Make a simple test call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

# Global CV generator instance
cv_generator = CVGenerator() 