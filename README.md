# CVTailor - Generate Your CV in 60 Seconds

An AI-powered CV generation tool that creates tailored resumes, cover letters, and interview prep in under a minute.

## 🏗️ Professional Architecture

CVTailor is built with a modular, scalable architecture following industry best practices:

```
CVTailor/
├── src/                          # Source code
│   ├── config/                   # Configuration management
│   │   └── settings.py          # App settings and environment variables
│   ├── frontend/                 # UI components
│   │   └── components.py        # Streamlit UI components
│   ├── backend/                  # Business logic
│   │   └── cv_generator.py      # OpenAI API integration
│   ├── utils/                    # Utilities and helpers
│   │   ├── prompts.py           # Prompt management
│   │   └── validation.py        # Form validation
│   └── main.py                  # Application entry point
├── data/                         # Data files
│   └── prompts.json             # AI prompt templates
├── tests/                        # Test files (future)
├── app.py                       # Streamlit entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Payment Integration (for future use)
TAP_PAYMENTS_SECRET_KEY=your_tap_payments_secret_key_here
TAP_PAYMENTS_PUBLIC_KEY=your_tap_payments_public_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 📋 Features

- **Multi-language Support**: English and Arabic interface
- **English CV Output**: All CVs generated in English regardless of interface language
- **Tone Customization**: Formal, Friendly, and Khaleej (Gulf region)
- **Comprehensive Form**: 15+ fields for complete CV information
- **Flexible Input**: Natural language descriptions for experience and projects
- **Required Fields**: Job Description and Education validation
- **Free Trial**: One free CV generation per session
- **User Feedback**: Rating system for continuous improvement

## 🏗️ Architecture Overview

### **Frontend Layer** (`src/frontend/`)
- **Streamlit Components**: Modular UI components
- **Form Handling**: Comprehensive CV form with validation
- **Bilingual Support**: English/Arabic interface
- **Results Display**: Tabbed results with CV preview, suggestions, and interview prep

### **Backend Layer** (`src/backend/`)
- **CV Generator**: OpenAI API integration
- **Prompt Management**: Versioned prompt templates
- **Error Handling**: Robust error management
- **API Validation**: OpenAI API key validation

### **Configuration Layer** (`src/config/`)
- **Settings Management**: Centralized configuration
- **Environment Variables**: Secure API key management
- **Constants**: Application constants and defaults

### **Utilities Layer** (`src/utils/`)
- **Form Validation**: Input validation and sanitization
- **Prompt Management**: Dynamic prompt loading and versioning
- **Data Processing**: User input processing and formatting

## 🔧 Configuration

### **Settings** (`src/config/settings.py`)
- OpenAI API configuration
- Application constants
- Pricing configuration
- Supported languages and tones
- Validation rules

### **Prompts** (`data/prompts.json`)
- Versioned prompt templates
- Language-specific prompts
- Tone-specific CV generation
- Interview preparation prompts

### **Environment Variables**
- `OPENAI_API_KEY`: Required for LLM functionality
- `TAP_PAYMENTS_*`: For payment integration (future)
- `DATABASE_URL`: For logging and analytics (future)

## 🚧 Development Workflow

### **Adding New Features**
1. **Frontend**: Add components to `src/frontend/components.py`
2. **Backend**: Add business logic to `src/backend/`
3. **Configuration**: Update `src/config/settings.py`
4. **Validation**: Add validation rules to `src/utils/validation.py`

### **Modifying Prompts**
1. Edit `data/prompts.json`
2. Update version number
3. Test with different job types
4. Monitor output quality

### **Adding New Languages**
1. Update `settings.SUPPORTED_LANGUAGES`
2. Add translations to UI components
3. Update validation messages
4. Test bilingual functionality

## 📊 Monitoring & Analytics

### **Current Metrics**
- CV generation success rate
- User feedback ratings
- API usage and costs
- Most popular job types
- Form completion rates

### **Future Metrics**
- Conversion rates (free to paid)
- User retention
- A/B test results
- Regional usage patterns
- Prompt performance

## 🔒 Privacy & Security

- **No Data Storage**: No user data stored long-term
- **In-Memory Processing**: All processing done in memory
- **Input Sanitization**: User input validation and sanitization
- **API Security**: Secure OpenAI API key management
- **Optional Feedback**: Anonymous feedback collection

## 🧪 Testing

### **Manual Testing**
1. Test form validation with various inputs
2. Test CV generation with different job types
3. Test bilingual interface functionality
4. Test error handling scenarios

### **Future Automated Testing**
- Unit tests for each module
- Integration tests for API calls
- UI tests for form validation
- Performance tests for CV generation

## 🚀 Deployment

### **Local Development**
```bash
streamlit run app.py
```

### **Production Deployment**
1. **Hugging Face Spaces**: Push to repository for auto-deployment
2. **Docker**: Containerize for cloud deployment
3. **Environment Variables**: Set production API keys
4. **Monitoring**: Add logging and analytics

## 💡 Development Tips

### **Code Organization**
- Keep modules focused and single-purpose
- Use clear naming conventions
- Add comprehensive docstrings
- Follow PEP 8 style guidelines

### **Error Handling**
- Always handle API failures gracefully
- Provide meaningful error messages
- Log errors for debugging
- Implement fallback mechanisms

### **Performance**
- Cache prompt templates
- Optimize API calls
- Minimize redundant processing
- Monitor memory usage

## 🤝 Contributing

This is a solo project, but feedback and suggestions are welcome!

### **Code Standards**
- Follow the existing modular structure
- Add type hints to all functions
- Include docstrings for all classes and methods
- Test changes thoroughly

## 📄 License

Private project - All rights reserved

---

**Built with ❤️ for job seekers in the MENA region**

*Professional, scalable, and ready for production deployment.* 