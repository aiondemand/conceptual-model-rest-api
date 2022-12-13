from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@172.17.0.3:3306/mydb"
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


@app.get("/")
def read_root():
    return {"message":"hello world"}