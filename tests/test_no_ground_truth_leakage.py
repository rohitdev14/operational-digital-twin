import inspect
import intelligence.evidence as evidence
import intelligence.diagnosis as diagnosis

def test_diagnostic_code_does_not_consume_injected_failure_cause():
    source=inspect.getsource(diagnosis)
    assert "failure_cause" not in source
    assert "scenario" not in source
    assert "failure_cause" in evidence.HIDDEN_FIELDS
    assert "scenario" in evidence.HIDDEN_FIELDS
