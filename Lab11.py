import os
import matplotlib.pyplot as plt

def main():
    # Parse students.txt - ID is at the END of each line
    student_id_to_name = {}
    student_name_to_id = {}
    with open('data/students.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Find the 3-digit ID at the end
            parts = line.split()
            student_id = parts[-1]  # ID is the last element
            name = ' '.join(parts[:-1])  # Everything except last element is the name
            student_id_to_name[student_id] = name
            student_name_to_id[name] = student_id

    # Parse assignments.txt - 3 lines per assignment
    assignments = []
    assignment_name_to_id = {}
    assignment_id_to_points = {}  # Just store points for simplicity
    total_possible = 0
    
    with open('data/assignments.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        i = 0
        while i < len(lines):
            if i + 2 >= len(lines):
                break
                
            name = lines[i]
            assignment_id = lines[i+1]
            points = int(lines[i+2])
            
            assignments.append((name, assignment_id, points))
            assignment_name_to_id[name] = assignment_id
            assignment_id_to_points[assignment_id] = points
            total_possible += points
            
            i += 3

    # Parse submission files
    submissions_by_assignment = {}  # assignment_id -> list of percentages
    submissions_by_student = {}     # student_id -> {assignment_id: percentage}
    
    for filename in os.listdir('data'):
        if filename in ['students.txt', 'assignments.txt']:
            continue
            
        # Check if filename matches any known assignment ID
        for _, assignment_id, _ in assignments:
            if filename == assignment_id:
                file_path = os.path.join('data', filename)
                with open(file_path, 'r') as f_sub:
                    for line in f_sub:
                        parts = line.split()
                        if len(parts) < 2:
                            continue
                            
                        student_id = parts[0]
                        percentage = float(parts[1])
                        
                        # Store by assignment
                        if assignment_id not in submissions_by_assignment:
                            submissions_by_assignment[assignment_id] = []
                        submissions_by_assignment[assignment_id].append(percentage)
                        
                        # Store by student
                        if student_id not in submissions_by_student:
                            submissions_by_student[student_id] = {}
                        submissions_by_student[student_id][assignment_id] = percentage
                break

    # Display menu
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
            print(f"{round(grade_percent)}%")
            
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
                print(f"Min: {round(min_val)}%")
                print(f"Avg: {round(avg_val)}%")
                print(f"Max: {round(max_val)}%")
                
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
