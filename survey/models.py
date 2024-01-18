from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import os
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

def get_db():
    engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/hackathon_survey?charset=utf8')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class QuestionType(Base):
    __tablename__ = 'question_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    topic_name = Column(String(255), nullable=False)
    topic_statement = Column(String(255), nullable=False)

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question_type = Column(Integer, ForeignKey('question_type.id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topic.id'), nullable=False)
    name = Column(String(255), nullable=False)

    topic = relationship('Topic', backref='questions')
    question_type_rel = relationship('QuestionType', backref='questions')

class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('question_type.id'), nullable=False)
    name = Column(String(255), nullable=False)

    question_type_rel = relationship('QuestionType', backref='choices')

class Response(Base):
    __tablename__ = 'response'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('choices.id'), nullable=False)

    question = relationship('Question', backref='responses')
    answer = relationship('Choices', backref='responses')

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    name = Column(Integer, nullable=False)
    language_id = Column(Integer, ForeignKey('language.id'), nullable=False)

    language = relationship('Language', backref='users')

