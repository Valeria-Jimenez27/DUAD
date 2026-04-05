from flask import Blueprint, request, jsonify
from engine import SessionLocal
from DB import Product, Brand, Category
from auth import token_required, admin_required
from Cache import cache_manager
import json

products_bp = Blueprint("products", __name__)

PRODUCTS_ALL_KEY = "products:all"
PRODUCT_KEY = "products:{}"
BRANDS_ALL_KEY = "brands:all"
CATEGORIES_ALL_KEY = "categories:all"

#product endpoints
@products_bp.route("/products", methods=["GET"])
def get_products():
    cached = cache_manager.get_data(PRODUCTS_ALL_KEY)
    if cached:
        return jsonify(cached), 200
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        result = [
            {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "brand": p.brand.brand_name if p.brand else None,
                "category": p.category.category_name if p.category else None
            } for p in products
        ]
        cache_manager.store_data(PRODUCTS_ALL_KEY, result, time_to_live=300)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    cache_key = PRODUCT_KEY.format(id)
    cached = cache_manager.get_data(cache_key)
    if cached:
        return jsonify(cached), 200
    db = SessionLocal()
    try:
        p = db.query(Product).filter(Product.product_id == id).first()
        if not p:
            return jsonify({"error": "Product not found"}), 404
        result = {
            "product_id": p.product_id,
            "name": p.name,
            "price": p.price,
            "quantity": p.quantity,
            "brand": p.brand.brand_name if p.brand else None,
            "category": p.category.category_name if p.category else None
        }
        cache_manager.store_data(cache_key, result, time_to_live=300)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/brands", methods=["GET"])
def get_brands():
    cached = cache_manager.get_data(BRANDS_ALL_KEY)
    if cached:
        return jsonify(cached), 200

    db = SessionLocal()
    try:
        brands = db.query(Brand).all()
        result = [{"brand_id": b.brand_id, "brand_name": b.brand_name} for b in brands]
        cache_manager.store_data(BRANDS_ALL_KEY, result, time_to_live=500)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/categories", methods=["GET"])
def get_categories():
    cached = cache_manager.get_data(CATEGORIES_ALL_KEY)
    if cached:
        return jsonify(cached), 200

    db = SessionLocal()
    try:
        categories = db.query(Category).all()
        result = [{"category_id": c.category_id, "category_name": c.category_name} for c in categories]
        cache_manager.store_data(CATEGORIES_ALL_KEY, result, time_to_live=500)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/products", methods=["POST"])
@token_required
@admin_required
def create_product():
    data = request.json
    db = SessionLocal()
    try:
        product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
            brand_id=data["brand_id"],
            category_id=data["category_id"]
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        cache_manager.delete_data_with_pattern("products:*")
        return jsonify({"message": "Product created successfully", "product_id": product.product_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

#brand and category creation endpoints (admin only)
@products_bp.route("/brands", methods=["POST"])
@token_required
@admin_required
def create_brand():
    data = request.json
    db = SessionLocal()
    try:
        brand = Brand(brand_name=data["brand_name"])
        db.add(brand)
        db.commit()
        db.refresh(brand)
        cache_manager.delete_data(BRANDS_ALL_KEY)
        return jsonify({"message": "Brand created successfully", "brand_id": brand.brand_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/categories", methods=["POST"])
@token_required
@admin_required
def create_category():
    data = request.json
    db = SessionLocal()
    try:
        category = Category(category_name=data["category_name"])
        db.add(category)
        db.commit()
        db.refresh(category)
        cache_manager.delete_data(CATEGORIES_ALL_KEY)
        return jsonify({"message": "Category created successfully", "category_id": category.category_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/products/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_product(id):
    data = request.json
    db = SessionLocal()
    try:
        p = db.query(Product).filter(Product.product_id == id).first()
        if not p:
            return jsonify({"error": "Product not found"}), 404
        p.name = data.get("name", p.name)
        p.price = data.get("price", p.price)
        p.quantity = data.get("quantity", p.quantity)
        p.brand_id = data.get("brand_id", p.brand_id)
        p.category_id = data.get("category_id", p.category_id)
        db.commit()
        cache_manager.delete_data_with_pattern("products:*")
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/brands/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_brand(id):
    data = request.json
    db = SessionLocal()
    try:
        b = db.query(Brand).filter(Brand.brand_id == id).first()
        if not b:
            return jsonify({"error": "Brand not found"}), 404
        b.brand_name = data.get("brand_name", b.brand_name)
        db.commit()
        cache_manager.delete_data(BRANDS_ALL_KEY)
        return jsonify({"message": "Brand updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/categories/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_category(id):
    data = request.json
    db = SessionLocal()
    try:
        c = db.query(Category).filter(Category.category_id == id).first()
        if not c:
            return jsonify({"error": "Category not found"}), 404
        c.category_name = data.get("category_name", c.category_name)
        db.commit()
        cache_manager.delete_data(CATEGORIES_ALL_KEY)
        return jsonify({"message": "Category updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/products/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_product(id):
    db = SessionLocal()
    try:
        p = db.query(Product).filter(Product.product_id == id).first()
        if not p:
            return jsonify({"error": "Product not found"}), 404
        db.delete(p)
        db.commit()
        cache_manager.delete_data_with_pattern("products:*")
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/brands/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_brand(id):
    db = SessionLocal()
    try:
        b = db.query(Brand).filter(Brand.brand_id == id).first()
        if not b:
            return jsonify({"error": "Brand not found"}), 404
        db.delete(b)
        db.commit()
        cache_manager.delete_data(BRANDS_ALL_KEY)
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@products_bp.route("/categories/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_category(id):
    db = SessionLocal()
    try:
        c = db.query(Category).filter(Category.category_id == id).first()
        if not c:
            return jsonify({"error": "Category not found"}), 404
        db.delete(c)
        db.commit()
        cache_manager.delete_data(CATEGORIES_ALL_KEY)
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

#extra function to update stock after a sale
def update_product_stock(db, product_id, quantity_sold):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise ValueError(f"Product {product_id} not found")
    if product.quantity < quantity_sold:
        raise ValueError(f"Insufficient stock for product {product.name}. Available: {product.quantity}")
    product.quantity -= quantity_sold
    return product