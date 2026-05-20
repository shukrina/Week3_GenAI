import re

def validate_sql(query: str):
    """Ensures the query is only a SELECT statement."""
    forbidden_words = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
    
    # Check if it starts with SELECT
    if not query.strip().upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."
    
    # Check for forbidden keywords
    for word in forbidden_words:
        if re.search(rf"\b{word}\b", query, re.IGNORECASE):
            return False, f"Security Breach: {word} command is not allowed."
            
    return True, ""