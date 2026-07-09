import uuid
from datetime import datetime, timezone
from app.firebase import get_db

# -----------------------------
# COMMON UTILITIES
# -----------------------------
def get_timestamp():
    """Generates a safe, timezone-aware UTC ISO 8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


def generate_id(prefix="PHX"):
    """Generates a standard 10-character hexadecimal suffix alphanumeric ID."""
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


# -----------------------------
# GENERAL CONTACT FORM STORAGE
# -----------------------------
def save_general_query(data):
    try:
        db = get_db()
        doc_id = generate_id("GEN")

        payload = {
            "id": doc_id,
            "type": "general",
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "company": data.get("company"),
            "website": data.get("website"),
            "service": data.get("service"),
            "message": data.get("message"),
            "status": "new",
            "created_at": get_timestamp()
        }

        # Save documents using explicit custom generated ID
        db.collection("general_queries").document(doc_id).set(payload)

        return {
            "success": True,
            "message": "General query saved successfully",
            "id": doc_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------
# ENTERPRISE EMERGENCY STORAGE
# -----------------------------
def save_enterprise_incident(data):
    try:
        db = get_db()
        doc_id = generate_id("ENT")

        payload = {
            "id": doc_id,
            "type": "enterprise_emergency",
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "company": data.get("company"),
            "website": data.get("website"),
            "client_id": data.get("clientId"),
            "severity": data.get("severity", "high"),
            "message": data.get("message"),
            "status": "critical",
            "priority": "P1",
            "created_at": get_timestamp()
        }

        db.collection("enterprise_incidents").document(doc_id).set(payload)

        return {
            "success": True,
            "message": "Enterprise incident logged successfully",
            "id": doc_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------
# CAREER APPLICATION STORAGE
# -----------------------------
def save_career_application(data):
    try:
        db = get_db()
        doc_id = generate_id("CAR")  # Career के लिए CAR प्रीफ़िक्स

        payload = {
            "id": doc_id,
            "type": "career",
            "job_role": data.get("jobRole"),
            "full_name": data.get("fullName"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "employment_type": data.get("employmentType"),
            "experience": data.get("experience"),
            "github": data.get("github"),
            "linkedin": data.get("linkedin"),
            "resume_link": data.get("resumeLink"),
            "cover_letter": data.get("coverLetter"),
            "status": "applied",
            "created_at": get_timestamp()
        }

        # स्पष्ट रूप से कस्टम जेनरेटेड ID के साथ स्टोर करें
        db.collection("career_applications").document(doc_id).set(payload)

        return {
            "success": True,
            "message": "Career application saved successfully",
            "id": doc_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------
# RESEARCH VULNERABILITY STORAGE (NEW - FOR ADMIN PANEL)
# -----------------------------
def save_vulnerability(data):
    """
    Invoked by the Admin Panel engine to securely save or update core 
    vulnerability payloads targeted for public streaming on the Research Lab interface.
    """
    try:
        db = get_db()
        doc_id = generate_id("VUL")  # Vulnerability के लिए VUL प्रीफ़िक्स

        payload = {
            "id": doc_id,
            "type": "vulnerability",
            "title": data.get("title"),
            "tag": data.get("tag"),
            "level": data.get("level"),
            "desc": data.get("desc"),
            "details": data.get("details"),
            "impact": data.get("impact"),
            "attackScenario": data.get("attackScenario"),
            "mitigation": data.get("mitigation"),
            "created_at": get_timestamp()
        }

        # Save explicitly via clean structured custom generated ID block
        db.collection("research_reports").document(doc_id).set(payload)

        return {
            "success": True,
            "message": "Vulnerability record written to global node securely.",
            "id": doc_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------
# FETCH FUNCTIONS (Dashboard Ready)
# -----------------------------
def get_all_general_queries(limit=50):
    try:
        db = get_db()
        # .stream() executes the query and reads documents as a generator
        docs = db.collection("general_queries").order_by("created_at", direction="DESCENDING").limit(limit).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        return {"error": str(e)}


def get_all_enterprise_incidents(limit=50):
    try:
        db = get_db()
        docs = db.collection("enterprise_incidents").order_by("created_at", direction="DESCENDING").limit(limit).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        return {"error": str(e)}


def get_all_career_applications(limit=50):
    """Fetches all logged career applications ordered by creation timestamp."""
    try:
        db = get_db()
        docs = db.collection("career_applications").order_by("created_at", direction="DESCENDING").limit(limit).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        return {"error": str(e)}


def get_all_vulnerabilities(limit=50):
    try:
        db = get_db()
        docs = (
            db.collection("research_reports")
            .order_by("created_at", direction="DESCENDING")
            .limit(limit)
            .stream()
        )

        return [doc.to_dict() for doc in docs]

    except Exception as e:
        return {"error": str(e)}