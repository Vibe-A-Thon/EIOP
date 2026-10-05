"""Generate real document files for the EOIP demo.

Creates .docx, .xlsx, .pptx, .csv, and .txt files in demo/demodata/documents/.
These are actual binary/text files that can be opened by their respective apps.

Usage:
    python -m demo.autodemo.generate_documents
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1] / "demodata" / "documents"


def _ensure_deps():
    try:
        import docx  # noqa: F401
        import openpyxl  # noqa: F401
        import pptx  # noqa: F401
    except ImportError:
        print("Installing required packages: python-docx, openpyxl, python-pptx")
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install",
             "python-docx", "openpyxl", "python-pptx", "--quiet"],
        )


def create_architecture_doc():
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    doc.add_heading("MFS Payment Gateway Architecture v2", 0)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Meridian Financial Services — Confidential").italic = True

    doc.add_heading("1. Overview", level=1)
    doc.add_paragraph(
        "The MFS Payment Gateway v2 is the core payment processing platform for "
        "Meridian Financial Services. It handles payment authorization, tokenization, "
        "settlement, and merchant webhook notifications. The platform processes "
        "approximately 2.5 million transactions daily with a 99.95% availability SLO."
    )

    doc.add_heading("2. Infrastructure Topology", level=1)
    doc.add_heading("2.1 OpenShift Pods", level=2)
    table = doc.add_table(rows=4, cols=4, style="Light Grid Accent 1")
    headers = ["Pod", "Namespace", "Replicas", "Services"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    data = [
        ["mfs-pay-pod-01", "mfs-payments", "4", "Payment processing, tokenization, webhook"],
        ["mfs-pay-pod-02", "mfs-payments", "2", "Payment processing (secondary)"],
        ["mfs-pay-pod-03", "mfs-payments", "2", "Analytics, settlement processing"],
    ]
    for r, row_data in enumerate(data, 1):
        for c, val in enumerate(row_data):
            table.rows[r].cells[c].text = val

    doc.add_heading("2.2 Databases", level=2)
    table2 = doc.add_table(rows=3, cols=4, style="Light Grid Accent 1")
    for i, h in enumerate(["Host", "Database", "Service Account", "Purpose"]):
        table2.rows[0].cells[i].text = h
    db_data = [
        ["pghost-prod-01.mfs.internal", "mfs_payments_db", "svc-payment-api", "Payment transactions"],
        ["pghost-prod-03.mfs.internal", "mfs_audit_db", "svc-payment-api", "Audit and compliance logs"],
    ]
    for r, row_data in enumerate(db_data, 1):
        for c, val in enumerate(row_data):
            table2.rows[r].cells[c].text = val

    doc.add_heading("2.3 Service Accounts", level=2)
    for sa in ["svc-payment-api", "svc-token-vault", "svc-webhook-dispatch", "svc-analytics"]:
        doc.add_paragraph(sa, style="List Bullet")

    doc.add_heading("3. Key Tables", level=1)
    doc.add_paragraph(
        "payments, payment_methods, tokens, idempotency_keys, "
        "webhook_registrations, webhook_delivery_log, webhook_dlq, "
        "analytics_aggregates, settlement_batches, reconciliation_records"
    )

    doc.add_heading("4. External Dependencies", level=1)
    deps = [
        "hsm-gateway.mfs.internal:8443 — Hardware Security Module (tokenization)",
        "vault.mfs.internal — HashiCorp Vault (secrets management)",
        "redis-cluster.mfs.internal — Redis (idempotency cache, rate limiting)",
        "kafka-broker.mfs.internal:9092 — Kafka (event streaming)",
    ]
    for d in deps:
        doc.add_paragraph(d, style="List Bullet")

    path = OUT_DIR / "MFS-Payment-Gateway-Architecture-v2.docx"
    doc.save(str(path))
    print(f"  Created {path.name}")


def create_compliance_doc():
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    doc.add_heading("MFS PCI DSS Compliance Report", 0)
    doc.add_paragraph("Meridian Financial Services — Q3 2026 Assessment")

    doc.add_heading("Executive Summary", level=1)
    doc.add_paragraph(
        "This report summarizes PCI DSS v4.0 compliance status for the MFS Payment "
        "Gateway platform. Overall compliance: 94% of controls satisfied. "
        "6 controls require remediation before the Q4 2026 assessment deadline."
    )

    doc.add_heading("Requirement Coverage", level=1)
    requirements = [
        ("1. Network Security", "PASS", "Firewall rules, network segmentation verified"),
        ("2. Default Passwords", "PASS", "No default credentials in production"),
        ("3. Protect Stored Data", "PASS", "AES-256 encryption at rest for PAN data"),
        ("4. Encrypt Transmission", "PASS", "TLS 1.3 for all in-transit data"),
        ("5. Anti-Virus", "PASS", "CrowdStrike deployed on all nodes"),
        ("6. Secure Systems", "PARTIAL", "2 pods missing latest security patches"),
        ("7. Access Control", "PASS", "RBAC with least-privilege service accounts"),
        ("8. Unique IDs", "PASS", "Individual service accounts per service"),
        ("9. Physical Access", "PASS", "Cloud provider controls verified"),
        ("10. Logging", "PARTIAL", "Audit log retention needs extension to 12 months"),
        ("11. Security Testing", "PASS", "Quarterly penetration testing completed"),
        ("12. Security Policy", "PASS", "Information security policy reviewed and updated"),
    ]
    table = doc.add_table(rows=len(requirements) + 1, cols=3, style="Light Grid Accent 1")
    for i, h in enumerate(["Requirement", "Status", "Evidence"]):
        table.rows[0].cells[i].text = h
    for r, (req, status, evidence) in enumerate(requirements, 1):
        table.rows[r].cells[0].text = req
        table.rows[r].cells[1].text = status
        table.rows[r].cells[2].text = evidence

    doc.add_heading("Remediation Items", level=1)
    doc.add_paragraph("REQ-6: Apply security patches to mfs-pay-pod-02 and mfs-pay-pod-03", style="List Number")
    doc.add_paragraph("REQ-10: Extend Kibana audit log retention from 90 days to 365 days", style="List Number")

    path = OUT_DIR / "MFS-PCI-DSS-Compliance-Report.docx"
    doc.save(str(path))
    print(f"  Created {path.name}")


def create_fraud_architecture_doc():
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    doc.add_heading("MFS Fraud Detection ML Architecture", 0)
    doc.add_paragraph("Meridian Financial Services — Technical Design Document")

    doc.add_heading("1. ML Pipeline Overview", level=1)
    doc.add_paragraph(
        "The fraud detection platform uses a multi-stage ML pipeline: "
        "raw transaction ingestion via Kafka, real-time feature extraction (47 features), "
        "fraud scoring via XGBoost model, and result publishing to downstream consumers. "
        "Model serving achieves sub-50ms p99 latency via ONNX Runtime on mfs-fraud-pod-01/02."
    )

    doc.add_heading("2. Model Versioning", level=1)
    table = doc.add_table(rows=4, cols=5, style="Light Grid Accent 1")
    for i, h in enumerate(["Version", "AUC", "Precision", "Recall", "FP Rate"]):
        table.rows[0].cells[i].text = h
    versions = [
        ["v2.1", "0.978", "0.955", "0.948", "2.1%"],
        ["v2.2 (champion)", "0.982", "0.961", "0.954", "1.8%"],
        ["v2.3 (challenger)", "0.985", "0.948", "0.967", "4.2%"],
    ]
    for r, row_data in enumerate(versions, 1):
        for c, val in enumerate(row_data):
            table.rows[r].cells[c].text = val

    doc.add_heading("3. Feature Engineering", level=1)
    doc.add_paragraph("47 features across 5 categories:")
    for cat in ["Transaction (amount, currency, merchant_category, channel)",
                "Velocity (1min/5min/1hr/24hr counts per account/merchant/device)",
                "Device (fingerprint hash, IP geolocation, browser profile)",
                "Account (age, history length, average transaction amount)",
                "Merchant (risk score, category code, country risk level)"]:
        doc.add_paragraph(cat, style="List Bullet")

    doc.add_heading("4. Infrastructure", level=1)
    doc.add_paragraph("Pods: mfs-fraud-pod-01, mfs-fraud-pod-02 (scoring), mfs-model-pod-01 (training)")
    doc.add_paragraph("Database: mfs_fraud_db on pghost-prod-02.mfs.internal")
    doc.add_paragraph("MLflow: mlflow.mfs.internal (experiment tracking, model registry)")
    doc.add_paragraph("Feature Store: feast.mfs.internal (online/offline feature serving)")

    path = OUT_DIR / "MFS-Fraud-Detection-ML-Architecture.docx"
    doc.save(str(path))
    print(f"  Created {path.name}")


def create_postmortem_doc():
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    doc.add_heading("Incident Postmortem — INC0080101", 0)
    doc.add_paragraph("Payment Gateway Connection Pool Exhaustion")

    doc.add_heading("Summary", level=1)
    doc.add_paragraph(
        "On 2026-09-20 at 14:32 UTC, the payment gateway experienced connection pool "
        "exhaustion on pghost-prod-01.mfs.internal, causing payment processing failures "
        "for approximately 23 minutes. 847 transactions were affected."
    )

    doc.add_heading("Timeline", level=1)
    events = [
        "14:32 — PagerDuty alert: DB connection pool > 90% threshold",
        "14:35 — On-call (Arjun Deshmukh) acknowledged, began investigation",
        "14:38 — Identified connection leak in TokenizationService under concurrent load",
        "14:42 — Increased connection pool from 50 to 100 as temporary mitigation",
        "14:48 — Deployed hotfix to close connections in error path (MR !402)",
        "14:55 — Connection pool stabilized at 35% utilization",
        "15:00 — All payment processing resumed normally",
    ]
    for e in events:
        doc.add_paragraph(e, style="List Bullet")

    doc.add_heading("Root Cause", level=1)
    doc.add_paragraph(
        "The TokenizationService was not closing database connections in the error handler "
        "path when HSM timeout exceptions occurred. Under concurrent tokenization requests "
        "(peak: 450 req/s), leaked connections accumulated until the pool was exhausted."
    )

    doc.add_heading("Remediation", level=1)
    doc.add_paragraph("Immediate: Connection close in error handler (MR !402, PAY-901)", style="List Number")
    doc.add_paragraph("Short-term: Connection pool monitoring dashboard in Grafana", style="List Number")
    doc.add_paragraph("Long-term: Circuit breaker pattern for HSM calls (PAY-902)", style="List Number")

    path = OUT_DIR / "MFS-Incident-Postmortem-INC0080101.docx"
    doc.save(str(path))
    print(f"  Created {path.name}")


def create_service_inventory_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    wb = Workbook()
    ws = wb.active
    ws.title = "Service Inventory"

    header_fill = PatternFill(start_color="1A73E8", end_color="1A73E8", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    headers = ["Service", "Repository", "Service Account", "Pod(s)", "Database", "Owner Team", "SLO Availability", "SLO Latency P99"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    services = [
        ["mfs-payment-gateway", "mfs-payment-gateway", "svc-payment-api", "mfs-pay-pod-01, mfs-pay-pod-02", "mfs_payments_db (pghost-prod-01)", "Payment Services", "99.95%", "<200ms"],
        ["mfs-tokenization", "mfs-payment-gateway", "svc-token-vault", "mfs-pay-pod-01", "mfs_payments_db (pghost-prod-01)", "Payment Services", "99.99%", "<100ms"],
        ["mfs-webhook-api", "mfs-payment-gateway", "svc-webhook-dispatch", "mfs-pay-pod-01", "mfs_payments_db (pghost-prod-01)", "Payment Services", "99.5%", "<500ms"],
        ["mfs-analytics", "mfs-payment-gateway", "svc-analytics", "mfs-pay-pod-03", "mfs_payments_db (pghost-prod-01)", "Payment Services", "99.9%", "<1s"],
        ["mfs-settlement", "mfs-payment-gateway", "svc-payment-api", "mfs-pay-pod-03", "mfs_payments_db (pghost-prod-01)", "Payment Services", "99.9%", "<5s"],
        ["mfs-fraud-engine", "mfs-fraud-engine", "svc-fraud-engine", "mfs-fraud-pod-01, mfs-fraud-pod-02", "mfs_fraud_db (pghost-prod-02)", "Fraud & Risk", "99.99%", "<50ms"],
        ["mfs-txn-monitor", "mfs-fraud-engine", "svc-txn-monitor", "mfs-txn-mon-pod-01", "mfs_fraud_db (pghost-prod-02)", "Fraud & Risk", "99.9%", "<200ms"],
        ["mfs-aml-engine", "mfs-fraud-engine", "svc-aml-engine", "mfs-aml-pod-01", "mfs_aml_db (pghost-prod-02)", "Fraud & Risk", "99.9%", "<1s"],
        ["mfs-model-serving", "mfs-fraud-engine", "svc-model-serving", "mfs-model-pod-01", "mfs_fraud_db (pghost-prod-02)", "ML Engineering", "99.99%", "<50ms"],
        ["mfs-kyc-engine", "mfs-fraud-engine", "svc-kyc-engine", "mfs-kyc-pod-01", "mfs_customers_db (pghost-prod-03)", "Identity & Compliance", "99.9%", "<500ms"],
        ["mfs-case-engine", "mfs-fraud-engine", "svc-case-engine", "mfs-case-pod-01", "mfs_fraud_db (pghost-prod-02)", "Fraud Operations", "99.9%", "<200ms"],
        ["mfs-customer-portal", "mfs-customer-portal", "svc-portal", "mfs-portal-pod-01", "N/A (API gateway)", "Customer Experience", "99.95%", "<300ms"],
    ]
    for r, row_data in enumerate(services, 2):
        for c, val in enumerate(row_data, 1):
            ws.cell(row=r, column=c, value=val)

    for col in range(1, len(headers) + 1):
        ws.column_dimensions[chr(64 + col)].width = 22

    path = OUT_DIR / "MFS-Service-Inventory.xlsx"
    wb.save(str(path))
    print(f"  Created {path.name}")


def create_test_coverage_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    wb = Workbook()
    ws = wb.active
    ws.title = "Test Coverage Matrix"

    header_fill = PatternFill(start_color="34A853", end_color="34A853", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    headers = ["Feature", "Jira Key", "Unit Tests", "Integration Tests", "E2E Tests", "Overall Coverage", "Last Run", "Status"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    rows = [
        ["Payment Processing", "PAY-100", "94%", "87%", "72%", "84%", "2026-10-02", "PASS"],
        ["Tokenization", "PAY-101", "91%", "85%", "68%", "81%", "2026-10-02", "PASS"],
        ["Idempotency", "PAY-102", "88%", "82%", "65%", "78%", "2026-10-01", "PASS"],
        ["3DS Authentication", "PAY-103", "85%", "78%", "60%", "74%", "2026-10-01", "PASS"],
        ["Webhook Dispatch", "PAY-401", "76%", "62%", "45%", "61%", "2026-10-03", "PARTIAL"],
        ["Webhook Retry/DLQ", "PAY-402", "72%", "55%", "30%", "52%", "2026-10-03", "PARTIAL"],
        ["Analytics Aggregator", "PAY-501", "68%", "48%", "25%", "47%", "2026-10-03", "PARTIAL"],
        ["Settlement Reporting", "PAY-502", "45%", "30%", "0%", "25%", "2026-10-03", "IN PROGRESS"],
        ["Fraud Scoring", "FRD-101", "92%", "88%", "75%", "85%", "2026-10-02", "PASS"],
        ["Feature Extraction", "FRD-102", "89%", "82%", "70%", "80%", "2026-10-02", "PASS"],
        ["Velocity Monitor", "FRD-201", "87%", "80%", "65%", "77%", "2026-10-01", "PASS"],
        ["AML Rule Engine", "FRD-301", "82%", "72%", "55%", "70%", "2026-10-02", "PASS"],
        ["KYC Document OCR", "FRD-401", "65%", "45%", "20%", "43%", "2026-10-03", "IN PROGRESS"],
        ["Case Routing", "FRD-501", "60%", "40%", "15%", "38%", "2026-10-03", "IN PROGRESS"],
    ]
    for r, row_data in enumerate(rows, 2):
        for c, val in enumerate(row_data, 1):
            ws.cell(row=r, column=c, value=val)

    for col in range(1, len(headers) + 1):
        ws.column_dimensions[chr(64 + col)].width = 18

    path = OUT_DIR / "MFS-Test-Coverage-Matrix.xlsx"
    wb.save(str(path))
    print(f"  Created {path.name}")


def create_change_calendar_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    wb = Workbook()
    ws = wb.active
    ws.title = "Change Calendar"

    header_fill = PatternFill(start_color="FBBC04", end_color="FBBC04", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="000000")

    headers = ["Change ID", "Date", "Service", "Description", "Risk", "Status", "Owner"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font

    changes = [
        ["CHG0090101", "2026-09-20", "mfs-payment-gateway", "Deploy payment processing v2", "Low", "Closed", "Raj Patel"],
        ["CHG0090201", "2026-09-22", "mfs-payment-gateway", "Deploy tokenization HSM integration", "Moderate", "Closed", "Arjun Deshmukh"],
        ["CHG0090301", "2026-09-25", "mfs-payment-gateway", "Deploy idempotency key service", "Low", "Closed", "Alex Kim"],
        ["CHG0090401", "2026-09-27", "mfs-fraud-engine", "Deploy fraud scoring model v2", "Moderate", "Closed", "Raj Patel"],
        ["CHG0090501", "2026-09-29", "mfs-txn-monitor", "Deploy velocity monitor", "Moderate", "Closed", "Li Wei"],
        ["CHG0090601", "2026-10-02", "mfs-aml-engine", "Deploy AML rule engine v1", "High", "Authorized", "Raj Patel"],
        ["CHG0090701", "2026-10-05", "mfs-kyc-engine", "Deploy KYC document verification", "Moderate", "New", "Nadia Kowalski"],
        ["CHG0090801", "2026-10-07", "mfs-case-engine", "Deploy case management routing", "Low", "Assess", "David Okoye"],
    ]
    for r, row_data in enumerate(changes, 2):
        for c, val in enumerate(row_data, 1):
            ws.cell(row=r, column=c, value=val)

    for col in range(1, len(headers) + 1):
        ws.column_dimensions[chr(64 + col)].width = 22

    path = OUT_DIR / "MFS-Change-Calendar.xlsx"
    wb.save(str(path))
    print(f"  Created {path.name}")


def create_sprint_burndown_csv():
    path = OUT_DIR / "PAY-Sprint14-Burndown.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Day", "Date", "Planned Remaining", "Actual Remaining", "Ideal Burndown"])
        data = [
            [1, "2026-09-16", 55, 55, 55],
            [2, "2026-09-17", 55, 52, 50.4],
            [3, "2026-09-18", 55, 48, 45.8],
            [4, "2026-09-19", 55, 45, 41.3],
            [5, "2026-09-20", 55, 43, 36.7],
            [6, "2026-09-23", 55, 38, 32.1],
            [7, "2026-09-24", 55, 34, 27.5],
            [8, "2026-09-25", 55, 28, 22.9],
            [9, "2026-09-26", 55, 22, 18.3],
            [10, "2026-09-27", 55, 15, 13.8],
            [11, "2026-09-30", 55, 8, 9.2],
            [12, "2026-10-01", 55, 3, 4.6],
            [13, "2026-10-02", 55, 0, 0],
        ]
        for row in data:
            writer.writerow(row)
    print(f"  Created {path.name}")


def create_model_metrics_csv():
    path = OUT_DIR / "FRD-Model-Performance-Metrics.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Model Version", "Training Date", "AUC", "Precision", "Recall",
                          "F1 Score", "False Positive Rate", "Inference P99 (ms)", "Status"])
        data = [
            ["v1.8", "2026-01-15", 0.965, 0.938, 0.931, 0.934, "3.2%", 42, "Retired"],
            ["v1.9", "2026-03-20", 0.971, 0.945, 0.940, 0.942, "2.8%", 40, "Retired"],
            ["v2.0", "2026-05-10", 0.975, 0.952, 0.946, 0.949, "2.4%", 38, "Retired"],
            ["v2.1", "2026-07-15", 0.978, 0.955, 0.948, 0.951, "2.1%", 36, "Retired"],
            ["v2.2", "2026-08-20", 0.982, 0.961, 0.954, 0.957, "1.8%", 35, "Champion"],
            ["v2.3", "2026-09-25", 0.985, 0.948, 0.967, 0.957, "4.2%", 34, "Challenger (FP issue)"],
        ]
        for row in data:
            writer.writerow(row)
    print(f"  Created {path.name}")


def create_platform_overview_pptx():
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(2))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "MFS Platform Overview"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x73, 0xE8)
    p.alignment = PP_ALIGN.CENTER
    p = tf.add_paragraph()
    p.text = "Q4 2026 — Meridian Financial Services"
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(0x5F, 0x63, 0x68)
    p.alignment = PP_ALIGN.CENTER

    # Slide 2: Platform at a Glance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    title.text_frame.add_paragraph().text = "Platform at a Glance"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.bold = True
    metrics = [
        ("2.5M", "Daily Transactions"),
        ("99.95%", "Payment Gateway SLO"),
        ("35ms", "Fraud Score P99"),
        ("12", "Microservices"),
        ("18", "OpenShift Nodes"),
        ("3", "PostgreSQL Clusters"),
    ]
    for i, (val, label) in enumerate(metrics):
        col = i % 3
        row = i // 3
        x = Inches(1 + col * 4)
        y = Inches(1.5 + row * 2.5)
        box = slide.shapes.add_textbox(x, y, Inches(3), Inches(2))
        tf = box.text_frame
        p = tf.add_paragraph()
        p.text = val
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x1A, 0x73, 0xE8)
        p.alignment = PP_ALIGN.CENTER
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(16)
        p.alignment = PP_ALIGN.CENTER

    # Slide 3: Architecture Domains
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    title.text_frame.add_paragraph().text = "Architecture Domains"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.bold = True
    domains = [
        ("Payment Gateway (PAY)", "Transaction processing, tokenization,\nwebhook notifications, settlement,\nanalytics & reporting"),
        ("Fraud Detection (FRD)", "ML fraud scoring, velocity monitoring,\nanomaly detection, AML compliance,\nKYC verification, case management"),
        ("Shared Platform", "Common libraries, API gateway,\ncustomer portal, observability,\nCI/CD pipelines"),
    ]
    for i, (name, desc) in enumerate(domains):
        x = Inches(0.5 + i * 4.2)
        box = slide.shapes.add_textbox(x, Inches(1.8), Inches(3.8), Inches(4))
        tf = box.text_frame
        p = tf.add_paragraph()
        p.text = name
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x1A, 0x73, 0xE8)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(14)
        p.space_before = Pt(12)

    # Slide 4: Q4 Initiatives
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    title.text_frame.add_paragraph().text = "Q4 2026 Key Initiatives"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.bold = True
    initiatives = [
        "EPC-101: Payment Gateway v2 — Webhook notifications, analytics, settlement",
        "EPC-104: Merchant Integration Platform — Webhook API, analytics API",
        "EPC-201: Fraud Detection ML Platform — Model versioning, A/B testing",
        "EPC-202: Transaction Monitoring — Velocity checks, anomaly detection",
        "EPC-203: AML Compliance Engine — Pattern detection, SAR automation",
        "EPC-204: Identity Verification — KYC document verification, liveness detection",
    ]
    for i, text in enumerate(initiatives):
        box = slide.shapes.add_textbox(Inches(1), Inches(1.5 + i * 0.9), Inches(11), Inches(0.8))
        p = box.text_frame.add_paragraph()
        p.text = text
        p.font.size = Pt(16)

    # Slide 5: Risk & Compliance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    title.text_frame.add_paragraph().text = "Risk & Compliance Status"
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.text_frame.paragraphs[0].font.bold = True
    items = [
        "PCI DSS v4.0: 94% compliant (2 remediation items pending)",
        "SOX Controls: All financial reporting controls verified",
        "Service Accounts: 11 production accounts, all following least-privilege",
        "Secrets Rotation: 90-day policy enforced via Vault",
        "Open Incidents: 1 active (INC0080201 — ML model false positive spike)",
        "Open Problems: 2 (PRB0010001 — DB connection leaks, PRB0020001 — ML model drift)",
    ]
    for i, text in enumerate(items):
        box = slide.shapes.add_textbox(Inches(1), Inches(1.5 + i * 0.9), Inches(11), Inches(0.8))
        p = box.text_frame.add_paragraph()
        p.text = text
        p.font.size = Pt(16)

    path = OUT_DIR / "MFS-Platform-Overview-Q4-2026.pptx"
    prs.save(str(path))
    print(f"  Created {path.name}")


def create_release_review_pptx():
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(2))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "Payment Gateway v2 — Release Review"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x73, 0xE8)
    p.alignment = PP_ALIGN.CENTER
    p = tf.add_paragraph()
    p.text = "Sprint 26.14 Release Readiness Assessment"
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(0x5F, 0x63, 0x68)
    p.alignment = PP_ALIGN.CENTER

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    title.text_frame.add_paragraph().text = "Release Readiness Checklist"
    title.text_frame.paragraphs[0].font.size = Pt(28)
    title.text_frame.paragraphs[0].font.bold = True
    checks = [
        "[PASS] All unit tests passing (94% coverage)",
        "[PASS] Integration tests passing (87% coverage)",
        "[PASS] Security scan — no critical/high findings",
        "[PASS] Performance tests — p99 < 200ms",
        "[PARTIAL] E2E tests — webhook scenarios incomplete (72%)",
        "[PASS] Change approvals — CHG0090101 through CHG0090301",
        "[PASS] Rollback plan documented and tested",
        "[PASS] On-call team briefed (payments-oncall rotation)",
    ]
    for i, text in enumerate(checks):
        box = slide.shapes.add_textbox(Inches(1), Inches(1.3 + i * 0.7), Inches(11), Inches(0.6))
        p = box.text_frame.add_paragraph()
        p.text = text
        p.font.size = Pt(15)

    path = OUT_DIR / "MFS-Payment-Gateway-v2-Release-Review.pptx"
    prs.save(str(path))
    print(f"  Created {path.name}")


def create_deployment_checklist_txt():
    path = OUT_DIR / "deployment-checklist-PAY.txt"
    path.write_text("""\
