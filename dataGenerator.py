from faker import Faker
import random
import json
import datetime
import pymysql.cursors
from db_config import get_connection  # import your db connection function

fake = Faker()

conn = get_connection()
cursor = conn.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT role_id FROM USERPROFILE")
roles = [row['role_id'] for row in cursor.fetchall()]

# Divide 100 users across roles
total_users = 100
users_per_role = total_users // len(roles)

def generate_singapore_address():
    block = random.randint(1, 999)
    street_names = [
        "Orchard Road", "Clementi Avenue", "Bedok North Road", "Yishun Ring Road",
        "Bukit Timah Road", "Ang Mo Kio Ave", "Serangoon North Ave", "Tampines Street",
        "Jurong West Street", "Hougang Avenue"
    ]
    street = random.choice(street_names)
    unit = f"#{random.randint(1, 30):02d}-{random.randint(1, 99):03d}"
    postal = f"{random.randint(100000, 829999)}"
    return f"Blk {block} {street} {unit}, Singapore {postal}"

# Generate 100 users distributed across roles
for _ in range(100):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.unique.email().replace('@example.com', '@gmail.com')
    password = fake.password(length=10)  # Plaintext password as per request
    address = generate_singapore_address()
    phone = f"{random.choice(['8', '9'])}{fake.random_number(digits=7, fix_len=True)}"
    role_id = random.choice(roles)
    is_active = random.choice([True, False])

    cursor.execute("""
        INSERT INTO USERS (email, password, role_id, first_name, last_name, address, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (email, password, role_id, first_name, last_name, address, phone))



# Use a set to ensure unique category names
category_names = set()

while len(category_names) < 100:
    # Generate unique category name like "Window Cleaning", "Office Cleaning", etc.
    prefix = fake.unique.word().capitalize()
    category_name = f"{prefix} Cleaning"
    description = fake.sentence(nb_words=10)
    category_status = random.choice([True, False])

    # Insert into CATEGORY table
    cursor.execute("""
        INSERT INTO CATEGORY (name, description, categoryStatus)
        VALUES (%s, %s, %s)
    """, (category_name, description, category_status))

    category_names.add(category_name)

# CleaningService Generator
cursor.execute("SELECT userID FROM USERS WHERE role_id = (SELECT role_id FROM USERPROFILE WHERE role_name = 'Cleaner')")
cleaners = [row['userID'] for row in cursor.fetchall()]

cursor.execute("SELECT categoryID FROM CATEGORY")
categories = [row['categoryID'] for row in cursor.fetchall()]

for _ in range(100):
    cleaner_id = random.choice(cleaners)
    category_id = random.choice(categories)
    title = f"{fake.word().capitalize()} Cleaning Service"
    description = fake.text(max_nb_chars=100)
    price = round(random.uniform(30, 200), 2)
    service_status = random.choice([True, False])

    cursor.execute("""
        INSERT INTO CLEANINGSERVICE (cleanerID, categoryID, title, description, price, serviceStatus)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (cleaner_id, category_id, title, description, price, service_status))

cursor.execute("SELECT userID FROM USERS WHERE role_id = (SELECT role_id FROM USERPROFILE WHERE role_name = 'Homeowner')")
homeowners = [row['userID'] for row in cursor.fetchall()]

cursor.execute("SELECT serviceID FROM CLEANINGSERVICE")
services = [row['serviceID'] for row in cursor.fetchall()]

for _ in range(100):
    homeowner_id = random.choice(homeowners)
    service_id = random.choice(services)
    cursor.execute("""
        INSERT INTO SHORTLIST (homeownerID, serviceID)
        VALUES (%s, %s)
    """, (homeowner_id, service_id))

booking_statuses = ["Pending", "Confirmed", "Completed", "Cancelled"]

for _ in range(100):
    homeowner_id = random.choice(homeowners)
    service_id = random.choice(services)

    # Get cleanerID linked to service
    cursor.execute("SELECT cleanerID, price FROM CLEANINGSERVICE WHERE serviceID = %s", (service_id,))
    service = cursor.fetchone()
    cleaner_id = service['cleanerID']
    price = float(service['price'])

    booking_date = fake.date_between(start_date='-30d', end_date='+30d')
    booking_hour = random.randint(8, 18)  # between 8 AM and 6 PM
    booking_status = random.choice(booking_statuses)

    cursor.execute("""
        INSERT INTO BOOKING (homeownerID, serviceID, cleanerID, bookingDate, bookingHour, totalPrice, bookingStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (homeowner_id, service_id, cleaner_id, booking_date, booking_hour, price, booking_status))

# Report types available
#report_types = ['Daily Report', 'Weekly Report', 'Monthly Report']

#service_types = ["Office Cleaning", "Basic Home Cleaning", "Full House Deep Clean"]


# Generate 100 report entries
#for _ in range(100):
    # Randomly select report type and generate the report date
    #report_type = random.choice(report_types)
   # report_date = fake.date_this_year()  # Random date in the current year
    
    # Ensure the date is converted to a string (YYYY-MM-DD)
    #if isinstance(report_date, datetime.date):  # Check if it's a date object
       # report_date_str = report_date.strftime('%Y-%m-%d')
    #else:
        #report_date_str = str(report_date)

    # Generate service distribution (random number of services)
    #service_distribution = {service: random.randint(0, 3) for service in service_types}
    
    # Generate other report metrics
    #total_revenue = round(random.uniform(100.0, 1000.0), 2)  # Random total revenue
    #total_bookings = sum(service_distribution.values())  # Total bookings based on distribution
    #pending_bookings = random.randint(0, total_bookings)  # Random pending bookings
    #confirmed_bookings = total_bookings - pending_bookings  # Confirmed bookings = total - pending
    
    # Structure the data as JSON
    #report_data = {
        #"report_date": report_date_str,
        #"total_revenue": total_revenue,
        #"total_bookings": total_bookings,
        #"pending_bookings": pending_bookings,
        #"confirmed_bookings": confirmed_bookings,
        #"service_distribution": service_distribution
    #}
    
    # Convert the report data to a JSON string for insertion into the DB
    #report_data_json = json.dumps(report_data)
    
    # Insert into the REPORT table
    #cursor.execute("""
    #    INSERT INTO REPORT (reportType, reportData)
    #    VALUES (%s, %s)
    #""", (report_type, report_data_json))

conn.commit()
cursor.close()
conn.close()
