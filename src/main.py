"""
Main application entry point for CVTailor.
"""
import streamlit as st
import logging
from typing import Dict, Any

# Use absolute imports for Streamlit compatibility
from config.settings import settings
from frontend.components import ui_components
from backend.cv_generator import cv_generator
from utils.validation import form_validator
from utils.formatting import formatter
from utils.email_sender import email_sender
from utils.database import db_manager
from utils.pdf_generator import pdf_generator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title=f"{settings.APP_NAME} - {settings.APP_DESCRIPTION}",
        page_icon="📄",
        layout="wide"
    )

def build_user_profile(form_data: Dict[str, Any]) -> str:
    """Build user profile string from form data."""
    return f"""
Name: {form_data.get('name', '')}
Email: {form_data.get('email', '')}
Phone: {form_data.get('phone', '')}
Location: {form_data.get('location', '')}
LinkedIn: {form_data.get('linkedin', '')}
Website: {form_data.get('website', '')}

Education: {form_data.get('education', '')}

Work Experience: {form_data.get('experience', '')}

Technical Skills: {form_data.get('technical_skills', '')}
Soft Skills: {form_data.get('soft_skills', '')}

Projects: {form_data.get('projects', '')}

Certifications: {form_data.get('certifications', '')}
Languages: {form_data.get('languages', '')}
Achievements: {form_data.get('achievements', '')}
Interests: {form_data.get('interests', '')}
"""

def validate_form_data(form_data: Dict[str, Any]) -> bool:
    """Validate form data and show errors if any."""
    # Sanitize inputs
    sanitized_data = {}
    for key, value in form_data.items():
        if isinstance(value, str):
            sanitized_data[key] = form_validator.sanitize_input(value)
        else:
            sanitized_data[key] = value
    
    # Validate form
    validation_result = form_validator.validate_cv_form(sanitized_data)
    
    if not validation_result.is_valid:
        for error in validation_result.errors:
            st.error(f"❌ {error}")
        return False
    
    if validation_result.warnings:
        for warning in validation_result.warnings:
            st.warning(f"⚠️ {warning}")
    
    return True

def main():
    """Main function to run the CVTailor application."""
    # Initialize session state
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

    # Render sidebar and get settings
    ui_language, tone = ui_components.render_sidebar()
    
    # Set page direction based on language
    if ui_language == "ar":
        st.markdown(
            """
            <style>
            body, .stApp {
                direction: rtl;
            }
            .stSidebar, .stSidebar * {
                direction: ltr; /* Keep sidebar LTR for better layout */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Render header
    ui_components.render_header(ui_language)
    
    # Render CV form
    form_data = ui_components.render_cv_form(ui_language)
    
    # Handle form submission
    if form_data["submitted"]:
        # Sanitize and format form data
        form_data['location'] = formatter.format_location(form_data.get('location', ''))

        # Validate form data
        if not validate_form_data(form_data):
            return
        
        # Save anonymized data to the database
        try:
            form_data_with_tone = {**form_data, 'tone': tone}
            db_manager.save_cv_data(form_data_with_tone)
        except Exception as e:
            logger.error(f"Failed to save data to database: {e}")

        # Store user info in session state for PDF generation
        st.session_state.user_name = form_data.get("name", "")
        st.session_state.user_email = form_data.get("email", "")
        st.session_state.user_phone = form_data.get("phone", "")
        st.session_state.user_location = form_data.get("location", "")
        st.session_state.user_linkedin = form_data.get("linkedin", "")
        st.session_state.user_website = form_data.get("website", "")
        
        # Show loading spinner
        with st.spinner("Generating your CV..."):
            # Build user profile
            user_profile = build_user_profile(form_data)
            
            # Generate CV content
            cv_result = cv_generator.generate_cv(
                job_description=form_data["job_description"],
                user_profile=user_profile,
                tone=tone,
            )
            
            # Generate Cover Letter content
            with st.spinner("Generating cover letter..."):
                cover_letter_result = cv_generator.generate_cover_letter(
                    job_description=form_data["job_description"],
                    user_profile=user_profile,
                    tone=tone,
                )

            final_result = {**cv_result, "cover_letter": cover_letter_result}

            # Generate PDF in memory
            with st.spinner("Creating PDF document..."):
                pdf_buffer = pdf_generator.generate_cv_pdf(final_result, form_data)
                final_result['pdf_buffer'] = pdf_buffer.getvalue()

            # Send email if address is provided
            if form_data.get("email_for_delivery"):
                with st.spinner("Sending email..."):
                    try:
                        email_body = """
                        <html><body>
                        <p>Hi,</p>
                        <p>Thank you for using CVTailor! Your personalized documents are attached.</p>
                        <p>We wish you the best of luck in your job search.</p>
                        <p>Sincerely,<br>The CVTailor Team</p>
                        </body></html>
                        """
                        attachments = [
                            (final_result['pdf_buffer'], "Your_CV.pdf", "application/pdf"),
                            (final_result['cover_letter'].encode('utf-8'), "Cover_Letter.txt", "text/plain")
                        ]
                        email_sender.send_email_with_attachments(
                            recipient_email=form_data["email_for_delivery"],
                            subject="Your Generated CV and Cover Letter from CVTailor",
                            body=email_body,
                            attachments=attachments
                        )
                        st.success(f"Your documents have been sent to {form_data['email_for_delivery']}!")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")

            # Render results to the screen
            ui_components.render_results(final_result, ui_language)

if __name__ == "__main__":
    main() 