============================================================
  MFS Payment Gateway — Deployment Checklist
  Meridian Financial Services
============================================================

PRE-DEPLOYMENT
--------------
[ ] Verify all CI/CD pipeline stages passed (lint, test, build, staging)
[ ] Confirm change approval in ServiceNow (CHG number: _________)
[ ] Verify rollback plan is documented and tested
[ ] Confirm on-call team is aware (payments-oncall PagerDuty rotation)
[ ] Verify database migrations are idempotent
[ ] Check Grafana dashboards for baseline metrics
[ ] Confirm Kibana log queries are ready for monitoring
[ ] Verify Vault secrets are rotated (if applicable)

DEPLOYMENT STEPS
-----------------
[ ] Scale down mfs-pay-pod-02 (secondary) first
[ ] Deploy new image to mfs-pay-pod-02
[ ] Verify health check passes on mfs-pay-pod-02
[ ] Run smoke tests against mfs-pay-pod-02
[ ] Scale down mfs-pay-pod-01 (primary)
[ ] Deploy new image to mfs-pay-pod-01
[ ] Verify health check passes on mfs-pay-pod-01
[ ] Deploy to mfs-pay-pod-03 (analytics/settlement) if applicable
[ ] Verify all pods are healthy in OpenShift console

POST-DEPLOYMENT
----------------
[ ] Monitor Grafana payment-gateway-slo dashboard for 30 minutes
[ ] Verify transaction success rate > 99.9%
[ ] Check Kibana for ERROR level logs in payment-logs-*
[ ] Verify webhook delivery success rate > 99.5%
[ ] Confirm Datadog monitors are green
[ ] Update ServiceNow change record to Closed
[ ] Send deployment notification to #mfs-releases Slack channel

