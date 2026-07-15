"""API for the AI Security Data Platform."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from app.database import get_connection, initialize_database
from app.models import SecurityEvent, SecurityEventCreate


DASHBOARD_PATH = Path(__file__).resolve().parent / "static" / "dashboard.html"


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Prepare the database when the platform starts."""
    initialize_database()
    yield


app = FastAPI(
    title="AI Security Data Platform",
    description="Collects and organizes events from security devices.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def platform_information() -> dict[str, str]:
    """Return basic platform information."""
    return {
        "platform": "AI Security Data Platform",
        "status": "online",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the API is running."""
    return {"status": "healthy"}

@app.get("/dashboard", include_in_schema=False)
def dashboard() -> FileResponse:
    """Display the security-event dashboard."""
    return FileResponse(DASHBOARD_PATH)

@app.post("/events", response_model=SecurityEvent, status_code=201)
def create_event(event: SecurityEventCreate) -> dict:
    """Store a new security event."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO security_events (
                device_id,
                event_type,
                severity,
                description,
                confidence
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.device_id,
                event.event_type,
                event.severity,
                event.description,
                event.confidence,
            ),
        )
        connection.commit()

        stored_event = connection.execute(
            "SELECT * FROM security_events WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return dict(stored_event)


@app.get("/events", response_model=list[SecurityEvent])
def list_events(
    limit: int = Query(default=100, ge=1, le=500),
) -> list[dict]:
    """Return the newest security events."""
    with get_connection() as connection:
        events = connection.execute(
            """
            SELECT *
            FROM security_events
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(event) for event in events]