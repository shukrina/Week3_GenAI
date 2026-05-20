import time
from app.database import execute_raw_sql
from app.validator import validate_sql
from app.sql_generator import generate_sql_pipeline, generate_summary

def run_mini_sql_agent(question: str, db):
    max_retries = 3
    error_msg = None
    start_time = time.time()
    
    for attempt in range(1, max_retries + 1):
        print(f"--- Attempt {attempt} ---")
        
        # Step 1 & 2: Understand & Generate SQL
        sql = generate_sql_pipeline(question, error_message=error_msg)
        
        #If the result is an error string from the SDK, don't validate
        if sql.startswith("Error:"):
            return {
                "status": "error",
                "message": "AI Provider Quota Reached. Please wait a moment before trying again.",
                "details": sql
            }

        # sql = generate_sql_pipeline(question, error_message=error_msg)
        
        # Safe Query Validation
        is_valid, v_msg = validate_sql(sql)
        if not is_valid:
            error_msg = v_msg
            continue # Try again if validation failed

        # Step 3: Execute Query
        try:
            results = execute_raw_sql(sql, db)
            execution_time = round(time.time() - start_time, 2)
            
            # Step 5: Final Output (Summary)
            summary = generate_summary(question, results)
            
            print(f"Success on attempt {attempt}! Time: {execution_time}s")
            return {
                "sql": sql,
                "result": results,
                "summary": summary,
                "status": "success",
                "execution_time_sec": execution_time,
                "attempts": attempt
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error on attempt {attempt}: {error_msg}")

    # Fallback if all 3 retries fail
    return {
        "status": "failure",
        "message": "The agent was unable to resolve the query after 3 attempts.",
        "last_error": error_msg,
        "fallback_response": "I'm sorry, I'm having trouble accessing that specific data right now. Please try rephrasing your question."
    }

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
        