ROLLBACK TRIGGERS
------------------
- Transaction success rate drops below 99%
- P99 latency exceeds 500ms for 5+ minutes
- Error rate exceeds 1% for 3+ minutes
- Database connection pool exceeds 80%
- Any P1 incident triggered

ROLLBACK PROCEDURE
-------------------
1. oc rollback mfs-payment-gateway -n mfs-payments (on ocp-prod-east)
2. Verify previous image is running on all pods
3. Run smoke tests against rolled-back pods
4. Update ServiceNow change to "Backed Out"
5. Create incident record for root cause analysis
""", encoding="utf-8")
    print(f"  Created {path.name}")


def create_runbook_txt():
    path = OUT_DIR / "runbook-fraud-engine-alerts.txt"
    path.write_text("""\
============================================================
  MFS Fraud Engine — Alert Runbook
  Meridian Financial Services
============================================================

ALERT: Fraud Score Latency P99 > 50ms
---------------------------------------
Severity: CRITICAL
Dashboard: grafana.mfs.internal/d/model-serving-slo
Steps:
  1. Check mfs-fraud-pod-01/02 CPU and memory utilization
  2. Verify ONNX Runtime health: curl mfs-fraud-pod-01:8080/health
  3. Check Kafka consumer lag on mfs.txn.features topic
  4. If CPU > 80%: scale up replicas (oc scale --replicas=4)
  5. If memory > 85%: restart pod (oc delete pod)
  6. If Kafka lag > 10000: check feature extraction pipeline
