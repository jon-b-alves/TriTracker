from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from contextlib import contextmanager

# engine provides connectivity to database
ENGINE = create_engine("")


# used to create model classes below
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)
    pace = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users", nullable=False))
    user = relationship("User", back_populates="workouts", cascade="all, delete-orphan")


def create_tables(engine) -> None:
    Base.metadata.create_all(engine)

@contextmanager
def session_context_manager(engine):
    session = _create_session(engine)

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def _create_session(engine) -> sessionmaker:
    return sessionmaker(bind=engine)