"""
Complete Academic Pulse ETL Pipeline
===================================
This script runs the entire ETL process in the correct order.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.append('src')

def run_extraction():
    """Run data extraction"""
    print("=" * 60)
    print("📥 STEP 1: DATA EXTRACTION")
    print("=" * 60)
    
    try:
        from extract.data_extractor import StudentFeedbackExtractor
        
        extractor = StudentFeedbackExtractor()
        result = extractor.extract_data(num_records=500)
        
        print(f"✅ Extraction completed successfully!")
        print(f"   - Records created: {len(result['records'])}")
        print(f"   - File saved: {result['csv_path']}")
        
        return True, result
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False, None

def run_transformation():
    """Run data transformation"""
    print("\n" + "=" * 60)
    print("🔄 STEP 2: DATA TRANSFORMATION")
    print("=" * 60)
    
    try:
        from transform.data_transformer import StudentFeedbackTransformer
        
        transformer = StudentFeedbackTransformer()
        result = transformer.transform()
        
        print(f"✅ Transformation completed successfully!")
        print(f"   - Records processed: {result['quality_report']['records_processed']}")
        print(f"   - Records cleaned: {result['quality_report']['records_cleaned']}")
        print(f"   - Data quality score: {result['quality_report']['data_quality_score']}%")
        
        return True, result
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return False, None

def run_analysis():
    """Run data analysis"""
    print("\n" + "=" * 60)
    print("📊 STEP 3: DATA ANALYSIS")
    print("=" * 60)
    
    try:
        # Load processed data and run basic analysis
        processed_file = Path("data/processed/processed_feedback.csv")
        
        if not processed_file.exists():
            print("❌ No processed data file found")
            return False, None
        
        import csv
        from collections import defaultdict, Counter
        
        # Load data
        records = []
        with open(processed_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append(row)
        
        print(f"📖 Loaded {len(records)} processed records")
        
        # Basic analysis
        total_records = len(records)
        
        # Convert numeric fields
        for record in records:
            record['satisfaction_score'] = float(record['satisfaction_score'])
            record['engagement_score'] = float(record['engagement_score'])
            record['overall_rating'] = int(record['overall_rating'])
        
        # Calculate averages
        avg_satisfaction = sum(r['satisfaction_score'] for r in records) / total_records
        avg_engagement = sum(r['engagement_score'] for r in records) / total_records
        avg_overall = sum(r['overall_rating'] for r in records) / total_records
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Average Satisfaction Score: {avg_satisfaction:.2f}/5")
        print(f"   Average Engagement Score: {avg_engagement:.2f}/5")
        print(f"   Average Overall Rating: {avg_overall:.2f}/5")
        
        # Performance distribution
        performance_dist = Counter(r['performance_category'] for r in records)
        print(f"\n🏆 PERFORMANCE DISTRIBUTION:")
        for category, count in performance_dist.items():
            percentage = (count / total_records) * 100
            print(f"   {category}: {count} ({percentage:.1f}%)")
        
        # Top instructors
        instructor_scores = defaultdict(list)
        for record in records:
            instructor_scores[record['instructor_id']].append(record['satisfaction_score'])
        
        instructor_averages = {
            instructor: sum(scores) / len(scores)
            for instructor, scores in instructor_scores.items()
        }
        
        top_instructors = sorted(instructor_averages.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n🥇 TOP 5 INSTRUCTORS:")
        for i, (instructor, score) in enumerate(top_instructors, 1):
            print(f"   {i}. {instructor}: {score:.2f}/5")
        
        # Course analysis
        course_scores = defaultdict(list)
        for record in records:
            course_scores[record['course_id']].append(record['satisfaction_score'])
        
        course_averages = {
            course: sum(scores) / len(scores)
            for course, scores in course_scores.items()
        }
        
        top_courses = sorted(course_averages.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n📚 TOP 5 COURSES:")
        for i, (course, score) in enumerate(top_courses, 1):
            print(f"   {i}. {course}: {score:.2f}/5")
        
        # Difficulty analysis
        difficulty_dist = Counter(r['difficulty_category'] for r in records)
        print(f"\n⚡ DIFFICULTY DISTRIBUTION:")
        for category, count in difficulty_dist.items():
            percentage = (count / total_records) * 100
            print(f"   {category}: {count} ({percentage:.1f}%)")
        
        # Department analysis
        dept_scores = defaultdict(list)
        for record in records:
            dept_scores[record['department']].append(record['satisfaction_score'])
        
        dept_averages = {
            dept: sum(scores) / len(scores)
            for dept, scores in dept_scores.items()
        }
        
        print(f"\n🏢 DEPARTMENT PERFORMANCE:")
        for dept, score in sorted(dept_averages.items(), key=lambda x: x[1], reverse=True):
            count = len(dept_scores[dept])
            print(f"   {dept}: {score:.2f}/5 (n={count})")
        
        return True, {
            'total_records': total_records,
            'avg_satisfaction': avg_satisfaction,
            'avg_engagement': avg_engagement,
            'performance_dist': dict(performance_dist),
            'top_instructors': top_instructors[:3],
            'top_courses': top_courses[:3]
        }
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False, None

def main():
    """Run complete ETL pipeline"""
    print("🎓 ACADEMIC PULSE ETL PIPELINE")
    print("🚀 Starting complete ETL process...")
    
    # Step 1: Extract
    extract_success, extract_result = run_extraction()
    if not extract_success:
        print("❌ Pipeline failed at extraction step")
        return
    
    # Step 2: Transform
    transform_success, transform_result = run_transformation()
    if not transform_success:
        print("❌ Pipeline failed at transformation step")
        return
    
    # Step 3: Analyze
    analyze_success, analyze_result = run_analysis()
    if not analyze_success:
        print("❌ Pipeline failed at analysis step")
        return
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   Raw records extracted: {len(extract_result['records'])}")
    print(f"   Records processed: {transform_result['quality_report']['records_cleaned']}")
    print(f"   Data quality score: {transform_result['quality_report']['data_quality_score']}%")
    print(f"   Average satisfaction: {analyze_result['avg_satisfaction']:.2f}/5")
    
    print(f"\n📁 FILES CREATED:")
    print(f"   - Raw data: data/raw/student_feedback.csv")
    print(f"   - Processed data: data/processed/processed_feedback.csv")
    print(f"   - Metadata: data/raw/metadata.json")
    print(f"   - Quality report: data/processed/data_quality_report.json")
    print(f"   - Aggregations: data/processed/aggregations.json")
    
    print(f"\n🏆 TOP PERFORMERS:")
    for i, (instructor, score) in enumerate(analyze_result['top_instructors'], 1):
        print(f"   {i}. Instructor {instructor}: {score:.2f}/5")
    
    print(f"\n📚 TOP COURSES:")
    for i, (course, score) in enumerate(analyze_result['top_courses'], 1):
        print(f"   {i}. {course}: {score:.2f}/5")

if __name__ == "__main__":
    main()
