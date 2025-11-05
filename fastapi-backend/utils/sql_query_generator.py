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

INSTRUCTIONS:
1. Generate ONLY the SQL query without any explanation or markdown formatting
2. Use proper PostgreSQL syntax
3. Use table aliases for better readability when joining tables
4. Include appropriate WHERE clauses based on the natural language query
5. Use JOIN operations when querying across related tables
6. For aggregations, use appropriate GROUP BY clauses
7. For ordering results, use ORDER BY when it makes sense
8. Use LIKE with '%' wildcards for partial text matching when appropriate
9. Return SELECT queries only, you only need to retrieve data.
10. Handle date/time comparisons appropriately using timestamp operations
11. For yes/no or boolean-like fields (is_liked, is_healthy), assume values are stored as strings like 'yes'/'no' or 'true'/'false'

EXAMPLES:
- "Show all members in a family" → SELECT m.* FROM member m WHERE m.family_id = ?
- "Get all liked foods for a member" → SELECT f.* FROM food f WHERE f.member_id = ? AND f.is_liked = 'yes'
- "Find healthy foods eaten by members of a family" → SELECT f.* FROM food f JOIN member m ON f.member_id = m.member_id WHERE m.family_id = ? AND f.is_healthy = 'yes'

Now, convert the following natural language query to SQL:"""
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