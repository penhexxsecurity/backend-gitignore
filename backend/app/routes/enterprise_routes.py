import io
from flask import Blueprint, request, jsonify, send_file
from app.services.firestore_service import save_enterprise_incident
from xhtml2pdf import pisa

enterprise_bp = Blueprint("enterprise_bp", __name__)

@enterprise_bp.route("/submit", methods=["POST"])
def submit_enterprise_incident():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Request body is empty"}), 400

        required_fields = ["name", "email", "phone", "company", "clientId", "message"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        if not data.get("severity"):
            data["severity"] = "high"

        result = save_enterprise_incident(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "🚨 Enterprise incident logged successfully. Security team notified.",
                "incident_id": result.get("id"),
                "priority": "P1_ACTIVE"
            }), 200

        return jsonify(result), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500


@enterprise_bp.route("/generate-invoice-pdf", methods=["POST"])
def generate_invoice_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Payload is empty"}), 400

        tracking_id = data.get('trackingId', 'PHX-ENT-0000')
        timestamp = data.get('timestamp', '')
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        company = data.get('company', '')
        website = data.get('website', '')
        message = data.get('message', '')
        client_id = data.get('clientId', 'N/A')
        severity = data.get('severity', 'HIGH').upper()

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
                    color: #ef4444;
                    text-transform: uppercase;
                    font-weight: bold;
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
                        <span class="company-name">PENHEX SECURITY [EMERGENCY]</span><br>
                        <span class="invoice-tag">🚨 Critical Incident Receipt</span>
                    </td>
                    <td class="header-td" style="text-align: right; font-size: 9pt; color: #4b5563;">
                        <strong>Incident Hub:</strong> security@penhexx.com<br>
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
                        Tracking Reference: <span class="meta-highlight" style="color: #ef4444;">{tracking_id}</span><br>
                        Timestamp: <span class="meta-highlight">{timestamp}</span><br>
                        Tunnel Verification: <span class="meta-highlight">P1_DISPATCH_CHANNEL</span>
                    </td>
                </tr>
            </table>

            <div class="section-title">Incident Parameter Specifications</div>
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
                        <td class="data-td">Route: /ENTERPRISE</td>
                    </tr>
                    <tr>
                        <td class="data-td label-cell">PenHex Client Key</td>
                        <td class="data-td" style="color: #111827; font-weight: bold;">{client_id}</td>
                    </tr>
                    <tr>
                        <td class="data-td label-cell">Severity Triage</td>
                        <td class="data-td" style="color: #ef4444; font-weight: bold;">{severity}</td>
                    </tr>
                </tbody>
            </table>

            <div class="section-title">Incident Parameters / Description Context</div>
            <div class="description-box">
                {message}
            </div>

            <div class="footer-notice">
                This document indicates an active infrastructure anomaly paging event. Highly confidential security clearance record. PenHex Inc. © 2026.
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
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"PenHex_Incident_Record_{tracking_id}.pdf"
        )

    except Exception as e:
        print("PDF Backend Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500