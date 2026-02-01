import os
from fpdf import FPDF
from datetime import datetime

class ForensicReporter:
    def __init__(self):
        self.evidence_dir = "evidence_locker"
        if not os.path.exists(self.evidence_dir):
            os.makedirs(self.evidence_dir)

    def add_report(self, scan_data):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt="SENTINEL LINK: FORENSIC REPORT", ln=True, align='C')
            pdf.ln(10)
            
            # Metadata
            pdf.set_font("Arial", size=10)
            pdf.cell(190, 8, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.cell(190, 8, txt=f"Target URL: {scan_data.get('url')}", ln=True)
            pdf.cell(190, 8, txt=f"Risk Score: {scan_data.get('risk_score')}/100", ln=True)
            
            # Flags
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, txt="DETECTED THREATS:", ln=True)
            pdf.set_font("Arial", size=10)
            for flag in scan_data.get('flags', []):
                pdf.cell(190, 6, txt=f"[!] {flag}", ln=True)
                
            # Network Data
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, txt="SERVER FINGERPRINT:", ln=True)
            pdf.set_font("Courier", size=9)
            logs = str(scan_data.get('network_logs', {}))
            pdf.multi_cell(0, 5, txt=logs)

            # Save File
            filename = f"evidence_{datetime.now().strftime('%H%M%S')}.pdf"
            file_path = os.path.join(self.evidence_dir, filename)
            pdf.output(file_path)
            
            # RETURN ABSOLUTE PATH
            return os.path.abspath(file_path)

        except Exception as e:
            print(f"PDF Error: {e}")
            return os.path.abspath(os.path.join(self.evidence_dir, "error_log.pdf"))