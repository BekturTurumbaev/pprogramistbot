"""The module is responsible for tables and relations betweeen them inside of the database."""
# Standard library imports
import datetime

# Third party imports
from sqlalchemy import (
    Column, ForeignKey,
    Integer, String, TIMESTAMP,
    SmallInteger, BigInteger, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import insert

# Local application imports
from database.settings import engine


Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        # It is forbidden to leave just -> datetime.datetime.now convert it to str first!
        server_default=str(datetime.datetime.now()),
        comment='The date an object has been created'
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=str(datetime.datetime.now()),
        onupdate=datetime.datetime.now,
        comment='The date an object has been updated'
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Reception(BaseModel):
    __tablename__ = 'reception'

    apply = Column(
        Integer,
        nullable=False,
        comment='How much times the APPLY button has been pressed',
        default=1
    )

    about_courses = Column(
        BigInteger,
        nullable=False,
        comment='How much times the ABOUT_COURSES button has been pressed',
        default=1
    )

    about_company = Column(
        Integer,
        nullable=False,
        comment='How much times the ABOUT_COMPANY button has been pressed',
        default=1
    )

    vacancies = Column(
        BigInteger,
        nullable=False,
        comment='How much times the VACANCIES button has been pressed',
        default=1
    )

    news = Column(
        Integer,
        nullable=False,
        comment='How much times the NEWS button has been pressed',
        default=1
    )


    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Department(BaseModel):
    __tablename__ = 'department'

    department_name = Column(
        String,
        nullable=False,
        unique=True,
        comment='Programming language name'
    )

    customers = relationship('Customer', back_populates='department')
    courses = relationship('Course', back_populates='department')
    vacancies = relationship('Vacancy', back_populates='department')
    news = relationship('News', back_populates='department')

    def __repr__(self):
        return self.department_name



class Customer(BaseModel):
    __tablename__ = 'customer'

    chat_id = Column(
        Integer,
        nullable=False,
        comment='The chat id of User who applied for registration'
    )

    first_name = Column(
        String,
        nullable=False,
        comment='How much times the apply button has been pressed'
    )

    last_name = Column(
        String,
        nullable=True,
        comment='How much times the apply button has been pressed'
    )

    phone = Column(
        BigInteger,
        nullable=True,
        comment='How much times the apply button has been pressed'
    )

    time = Column(
        SmallInteger,
        nullable=True,
        comment='The time when a group start to study. Morning or Evening'
    )

    department_name = Column(
        String, 
        ForeignKey('department.department_name')
    )

    department = relationship(
        "Department", 
        back_populates="customers"
    )

    def __repr__(self):
        return f'{self.department_name} | {self.first_name} | {self.last_name}'


class Course(BaseModel):
    __tablename__ = 'course'

    department_id = Column(
        Integer, 
        ForeignKey('department.id')
    )

    department = relationship(
        "Department", 
        back_populates="courses"
    )

    department_info = Column(
        Text,
        nullable=False,
        comment='The information about course'
    )

    def __repr__(self):
        return f'{self.department}'


class Vacancy(BaseModel):
    __tablename__ = 'vacancy'

    vacancy_type = Column(
        SmallInteger,
        nullable=False,
        comment='If VACANCY_TYPE = 1 it means that vacancy provided by P-Programist, otherwise the vacancy provided by another resource'
    )

    department_id = Column(
        Integer, 
        ForeignKey('department.id')
    )

    department = relationship(
        "Department", 
        back_populates="vacancies"
    )

    vacancy_label = Column(
        String,
        nullable=False,
        comment='The header of vacancy'
    )

    vacancy_info = Column(
        Text,
        nullable=False,
        comment='These are the details of vacancy'
    )

    def __repr__(self):
        return f'{self.department.department_name} - {self.vacancy_label}'


class News(BaseModel):
    __tablename__ = 'news'

    department_id = Column(
        Integer, 
        ForeignKey('department.id')
    )

    department = relationship(
        "Department", 
        back_populates="news"
    )

    news_source = Column(
        String,
        nullable=False,
        comment='The source where the statistic has been taken from'
    )

    news_label = Column(
        String,
        nullable=False,
        comment='The header of an article'
    )

    def __repr__(self):
        return f'{self.department.department_name} - {self.news_label}'


if __name__ == "__main__":
    import asyncio
    from sqlalchemy.ext.asyncio import AsyncSession

    async def recreate_database():
        '''
            When you want to set a connection with the database,
            You have to call the .begin() method from engine.
            After this method initialized You will get asynchronous connection with database.
        '''
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)


        async with AsyncSession(engine, expire_on_commit=False) as session:
            async with session.begin():
                python = Department(id=1, department_name='Python')
                sys_admin = Department(id=2, department_name='System Administrator')
                javascript = Department(id=3, department_name='Javascript')
                java = Department(id=4, department_name='Java')

                session.add_all(
                    [
                        python,
                        sys_admin,
                        javascript,
                        java
                    ]
                )
            python_info = insert(Course).values(
                {
                    "department_info": '''*Длительность:* 4️⃣ месяца
*Стоимость:* 150$ / за месяц 🤏
*Программа обучения:* 
    Месяц 1: *Английский + Математика + Linux*
    Месяц 2: *Знакомство с синтаксисом языка Python*
    Месяц 3: *Углубленное изучения языка + Базы Данных*
    Месяц 4: *Изучения фрэймворка Django*
    
*Дополнительная информация:*
    Во время изучения языка программирования(ЯП) Python вы также получаете:
    1. Изучение необходимых библиотек относящихся к ЯП Python 😱😱😱
    2. Изучение нескольких Баз Данных 🧐
    3. Возможность научиться создавать Telegram боты 🤖
    4. Изучить вёрстку на HTML+CSS 👩‍🎤🧑‍🎤
    5. Возможность работать на оплачиваемых проектах 🤑
    6. Участие в локальных Хакатонах 🏆
    7. Коворкинг и новые знакомства 🧍‍♀️🧍🐼🦉👽
    8. Многое многое другое... 🤤😍🤩

''',
                "department_id": python.id
                    }
            )
            sys_admin = insert(Course).values(
                {
                    "department_info": '''*Длительность:* 4️⃣ месяца
*Стоимость:* 140$ / за месяц 🤏
*Программа обучения:* 
    Месяц 1: *Английский + Математика + Linux*
    Месяц 2: *Знакомство с синтаксисом языка Python*
    Месяц 3: *Углубленное изучения языка + Базы Данных*
    Месяц 4: *Изучения фрэймворка Django*
    
*Дополнительная информация:*
    Во время изучения языка программирования(ЯП) Python вы также получаете:
    1. Изучение необходимых библиотек относящихся к ЯП Python 😱😱😱
    2. Изучение нескольких Баз Данных 🧐
    3. Возможность научиться создавать Telegram боты 🤖
    4. Изучить вёрстку на HTML+CSS 👩‍🎤🧑‍🎤
    5. Возможность работать на оплачиваемых проектах 🤑
    6. Участие в локальных Хакатонах 🏆
    7. Коворкинг и новые знакомства 🧍‍♀️🧍🐼🦉👽
    8. Многое многое другое... 🤤😍🤩

''',
                "department_id": sys_admin.id
                    }
            )
            await session.execute(python_info)
            await session.commit()

    asyncio.run(recreate_database())