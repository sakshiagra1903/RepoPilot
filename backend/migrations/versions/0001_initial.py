"""Initial RepoPilot schema."""
from alembic import op
from app.db import Base
from app import models

def upgrade():
    bind=op.get_bind()
    Base.metadata.create_all(bind=bind)

def downgrade():
    bind=op.get_bind()
    Base.metadata.drop_all(bind=bind)
