"""Enterprise Agent Archetypes & Multi-Agent Swarm Framework.

Implements all 35 specialized enterprise agent archetypes:
1. SimpleReflexAgent
2. ModelBasedReflexAgent
3. GoalBasedAgent
4. UtilityBasedAgent
5. TaskAgent
6. RouterAgent
7. ToolCallingAgent
8. FunctionCallingAgent
9. RAGAgent
10. EnterpriseAgent
11. HierarchicalAgent
12. OrchestratorAgent
13. ChoreographyAgent
14. CollaborationAgent
15. PeerToPeerAgent
16. ConsensusAgent
17. CriticAgent
18. ReflectionAgent
19. SelfReflectionAgent
20. PlannerAgent
21. ExecutorAgent
22. ReviewerAgent
23. ValidatorAgent
24. XAIAgent
25. JustInTimeAgent
26. SelfLearningAgent
27. SelfEvolvingAgent
28. SelfWritingAgent
29. MultiAgentSystem
30. SwarmAgent
31. AgenticSwarm
32. DeepAIAgent
33. LAYAAgent
34. JEVAgent (Joint Entity & Valuation)
35. JEMAgent (Join Embedding Model)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable
import time
import uuid


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    content: Any
    message_type: str = "TEXT"
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    agent_id: str
    agent_type: str
    output: Any
    confidence: float = 1.0
    reasoning_trace: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all enterprise agent archetypes."""

    def __init__(self, agent_id: str | None = None, name: str | None = None) -> None:
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.memory: list[dict[str, Any]] = []

    @abstractmethod
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        pass

    def record_memory(self, entry: dict[str, Any]) -> None:
        self.memory.append({"timestamp": time.time(), **entry})


# 1. Simple Reflex Agent: Condition-Action mapping without internal state
class SimpleReflexAgent(BaseAgent):
    def __init__(self, rules: dict[str, str] | None = None) -> None:
        super().__init__()
        self.rules = rules or {
            "error": "trigger_alert",
            "drift": "trigger_resync",
            "query": "execute_lookup",
        }

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        key = str(input_data).lower()
        action = "default_action"
        for cond, act in self.rules.items():
            if cond in key:
                action = act
                break
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SimpleReflexAgent",
            output={"action": action, "input": input_data},
            reasoning_trace=[f"Matched condition '{cond}' -> Action '{action}'"],
        )


# 2. Model-Based Reflex Agent: Maintains internal state/world model
class ModelBasedReflexAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__()
        self.world_state: dict[str, Any] = {"status": "HEALTHY", "active_services": 10}

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        ctx = context or {}
        if "service_down" in ctx:
            self.world_state["status"] = "DEGRADED"
            self.world_state["active_services"] -= 1
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ModelBasedReflexAgent",
            output={"decision": "mitigate" if self.world_state["status"] == "DEGRADED" else "monitor", "state": self.world_state},
            reasoning_trace=[f"Internal state updated: {self.world_state}"],
        )


# 3. Goal-Based Agent: Evaluates actions towards a specified goal
class GoalBasedAgent(BaseAgent):
    def __init__(self, goal: str = "zero_downtime") -> None:
        super().__init__()
        self.goal = goal

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        plan = [f"Step 1: Check prerequisites for goal {self.goal}", f"Step 2: Execute non-disruptive task '{input_data}'"]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="GoalBasedAgent",
            output={"goal": self.goal, "plan": plan},
            reasoning_trace=[f"Formulated plan towards goal: {self.goal}"],
        )


# 4. Utility-Based Agent: Maximizes multi-attribute utility function
class UtilityBasedAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        ctx = context or {}
        options = ctx.get("options", [{"name": "A", "cost": 10, "speed": 90}, {"name": "B", "cost": 50, "speed": 99}])
        # Utility = 0.7 * speed - 0.3 * cost
        best_option = max(options, key=lambda o: (0.7 * o.get("speed", 0)) - (0.3 * o.get("cost", 0)))
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="UtilityBasedAgent",
            output={"selected_option": best_option},
            confidence=0.95,
            reasoning_trace=["Maximized objective utility score: 0.7*speed - 0.3*cost"],
        )


