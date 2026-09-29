import os

import mysql.connector
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    try:
        connection = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            port=int(os.environ.get("DB_PORT", "3306")),
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT class_id, name, room, capacity, schedule_time "
            "FROM gym_class ORDER BY class_id"
        )
        classes = cursor.fetchall()

        cursor.close()
        connection.close()

        rows = "".join(
            f"<tr><td>{item['class_id']}</td><td>{item['name']}</td>"
            f"<td>{item['room']}</td><td>{item['capacity']}</td>"
            f"<td>{item['schedule_time']}</td></tr>"
            for item in classes
        )

        return (
            "<h1>คลาสฟิตเนส</h1>"
            "<table border='1' cellpadding='8'>"
            "<tr><th>รหัส</th><th>ชื่อคลาส</th><th>ห้อง</th>"
            "<th>จำนวนคน</th><th>เวลา</th></tr>"
            f"{rows}</table>"
        )

    except Exception as error:
        return f"เชื่อมต่อฐานข้อมูลไม่สำเร็จ: {error}", 500


if __name__ == "__main__":
    app.run(debug=True)