Escalation: Nadia Kowalski -> Sarah Chen -> VP Engineering

ALERT: False Positive Rate > 2%
---------------------------------
Severity: CRITICAL
Dashboard: grafana.mfs.internal/d/model-serving-slo
Steps:
  1. Check current model version in MLflow (mlflow.mfs.internal)
  2. Compare prediction score distribution vs baseline
  3. Check feature freshness in Feast feature store
  4. If model v2.3 is active: rollback to v2.2 champion
  5. Run model validation notebook for drift analysis
  6. Create INC ticket referencing FP rate metrics
Escalation: Nadia Kowalski -> Sarah Chen

ALERT: AML Rule Engine Downtime
---------------------------------
Severity: HIGH
Dashboard: grafana.mfs.internal/d/aml-monitoring
Steps:
  1. Check mfs-aml-pod-01 status in OpenShift
  2. Verify mfs_aml_db connectivity on pghost-prod-02
  3. Check svc-aml-engine service account validity
  4. Restart pod if health check failing
  5. If DB unreachable: engage DBA team
Escalation: Priya Sharma -> Sarah Chen

ALERT: Webhook DLQ Depth > 100
---------------------------------
Severity: WARNING
Dashboard: grafana.mfs.internal/d/webhook-delivery-slo
Steps:
  1. Check webhook_dlq table row count
  2. Identify top failing merchant endpoints
  3. Verify merchant webhook URLs are reachable
  4. If merchant side: notify merchant support team
  5. If MFS side: check svc-webhook-dispatch logs in Kibana
  6. Replay DLQ entries after root cause is fixed
