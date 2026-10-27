import spacy
import re
from pypdf import PdfReader
import pandas as pd

nlp = spacy.load("en_core_web_sm")

resume = input("Path to resume?")


def load_skills(csvpath):
    df = pd.read_csv(csvpath)
    skillslist = df["Skill Name"].tolist()
    lowerlist = [item.lower() for item in skillslist]
    return lowerlist


def extract_text(path):
    reader = PdfReader(path)
    text = "\n".join(p.extract_text() for p in reader.pages)
    return text


def extract_email(emailtext):
    email_pattern = r"\b[a-za-z0-9._%+-]+@[a-za-z0-9.-]+\.[a-za-z]{2,}\b"
    match = re.search(email_pattern, emailtext)
    email = match.group if match else None
    return email


def extract_phone(phonetext):
    phone_pattern = r"\+?\b[0-9]{1,4}[-.\s]?\(?[0-9]{1,3}\)?[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,6}\b"
    match = re.search(phone_pattern, phonetext)
    phone = match.group if match else None
    return phone


def extract_name(nametext):
    doc = nlp(nametext)
    for entity in doc.ents:
        if entity.label == "PERSON":
            return entity
        else:
            return "No name found! (english)"


def extract_skills(skillstext, skillslist):
    text = skillstext.lower()
    found = []
    for skill in skillslist:
        pattern = r"(?<![\w+#])" + re.escape(skill) + r"(?![\w+#])"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(found)


def extract_degrees(text):
    degree_words = [
        "bsc",
        "b.sc",
        "beng",
        "b.eng",
        "btech",
        "b.tech",
        "bachelor",
        "msc",
        "m.sc",
        "meng",
        "m.eng",
        "mtech",
        "m.tech",
        "master of",
        "master's",
        "masters",
        "mba",
        "phd",
        "ph.d",
        "hnd",
        "ond",
    ]
    university_words = ["University", "College", "Polythecnic"]
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = []
    for i, line in enumerate(lines):
        if any(d in line.lower() for d in degree_words):
            uni = next(
                (
                    l
                    for l in lines[i : i + 3]
                    if any(u in l.lower() for u in university_words)
                ),
                None,
            )
            results.append([line, uni])
    return results


final_results = [
    extract_name(resume),
    extract_email(resume),
    extract_phone(resume),
    extract_skills(resume, "technical_skills.csv"),
    extract_degrees(resume),
]

final = pd.DataFrame(
    columns=["name", "email", "phone", "skills", "degree", "university"]
)
final.loc[len(final)] = final_results
