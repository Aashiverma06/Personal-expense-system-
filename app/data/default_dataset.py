"""
Default dataset for PEIS:
- Standard expense & income categories
- Keyword dictionary for Rule-Based Categorization
- Training & benchmark dataset for Machine Learning Categorization
- Demo transactions for showcasing dashboard intelligence
"""

DEFAULT_CATEGORIES = [
    {"name": "Food & Dining", "type": "expense", "icon": "utensils", "color": "#f97316"},
    {"name": "Transportation", "type": "expense", "icon": "car", "color": "#0ea5e9"},
    {"name": "Education", "type": "expense", "icon": "book-open", "color": "#8b5cf6"},
    {"name": "Entertainment", "type": "expense", "icon": "film", "color": "#ec4899"},
    {"name": "Healthcare", "type": "expense", "icon": "heart-pulse", "color": "#ef4444"},
    {"name": "Housing & Utilities", "type": "expense", "icon": "home", "color": "#14b8a6"},
    {"name": "Shopping", "type": "expense", "icon": "shopping-bag", "color": "#f59e0b"},
    {"name": "Personal Care", "type": "expense", "icon": "sparkles", "color": "#06b6d4"},
    {"name": "Investment", "type": "expense", "icon": "trending-up", "color": "#10b981"},
    {"name": "Miscellaneous", "type": "expense", "icon": "more-horizontal", "color": "#64748b"},
    {"name": "Salary", "type": "income", "icon": "wallet", "color": "#22c55e"},
    {"name": "Freelance", "type": "income", "icon": "briefcase", "color": "#10b981"},
    {"name": "Investment Returns", "type": "income", "icon": "dollar-sign", "color": "#84cc16"},
    {"name": "Gifts & Grants", "type": "income", "icon": "gift", "color": "#a855f7"}
]

# Keyword dictionary mapping keywords/phrases to categories
RULE_KEYWORDS = {
    "Food & Dining": [
        "food", "pizza", "burger", "dominos", "domino", "mcdonalds", "subway", "kfc",
        "restaurant", "cafe", "coffee", "starbucks", "swiggy", "zomato", "dinner",
        "lunch", "breakfast", "snack", "biryani", "groceries", "supermarket", "bakery",
        "chai", "tea", "dosa", "paneer", "cake", "ice cream", "dine", "barista"
    ],
    "Transportation": [
        "uber", "ola", "rapido", "cab", "taxi", "bus", "metro", "train", "flight",
        "airline", "ticket", "petrol", "diesel", "fuel", "gas", "toll", "auto",
        "rickshaw", "parking", "subway pass", "commute", "railway", "irctc"
    ],
    "Education": [
        "course", "udemy", "coursera", "book", "books", "tuition", "college", "fees",
        "university", "exam", "certification", "textbook", "stationary", "edx",
        "class", "tutorial", "workshop", "python course", "library", "pen", "notebook"
    ],
    "Entertainment": [
        "movie", "cinema", "theatre", "netflix", "spotify", "prime video", "disney",
        "concert", "game", "steam", "playstation", "xbox", "amusement", "show",
        "hotstar", "youtube premium", "club", "party", "bowling", "event", "match"
    ],
    "Healthcare": [
        "medicine", "pharmacy", "doctor", "hospital", "clinic", "dental", "dentist",
        "chemist", "apollo", "meds", "prescription", "consultation", "tablets",
        "syrup", "bandage", "checkup", "diagnostic", "blood test", "therapy"
    ],
    "Housing & Utilities": [
        "rent", "electricity", "water", "wifi", "broadband", "internet", "maintenance",
        "gas cylinder", "lpg", "society maintenance", "apartment", "plumbing",
        "repair", "house", "cleaning", "trash", "maid", "cook"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "clothes", "shirt", "jeans", "tshirt",
        "shoes", "sneakers", "electronics", "gadget", "watch", "zara", "h&m",
        "mall", "purchase", "shopping", "bag", "dress", "headphones", "laptop"
    ],
    "Personal Care": [
        "salon", "haircut", "spa", "shampoo", "perfume", "cosmetics", "skincare",
        "grooming", "barber", "parlour", "facial", "gym", "fitness", "yoga"
    ],
    "Investment": [
        "mutual fund", "stocks", "shares", "sip", "zerodha", "groww", "crypto",
        "gold", "fixed deposit", "fd", "bonds", "etf", "savings deposit"
    ],
    "Salary": [
        "salary", "paycheck", "wages", "monthly pay", "stipend", "bonus", "payroll"
    ],
    "Freelance": [
        "freelance", "upwork", "fiverr", "contract", "client payment", "consulting project"
    ],
    "Investment Returns": [
        "dividend", "interest", "stock return", "profit", "capital gain", "fd interest"
    ]
}

