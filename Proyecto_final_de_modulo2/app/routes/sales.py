from flask import Blueprint, request, jsonify
from app.database.engine import SessionLocal
from app.models.DB import ShoppingCart, CartItem, Order, OrderDetail, Customer, Product
from app.services.auth import token_required, admin_required
from app.routes.products import update_product_stock
from app.services.Cache import cache_manager
from datetime import datetime

sales_bp = Blueprint("sales", __name__)

INVOICE_KEY = "invoice:{}"
ORDERS_ALL_KEY = "orders:all"

#shopping cart endpoints
@sales_bp.route("/carts", methods=["POST"])
@token_required
def create_cart():
    data = request.json
    db = SessionLocal()
    try:
        existing_cart = db.query(ShoppingCart).filter(
            ShoppingCart.customer_id == data["customer_id"],
            ShoppingCart.is_active == True
        ).first()
        if existing_cart:
            return jsonify({"message": "Customer already has an active cart", "cart_id": existing_cart.cart_id}), 200
        cart = ShoppingCart(customer_id=data["customer_id"])
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return jsonify({"message": "Cart created", "cart_id": cart.cart_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/carts/<int:cart_id>", methods=["GET"])
@token_required
def get_cart(cart_id):
    db = SessionLocal()
    try:
        cart = db.query(ShoppingCart).filter(ShoppingCart.cart_id == cart_id).first()
        if not cart:
            return jsonify({"error": "Cart not found"}), 404
        items = []
        for item in cart.items:
            product = item.product
            items.append({
                "cart_item_id": item.cart_item_id,
                "product_id": item.product_id,
                "product_name": product.name if product else None,
                "unit_price": product.price if product else None,
                "quantity": item.quantity,
                "subtotal": product.price * item.quantity if product else None
            })
        return jsonify({
            "cart_id": cart.cart_id,
            "customer_id": cart.customer_id,
            "created_at": str(cart.created_at),
            "is_active": cart.is_active,
            "items": items,
            "total": sum(i["subtotal"] for i in items if i["subtotal"])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/carts/customer/<int:customer_id>", methods=["GET"])
@token_required
def get_customer_carts(customer_id):
    db = SessionLocal()
    try:
        carts = db.query(ShoppingCart).filter(
            ShoppingCart.customer_id == customer_id,
            ShoppingCart.is_active == True
        ).all()
        result = [{"cart_id": c.cart_id, "created_at": str(c.created_at)} for c in carts]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/carts/<int:cart_id>/items", methods=["POST"])
@token_required
def add_item_to_cart(cart_id):
    data = request.json
    db = SessionLocal()
    try:
        cart = db.query(ShoppingCart).filter(
            ShoppingCart.cart_id == cart_id,
            ShoppingCart.is_active == True
        ).first()
        if not cart:
            return jsonify({"error": "Active cart not found"}), 404
        product = db.query(Product).filter(Product.product_id == data["product_id"]).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        if product.quantity < data["quantity"]:
            return jsonify({"error": f"Insufficient stock. Available: {product.quantity}"}), 400
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == data["product_id"]
        ).first()
        if existing_item:
            existing_item.quantity += data["quantity"]
        else:
            item = CartItem(cart_id=cart_id, product_id=data["product_id"], quantity=data["quantity"])
            db.add(item)
        db.commit()
        return jsonify({"message": "Item added to cart"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/carts/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
@token_required
def remove_item_from_cart(cart_id, item_id):
    db = SessionLocal()
    try:
        item = db.query(CartItem).filter(
            CartItem.cart_item_id == item_id,
            CartItem.cart_id == cart_id
        ).first()
        if not item:
            return jsonify({"error": "Item not found"}), 404
        db.delete(item)
        db.commit()
        return jsonify({"message": "Item removed from cart"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


#sales endpoints
@sales_bp.route("/carts/<int:cart_id>/checkout", methods=["POST"])
@token_required
def checkout(cart_id):
    data = request.json
    db = SessionLocal()
    try:
        cart = db.query(ShoppingCart).filter(
            ShoppingCart.cart_id == cart_id,
            ShoppingCart.is_active == True
        ).first()
        if not cart:
            return jsonify({"error": "Active cart not found"}), 404
        if not cart.items:
            return jsonify({"error": "Cart is empty"}), 400
        if not data.get("billing_address"):
            return jsonify({"error": "Billing address is required"}), 400
        if not data.get("payment_method"):
            return jsonify({"error": "Payment method is required"}), 400
        total = 0
        order_details = []
        for item in cart.items:
            product = update_product_stock(db, item.product_id, item.quantity)
            subtotal = product.price * item.quantity
            total += subtotal
            order_details.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": product.price
            })

        order = Order(
            customer_id=cart.customer_id,
            total_amount=total,
            billing_address=data["billing_address"],
            payment_method=data["payment_method"],
            order_date=datetime.now()
        )
        db.add(order)
        db.flush()

        for detail in order_details:
            db.add(OrderDetail(
                order_id=order.order_id,
                product_id=detail["product_id"],
                quantity=detail["quantity"],
                unit_price=detail["unit_price"]
            ))

        cart.is_active = False
        db.commit()
        cache_manager.delete_data_with_pattern("invoice:*")
        cache_manager.delete_data(ORDERS_ALL_KEY)
        cache_manager.delete_data_with_pattern("products:*")
        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.order_id,
            "total_amount": total,
            "billing_address": order.billing_address,
            "payment_method": order.payment_method
        }), 201
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

#Invoices and order management endpoints
@sales_bp.route("/orders/<int:order_id>/invoice", methods=["GET"])
@token_required
def get_invoice(order_id):
    cache_key = INVOICE_KEY.format(order_id)
    cached = cache_manager.get_data(cache_key)
    if cached:
        return jsonify({"invoice": cached}), 200

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404
        customer = db.query(Customer).filter(Customer.customer_id == order.customer_id).first()
        items = []
        for detail in order.details:
            product = detail.product
            items.append({
                "product_id": detail.product_id,
                "product_name": product.name if product else None,
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "subtotal": detail.quantity * detail.unit_price
            })
        invoice_data = {
            "order_id": order.order_id,
            "order_date": str(order.order_date),
            "customer": {
                "customer_id": customer.customer_id,
                "name": f"{customer.first_name} {customer.last_name}",
                "email": customer.email,
                "phone": customer.phone
            },
            "billing_address": order.billing_address,
            "payment_method": order.payment_method,
            "items": items,
            "total_amount": order.total_amount,
            "status": order.status
        }
        cache_manager.store_data(cache_key, invoice_data, time_to_live=600)
        return jsonify({"invoice": invoice_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/orders", methods=["GET"])
@token_required
@admin_required
def get_orders():
    cached = cache_manager.get_data(ORDERS_ALL_KEY)
    if cached:
        return jsonify(cached), 200

    db = SessionLocal()
    try:
        orders = db.query(Order).all()
        result = [
            {
                "order_id": o.order_id,
                "customer_id": o.customer_id,
                "order_date": str(o.order_date),
                "total_amount": o.total_amount,
                "status": o.status
            } for o in orders
        ]
        cache_manager.store_data(ORDERS_ALL_KEY, result, time_to_live=120)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@sales_bp.route("/orders/<int:order_id>/refund", methods=["POST"])
@token_required
@admin_required
def refund_order(order_id):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404
        if order.status == "refunded":
            return jsonify({"error": "Order already refunded"}), 400
        for detail in order.details:
            product = db.query(Product).filter(Product.product_id == detail.product_id).first()
            if product:
                product.quantity += detail.quantity
        order.status = "refunded"
        
        db.commit()
        cache_manager.delete_data(INVOICE_KEY.format(order_id))
        cache_manager.delete_data(ORDERS_ALL_KEY)
        cache_manager.delete_data_with_pattern("products:*")
        return jsonify({
            "message": "Order refunded successfully",
            "order_id": order.order_id,
            "refunded_amount": order.total_amount
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()