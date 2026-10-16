"""Evaluation & Benchmarking engine — unified eval framework, automated
regression detection, benchmark suites, and quality gates."""

from eoip.evaluation.engine import (
    Benchmark,
    BenchmarkResult,
    BenchmarkSuite,
    EvalMetric,
    EvaluationEngine,
    QualityGate,
    RegressionDetector,
    TestCase,
    TestResult,
    get_evaluation_engine,
)

__all__ = [
    "Benchmark",
    "BenchmarkResult",
    "BenchmarkSuite",
    "EvalMetric",
    "EvaluationEngine",
    "QualityGate",
    "RegressionDetector",
    "TestCase",
    "TestResult",
    "get_evaluation_engine",
]
