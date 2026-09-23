from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text
from datetime import datetime
from enum import Enum
import uuid

class PatchNoteType(Enum):
    BUG_FIX = "Bug Fix"
    FEATURE = "Feature"
    OTHER = "Other"

class PatchNote(SQLModel, table=True):
    id: uuid.uuid4 | None = Field(default=None, primary_key=True)
    version: str
    title: str
    content: str
    published_at : datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    category: PatchNoteType = Field(sa_column=Column(
        Enum(PatchNoteType),
        default=PatchNoteType.OTHER,
        nullable=False,
        index=False
    ))
