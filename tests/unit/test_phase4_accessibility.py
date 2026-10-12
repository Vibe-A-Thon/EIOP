"""Unit Tests for Accessibility Scanner (TEST-005)."""

import pytest

from eoip.testing.a11y_scanner import (
    AccessibilityScanner,
    WCAGRule,
)


class TestAccessibilityScanner:
    def test_compliant_html_snippet(self):
        scanner = AccessibilityScanner()
        html = """
        <main>
            <h1>Knowledge Graph Dashboard</h1>
            <img src="/logo.svg" alt="EOIP Logo" />
            <button aria-label="Run Traversal">Search</button>
            <input type="text" id="query_input" aria-label="Graph Cypher Query" />
        </main>
        """
        report = scanner.audit_html(html)
        assert report.conforms is True
        assert len(report.violations) == 0

    def test_missing_img_alt_violation(self):
        scanner = AccessibilityScanner()
        html = '<img src="/chart.png" />'
        report = scanner.audit_html(html)
        assert report.conforms is False
        assert any(v.rule == WCAGRule.SC_1_1_1_NON_TEXT for v in report.violations)

    def test_empty_button_without_aria_label(self):
        scanner = AccessibilityScanner()
        html = '<button class="icon-btn"></button>'
        report = scanner.audit_html(html)
        assert report.conforms is False
        assert any(v.rule == WCAGRule.SC_4_1_2_NAME_ROLE_VALUE for v in report.violations)

    def test_unlabeled_input(self):
        scanner = AccessibilityScanner()
        html = '<input type="text" name="secret_param" />'
        report = scanner.audit_html(html)
        assert report.conforms is False
        assert any(v.rule == WCAGRule.SC_1_3_1_INFO_RELATIONSHIPS for v in report.violations)

    def test_contrast_ratio_calculation(self):
        scanner = AccessibilityScanner()
        # Black on White: ~21:1
        ratio = scanner.calculate_contrast_ratio("#000000", "#ffffff")
        assert ratio >= 20.0

        # WCAG AA requires at least 4.5:1 for normal text
        # Dark navy (#0a192f) on white (#ffffff)
        navy_ratio = scanner.calculate_contrast_ratio("#0a192f", "#ffffff")
        assert navy_ratio >= 4.5
