"""
Academic Pulse Dashboard
=======================
Interactive dashboard for exploring the data.
"""

import csv
from pathlib import Path
from collections import Counter

def main_menu():
    """Display main menu"""
    print("\n🎓 ACADEMIC PULSE DASHBOARD")
    print("=" * 40)
    print("1. 📊 Quick Overview")
    print("2. 🏆 Instructor Rankings")
    print("3. 📚 Course Analysis")
    print("4. 📈 Performance Trends")
    print("5. 🔍 Custom Search")
    print("0. ❌ Exit")
    print("-" * 40)
    
    choice = input("Select option (0-5): ").strip()
    return choice

def load_data():
    """Load processed data"""
    file_path = Path("data/processed/processed_feedback.csv")
    if not file_path.exists():
        print("❌ No data found. Run ETL pipeline first!")
        return None
    
    records = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(row)
    return records

def quick_overview(records):
    """Show quick overview"""
    print("\n📊 QUICK OVERVIEW")
    print("-" * 30)
    total = len(records)
    avg_satisfaction = sum(float(r['satisfaction_score']) for r in records) / total
    
    print(f"Total Records: {total}")
    print(f"Average Satisfaction: {avg_satisfaction:.2f}/5")
    
    performance_dist = Counter(r['performance_category'] for r in records)
    print("\nPerformance Distribution:")
    for category, count in performance_dist.most_common():
        pct = (count / total) * 100
        bar = "█" * int(pct / 5)
        print(f"  {category:<10}: {bar:<20} {pct:5.1f}%")

def instructor_rankings(records):
    """Show instructor rankings"""
    print("\n🏆 INSTRUCTOR RANKINGS")
    print("-" * 35)
    
    instructor_scores = {}
    instructor_counts = {}
    
    for record in records:
        instructor = record['instructor_id']
        score = float(record['satisfaction_score'])
        
        if instructor not in instructor_scores:
            instructor_scores[instructor] = 0
            instructor_counts[instructor] = 0
        
        instructor_scores[instructor] += score
        instructor_counts[instructor] += 1
    
    # Calculate averages and sort
    instructor_averages = []
    for instructor in instructor_scores:
        avg = instructor_scores[instructor] / instructor_counts[instructor]
        count = instructor_counts[instructor]
        instructor_averages.append((instructor, avg, count))
    
    instructor_averages.sort(key=lambda x: x[1], reverse=True)
    
    print("Rank │ Instructor │ Rating │ Reviews")
    print("─────┼────────────┼────────┼────────")
    for i, (instructor, avg, count) in enumerate(instructor_averages, 1):
        stars = "★" * int(avg) + "☆" * (5 - int(avg))
        print(f"{i:4} │ {instructor:<10} │ {avg:6.2f} │ {count:7}")

def custom_search(records):
    """Custom search functionality"""
    print("\n🔍 CUSTOM SEARCH")
    print("-" * 25)
    print("1. Search by Instructor")
    print("2. Search by Course")
    print("3. Search by Semester")
    
    choice = input("Select search type (1-3): ").strip()
    
    if choice == "1":
        instructor_id = input("Enter instructor ID (e.g., INST01): ").strip().upper()
        matching = [r for r in records if r['instructor_id'] == instructor_id]
        
        if matching:
            avg_score = sum(float(r['satisfaction_score']) for r in matching) / len(matching)
            print(f"\n{instructor_id} Results:")
            print(f"  Reviews: {len(matching)}")
            print(f"  Average Rating: {avg_score:.2f}/5")
            
            courses = set(r['course_id'] for r in matching)
            print(f"  Courses Taught: {', '.join(sorted(courses))}")
        else:
            print(f"No records found for {instructor_id}")
    
    elif choice == "2":
        course_id = input("Enter course ID (e.g., COURSE01): ").strip().upper()
        matching = [r for r in records if r['course_id'] == course_id]
        
        if matching:
            avg_score = sum(float(r['satisfaction_score']) for r in matching) / len(matching)
            avg_difficulty = sum(int(r['difficulty_level']) for r in matching) / len(matching)
            print(f"\n{course_id} Results:")
            print(f"  Reviews: {len(matching)}")
            print(f"  Average Satisfaction: {avg_score:.2f}/5")
            print(f"  Average Difficulty: {avg_difficulty:.1f}/5")
            
            instructors = set(r['instructor_id'] for r in matching)
            print(f"  Instructors: {', '.join(sorted(instructors))}")
        else:
            print(f"No records found for {course_id}")
    
    elif choice == "3":
        semester = input("Enter semester (e.g., Fall2024): ").strip()
        matching = [r for r in records if semester.lower() in r['semester'].lower()]
        
        if matching:
            avg_score = sum(float(r['satisfaction_score']) for r in matching) / len(matching)
            print(f"\n{semester} Results:")
            print(f"  Reviews: {len(matching)}")
            print(f"  Average Satisfaction: {avg_score:.2f}/5")
            
            courses = len(set(r['course_id'] for r in matching))
            instructors = len(set(r['instructor_id'] for r in matching))
            print(f"  Courses Offered: {courses}")
            print(f"  Active Instructors: {instructors}")
        else:
            print(f"No records found for {semester}")

def main():
    """Main dashboard function"""
    records = load_data()
    if not records:
        return
    
    while True:
        choice = main_menu()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            quick_overview(records)
        elif choice == "2":
            instructor_rankings(records)
        elif choice == "3":
            print("\n📚 Course analysis feature coming soon!")
        elif choice == "4":
            print("\n📈 Trends analysis feature coming soon!")
        elif choice == "5":
            custom_search(records)
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
