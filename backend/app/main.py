from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas, auth
from app.database import SessionLocal, engine

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 token reader
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ------------------------
# Database Session Dependency
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# Current User (JWT Decode)
# ------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ------------------------
# User Registration
# ------------------------
@app.post("/api/auth/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username
    }



# ------------------------
# User Login
# ------------------------
@app.post("/api/auth/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth.create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}


# ------------------------
# Create Sweet
# ------------------------
@app.post("/api/sweets")
def create_sweet(
    data: schemas.SweetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = models.Sweet(
        name=data.name,
        category=data.category,
        price=data.price,
        quantity=data.quantity,
    )

    db.add(sweet)
    db.commit()
    db.refresh(sweet)

    return sweet


# ------------------------
# List All Sweets
# ------------------------
@app.get("/api/sweets")
def list_sweets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Sweet).all()


# ------------------------
# Search Sweets
# ------------------------
@app.get("/api/sweets/search")
def search_sweets(
    name: str = "",
    category: str = "",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(models.Sweet)

    if name:
        query = query.filter(models.Sweet.name.contains(name))
    if category:
        query = query.filter(models.Sweet.category.contains(category))

    return query.all()


# ------------------------
# Update Sweet
# ------------------------
@app.put("/api/sweets/{sweet_id}")
def update_sweet(
    sweet_id: int,
    data: schemas.SweetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.name = data.name
    sweet.category = data.category
    sweet.price = data.price
    sweet.quantity = data.quantity

    db.commit()
    return sweet


# ------------------------
# Delete Sweet (Admin only)
# ------------------------
@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(
    sweet_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(sweet)
    db.commit()

    return {"message": "Sweet deleted"}


# ------------------------
# Purchase Sweet
# ------------------------
@app.post("/api/sweets/{sweet_id}/purchase")
def buy_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Not found")

    if sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    sweet.quantity -= 1
    db.commit()

    return sweet


# ------------------------
# Restock Sweet (Admin only)
# ------------------------
@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    amount: int = 1,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

    if not sweet:
        raise HTTPException(status_code=404, detail="Not found")

    sweet.quantity += amount
    db.commit()

    return sweet
