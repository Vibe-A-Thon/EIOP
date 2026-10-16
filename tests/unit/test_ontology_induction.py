import json
import pytest
from eoip.moonshot.ontology_induction import (
    CorpusOntologyInducer,
    EntityTypeProposal,
    InductionSHACLValidator,
    PropertyProposal,
    SHACLPropertyShape,
    SHACLShape,
    TypeConsolidationGuard,
)


class MockLLMProvider:
    def __init__(self, response_data: dict):
        self.response_data = response_data

    def generate(self, prompt: str, *, max_tokens: int = 2048, temperature: float = 0.1) -> str:
        return json.dumps(self.response_data)


@pytest.mark.req("KGR-G-015")
def test_ontology_induction_from_text():
    mock_schema = {
        "entity_types": [
            {
                "name": "Microservice",
                "description": "A standalone deployable service",
                "properties": [
                    {"name": "service_name", "data_type": "string", "required": True},
                    {"name": "port", "data_type": "integer", "required": False},
                ],
                "parent_type": None,
            }
        ],
        "relationship_types": [
            {
                "name": "CALLS_API",
                "source_type": "Microservice",
                "target_type": "Microservice",
                "description": "Synchronous HTTP/gRPC invocation",
                "cardinality": "many-to-many",
            }
        ],
    }
    llm = MockLLMProvider(mock_schema)
    inducer = CorpusOntologyInducer(llm)

    result = inducer.induce(["Service A communicates with Service B over port 8080."])
    assert len(result.entity_types) == 1
    assert result.entity_types[0].name == "Microservice"
    assert len(result.entity_types[0].properties) == 2

    assert len(result.relationship_types) == 1
    assert result.relationship_types[0].name == "CALLS_API"

    assert len(result.shacl_shapes) == 1
    shape = result.shacl_shapes[0]
    assert shape.target_class == "Microservice"
    turtle = shape.to_turtle()
    assert "sh:targetClass eoip:Microservice" in turtle
    assert "sh:path eoip:service_name" in turtle


@pytest.mark.req("KGR-G-015")
def test_ontology_induction_anti_drift_validation():
    baseline_shape = SHACLShape(
        target_class="Database",
        properties=[
            SHACLPropertyShape(path="db_name", datatype="string", min_count=1),
            SHACLPropertyShape(path="engine", datatype="string"),
        ],
    )
    validator = InductionSHACLValidator([baseline_shape])

    # Case 1: Proposed drops 'engine' -> drift violation
    drift_proposal = [
        EntityTypeProposal(
            name="Database",
            description="DB",
            properties=[PropertyProposal(name="db_name", data_type="string", description="")],
        )
    ]
    violations = validator.validate(drift_proposal)
    assert any("would remove baseline properties: {'engine'}" in v for v in violations)

    # Case 2: Proposed changes type of 'db_name' to integer -> drift violation
    type_drift_proposal = [
        EntityTypeProposal(
            name="Database",
            description="DB",
            properties=[
                PropertyProposal(name="db_name", data_type="integer", description=""),
                PropertyProposal(name="engine", data_type="string", description=""),
            ],
        )
    ]
    type_violations = validator.validate(type_drift_proposal)
    assert any("type changed from 'string' to 'integer'" in v for v in type_violations)

    # Case 3: Valid conforming proposal -> 0 violations
    valid_proposal = [
        EntityTypeProposal(
            name="Database",
            description="DB",
            properties=[
                PropertyProposal(name="db_name", data_type="string", description=""),
                PropertyProposal(name="engine", data_type="string", description=""),
                PropertyProposal(name="port", data_type="integer", description=""),
            ],
        )
    ]
    assert len(validator.validate(valid_proposal)) == 0


@pytest.mark.req("KGR-G-015")
def test_ontology_type_consolidation():
    proposals = [
        EntityTypeProposal(
            name="microservice",
            description="First desc",
            properties=[PropertyProposal(name="name", data_type="string", description="")],
            confidence=0.6,
            evidence_count=1,
        ),
        EntityTypeProposal(
            name="Microservice",
            description="Second desc",
            properties=[PropertyProposal(name="port", data_type="integer", description="")],
            confidence=0.8,
            evidence_count=2,
        ),
    ]
    consolidated = TypeConsolidationGuard.consolidate_entity_types(proposals)
    assert len(consolidated) == 1
    merged = consolidated[0]
    assert merged.name == "microservice"
    assert len(merged.properties) == 2
    assert merged.evidence_count == 3
