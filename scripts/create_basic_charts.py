"""
Basic Charts for Academic Pulse Data
====================================
Creates simple text-based charts and basic analysis.
"""

import csv
from pathlib import Path
from collections import Counter, defaultdict

def load_data():
    """Load processed data"""
    file_path = Path("data/processed/processed_feedback.csv")
    
    if not file_path.exists():
        print("❌ No processed data found.")
        return None
    
    records = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['satisfaction_score'] = float(row['satisfaction_score'])
            row['overall_rating'] = int(row['overall_rating'])
            records.append(row)
    
    return records

def create_text_chart(data, title, max_width=50):
    """Create a simple text-based bar chart"""
    print(f"\n📊 {title}")
    print("=" * len(title))
    
    if not data:
        return
    
    max_value = max(data.values())
    
    for label, value in data.items():
        bar_length = int((value / max_value) * max_width)
        bar = "█" * bar_length
        print(f"{label:15} │{bar:<{max_width}} │ {value}")

def analyze_performance_by_category(records):
    """Analyze performance by different categories"""
    
    # Performance distribution
    performance_dist = Counter(r['performance_category'] for r in records)
    create_text_chart(dict(performance_dist), "Performance Distribution")
    
    # Difficulty distribution
    difficulty_dist = Counter(r['difficulty_category'] for r in records)
    create_text_chart(dict(difficulty_dist), "Difficulty Distribution")
    
    # Department performance
    dept_scores = defaultdict(list)
    for record in records:
        dept_scores[record['department']].append(record['satisfaction_score'])
    
    dept_averages = {
        dept: round(sum(scores) / len(scores), 2)
        for dept, scores in dept_scores.items()
    }
    create_text_chart(dept_averages, "Average Satisfaction by Department")
    
    # Semester trends
    semester_scores = defaultdict(list)
    for record in records:
        semester_scores[record['semester']].append(record['satisfaction_score'])
    
    semester_averages = {
        semester: round(sum(scores) / len(scores), 2)
        for semester, scores in semester_scores.items()
    }
    create_text_chart(semester_averages, "Average Satisfaction by Semester")

def create_top_performers_chart(records):
    """Show top performing instructors and courses"""
    
    # Top instructors
    instructor_scores = defaultdict(list)
    for record in records:
        instructor_scores[record['instructor_id']].append(record['satisfaction_score'])
    
    instructor_averages = {
        instructor: sum(scores) / len(scores)
        for instructor, scores in instructor_scores.items()
        if len(scores) >= 5  # At least 5 reviews
    }
    
    top_instructors = dict(sorted(instructor_averages.items(), key=lambda x: x[1], reverse=True)[:8])
    top_instructors = {k: round(v, 2) for k, v in top_instructors.items()}
    create_text_chart(top_instructors, "Top Instructors (≥5 reviews)")
    
    # Top courses
    course_scores = defaultdict(list)
    for record in records:
        course_scores[record['course_id']].append(record['satisfaction_score'])
    
    course_averages = {
        course: sum(scores) / len(scores)
        for course, scores in course_scores.items()
        if len(scores) >= 3  # At least 3 reviews
    }
    
    top_courses = dict(sorted(course_averages.items(), key=lambda x: x[1], reverse=True)[:8])
    top_courses = {k: round(v, 2) for k, v in top_courses.items()}
    create_text_chart(top_courses, "Top Courses (≥3 reviews)")

def create_correlation_analysis(records):
    """Analyze correlations between different metrics"""
    print(f"\n📈 CORRELATION ANALYSIS")
    print("=" * 25)
    
    # Difficulty vs Satisfaction
    easy_courses = [r for r in records if r['difficulty_category'] == 'Easy']
    hard_courses = [r for r in records if r['difficulty_category'] == 'Very Hard']
    
    if easy_courses and hard_courses:
        easy_avg = sum(r['satisfaction_score'] for r in easy_courses) / len(easy_courses)
        hard_avg = sum(r['satisfaction_score'] for r in hard_courses) / len(hard_courses)
        
        print(f"Easy courses satisfaction: {easy_avg:.2f}/5 (n={len(easy_courses)})")
        print(f"Very hard courses satisfaction: {hard_avg:.2f}/5 (n={len(hard_courses)})")
        print(f"Difference: {easy_avg - hard_avg:.2f} points")
    
    # Engagement vs Satisfaction
    high_engagement = [r for r in records if r['engagement_score'] > '0.8']
    low_engagement = [r for r in records if r['engagement_score'] < '0.6']
    
    if high_engagement and low_engagement:
        high_sat = sum(r['satisfaction_score'] for r in high_engagement) / len(high_engagement)
        low_sat = sum(r['satisfaction_score'] for r in low_engagement) / len(low_engagement)
        
        print(f"\nHigh engagement satisfaction: {high_sat:.2f}/5 (n={len(high_engagement)})")
        print(f"Low engagement satisfaction: {low_sat:.2f}/5 (n={len(low_engagement)})")
        print(f"Difference: {high_sat - low_sat:.2f} points")

def main():
    """Main function"""
    print("📊 ACADEMIC PULSE - DATA VISUALIZATION")
    print("=" * 45)
    
    records = load_data()
    if not records:
        print("Run the ETL pipeline first: python3 scripts/run_complete_etl.py")
        return
    
    print(f"📖 Analyzing {len(records)} feedback records...")
    
    # Create various analyses
    analyze_performance_by_category(records)
    create_top_performers_chart(records)
    create_correlation_analysis(records)
    
    print(f"\n🎉 Analysis complete!")
    print(f"💡 Insights:")
    print(f"  - Review the top performers for best practices")
    print(f"  - Focus improvement efforts on poor-performing areas")
    print(f"  - Consider difficulty-satisfaction relationships for course design")

if __name__ == "__main__":
    main()
