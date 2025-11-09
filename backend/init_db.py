"""Initialize database with sample data."""
from app import create_app
from app.models import (
    db, UserCategory, User, Ward, QuizQuestion, QuizOption,
    Campaign, RecyclerLocation, RwaGroup
)
from datetime import datetime, date

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create user categories
    categories = [
        {"key": "PRIMARY", "label": "Primary User"},
        {"key": "SECONDARY", "label": "Secondary User (RWA/Collector)"},
        {"key": "TERTIARY", "label": "Tertiary User (Government/NGO)"}
    ]
    
    for cat_data in categories:
        if not UserCategory.query.filter_by(key=cat_data["key"]).first():
            category = UserCategory(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    
    # Create sample wards
    wards_data = [
        {"ward_number": "1", "name": "Park Street", "pincode": "700001"},
        {"ward_number": "2", "name": "Salt Lake", "pincode": "700064"},
        {"ward_number": "3", "name": "Howrah", "pincode": "700001"},
    ]
    
    for ward_data in wards_data:
        if not Ward.query.filter_by(ward_number=ward_data["ward_number"]).first():
            ward = Ward(**ward_data)
            db.session.add(ward)
    
    db.session.commit()
    
    # Create sample quiz questions
    questions_data = [
        {
            "question_text": "Which category does a waste plastic bottle belong to?",
            "category": "Recycling",
            "options": [
                {"text": "Wet Waste", "is_correct": False},
                {"text": "Dry Waste", "is_correct": True},
                {"text": "Hazardous Waste", "is_correct": False},
                {"text": "E-Waste", "is_correct": False}
            ]
        },
        {
            "question_text": "What should you do with kitchen scraps like vegetable peels?",
            "category": "Composting",
            "options": [
                {"text": "Throw in dry waste", "is_correct": False},
                {"text": "Compost or put in wet waste bin", "is_correct": True},
                {"text": "Burn them", "is_correct": False},
                {"text": "Throw in hazardous waste", "is_correct": False}
            ]
        },
        {
            "question_text": "Which item is considered hazardous waste?",
            "category": "Conservation",
            "options": [
                {"text": "Newspaper", "is_correct": False},
                {"text": "Battery", "is_correct": True},
                {"text": "Plastic bag", "is_correct": False},
                {"text": "Food waste", "is_correct": False}
            ]
        },
        {
            "question_text": "What is the benefit of waste segregation?",
            "category": "Sustainability",
            "options": [
                {"text": "Increases landfill waste", "is_correct": False},
                {"text": "Enables recycling and reduces environmental impact", "is_correct": True},
                {"text": "Makes waste collection harder", "is_correct": False},
                {"text": "No benefit", "is_correct": False}
            ]
        }
    ]
    
    for q_data in questions_data:
        question = QuizQuestion(
            question_text=q_data["question_text"],
            category=q_data["category"]
        )
        db.session.add(question)
        db.session.flush()
        
        for opt_data in q_data["options"]:
            option = QuizOption(
                question_id=question.id,
                option_text=opt_data["text"],
                is_correct=opt_data["is_correct"]
            )
            db.session.add(option)
    
    db.session.commit()
    
    # Create sample campaigns
    campaigns_data = [
        {
            "name": "Community Cleanup Drive",
            "description": "Join us for a community cleanup drive in Park Street area",
            "event_datetime": datetime(2025, 2, 15, 10, 0),
            "location": "Park Street, Kolkata",
            "pincode": "700001",
            "image_url": None
        },
        {
            "name": "Waste Segregation Workshop",
            "description": "Learn proper waste segregation techniques",
            "event_datetime": datetime(2025, 2, 20, 14, 0),
            "location": "Community Center, Salt Lake",
            "pincode": "700064",
            "image_url": None
        }
    ]
    
    ward_1 = Ward.query.filter_by(ward_number="1").first()
    ward_2 = Ward.query.filter_by(ward_number="2").first()
    
    for idx, camp_data in enumerate(campaigns_data):
        if not Campaign.query.filter_by(name=camp_data["name"]).first():
            camp_data["ward_id"] = ward_1.id if idx == 0 else ward_2.id
            campaign = Campaign(**camp_data)
            db.session.add(campaign)
    
    db.session.commit()
    
    # Create sample recycler locations
    recyclers_data = [
        {
            "name": "Green Recyclers",
            "address": "123 Main Street, Park Street",
            "pincode": "700001",
            "phone": "+91-9876543210",
            "website": "https://greenrecyclers.com"
        },
        {
            "name": "Eco Waste Solutions",
            "address": "456 Eco Road, Salt Lake",
            "pincode": "700064",
            "phone": "+91-9876543211",
            "website": None
        }
    ]
    
    for rec_data in recyclers_data:
        if not RecyclerLocation.query.filter_by(name=rec_data["name"]).first():
            rec_data["ward_id"] = ward_1.id if rec_data["pincode"] == "700001" else ward_2.id
            recycler = RecyclerLocation(**rec_data)
            db.session.add(recycler)
    
    db.session.commit()
    
    # Create sample RWA groups
    rwa_groups_data = [
        {"name": "Park Street RWA", "ward_number": "1", "pincode": "700001"},
        {"name": "Salt Lake RWA", "ward_number": "2", "pincode": "700064"}
    ]
    
    for rwa_data in rwa_groups_data:
        if not RwaGroup.query.filter_by(name=rwa_data["name"]).first():
            rwa = RwaGroup(**rwa_data)
            db.session.add(rwa)
    
    db.session.commit()
    
    print("Database initialized successfully!")
    print("Sample data created:")
    print("- User categories")
    print("- Wards")
    print("- Quiz questions")
    print("- Campaigns")
    print("- Recycler locations")
    print("- RWA groups")

