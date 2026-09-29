import os

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


def get_classes():
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", "3306")),
    )
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT class_id, name, room, capacity, schedule_time "
            "FROM gym_class ORDER BY class_id"
        )
        return cursor.fetchall()
    finally:
        connection.close()


@app.route("/")
def home():
    try:
        classes = get_classes()
        return render_template("index.html", classes=classes, error=None)
    except Exception:
        return render_template(
            "index.html", classes=[], error="เชื่อมต่อฐานข้อมูลไม่สำเร็จ กรุณาตรวจการตั้งค่าหรือแจ้งผู้ดูแลระบบ"
        ), 500


if __name__ == "__main__":
    app.run(debug=True)
