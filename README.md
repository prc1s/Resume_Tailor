# ResumeTailor

**Automatically tailor your resume to any job description** using the power of LLMs and a lightweight MLOps pipeline.

---

## 📋 Overview  
ResumeTailor helps you maximize your chances of landing an interview by:

- **Parsing** your uploaded resume (PDF or text)  
- **Analyzing** a target job description  
- **Rewriting** your bullet points to include the right keywords, tone, and structure  
- **Delivering** a ready-to-download tailored resume in seconds  

---

## 🚀 Key Features  
- **Zero setup:** Web UI (Streamlit) for instant uploads  
- **LLM integration:** GPT-4 (or swap in your choice of model)  
- **Extensible pipeline:** Easily replace or add modules (e.g. semantic scoring, localization)  
- **Downloadable output:** One-click export of your new resume  
- **Containerized:** Dockerfile included for “works everywhere” deployment  

---

## 🔧 Tech Stack  
- **Frontend:** Streamlit  
- **Text extraction:** PyMuPDF (`fitz`) & Python  
- **LLM API:** OpenAI GPT-4 (via `openai` SDK)  
- **Deployment:** Docker (+ AWS EC2 / Hugging Face Spaces / Render)  

---

## ⚡ Quick Start  
1. Clone this repo & enter folder  
2. Create a `.env` with your `OPENAI_API_KEY`  
3. Install deps:  
   ```bash
   pip install -r requirements.txt
