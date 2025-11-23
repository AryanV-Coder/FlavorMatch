# 🍽️ What's for Dinner? — A Family Food Recommendation System

🚀 **Live Demo:** [https://flavor-match-aat.vercel.app](https://flavor-match-aat.vercel.app)

## 📖 Introduction
In every household, one common question arises daily — *“Aaj khane mein kya banau?”*  
This project aims to solve that problem by tracking the food preferences of family members and recommending dishes they are likely to enjoy.  
The system uses a relational database to store data about families, their members, and their food choices.  
Over time, the system learns patterns and provides personalized food suggestions.

---

## 🎯 Objectives
- To design and implement a normalized relational database system.
- To allow multiple families to register and maintain their own member data.
- To record each member’s eating preferences (liked/unliked, healthy/junk).
- To provide food recommendations based on family members' past preferences.
- To demonstrate the use of **primary keys**, **foreign keys**, **relationships**, and **constraints** in a real-world scenario.

---

## 🧩 Core Concepts Used
- **Entity-Relationship (ER) Modeling**  
  Defined clear 1–M relationships between Family → Member → Food.
- **Normalization**  
  Data divided across multiple tables to remove redundancy.
- **Primary & Foreign Keys**  
  Used to establish and enforce referential integrity.
- **Cascade Operations**  
  Ensures automatic cleanup when a family or member is deleted.
- **SQL Constraints**  
  `UNIQUE`, `NOT NULL`, `ON UPDATE CASCADE`, and `ON DELETE CASCADE` used for data integrity.
- **Timestamp Handling**  
  Each food entry is time-stamped for future analytics.

---

## 👨‍💻 Tech Stack
- **Backend:** PostgreSQL, Node.js (Express), FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel (Frontend + Node.js Backend)

---

## 📁 Project Structure
```
FlavorMatch/
├── api/                           # Node.js Backend (Express)
│   ├── server.js                  # Main server file
│   ├── package.json               # Node.js dependencies
│   ├── config/
│   │   └── db.js                  # PostgreSQL connection config
│   ├── controllers/
│   │   └── authController.js      # Authentication logic
│   └── routes/
│       └── authRoutes.js          # API routes
│
├── fastapi-backend/               # Python Backend (FastAPI)
│   ├── main.py                    # FastAPI main application
│   ├── requirements.txt           # Python dependencies
│   ├── models/
│   │   └── prompt_request.py      # Request models
│   ├── routers/
│   │   └── chat.py                # Chat API endpoints
│   └── utils/
│       ├── chatbot_response.py    # AI chatbot logic
│       ├── gemini.py              # Google Gemini AI integration
│       ├── sql_query_generator.py # SQL query generation
│       └── supabase_config.py     # Supabase configuration
│
├── public/                        # Frontend (Static Files)
│   ├── index.html                 # Login page
│   ├── register_family.html       # Family registration
│   ├── register_member.html       # Member registration
│   └── dashboard.html             # Food tracking dashboard
│
├── vercel.json                    # Vercel deployment configuration
├── postgresql_table_creation_code.txt  # Database schema
└── README.md                      # Project documentation
```

---

## 🧠 System Design

### **1️⃣ Family Table**
| Column Name      | Type             | Description |
|------------------|------------------|-------------|
| family_id        | BIGINT (PK)      | Unique ID for each family |
| family_username  | VARCHAR (Unique) | Unique username for the family |

### **2️⃣ Member Table**
| Column Name       | Type             | Description |
|-------------------|------------------|-------------|
| member_id         | BIGINT (PK)      | Unique ID for each member |
| family_id         | BIGINT (FK)      | References `family(family_id)` |
| member_username   | VARCHAR          | Member’s name (unique per family) |
| member_password   | VARCHAR          | Password for member login |

### **3️⃣ Food Table**
| Column Name  | Type             | Description |
|--------------|------------------|-------------|
| food_id      | BIGINT (PK)      | Unique ID for each food entry |
| timestamp    | TIMESTAMP        | When the food was logged |
| member_id    | BIGINT (FK)      | References `member(member_id)` |
| food         | VARCHAR          | Name of the food |
| is_liked     | VARCHAR          | User’s feedback (Yes/No) |
| is_healthy   | VARCHAR          | Health tag (Healthy/Junk) |

---

## 🔗 Relationships
- **Family (1) → Member (M)**  
  A family can have multiple members.  
- **Member (1) → Food (M)**  
  A member can log multiple food items.

---

## ⚙️ Execution Plan
1. Create the PostgreSQL database and execute the schema SQL scripts.  
2. Build a simple web interface with three pages:
   - **Family Registration/Login**
   - **Member Registration/Login**
   - **Food Activity Page**
     - “What did you eat today?”
     - “What can I eat today?”
3. Store and fetch data using SQL queries to track user preferences.
4. Use a lightweight AI or rule-based engine for food recommendations.

---

## 🎯 Expected Outcome
- A functional, multi-user web system for tracking and suggesting food items.
- Demonstrates **DBMS concepts** like relationships, constraints, and normalization.
- Real-world use case showing how data can power small-scale personalized recommendations.

---

## 🏁 Conclusion
This project showcases how an everyday household problem can be modeled and solved using relational databases.  
Through clear entity relationships, efficient schema design, and structured queries, the system highlights the practical implementation of DBMS principles in a real-world scenario.

---

### 💡 Project by: *Aryan Varshney*, *Aneri Gupta* & *Tarushi Goel*