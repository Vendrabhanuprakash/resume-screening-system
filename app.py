from flask import Flask, render_template, request
import os

from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    skill_analysis
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]

    jd = request.form["job_description"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    resume_text = extract_text_from_pdf(filepath)

    resume_text = clean_text(resume_text)

    jd = clean_text(jd)

    score = calculate_similarity(
        resume_text,
        jd
    )

    matching, missing = skill_analysis(
        resume_text,
        jd
    )

    return render_template(
        "result.html",
        score=score,
        matching=matching[:20],
        missing=missing[:20]
    )


if __name__ == "__main__":
    app.run(debug=True)