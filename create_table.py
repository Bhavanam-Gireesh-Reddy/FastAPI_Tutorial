from database import engine, Base
import model

Base.metadata.create_all(bind = engine)

print("Table Created Successfully")