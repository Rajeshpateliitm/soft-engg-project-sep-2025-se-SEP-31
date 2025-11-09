"""Initialize database with sample data."""
from app.models import (
    db, UserCategory, User, Ward, QuizQuestion, QuizOption,
    Campaign, RecyclerLocation, RwaGroup, RwaMembership
)
from datetime import datetime


def init_sample_data():
    """Initialize database with sample data if it doesn't exist."""
    try:
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
        
        # Create predefined secondary users (Waste Collectors and RWA Managers)
        # These users are provisioned and do not use public sign-up
        secondary_category = UserCategory.query.filter_by(key="SECONDARY").first()
        ward_1 = Ward.query.filter_by(ward_number="1").first()
        ward_2 = Ward.query.filter_by(ward_number="2").first()
        
        if secondary_category:
            secondary_users_data = [
                {
                    "email": "collector1@wastewise.com",
                    "username": "waste_collector_1",
                    "password": "Collector@123",
                    "house_number": None,
                    "ward_number": "1",
                    "ward_id": ward_1.id if ward_1 else None,
                    "family_members_count": None,
                    "pincode": "700001",
                    "user_category_id": secondary_category.id
                },
                {
                    "email": "collector2@wastewise.com",
                    "username": "waste_collector_2",
                    "password": "Collector@123",
                    "house_number": None,
                    "ward_number": "2",
                    "ward_id": ward_2.id if ward_2 else None,
                    "family_members_count": None,
                    "pincode": "700064",
                    "user_category_id": secondary_category.id
                },
                {
                    "email": "rwa_manager1@wastewise.com",
                    "username": "rwa_manager_parkstreet",
                    "password": "RWA@Manager123",
                    "house_number": None,
                    "ward_number": "1",
                    "ward_id": ward_1.id if ward_1 else None,
                    "family_members_count": None,
                    "pincode": "700001",
                    "user_category_id": secondary_category.id
                },
                {
                    "email": "rwa_manager2@wastewise.com",
                    "username": "rwa_manager_saltlake",
                    "password": "RWA@Manager123",
                    "house_number": None,
                    "ward_number": "2",
                    "ward_id": ward_2.id if ward_2 else None,
                    "family_members_count": None,
                    "pincode": "700064",
                    "user_category_id": secondary_category.id
                }
            ]
            
            for user_data in secondary_users_data:
                # Check if user already exists
                if User.query.filter_by(email=user_data["email"]).first():
                    continue
                
                # Extract password before creating user
                password = user_data.pop("password")
                
                # Create user
                user = User(**user_data)
                user.set_password(password)
                db.session.add(user)
            
            db.session.commit()
            print("✅ Predefined secondary users created")
        
        # Create predefined tertiary user (Government/NGO)
        # This user is provisioned and does not use public sign-up
        tertiary_category = UserCategory.query.filter_by(key="TERTIARY").first()
        
        if tertiary_category:
            tertiary_user_data = {
                "email": "tertiary@wastewise.com",
                "username": "government_admin",
                "password": "Tertiary@123",
                "house_number": None,
                "ward_number": None,
                "ward_id": None,
                "family_members_count": None,
                "pincode": None,
                "user_category_id": tertiary_category.id
            }
            
            # Check if tertiary user already exists
            if not User.query.filter_by(email=tertiary_user_data["email"]).first():
                # Extract password before creating user
                password = tertiary_user_data.pop("password")
                
                # Create user
                tertiary_user = User(**tertiary_user_data)
                tertiary_user.set_password(password)
                db.session.add(tertiary_user)
                db.session.commit()
                print("✅ Predefined tertiary user created")
        
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
            # Check if question already exists
            if QuizQuestion.query.filter_by(question_text=q_data["question_text"]).first():
                continue
                
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
        ward_1 = Ward.query.filter_by(ward_number="1").first()
        ward_2 = Ward.query.filter_by(ward_number="2").first()
        
        if ward_1 and ward_2:
            campaigns_data = [
                {
                    "name": "Community Cleanup Drive",
                    "description": "Join us for a community cleanup drive in Park Street area",
                    "event_datetime": datetime(2025, 2, 15, 10, 0),
                    "location": "Park Street, Kolkata",
                    "pincode": "700001",
                    "image_url": None,
                    "ward_id": ward_1.id
                },
                {
                    "name": "Waste Segregation Workshop",
                    "description": "Learn proper waste segregation techniques",
                    "event_datetime": datetime(2025, 2, 20, 14, 0),
                    "location": "Community Center, Salt Lake",
                    "pincode": "700064",
                    "image_url": None,
                    "ward_id": ward_2.id
                }
            ]
            
            for camp_data in campaigns_data:
                if not Campaign.query.filter_by(name=camp_data["name"]).first():
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
                    "website": "https://greenrecyclers.com",
                    "ward_id": ward_1.id
                },
                {
                    "name": "Eco Waste Solutions",
                    "address": "456 Eco Road, Salt Lake",
                    "pincode": "700064",
                    "phone": "+91-9876543211",
                    "website": None,
                    "ward_id": ward_2.id
                }
            ]
            
            for rec_data in recyclers_data:
                if not RecyclerLocation.query.filter_by(name=rec_data["name"]).first():
                    recycler = RecyclerLocation(**rec_data)
                    db.session.add(recycler)
            
            db.session.commit()
            
            # Create sample RWA groups
            rwa_groups_data = [
                {"name": "Park Street RWA", "ward_number": "1", "pincode": "700001"},
                {"name": "Salt Lake RWA", "ward_number": "2", "pincode": "700064"}
            ]
            
            rwa_group_1 = None
            rwa_group_2 = None
            
            for rwa_data in rwa_groups_data:
                existing_rwa = RwaGroup.query.filter_by(name=rwa_data["name"]).first()
                if not existing_rwa:
                    rwa = RwaGroup(**rwa_data)
                    db.session.add(rwa)
                    db.session.flush()
                    if rwa_data["ward_number"] == "1":
                        rwa_group_1 = rwa
                    elif rwa_data["ward_number"] == "2":
                        rwa_group_2 = rwa
                else:
                    if rwa_data["ward_number"] == "1":
                        rwa_group_1 = existing_rwa
                    elif rwa_data["ward_number"] == "2":
                        rwa_group_2 = existing_rwa
            
            db.session.commit()
            
            # Add secondary users to RWA groups as collectors/admins
            if rwa_group_1 and rwa_group_2:
                # Get secondary users
                collector1 = User.query.filter_by(email="collector1@wastewise.com").first()
                rwa_manager1 = User.query.filter_by(email="rwa_manager1@wastewise.com").first()
                collector2 = User.query.filter_by(email="collector2@wastewise.com").first()
                rwa_manager2 = User.query.filter_by(email="rwa_manager2@wastewise.com").first()
                
                # Add collectors to RWA groups
                if collector1 and not RwaMembership.query.filter_by(user_id=collector1.id, rwa_group_id=rwa_group_1.id).first():
                    membership = RwaMembership(
                        rwa_group_id=rwa_group_1.id,
                        user_id=collector1.id,
                        role="collector"
                    )
                    db.session.add(membership)
                
                if collector2 and not RwaMembership.query.filter_by(user_id=collector2.id, rwa_group_id=rwa_group_2.id).first():
                    membership = RwaMembership(
                        rwa_group_id=rwa_group_2.id,
                        user_id=collector2.id,
                        role="collector"
                    )
                    db.session.add(membership)
                
                # Add RWA managers to RWA groups as admins
                if rwa_manager1 and not RwaMembership.query.filter_by(user_id=rwa_manager1.id, rwa_group_id=rwa_group_1.id).first():
                    membership = RwaMembership(
                        rwa_group_id=rwa_group_1.id,
                        user_id=rwa_manager1.id,
                        role="admin"
                    )
                    db.session.add(membership)
                
                if rwa_manager2 and not RwaMembership.query.filter_by(user_id=rwa_manager2.id, rwa_group_id=rwa_group_2.id).first():
                    membership = RwaMembership(
                        rwa_group_id=rwa_group_2.id,
                        user_id=rwa_manager2.id,
                        role="admin"
                    )
                    db.session.add(membership)
                
                db.session.commit()
                print("✅ RWA memberships created for secondary users")
        
        print("✅ Database initialized with sample data")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize sample data: {e}")
        db.session.rollback()