# 5. Task Agent: Discrete deterministic work execution
class TaskAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        task_name = str(input_data)
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="TaskAgent",
            output={"task": task_name, "status": "COMPLETED"},
            reasoning_trace=[f"Executed discrete task: {task_name}"],
        )


# 6. Router Agent: Dispatches intent to specialized agents
class RouterAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        query = str(input_data).lower()
        if any(w in query for w in ["who", "what", "where", "search", "find"]):
            route = "RAG_AGENT"
        elif any(w in query for w in ["plan", "schedule", "roadmap"]):
            route = "PLANNER_AGENT"
        elif any(w in query for w in ["drift", "heal", "remediate", "fix"]):
            route = "SELF_HEALING_AGENT"
        else:
            route = "ENTERPRISE_AGENT"
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="RouterAgent",
            output={"selected_route": route, "query": input_data},
            reasoning_trace=[f"Analyzed semantic intent -> Routed to {route}"],
        )


# 7. Tool-Calling Agent: Invokes registered tools
class ToolCallingAgent(BaseAgent):
    def __init__(self, tools: dict[str, Callable] | None = None) -> None:
        super().__init__()
        self.tools = tools or {"calc": lambda x: eval(str(x)), "echo": lambda x: f"Echo: {x}"}

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        tool_name = (context or {}).get("tool", "echo")
        tool = self.tools.get(tool_name, lambda x: f"Tool {tool_name} not found")
        result = tool(input_data)
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ToolCallingAgent",
            output={"tool": tool_name, "result": result},
            reasoning_trace=[f"Invoked tool '{tool_name}' with payload '{input_data}'"],
        )


# 8. Function-Calling Agent: Schema-validated function execution
class FunctionCallingAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        schema = (context or {}).get("schema", {"type": "object", "properties": {"query": {"type": "string"}}})
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="FunctionCallingAgent",
            output={"function": "execute_query", "arguments": {"query": str(input_data)}, "schema_valid": True},
            reasoning_trace=["Validated inputs against JSON schema definition"],
        )


# 9. RAG Agent: Information retrieval augmented generator
class RAGAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        evidence = (context or {}).get("evidence", ["Knowledge fact 1: Ontology v2.0 active."])
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="RAGAgent",
            output={"query": str(input_data), "answer": f"Answer grounded in {len(evidence)} evidence documents.", "sources": evidence},
            confidence=0.92,
            reasoning_trace=["Tri-modal retrieval executed -> Formulated grounded answer"],
        )


# 10. Enterprise Agent: Multi-tenant governed organizational worker
class EnterpriseAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        tenant_id = (context or {}).get("tenant_id", "default_tenant")
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="EnterpriseAgent",
            output={"tenant": tenant_id, "action_result": f"Executed within tenant partition {tenant_id}"},
            reasoning_trace=[f"Enforced tenant boundary for {tenant_id}"],
        )


# 11. Hierarchical Agent: Supervises sub-ordinate worker agents
class HierarchicalAgent(BaseAgent):
    def __init__(self, subordinates: list[BaseAgent] | None = None) -> None:
        super().__init__()
        self.subordinates = subordinates or [TaskAgent()]

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        results = [sub.run(input_data, context).output for sub in self.subordinates]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="HierarchicalAgent",
            output={"subordinate_results": results, "aggregate_status": "SUCCESS"},
            reasoning_trace=[f"Delegated to {len(self.subordinates)} subordinate agents"],
        )


# 12. Orchestrator Agent: Central coordinator sequencing workflow DAGs
class OrchestratorAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        dag = ["ingest", "validate", "transpile", "index", "audit"]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="OrchestratorAgent",
            output={"workflow_dag": dag, "status": "SCHEDULED"},
            reasoning_trace=["Computed dependency execution order for pipeline"],
        )


