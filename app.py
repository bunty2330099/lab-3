from flask import Flask, render_template, request
import ollama
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""

    if request.method == "POST":
        mode = request.form["mode"]

        if mode == "document":
            document_text = request.form["document_text"]
            question = request.form["question"]

            prompt = f"""
            Answer only from the document.

            {document_text[:3000]}

            Question:
            {question}
            """

        elif mode == "scrape":
            url = request.form["url"]
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            scraped_text = soup.get_text()

            prompt = f"""
            Summarize this webpage:

            {scraped_text[:3000]}
            """

        result = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        response = result["message"]["content"]

    return render_template("dashboard.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
