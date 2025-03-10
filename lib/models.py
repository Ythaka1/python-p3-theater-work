from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer(), primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer(), ForeignKey('roles.id')) 
    
    role = relationship('Role', backref=backref('auditions', lazy='joined', cascade="all, delete"))

    def call_back(self):
        self.hired = True
    
class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer(), primary_key=True)
    character_name = Column(String, nullable=False, unique=True)     
    
    @property
    def actors(self): 
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        return self.auditions.filter_by(hired=True).first() or "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = self.auditions.filter_by(hired=True).limit(2).all()
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"