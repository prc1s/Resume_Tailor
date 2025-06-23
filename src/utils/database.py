"""
Database management utility for CVTailor.
Handles saving anonymized CV data to an SQLite database.
"""
import sqlite3
import logging
from typing import Dict, Any
from config.settings import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages the SQLite database for storing anonymized CV data."""

    def __init__(self, db_file: str = settings.DATABASE_FILE):
        self.db_file = db_file
        self._create_table()

    def _create_table(self):
        """Creates the cv_data table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cv_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_description TEXT,
                        education TEXT,
                        experience TEXT,
                        technical_skills TEXT,
                        soft_skills TEXT,
                        projects TEXT,
                        certifications TEXT,
                        languages TEXT,
                        achievements TEXT,
                        interests TEXT,
                        tone TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database table creation error: {e}")

    def save_cv_data(self, form_data: Dict[str, Any]):
        """
        Saves anonymized CV information to the database.
        PII (Personally Identifiable Information) is excluded.
        """
        anonymized_data = {
            key: form_data[key] for key in form_data 
            if key not in ['name', 'email', 'phone', 'linkedin', 'website', 
                           'submitted', 'email_for_delivery', 'confirm_email']
        }
        
        # Ensure all expected columns are present
        columns = [
            'job_description', 'education', 'experience', 'technical_skills', 
            'soft_skills', 'projects', 'certifications', 'languages', 
            'achievements', 'interests', 'tone'
        ]
        for col in columns:
            if col not in anonymized_data:
                anonymized_data[col] = None

        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO cv_data (
                        job_description, education, experience, technical_skills, 
                        soft_skills, projects, certifications, languages, 
                        achievements, interests, tone
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(anonymized_data[col] for col in columns))
                conn.commit()
            logger.info("Anonymized CV data saved to database.")
        except sqlite3.Error as e:
            logger.error(f"Error saving CV data to database: {e}")

# Global database manager instance
db_manager = DatabaseManager() 