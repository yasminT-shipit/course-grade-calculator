import os
import matplotlib.pyplot as plt

def main():
    # Parse students.txt correctly - ID is first 3 characters, no space
    student_id_to_name = {}
    student_name_to_id = {}
    
    with open('data/students.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # First 3 characters are the ID
            student_id = line[:3]
            # Rest of the line is the name
            name = line[3:]
            
            student_id_to_name[student_id] = name
            student_name_to_id[name] = student_id

    # Parse assignments.txt correctly
    assignments = []
    assignment_name_to_id = {}
    assignment_id_to_points = {}
    
    with open('data/assignments.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        i = 0
        while i < len(lines):
            if i + 2 >= len(lines):
                break
                
            name = lines[i]
            assignment_id = lines[i+1]
            try:
                points = int(lines[i+2])
            except (ValueError, IndexError):
                i += 3
                continue
                
            assignments.append((name, assignment_id, points))
            assignment_name_to_id[name] = assignment_id
            assignment_id_to_points[assignment_id] = points
            
            i += 3

    # Parse submission files - they're in data/submissions directory
    submissions_by_assignment = {}  # assignment_id -> list of percentages
    submissions_by_student = {}     # student_id -> {assignment_id: percentage}
    
    # Check if submissions directory exists
    submissions_dir = os.path.join('data', 'submissions')
    if os.path.isdir(submissions_dir):
        # Process files in submissions directory
        for filename in os.listdir(submissions_dir):
            file_path = os.path.join(submissions_dir, filename)
            # Make sure it's a file, not a directory
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f_sub:
                    for line in f_sub:
                        # Format: student_id|assignment_id|score
                        parts = line.strip().split('|')
                        if len(parts) < 3:
                            continue
                            
                        student_id = parts[0].strip()
                        assignment_id = parts[1].strip()
                        try:
                            percentage = float(parts[2])
                        except ValueError:
                            continue
                        
                        # Verify this is a valid assignment ID
                        if assignment_id not in assignment_id_to_points:
                            continue
                        
                        # Store by assignment
                        if assignment_id not in submissions_by_assignment:
                            submissions_by_assignment[assignment_id] = []
                        submissions_by_assignment[assignment_id].append(percentage)
                        
                        # Store by student
                        if student_id not in submissions_by_student:
                            submissions_by_student[student_id] = {}
                        submissions_by_student[student_id][assignment_id] = percentage
    else:
        # Fallback: process files directly in data directory (for older formats)
        for filename in os.listdir('data'):
            if filename in ['students.txt', 'assignments.txt']:
                continue
                
            file_path = os.path.join('data', filename)
            # Make sure it's a file, not a directory
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f_sub:
                    for line in f_sub:
                        # Format: student_id|assignment_id|score
                        parts = line.strip().split('|')
                        if len(parts) < 3:
                            continue
                            
                        student_id = parts[0].strip()
                        assignment_id = parts[1].strip()
                        try:
                            percentage = float(parts[2])
                        except ValueError:
                            continue
                        
                        # Verify this is a valid assignment ID
                        if assignment_id not in assignment_id_to_points:
                            continue
                        
                        # Store by assignment
                        if assignment_id not in submissions_by_assignment:
                            submissions_by_assignment[assignment_id] = []
                        submissions_by_assignment[assignment_id].append(percentage)
                        
                        # Store by student
                        if student_id not in submissions_by_student:
                            submissions_by_student[student_id] = {}
                        submissions_by_student[student_id][assignment_id] = percentage

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
            
            # Calculate total points earned across all assignments
            for _, assignment_id, points in assignments:
                if student_id in submissions_by_student and assignment_id in submissions_by_student[student_id]:
                    percentage = submissions_by_student[student_id][assignment_id]
                    # Convert percentage to points: (percentage/100) * assignment_points
                    points_earned = (percentage / 100.0) * points
                    total_points_earned += points_earned
            
            # The problem states total possible points is 1000
            grade_percent = (total_points_earned / 1000.0) * 100.0
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
