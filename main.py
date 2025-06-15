from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
from writer_ollama import ai_writer
from reviewer_ollama import ai_reviewer

app = FastAPI()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

@app.post("/scrape_and_process/")
def scrape_and_process(url: str, chapter_name: str = "chapter1"):
    try:
        # Step 1: Run Playwright scrapper as subprocess
        print("[*] Scraping via subprocess...")
        result = subprocess.run(
            ["python", "scrapper.py", url, chapter_name],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Scraper failed:\n{result.stderr}")

        # Step 2: Load scraped text
        text_path = os.path.join(output_dir, f"{chapter_name}.txt")
        with open(text_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Step 3: Rewrite
        spun_text = ai_writer(raw_text)
        spun_path = os.path.join(output_dir, f"{chapter_name}_spun.txt")
        with open(spun_path, "w", encoding="utf-8") as f:
            f.write(spun_text)

        # Step 4: Review
        final_text = ai_reviewer(spun_text)
        final_path = os.path.join(output_dir, f"{chapter_name}_final.txt")
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        return {
            "message": "Scraping + AI processing complete",
            "raw_text": text_path,
            "screenshot": os.path.join(output_dir, f"{chapter_name}.png"),
            "rewritten": spun_path,
            "final": final_path
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/{filename}")
def get_file(filename: str):
    path = os.path.join(output_dir, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain")
    else:
        raise HTTPException(status_code=404, detail="File not found")


from vector_store import add_version, search_versions
import datetime

@app.post("/save_version/")
def save_version_api(chapter_name: str, version_id: str, text: str, comment: str = ""):
    metadata = {
        "version_id": version_id,
        "comment": comment,
        "timestamp": str(datetime.datetime.now()),
        "status": "final"
    }
    try:
        add_version(chapter_name, text, metadata)
        return {"message": "Version saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search_versions/")
def search_versions_api(query: str, top_k: int = 3):
    try:
        return search_versions(query, top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
