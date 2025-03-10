from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Role, Audition

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def seed_data():
   
    role1 = Role(character_name="Hamlet")
    role2 = Role(character_name="Macbeth")
    session.add_all([role1, role2])
    session.commit()

   
    audition1 = Audition(actor="John Doe", location="NYC", phone=1234567890, role_id=role1.id)
    audition2 = Audition(actor="Jane Smith", location="LA", phone=9876543210, role_id=role1.id)

    session.add_all([audition1, audition2])
    session.commit()

    
    audition1.call_back()
    session.commit()

if __name__ == "__main__":
    seed_data()

   
    role = session.query(Role).first()

    print("Actors:", role.actors)  
    print("Locations:", role.locations)  
    print("Lead:", role.lead())  
    print("Understudy:", role.understudy())  
