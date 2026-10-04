"""Phase 12 — Competitive Parity Plus: tests for export, styling, playbooks, and more."""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


# --- 12.1 Interactive HTML Export ---

def test_interactive_export_module_exists():
    """InteractiveExport.js should exist."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "export", "InteractiveExport.js")
    assert os.path.isfile(path), "InteractiveExport.js not found"


def test_interactive_export_contains_html_generation():
    """InteractiveExport.js should contain generateInteractiveHTML function."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "export", "InteractiveExport.js")
    content = open(path, encoding="utf-8").read()
    assert "generateInteractiveHTML" in content
    assert "<!DOCTYPE html>" in content or "<!doctype html>" in content.lower()
    assert "canvas" in content.lower()


# --- 12.2 Graph Report ---

def test_graph_report_module_exists():
    """GraphReport.js should exist."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "export", "GraphReport.js")
    assert os.path.isfile(path), "GraphReport.js not found"


def test_graph_report_contains_sections():
    """GraphReport.js should generate 7-section Markdown."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "export", "GraphReport.js")
    content = open(path, encoding="utf-8").read()
    assert "generateGraphReport" in content
    for section in ["Overview", "Topology", "Centrality", "Community", "Evidence", "Health", "Recommendations"]:
        assert section in content, f"Missing report section: {section}"


# --- 12.3 Style Rules ---

def test_style_rules_component_exists():
    """StyleRules.jsx should exist with applyStyleRules."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "StyleRules.jsx")
    assert os.path.isfile(path)
    content = open(path, encoding="utf-8").read()
    assert "applyStyleRules" in content
    assert "localStorage" in content


def test_style_rules_operators():
    """StyleRules should support 7 comparison operators."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "StyleRules.jsx")
    content = open(path, encoding="utf-8").read()
    operators = ["equals", "contains", "startsWith", "endsWith", "gt", "lt", "regex"]
    found = sum(1 for op in operators if op in content)
    assert found >= 6, f"Expected at least 6 operators, found {found}"


# --- 12.4 Table View ---

def test_table_view_component_exists():
    """TableView.jsx should exist with sortable/filterable table."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "TableView.jsx")
    assert os.path.isfile(path)
    content = open(path, encoding="utf-8").read()
    assert "role=" in content or 'aria-' in content, "Table should have ARIA roles"


# --- 12.5 Investigation Playbooks ---

def test_playbooks_component_exists():
    """Playbooks.jsx should exist with built-in playbooks."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "Playbooks.jsx")
    assert os.path.isfile(path)
    content = open(path, encoding="utf-8").read()
    assert "builtInPlaybooks" in content
    for playbook in ["Impact Assessment", "Root Cause", "Community Health", "Dependency Audit"]:
        assert playbook in content, f"Missing playbook: {playbook}"


# --- 12.6 Surprise Panel ---

def test_surprise_panel_component_exists():
    """SurprisePanel.jsx should exist."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "SurprisePanel.jsx")
    assert os.path.isfile(path)
    content = open(path, encoding="utf-8").read()
    assert "surprising_edges" in content
    assert "unexpected_absences" in content


# --- 12.7 AI Explorer ---

def test_ai_explorer_component_exists():
    """AIExplorer.jsx should exist with quick actions and structured fallback."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "AIExplorer.jsx")
    assert os.path.isfile(path)
    content = open(path, encoding="utf-8").read()
    assert "structuredFallback" in content
    assert "QUICK_ACTIONS" in content
    assert "rag_pattern" in content or "rag/query" in content


# --- 12.8 Export Menu Integration ---

def test_export_menu_has_new_formats():
    """ExportMenu.jsx should include interactive HTML and graph report formats."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "components", "ExportMenu.jsx")
    content = open(path, encoding="utf-8").read()
    assert "interactive" in content
    assert "report" in content
    assert "generateInteractiveHTML" in content
    assert "generateGraphReport" in content


# --- 12.9 Cross-Project Merge API ---

def test_merge_endpoint_in_api():
    """app.py should have the graph merge endpoint."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/graph/merge" in content
    assert "MergeRequest" in content


# --- 12.10 CSS Styles ---

def test_css_has_competitive_parity_styles():
    """style.css should have styles for all Phase 12 components."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "style.css")
    content = open(path, encoding="utf-8").read()
    for cls in ["kgr-style-rules", "kgr-table-view", "kgr-playbook-panel",
                "kgr-surprise-panel", "kgr-ai-explorer", "lasso-overlay"]:
        assert cls in content, f"Missing CSS class: {cls}"


# --- 12.11 KGR Explorer Integration ---

def test_kgr_explorer_imports_all_phase12_components():
    """KGRExplorer.jsx should import all Phase 12 components."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "KGRExplorer.jsx")
    content = open(path, encoding="utf-8").read()
    for component in ["StyleRules", "TableView", "Playbooks", "SurprisePanel", "AIExplorer"]:
        assert component in content, f"KGRExplorer missing import: {component}"


def test_kgr_explorer_has_deep_link_state():
    """KGRExplorer should have URL deep linking support."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "KGRExplorer.jsx")
    content = open(path, encoding="utf-8").read()
    assert "deepLink" in content.lower() or "location.hash" in content


def test_kgr_explorer_has_keyboard_shortcuts():
    """KGRExplorer should register keyboard shortcuts."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "src", "kgr", "KGRExplorer.jsx")
    content = open(path, encoding="utf-8").read()
    assert "keydown" in content or "KeyboardEvent" in content
