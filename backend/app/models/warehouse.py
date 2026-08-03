from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Warehouse(Base):
    """
    Warehouse Master
    """

    __tablename__ = "warehouses"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "warehouse_code",
            name="uq_warehouse_org_code",
        ),
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    warehouse_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    warehouse_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    warehouse_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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