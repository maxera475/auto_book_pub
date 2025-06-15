import streamlit as st
import difflib
import requests
import datetime

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Human-in-the-Loop AI Editor", layout="wide")
st.title("🧠 Human-in-the-Loop AI Content Editor")

st.sidebar.header("📋 Chapter Settings")
url_list = st.sidebar.text_area("Enter one or more chapter URLs (one per line)", "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")
chapter_name_prefix = st.sidebar.text_input("Chapter Name Prefix", "chapter")

if st.sidebar.button("🚀 Load Chapters & AI Versions"):
    urls = url_list.strip().splitlines()
    st.session_state['chapters'] = []
    for idx, url in enumerate(urls):
        chapter_name = f"{chapter_name_prefix}{idx+1}"
        with st.spinner(f"Processing {chapter_name}..."):
            response = requests.post(f"{API_BASE_URL}/scrape_and_process/", params={"url": url, "chapter_name": chapter_name})
            if response.status_code == 200:
                data = response.json()
                data['chapter_name'] = chapter_name
                st.session_state['chapters'].append(data)
            else:
                st.error(f"Failed to process {chapter_name}: {response.text}")

if 'chapters' in st.session_state:
    for chapter in st.session_state['chapters']:
        chapter_name = chapter['chapter_name']

        def load_file(filename):
            return requests.get(f"{API_BASE_URL}/get/{filename}").text

        st.markdown(f"## 📘 Chapter: {chapter_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📄 Original")
            original = load_file(chapter_name + ".txt")
            st.text_area(f"Original - {chapter_name}", original, height=400, disabled=True)

        with col2:
            st.subheader("📝 AI Written")
            ai_written = load_file(chapter_name + "_spun.txt")
            st.text_area(f"AI - {chapter_name}", ai_written, height=400, disabled=True)

        with col3:
            st.subheader("✍️ Human Editor")
            user_edit = st.text_area(f"Edit - {chapter_name}", ai_written, height=400)
            if f'human_edited_{chapter_name}' not in st.session_state:
                st.session_state[f'human_edited_{chapter_name}'] = user_edit

            if st.button(f"💬 Comment - {chapter_name}"):
                st.session_state[f'comment_{chapter_name}'] = st.text_input("Comment on your change:")

            if st.button(f"✅ Finalize - {chapter_name}"):
                st.session_state[f'human_edited_{chapter_name}'] = user_edit
                comment = st.session_state.get(f'comment_{chapter_name}', "")
                version_id = datetime.datetime.now().isoformat()
                save_response = requests.post(
                    f"{API_BASE_URL}/save_version/",
                    params={
                        "chapter_name": chapter_name,
                        "version_id": version_id,
                        "text": user_edit,
                        "comment": comment
                    }
                )
                if save_response.status_code == 200:
                    st.success("Version saved to vector store.")
                else:
                    st.error(f"Failed to save version: {save_response.text}")

        if st.checkbox(f"🔍 Show Diff - {chapter_name}"):
            diff = difflib.unified_diff(ai_written.splitlines(), user_edit.splitlines(), lineterm="")
            st.code("\n".join(diff), language="diff")

        if f'comment_{chapter_name}' in st.session_state:
            st.info(f"💬 Comment: {st.session_state[f'comment_{chapter_name}']}")

        # Download buttons for each version
        for label, file_key in {
            "📄 Download Original": f"{chapter_name}.txt",
            "📝 Download Rewritten": f"{chapter_name}_spun.txt",
            "✅ Download Final": f"{chapter_name}_final.txt",
        }.items():
            file_data = requests.get(f"{API_BASE_URL}/get/{file_key}").text
            st.download_button(label, data=file_data, file_name=file_key)

else:
    st.info("👈 Enter one or more URLs and click 'Load Chapters & AI Versions' to begin.")

st.subheader("🔍 Search Saved Versions")
query = st.text_input("Search by topic or phrase")
top_k = st.slider("Number of results to return:", min_value=1, max_value=10, value=3)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        try:
            with st.spinner("Searching version store..."):
                response = requests.get(
                    f"{API_BASE_URL}/search_versions/",
                    params={"query": query, "top_k": top_k},
                    timeout=15
                )
                if response.status_code == 200:
                    results = response.json()["matches"]
                    if results:
                        for idx, match in enumerate(results):
                            st.markdown(f"### 📌 Match {idx + 1}")
                            st.text_area("Text", match["text"], height=250)
                            st.json(match["metadata"])
                    else:
                        st.info("No matching versions found.")
                else:
                    st.error(f"Search failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
