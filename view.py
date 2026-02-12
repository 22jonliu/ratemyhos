from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas using environment variable
client = MongoClient(os.getenv('MONGODB_URI'))

# Access your database - CORRECTED NAME
db = client['healthcare_platform']

# Access your collections
facilities_collection = db['healthcare_facilities']
reviews_collection = db['reviews']

def display_facility_with_reviews(facility_id=None, facility_name=None):
    """Display a specific facility and all its reviews"""
    
    if facility_id is not None:
        facility = facilities_collection.find_one({'id': facility_id})
    elif facility_name:
        facility = facilities_collection.find_one({'name': facility_name})
    else:
        print("Please provide either facility_id or facility_name")
        return
    
    if not facility:
        print("Facility not found!")
        return
    
    print("\n" + "=" * 80)
    print(f"FACILITY: {facility['name']}")
    print("=" * 80)
    print(f"ID: {facility['id']}")
    print(f"Address: {facility['address']['full_address']}")
    
    # Find all reviews for this facility
    facility_reviews = list(reviews_collection.find({'facility_id': facility['id']}))
    
    print(f"\nTotal Reviews: {len(facility_reviews)}")
    
    if facility_reviews:
        # Calculate average ratings
        avg_overall = sum(r['ratings']['overall'] for r in facility_reviews) / len(facility_reviews)
        avg_work_life = sum(r['ratings']['work_life_balance'] for r in facility_reviews) / len(facility_reviews)
        avg_salary = sum(r['ratings']['salary_benefits'] for r in facility_reviews) / len(facility_reviews)
        avg_management = sum(r['ratings']['management'] for r in facility_reviews) / len(facility_reviews)
        
        print(f"\nAverage Ratings:")
        print(f"  Overall: {avg_overall:.2f}/5.0")
        print(f"  Work-Life Balance: {avg_work_life:.2f}/5.0")
        print(f"  Salary & Benefits: {avg_salary:.2f}/5.0")
        print(f"  Management: {avg_management:.2f}/5.0")
        
        print("\n" + "-" * 80)
        print("REVIEWS:")
        print("-" * 80)
        
        for review in facility_reviews:
            print(f"\n[Review #{review['review_id']}] {review['job_title']} - {review['department']}")
            print(f"Experience: {review['years_of_experience']} | Posted: {review['date_posted']}")
            
            comp = review['compensation']
            print(f"Pay: ${comp['hourly_rate']}/hr (${comp['annual_salary']:,}/year)")
            
            print(f"Overall Rating: {review['ratings']['overall']}/5.0")
            print(f"Pros: {review['pros']}")
            print(f"Cons: {review['cons']}")
            print(f"Would Recommend: {'✓ Yes' if review['would_recommend'] else '✗ No'}")
            print("-" * 80)

def search_reviews_by_job_title(job_title):
    """Find all reviews for a specific job title across all facilities"""
    
    print(f"\n{'=' * 80}")
    print(f"REVIEWS FOR: {job_title}")
    print("=" * 80)
    
    reviews = list(reviews_collection.find({'job_title': {'$regex': job_title, '$options': 'i'}}))
    
    if not reviews:
        print(f"No reviews found for job title: {job_title}")
        return
    
    print(f"Found {len(reviews)} reviews\n")
    
    for review in reviews:
        print(f"Facility: {review['facility_name']}")
        print(f"Department: {review['department']} | Experience: {review['years_of_experience']}")
        
        comp = review['compensation']
        print(f"Pay: ${comp['hourly_rate']}/hr (${comp['annual_salary']:,}/year)")
        print(f"Overall Rating: {review['ratings']['overall']}/5.0")
        print(f"Pros: {review['pros']}")
        print(f"Cons: {review['cons']}")
        print("-" * 80)

def compare_facilities():
    """Compare all facilities side by side"""
    
    print("\n" + "=" * 80)
    print("FACILITY COMPARISON")
    print("=" * 80)
    
    facilities = list(facilities_collection.find())
    
    for facility in facilities:
        reviews = list(reviews_collection.find({'facility_id': facility['id']}))
        
        print(f"\n{facility['name']}")
        print(f"Address: {facility['address']['city']}, {facility['address']['state']}")
        print(f"Total Reviews: {len(reviews)}")
        
        if reviews:
            avg_overall = sum(r['ratings']['overall'] for r in reviews) / len(reviews)
            avg_salary_rating = sum(r['ratings']['salary_benefits'] for r in reviews) / len(reviews)
            avg_actual_salary = sum(r['compensation']['annual_salary'] for r in reviews) / len(reviews)
            recommend_pct = sum(1 for r in reviews if r['would_recommend']) / len(reviews) * 100
            
            print(f"Average Overall Rating: {avg_overall:.2f}/5.0")
            print(f"Average Salary Rating: {avg_salary_rating:.2f}/5.0")
            print(f"Average Actual Salary: ${avg_actual_salary:,.2f}/year")
            print(f"Recommend: {recommend_pct:.0f}%")
        else:
            print("No reviews yet")
        
        print("-" * 80)

def get_salary_insights_by_role(job_title):
    """Get salary insights for a specific role across all facilities"""
    
    print(f"\n{'=' * 80}")
    print(f"SALARY INSIGHTS: {job_title}")
    print("=" * 80)
    
    reviews = list(reviews_collection.find({'job_title': {'$regex': job_title, '$options': 'i'}}))
    
    if not reviews:
        print(f"No data found for: {job_title}")
        return
    
    salaries = [r['compensation']['annual_salary'] for r in reviews]
    hourly_rates = [r['compensation']['hourly_rate'] for r in reviews]
    
    print(f"\nBased on {len(reviews)} reviews:")
    print(f"Average Salary: ${sum(salaries)/len(salaries):,.2f}/year")
    print(f"Salary Range: ${min(salaries):,} - ${max(salaries):,}")
    print(f"Average Hourly: ${sum(hourly_rates)/len(hourly_rates):.2f}/hour")
    print(f"Hourly Range: ${min(hourly_rates):.2f} - ${max(hourly_rates):.2f}")
    
    print("\nBy Facility:")
    for review in reviews:
        print(f"  {review['facility_name']}: ${review['compensation']['annual_salary']:,}/year (${review['compensation']['hourly_rate']}/hr)")

# ============================================================================
# MAIN EXECUTION - Uncomment the function you want to run
# ============================================================================

# Example 1: View a specific facility and all its reviews
print("\n### EXAMPLE 1: View Saint Michael's Medical Center ###")
display_facility_with_reviews(facility_id=0)

# Example 2: Search reviews by job title
print("\n\n### EXAMPLE 2: Search for RN reviews ###")
search_reviews_by_job_title("Registered Nurse")

# Example 3: Compare all facilities
print("\n\n### EXAMPLE 3: Compare all facilities ###")
compare_facilities()

# Example 4: Get salary insights for a specific role
print("\n\n### EXAMPLE 4: Salary insights for CNAs ###")
get_salary_insights_by_role("CNA")

# Close connection
client.close()