from sqlalchemy import create_engine, Column,  Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Session, relationship, DeclarativeBase
import arrow

sqlite_database = 'sqlite:///database.db'

engine = create_engine(sqlite_database, echo=True)

class  Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)

    incomes = relationship('Income', back_populates='user')
    expenses = relationship('Expense', back_populates='user')


class Income(Base):
    __tablename_ = 'incomes'

    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=arrow.now().datetime)
    user_id = Column(Integer, ForeignKey=('users.tg_id'))

    user = relationship('User', back_populates='incomes')

class Expense(Base):
    __tablename_ = 'expenses'

    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=arrow.now().datetime)
    user_id = Column(Integer, ForeignKey=('users.tg_id'))

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
        return users.tg_id

async def add_ex(name, amount, category, tg_id):
    with Session(autoflush=False, bind=engine) as db:
            new_income = Income(name=name, amount=amount, category=category, user_id=tg_id)
            db.add(new_income)
            db.commit()

async def add_in(name, amount, tg_id):
    with Session(autoflush=False, bind=engine) as db:
            new_income = Income(name=name, amount=amount, user_id=tg_id)
            db.add(new_income)
            db.commit()

async def get_ex_or_in_for_mon(type, tg_id):
    with Session(autoflush=False, bind=engine) as db: # get all expenses/incomes for month  
        start_of_month = arrow.now().span("month")[0]
        if type == 'ex':
            exs = db.query(Expense).filter(Expense.user_id == tg_id, Expense.created_at >= start_of_month).all()
            return exs
        elif type == 'in':
            ins = db.query(Income).filter(Income.user_id == tg_id, Income.created_at >= start_of_month).all()
            return ins

async def get_ex_or_in_for_week(type, tg_id):
    with Session(autoflush=False, bind=engine) as db: # get all expenses/incomes for week
        start_of_week = arrow.now().span("week")[0]
        if type == 'ex':
            exs = db.query(Expense).filter(Expense.user_id == tg_id, Expense.created_at >= start_of_week).all()
            return exs
        elif type == 'in':
            ins = db.query(Income).filter(Income.user_id == tg_id, Income.created_at >= start_of_week).all()
            return ins  
        

async def get_ex_or_in_for_year(type, tg_id):
    with Session(autoflush=False, bind=engine) as db: # get all expenses/incomes for year
        start_of_year = arrow.now().span("year")[0]
        if type == 'ex':
            exs = db.query(Expense).filter(Expense.user_id == tg_id, Expense.created_at >= start_of_year).all()
            return exs
        elif type == 'in':
            ins = db.query(Income).filter(Income.user_id == tg_id, Income.created_at >= start_of_year).all()
            return ins  

            
