import mysql.connector
import config

DB_FIELDS = {
    "members": {
        "table": "member", "id": "member_id",
        "fields": ["name", "gender", "phone", "email", "join_date", "package_type"],
        "required": ["name", "join_date"],
        "select": "SELECT member_id, name, gender, phone, email, join_date, package_type FROM member",
        "order": "member_id",
    },
    "trainers": {
        "table": "trainer", "id": "trainer_id",
        "fields": ["name", "specialty", "phone", "mentor_trainer_id"],
        "required": ["name"],
        "select": "SELECT trainer_id, name, specialty, phone, mentor_trainer_id FROM trainer",
        "order": "trainer_id",
    },
    "classes": {
        "table": "gym_class", "id": "class_id",
        "fields": ["trainer_id", "name", "room", "capacity", "schedule_time"],
        "required": ["trainer_id", "name", "capacity", "schedule_time"],
        "select": "SELECT c.class_id, c.trainer_id, c.name, t.name AS trainer_name, c.room, c.capacity, c.schedule_time FROM gym_class c LEFT JOIN trainer t ON t.trainer_id=c.trainer_id",
        "order": "c.class_id",
    },
    "bookings": {
        "table": "booking", "id": "booking_id",
        "fields": ["member_id", "class_id", "book_date", "status"],
        "required": ["member_id", "class_id", "book_date", "status"],
        "select": "SELECT b.booking_id, b.member_id, m.name AS member_name, b.class_id, c.name AS class_name, b.book_date, b.status FROM booking b LEFT JOIN member m ON m.member_id=b.member_id LEFT JOIN gym_class c ON c.class_id=b.class_id",
        "order": "b.booking_id",
    },
    "equipment": {
        "table": "equipment", "id": "equip_id",
        "fields": ["name", "zone", "status", "total_quantity"],
        "required": ["name", "status", "total_quantity"],
        "select": "SELECT equip_id, name, zone, status, total_quantity FROM equipment",
        "order": "equip_id",
    },
}

ENTITIES = {
    "members": {"label": "สมาชิก", "idKey": "member_id", "api": "/api/members", "search": [{"key":"q","label":"ชื่อ / เบอร์โทร / อีเมล","type":"text"}], "form": [
        {"key":"name","label":"ชื่อสมาชิก","type":"text","required":True}, {"key":"gender","label":"เพศ","type":"select","options":["Male","Female","Other"]}, {"key":"phone","label":"โทรศัพท์","type":"text"}, {"key":"email","label":"อีเมล","type":"email"}, {"key":"join_date","label":"วันที่สมัคร","type":"date","required":True}, {"key":"package_type","label":"แพ็กเกจ","type":"text"}]},
    "trainers": {"label": "เทรนเนอร์", "idKey": "trainer_id", "api": "/api/trainers", "search": [{"key":"q","label":"ชื่อ / ความเชี่ยวชาญ / โทรศัพท์","type":"text"}], "form": [
        {"key":"name","label":"ชื่อเทรนเนอร์","type":"text","required":True}, {"key":"specialty","label":"ความเชี่ยวชาญ","type":"text"}, {"key":"phone","label":"โทรศัพท์","type":"text"}, {"key":"mentor_trainer_id","label":"รหัสเทรนเนอร์พี่เลี้ยง (เว้นว่างได้)","type":"number"}]},
    "classes": {"label": "คลาสฟิตเนส", "idKey": "class_id", "api": "/api/classes", "search": [{"key":"q","label":"ชื่อคลาส / ห้อง / เทรนเนอร์","type":"text"}], "form": [
        {"key":"trainer_id","label":"รหัสเทรนเนอร์","type":"number","required":True}, {"key":"name","label":"ชื่อคลาส","type":"text","required":True}, {"key":"room","label":"ห้อง","type":"text"}, {"key":"capacity","label":"จำนวนรับ","type":"number","required":True}, {"key":"schedule_time","label":"วันและเวลา","type":"datetime-local","required":True}]},
    "bookings": {"label": "การจอง", "idKey": "booking_id", "api": "/api/bookings", "search": [{"key":"q","label":"ชื่อสมาชิก / คลาส / สถานะ","type":"text"}], "form": [
        {"key":"member_id","label":"รหัสสมาชิก","type":"number","required":True}, {"key":"class_id","label":"รหัสคลาส","type":"number","required":True}, {"key":"book_date","label":"วันและเวลาที่จอง","type":"datetime-local","required":True}, {"key":"status","label":"สถานะ","type":"select","options":["CONFIRMED","CANCELLED"],"required":True}]},
    "equipment": {"label": "อุปกรณ์", "idKey": "equip_id", "api": "/api/equipment", "search": [{"key":"q","label":"ชื่ออุปกรณ์ / โซน / สถานะ","type":"text"}], "form": [
        {"key":"name","label":"ชื่ออุปกรณ์","type":"text","required":True}, {"key":"zone","label":"โซน","type":"text"}, {"key":"status","label":"สถานะ","type":"text","required":True}, {"key":"total_quantity","label":"จำนวน","type":"number","required":True}]},
}


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT,
    )


