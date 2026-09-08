from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.db.database import get_db_connection
from api.v1.routes import auth
from api.v1.routes import posts

# from api.core.exception_handlers import (
#     http_exception_handler,
#     validation_exception_handler,
#     general_exception_handler
# )

from api.core.error_exception import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)


app = FastAPI()


# -------------------------
# Exception Handlers
# -------------------------

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home_page():

    return {
        "message": "Welcome to my API application"
    }


# -------------------------
# Routers
# -------------------------

app.include_router(auth.router)
app.include_router(posts.router)


# -------------------------
# Database
# -------------------------

def create_table():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create database table
create_table()