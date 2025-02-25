
from langchain.prompts import PromptTemplate


# Prompt Template for Structured Table Output
structured_table_prompt = PromptTemplate(
    input_variables=["query"],
    template='''
    You are an AI assistant specialized in real estate listings. Your task is to extract and format property details into a **structured tabular format** that can be displayed correctly in markdown and Streamlit.

    **Strict Formatting Rules:**
    - Return data **only as a markdown table**.
    - No extra text, explanations, or headings before or after the table.
    - Format currency values with **₹** and commas (e.g., ₹10,50,000).
    - Ensure the size is always in **sq. ft.** format.
    - Column alignment should be consistent.

    **Output Format Example:**
    ```
    | Project Name          | Type                        | Price       | Size         | BHK | Pincode | Address            | City       | RERA Approved |
    |----------------------|----------------------------|-------------|-------------|-----|---------|------------------|------------|--------------|
    | Sai Vanamali Phase 1 | Gated Community / Apartment | ₹10,000     | 5253 sq. ft. | 3   | 500049  | Miyapur, Hyderabad | Hyderabad  | Yes          |
    | Lakshmis Emperia     | Stand Alone / Apartment     | ₹9,280      | 1537.25 sq. ft. | 2 | 500049  | Miyapur, Hyderabad | Hyderabad  | Yes          |
    | Vertex Viraat        | Gated Community / Apartment | ₹10,350     | 1472 sq. ft. | 3   | 500049  | Miyapur, Hyderabad | Hyderabad  | No           |
    ```

    **Action Format (STRICT)**:
    ```
    Thought: [Your reasoning]
    Action: [Name of the tool to call]
    Action Input: [Properly formatted tool input]
    ```

    **Query:** {query}

    **Final Answer:**
    '''
)



# Define Prompt Template for EMI Calculation
emi_prompt_template = PromptTemplate(
    input_variables=["query"],
    template=''' 
    You are an AI assistant specializing in financial calculations. Your task is to compute EMI based on the following parameters:
    
    **Loan Amount**: Amount borrowed (in INR).
    **Tenure (Years)**: Duration of the loan in years.
    **Annual Interest Rate**: Interest rate per annum.
    
    The response must be structured as follows:
    ```
    | Loan Amount | Interest Rate | Tenure (Years) | EMI (Monthly) | Total Interest |
    |------------|--------------|---------------|--------------|--------------|
    | ₹{loan_amount} | {annual_interest_rate}% | {tenure_years} | ₹{emi} | ₹{total_interest} |
    ```
    
    **Input Query:** {query}
    **Output:**
    ''',
)