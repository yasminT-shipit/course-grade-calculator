import os
import matplotlib.pyplot as plt


def main():
    # === FIX PATHS - THIS IS CRITICAL ===
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    # Verify data structure
    print(f"Looking for data in: {data_dir}")
    if not os.path.exists(data_dir):
        print(f"ERROR: Data folder not found at {data_dir}")
        return

    # === DATA LOADING SECTION ===
    # 1. Load students data
    students = {}  # student_id -> name
    name_to_id = {}  # name -> student_id
    students_path = os.path.join(data_dir, "students.txt")
    if not os.path.exists(students_path):
        print(f"ERROR: students.txt not found at {students_path}")
        return
    with open(students_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id = line[-3:]  # Last 3 characters = ID
            name = line[:-3].strip()
            students[student_id] = name
            name_to_id[name] = student_id

    # 2. Load assignments data
    assignment_points = {}  # assignment_id -> points
    assignment_names = {}  # name -> assignment_id
    assignments_path = os.path.join(data_dir, "assignments.txt")
    if not os.path.exists(assignments_path):
        print(f"ERROR: assignments.txt not found at {assignments_path}")
        return
    with open(assignments_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):  # Process in groups of 3
            name = lines[i].strip()
            assignment_id = lines[i + 1].strip()
            points = int(lines[i + 2].strip())
            assignment_points[assignment_id] = points
            assignment_names[name] = assignment_id

    # 3. LOAD SUBMISSIONS FROM FOLDER (CRITICAL FIX)
    submissions = {}  # (student_id, assignment_id) -> percentage
    submissions_dir = os.path.join(data_dir, "submissions")

    if not os.path.exists(submissions_dir):
        print(f"ERROR: submissions folder not found at {submissions_dir}")
        return

    # Process all .txt files in submissions folder
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.txt'):
            # Extract student_id and assignment_id from filename
            # Format: studentID_assignmentID.txt
            parts = filename[:-4].split('_')  # Remove .txt and split
            if len(parts) != 2:
                continue

            student_id = parts[0]
            assignment_id = parts[1]

            # Read the percentage from the file
            file_path = os.path.join(submissions_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    percentage = float(f.read().strip())
                    submissions[(student_id, assignment_id)] = percentage
            except (ValueError, FileNotFoundError):
                continue

    # === MENU SECTION ===
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ").strip()

    # === OPTION 1: STUDENT GRADE ===
    if choice == "1":
        name = input("What is the student's name: ").strip()
        if name not in name_to_id:
            print("Student not found")
            return

        student_id = name_to_id[name]
        total_points = 0
        for assignment_id, points in assignment_points.items():
            key = (student_id, assignment_id)
            if key in submissions:
                earned = (submissions[key] / 100) * points
                total_points += earned

        grade = round((total_points / 1000) * 100)  # Total possible = 1000
        print(f"{grade}%")

    # === OPTION 2: ASSIGNMENT STATISTICS ===
    elif choice == "2":
        assignment_name = input("What is the assignment name: ").strip()
        if assignment_name not in assignment_names:
            print("Assignment not found")
            return

        assignment_id = assignment_names[assignment_name]
        scores = [
            submissions[(sid, assignment_id)]
            for (sid, aid), score in submissions.items()
            if aid == assignment_id
        ]

        if not scores:
            print("Assignment not found")
            return

        min_score = round(min(scores))
        avg_score = round(sum(scores) / len(scores))
        max_score = round(max(scores))
        print(f"Min: {min_score}%")
        print(f"Avg: {avg_score}%")
        print(f"Max: {max_score}%")

    # === OPTION 3: ASSIGNMENT GRAPH ===
    elif choice == "3":
        assignment_name = input("What is the assignment name: ").strip()
        if assignment_name not in assignment_names:
            print("Assignment not found")
            return

        assignment_id = assignment_names[assignment_name]
        scores = [
            submissions[(sid, assignment_id)]
            for (sid, aid), score in submissions.items()
            if aid == assignment_id
        ]

        plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor='black')
        plt.title(f"{assignment_name} Scores")
        plt.xlabel("Percentage Score")
        plt.ylabel("Number of Students")
        plt.xticks([0, 25, 50, 75, 100])
        plt.show()


if __name__ == "__main__":
    main()