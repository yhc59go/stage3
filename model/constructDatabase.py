from communicateWithRDS import communicateWithRDS
from dotenv import load_dotenv
import os

load_dotenv()
databaseName=os.getenv("databaseName")
pool_name=os.getenv("pool_name")

#Construct messageBoard tabel
databasePoolInstance=communicateWithRDS(databaseName,pool_name)
databasePoolInstance.createTabel_messageBoard()
		