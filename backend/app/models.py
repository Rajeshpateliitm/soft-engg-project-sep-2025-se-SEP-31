"""Database tables for the Flask backend (tables only).

Derived from the wireframe for Login and Registration.

"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy instance to be initialized in the Flask app factory
db = SQLAlchemy()


class TimestampMixin:
    """Common timestamp columns."""

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)  # row creation time
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False  # last update time
    )


class SoftDeleteMixin:
    """Soft delete flag."""

    is_active = db.Column(db.Boolean, default=True, nullable=False)  # false => archived/soft-deleted


class UserCategory(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "user_categories"

    id = db.Column(db.Integer, primary_key=True)  # PK
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)  # stable identifier (e.g., PRIMARY)
    label = db.Column(db.String(128), nullable=False)  # human-readable label

    # relationships
    users = relationship("User", back_populates="user_category")  # users assigned to this category


class User(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # PK
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)  # login email (unique)
    username = db.Column(db.String(150), unique=True, nullable=True, index=True)  # optional display handle
    password_hash = db.Column(db.String(255), nullable=False)  # hashed password
    house_number = db.Column(db.String(50), nullable=True)  # household address number
    ward_number = db.Column(db.String(50), nullable=True)  # administrative ward identifier (legacy text)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=True, index=True)  # FK -> ward (preferred)
    family_members_count = db.Column(db.Integer, nullable=True)  # number of members in household
    pincode = db.Column(db.String(12), nullable=True, index=True)  # postal code for geo queries
    points = db.Column(db.Integer, default=0, nullable=False)  # gamification/leaderboard points
    user_category_id = db.Column(
        db.Integer, db.ForeignKey("user_categories.id"), nullable=True, index=True  # foreign key to category
    )

    user_category = relationship("UserCategory", back_populates="users")  # ORM relation to category
    ward = relationship("Ward", back_populates="users")  # ORM relation to ward

    # relationships (from other tables)
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all,delete-orphan")  # user's quiz history
    waste_logs = relationship("WasteLog", back_populates="user", cascade="all,delete-orphan")  # daily waste entries
    campaign_registrations = relationship("CampaignRegistration", back_populates="user", cascade="all,delete-orphan")  # event signups
    engagements = relationship("Engagement", back_populates="user", cascade="all,delete-orphan")  # monthly engagement stats

    def set_password(self, password):
        """Set password hash with increased security parameters."""
        # Use pbkdf2:sha256 for Python 3.9 compatibility (scrypt requires Python 3.11+)
        # Increased iterations to 100,000 for better protection against brute-force attacks
        # Format: pbkdf2:sha256:iterations (iterations specified in method string)
        # salt_length=16 provides strong salt generation
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256:100000',  # 100,000 iterations for better security
            salt_length=16
        )

    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)


class QuizQuestion(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)  # PK
    question_text = db.Column(db.Text, nullable=False)  # question body
    category = db.Column(db.String(64), nullable=True, index=True)  # topic/category label
    options = relationship("QuizOption", back_populates="question", cascade="all,delete-orphan")  # choices for this question


class QuizOption(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "quiz_options"

    id = db.Column(db.Integer, primary_key=True)  # PK
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False, index=True)  # FK -> question
    option_text = db.Column(db.Text, nullable=False)  # answer option text
    is_correct = db.Column(db.Boolean, default=False, nullable=False)  # marks correct option
    question = relationship("QuizQuestion", back_populates="options")  # parent question
    answers = relationship("QuizAnswer", back_populates="selected_option")  # selected in answers


class QuizAttempt(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)  # PK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    score = db.Column(db.Integer, default=0, nullable=False)  # number of correct answers
    total_questions = db.Column(db.Integer, default=0, nullable=False)  # attempted count
    user = relationship("User", back_populates="quiz_attempts")  # attempt owner
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all,delete-orphan")  # per-question responses


class QuizAnswer(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "quiz_answers"

    id = db.Column(db.Integer, primary_key=True)  # PK
    attempt_id = db.Column(db.Integer, db.ForeignKey("quiz_attempts.id"), nullable=False, index=True)  # FK -> attempt
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False, index=True)  # FK -> question
    selected_option_id = db.Column(db.Integer, db.ForeignKey("quiz_options.id"), nullable=True, index=True)  # chosen option
    is_correct = db.Column(db.Boolean, default=False, nullable=False)  # correctness flag
    attempt = relationship("QuizAttempt", back_populates="answers")  # parent attempt
    selected_option = relationship("QuizOption", back_populates="answers")  # selected choice
    question = relationship("QuizQuestion")  # denormalized link for convenience


class RandomQuizAttempt(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "random_quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)  # PK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    attempt_date = db.Column(db.Date, server_default=func.current_date(), nullable=False, index=True)  # date of attempt
    user = relationship("User")  # user who generated the quiz


class WasteLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "waste_logs"

    id = db.Column(db.Integer, primary_key=True)  # PK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    log_date = db.Column(db.Date, server_default=func.current_date(), nullable=False, index=True)  # entry date
    category = db.Column(db.String(64), nullable=False, index=True)  # waste category (wet/dry/etc.)
    quantity_kg = db.Column(db.Float, nullable=False)  # weight in kilograms
    notes = db.Column(db.Text, nullable=True)  # optional remarks
    separated = db.Column(db.Boolean, default=False, nullable=False)  # whether waste was separated
    recycled = db.Column(db.Boolean, default=False, nullable=False)  # whether waste was recycled/reused/donated
    questions_doubts = db.Column(db.Text, nullable=True)  # questions if not separated
    feedback = db.Column(db.Text, nullable=True)  # general feedback
    user = relationship("User", back_populates="waste_logs")  # owner of the log


class Engagement(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "engagements"

    id = db.Column(db.Integer, primary_key=True)  # PK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    month = db.Column(db.Date, nullable=False, index=True)  # first day of month represents the period
    engagement_type = db.Column(db.String(64), nullable=False, index=True)  # metric name (e.g., logins)
    value = db.Column(db.Integer, default=0, nullable=False)  # metric value
    user = relationship("User", back_populates="engagements")  # owner of metric


class Campaign(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)  # PK
    name = db.Column(db.String(200), nullable=False)  # campaign title
    description = db.Column(db.Text, nullable=True)  # details shown on card
    event_datetime = db.Column(db.DateTime, nullable=True, index=True)  # scheduled date/time
    location = db.Column(db.String(255), nullable=True)  # venue/location text
    pincode = db.Column(db.String(12), nullable=True, index=True)  # area filter
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=True, index=True)  # optional FK -> ward
    image_url = db.Column(db.String(500), nullable=True)  # optional image reference
    registrations = relationship("CampaignRegistration", back_populates="campaign", cascade="all,delete-orphan")  # user signups
    ward = relationship("Ward", back_populates="campaigns")  # campaign's ward


class CampaignRegistration(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "campaign_registrations"

    id = db.Column(db.Integer, primary_key=True)  # PK
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False, index=True)  # FK -> campaign
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    status = db.Column(db.String(32), default="registered", nullable=False, index=True)  # registered | attended | cancelled
    campaign = relationship("Campaign", back_populates="registrations")  # campaign joined
    user = relationship("User", back_populates="campaign_registrations")  # joining user


class RecyclerLocation(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "recycler_locations"

    id = db.Column(db.Integer, primary_key=True)  # PK
    name = db.Column(db.String(200), nullable=False)  # recycler name
    address = db.Column(db.String(500), nullable=True)  # street address
    pincode = db.Column(db.String(12), nullable=True, index=True)  # area for search
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=True, index=True)  # optional FK -> ward
    latitude = db.Column(db.Float, nullable=True)  # geo latitude
    longitude = db.Column(db.Float, nullable=True)  # geo longitude
    phone = db.Column(db.String(32), nullable=True)  # contact phone
    website = db.Column(db.String(255), nullable=True)  # optional website
    ward = relationship("Ward", back_populates="recyclers")  # ward relation


# ----------------------- Secondary user (RWA/Collector) -----------------------

class RwaGroup(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "rwa_groups"

    id = db.Column(db.Integer, primary_key=True)  # PK
    name = db.Column(db.String(200), nullable=False, unique=True)  # group name
    ward_number = db.Column(db.String(50), nullable=True, index=True)  # ward the RWA covers
    pincode = db.Column(db.String(12), nullable=True, index=True)  # area mapping
    members = relationship("RwaMembership", back_populates="rwa_group", cascade="all,delete-orphan")  # memberships


class RwaMembership(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "rwa_memberships"

    id = db.Column(db.Integer, primary_key=True)  # PK
    rwa_group_id = db.Column(db.Integer, db.ForeignKey("rwa_groups.id"), nullable=False, index=True)  # FK -> RWA group
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # FK -> user
    role = db.Column(db.String(32), nullable=False, index=True)  # member | admin | collector
    rwa_group = relationship("RwaGroup", back_populates="members")  # group
    user = relationship("User")  # member user


class PickupRequest(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "pickup_requests"

    id = db.Column(db.Integer, primary_key=True)  # PK
    request_code = db.Column(db.String(32), nullable=True, unique=True, index=True)  # human-friendly tracking code

    # requester and assignment
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)  # who requested pickup
    assigned_collector_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)  # assigned collector

    # when and where
    requested_at = db.Column(db.DateTime, server_default=func.now(), nullable=False, index=True)  # request timestamp
    scheduled_at = db.Column(db.DateTime, nullable=True, index=True)  # scheduled time (if set)
    pickup_location = db.Column(db.String(500), nullable=True)  # address or landmark
    pincode = db.Column(db.String(12), nullable=True, index=True)  # area for filtering

    # details
    quantity = db.Column(db.Float, nullable=True)  # estimated weight/volume
    notes = db.Column(db.Text, nullable=True)  # requester notes

    # workflow
    status = db.Column(  # pending | accepted | rejected | completed
        db.String(32),
        default="pending",
        nullable=False,
        index=True,
    )
    decision_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # who changed status
    decision_at = db.Column(db.DateTime, nullable=True)  # when status was changed
    requester = relationship("User", foreign_keys=[requester_id], backref="pickup_requests")  # relation to requester
    collector = relationship("User", foreign_keys=[assigned_collector_id], backref="pickup_assignments")  # relation to collector
    decision_by = relationship("User", foreign_keys=[decision_by_user_id])  # relation to deciding user


# ------------------------------ Tertiary user -------------------------------

class Ward(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "wards"

    id = db.Column(db.Integer, primary_key=True)  # PK
    ward_number = db.Column(db.String(50), nullable=False, unique=True, index=True)  # official ward identifier
    name = db.Column(db.String(200), nullable=True)  # optional friendly name
    pincode = db.Column(db.String(12), nullable=True, index=True)  # predominant pincode
    summaries = relationship("WardMonthlySummary", back_populates="ward", cascade="all,delete-orphan")  # monthly KPI rows
    users = relationship("User", back_populates="ward")  # residents in this ward
    campaigns = relationship("Campaign", back_populates="ward")  # campaigns scoped to this ward
    recyclers = relationship("RecyclerLocation", back_populates="ward")  # recyclers in this ward


class WardMonthlySummary(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ward_monthly_summaries"

    id = db.Column(db.Integer, primary_key=True)  # PK
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=False, index=True)  # FK -> ward
    year = db.Column(db.Integer, nullable=False, index=True)  # reporting year
    month = db.Column(db.Integer, nullable=False, index=True)  # reporting month (1-12)
    total_households = db.Column(db.Integer, nullable=False, default=0)  # households in ward
    avg_wet_kg_per_day = db.Column(db.Float, nullable=False, default=0.0)  # average wet waste per day
    avg_dry_kg_per_day = db.Column(db.Float, nullable=False, default=0.0)  # average dry waste per day
    avg_hazardous_kg_per_day = db.Column(db.Float, nullable=False, default=0.0)  # hazardous waste per day
    segregation_compliance_pct = db.Column(db.Float, nullable=False, default=0.0)  # percent households segregating
    remarks = db.Column(db.Text, nullable=True)  # admin notes or actions
    ward = relationship("Ward", back_populates="summaries")  # parent ward

    __table_args__ = (
        db.UniqueConstraint("ward_id", "year", "month", name="uq_ward_month"),
    )