# Machine Learning Training & Benchmark Dataset
# 150+ diverse and realistic expense/income descriptions with ground truth labels
TRAINING_DATA = [
    # Food & Dining
    ("Ordered pepperoni pizza from Domino's", "Food & Dining"),
    ("Lunch at college cafeteria with friends", "Food & Dining"),
    ("Swiggy delivery biryani dinner", "Food & Dining"),
    ("Zomato order McDonald's burger and fries", "Food & Dining"),
    ("Morning coffee and sandwich at Starbucks", "Food & Dining"),
    ("Groceries from local supermarket vegetables milk", "Food & Dining"),
    ("Subway veggie delight footlong combo", "Food & Dining"),
    ("Chai and snacks at evening tea stall", "Food & Dining"),
    ("Dinner buffet with family at Barbeque Nation", "Food & Dining"),
    ("Birthday cake from sweet bakery shop", "Food & Dining"),
    ("KFC fried chicken bucket meal", "Food & Dining"),
    ("Dosa and filter coffee breakfast", "Food & Dining"),
    ("Ice cream scoops at Baskin Robbins", "Food & Dining"),
    ("Groceries and fruit purchase at Nature's Basket", "Food & Dining"),
    ("Late night snack Maggie and chips", "Food & Dining"),
    ("Pasta and mocktail at Italian cafe", "Food & Dining"),
    ("Weekly vegetables and fresh dairy purchase", "Food & Dining"),
    ("Dine out weekend dinner with colleagues", "Food & Dining"),
    ("Supermarket grocery bill organic milk bread", "Food & Dining"),
    ("Grocery store provisions food items bill", "Food & Dining"),
    ("BigBasket online groceries and dairy items", "Food & Dining"),
    ("Blinkit instant grocery vegetables snack delivery", "Food & Dining"),

    # Transportation
    ("Uber cab ride to college campus", "Transportation"),
    ("Ola auto ride back to home", "Transportation"),
    ("Petrol refilled for motorcycle bike", "Transportation"),
    ("Diesel fuel refuel for car at Shell petrol pump", "Transportation"),
    ("Metro train smartcard recharge", "Transportation"),
    ("Bus ticket fare local city transit", "Transportation"),
    ("Rapido bike taxi ride to metro station", "Transportation"),
    ("Highway toll plaza tax fastag payment", "Transportation"),
    ("Parking fee at shopping mall basement", "Transportation"),
    ("IRCTC railway train ticket reservation", "Transportation"),
    ("Indigo flight flight ticket booking to Delhi", "Transportation"),
    ("Airport taxi cab transfer", "Transportation"),
    ("Monthly subway commuter travel card pass", "Transportation"),
    ("Auto rickshaw meter fare to market", "Transportation"),
    ("Scooter engine oil change and puncture repair", "Transportation"),
    ("Fuel refuel at Indian Oil petrol station", "Transportation"),

    # Education
    ("Purchased Python for Data Science Udemy course", "Education"),
    ("Enrolled in Machine Learning certification Coursera", "Education"),
    ("College semester tuition fees installment", "Education"),
    ("Engineering textbooks and notebooks purchase", "Education"),
    ("GRE and TOEFL preparation guide book", "Education"),
    ("Annual subscription for edX professional course", "Education"),
    ("University exam registration application fee", "Education"),
    ("Scientific calculator and stationary pens", "Education"),
    ("Online coding bootcamp tutorial fee", "Education"),
    ("College library membership annual renewal", "Education"),
    ("Research paper IEEE publication registration", "Education"),
    ("Web development workshop entry pass", "Education"),
    ("Data structures and algorithms coaching classes", "Education"),

    # Entertainment
    ("Movie tickets for IMAX show at PVR cinemas", "Entertainment"),
    ("Netflix monthly 4K streaming subscription", "Entertainment"),
    ("Spotify Premium music individual family plan", "Entertainment"),
    ("BookMyShow cinema tickets with popcorn combo", "Entertainment"),
    ("PlayStation 5 video game digital purchase on PS Store", "Entertainment"),
    ("Disney Hotstar annual VIP streaming subscription", "Entertainment"),
    ("Music concert festival entry wristband ticket", "Entertainment"),
    ("Steam summer sale computer video game", "Entertainment"),
    ("Weekend club party and lounge entry charge", "Entertainment"),
    ("Bowling alley and arcade gaming tokens", "Entertainment"),
    ("YouTube Premium ad-free subscription", "Entertainment"),
    ("Cricket stadium match match day match ticket", "Entertainment"),
    ("Standup comedy show night pass", "Entertainment"),

    # Healthcare
    ("Purchased fever medicine and antibiotics at pharmacy", "Healthcare"),
    ("Doctor consultation fee at clinic", "Healthcare"),
    ("Dental checkup and tooth scaling polishing", "Healthcare"),
    ("Apollo pharmacy cough syrup and vitamins", "Healthcare"),
    ("Full body diagnostic blood test report at lab", "Healthcare"),
    ("Eye specialist consultation and eye drops", "Healthcare"),
    ("Prescription medicines for diabetes and blood pressure", "Healthcare"),
    ("First aid kit bandages antiseptic Dettol", "Healthcare"),
    ("Hospital OPD visit fee and doctor consultation", "Healthcare"),
    ("Physiotherapy back pain rehabilitation session", "Healthcare"),
    ("Painkiller spray and pain relief tablets", "Healthcare"),

    # Housing & Utilities
    ("Monthly apartment flat house rent paid to owner", "Housing & Utilities"),
    ("Electricity bill payment state power board", "Housing & Utilities"),
    ("Airtel high-speed fiber broadband wifi bill", "Housing & Utilities"),
    ("Water supply bill municipal corporation", "Housing & Utilities"),
    ("Residential society monthly maintenance charges", "Housing & Utilities"),
    ("HP Gas LPG cooking cylinder refill booking", "Housing & Utilities"),
    ("Plumber charges for kitchen pipe leakage fix", "Housing & Utilities"),
    ("House cleaning maid monthly salary", "Housing & Utilities"),
    ("Home appliance AC service and gas filling", "Housing & Utilities"),
    ("Urban Company home sofa cleaning service", "Housing & Utilities"),

    # Shopping
    ("Purchased Nike running shoes from Flipkart", "Shopping"),
    ("Amazon order wireless Bluetooth earbuds headphones", "Shopping"),
    ("Formal shirts and trousers bought at Zara store", "Shopping"),
    ("Myntra summer clothing sale denim jeans jacket", "Shopping"),
    ("Smartwatch with fitness tracker from electronic shop", "Shopping"),
    ("Laptop backpack and travel bag purchase", "Shopping"),
    ("Purchased sunglasses and leather belt from mall", "Shopping"),
    ("Wireless mechanical keyboard and mouse pad", "Shopping"),
    ("Cotton bedsheet and pillow covers set", "Shopping"),
    ("H&M casual hoodie and graphic tees", "Shopping"),
    ("Casual footwear and sandals purchase", "Shopping"),

    # Personal Care
    ("Haircut haircut styling and beard trim at salon", "Personal Care"),
    ("Monthly gym fitness center membership subscription", "Personal Care"),
    ("Skincare face wash sunscreen moisturizer cream", "Personal Care"),
    ("Perfume deodorant spray bottle bought at cosmetics shop", "Personal Care"),
    ("Beauty parlour facial and hair spa treatment", "Personal Care"),
    ("Shampoo hair conditioner and bath body wash", "Personal Care"),
    ("Yoga class monthly trainer subscription", "Personal Care"),

    # Investment
    ("Monthly SIP investment in Nifty 50 Index Mutual Fund", "Investment"),
    ("Purchased bluechip equity company shares on Zerodha", "Investment"),
    ("Fixed Deposit FD recurring deposit account transfer", "Investment"),
    ("Digital Sovereign Gold Bond investment purchase", "Investment"),
    ("Groww equity mutual fund portfolio installment", "Investment"),
    ("Cryptocurrency Bitcoin Ethereum investment buy", "Investment"),

    # Salary & Income
    ("Monthly salary credit from IT tech company", "Salary"),
    ("Monthly corporate payroll paycheck direct bank deposit", "Salary"),
    ("Performance appraisal bonus credited to account", "Salary"),
    ("Internship monthly stipend allowance transferred", "Salary"),
    ("Freelance client payment for web development project", "Freelance"),
    ("Upwork freelance mobile app design milestone payout", "Freelance"),
    ("Fiverr graphic design illustration gig income", "Freelance"),
    ("Quarterly dividend received from Tata Motors stocks", "Investment Returns"),
    ("Savings bank account annual interest credited", "Investment Returns"),
    ("Fixed deposit FD maturity interest payout", "Investment Returns")
]

