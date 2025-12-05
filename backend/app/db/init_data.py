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
                },
                {
                    
                    "name": "Plastic-Free Neighborhood Drive",
                    "description": "Join us for a hands-on community initiative to reduce single-use plastics and promote sustainable alternatives.",
                    "event_datetime": datetime(2026, 3, 5, 10, 30),
                    "location": "BD Market Park, Salt Lake",
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
            
            # Create sample recycler locations with coordinates for Kolkata (pincode 700001)
            # Coordinates are approximate locations in Kolkata area
            recyclers_data = [
                {
                    "name": "GreenCycle Recyclers",
                    "address": "123, Girish Park, Kolkata-700031",
                    "pincode": "700001",
                    "phone": "+91 98765 43210",
                    "website": "https://greencyclerecyclers.com",
                    "ward_id": ward_1.id,
                    "latitude": 22.5726,  # Approximate Kolkata coordinates
                    "longitude": 88.3639
                },
                {
                    "name": "Hazardous E-Waste Solutions Hub",
                    "address": "45, Bypass Road, Kolkata 700002",
                    "pincode": "700001",
                    "phone": "+91 9123456789",
                    "website": "https://ewastesolutions.com",
                    "ward_id": ward_1.id,
                    "latitude": 22.5626,
                    "longitude": 88.3630
                },
                {
                    "name": "Goonj",
                    "address": "10, Central Avenue, Kolkata-700041",
                    "pincode": "700001",
                    "phone": "+91 76543 21098",
                    "website": "https://goonj.org",
                    "ward_id": ward_1.id,
                    "latitude": 22.5826,
                    "longitude": 88.3739
                },
                {
                    "name": "Green Recyclers",
                    "address": "123 Main Street, Park Street",
                    "pincode": "700001",
                    "phone": "+91-9876543210",
                    "website": "https://greenrecyclers.com",
                    "ward_id": ward_1.id,
                    "latitude": 22.5526,
                    "longitude": 88.3539
                },
                {
                    "name": "Eco Waste Solutions",
                    "address": "456 Eco Road, Salt Lake",
                    "pincode": "700064",
                    "phone": "+91-9876543211",
                    "website": None,
                    "ward_id": ward_2.id,
                    "latitude": 22.5726,
                    "longitude": 88.4039
                }
            ]
            
            for rec_data in recyclers_data:
                existing_recycler = RecyclerLocation.query.filter_by(name=rec_data["name"]).first()
                if not existing_recycler:
                    recycler = RecyclerLocation(**rec_data)
                    db.session.add(recycler)
                else:
                    # Update existing recycler with coordinates and other details if missing
                    updated = False
                    if not existing_recycler.latitude or not existing_recycler.longitude:
                        existing_recycler.latitude = rec_data.get("latitude")
                        existing_recycler.longitude = rec_data.get("longitude")
                        updated = True
                    
                    if rec_data.get("address") and (not existing_recycler.address or existing_recycler.address != rec_data["address"]):
                        existing_recycler.address = rec_data["address"]
                        updated = True
                    
                    if rec_data.get("phone") and (not existing_recycler.phone or existing_recycler.phone != rec_data["phone"]):
                        existing_recycler.phone = rec_data["phone"]
                        updated = True
                    
                    if rec_data.get("website") is not None and existing_recycler.website != rec_data["website"]:
                        existing_recycler.website = rec_data["website"]
                        updated = True
                    
                    if rec_data.get("pincode") and existing_recycler.pincode != rec_data["pincode"]:
                        existing_recycler.pincode = rec_data["pincode"]
                        updated = True
                    
                    if rec_data.get("ward_id") and existing_recycler.ward_id != rec_data["ward_id"]:
                        existing_recycler.ward_id = rec_data["ward_id"]
                        updated = True
            
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


def update_recyclers_data():
    """Update existing recyclers with coordinates and add new ones."""
    try:
        ward_1 = Ward.query.filter_by(ward_number="1").first()
        ward_2 = Ward.query.filter_by(ward_number="2").first()
        
        if not ward_1:
            print("❌ Error: Ward 1 not found. Please run database initialization first.")
            return
        
        # Recycler data with coordinates
        recyclers_data = [
            {
                "name": "GreenCycle Recyclers",
                "address": "123, Girish Park, Kolkata-700031",
                "pincode": "700001",
                "phone": "+91 98765 43210",
                "website": "https://greencyclerecyclers.com",
                "ward_id": ward_1.id,
                "latitude": 22.5726,
                "longitude": 88.3639
            },
            {
                "name": "Hazardous E-Waste Solutions Hub",
                "address": "45, Bypass Road, Kolkata 700002",
                "pincode": "700001",
                "phone": "+91 9123456789",
                "website": "https://ewastesolutions.com",
                "ward_id": ward_1.id,
                "latitude": 22.5626,
                "longitude": 88.3630
            },
            {
                "name": "Goonj",
                "address": "10, Central Avenue, Kolkata-700041",
                "pincode": "700001",
                "phone": "+91 76543 21098",
                "website": "https://goonj.org",
                "ward_id": ward_1.id,
                "latitude": 22.5826,
                "longitude": 88.3739
            },
            {
                "name": "Green Recyclers",
                "address": "123 Main Street, Park Street",
                "pincode": "700001",
                "phone": "+91-9876543210",
                "website": "https://greenrecyclers.com",
                "ward_id": ward_1.id,
                "latitude": 22.5526,
                "longitude": 88.3539
            },
            {
                "name": "Eco Waste Solutions",
                "address": "456 Eco Road, Salt Lake",
                "pincode": "700064",
                "phone": "+91-9876543211",
                "website": None,
                "ward_id": ward_2.id if ward_2 else ward_1.id,
                "latitude": 22.5726,
                "longitude": 88.4039
            }
        ]
        
        added_count = 0
        updated_count = 0
        
        print("=" * 60)
        print("Updating Recyclers with Coordinates")
        print("=" * 60)
        
        for rec_data in recyclers_data:
            existing_recycler = RecyclerLocation.query.filter_by(name=rec_data["name"]).first()
            
            if not existing_recycler:
                recycler = RecyclerLocation(**rec_data)
                db.session.add(recycler)
                added_count += 1
                print(f"✅ Added: {rec_data['name']}")
            else:
                updated = False
                updates = []
                
                if not existing_recycler.latitude or not existing_recycler.longitude:
                    existing_recycler.latitude = rec_data.get("latitude")
                    existing_recycler.longitude = rec_data.get("longitude")
                    updated = True
                    updates.append("coordinates")
                
                if rec_data.get("address") and (not existing_recycler.address or existing_recycler.address != rec_data["address"]):
                    existing_recycler.address = rec_data["address"]
                    updated = True
                    updates.append("address")
                
                if rec_data.get("phone") and (not existing_recycler.phone or existing_recycler.phone != rec_data["phone"]):
                    existing_recycler.phone = rec_data["phone"]
                    updated = True
                    updates.append("phone")
                
                if rec_data.get("website") is not None and existing_recycler.website != rec_data["website"]:
                    existing_recycler.website = rec_data["website"]
                    updated = True
                    updates.append("website")
                
                if rec_data.get("pincode") and existing_recycler.pincode != rec_data["pincode"]:
                    existing_recycler.pincode = rec_data["pincode"]
                    updated = True
                    updates.append("pincode")
                
                if rec_data.get("ward_id") and existing_recycler.ward_id != rec_data["ward_id"]:
                    existing_recycler.ward_id = rec_data["ward_id"]
                    updated = True
                    updates.append("ward_id")
                
                if updated:
                    updated_count += 1
                    print(f"🔄 Updated: {rec_data['name']} ({', '.join(updates)})")
        
        db.session.commit()
        
        total_recyclers = RecyclerLocation.query.filter_by(is_active=True).count()
        recyclers_with_coords = RecyclerLocation.query.filter(
            RecyclerLocation.latitude.isnot(None),
            RecyclerLocation.longitude.isnot(None),
            RecyclerLocation.is_active == True
        ).count()
        
        print("=" * 60)
        print(f"✅ Update completed!")
        print(f"   - Added: {added_count} recyclers")
        print(f"   - Updated: {updated_count} recyclers")
        print(f"   - Total active recyclers: {total_recyclers}")
        print(f"   - Recyclers with coordinates: {recyclers_with_coords}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error updating recyclers: {str(e)}")
        db.session.rollback()
        import traceback
        traceback.print_exc()
        raise

