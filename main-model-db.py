from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()

# Definición del modelo
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(Text)
    rating = Column(Integer)

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)

# Definición de modelos Pydantic para entrada y salida
class ReviewCreate(BaseModel):
    title: str
    text: str
    rating: int

class ReviewUpdate(BaseModel):
    title: str
    text: str
    rating: int

class ReviewOut(BaseModel):
    id: int
    title: str
    text: str
    rating: int

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    return db

# Inicializa la aplicación FastAPI
app = FastAPI()

# Ruta para obtener todas las reseñas
@app.get("/reviews/", response_model=list[ReviewOut])
async def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = db.query(Review).offset(skip).limit(limit).all()
    return reviews

# Ruta para crear una reseña
@app.post("/reviews/", response_model=ReviewOut)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Ruta para obtener una reseña por ID
@app.get("/reviews/{review_id}", response_model=ReviewOut)
async def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

# Ruta para actualizar una reseña por ID
@app.put("/reviews/{review_id}", response_model=ReviewOut)
async def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db_review.title = review.title
    db_review.text = review.text
    db_review.rating = review.rating
    db.commit()
    return db_review

# Ruta para eliminar una reseña por ID
@app.delete("/reviews/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted"}