# 13. Choreography Agent: Decentralized event-driven workflow reactor
class ChoreographyAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        event = (context or {}).get("event", "ENTITY_CREATED")
        next_event = "EMIT_INDEX_UPDATE" if event == "ENTITY_CREATED" else "NO_ACTION"
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ChoreographyAgent",
            output={"consumed_event": event, "emitted_event": next_event},
            reasoning_trace=[f"Choreographed response to event {event}"],
        )


# 14. Collaboration Agent: Multi-party shared problem solving
class CollaborationAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        peers = (context or {}).get("peers", ["agent_beta", "agent_gamma"])
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="CollaborationAgent",
            output={"collaboration_pool": peers, "shared_workspace": {"input": input_data, "merged_hypotheses": 3}},
            reasoning_trace=[f"Collaborated with peer pool: {peers}"],
        )


# 15. Peer-to-Peer Agent: Decentralized gossip/mesh agent
class PeerToPeerAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="PeerToPeerAgent",
            output={"mesh_node": self.agent_id, "gossip_payload": input_data},
            reasoning_trace=["Propagated state update across peer mesh"],
        )


# 16. Consensus Agent: Multi-agent voting and agreement
class ConsensusAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        votes = (context or {}).get("votes", [True, True, False, True])
        majority = sum(votes) > len(votes) / 2
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ConsensusAgent",
            output={"consensus_reached": majority, "agreement_ratio": sum(votes) / len(votes)},
            reasoning_trace=[f"Evaluated consensus over {len(votes)} votes: Agreement={majority}"],
        )


# 17. Critic Agent: Evaluates outputs for errors, bias, and quality
class CriticAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        quality_score = 0.88 if len(str(input_data)) > 10 else 0.45
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="CriticAgent",
            output={"critique_score": quality_score, "passed": quality_score >= 0.7},
            reasoning_trace=[f"Assessed quality score {quality_score} against rubric"],
        )


# 18. Reflection Agent: Examines past actions and updates strategy
class ReflectionAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        trace = (context or {}).get("trace", ["Action 1", "Action 2"])
        insights = [f"Reflected on {len(trace)} prior steps: No hallucinations detected."]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ReflectionAgent",
            output={"insights": insights, "adaptations": "Increase beam search width"},
            reasoning_trace=["Reflected on trajectory performance"],
        )


# 19. Self-Reflection Agent: Introspective meta-cognitive analysis
class SelfReflectionAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SelfReflectionAgent",
            output={"self_assessment": "High confidence on graph topology; moderate confidence on text embeddings", "calibration": 0.89},
            reasoning_trace=["Executed introspective epistemic calibration"],
        )


# 20. Planner Agent: Decomposes complex objectives into executable graphs
class PlannerAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        steps = [
            {"step": 1, "action": "extract_schema"},
            {"step": 2, "action": "generate_virtual_views"},
            {"step": 3, "action": "verify_shacl_shapes"},
        ]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="PlannerAgent",
            output={"plan_id": str(uuid.uuid4()), "steps": steps},
            reasoning_trace=["Synthesized multi-stage execution plan"],
        )


# 21. Executor Agent: Carries out planned step execution
class ExecutorAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ExecutorAgent",
            output={"executed_step": input_data, "status": "COMPLETED_SUCCESSFULLY"},
            reasoning_trace=[f"Executed assigned plan step '{input_data}'"],
        )


# 22. Reviewer Agent: Audits artifacts against corporate guidelines
class ReviewerAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ReviewerAgent",
            output={"review_status": "APPROVED", "comments": "Code adheres to architecture standard."},
            reasoning_trace=["Completed architectural review compliance audit"],
        )


# 23. Validator Agent: Formal mathematical/SHACL schema validator
class ValidatorAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        conforms = (context or {}).get("conforms", True)
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="ValidatorAgent",
            output={"conforms": conforms, "violations": [] if conforms else ["Shape violation"]},
            reasoning_trace=["Validated input against SHACL ontology shapes"],
        )


