from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Numeric,
    func,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Product(Base):
    """
    Product Master
    """

    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "product_code",
            name="uq_product_org_code",
        ),
    )

    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.category_id"),
        nullable=False,
    )

    unit_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("units.unit_id"),
        nullable=False,
    )

    product_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    product_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    product_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
    )

    reorder_level: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
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