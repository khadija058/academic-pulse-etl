import csv
import random
import json
from datetime import datetime
from pathlib import Path

class StudentFeedbackExtractor:
    def __init__(self):
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print("📁 Data extractor initialized")
    
    def create_sample_data(self, num_records=100):
        print(f"🔄 Creating {num_records} sample records...")
        
        records = []
        for i in range(1, num_records + 1):
            record = {
                'feedback_id': i,
                'student_id': f'STU{i:03d}',
                'course_id': f'COURSE{random.randint(1, 10):02d}',
                'instructor_id': f'INST{random.randint(1, 5):02d}',
                'semester': random.choice(['Fall2024', 'Spring2024', 'Summer2024']),
                'overall_rating': random.randint(1, 5),
                'course_content_rating': random.randint(1, 5),
                'instructor_effectiveness': random.randint(1, 5),
                'difficulty_level': random.randint(1, 5),
                'workload_rating': random.randint(1, 5),
                'recommendation_score': random.randint(1, 5),
                'attendance_rate': round(random.uniform(0.6, 1.0), 2),
                'assignment_quality': random.randint(1, 5),
                'feedback_date': '2024-07-13',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            records.append(record)
        
        return records
    
    def save_to_csv(self, records, filename="student_feedback.csv"):
        file_path = self.data_dir / filename
        
        if records:
            fieldnames = list(records[0].keys())
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
        
        print(f"💾 Saved {len(records)} records to {file_path}")
        return file_path
    
    def extract_data(self, num_records=100):
        print("🚀 Starting data extraction...")
        records = self.create_sample_data(num_records)
        csv_path = self.save_to_csv(records)
        print("✅ Data extraction completed!")
        
        return {
            'records': records,
            'csv_path': csv_path
        }

if __name__ == "__main__":
    extractor = StudentFeedbackExtractor()
    result = extractor.extract_data()
    
    print(f"\n📊 Sample records:")
    for i, record in enumerate(result['records'][:3]):
        print(f"Record {i+1}: {record}")
