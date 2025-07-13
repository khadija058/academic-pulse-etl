"""
Quick Data Summary Script
========================
Provides a quick overview of the processed data.
"""

import csv
import json
from pathlib import Path
from collections import Counter

def load_processed_data():
    """Load processed data"""
    file_path = Path("data/processed/processed_feedback.csv")
    
    if not file_path.exists():
        print("❌ No processed data found. Run the ETL pipeline first!")
        return None
    
    records = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numeric fields
            row['satisfaction_score'] = float(row['satisfaction_score'])
            row['engagement_score'] = float(row['engagement_score'])
            row['overall_rating'] = int(row['overall_rating'])
            records.append(row)
    
    return records

def print_summary(records):
    """Print data summary"""
    if not records:
        return
    
    total = len(records)
    
    print("📊 ACADEMIC PULSE DATA SUMMARY")
    print("=" * 50)
    print(f"Total Feedback Records: {total}")
    
    # Basic stats
    avg_satisfaction = sum(r['satisfaction_score'] for r in records) / total
    avg_engagement = sum(r['engagement_score'] for r in records) / total
    avg_overall = sum(r['overall_rating'] for r in records) / total
    
    print(f"\n📈 Average Scores:")
    print(f"  Satisfaction: {avg_satisfaction:.2f}/5")
    print(f"  Engagement: {avg_engagement:.2f}/5")
    print(f"  Overall Rating: {avg_overall:.2f}/5")
    
    # Unique counts
    unique_students = len(set(r['student_id'] for r in records))
    unique_courses = len(set(r['course_id'] for r in records))
    unique_instructors = len(set(r['instructor_id'] for r in records))
    unique_semesters = len(set(r['semester'] for r in records))
    
    print(f"\n📋 Data Coverage:")
    print(f"  Students: {unique_students}")
    print(f"  Courses: {unique_courses}")
    print(f"  Instructors: {unique_instructors}")
    print(f"  Semesters: {unique_semesters}")
    
    # Performance distribution
    performance_dist = Counter(r['performance_category'] for r in records)
    print(f"\n🏆 Performance Distribution:")
    for category in ['Excellent', 'Good', 'Fair', 'Poor']:
        if category in performance_dist:
            count = performance_dist[category]
            pct = (count / total) * 100
            print(f"  {category}: {count} ({pct:.1f}%)")
    
    # Difficulty distribution
    difficulty_dist = Counter(r['difficulty_category'] for r in records)
    print(f"\n⚡ Difficulty Distribution:")
    for category in ['Easy', 'Moderate', 'Hard', 'Very Hard']:
        if category in difficulty_dist:
            count = difficulty_dist[category]
            pct = (count / total) * 100
            print(f"  {category}: {count} ({pct:.1f}%)")

def main():
    records = load_processed_data()
    if records:
        print_summary(records)
    else:
        print("Run: python3 scripts/run_complete_etl.py")

if __name__ == "__main__":
    main()