""", encoding="utf-8")
    print(f"  Created {path.name}")


def create_audit_txt():
    path = OUT_DIR / "service-accounts-audit-Q3.txt"
    path.write_text("""\
============================================================
  MFS Service Account Audit — Q3 2026
  Meridian Financial Services
  Audit Date: 2026-09-30
  Auditor: Marcus Thompson (Platform Engineering)
============================================================

SUMMARY
--------
Total production service accounts: 11
Compliant: 9
Non-compliant: 2
Rotation overdue: 1

DETAILED FINDINGS
------------------

svc-payment-api
  Status: COMPLIANT
  Owner: Payment Services Team
  Last rotated: 2026-09-15
  Access: mfs_payments_db (read/write), mfs_audit_db (write)
  Pods: mfs-pay-pod-01, mfs-pay-pod-02, mfs-pay-pod-03

svc-token-vault
  Status: COMPLIANT
  Owner: Payment Services Team
  Last rotated: 2026-09-01
  Access: HSM gateway, Vault secrets
  Pods: mfs-pay-pod-01

svc-webhook-dispatch
  Status: COMPLIANT
  Owner: Payment Services Team
  Last rotated: 2026-09-20
  Access: Kafka mfs.payment.events, Vault webhook signing keys
  Pods: mfs-pay-pod-01

