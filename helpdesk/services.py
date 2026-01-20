# helpdesk/services.py

# =====================================
# LOAD CAMPUS DATA
# =====================================
def load_campus_data():
    try:
        with open("helpdesk/campus_data.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


# =====================================
# EXTRACT SECTION FROM CAMPUS DATA
# =====================================
def extract_section(data, section_name):
    start_tag = f"[{section_name}]"
    if start_tag not in data:
        return None

    section = data.split(start_tag, 1)[1]
    section = section.split("[", 1)[0]
    return section.strip()


# =====================================
# INTENT DETECTION (LIGHT + SAFE)
# =====================================
def detect_intent(question):
    q = question.lower()

    # Academic / advice intent
    if any(p in q for p in [
        "how to", "how can i", "tips", "improve",
        "score more", "study", "prepare", "focus",
        "stress", "exam fear", "motivation"
    ]):
        return "ACADEMIC_ADVICE"

    # Exams
    if "exam" in q and any(w in q for w in ["when", "date", "schedule"]):
        return "EXAMS"

    # Fees
    if any(w in q for w in ["fee", "fees", "payment", "pay"]):
        return "FEES"

    # Scholarships
    if "scholarship" in q:
        return "SCHOLARSHIPS"

    # Placements
    if any(w in q for w in ["placement", "job", "internship"]):
        return "PLACEMENTS"

    # Contacts
    if any(w in q for w in ["contact", "email", "office"]):
        return "CONTACTS"

    return None


# =====================================
# GENERAL AI-STYLE RESPONSE (SAFE FALLBACK)
# =====================================
def generate_general_ai_response(question):
    return (
        "I understand your concern.\n\n"
        f"You asked:\n\"{question}\"\n\n"
        "Here are some helpful suggestions:\n"
        "- Break the problem into smaller steps\n"
        "- Focus on understanding concepts, not memorization\n"
        "- Practice regularly and review mistakes\n"
        "- Maintain a balanced routine (sleep + revision)\n"
        "- Reach out to faculty or mentors when stuck\n\n"
        "If you want, ask a more specific follow-up question."
    )


# =====================================
# MAIN CAMPUS AI SERVICE (CORE LOGIC)
# =====================================
def ask_campus_ai(question):
    campus_data = load_campus_data()
    intent = detect_intent(question)

    # 1️⃣ Academic guidance → AI-style response
    if intent == "ACADEMIC_ADVICE":
        return generate_general_ai_response(question)

    # 2️⃣ Administrative facts → campus_data.txt
    if intent in ["EXAMS", "FEES", "SCHOLARSHIPS", "PLACEMENTS", "CONTACTS"]:
        section_data = extract_section(campus_data, intent)
        if section_data:
            return (
                "Here’s what I found regarding your question:\n\n"
                f"{section_data}\n\n"
                "— Based on official campus information."
            )

    # 3️⃣ EVERYTHING ELSE → friendly AI fallback
    return generate_general_ai_response(question)
