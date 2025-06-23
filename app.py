"""
CVTailor - Generate Your Professional CV in 60 Seconds

Entry point for the Streamlit application.
"""
import sys
from pathlib import Path

# Add src directory to Python path to ensure absolute imports work
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Now that the path is set, we can import the main app
from main import main

if __name__ == "__main__":
    main()
