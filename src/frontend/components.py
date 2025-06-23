"""
Frontend components for CVTailor application.
"""
import streamlit as st
from typing import Dict, Any, Optional

# Use absolute imports for Streamlit compatibility
from utils.validation import form_validator
from utils.pdf_generator import pdf_generator
from config.settings import settings
from utils.localization import get_local_text

class UIComponents:
    """Encapsulates all UI rendering logic."""

    def render_header(self, ui_language: str):
        """Renders the main page header."""
        st.title(get_local_text(ui_language, "main_title"))
        st.write(get_local_text(ui_language, "subtitle"))
        st.divider()
    
    def render_sidebar(self) -> tuple[str, str]:
        """Renders the sidebar with all its options and returns language and tone."""
        with st.sidebar:
            st.header(get_local_text("en", "website_language")) # Keep this LTR
            ui_language = st.selectbox(
                label="", 
                options=settings.SUPPORTED_LANGUAGES, 
                format_func=lambda x: "العربية" if x == "ar" else "English",
                label_visibility="collapsed"
            )

            st.header(get_local_text(ui_language, "admin_access"))
            admin_key = st.text_input(
                get_local_text(ui_language, "admin_key_placeholder"), 
                type="password", 
                key="admin_key"
            )
            if admin_key:
                if admin_key == settings.ADMIN_SECRET_KEY:
                    st.session_state.is_admin = True
                    st.success(get_local_text(ui_language, "admin_success"))
                else:
                    st.error(get_local_text(ui_language, "admin_fail"))

            if st.session_state.get('is_admin', False):
                st.info(get_local_text(ui_language, "admin_status"))

            st.header(get_local_text(ui_language, "settings_header"))
            tone = st.radio(
                get_local_text(ui_language, "tone_label"), 
                settings.SUPPORTED_TONES, 
                index=0,
                format_func=lambda x: x.title()
            )

            st.header(get_local_text(ui_language, "pricing_header"))
            st.info(get_local_text(ui_language, "pricing_info").format(
                limit=settings.FREE_TRIAL_LIMIT,
                price=settings.PRICE_PER_CV
            ))

            st.markdown("---")
            st.info(get_local_text(ui_language, "version_info").format(version=settings.VERSION))
            
        return ui_language, tone

    def render_cv_form(self, ui_language: str) -> dict:
        """Renders the main CV generation form."""
        with st.form("cv_form"):
            st.header(get_local_text(ui_language, "form_header"))
            st.caption(get_local_text(ui_language, "required_fields"))

            job_description = st.text_area(
                label=get_local_text(ui_language, "job_description_label"),
                placeholder=get_local_text(ui_language, "job_description_placeholder"),
                height=150
            )
            education = st.text_area(
                label=get_local_text(ui_language, "education_label"),
                placeholder=get_local_text(ui_language, "education_placeholder"),
                height=100
            )
            
            st.subheader(get_local_text(ui_language, "personal_info"))
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(get_local_text(ui_language, "full_name_label"), placeholder=get_local_text(ui_language, "full_name_placeholder"))
                phone = st.text_input(get_local_text(ui_language, "phone_label"), placeholder=get_local_text(ui_language, "phone_placeholder"))
                linkedin = st.text_input(get_local_text(ui_language, "linkedin_label"), placeholder=get_local_text(ui_language, "linkedin_placeholder"))
            with col2:
                email = st.text_input(get_local_text(ui_language, "email_label"), placeholder=get_local_text(ui_language, "email_placeholder"))
                location = st.text_input(get_local_text(ui_language, "location_label"), placeholder=get_local_text(ui_language, "location_placeholder"))
                website = st.text_input(get_local_text(ui_language, "website_label"), placeholder=get_local_text(ui_language, "website_placeholder"))

            st.subheader(get_local_text(ui_language, "experience_label"))
            experience = st.text_area(
                label=get_local_text(ui_language, "experience_label"),
                placeholder=get_local_text(ui_language, "experience_placeholder"),
                height=200,
                help=get_local_text(ui_language, "experience_help"),
                label_visibility="collapsed"
            )

            st.subheader(get_local_text(ui_language, "skills_header"))
            col1, col2 = st.columns(2)
            with col1:
                technical_skills = st.text_area(get_local_text(ui_language, "technical_skills_label"), placeholder=get_local_text(ui_language, "technical_skills_placeholder"))
            with col2:
                soft_skills = st.text_area(get_local_text(ui_language, "soft_skills_label"), placeholder=get_local_text(ui_language, "soft_skills_placeholder"))
            
            st.subheader(get_local_text(ui_language, "projects_label"))
            projects = st.text_area(
                label=get_local_text(ui_language, "projects_label"),
                placeholder=get_local_text(ui_language, "projects_placeholder"),
                height=150,
                help=get_local_text(ui_language, "projects_help"),
                label_visibility="collapsed"
            )
            
            with st.expander(get_local_text(ui_language, "additional_info")):
                col1, col2 = st.columns(2)
                with col1:
                    certifications = st.text_area(get_local_text(ui_language, "certifications_label"), placeholder=get_local_text(ui_language, "certifications_placeholder"))
                    achievements = st.text_area(get_local_text(ui_language, "achievements_label"), placeholder=get_local_text(ui_language, "achievements_placeholder"))
                with col2:
                    languages = st.text_area(get_local_text(ui_language, "languages_label"), placeholder=get_local_text(ui_language, "languages_placeholder"))
                    interests = st.text_area(get_local_text(ui_language, "interests_label"), placeholder=get_local_text(ui_language, "interests_placeholder"))

            with st.expander(get_local_text(ui_language, "delivery_options")):
                email_for_delivery = st.text_input(get_local_text(ui_language, "delivery_email_label"))
                confirm_email = st.text_input(get_local_text(ui_language, "delivery_email_confirm"))

            submitted = st.form_submit_button(
                label=get_local_text(ui_language, "generate_button"),
                use_container_width=True,
                type="primary"
            )

        form_data = {
            "submitted": submitted,
            "job_description": job_description,
            "education": education,
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "website": website,
            "experience": experience,
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "projects": projects,
            "certifications": certifications,
            "languages": languages,
            "achievements": achievements,
            "interests": interests,
            "email_for_delivery": email_for_delivery,
            "confirm_email": confirm_email,
        }
        return form_data
    
    @staticmethod
    def render_results(result: Dict[str, Any], ui_language: str):
        """Render the CV generation results."""
        if "error" in result:
            st.error(f"Error generating CV: {result['error']}")
            return
        
        # Display success message
        st.success(get_local_text(ui_language, "generation_success"))
        
        # Create tabs for different sections
        tab_titles = [
            get_local_text(ui_language, "preview_tab"),
            get_local_text(ui_language, "cover_letter_tab"),
            get_local_text(ui_language, "download_tab"),
        ]
        
        cv_preview, cover_letter_tab, download_tab = st.tabs(tab_titles)
        
        # CV Preview Tab
        with cv_preview:
            UIComponents._render_cv_preview(result, ui_language)
        
        # Cover Letter Tab
        with cover_letter_tab:
            st.header(get_local_text(ui_language, "cover_letter_header"))
            cover_letter = result.get('cover_letter', 'Could not generate a cover letter.')
            st.text_area(
                label=get_local_text(ui_language, "cover_letter_header"), 
                value=cover_letter, 
                height=500,
                label_visibility="collapsed"
            )
        
        # Download Tab
        with download_tab:
            UIComponents._render_download_section(result, ui_language)
        
        # Feedback section
        UIComponents._render_feedback_section(ui_language)
    
    @staticmethod
    def _render_cv_preview(result: Dict[str, Any], ui_language: str):
        """Render CV preview content."""
        if result.get("raw_response"):
            st.subheader("Generated CV")
            st.text(result["raw_response"])
            return
        
        # Professional Summary
        if result.get("summary"):
            st.subheader("📋 Professional Summary")
            st.write(result["summary"])
            st.divider()
        
        # Work Experience
        if result.get("experience"):
            st.subheader("💼 Work Experience")
            st.markdown(result["experience"])
            st.divider()
        
        # Education
        if result.get("education"):
            st.subheader("🎓 Education")
            st.markdown(result["education"])
            st.divider()
        
        # Skills
        if result.get("skills"):
            st.subheader("🛠️ Skills")
            st.markdown(result["skills"])
            st.divider()
        
        # Projects
        if result.get("projects"):
            st.subheader("🚀 Projects")
            st.markdown(result["projects"])
            st.divider()
        
        # Languages
        if result.get("languages"):
            st.subheader("🌍 Languages")
            st.markdown(result["languages"])
            st.divider()
        
        # Certifications
        if result.get("certifications"):
            st.subheader("🏆 Certifications")
            st.markdown(result["certifications"])
            st.divider()
        
        # Achievements
        if result.get("achievements"):
            st.subheader("🏅 Achievements & Awards")
            st.markdown(result["achievements"])
            st.divider()
        
        # If no structured content, show raw response
        if not any([result.get("summary"), result.get("experience"), result.get("education")]):
            st.subheader("Generated CV")
            st.text(result.get("raw_response", "CV content not available"))
    
    @staticmethod
    def _render_download_section(result: Dict[str, Any], ui_language: str):
        """Render download section with PDF generation."""
        st.header(get_local_text(ui_language, "download_header"))
        
        # Admin bypass for download limits
        if st.session_state.get('is_admin', False):
            st.info(get_local_text(ui_language, "download_info_admin"))
        else:
            st.write(get_local_text(ui_language, "download_info_user"))

        user_info = {
            "name": st.session_state.get("user_name", "Your Name"),
            "email": st.session_state.get("user_email", ""),
            "phone": st.session_state.get("user_phone", ""),
            "location": st.session_state.get("user_location", ""),
            "linkedin": st.session_state.get("user_linkedin", ""),
            "website": st.session_state.get("user_website", "")
        }
        
        # Trial logic for non-admins
        if not st.session_state.get('is_admin', False):
            if st.session_state.get("free_trial_used", False) and 'download_clicked' in st.session_state:
                st.warning(get_local_text(ui_language, "download_warning"))
                if st.button("💳 Purchase for SAR 29"):
                    st.info("Payment integration coming soon...")
                return

        try:
            file_name = f"{user_info['name'].replace(' ', '_')}_CV.pdf"

            st.download_button(
                label=get_local_text(ui_language, "download_button_label"),
                data=result['pdf_buffer'],
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True,
                on_click=lambda: st.session_state.update(free_trial_used=True, download_clicked=True)
            )
            if not st.session_state.get('is_admin', False):
                st.caption(get_local_text(ui_language, "download_caption"))

        except Exception as e:
            st.error(f"Sorry, we couldn't generate the PDF. Please try again.")
            logger.error(f"PDF Generation Failed: {e}")
        
        st.button("📝 Download DOCX (Coming Soon)", disabled=True)
    
    @staticmethod
    def _render_feedback_section(ui_language: str):
        """Render feedback section."""
        st.divider()
        st.subheader(get_local_text(ui_language, "feedback_header"))
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(get_local_text(ui_language, "feedback_yes")):
                st.success(get_local_text(ui_language, "feedback_thanks"))
        
        with col2:
            if st.button(get_local_text(ui_language, "feedback_no")):
                st.info(get_local_text(ui_language, "feedback_improve"))
        
        with col3:
            if st.button("⭐ Rate"):
                rating = st.slider("Rate your experience", 1, 5, 3)
                if st.button("Submit Rating"):
                    st.success(f"Thank you for your {rating}-star rating!")

# Global UI components instance
ui_components = UIComponents() 