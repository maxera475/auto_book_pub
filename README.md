📚 Automated Book Publication System with AI & Versioning
This project automates the workflow of scraping online book chapters, rewriting them using AI, allowing human edits, and storing versions for semantic search and reuse.

🚀 Features
✅ Chapter Scraping from URLs (e.g. WikiSource)

🤖 AI Rewriting using Ollama-based models (Writer)

🧠 AI Reviewing using Ollama-based models (Reviewer)

✍️ Human-in-the-loop editing via Streamlit

🧾 Version Storage with ChromaDB + Sentence Transformers

🔍 Semantic Search of saved versions

🧱 Modular architecture (FastAPI + Streamlit + ChromaDB)

🏗️ Tech Stack
Layer	Tool
UI	Streamlit
API Backend	FastAPI
Scraping	Playwright
AI Writing/Review	Ollama or LLMs
Version DB	ChromaDB + SentenceTransformers
Search	Semantic Vector Search

📁 Project Structure
bash
Copy
Edit
auto_book_pub/
├── main.py                     # FastAPI backend
├── scrapper.py                 # Playwright scraper
├── writer_ollama.py           # AI writer module
├── reviewer_ollama.py         # AI reviewer module
├── vector_store.py            # ChromaDB versioning
├── app.py                     # Main UI
├── output/                    # Stores screenshots & chapters
├── requirements.txt
└── README.md
✅ How It Works
User inputs chapter URLs in Streamlit

Streamlit calls FastAPI to:

Scrape the webpage

Rewrite and review content using AI

Save original, AI-written, and reviewed versions

User edits content → Clicks ✅ Finalize

Final version is stored in ChromaDB

User can search all saved versions semantically

💻 Installation
bash
Copy
Edit
git clone https://github.com/your-repo/auto_book_pub.git
cd auto_book_pub

# Create and activate environment
conda create -n autobook python=3.10
conda activate autobook

# Install dependencies
pip install -r requirements.txt

# Install Playwright dependencies
playwright install
⚙️ Run the System
1. Start FastAPI Backend
bash
Copy
Edit
uvicorn main:app --reload
2. Start Streamlit App
bash
Copy
Edit
streamlit run streamlit_app.py
Open: http://localhost:8501

🔍 Example Semantic Queries
Try searching:

"sunrise over the sea"

"prayer before battle"

"moment of silence"

"storm and shipwreck"

These will match content across all saved chapter versions.

🧠 Tips & Notes
Ensure AI writer/reviewer modules (like Ollama) are available and models are downloaded

Use the same chapter_name_prefix to organize chapters per book

Versions are stored with metadata: timestamp, comment, status

ChromaDB is in-memory by default — enable persistence in vector_store.py

🗃️ Enable Persistent Storage
Modify in vector_store.py:

python
Copy
Edit
from chromadb.config import Settings
chroma_client = chromadb.Client(Settings(persist_directory='./chroma_store'))
Then add:

python
Copy
Edit
chroma_client.persist()
🛠️ Future Enhancements
 Multi-user version history

 Feedback scoring for retrieval ranking

 Export to PDF/ePub

 Chapter-title-based identifiers

 RAG-enabled smart summary generation

🤝 Contributors
Arpan Mishra — Core Developer

Let me know if you'd like this turned into a live README.md file or added to GitHub with badge/shields. I can also generate a short demo video script if you're planning a showcase.