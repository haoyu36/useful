from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = 'mysql+pymysql://web:123456@localhost/xxx'


DeclarativeBase = declarative_base()
engine = create_engine(DB_URL)


class Question(DeclarativeBase):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    title = Column(String(100))
    url = Column(String(100))
    answer_count = Column(Integer)
    follower_count = Column(Integer)


class Answer(DeclarativeBase):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer)
    content = Column(Text)
    url = Column(String(100))
    voteup_count = Column(Integer)


class QuestionAnswer(DeclarativeBase):
    __tablename__ = 'questionanswer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    answer_id = Column(Integer)



session = sessionmaker(bind=engine)()


def create_question(**kw):
    item = Question(**kw)
    try:
        session.add(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    return item


def create_answer(**kw):
    item = Answer(**kw)
    try:
        session.add(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    return item

def create_question_answer(**kw):
    item = QuestionAnswer(**kw)
    try:
        session.add(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    return item


if __name__ == '__main__':
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)