svc-analytics
  Status: COMPLIANT
  Owner: Payment Services Team
  Last rotated: 2026-09-10
  Access: mfs_payments_db (read-only)
  Pods: mfs-pay-pod-03

svc-fraud-engine
  Status: COMPLIANT
  Owner: Fraud & Risk Team
  Last rotated: 2026-08-25
  Access: mfs_fraud_db (read/write)
  Pods: mfs-fraud-pod-01, mfs-fraud-pod-02

svc-txn-monitor
  Status: COMPLIANT
  Owner: Fraud & Risk Team
  Last rotated: 2026-09-05
  Access: Kafka topics, mfs_fraud_db (read/write velocity_windows)
  Pods: mfs-txn-mon-pod-01

svc-aml-engine
  Status: NON-COMPLIANT (excessive access)
  Owner: Fraud & Risk Team
  Last rotated: 2026-09-12
  Access: mfs_aml_db (read/write), mfs_fraud_db (read) -- READ access
    to mfs_fraud_db not required per current architecture
  Remediation: Remove mfs_fraud_db read access by 2026-10-15
  Pods: mfs-aml-pod-01

svc-model-serving
  Status: NON-COMPLIANT (rotation overdue)
  Owner: ML Engineering Team
  Last rotated: 2026-06-20 (102 days ago, exceeds 90-day policy)
  Access: mfs_fraud_db.model_registry (read)
  Remediation: Rotate immediately, update Vault lease
  Pods: mfs-model-pod-01

