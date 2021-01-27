from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:my-secret-pw@mysql-container:3306/test', echo=True) # подключились к mysql

Base = declarative_base()


class Parser(Base):
    __tablename__ = 'parser'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    count = Column(Integer)
    file_name = Column(String(1000))

    def __repr__(self):
        return f'<Parser(name="{self.name}")>'


Base.metadata.create_all(engine)
