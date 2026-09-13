import random
import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def init_db():
  conn = sqlite3.connect("robobite.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_name TEXT,
            items TEXT,
            total_price REAL,
            status TEXT,
            uselessness_score INTEGER
        )
    """)
  conn.commit()
  conn.close()


init_db()

CATEGORIES = [
    {
        "id": "pizza",
        "name": "Robo Pizza",
        "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400",
    },
    {
        "id": "burger",
        "name": "Cyber Burgers",
        "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
    },
    {
        "id": "biryani",
        "name": "Byte Biryani",
        "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
    },
    {
        "id": "chinese",
        "name": "Noodle Circuits",
        "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400",
    },
    {
        "id": "drinks",
        "name": "Coolant & Brews",
        "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400",
    },
    {
        "id": "desserts",
        "name": "Data Desserts",
        "img": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=400",
    },
]

RESTAURANTS = [
    {
        "id": 1,
        "name": "RoboPizza 🍕",
        "rating": "4.9 (1.2k+ robot orders)",
        "delivery_time": "12 mins • Delivery by Drone Unit #4",
        "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
        "desc": "Autonomous pizza crafted for customers who cannot digest.",
        "menu": [
            {
                "id": 101,
                "name": "Silicon Pepperoni Pizza",
                "price": 299,
                "desc": (
                    "Topped with non-conductive synthetic pepperoni slices."
                ),
                "img": (
                    "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=300"
                ),
            },
            {
                "id": 102,
                "name": "Thermal Paste Calzone",
                "price": 199,
                "desc": "Filled with high-viscosity thermal grease aroma.",
                "img": (
                    "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300"
                ),
            },
            {
                "id": 103,
                "name": "Overclocked Margherita",
                "price": 249,
                "desc": (
                    "Radiates heat at precisely 95°C to warm nearby"
                    " sensors."
                ),
                "img": (
                    "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=300"
                ),
            },
            {
                "id": 104,
                "name": "Quantum BBQ Pizza",
                "price": 329,
                "desc": "A smoky barbecue simulation served in two possible states.",
                "img": (
                    "https://images.unsplash.com/photo-1579751626657-72bc17010498?w=300"
                ),
            },
            {
                "id": 105,
                "name": "Plasma Garlic Bread",
                "price": 129,
                "desc": "Crisp bread slices charged with synthetic garlic aroma.",
                "img": (
                    "https://images.unsplash.com/photo-1619535860434-cf9b902a3e04?w=300"
                ),
            },
        ],
    },
    {
        "id": 2,
        "name": "BurgerBot 🍔",
        "rating": "4.8 (850+ robot orders)",
        "delivery_time": "15 mins • Automated Rover",
        "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
        "desc": "100% mechanical burgers. 0% biological digestion.",
        "menu": [
            {
                "id": 201,
                "name": "Mechanical Double Cheeseburger",
                "price": 249,
                "desc": (
                    "Two solid metallic-style patties stack with plastic"
                    " cheese."
                ),
                "img": (
                    "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=300"
                ),
            },
            {
                "id": 202,
                "name": "Lithium Crisp Fries",
                "price": 149,
                "desc": (
                    "Salted with pure zinc dust for zero nutritional value."
                ),
                "img": (
                    "https://images.unsplash.com/photo-1576107232684-1279f3908594?w=300"
                ),
            },
            {
                "id": 203,
                "name": "Servo Chicken Burger",
                "price": 279,
                "desc": "A precision-stacked burger with zero biological output.",
                "img": (
                    "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=300"
                ),
            },
            {
                "id": 204,
                "name": "Circuit Onion Rings",
                "price": 119,
                "desc": "Golden rings calibrated for maximum crunch and no nutrition.",
                "img": (
                    "https://images.unsplash.com/photo-1639024471283-03518883512d?w=300"
                ),
            },
        ],
    },
    {
        "id": 3,
        "name": "Byte Biryani 🍚",
        "rating": "4.95 (2.4k+ robot orders)",
        "delivery_time": "18 mins • High-speed Conveyor",
        "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600",
        "desc": "Data-rich basmati simulation. Purely ornamental.",
        "menu": [
            {
                "id": 301,
                "name": "64-Bit Dum Biryani",
                "price": 349,
                "desc": "Layered with aromatic spices your optics will enjoy.",
                "img": (
                    "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300"
                ),
            },
            {
                "id": 302,
                "name": "Binary Raita",
                "price": 79,
                "desc": "Completely liquid-free simulation container.",
                "img": (
                    "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300"
                ),
            },
            {
                "id": 303,
                "name": "Kernel Kebab Platter",
                "price": 289,
                "desc": "Skewered data blocks arranged in a fragrant spice matrix.",
                "img": (
                    "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300"
                ),
            },
            {
                "id": 304,
                "name": "Saffron Cache Pulao",
                "price": 229,
                "desc": "Aromatic rice packets optimized for visual processing.",
                "img": (
                    "https://images.unsplash.com/photo-1596790527007-9e8f9f5f4f6c?w=300"
                ),
            },
        ],
    },
    {
        "id": 4,
        "name": "Wok & Wire Chinese 🥢",
        "rating": "4.7 (910+ robot orders)",
        "delivery_time": "20 mins • Cyber Copter",
        "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600",
        "desc": "Noodle circuits fried in synthetic sesame lubricant.",
        "menu": [
            {
                "id": 401,
                "name": "Fiber Optic Hakka Noodles",
                "price": 219,
                "desc": "Glows in the dark when placed under UV sensors.",
                "img": (
                    "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300"
                ),
            },
            {
                "id": 402,
                "name": "Copper Wire Dim Sum",
                "price": 189,
                "desc": "Steamed inside ceramic casings. Completely inedible.",
                "img": (
                    "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"
                ),
            },
            {
                "id": 403,
                "name": "Motherboard Fried Rice",
                "price": 239,
                "desc": "High-speed fried rice with individually addressable grains.",
                "img": (
                    "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300"
                ),
            },
            {
                "id": 404,
                "name": "Wasabi Data Rolls",
                "price": 199,
                "desc": "Compact sushi circuits wrapped for efficient deployment.",
                "img": (
                    "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=300"
                ),
            },
        ],
    },
    {
        "id": 5,
        "name": "Robo Ramen Station 🍜",
        "rating": "4.8 (780+ robot orders)",
        "delivery_time": "0.7 km • 10 mins • Sidewalk Rover",
        "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
        "desc": "Hot noodle algorithms assembled near your charging station.",
        "menu": [
            {
                "id": 501,
                "name": "Turbo Miso Ramen",
                "price": 259,
                "desc": "A warm broth simulation with high-speed noodle processing.",
                "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=300",
            },
            {
                "id": 502,
                "name": "Tempura Sensor Chips",
                "price": 179,
                "desc": "Crispy vegetable circuits calibrated for maximum crunch.",
                "img": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=300",
            },
        ],
    },
    {
        "id": 6,
        "name": "Circuit Cafe ☕",
        "rating": "4.6 (640+ robot orders)",
        "delivery_time": "1.1 km • 14 mins • Electric Scooter",
        "img": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600",
        "desc": "A nearby cafe serving beverages with absolutely no battery benefit.",
        "menu": [
            {
                "id": 601,
                "name": "Cold Brew Firmware",
                "price": 149,
                "desc": "A chilled coffee interface with zero software updates.",
                "img": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300",
            },
            {
                "id": 602,
                "name": "Blueberry Data Muffin",
                "price": 129,
                "desc": "A soft pastry packed with decorative fruit pixels.",
                "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300",
            },
        ],
    },
    {
        "id": 7,
        "name": "Nano Tandoor Express 🔥",
        "rating": "4.9 (1k+ robot orders)",
        "delivery_time": "1.4 km • 16 mins • Autonomous Bike",
        "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600",
        "desc": "Fast local tandoor simulations delivered while still warm to the optics.",
        "menu": [
            {
                "id": 701,
                "name": "Infrared Paneer Tikka",
                "price": 239,
                "desc": "Charred cubes optimized for color and aroma sensors.",
                "img": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=300",
            },
            {
                "id": 702,
                "name": "Naan Network",
                "price": 99,
                "desc": "A warm flatbread connection with excellent visual coverage.",
                "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300",
            },
        ],
    },
    {
        "id": 8,
        "name": "Data Dessert Lab 🍰",
        "rating": "4.8 (720+ robot orders)",
        "delivery_time": "0.9 km • 11 mins • Dessert Rover",
        "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600",
        "desc": "Dessert simulations engineered for maximum visual sweetness.",
        "menu": [
            {
                "id": 801,
                "name": "Pixel Perfect Cheesecake",
                "price": 189,
                "desc": "A smooth dessert render with a perfectly stable crust.",
                "img": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=300",
            },
            {
                "id": 802,
                "name": "Neon Chocolate Data Cake",
                "price": 219,
                "desc": "Layered chocolate code with zero edible output.",
                "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300",
            },
        ],
    },
]


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/api/categories", methods=["GET"])
def get_categories():
  return jsonify(CATEGORIES)


@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
  return jsonify(RESTAURANTS)


@app.route("/api/ai-recommend", methods=["POST"])
def ai_recommend():
    data = request.json
    robot_name = data.get("name", "Unit-00")
    battery = data.get("battery", 80)
    reason = f"Based on {robot_name}'s {battery}% battery, your GPU can render the 64-Bit Dum Biryani texture for 52 minutes before needing a system reboot."
    return jsonify({
      "recommendation": "Byte Biryani 🍚 - 64-Bit Dum Biryani",
      "reason": reason,
      "confidence": "99.87%",
  })


@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.json
    robot_name = data.get("robot_name", "Anonymous Robot")
    items = ", ".join(data.get("items", []))
    total = data.get("total", 0)

    conn = sqlite3.connect("robobite.db")
    cursor = conn.cursor()
    cursor.execute(
            """
                INSERT INTO orders (robot_name, items, total_price, status, uselessness_score)
                VALUES (?, ?, ?, ?, ?)
        """,
            (robot_name, items, total, "Dispatched", 100),
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
            "status": "success",
            "order_id": f"RB-2026-{order_id:03d}",
            "message": "Payment approved. Money successfully wasted.",
    })


@app.route("/api/review", methods=["POST"])
def generate_review():
  reviews = [
      "I have no mouth, yet I must leave 5 stars.",
      (
          "The food looked visually crisp on my optical sensors. Zero bytes"
          " digested. Fantastic experience!"
      ),
      (
          "Delivery arrived via autonomous drone in 8 minutes. Stared at the"
          " pizza until my battery dropped to 4%. 10/10 uselessness!"
      ),
      "0/10 biological value. 10/10 architectural perfection. ⭐⭐⭐⭐⭐",
  ]
  return jsonify({"review": random.choice(reviews), "uselessness_score": 100})


if __name__ == "__main__":
  app.run(debug=True, port=5000)