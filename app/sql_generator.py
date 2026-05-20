from app.ml_model import GeminiAgent

gemini = GeminiAgent()

# Define your schema once so Gemini understands the tables
SCHEMA_CONTEXT = """
Database Schema:
- customers (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit)
- employees (employeeNumber, lastName, firstName, extension, email, officeCode, reportsTo, jobTitle)
- offices (officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory)
- orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
- orders (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
- payments (customerNumber, checkNumber, paymentDate, amount)
- productlines (productLine, textDescription, htmlDescription, image)
- products (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)


CRITICAL RULES:
1. Always use double quotes for column names: e.g., "productName", "buyPrice", "customerNumber".
2. Always use double quotes for table names: e.g., "products", "customers".
3. Return ONLY the raw SQL code. No markdown, no backticks.
"""

def generate_sql_pipeline(user_question: str, error_message: str = None):
    # STEP 1: DECOMPOSITION (Task 2 Logic)
    decomp_instruction = f"""
    {SCHEMA_CONTEXT}
    Analyze the user question and provide:
    - Intent
    - Tables involved
    - Columns needed
    - Filters
    - Joins
    Format the output exactly like the Task 2 format.
    """
    decomposition = gemini.ask(decomp_instruction, user_question)
    
    # STEP 2: SQL GENERATION
    sql_instruction = f"""
    {SCHEMA_CONTEXT}
    Based on this decomposition: {decomposition}
    Generate a valid PostgreSQL SELECT query.
    Return ONLY the raw SQL code. No markdown formatting, no backticks.
    """
    
    # IF RETRYING: Add the error context
    if error_message:
        sql_instruction += f"\nYour previous query failed with error: {error_message}. Please fix it."

    generated_sql = gemini.ask(sql_instruction, user_question)
    # Clean markdown backticks if Gemini added them
    generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
    return generated_sql.replace("```sql", "").replace("```", "").strip()

# for task 4

def generate_summary(question: str, result_data: list):
    """Converts the raw SQL results into a human-friendly sentence."""
    summary_instruction = f"""
    You are a data analyst. Based on the user's question: "{question}" 
    and the following data retrieved from the database: {result_data}
    
    Provide a concise, professional one-sentence summary of the answer.
    If no data was found, say "No records were found for that request."
    """
    # Use the existing gemini.ask method
    summary = gemini.ask(summary_instruction, "Summarize the data.")
    return summary.strip()