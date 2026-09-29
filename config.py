# config.py — การตั้งค่าการเชื่อมต่อฐานข้อมูลฟิตเนส
# ใส่ค่าจริงไว้ในไฟล์ .env ซึ่งถูกกันไม่ให้ส่งขึ้น GitHub
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

if not all((DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)):
    raise RuntimeError("กรุณาตั้ง DB_HOST, DB_USER, DB_PASSWORD และ DB_NAME ในไฟล์ .env")