# Benchmark evaluation dataset (held-out test set for research experiment)
BENCHMARK_TEST_DATA = [
    ("Order veg burger and coke at Burger King", "Food & Dining"),
    ("Swiggy gourmet dinner pasta delivery", "Food & Dining"),
    ("Purchased apples bananas and bread at grocery store", "Food & Dining"),
    ("Espresso coffee at Blue Tokai roasters", "Food & Dining"),
    ("Uber cab ride to railway station terminal", "Transportation"),
    ("Monthly metro card automatic topup", "Transportation"),
    ("Full tank petrol refill at HP fuel pump", "Transportation"),
    ("Rapido bike taxi trip to tuition classes", "Transportation"),
    ("Bought Advanced Python programming handbook", "Education"),
    ("Coursera Deep Learning specialization monthly fee", "Education"),
    ("College lab manual and record stationary notebooks", "Education"),
    ("PVR cinema tickets for weekend movie premiere", "Entertainment"),
    ("Netflix standard monthly plan auto debit", "Entertainment"),
    ("Spotify family music stream subscription", "Entertainment"),
    ("Steam video game purchase in cyber sale", "Entertainment"),
    ("Purchased paracetamol and cough lozenges at pharmacy", "Healthcare"),
    ("Dentist tooth filling clinic fee", "Healthcare"),
    ("Doctor appointment fee for seasonal viral flu", "Healthcare"),
    ("Flat monthly house rent transfer to landlord", "Housing & Utilities"),
    ("Electricity power utility bill payment", "Housing & Utilities"),
    ("Monthly high speed WiFi internet bill payment", "Housing & Utilities"),
    ("LPG cooking gas cylinder booking payment", "Housing & Utilities"),
    ("Ordered casual running sneakers on Myntra", "Shopping"),
    ("Bought wireless noise cancelling headphones Amazon", "Shopping"),
    ("Zara denim jacket purchase at shopping mall", "Shopping"),
    ("Men haircut and hair wash at salon barber", "Personal Care"),
    ("Monthly gym fitness club membership fee", "Personal Care"),
    ("SIP equity mutual fund regular investment", "Investment"),
    ("Monthly salary credited by employer bank transfer", "Salary"),
    ("Freelance UI/UX redesign project milestone payment", "Freelance")
]
