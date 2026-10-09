"""Machine-readable language taxonomy (gap analysis §5.3 correction).

The §5.3 correction requires that RDF-family and metadata *representation*
standards are classified as **Knowledge Representation**, NOT query languages.
This module is the single machine-readable source of truth for that
classification so registries, docs, and validators stay consistent.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Classification(str, Enum):
    QUERY_LANGUAGE = "Query Language"
    KNOWLEDGE_REPRESENTATION = "Knowledge Representation"
    TEMPLATE_LANGUAGE = "Template Language"


class LanguageRecord(BaseModel):
    id: str
    name: str
    classification: Classification
    family: str
    standard: str = Field(default="", description="governing standard / spec, if any")
    note: str = Field(default="")


# Semantic / representation standards — NOT query languages (§5.3 fix).
KNOWLEDGE_REPRESENTATION_STANDARDS: dict[str, LanguageRecord] = {
    rec.id: rec
    for rec in [
        LanguageRecord(id="rdf", name="RDF", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="RDF", standard="W3C RDF 1.1 Concepts",
                       note="Resource Description Framework data model — representation, not a query language."),
        LanguageRecord(id="rdfs", name="RDFS", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="RDF", standard="W3C RDF Schema 1.1",
                       note="RDF vocabulary description language (schema), not a query language."),
        LanguageRecord(id="owl", name="OWL", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Ontology", standard="W3C OWL 2",
                       note="Web Ontology Language — ontology axiomatization, not a query language."),
        LanguageRecord(id="skos", name="SKOS", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Vocabulary", standard="W3C SKOS Reference",
                       note="Simple Knowledge Organization System — thesaurus model."),
        LanguageRecord(id="shacl", name="SHACL", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Validation", standard="W3C SHACL",
                       note="Shapes Constraint Language — validation, not querying."),
        LanguageRecord(id="rdf_star", name="RDF-star", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="RDF", standard="W3C RDF-star CG",
                       note="RDF quoted-triples extension — data model."),
        LanguageRecord(id="json_ld", name="JSON-LD", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C JSON-LD 1.1",
                       note="JSON-based RDF serialization syntax."),
        LanguageRecord(id="turtle", name="Turtle", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C RDF 1.1 Turtle",
                       note="RDF serialization syntax."),
        LanguageRecord(id="trig", name="TriG", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C RDF 1.1 TriG",
                       note="RDF dataset serialization syntax."),
        LanguageRecord(id="n_triples", name="N-Triples", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C RDF 1.1 N-Triples",
                       note="Line-based RDF serialization syntax."),
        LanguageRecord(id="n_quads", name="N-Quads", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C RDF 1.1 N-Quads",
                       note="Line-based RDF dataset serialization syntax."),
        LanguageRecord(id="rdf_xml", name="RDF/XML", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Serialization", standard="W3C RDF 1.1 XML Syntax",
                       note="XML serialization syntax for RDF."),
        LanguageRecord(id="prov_o", name="PROV-O", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Provenance", standard="W3C PROV-O",
                       note="Provenance ontology — domain vocabulary."),
        LanguageRecord(id="dc", name="DC (Dublin Core)", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Metadata", standard="ISO 15836 / DCMI",
                       note="Dublin Core metadata vocabulary."),
        LanguageRecord(id="dublin_core_terms", name="Dublin Core Terms", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Metadata", standard="DCMI Metadata Terms",
                       note="Dublin Core refinements vocabulary."),
        LanguageRecord(id="owl_time", name="OWL-Time", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Ontology", standard="W3C OWL-Time",
                       note="Temporal ontology vocabulary."),
        LanguageRecord(id="sosa", name="SOSA", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Ontology", standard="W3C SOSA",
                       note="Sensor, Observation, Sample, and Actuator vocabulary."),
        LanguageRecord(id="ssn", name="SSN", classification=Classification.KNOWLEDGE_REPRESENTATION,
                       family="Ontology", standard="W3C SSN",
                       note="Semantic Sensor Network ontology."),
    ]
}

# Things that ARE query languages — used by the honesty check that KR records
# never appear in a query-language registry.
QUERY_LANGUAGE_IDS: frozenset[str] = frozenset(
    {
        "sparql", "sparql_update", "sparql_federated", "sparql_star", "geosparql",
        "graphql", "gremlin", "gremlin_dsl", "opencypher", "gql", "gsql", "ngql",
        "typeql", "aql", "pgql", "sqlpgq", "dql", "datalog", "sql",
        "sql_recursive_cte", "jsonpath", "jq", "jq_full", "xpath", "xquery",
        "lucene", "kql_kibana", "kql_kusto", "promql", "logql", "flux",
        "es_dsl", "mongo_aggregation", "surrealql", "sqlpp", "eoql", "osql", "eql",
    }
)


def is_query_language(language_id: str) -> bool:
    return language_id in QUERY_LANGUAGE_IDS


def classification_of(language_id: str) -> Classification | None:
    rec = KNOWLEDGE_REPRESENTATION_STANDARDS.get(language_id)
    if rec is not None:
        return rec.classification
    if language_id in QUERY_LANGUAGE_IDS:
        return Classification.QUERY_LANGUAGE
    return None


def assert_taxonomy_honesty() -> list[str]:
    """Return violations: any KR standard masquerading as a query language."""
    violations = []
    for rec_id, rec in KNOWLEDGE_REPRESENTATION_STANDARDS.items():
        if rec.classification == Classification.QUERY_LANGUAGE:
            violations.append(f"{rec_id} misclassified as query language")
        if rec_id in QUERY_LANGUAGE_IDS:
            violations.append(f"{rec_id} present in both KR standards and query languages")
    return violations
