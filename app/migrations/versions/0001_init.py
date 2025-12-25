from alembic import op
import sqlalchemy as sa
import app.models as models

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("role", sa.Enum(models.Role), nullable=False),
        sa.Column("active", sa.Boolean, default=True),
    )
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plate", sa.String, unique=True, nullable=False),
        sa.Column("seats", sa.Integer, nullable=False),
        sa.Column("model", sa.String, nullable=False),
        sa.Column("status", sa.Enum(models.VehicleStatus), default=models.VehicleStatus.available),
        sa.Column("permit_expire", sa.Date),
        sa.Column("inspection_expire", sa.Date),
        sa.Column("insurance_expire", sa.Date),
        sa.Column("note", sa.Text),
    )
    op.create_table(
        "staff",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("phone", sa.String, nullable=False),
        sa.Column("role", sa.Enum(models.StaffRole), nullable=False),
        sa.Column("id_type", sa.String),
        sa.Column("id_expire", sa.Date),
        sa.Column("status", sa.Enum(models.StaffStatus), default=models.StaffStatus.on_duty),
        sa.Column("note", sa.Text),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("customer", sa.String, nullable=False),
        sa.Column("contact", sa.String),
        sa.Column("phone", sa.String),
        sa.Column("ride_time", sa.DateTime, nullable=False),
        sa.Column("origin", sa.String, nullable=False),
        sa.Column("destination", sa.String, nullable=False),
        sa.Column("pax", sa.Integer, nullable=False),
        sa.Column("need_attendant", sa.Boolean, default=False),
        sa.Column("note", sa.Text),
        sa.Column("contract_no", sa.String),
        sa.Column("status", sa.Enum(models.OrderStatus), default=models.OrderStatus.pending),
    )
    op.create_table(
        "dispatches",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("vehicle_id", sa.Integer, sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("driver_id", sa.Integer, sa.ForeignKey("staff.id"), nullable=False),
        sa.Column("attendant_id", sa.Integer, sa.ForeignKey("staff.id")),
        sa.Column("trip_code", sa.String, unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime),
    )
    op.create_table(
        "trips",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("dispatch_id", sa.Integer, sa.ForeignKey("dispatches.id"), nullable=False),
        sa.Column("status", sa.Enum(models.TripStatus), default=models.TripStatus.assigned),
        sa.Column("accepted_at", sa.DateTime),
        sa.Column("departed_at", sa.DateTime),
        sa.Column("arrived_at", sa.DateTime),
        sa.Column("finished_at", sa.DateTime),
        sa.Column("receipt_path", sa.String),
    )
    op.create_table(
        "logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("actor", sa.String),
        sa.Column("role", sa.String),
        sa.Column("action", sa.String),
        sa.Column("target_type", sa.String),
        sa.Column("target_id", sa.Integer),
        sa.Column("created_at", sa.DateTime),
        sa.Column("summary", sa.Text),
    )


def downgrade():
    op.drop_table("logs")
    op.drop_table("trips")
    op.drop_table("dispatches")
    op.drop_table("orders")
    op.drop_table("staff")
    op.drop_table("vehicles")
    op.drop_table("users")
