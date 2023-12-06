from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    freebles = relationship('Freeble', backref=backref('company'))
    devs= relationship('Dev', back_populates='companies')
    

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    freebles = relationship('Freeble', backref=backref('dev'))
    companies= relationship('Company', back_populates='devs')
    

    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freeble(Base):
    __tablename__='freebies'

    id =Column(Integer(), primary_key=True)
    item_name=Column(String())
    value=Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

