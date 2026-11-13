"""
Test battery of the evolutionary arc. Each section names the EEE rule it exercises.

Run:  pytest -q examples/evolutionary-arc/code/tests
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_sink import (  # noqa: E402
    FLAG_DEFAULT,
    FLAG_DOMAIN,
    AuditEvent,
    FlagError,
    StoreUnavailable,
    build_sink,
    resolve_mode,
)

EV = AuditEvent(event_id="ev-1", actor="svc-a", action="task.created")


def healthy(_event):
    return None


def down(_event):
    raise StoreUnavailable("store down")


# ---------------------------------------------------------------------------
# Flag contract (chapter 06 §3): default neutral, explicit domain, no silent fallback
# ---------------------------------------------------------------------------
def test_flag_default_is_behaviour_neutral():
    assert FLAG_DEFAULT == "off"
    assert resolve_mode({}) == "off"


def test_flag_domain_is_tri_state_not_boolean():
    # Rule R1: a boolean in a three-state domain is the signature of the family.
    assert set(FLAG_DOMAIN) == {"off", "shadow", "enforce"}


def test_flag_value_outside_domain_fails_loud_not_silent_fallback():
    with pytest.raises(FlagError):
        resolve_mode({"AUDIT_SINK_MODE": "true"})  # a boolean sneaking in


# ---------------------------------------------------------------------------
# P1 · off — the stub proves the pipe, not the measurement
# ---------------------------------------------------------------------------
def test_p1_off_records_through_stub_with_scaffold_provenance():
    sink = build_sink({"AUDIT_SINK_MODE": "off"}, healthy)
    rec = sink.record(EV)
    assert rec.stored is True
    assert rec.provenance == "scaffold"  # never readable as a real measurement
    assert sink.real.records == []  # behaviour-neutral: nothing reached the real store


def test_p1_off_announces_scaffold_path_loudly():
    sink = build_sink({"AUDIT_SINK_MODE": "off"}, healthy)
    assert any("scaffold path is LIVE" in line for line in sink.loud_log)


# ---------------------------------------------------------------------------
# P2 · shadow — computes and logs divergence; does NOT decide
# ---------------------------------------------------------------------------
def test_p2_shadow_exercises_real_but_stub_decides():
    sink = build_sink({"AUDIT_SINK_MODE": "shadow"}, healthy)
    rec = sink.record(EV)
    assert rec.provenance == "scaffold"  # the stub is still authoritative
    assert len(sink.real.records) == 1  # the real path was exercised
    assert sink.intent_log[-1].diverged is False


def test_p2_shadow_logs_divergence_when_real_store_is_down():
    # Disagreeable pair (R2): stub_ok vs real_ok can disagree, and here they must.
    sink = build_sink({"AUDIT_SINK_MODE": "shadow"}, down)
    rec = sink.record(EV)
    assert rec.stored is True  # product unaffected
    assert sink.intent_log[-1].diverged is True


# ---------------------------------------------------------------------------
# P4 · enforce — the real adapter decides; M11 posture is fail-open with durable buffer (R7)
# ---------------------------------------------------------------------------
def test_p4_enforce_happy_path_records_real():
    sink = build_sink({"AUDIT_SINK_MODE": "enforce"}, healthy)
    rec = sink.record(EV)
    assert rec.provenance == "real"
    assert rec.stored is True
    assert sink.durable_buffer == []


@pytest.mark.parametrize(
    "fault",
    [
        pytest.param(down, id="store-unavailable"),
    ],
)
def test_p4_enforce_fault_injection_never_discards_evidence(fault):
    # Fault injection for the M11 row: evidence sink -> fail-open with durable buffer.
    sink = build_sink({"AUDIT_SINK_MODE": "enforce"}, fault)
    rec = sink.record(EV)
    assert rec.stored is False  # honest: not stored yet (no fabricated success)
    assert sink.durable_buffer == [EV]  # ...but never lost
    assert any("buffered ev-1" in line for line in sink.loud_log)


def test_p4_enforce_buffer_drains_when_store_recovers():
    state = {"up": False}

    def flaky(_event):
        if not state["up"]:
            raise StoreUnavailable("still down")

    sink = build_sink({"AUDIT_SINK_MODE": "enforce"}, flaky)
    sink.record(EV)
    assert len(sink.durable_buffer) == 1
    state["up"] = True
    assert sink.drain_buffer() == 1
    assert sink.durable_buffer == []
    assert [r.event_id for r in sink.real.records] == ["ev-1"]


# ---------------------------------------------------------------------------
# Negative control against loosening (chapter 06 §4): the neighbour must stay barred
# ---------------------------------------------------------------------------
def test_neighbour_stays_barred_enforce_does_not_fall_back_to_stub():
    # (3) in the (1)(2)(3) battery: making the sink tolerant to store failure must NOT
    # leak into "quietly answer from the scaffold". The stub must stay untouched in enforce.
    sink = build_sink({"AUDIT_SINK_MODE": "enforce"}, down)
    sink.record(EV)
    assert sink.stub.records == []  # no silent fallback to scaffold (anti-pattern)


# ---------------------------------------------------------------------------
# Declared debt as a closure detector (R29b): strict xfail
# ---------------------------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="debt: drain is manual; automatic retry is a later arc")
def test_debt_buffer_drains_automatically_without_operator_call():
    state = {"up": False}

    def flaky(_event):
        if not state["up"]:
            raise StoreUnavailable("down")

    sink = build_sink({"AUDIT_SINK_MODE": "enforce"}, flaky)
    sink.record(EV)
    state["up"] = True
    # Property not yet true: without calling drain_buffer() the buffer should empty itself.
    assert sink.durable_buffer == []
