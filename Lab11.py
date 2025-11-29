import os
import matplotlib.pyplot as plt

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    # 1. Load students data - FIXED PARSING
    students = {}  # student_id -> name
    name_to_id = {}  # name -> student_id
    with open(os.path.join(data_dir, "students.txt"), 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Find the 3-digit ID at the end (with possible leading zeros)
            for i in range(len(line)):
                if i >= 3 and line[i-3:i+1].isdigit() and (i == len(line) or not line[i].isdigit()):
                    student_id = line[i-3:i]
                    name = line[:i-3].strip()
                    students[student_id] = name
                    name_to_id[name] = student_id
                    break
            else:
                # Fallback: last 3 characters
                student_id = line[-3:]
                name = line[:-3].strip()
                students[student_id] = name
                name_to_id[name] = student_id

    # 2. Load assignments data - FIXED PARSING
    assignment_points = {}  # assignment_id -> points
    assignment_names = {}  # name -> assignment_id
    with open(os.path.join(data_dir, "assignments.txt"), 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            if i + 2 >= len(lines):
                break
            name = lines[i].strip()
            assignment_id = lines[i+1].strip()
            try:
                points = int(lines[i+2].strip())
            except ValueError:
                continue
            assignment_points[assignment_id] = points
            assignment_names[name] = assignment_id

    # 3. Load submissions from folder
    submissions = {}  # (student_id, assignment_id) -> percentage
    submissions_dir = os.path.join(data_dir, "submissions")
    
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.txt'):
            # Extract student_id and assignment_id from filename
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
