from flask import Flask, jsonify, render_template, request
import db

app = Flask(__name__)


def api_call(fn, *args):
    try:
        return jsonify({"ok": True, "data": fn(*args)})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Fitness API request failed")
        return jsonify({"ok": False, "error": f"{type(exc).__name__}: {exc}"}), 500


@app.route("/")
def page_home():
    return render_template("index.html")


@app.route("/report")
def page_report():
    return render_template("report.html")


@app.route("/api/<entity>", methods=["GET", "POST"])
def entity_collection(entity):
    if entity not in db.ENTITIES:
        return jsonify({"ok": False, "error": "ไม่พบเมนูนี้"}), 404
    if request.method == "GET":
        filters = {key: value for key, value in request.args.items() if value}
        return api_call(db.search, entity, filters)
    return api_call(db.create, entity, request.get_json(silent=True) or {})


@app.route("/api/<entity>/<int:row_id>", methods=["GET", "PUT", "DELETE"])
def entity_item(entity, row_id):
    if entity not in db.ENTITIES:
        return jsonify({"ok": False, "error": "ไม่พบเมนูนี้"}), 404
    if request.method == "GET":
        return api_call(db.get_one, entity, row_id)
    if request.method == "PUT":
        return api_call(db.update, entity, row_id, request.get_json(silent=True) or {})
    return api_call(db.delete, entity, row_id)


@app.route("/api/options")
def options():
    return api_call(db.form_options)


@app.route("/api/reports/summary")
def report_summary():
    return api_call(db.report_summary)


@app.route("/api/reports/popular-classes")
def report_popular_classes():
    return api_call(db.report_popular_classes)


@app.route("/api/reports/booking-status")
def report_booking_status():
    return api_call(db.report_booking_status)


if __name__ == "__main__":
    app.run(debug=True)

