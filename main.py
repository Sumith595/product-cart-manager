from fastapi import FastAPI,Depends
from models import Product
from database import Session,engine
import database_models
from sqlalchemy.orm import Session as DBSession
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://product-cart-manager-eta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return {"message":"Hello, World!"}

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

# Create tables first
database_models.Base.metadata.create_all(bind=engine)

def init_db():
    db=Session()
    count = db.query(database_models.Product).count()
    
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump(exclude={'id'})))
        db.commit()
    db.close()

init_db()

def db_get():
    db=Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db:DBSession=Depends(db_get)):
    
    db_products=db.query(database_models.Product).all()
    #db=Session()
    #db.query()
    return db_products

@app.get("/products/{id}")
def get_product(id:int,db:DBSession=Depends(db_get)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@app.post("/products")
def add_product(product:Product,db:DBSession=Depends(db_get)):
    db_product = database_models.Product(**product.model_dump(exclude={'id'}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}")
def update_product(id:int, product:Product,db:DBSession=Depends(db_get)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        return {"error": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id:int,db:DBSession=Depends(db_get)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    else:   
        return {"error": "Product not found"}