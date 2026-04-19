from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD

DATABASE_URL = "postgresql://postgres:anwesha2627@localhost/disaster_db"




engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
=======
DATABASE_URL = "postgresql://postgres:24beeg06@localhost/disaster_db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> origin/front-end

Base = declarative_base()