from sqlmodel import Field, SQLModel, Column
from datetime import datetime, timezone
from sqlalchemy import Enum as sql_enum
from enum import Enum
import uuid

class PatchNoteType(Enum):
    BUG_FIX = "Bug Fix"
    FEATURE = "Feature"
    OTHER = "Other"

class PatchNoteBase(SQLModel):
    version: str
    title: str
    content: str
    category: PatchNoteType = Field(sa_column=Column(
        sql_enum(PatchNoteType),
        nullable=False,
        index=False
    ))

class PatchNote(PatchNoteBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    published_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))

class PatchNoteCreate(PatchNoteBase):
    pass

class PatchNoteRead(PatchNoteBase):
    id: uuid.UUID
    published_at: datetime

class PatchNoteUpdate(PatchNoteBase):
    version: str | None = None
    title: str | None = None
    content: str | None = None
    category: PatchNoteType | None = Field(default=None)
