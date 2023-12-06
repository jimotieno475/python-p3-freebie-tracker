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

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freeble(item_name=item_name, value=value, company=self, dev=dev)
        return new_freebie

    @classmethod
    def oldest_company(cls):
        return cls.query.order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    freebles = relationship('Freeble', backref=backref('dev'))
    companies= relationship('Company', back_populates='devs')
    

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for freebie in self.freebles:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev
            return True
        return False
    
class Freeble(Base):
    __tablename__='freebies'

    id =Column(Integer(), primary_key=True)
    item_name=Column(String())
    value=Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
