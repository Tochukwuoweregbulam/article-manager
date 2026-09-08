from api.core.security import verify_password, pwd_context
from api.db.database import users_db, get_db_connection


def register_user(username: str, password: str, role: str = "user"):
    """Register a new user"""
    
    # Validate username
    if not username or len(username) < 3:
        return {
            "success": False,
            "message": "Username must be at least 3 characters long"
        }
    
    # Validate password
    if not password or len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters long"
        }
    
    # Validate password max length (bcrypt limit)
    if len(password) > 72:
        return {
            "success": False,
            "message": "Password must be less than 72 characters long"
        }
    
    # Check if user already exists in memory
    if username in users_db:
        return {
            "success": False,
            "message": "Username already exists"
        }
    
    # Hash password
    hashed_password = pwd_context.hash(password)
    
    # Save to SQLite database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        return {
            "success": False,
            "message": f"Database error: {str(e)}"
        }
    
    # Also store in memory for quick access
    user = {
        "username": username,
        "password": hashed_password,
        "role": role
    }
    
    users_db[username] = user
    
    return {
        "success": True,
        "message": "User registered successfully",
        "user": {
            "username": user["username"],
            "role": user["role"]
        }
    }


def authenticate_user(username: str, password: str):
    """Authenticate user with username and password"""

    # First check memory
    user = users_db.get(username)
    
    # If not in memory, check database
    if not user:
        try:
            conn = get_db_connection()
            result = conn.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            conn.close()
            
            if result:
                user = {
                    "username": result[0],
                    "password": result[1],
                    "role": result[2]
                }
                # Cache in memory
                users_db[username] = user
        except:
            return False
    
    if not user:
        return False

    if not verify_password(password, user["password"]):
        return False

    return user