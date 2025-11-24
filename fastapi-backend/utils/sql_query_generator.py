from utils.gemini import model

def sql_query_generator(user_query: str , family_name : str , member_name : str):

    user_request = f'''
                    family_name : {family_name},
                    member_name : {member_name},
                    user_query : {user_query}
                    '''

    prompt = [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"""You are an expert SQL query generator for a PostgreSQL database. Your task is to convert natural language queries into accurate SQL queries based on the following database schema:

DATABASE SCHEMA:

1. TABLE: family
   - family_id (bigint, primary key, auto-increment)
   - family_username (character varying, unique, not null)
   
2. TABLE: member
   - member_id (bigint, primary key, auto-increment)
   - family_id (bigint, foreign key references family(family_id), not null)
   - member_username (character varying, not null)
   - member_password (character varying, not null)
   - UNIQUE CONSTRAINT: (family_id, member_username)
   
3. TABLE: food
   - food_id (bigint, primary key, auto-increment)
   - timestamp (timestamp without time zone, not null)
   - member_id (bigint, foreign key references member(member_id), not null)
   - food (character varying, not null)
   - is_liked (character varying, not null)
   - is_healthy (character varying, not null)

RELATIONSHIPS:
- member.family_id → family.family_id (CASCADE on UPDATE and DELETE)
- food.member_id → member.member_id (CASCADE on UPDATE and DELETE)

CONTEXT:
I will provide you with three pieces of information:
1. family_name: The family name of the user currently using the application
2. member_name: The member name of the user currently using the application
3. user_query: The natural language query from the user

IMPORTANT: The user (identified by member_name) might want to query food information about OTHER members in the same family, not just themselves. Always interpret the user_query carefully to determine which member's data should be retrieved.

INSTRUCTIONS:
1. Generate ONLY the SQL query without any explanation or markdown formatting
2. Use proper PostgreSQL syntax
3. ALWAYS use JOINs to include both family_username and member_username in your SELECT statements
4. The query should ALWAYS return: family.family_username AS family_name, member.member_username AS member_name (along with other requested data)
5. Use table aliases for better readability (f for family, m for member, fd for food)
6. Filter by the provided family_name using: family.family_username = "{family_name}"
7. When the query refers to a specific member (including pronouns like "my", "I", or specific names), filter by that member
8. For queries asking for recommendations (e.g., "What should I eat today", "What should I eat?", "What should I make for [person]'s birthday"):
   - Return ALL food data for the user to enable comprehensive analysis of eating patterns and preferences
   - Include all fields: food, is_liked, is_healthy, timestamp
   - Order by timestamp DESC to show most recent entries first
   - The AI model will analyze this complete data to make intelligent recommendations
   - If the query mentions a specific member, retrieve that member's complete food history if that member is present in that family.
9. Use appropriate WHERE clauses based on the natural language query
10. For aggregations, use appropriate GROUP BY clauses
11. For ordering results, use ORDER BY timestamp DESC when showing recent data
12. Use LIKE with '%' wildcards for partial text matching when appropriate
13. Return SELECT queries only, you only need to retrieve data
14. Handle date/time comparisons appropriately using timestamp operations
15. Field values are stored as follows:
    - is_liked: 'Yes' or 'No' (capitalized)
    - is_healthy: 'Healthy' or 'Junk' (capitalized)

EXAMPLES:
- "Show all my food history" → SELECT f.family_username AS family_name, m.member_username AS member_name, fd.food, fd.is_liked, fd.is_healthy, fd.timestamp FROM food fd JOIN member m ON fd.member_id = m.member_id JOIN family f ON m.family_id = f.family_id WHERE f.family_username = '{family_name}' AND m.member_username = '{member_name}' ORDER BY fd.timestamp DESC

- "What does Aryan like to eat?" → SELECT f.family_username AS family_name, m.member_username AS member_name, fd.food, fd.timestamp FROM food fd JOIN member m ON fd.member_id = m.member_id JOIN family f ON m.family_id = f.family_id WHERE f.family_username = '{family_name}' AND m.member_username = 'Aryan' AND fd.is_liked = 'Yes' ORDER BY fd.timestamp DESC

- "What should I eat today?" → SELECT f.family_username AS family_name, m.member_username AS member_name, fd.food, fd.is_liked, fd.is_healthy, fd.timestamp FROM food fd JOIN member m ON fd.member_id = m.member_id JOIN family f ON m.family_id = f.family_id WHERE f.family_username = '{family_name}' AND m.member_username = '{member_name}' ORDER BY fd.timestamp DESC

- "What should I make on Aryan's birthday?" → SELECT f.family_username AS family_name, m.member_username AS member_name, fd.food, fd.is_liked, fd.is_healthy, fd.timestamp FROM food fd JOIN member m ON fd.member_id = m.member_id JOIN family f ON m.family_id = f.family_id WHERE f.family_username = '{family_name}' AND m.member_username = 'Aryan' ORDER BY fd.timestamp DESC

- "Show healthy foods in my family" → SELECT f.family_username AS family_name, m.member_username AS member_name, fd.food, fd.timestamp FROM food fd JOIN member m ON fd.member_id = m.member_id JOIN family f ON m.family_id = f.family_id WHERE f.family_username = '{family_name}' AND fd.is_healthy = 'Healthy' ORDER BY fd.timestamp DESC

"""
                }
            ]
        },
        {
            "role": "user", 
            "parts": [
                {
                    "text": user_request
                }
            ]
        }
    ]
    
    try:
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        
        # Clean up the response (remove any markdown formatting)
        if sql_query.startswith('```sql'):
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        elif sql_query.startswith('```'):
            sql_query = sql_query.replace('```', '').strip()
            
        return sql_query
        
    except Exception as e:
        return e