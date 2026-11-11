import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Numeric, DateTime, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool

app = FastAPI(title="AI Agent API Governance Demo", version="0.1.0")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./demo.db")
engine = create_engine(DATABASE_URL, **({"connect_args": {"check_same_thread": False}, "poolclass": StaticPool} if DATABASE_URL == "sqlite://" else {}))

class Base(DeclarativeBase):
    pass

class Usage(Base):
    __tablename__ = "usage_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    agent_id: Mapped[str] = mapped_column(String(120))
    department: Mapped[str] = mapped_column(String(120))
    api_name: Mapped[str] = mapped_column(String(120))
    cost_usd: Mapped[Decimal] = mapped_column(Numeric(14, 6))

@app.on_event("startup")
def create_schema():
    Base.metadata.create_all(engine)

def db_session():
    with Session(engine) as db:
        yield db

def demo_identity(x_demo_agent: Annotated[str | None, Header()] = None,
                  x_demo_department: Annotated[str | None, Header()] = None):
    if os.getenv("DEMO_AUTH", "false").lower() != "true":
        raise HTTPException(503, "Production identity verification not configured; deny by default")
    if not x_demo_agent or not x_demo_department:
        raise HTTPException(401, "Local demo identity headers required")
    if len(x_demo_agent) > 120 or len(x_demo_department) > 120:
        raise HTTPException(400, "Invalid demo identity")
    return {"agent": x_demo_agent, "department": x_demo_department}

class Call(BaseModel):
    api_name: str = Field(min_length=1, max_length=120)
    request_count: int = Field(default=1, ge=1, le=10000)
    unit_cost_usd: Decimal = Field(default=Decimal("0.001"), ge=0, le=100)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/usage")
def record(call: Call, identity=Depends(demo_identity), db: Session = Depends(db_session)):
    cost = call.unit_cost_usd * call.request_count
    event = Usage(agent_id=identity["agent"], department=identity["department"], api_name=call.api_name, cost_usd=cost)
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"event_id": event.id, "cost_usd": str(cost)}

@app.get("/api/v1/usage")
def usage(identity=Depends(demo_identity), db: Session = Depends(db_session)):
    rows = db.execute(select(Usage.api_name, func.count(Usage.id), func.sum(Usage.cost_usd))
                      .where(Usage.department == identity["department"])
                      .group_by(Usage.api_name)).all()
    return {"department": identity["department"], "items": [
        {"api": name, "events": count, "cost_usd": str(total)} for name, count, total in rows]}
