import spacy
import re
from pypdf import PdfReader

nlp = spacy.load("en_core_web_sm")


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
