from langchain_ollama import ChatOllama


# ================= AI MODEL =================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    num_gpu=0
)


# ================= ANALYZE COMPLAINT =================

def analyze_complaint(complaint):

    prompt = f"""
You are an AI assistant for a Smart City Complaint Management System.

Analyze this citizen complaint:

{complaint}

Return EXACTLY these 5 lines.

Category: Pothole
Department: Roads Department
Priority: Medium
Severity: Medium
Summary: Short summary of the complaint

Rules:
- Category must be exactly one of:
  Pothole, Garbage, Water Leakage, Street Light, Drainage, Other

- Department must be exactly one of:
  Roads Department, Sanitation Department, Water Department,
  Electrical Department, Drainage Department, General Department

- Priority must be exactly one of:
  Low, Medium, High, Critical

- Severity must be exactly one of:
  Low, Medium, High

- Summary must be one short sentence.
- Do not use the | symbol.
- Do not use Markdown.
- Do not use bullet points.
- Do not add any explanation.
- Return only the 5 required lines.
"""

    response = llm.invoke(prompt)

    result = str(response.content).strip()

    # Remove unwanted pipe characters
    result = result.replace("|", "")

    # Remove Markdown code fences if the model adds them
    result = result.replace("```text", "")
    result = result.replace("```", "")

    return result.strip()