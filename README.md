# Fitness Booking API

A FastAPI-based application for booking fitness classes like Yoga, Zumba, and HIIT with timezone support, input validation, and logging.

---

## Features

- List available fitness classes
- Book a class (with available slot validation)
- Convert class timings based on user-specified timezones
- Retrieve bookings by email
- Basic error handling and input validation
- Clean logging and environment-based configuration

---

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: SQLite (Async with SQLAlchemy)
- **Timezone Handling**: `zoneinfo`
- **Logging**: Python `logging` module
- **Environment Config**: `python-dotenv`

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nishpatel512/fitness_booking_api.git
cd fitness_booking_api
````

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root of the project and add:

```env
DATABASE_URL=sqlite+aiosqlite:///./booking.db
ENV=prod
TIMEZONE=Asia/Kolkata
```

### 5. Seed the Database

```bash
python seed_data.py
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The app will be available at: [http://localhost:8000](http://localhost:8000)

---

## Sample Requests

### Get All Classes (with optional timezone)

**cURL:**

```bash
curl -X GET "http://localhost:8000/classes?tz=UTC" -H "accept: application/json"
```

**Postman:**

* Method: `GET`
* URL: `http://localhost:8000/classes?tz=UTC`

---

### Book a Class

**cURL:**

```bash
curl -X POST "http://localhost:8000/book" \
-H "Content-Type: application/json" \
-d '{
  "class_id": 1,
  "client_name": "Nish Patel",
  "client_email": "nish@example.com"
}'
```

**Postman:**

* Method: `POST`
* URL: `http://localhost:8000/book`
* Body → Raw → JSON:

```json
{
  "class_id": 1,
  "client_name": "Nish Patel",
  "client_email": "nish@example.com"
}
```

---

### Get Bookings by Email

**cURL:**

```bash
curl -X GET "http://localhost:8000/bookings?email=nish@example.com" -H "accept: application/json"
```

**Postman:**

* Method: `GET`
* URL: `http://localhost:8000/bookings?email=nish@example.com`

---

## License

MIT

---

## Author

[Nish Patel](https://github.com/nishpatel512)
