import csv
from pathlib import Path
from collections import Counter

def load_data():
    file_path = Path("data/processed/processed_feedback.csv")
    
    if not file_path.exists():
        print("❌ No processed data found. Run transformer first!")
        return None
    
    records = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(row)
    
    return records

def analyze_data(records):
    print("📊 ACADEMIC PULSE ANALYSIS")
    print("=" * 40)
    print(f"Total Records: {len(records)}")
    
    # Basic stats
    satisfaction_scores = [float(r['satisfaction_score']) for r in records]
    avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
    print(f"Average Satisfaction: {avg_satisfaction:.2f}/5")
    
    # Performance distribution
    performance_dist = Counter(r['performance_category'] for r in records)
    print(f"\n🏆 Performance Distribution:")
    for category, count in performance_dist.items():
        pct = (count / len(records)) * 100
        print(f"  {category}: {count} ({pct:.1f}%)")
    
    # Difficulty distribution
    difficulty_dist = Counter(r['difficulty_category'] for r in records)
    print(f"\n⚡ Difficulty Distribution:")
    for category, count in difficulty_dist.items():
        pct = (count / len(records)) * 100
        print(f"  {category}: {count} ({pct:.1f}%)")
    
    # Top instructors
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
    
    print(f"\n🥇 Top Instructors:")
    instructor_averages = []
    for instructor in instructor_scores:
        avg = instructor_scores[instructor] / instructor_counts[instructor]
        instructor_averages.append((instructor, avg, instructor_counts[instructor]))
    
    instructor_averages.sort(key=lambda x: x[1], reverse=True)
    
    for i, (instructor, avg, count) in enumerate(instructor_averages[:5], 1):
        print(f"  {i}. {instructor}: {avg:.2f}/5 (n={count})")

def main():
    records = load_data()
    if records:
        analyze_data(records)
    else:
        print("Run the extractor and transformer first:")
        print("  python3 src/extract/data_extractor.py")
        print("  python3 src/transform/data_transformer.py")

if __name__ == "__main__":
    main()
