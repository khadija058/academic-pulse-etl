import csv
from pathlib import Path

class StudentFeedbackTransformer:
    def __init__(self):
        self.input_dir = Path("data/raw")
        self.output_dir = Path("data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print("🔄 Data transformer initialized")
    
    def load_raw_data(self, filename="student_feedback.csv"):
        file_path = self.input_dir / filename
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return None
        
        records = []
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append(row)
        
        print(f"📖 Loaded {len(records)} records")
        return records
    
    def enhance_data(self, records):
        print("➕ Enhancing data with calculated fields...")
        
        enhanced_records = []
        for record in records:
            # Convert to numbers
            overall = int(record['overall_rating'])
            content = int(record['course_content_rating'])
            instructor = int(record['instructor_effectiveness'])
            recommendation = int(record['recommendation_score'])
            
            # Calculate satisfaction score
            satisfaction_score = (overall + content + instructor + recommendation) / 4
            record['satisfaction_score'] = round(satisfaction_score, 2)
            
            # Add difficulty category
            difficulty = int(record['difficulty_level'])
            if difficulty <= 2:
                record['difficulty_category'] = 'Easy'
            elif difficulty == 3:
                record['difficulty_category'] = 'Moderate'
            elif difficulty == 4:
                record['difficulty_category'] = 'Hard'
            else:
                record['difficulty_category'] = 'Very Hard'
            
            # Add performance category
            if satisfaction_score >= 4:
                record['performance_category'] = 'Excellent'
            elif satisfaction_score >= 3:
                record['performance_category'] = 'Good'
            else:
                record['performance_category'] = 'Poor'
            
            enhanced_records.append(record)
        
        print(f"✅ Enhanced {len(enhanced_records)} records")
        return enhanced_records
    
    def save_processed_data(self, records, filename="processed_feedback.csv"):
        file_path = self.output_dir / filename
        
        if records:
            fieldnames = list(records[0].keys())
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
        
        print(f"💾 Saved processed data to {file_path}")
        return file_path
    
    def transform(self):
        print("🚀 Starting data transformation...")
        
        # Load raw data
        raw_records = self.load_raw_data()
        if not raw_records:
            return None
        
        # Enhance data
        enhanced_records = self.enhance_data(raw_records)
        
        # Save processed data
        processed_file = self.save_processed_data(enhanced_records)
        
        print("✅ Data transformation completed!")
        return {
            'processed_records': enhanced_records,
            'processed_file': processed_file
        }

if __name__ == "__main__":
    transformer = StudentFeedbackTransformer()
    result = transformer.transform()
    
    if result:
        print(f"\n📊 Sample enhanced record:")
        sample = result['processed_records'][0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
