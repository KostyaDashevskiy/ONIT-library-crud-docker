import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 1. Настройка БД и ORM (Получаем URL из переменных окружения)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@localhost:5432/books_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель ORM
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# 2. Настройка FastAPI и GUI (Jinja2)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD ОПЕРАЦИИ ---

# READ (Отображение GUI)
@app.get("/")
def read_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# CREATE (Добавление)
@app.post("/add")
def add_book(title: str = Form(...), author: str = Form(...), db: Session = Depends(get_db)):
    new_book = Book(title=title, author=author)
    db.add(new_book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# UPDATE (Обновление)
@app.post("/update/{book_id}")
def update_book(book_id: int, title: str = Form(...), author: str = Form(...), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.title = title
        book.author = author
        db.commit()
    return RedirectResponse(url="/", status_code=303)

# DELETE (Удаление)
@app.post("/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

# Healthcheck для Docker (ЛР№2)
@app.get("/health")
def health_check():
    return {"status": "ok"}