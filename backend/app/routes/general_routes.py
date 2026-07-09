import io
from flask import Blueprint, request, jsonify, send_file
# firestore_service से आवश्यक सभी फंक्शन्स इम्पोर्ट करें
from app.services.firestore_service import (
    save_general_query, 
    save_career_application, 
    get_all_vulnerabilities
)
from xhtml2pdf import pisa

general_bp = Blueprint("general_bp", __name__)


# -----------------------------------
# NEW: LIVE VULNERABILITIES ROUTE
# -----------------------------------
@general_bp.route("/vulnerabilities", methods=["GET"])
def fetch_live_vulnerabilities():
    """
    Streams dynamic security vulnerabilities logged via the Admin Panel 
    to populate the Research Labs analytical grid.
    """
    try:
        records = get_all_vulnerabilities()
        
        # यदि सर्विस से डिक्शनरी एरर रिस्पॉन्स आता है
        if isinstance(records, dict) and "error" in records:
            return jsonify({"success": False, "error": records["error"]}), 500
            
        return jsonify({
            "success": True, 
            "data": records
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500


# -----------------------------------
# NEW: CAREER APPLICATION ROUTE
# -----------------------------------
@general_bp.route("/careers", methods=["POST"])
def apply_for_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Request body is empty"}), 400

        # Frontend variables के साथ exact mapping
        required_fields = ["fullName", "email", "phone", "employmentType", "experience", "resumeLink"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        # आपकी अपडेटेड सर्विस को कॉल करें
        result = save_career_application(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "Career application saved successfully",
                "application_id": result.get("id")
            }), 201

        return jsonify(result), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500


# -----------------------------------
# GENERAL BUSINESS QUERY ROUTE
# -----------------------------------
@general_bp.route("/submit", methods=["POST"])
def submit_general_query():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Request body is empty"}), 400

        # Frontend variables ke sath exact mapping (lowercase fields)
        required_fields = ["name", "email", "phone", "company", "website", "message"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        result = save_general_query(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "General query submitted successfully",
                "query_id": result.get("id"),
                "status": "received"
            }), 200

        return jsonify(result), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500


# -----------------------------------
# DYNAMIC PDF INVOICE GENERATION ROUTE
# -----------------------------------
@general_bp.route("/generate-invoice-pdf", methods=["POST"])
def generate_invoice_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Payload is empty"}), 400

        # Extract data components safely matching frontend payload names
        tracking_id = data.get('trackingId', 'PHX-GEN-0000')
        timestamp = data.get('timestamp', '')
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        company = data.get('company', '')
        website = data.get('website', '')
        message = data.get('message', '')
        service_plan = data.get('service', 'web-app') # Converted back to 'service' to match frontend

        # Map dynamic service plans to readable string formats
        service_mapping = {
            "web-app": "1. Web Application Security Testing Plans",
            "api-security": "2. API Security Testing Plans",
            "cloud-assessment": "3. Cloud Security Assessment Plans",
            "penhexx-360": "4. Penhexx 360 Security Suite (Combo Plans)",
            "awareness-training": "5. Security Awareness Training"
        }
        readable_service = service_mapping.get(service_plan, service_plan)

        # Clean Professional Light Layout (Microsoft Reference Design)
        html_content = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: a4;
                    margin: 15mm 12mm;
                }}
                body {{
                    background-color: #ffffff;
                    color: #1f2937;
                    font-family: Helvetica, Arial, sans-serif;
                    line-height: 1.4;
                }}
                .invoice-header-table {{
                    width: 100%;
                    border-bottom: 1px solid #e5e7eb;
                    margin-bottom: 25px;
                }}
                .header-td {{
                    background-color: #ffffff;
                    border: none;
                    padding: 0px 0px 15px 0px;
                }}
                .company-name {{
                    font-size: 24pt;
                    font-weight: bold;
                    color: #111827;
                }}
                .invoice-tag {{
                    font-size: 10pt;
                    color: #4b5563;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .meta-table {{
                    width: 100%;
                    margin-bottom: 30px;
                }}
                .meta-td {{
                    width: 50%;
                    vertical-align: top;
                    font-size: 9.5pt;
                    color: #4b5563;
                    background-color: #ffffff;
                    border: none;
                    padding: 0px;
                }}
                .meta-highlight {{
                    color: #111827;
                    font-weight: bold;
                }}
                .section-title {{
                    font-size: 11pt;
                    font-weight: bold;
                    color: #111827;
                    margin-top: 20px;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .data-table {{
                    width: 100%;
                    margin-bottom: 25px;
                }}
                th {{
                    background-color: #f9fafb;
                    color: #374151;
                    font-size: 9pt;
                    text-transform: uppercase;
                    font-weight: bold;
                    padding: 10px;
                    text-align: left;
                    border-bottom: 2px solid #e5e7eb;
                }}
                .data-td {{
                    padding: 10px;
                    font-size: 9.5pt;
                    border-bottom: 1px solid #f3f4f6;
                    color: #374151;
                    background-color: #ffffff;
                }}
                .label-cell {{
                    color: #6b7280;
                    font-weight: bold;
                    width: 35%;
                }}
                .description-box {{
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    padding: 15px;
                    font-size: 9.5pt;
                    color: #374151;
                    margin-top: 5px;
                }}
                .footer-notice {{
                    text-align: center;
                    margin-top: 60px;
                    font-size: 8pt;
                    color: #9ca3af;
                    border-top: 1px solid #e5e7eb;
                    padding-top: 15px;
                }}
            </style>
        </head>
        <body>
            <table class="invoice-header-table">
                <tr>
                    <td class="header-td" style="text-align: left;">
                        <span class="company-name">PENHEX SECURITY</span><br>
                        <span class="invoice-tag">Secure Transmission Receipt</span>
                    </td>
                    <td class="header-td" style="text-align: right; font-size: 9pt; color: #4b5563;">
                        <strong>Corporate HeadNode:</strong> contact@penhexx.com<br>
                        <strong>Web Infrastructure:</strong> www.penhexx.com<br>
                        <strong>Authority Signatory:</strong> Tushar Kaushik, CEO
                    </td>
                </tr>
            </table>

            <table class="meta-table">
                <tr>
                    <td class="meta-td" style="text-align: left;">
                        <strong style="color: #111827; font-size: 10pt;">Issued To (Client Node):</strong><br>
                        <span class="meta-highlight">{name}</span><br>
                        {company}<br>
                        {email}<br>
                        {phone}<br>
                        <span style="font-size: 8.5pt; color: #6b7280;">{website}</span>
                    </td>
                    <td class="meta-td" style="text-align: right;">
                        <strong style="color: #111827; font-size: 10pt;">Transaction Metadata:</strong><br>
                        Tracking Reference: <span class="meta-highlight" style="color: #111827;">{tracking_id}</span><br>
                        Timestamp: <span class="meta-highlight">{timestamp}</span><br>
                        Tunnel Verification: <span class="meta-highlight">TLS_AES_256_GCM</span>
                    </td>
                </tr>
            </table>

            <div class="section-title">Parameter Record Specifications</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Structure Layer</th>
                        <th>Registered Core Context Metric</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="data-td label-cell">Pipeline Domain Path</td>
                        <td class="data-td">Route: /GENERAL</td>
                    </tr>
                    <tr>
                        <td class="data-td label-cell">Service Blueprint Plan</td>
                        <td class="data-td" style="color: #111827; font-weight: bold;">{service_plan}</td>
                    </tr>
                </tbody>
            </table>

            <div class="section-title">Project Description / Scope</div>
            <div class="description-box">
                {message}
            </div>

            <div class="footer-notice">
                All parameters scanned and processed under secure infrastructure protocols. Confidential transaction payload document. PenHex Inc. © 2026.
            </div>
        </body>
        </html>
        """

        pdf_stream = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_stream)

        if pisa_status.err:
            return jsonify({"success": False, "message": "PDF layout engine generation error"}), 500
        pdf_stream.seek(0)

        return send_file(
            pdf_stream,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"PenHex_Invoice_{tracking_id}.pdf"
)

    except Exception as e:
        print("PDF Backend Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# HEALTH CHECK ENDPOINT
# -----------------------------------
@general_bp.route("/health", methods=["GET"])
def general_health():
    return jsonify({
        "status": "ok",
        "service": "PenHex General Query API Sub-router",
        "mode": "active"
    }), 200