import os
import matplotlib.pyplot as plt

def main():
    student_id_to_name = {}
    student_name_to_id = {}
    with open('data/students.txt', 'r') as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            student_id = parts[0]
            name = ' '.join(parts[1:])
            student_id_to_name[student_id] = name
            student_name_to_id[name] = student_id

    assignments = []
    assignment_name_to_id = {}
    assignment_id_to_info = {}
    with open('data/assignments.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        i = 0
        while i < len(lines):
            name = lines[i]
            i += 1
            if i >= len(lines):
                break
            assignment_id = lines[i]
            i += 1
            if i >= len(lines):
                break
            points = int(lines[i])
            i += 1
            assignments.append((name, assignment_id, points))
            assignment_name_to_id[name] = assignment_id
            assignment_id_to_info[assignment_id] = (name, points)
    
    total_possible = sum(points for _, _, points in assignments)
    
    submissions_by_assignment = {}
    submissions_by_student = {}
    
    data_dir = 'data'
    for filename in os.listdir(data_dir):
        if filename == 'students.txt' or filename == 'assignments.txt':
            continue
        if len(filename) in (4, 5) and filename.isdigit():
            assignment_id = filename
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as f_sub:
                for line in f_sub:
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    student_id = parts[0]
                    try:
                        percentage = float(parts[1])
                    except ValueError:
                        continue
                    
                    if assignment_id not in submissions_by_assignment:
                        submissions_by_assignment[assignment_id] = []
                    submissions_by_assignment[assignment_id].append(percentage)
                    
                    if student_id not in submissions_by_student:
                        submissions_by_student[student_id] = {}
                    submissions_by_student[student_id][assignment_id] = percentage

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print()
    selection = input("Enter your selection: ").strip()
    
    if selection == '1':
        name = input("What is the student's name: ").strip()
        if name not in student_name_to_id:
            print("Student not found")
        else:
            student_id = student_name_to_id[name]
            total_points_earned = 0.0
            for _, assignment_id, points in assignments:
                if student_id in submissions_by_student and assignment_id in submissions_by_student[student_id]:
                    percentage = submissions_by_student[student_id][assignment_id]
                    points_earned = (percentage * points) / 100.0
                    total_points_earned += points_earned
            grade_percent = (total_points_earned / total_possible) * 100.0
            grade_percent = round(grade_percent)
            print(f"{int(grade_percent)}%")
            
    elif selection == '2':
        assignment_name = input("What is the assignment name: ").strip()
        if assignment_name not in assignment_name_to_id:
            print("Assignment not found")
        else:
            assignment_id = assignment_name_to_id[assignment_name]
            if assignment_id not in submissions_by_assignment:
                print("Assignment not found")
            else:
                percentages = submissions_by_assignment[assignment_id]
                min_val = min(percentages)
                max_val = max(percentages)
                avg_val = sum(percentages) / len(percentages)
                min_val = round(min_val)
                max_val = round(max_val)
                avg_val = round(avg_val)
                print(f"Min: {int(min_val)}%")
                print(f"Avg: {int(avg_val)}%")
                print(f"Max: {int(max_val)}%")
                
    elif selection == '3':
        assignment_name = input("What is the assignment name: ").strip()
        if assignment_name not in assignment_name_to_id:
            print("Assignment not found")
        else:
            assignment_id = assignment_name_to_id[assignment_name]
            if assignment_id not in submissions_by_assignment:
                print("Assignment not found")
            else:
                percentages = submissions_by_assignment[assignment_id]
                plt.hist(percentages, bins=[0, 25, 50, 75, 100])
                plt.show()

if __name__ == "__main__":
    main()
