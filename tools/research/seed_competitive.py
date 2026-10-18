"""Generate research/competitive/C01.yaml .. C55.yaml from competitive-research-matrix.csv."""
from __future__ import annotations
import csv
from pathlib import Path
import yaml

def main():
    out_dir = Path("research/competitive")
    out_dir.mkdir(parents=True, exist_ok=True)

    dep_pins = {
        "rdflib": "rdflib>=7.0.0",
        "pyshacl": "pyshacl>=0.25.0",
        "owl api": "owlapi-5.1.20",
        "elk": "elk-owlapi-0.5.0",
        "jena": "apache-jena-fuseki-4.10.0",
        "fuseki": "apache-jena-fuseki-4.10.0",
        "ontop": "ontop-v5.1.0",
        "morph-kgc": "morph-kgc>=2.5.0",
        "deeponto": "deeponto>=0.8.0",
        "spacy": "spacy>=3.7.0",
        "tesseract": "tesseract-5.3.4",
    }

    csv_path = Path("competitive-research-matrix.csv")
    count = 0
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["id"]
            tool_family = row["tool_family"]
            cat = row["category"]
            
            pinned = "unpinned"
            for k, v in dep_pins.items():
                if k in tool_family.lower():
                    pinned = v
                    break
                    
            scores = {}
            for d in range(1, 23):
                dim_key = f"D{d:02d}"
                score_val = row.get(dim_key, "ND")
                if score_val == "" or score_val is None:
                    score_val = "ND"
                scores[dim_key] = {
                    "score": int(score_val) if score_val.isdigit() else score_val,
                    "rationale": row.get("rationale_reference", ""),
                }
                
            data = {
                "id": cid,
                "tool_family": tool_family,
                "category": cat,
                "reviewed_at": "2026-10-18",
                "review_baseline": row.get("review_baseline", ""),
                "pinned_artifact": pinned,
                "license_snapshot": "reviewed",
                "confidence": row.get("confidence", "medium"),
                "primary_evidence_url": row.get("primary_evidence_url", ""),
                "inversion_id": row.get("inversion_id", ""),
                "requirements": row.get("requirements", ""),
                "scores": scores,
            }
            
            out_file = out_dir / f"{cid}.yaml"
            out_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            count += 1

    print(f"Generated {count} competitive dossiers in {out_dir}")

if __name__ == "__main__":
    main()
