from sqlalchemy import create_engine, Column,  Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Session, relationship, DeclarativeBase
import arrow

sqlite_database = 'sqlite:///database.db'

engine = create_engine(sqlite_database)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)

    incomes = relationship('Income', back_populates='user')
    expenses = relationship('Expense', back_populates='user')


class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=arrow.now().datetime)
    user_id = Column(Integer, ForeignKey('users.tg_id'))

    user = relationship('User', back_populates='incomes')

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=arrow.now().datetime)
    user_id = Column(Integer, ForeignKey('users.tg_id'))

    user = relationship('User', back_populates='expenses')


async def add_user(tg_id):
    with Session(autoflush=False, bind=engine) as db: # add user if not exists
        user = db.query(User).filter(User.tg_id == tg_id).first()
        if user:
            return user
        else:
            user = User(tg_id=tg_id)
            db.add(user)    
            db.commit()

async def get_users():
    with Session(autoflush=False, bind=engine) as db: # get all users
        users = db.query(User).all()
        users_id = []
        for user in users:
            users_id.append(user.tg_id)
        return users_id
    
async def add_ex(name, amount, category, tg_id):
    with Session(autoflush=False, bind=engine) as db:
            new_expense = Expense(name=name, amount=amount, category=category, user_id=tg_id)
            db.add(new_expense)
            db.commit()

async def add_in(name, amount, tg_id):
    with Session(autoflush=False, bind=engine) as db:
            new_income = Income(name=name, amount=amount, user_id=tg_id)
            db.add(new_income)
            db.commit()
            
async def get_incomes_by_term(type, tg_id):
    with Session(autoflush=False, bind=engine) as db:
        term = arrow.now().span(type)[0].datetime  # Convert arrow to datetime here
        ins = db.query(Income).filter(Income.user_id == tg_id, Income.created_at >= term).all()
        return ins

async def get_expenses_by_term(type,tg_id):
    with Session(autoflush=False, bind=engine) as db:
        term = arrow.now().span(type)[0].datetime
        exs = db.query(Expense).filter(Expense.user_id == tg_id, Expense.created_at >= term).all()
        return exs