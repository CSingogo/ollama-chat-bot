from database import SessionLocal, create_db_and_tables
from sqlmodel import Field, Session, select,SQLModel,create_engine



from models import User

def seed_database(session: Session) -> None: 
    if not session.exec(select(User)).first(): 
        print("🌱 Seeding database with mock users...")
        for u in mock_users:
            session.add(u)

        session.commit()
    else:
        print("Database already has data. Skipping seed.")


mock_users = [
    User(
        name="Alice Smith",
        account_status="Active",
        subscription_plan="Pro Plan",
        is_active=True
    ),
    User(
        name="Bob Jones",
        account_status="Locked",
        subscription_plan="Free Plan",
        is_active=True
    ),
    User(
        name="Charlie Brown",
        account_status="Active",
        subscription_plan="Enterprise Plan",
        is_active=False
    ),
    User(
        name="Diana Prince",
        account_status="active",
        subscription_plan="Free Plan",
        is_active=True
    )
]



if __name__ == "__main__":
    create_db_and_tables()
    session = SessionLocal()
    seed_database(session=session)
