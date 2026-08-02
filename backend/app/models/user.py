from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    """
    Application User
    """

    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    supabase_user_uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("roles.role_id"),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    created_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )

    updated_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )