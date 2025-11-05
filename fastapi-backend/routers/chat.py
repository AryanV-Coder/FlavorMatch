from fastapi import APIRouter, HTTPException
from models.prompt_request import PromptRequest
from utils.supabase_config import connect_postgres
from utils.sql_query_generator import sql_query_generator
from utils.chatbot_response import ai_analysis

router = APIRouter()

@router.post("/chat")
async def chat(user_request : PromptRequest):
    if user_request.request is None :
        print("🛑 NOTHING RECIEVED")
        raise HTTPException(status_code = 400, detail = "Nothing Recieved")
    else :
        query = sql_query_generator(user_query = user_request.request, family_name=user_request.family_name,member_name=user_request.member_name)
        print(f"✅ SQL QUERY GENERATED : {query}")

        conn,cursor = connect_postgres()

        try :
            cursor.execute(query)
            print("✅ Query Successful !!")

            result = cursor.fetchall()
            print(f"✅ Response after select query : {result}")
        except Exception as e:
            print(f"🛑 ERROR : {e}")
            raise HTTPException(status_code=500, detail = e)
        
        cursor.close()
        conn.close()

        response = ai_analysis(user_request=user_request.request,data = result)

        return {
            "status" : "success",
            "response" : response
        }