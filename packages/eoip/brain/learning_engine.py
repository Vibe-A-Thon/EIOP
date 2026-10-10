"""Enterprise Cognitive Learning Engine & Adaptive AI Paradigms.

Implements core machine learning and reinforcement learning paradigms:
1. Q-Learning & Reinforcement Learning (RL query policy optimization)
2. Imitation Learning / Behavioral Cloning (Human expert trajectory cloning)
3. Supervised Exemplar Learning (Few-shot demonstration store)
4. Unsupervised Learning (Graph clustering & spectral concept grouping)
5. Semi-Supervised Learning (Label propagation across knowledge graphs)
6. Self-Supervised Learning (Masked entity link & relationship prediction)
7. Adaptive, Self-Learning, Self-Evolving, and Self-Writing Agent Harness
"""

from __future__ import annotations

import enum
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from eoip.models.self_llm import TensorMath, get_self_llm_engine


class LearningParadigm(str, enum.Enum):
    REINFORCEMENT_LEARNING = "REINFORCEMENT_LEARNING"
    Q_LEARNING = "Q_LEARNING"
    SUPERVISED_LEARNING = "SUPERVISED_LEARNING"
    UNSUPERVISED_LEARNING = "UNSUPERVISED_LEARNING"
    SEMI_SUPERVISED_LEARNING = "SEMI_SUPERVISED_LEARNING"
    SELF_SUPERVISED_LEARNING = "SELF_SUPERVISED_LEARNING"
    IMITATION_LEARNING = "IMITATION_LEARNING"


class AgentEvolutionType(str, enum.Enum):
    STATIC_STATELESS = "STATIC_STATELESS"
    ADAPTIVE = "ADAPTIVE"
    SELF_LEARNING = "SELF_LEARNING"
    SELF_EVOLVING = "SELF_EVOLVING"
    SELF_WRITING = "SELF_WRITING"


# ============================================================================
# 1. Q-Learning & Reinforcement Learning Engine
# ============================================================================

class QLearningEngine:
    """Tabular and function-approximated Q-Learning for query routing policies."""

    ACTIONS = [
        "DETERMINISTIC_GRAPH",
        "NON_DETERMINISTIC_NEURAL",
        "PROBABILISTIC_BAYES",
        "HEURISTIC_SEARCH",
        "STOCHASTIC_MONTE_CARLO",
        "HYBRID_HYPERAUTOMATION",
    ]

    def __init__(self, alpha: float = 0.15, gamma: float = 0.90, epsilon: float = 0.10) -> None:
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        # Q-table: state_key -> {action: q_value}
        self.q_table: dict[str, dict[str, float]] = {}
        self.total_updates: int = 0

    def _discretize_state(self, query: str) -> str:
        """Map raw query into discrete state category based on semantic intent."""
        q_lower = query.lower()
        if any(kw in q_lower for kw in ["find", "match", "select", "where", "cypher", "sparql"]):
            return "STRUCTURED_GRAPH_QUERY"
        elif any(kw in q_lower for kw in ["why", "explain", "cause", "reason", "because"]):
            return "CAUSAL_EXPLANATION"
        elif any(kw in q_lower for kw in ["probability", "likely", "risk", "chance"]):
            return "RISK_PROBABILITY"
        elif any(kw in q_lower for kw in ["shortest", "fastest", "optimal", "rank", "path"]):
            return "OPTIMIZATION_SEARCH"
        elif any(kw in q_lower for kw in ["simulate", "scenario", "what-if", "random"]):
            return "SIMULATION_EXPLORATION"
        else:
            return "GENERAL_SYNTHESIS"

    def select_action(self, query: str, force_exploit: bool = False) -> str:
        """Epsilon-greedy action selection."""
        state = self._discretize_state(query)
        if state not in self.q_table:
            self.q_table[state] = {a: 1.0 for a in self.ACTIONS}

        # Exploration vs exploitation
        if not force_exploit and random.random() < self.epsilon:
            return random.choice(self.ACTIONS)

        # Greedily pick action with highest Q-value
        q_vals = self.q_table[state]
        best_action = max(q_vals.keys(), key=lambda a: q_vals[a])
        return best_action

    def update(self, query: str, action: str, reward: float, next_query: str | None = None) -> float:
        """Bellman equation update on Q-value."""
        state = self._discretize_state(query)
        if state not in self.q_table:
            self.q_table[state] = {a: 1.0 for a in self.ACTIONS}

        current_q = self.q_table[state].get(action, 1.0)

        if next_query:
            next_state = self._discretize_state(next_query)
            if next_state not in self.q_table:
                self.q_table[next_state] = {a: 1.0 for a in self.ACTIONS}
            max_future_q = max(self.q_table[next_state].values())
        else:
            max_future_q = current_q

        # Q(s, a) = Q(s, a) + alpha * (reward + gamma * max_a' Q(s', a') - Q(s, a))
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state][action] = round(new_q, 4)
        self.total_updates += 1
        return new_q


