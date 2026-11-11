import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, Numeric, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool

from .audit import emit_audit
from .auth import Principal, require_principal
from .quota import assert_within_quota
from .registry import authorize_api, resolve_agent

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./demo.db")
engine = create_engine(
    DATABASE_URL,
    **(
        {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
        if DATABASE_URL == "sqlite://"
        else {}
    ),
)


class Base(DeclarativeBase):
    pass


class Usage(Base):
    __tablename__ = "usage_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    agent_id: Mapped[str] = mapped_column(String(120))
    department: Mapped[str] = mapped_column(String(120))
    api_name: Mapped[str] = mapped_column(String(120))
    request_count: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    cost_usd: Mapped[Decimal] = mapped_column(Numeric(14, 6))


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="AI Agent API Governance Demo",
    version="0.2.0",
    lifespan=lifespan,
)


def db_session():
    with Session(engine) as db:
        yield db


class Call(BaseModel):
    api_name: str = Field(min_length=1, max_length=120)
    request_count: int = Field(default=1, ge=1, le=10000)
    unit_cost_usd: Decimal = Field(default=Decimal("0.001"), ge=0, le=100)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "demo_auth": os.getenv("DEMO_AUTH", "false").lower() in {"1", "true", "yes"},
        "entra_env_present": bool(os.getenv("ENTRA_TENANT_ID") and os.getenv("ENTRA_AUDIENCE")),
    }


@app.post("/api/v1/usage")
def record(
    call: Call,
    principal: Principal = Depends(require_principal),
    db: Session = Depends(db_session),
    x_request_id: Annotated[str | None, Header()] = None,
):
    policy = resolve_agent(principal.agent_id)
    if policy is None or not authorize_api(policy, call.api_name):
        emit_audit(
            action="usage.record",
            principal=principal,
            api_id=call.api_name,
            decision="deny",
            request_id=x_request_id,
            extra={"reason": "api_not_allowed"},
        )
        raise HTTPException(status_code=403, detail="API not allowed for agent")

    assert_within_quota(db, Usage, policy, additional=call.request_count)

    cost = call.unit_cost_usd * call.request_count
    event = Usage(
        agent_id=principal.agent_id,
        department=principal.department,
        api_name=call.api_name,
        request_count=call.request_count,
        cost_usd=cost,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    emit_audit(
        action="usage.record",
        principal=principal,
        api_id=call.api_name,
        decision="allow",
        request_id=x_request_id,
        extra={"event_id": event.id, "cost_usd": str(cost)},
    )
    return {"event_id": event.id, "cost_usd": str(cost)}


@app.get("/api/v1/usage")
def usage(
    principal: Principal = Depends(require_principal),
    db: Session = Depends(db_session),
    x_request_id: Annotated[str | None, Header()] = None,
):
    rows = db.execute(
        select(Usage.api_name, func.count(Usage.id), func.sum(Usage.cost_usd))
        .where(Usage.department == principal.department)
        .group_by(Usage.api_name)
    ).all()
    emit_audit(
        action="usage.read",
        principal=principal,
        api_id="gov-usage",
        decision="allow",
        request_id=x_request_id,
    )
    return {
        "department": principal.department,
        "items": [
            {"api": name, "events": count, "cost_usd": str(total)} for name, count, total in rows
        ],
    }
