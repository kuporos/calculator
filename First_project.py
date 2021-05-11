# Создать таблицу Учебной группы с помощью sqlalchemy.
#
# Создать таблицу Студент с помощью sqlalchemy.
# Студент должен быть связан с Учебной группой.
#
# Создать произвольное кол-во групп и добавить в них студентов.
#
# Создать таблицу журнала посещаемости с помощью sqlalchemy.
# В журнале ведется информация по: дате занятия, группе, студенту и статусу: присутствовал / не присутствовал.
#
# Получить кол-во присутствующих и отстутствующих студентов каждой группы за определенную дату.
# Получить кол-во присутствующих и отстутствующих студентов каждой группы за каждую дату занятия.
#
# Создать таблицу Книга с помощью sqlalchemy. Книга может быть взята в чтение несколькими студентами
# в разные промежутки времени.
# Создать таблицу со связью многие ко многим чтобы в зависимости от времени каждый студент мог взять в
# пользование книгу.
#
# Создать 5 книг. Получить всех студентов и добавить каждому студенту эти пять книг.
from sqlalchemy import create_engine, func
from sqlalchemy import Integer,Column,String,ForeignKey, Table
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import declarative_base, relationship,sessionmaker,backref

DB_USER = 'postgres'
DB_PASSWORD = '1111'
DB_NAME = 'students_dtabase'
DB_ECHO = True

engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}',
    echo=True
)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

class Study_Group(Base):
    __tablename__ = 'study_group'

    id = Column(Integer, primary_key=True)
    name = Column(Integer,unique=True)

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)

    study_group_id = Column(Integer, ForeignKey('study_group.id'))
    study_group = relationship("Study_Group", backref="student_study_group")

class Attendance_Log(Base):
    __tablename__ = 'attendance_log'

    id = Column(Integer,primary_key=True)
    date_of_class = Column(String)
    status = Column(Integer)

    study_group_id = Column(Integer, ForeignKey('study_group.id'))
    study_group = relationship("Study_Group", backref="attendance_log_study_group", lazy = "joined")

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", backref="attendance_log_student", lazy = "joined")

association_table = Table(
    'association', Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column (String)
    student = relationship ('Student', secondary=association_table, backref="book_student")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
#Получить кол-во присутствующих и отстутствующих студентов каждой группы за определенную дату.
# hm_students_one_day = session.query(Attendance_Log).filter(Attendance_Log.date_of_class == "02.05.2021").all()
# for students in hm_students_one_day:
#     print(f"Date: {students.date_of_class} Student: {students.student_id, students.student.name, students.student.surname, students.study_group.name} Status:{students.status}")

# Получить кол-во присутствующих и отстутствующих студентов каждой группы за каждую дату занятия.
hm_students_all_days = session.query(Attendance_Log.date_of_class, Attendance_Log.study_group_id, Attendance_Log.status, func.count(Attendance_Log.status)).group_by(Attendance_Log.date_of_class,Attendance_Log.study_group_id, Attendance_Log.status).all()
for a in sorted(hm_students_all_days):
    print(f" Date: {a.date_of_class} Group: {a.study_group_id} Status: {a.status} Count: {a[-1]}")

# Создать таблицу Книга с помощью sqlalchemy. Книга может быть взята в чтение несколькими студентами
# в разные промежутки времени.
# Создать таблицу со связью многие ко многим чтобы в зависимости от времени каждый студент мог взять в
# пользование книгу.
# Создать 5 книг. Получить всех студентов и добавить каждому студенту эти пять книг.

books_and_students= session.query(Book.title).join(association_table)
books_and_students2= session.query(Student.name).join(association_table)

students = session.query(Student).all()
for student in students:
    books = student.book_student
    for book in books:
        print(book.title)