# ============================================================================
# 2. Imitation Learning / Behavioral Cloning Engine
# ============================================================================

@dataclass
class ExpertTrajectory:
    trajectory_id: str
    query: str
    embedding: list[float]
    approach: str
    steps: list[str]
    outcome_rating: float
    timestamp: float


class ImitationLearningEngine:
    """Clones expert human engineering query trajectories."""

    def __init__(self) -> None:
        self.trajectories: list[ExpertTrajectory] = []
        self._llm = get_self_llm_engine()

    def record_demonstration(
        self,
        query: str,
        approach: str,
        steps: list[str],
        outcome_rating: float = 1.0,
    ) -> ExpertTrajectory:
        emb = self._llm.embed(query, dimensions=256)
        traj = ExpertTrajectory(
            trajectory_id=str(uuid.uuid4())[:8],
            query=query,
            embedding=emb,
            approach=approach,
            steps=steps,
            outcome_rating=outcome_rating,
            timestamp=time.time(),
        )
        self.trajectories.append(traj)
        return traj

    def clone_behavior(self, query: str) -> dict[str, Any] | None:
        """Find most similar expert demonstration and clone action plan."""
        if not self.trajectories:
            return None

        q_emb = self._llm.embed(query, dimensions=256)
        scored = []
        for traj in self.trajectories:
            sim = TensorMath.cosine_similarity(q_emb, traj.embedding)
            scored.append((sim, traj))

        scored.sort(key=lambda x: x[0], reverse=True)
        best_sim, best_traj = scored[0]

        if best_sim >= 0.65:
            return {
                "matched_expert_query": best_traj.query,
                "similarity": round(best_sim, 3),
                "recommended_approach": best_traj.approach,
                "cloned_steps": best_traj.steps,
            }
        return None


# ============================================================================
# 3. Semi-Supervised & Self-Supervised Knowledge Graph Learner
# ============================================================================

class KnowledgeGraphLearner:
    """Self-supervised link prediction and semi-supervised label propagation."""

    @staticmethod
    def predict_missing_links(
        entities: list[str],
        known_edges: list[tuple[str, str, str]],
    ) -> list[dict[str, Any]]:
        """Self-supervised link prediction: identifies highly probable latent edges."""
        engine = get_self_llm_engine()
        predicted = []
        existing_pairs = {(s, t) for s, _, t in known_edges} | {(t, s) for s, _, t in known_edges}

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                e1, e2 = entities[i], entities[j]
                if (e1, e2) not in existing_pairs:
                    emb1 = engine.embed(e1, dimensions=128)
                    emb2 = engine.embed(e2, dimensions=128)
                    affinity = TensorMath.cosine_similarity(emb1, emb2)
                    if affinity > 0.70:
                        predicted.append({
                            "source": e1,
                            "target": e2,
                            "predicted_relation": "CORRELATES_WITH",
                            "confidence": round(affinity, 3),
                            "paradigm": LearningParadigm.SELF_SUPERVISED_LEARNING.value,
                        })
        return predicted

    @staticmethod
    def propagate_labels(
        graph_nodes: list[dict[str, Any]],
        labeled_seed: dict[str, str],
        max_iterations: int = 5,
    ) -> dict[str, str]:
        """Semi-supervised label propagation across adjacency relationships."""
        labels = dict(labeled_seed)
        for _ in range(max_iterations):
            for node in graph_nodes:
                nid = node.get("id", "")
                if nid not in labels:
                    neighbors = node.get("neighbors", [])
                    neighbor_labels = [labels[nb] for nb in neighbors if nb in labels]
                    if neighbor_labels:
                        # Majority voting among labeled neighbors
                        labels[nid] = max(set(neighbor_labels), key=neighbor_labels.count)
        return labels


# ============================================================================
# 4. Unsupervised Concept Clustering
# ============================================================================

