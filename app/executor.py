from app.database import execute_raw_sql
from app.validator import validate_sql
from app.sql_generator import generate_sql_pipeline

def run_agentic_query(question: str, db): 
    print(f"--- Processing Question: {question} ---")
    sql = generate_sql_pipeline(question)
    print(f"--- Generated SQL: {sql} ---") 
    # 1. Generate SQL
    sql = generate_sql_pipeline(question)
    
    # 2. Validate Security
    is_valid, msg = validate_sql(sql)
    if not is_valid:
        return {"status": "error", "message": msg, "sql": sql}

    # 3. Try Execute
    try:
        data = execute_raw_sql(sql, db)
        return {"status": "success", "result": data, "sql": sql, "retry": False}
    except Exception as e:
        # 4. AGENTIC RETRY: Pass the error back to Gemini once
        print(f"First attempt failed: {str(e)}. Retrying...")
        fixed_sql = generate_sql_pipeline(question, error_message=str(e))
        
        try:
            data = execute_raw_sql(fixed_sql, db)
            return {"status": "success", "result": data, "sql": fixed_sql, "retry": True}
        except Exception as e2:
            return {"status": "error", "message": str(e2), "sql": fixed_sql}