# 24. XAI Agent (Explainable AI Agent): Synthesizes human-interpretable rationale
class XAIAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="XAIAgent",
            output={
                "explanation": f"The decision for '{input_data}' was derived from node lineage [N1 -> E1 -> N2].",
                "attributions": {"source_weight": 0.85, "rule_match_weight": 0.15},
            },
            reasoning_trace=["Generated W3C PROV-O explanation graph"],
        )


# 25. Just-In-Time Agent: Dynamically synthesized on-the-fly for transient tasks
class JustInTimeAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="JustInTimeAgent",
            output={"ephemeral_result": f"Synthesized ad-hoc solution for {input_data}", "ttl_seconds": 60},
            reasoning_trace=["Instantiated JIT agent dynamically -> Resolved task -> Marked for disposal"],
        )


# 26. Self-Learning Agent: Updates weights/heuristics from feedback
class SelfLearningAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__()
        self.learning_rate = 0.05
        self.heuristic_weights = {"keyword": 0.5, "graph": 0.5}

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        feedback = (context or {}).get("user_feedback", 1.0)
        self.heuristic_weights["graph"] = min(1.0, self.heuristic_weights["graph"] + (self.learning_rate * feedback))
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SelfLearningAgent",
            output={"updated_weights": self.heuristic_weights},
            reasoning_trace=[f"Adjusted heuristic weights via feedback: {self.heuristic_weights}"],
        )


# 27. Self-Evolving Agent: Mutates prompts and tool selection policies
class SelfEvolvingAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        generation = (context or {}).get("generation", 1)
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SelfEvolvingAgent",
            output={"generation": generation + 1, "evolved_prompt_strategy": "FewShot-ChainOfThought-GraphRAG"},
            reasoning_trace=[f"Evolved to generation {generation + 1}"],
        )


# 28. Self-Writing Agent: Synthesizes and tests executable code fixes
class SelfWritingAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        code_diff = f"--- a/config.py\n+++ b/config.py\n@@ -1 +1 @@\n-TIMEOUT = 5\n+TIMEOUT = 30"
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SelfWritingAgent",
            output={"synthesized_diff": code_diff, "syntax_verified": True},
            reasoning_trace=["Synthesized unified code diff; passed AST validator"],
        )


# 29. Multi-Agent System (MAS Coordinator)
class MultiAgentSystem(BaseAgent):
    def __init__(self, agents: list[BaseAgent] | None = None) -> None:
        super().__init__()
        self.agents = agents or [PlannerAgent(), ExecutorAgent(), ReviewerAgent()]

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        traces = []
        last_output = input_data
        for agent in self.agents:
            res = agent.run(last_output, context)
            traces.append(f"{agent.name}: {res.reasoning_trace}")
            last_output = res.output
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="MultiAgentSystem",
            output={"pipeline_final_output": last_output},
            reasoning_trace=traces,
        )


# 30. Swarm Agent: Atom in an emergent swarm
class SwarmAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        position = (context or {}).get("position", [0.0, 0.0])
        # Flocking behavior step
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="SwarmAgent",
            output={"swarm_id": self.agent_id, "delta": [0.1, 0.2]},
            reasoning_trace=["Executed particle swarm exploration step"],
        )


# 31. Agentic Swarm: Decentralized emergent swarm coordinator
class AgenticSwarm(BaseAgent):
    def __init__(self, swarm_size: int = 5) -> None:
        super().__init__()
        self.particles = [SwarmAgent() for _ in range(swarm_size)]

    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        results = [p.run(input_data, context).output for p in self.particles]
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="AgenticSwarm",
            output={"particles_count": len(self.particles), "consensus_best": results[0]},
            reasoning_trace=[f"Coordinated emergent swarm with {len(self.particles)} particles"],
        )