def run(sql, params=(), write=False):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        if write:
            conn.commit()
            return {"new_id": cur.lastrowid, "affected": cur.rowcount}
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def _config(entity):
    if entity not in DB_FIELDS:
        raise ValueError("ไม่พบชนิดข้อมูล")
    return DB_FIELDS[entity]


def search(entity, filters):
    cfg = _config(entity)
    sql = cfg["select"]
    params = []
    query = (filters.get("q") or "").strip()
    if query:
        searchable = {
            "members": ["name", "gender", "phone", "email", "package_type"],
            "trainers": ["name", "specialty", "phone"],
            "classes": ["c.name", "c.room", "t.name"],
            "bookings": ["m.name", "c.name", "b.status"],
            "equipment": ["name", "zone", "status"],
        }[entity]
        sql += " WHERE " + " OR ".join(f"CAST({col} AS CHAR) LIKE %s" for col in searchable)
        params.extend([f"%{query}%"] * len(searchable))
    sql += " ORDER BY " + cfg["order"]
    return run(sql, params)


def get_one(entity, row_id):
    cfg = _config(entity)
    rows = run(f"SELECT * FROM {cfg['table']} WHERE {cfg['id']}=%s", (row_id,))
    if not rows:
        raise ValueError("ไม่พบข้อมูลรายการนี้")
    return rows[0]


def _clean_data(entity, data):
    cfg = _config(entity)
    cleaned = {field: data.get(field) for field in cfg["fields"] if field in data}
    for key, value in list(cleaned.items()):
        if value == "":
            cleaned[key] = None
    missing = [field for field in cfg["required"] if not cleaned.get(field)]
    if missing:
        raise ValueError("กรุณากรอกข้อมูลที่จำเป็นให้ครบ")
    return cleaned


def create(entity, data):
    cfg = _config(entity)
    values = _clean_data(entity, data)
    if not values:
        raise ValueError("ไม่มีข้อมูลสำหรับบันทึก")
    fields = list(values)
    sql = f"INSERT INTO {cfg['table']} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
    return run(sql, [values[field] for field in fields], write=True)


def update(entity, row_id, data):
    cfg = _config(entity)
    values = _clean_data(entity, data)
    if not values:
        raise ValueError("ไม่มีข้อมูลสำหรับแก้ไข")
    fields = list(values)
    sql = f"UPDATE {cfg['table']} SET " + ", ".join(f"{field}=%s" for field in fields) + f" WHERE {cfg['id']}=%s"
    return run(sql, [values[field] for field in fields] + [row_id], write=True)


def delete(entity, row_id):
    cfg = _config(entity)
    return run(f"DELETE FROM {cfg['table']} WHERE {cfg['id']}=%s", (row_id,), write=True)


def form_options():
    return {
        "members": run("SELECT member_id, name FROM member ORDER BY name"),
        "trainers": run("SELECT trainer_id, name FROM trainer ORDER BY name"),
        "classes": run("SELECT class_id, name FROM gym_class ORDER BY name"),
    }


def report_summary():
    rows = run("SELECT (SELECT COUNT(*) FROM member) AS members, (SELECT COUNT(*) FROM trainer) AS trainers, (SELECT COUNT(*) FROM gym_class) AS classes, (SELECT COUNT(*) FROM booking) AS bookings, (SELECT COUNT(*) FROM equipment) AS equipment")
    return rows[0]


def report_popular_classes():
    return run("SELECT c.name AS class_name, COUNT(b.booking_id) AS booking_count FROM gym_class c LEFT JOIN booking b ON b.class_id=c.class_id GROUP BY c.class_id, c.name ORDER BY booking_count DESC, c.name LIMIT 10")


def report_booking_status():
    return run("SELECT status, COUNT(*) AS booking_count FROM booking GROUP BY status ORDER BY status")