class UnsupervisedClusterer:
    """Unsupervised concept clustering using dense semantic embeddings."""

    @staticmethod
    def cluster_concepts(concepts: list[str], k: int = 3) -> dict[int, list[str]]:
        engine = get_self_llm_engine()
        if not concepts:
            return {}

        embeddings = [engine.embed(c, dimensions=128) for c in concepts]
        actual_k = min(k, len(concepts))

        # Initial centroids
        centroids = [embeddings[i] for i in range(actual_k)]
        clusters: dict[int, list[str]] = {i: [] for i in range(actual_k)}

        for c, emb in zip(concepts, embeddings):
            best_idx = 0
            best_sim = -1.0
            for idx, cent in enumerate(centroids):
                sim = TensorMath.cosine_similarity(emb, cent)
                if sim > best_sim:
                    best_sim = sim
                    best_idx = idx
            clusters[best_idx].append(c)

        return clusters


# ============================================================================
# 5. Self-Writing & Self-Evolving Agent Harness
# ============================================================================

class SelfEvolvingAgentHarness:
    """Self-writing and self-evolving agent adaptation harness."""

    def __init__(self) -> None:
        self.evolved_prompts: dict[str, str] = {}
        self.evolution_history: list[dict[str, Any]] = []

    def evolve_prompt(self, task_name: str, base_prompt: str, failure_trace: list[str]) -> str:
        """Self-writing synthesis: rewrites prompt to overcome previous failure modes."""
        augmented_prompt = (
            f"{base_prompt}\n"
            f"[Self-Evolving Invariant Directive]: Avoid previous failure patterns: {'; '.join(failure_trace[-3:])}. "
            f"Adhere strictly to verified graph topology and deterministic type constraints."
        )
        self.evolved_prompts[task_name] = augmented_prompt
        self.evolution_history.append({
            "task_name": task_name,
            "timestamp": time.time(),
            "failure_trace_count": len(failure_trace),
            "evolution_type": AgentEvolutionType.SELF_WRITING.value,
        })
        return augmented_prompt

    def evolve_agent_prompt(
        self,
        agent_archetype: str,
        system_prompt: str,
        failure_trace: str | list[str],
    ) -> str:
        """Convenience alias for agent-level prompt evolution."""
        traces = [failure_trace] if isinstance(failure_trace, str) else failure_trace
        return self.evolve_prompt(
            task_name=agent_archetype,
            base_prompt=system_prompt,
            failure_trace=traces,
        )



# ============================================================================
# 6. Master Cognitive Learning Engine
# ============================================================================

class CognitiveLearningEngine:
    """Master engine orchestrating all learning paradigms and adaptive agents."""

    def __init__(self) -> None:
        self.q_learning = QLearningEngine()
        self.imitation_learning = ImitationLearningEngine()
        self.kg_learner = KnowledgeGraphLearner()
        self.clusterer = UnsupervisedClusterer()
        self.self_evolving = SelfEvolvingAgentHarness()

        # Seed initial expert demonstrations for common architectural patterns
        self.imitation_learning.record_demonstration(
            query="Analyze microservice dependencies and failure blast radius",
            approach="HYBRID",
            steps=[
                "1. Query graph for upstream/downstream dependency subgraphs",
                "2. Calculate betweenness centrality on bottleneck nodes",
                "3. Apply Monte Carlo failure cascades to measure blast radius",
                "4. Synthesize executive resilience playbook",
            ],
            outcome_rating=0.98,
        )
        self.imitation_learning.record_demonstration(
            query="Find all active payment services with database dependencies",
            approach="DETERMINISTIC",
            steps=[
                "1. Transpile natural language into openCypher query",
                "2. Validate against ontology schema constraints",
                "3. Execute on native graph database adapter",
                "4. Return structured record set with cryptographic hash",
            ],
            outcome_rating=1.0,
        )

    def get_learning_telemetry(self) -> dict[str, Any]:
        """Telemetry summarizing state of all learning algorithms."""
        return {
            "q_learning": {
                "total_updates": self.q_learning.total_updates,
                "states_discovered": len(self.q_learning.q_table),
                "q_table": self.q_learning.q_table,
            },
            "imitation_learning": {
                "demonstrations_stored": len(self.imitation_learning.trajectories),
            },
            "self_evolving": {
                "evolved_prompts_count": len(self.self_evolving.evolved_prompts),
                "evolution_events": len(self.self_evolving.evolution_history),
            },
            "paradigms_active": [p.value for p in LearningParadigm],
            "agent_evolution_types": [a.value for a in AgentEvolutionType],
        }
