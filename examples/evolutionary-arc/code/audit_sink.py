"""
EEE evolutionary arc — reference example (pure Python, no dependencies).

Property under construction:
    "Every audit event emitted by the application is durably recorded,
     even when the downstream audit store is unavailable."

The arc is anchored by a flag with a THREE-state domain (Rule R1):

    AUDIT_SINK_MODE = off | shadow | enforce

    off     -> P1: the stub records to an in-memory list (scaffold). Behaviour-neutral
               for the product: nothing reaches the real store, and every record is
               tagged with provenance "scaffold" so it can never be read as a measurement.
    shadow  -> P2: the real adapter is exercised, but it does NOT decide. The stub remains
               authoritative; the divergence between both is written to an intent log.
    enforce -> P4: the real adapter decides. Failure posture (M11, Rule R7):
               fail-open with a durable buffer. Evidence of an event that already
               happened is never discarded.

Everything that a flag must declare (default, domain, posture) lives here, next to the
code that consumes it, so a ghost flag is impossible by construction.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

FLAG_NAME = "AUDIT_SINK_MODE"
FLAG_DOMAIN = ("off", "shadow", "enforce")
FLAG_DEFAULT = "off"  # behaviour-neutral default in code (P1)


class FlagError(ValueError):
    """Raised when the flag carries a value outside its declared domain."""


def resolve_mode(env: Optional[Dict[str, str]] = None) -> str:
    """Resolve the flag from the environment.

    A value outside the domain is an error, never a silent fallback to default:
    silent fallback is config-as-state and hides a mis-deploy.
    """
    env = os.environ if env is None else env
    raw = env.get(FLAG_NAME, FLAG_DEFAULT).strip().lower()
    if raw not in FLAG_DOMAIN:
        raise FlagError(
            "%s=%r is outside the declared domain %s" % (FLAG_NAME, raw, FLAG_DOMAIN)
        )
    return raw


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    actor: str
    action: str


@dataclass
class Record:
    event_id: str
    provenance: str  # "scaffold" | "real" — never a bare boolean (Rule R1)
    stored: bool


class StoreUnavailable(RuntimeError):
    """The downstream audit store could not be reached."""


class StubSink:
    """P1 scaffold. Proves the pipe, not the measurement."""

    def __init__(self) -> None:
        self.records: List[Record] = []

    def write(self, event: AuditEvent) -> Record:
        rec = Record(event_id=event.event_id, provenance="scaffold", stored=True)
        self.records.append(rec)
        return rec


class RealSink:
    """The real adapter. `transport` is injected so failure can be injected in tests."""

    def __init__(self, transport: Callable[[AuditEvent], None]) -> None:
        self._transport = transport
        self.records: List[Record] = []

    def write(self, event: AuditEvent) -> Record:
        self._transport(event)  # may raise StoreUnavailable
        rec = Record(event_id=event.event_id, provenance="real", stored=True)
        self.records.append(rec)
        return rec


@dataclass
class IntentLogEntry:
    event_id: str
    stub_ok: bool
    real_ok: bool

    @property
    def diverged(self) -> bool:
        return self.stub_ok != self.real_ok


@dataclass
class AuditSink:
    """Flag-governed facade. This is the single place where the mode is consumed."""

    mode: str
    stub: StubSink
    real: RealSink
    intent_log: List[IntentLogEntry] = field(default_factory=list)
    durable_buffer: List[AuditEvent] = field(default_factory=list)
    loud_log: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.mode not in FLAG_DOMAIN:
            raise FlagError("mode %r outside domain %s" % (self.mode, FLAG_DOMAIN))
        # Explicit, loud boot line whenever a scaffold path is live (never silent).
        if self.mode != "enforce":
            self.loud_log.append("%s=%s: scaffold path is LIVE" % (FLAG_NAME, self.mode))

    def record(self, event: AuditEvent) -> Record:
        if self.mode == "off":
            return self.stub.write(event)

        if self.mode == "shadow":
            # Shadow computes and logs divergence; the stub still decides.
            stub_rec = self.stub.write(event)
            try:
                self.real.write(event)
                real_ok = True
            except StoreUnavailable:
                real_ok = False
            self.intent_log.append(
                IntentLogEntry(event_id=event.event_id, stub_ok=stub_rec.stored, real_ok=real_ok)
            )
            return stub_rec

        # enforce — the real adapter decides. M11 posture: FAIL-OPEN with durable buffer.
        try:
            return self.real.write(event)
        except StoreUnavailable:
            self.durable_buffer.append(event)
            self.loud_log.append("store unavailable; buffered %s" % event.event_id)
            return Record(event_id=event.event_id, provenance="real", stored=False)

    def drain_buffer(self) -> int:
        """Replay buffered events once the store is back. Returns how many were flushed."""
        flushed = 0
        remaining: List[AuditEvent] = []
        for ev in self.durable_buffer:
            try:
                self.real.write(ev)
                flushed += 1
            except StoreUnavailable:
                remaining.append(ev)
        self.durable_buffer = remaining
        return flushed


def build_sink(env: Optional[Dict[str, str]], transport: Callable[[AuditEvent], None]) -> AuditSink:
    return AuditSink(mode=resolve_mode(env), stub=StubSink(), real=RealSink(transport))
