

CSE_SUBJECTS = [
    "Data Structures",
    "Algorithms",
    "Operating Systems",
    "Database Management",
    "Computer Networks",
    "Software Engineering",
    "Theory of Computation",
]

BIOTECH_SUBJECTS = [
    "Genetics",
    "Biochemistry",
    "Microbiology",
    "Cell Biology",
    "Molecular Biology",
    "Bioinformatics",
    "Immunology",
]

NUM_CLASSES = 10
STUDENTS_PER_CLASS = 50


def generate_students(stream_prefix: str, subjects: list) -> dict:
    students = {}
    total = NUM_CLASSES * STUDENTS_PER_CLASS
    for i in range(1, total + 1):
        reg = f"{i}{stream_prefix}"
        students[reg] = list(subjects)
    return students


CSE_STUDENTS = generate_students("CS", CSE_SUBJECTS)
BIO_STUDENTS = generate_students("Bio", BIOTECH_SUBJECTS)
ALL_STUDENTS = {**CSE_STUDENTS, **BIO_STUDENTS}


def build_conflict_map(students: dict) -> dict:
    conflict_map = {}
    for reg, subjects in students.items():
        for subj in subjects:
            conflict_map.setdefault(subj, set()).add(reg)
    return conflict_map


def greedy_schedule(conflict_map: dict) -> dict:
    exams_sorted = sorted(conflict_map.keys(),
                          key=lambda e: len(conflict_map[e]),
                          reverse=True)

    schedule = {}
    student_day_map = {}

    for exam in exams_sorted:
        students_in_exam = conflict_map[exam]

        blocked_days = set()
        for reg in students_in_exam:
            blocked_days |= student_day_map.get(reg, set())

        # max 1 exam per stream per day
        stream = "CS" if exam in CSE_SUBJECTS else "Bio"
        for day, day_exams in schedule.items():
            for assigned in day_exams:
                assigned_stream = "CS" if assigned in CSE_SUBJECTS else "Bio"
                if assigned_stream == stream:
                    blocked_days.add(day)

        # GREEDY CHOICE: first available day
        day = 1
        while day in blocked_days:
            day += 1

        schedule.setdefault(day, []).append(exam)
        for reg in students_in_exam:
            student_day_map.setdefault(reg, set()).add(day)

    return schedule


def assign_halls(schedule: dict, conflict_map: dict) -> list:
    halls = []
    for day in sorted(schedule.keys()):
        day_exams = schedule[day]
        cse_exams = [e for e in day_exams if e in CSE_SUBJECTS]
        bio_exams = [e for e in day_exams if e in BIOTECH_SUBJECTS]

        for cse_exam in cse_exams:
            cse_regs = sorted(conflict_map[cse_exam],
                              key=lambda r: int(r.replace("CS", "")))
            bio_exam = bio_exams[0] if bio_exams else None
            bio_regs = (sorted(conflict_map[bio_exam],
                               key=lambda r: int(r.replace("Bio", "")))
                        if bio_exam else [])

            cse_batches = [cse_regs[i:i+25] for i in range(0, len(cse_regs), 25)]
            bio_batches = [bio_regs[i:i+25] for i in range(0, len(bio_regs), 25)]

            hall_no = 1
            for cse_batch, bio_batch in zip(cse_batches, bio_batches):
                halls.append({
                    "day": day,
                    "hall": hall_no,
                    "cse_exam": cse_exam,
                    "bio_exam": bio_exam,
                    "cse_students": cse_batch,
                    "bio_students": bio_batch,
                    "total_students": len(cse_batch) + len(bio_batch),
                })
                hall_no += 1

    return halls
