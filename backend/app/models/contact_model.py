from datetime import datetime
import uuid


class ContactModel:
    def __init__(self, data, form_type="general"):
        """
        form_type: 'general' or 'enterprise'
        """

        self.id = str(uuid.uuid4())
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.website = data.get("website")
        self.company = data.get("company")
        self.message = data.get("message")

        # Form classification
        self.form_type = form_type

        # General specific
        self.service = data.get("service", None)

        # Enterprise specific
        self.client_id = data.get("clientId", None)
        self.severity = data.get("severity", None)

        # Metadata
        self.status = "new"
        self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        """
        Convert object into Firestore-ready dictionary
        """

        base_data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "company": self.company,
            "message": self.message,
            "form_type": self.form_type,
            "status": self.status,
            "created_at": self.created_at,
        }

        # Add general form fields if present
        if self.service:
            base_data["service"] = self.service

        # Add enterprise fields if present
        if self.client_id:
            base_data["client_id"] = self.client_id

        if self.severity:
            base_data["severity"] = self.severity

        return base_data