svc-kyc-engine
  Status: COMPLIANT
  Owner: Identity & Compliance Team
  Last rotated: 2026-09-28
  Access: mfs_customers_db (read/write)
  Pods: mfs-kyc-pod-01

svc-case-engine
  Status: COMPLIANT
  Owner: Fraud Operations Team
  Last rotated: 2026-09-22
  Access: mfs_fraud_db (read/write fraud_cases, case_evidence)
  Pods: mfs-case-pod-01

svc-notification-svc
  Status: COMPLIANT
  Owner: Platform Team
  Last rotated: 2026-09-18
  Access: Email gateway, SMS gateway
  Pods: mfs-notification-pod-01

RECOMMENDATIONS
----------------
1. Rotate svc-model-serving credentials immediately
2. Remove mfs_fraud_db read access from svc-aml-engine
3. Implement automated rotation alerts in Vault
4. Schedule Q4 audit for 2026-12-31
""", encoding="utf-8")
    print(f"  Created {path.name}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_deps()

    print("Generating EOIP demo documents...")
    print()

    print("Word Documents (.docx):")
    create_architecture_doc()
    create_compliance_doc()
    create_fraud_architecture_doc()
    create_postmortem_doc()

    print("\nExcel Workbooks (.xlsx):")
    create_service_inventory_xlsx()
    create_test_coverage_xlsx()
    create_change_calendar_xlsx()

    print("\nCSV Files:")
    create_sprint_burndown_csv()
    create_model_metrics_csv()

    print("\nPowerPoint Presentations (.pptx):")
    create_platform_overview_pptx()
    create_release_review_pptx()

    print("\nText Files (.txt):")
    create_deployment_checklist_txt()
    create_runbook_txt()
    create_audit_txt()

    print(f"\nAll {len(list(OUT_DIR.iterdir()))} documents created in {OUT_DIR}")


if __name__ == "__main__":
    main()