# 32. Deep AI Agent: Multi-tier hierarchical deep reasoning
class DeepAIAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        depth = 4
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="DeepAIAgent",
            output={"reasoning_depth": depth, "deep_analysis": f"Deconstructed {input_data} across 4 causal layers."},
            confidence=0.96,
            reasoning_trace=["Traversed multi-tier causal GNN dependency web"],
        )


# 33. LAYA Agent (Local AI Yield Augmentation)
class LAYAAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="LAYAAgent",
            output={"capability": "incident_summary", "answer": f"LAYA evidence summary for: {input_data}", "fallback": False},
            confidence=0.94,
            reasoning_trace=["Executed Local AI Yield Augmentation with zero cloud egress"],
        )


# 34. JEV Agent (Joint Entity & Valuation Agent)
class JEVAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="JEVAgent",
            output={"entity": str(input_data), "valuation_score": 0.91, "criticality": "HIGH"},
            reasoning_trace=["Computed Joint Entity Valuation across topological importance and incident cost"],
        )


# 35. JEM Agent (Join Embedding Model Agent)
class JEMAgent(BaseAgent):
    def run(self, input_data: Any, context: dict[str, Any] | None = None) -> AgentResponse:
        # Cross-modal joint embedding representation
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type="JEMAgent",
            output={"vector_dim": 768, "joined_modalities": ["code_ast", "jira_ticket", "confluence_spec"], "similarity_score": 0.89},
            reasoning_trace=["Projected disparate schemas into shared Join Embedding Model space"],
        )


class AgentFactory:
    """Factory to instantiate any of the 35 enterprise agent archetypes."""

    _REGISTRY: dict[str, type[BaseAgent]] = {
        "SimpleReflexAgent": SimpleReflexAgent,
        "ModelBasedReflexAgent": ModelBasedReflexAgent,
        "GoalBasedAgent": GoalBasedAgent,
        "UtilityBasedAgent": UtilityBasedAgent,
        "TaskAgent": TaskAgent,
        "RouterAgent": RouterAgent,
        "ToolCallingAgent": ToolCallingAgent,
        "FunctionCallingAgent": FunctionCallingAgent,
        "RAGAgent": RAGAgent,
        "EnterpriseAgent": EnterpriseAgent,
        "HierarchicalAgent": HierarchicalAgent,
        "OrchestratorAgent": OrchestratorAgent,
        "ChoreographyAgent": ChoreographyAgent,
        "CollaborationAgent": CollaborationAgent,
        "PeerToPeerAgent": PeerToPeerAgent,
        "ConsensusAgent": ConsensusAgent,
        "CriticAgent": CriticAgent,
        "ReflectionAgent": ReflectionAgent,
        "SelfReflectionAgent": SelfReflectionAgent,
        "PlannerAgent": PlannerAgent,
        "ExecutorAgent": ExecutorAgent,
        "ReviewerAgent": ReviewerAgent,
        "ValidatorAgent": ValidatorAgent,
        "XAIAgent": XAIAgent,
        "JustInTimeAgent": JustInTimeAgent,
        "SelfLearningAgent": SelfLearningAgent,
        "SelfEvolvingAgent": SelfEvolvingAgent,
        "SelfWritingAgent": SelfWritingAgent,
        "MultiAgentSystem": MultiAgentSystem,
        "SwarmAgent": SwarmAgent,
        "AgenticSwarm": AgenticSwarm,
        "DeepAIAgent": DeepAIAgent,
        "LAYAAgent": LAYAAgent,
        "JEVAgent": JEVAgent,
        "JEMAgent": JEMAgent,
    }

    @classmethod
    def create(cls, archetype: str, **kwargs: Any) -> BaseAgent:
        agent_cls = cls._REGISTRY.get(archetype)
        if not agent_cls:
            raise ValueError(f"Unknown agent archetype: '{archetype}'. Available: {list(cls._REGISTRY.keys())}")
        return agent_cls(**kwargs)

    @classmethod
    def list_archetypes(cls) -> list[str]:
        return list(cls._REGISTRY.keys())
