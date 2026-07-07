
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS


from scheduler import (
    build_conflict_map,
    greedy_schedule,
    assign_halls,
    ALL_STUDENTS,
    CSE_SUBJECTS,
    BIOTECH_SUBJECTS,
    CSE_STUDENTS,
    BIO_STUDENTS,
)

app = Flask(__name__, static_folder=".")
CORS(app)

print("Running greedy algorithm...")
_conflict_map = build_conflict_map(ALL_STUDENTS)
_schedule     = greedy_schedule(_conflict_map)
_halls        = assign_halls(_schedule, _conflict_map)
print(f"Done — {max(_schedule.keys())} days, {len(_halls)} hall slots.")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/schedule")
def get_schedule():
    return jsonify({
        "total_days":     max(_schedule.keys()),
        "total_students": len(ALL_STUDENTS),
        "cse_subjects":   CSE_SUBJECTS,
        "bio_subjects":   BIOTECH_SUBJECTS,
        "schedule":       {str(k): v for k, v in _schedule.items()},
        "halls":          _halls,
    })



@app.route("/api/student/<reg_no>")
def get_student(reg_no):
    raw = reg_no.strip()
    if raw.upper().endswith("BIO"):
        reg = raw[:-3] + "Bio"
    elif raw.upper().endswith("CS"):
        reg = raw[:-2] + "CS"
    else:
        reg = raw

    for hall in _halls:
        if reg in hall["cse_students"]:
            return jsonify({
                "reg_no": reg, "stream": "CSE",
                "exam": hall["cse_exam"],
               "hall": hall["hall"],
            })
        if reg in hall["bio_students"]:
            return jsonify({
                "reg_no": reg, "stream": "Biotech",
                "exam": hall["bio_exam"],
             "hall": hall["hall"],
            })

    return jsonify({"error": f"Student '{reg_no}' not found"}), 404

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Exam Scheduler running!")
    print("  Visit: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
