from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3 # [추가] DB를 사용하기 위한 도구

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- [DB 초기 설정] 서버가 켜질 때 실행됩니다 ---
def init_db():
    conn = sqlite3.connect("database.db") # database.db라는 파일을 만듭니다
    cursor = conn.cursor()
    # users 테이블이 없으면 새로 만듭니다
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db() # 서버 시작 시 DB 준비

class User(BaseModel):
    name: str = None
    email: str
    password: str

@app.post("/signup")
async def signup(user: User):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        # DB에 사용자 정보 넣기
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                       (user.name, user.email, user.password))
        conn.commit()
        conn.close()
        print(f"DB 저장 완료: {user.name}")
        return {"message": "회원가입 성공! 이제 정보가 사라지지 않아요. ✨"}
    except sqlite3.IntegrityError:
        return {"message": "이미 가입된 이메일입니다. 🍎"}

@app.post("/login")
async def login(user: User):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # 이메일과 비밀번호가 일치하는 사람 찾기
    cursor.execute("SELECT name FROM users WHERE email = ? AND password = ?", 
                   (user.email, user.password))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"message": "success", "username": result[0]}
    else:
        return {"message": "fail"}