from app.db.session import Base, engine


def seed() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    seed()
