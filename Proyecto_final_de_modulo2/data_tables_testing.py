from dotenv import load_dotenv
load_dotenv()

from engine import SessionLocal
from DB import Brand, Category, Product

db = SessionLocal()

try:
    brands = [
        Brand(brand_id=1, brand_name="NutriSource"),
        Brand(brand_id=2, brand_name="Balance"),
        Brand(brand_id=3, brand_name="Hills"),
        Brand(brand_id=4, brand_name="1st Choice"),
        Brand(brand_id=5, brand_name="Zeedog"),
        Brand(brand_id=6, brand_name="Cannaluv"),
        Brand(brand_id=7, brand_name="Nexgard"),
    ]
    db.add_all(brands)
    db.commit()
    print("Brands inserted successfully!")


    categories = [
        Category(category_id=1, category_name="Dog Food"),
        Category(category_id=2, category_name="Cat Food"),
        Category(category_id=3, category_name="Pet Accessories"),
        Category(category_id=4, category_name="Health"),
    ]
    db.add_all(categories)
    db.commit()
    print("Categories inserted successfully!")


    products = [
        Product(name="Nutrisource Large Breed 11.7kg",      price=65.00,  quantity=30, brand_id=1, category_id=1),
        Product(name="Balance Active Dog 15kg",              price=110.00, quantity=27, brand_id=2, category_id=1),
        Product(name="Balance Chicken and Rice puppy 2kg",   price=40.00,  quantity=50, brand_id=2, category_id=1),
        Product(name="Nutrisource Beef and Rice 11.7kg",     price=90.00,  quantity=45, brand_id=1, category_id=1),
        Product(name="Hills sensitive skin feline 3.17kg",   price=32.00,  quantity=34, brand_id=3, category_id=2),
        Product(name="Hills urinary care feline 2.8kg",      price=70.00,  quantity=22, brand_id=3, category_id=2),
        Product(name="Hills multibenefit feline 1.8kg",      price=58.00,  quantity=10, brand_id=3, category_id=2),
        Product(name="1st Choice Hypoallergenic 16 kg",      price=120.00, quantity=12, brand_id=4, category_id=1),
        Product(name="Balance Chicken senior 15kg",          price=100.00, quantity=25, brand_id=2, category_id=1),
        Product(name="Hills Dermcomplete 2.8kg",             price=62.00,  quantity=8,  brand_id=3, category_id=1),
        Product(name="Zeedog stars harness",                 price=40.00,  quantity=4,  brand_id=5, category_id=3),
        Product(name="Zeedog pink harness",                  price=35.00,  quantity=3,  brand_id=5, category_id=3),
        Product(name="Cannaluv CBD oil 500mg",               price=42.00,  quantity=5,  brand_id=6, category_id=4),
        Product(name="Nexgard Spectra 3.6-10kg",             price=20.00,  quantity=10, brand_id=7, category_id=4),
        Product(name="Nexgard Spectra 10-15kg",              price=25.00,  quantity=12, brand_id=7, category_id=4),
    ]
    db.add_all(products)
    db.commit()
    print("Products inserted successfully!")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()