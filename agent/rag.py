import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_knowledge_base(path: str):
    """Load JSON knowledge base and convert to LangChain Documents"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    # Case 1: List
    if isinstance(data, list):
        for item in data:
            # If item is dict
            if isinstance(item, dict):
                content = "\n".join(f"{k}: {v}" for k, v in item.items())
            # If item is string
            else:
                content = str(item)

            documents.append(Document(page_content=content))

    # Case 2: Dict
    elif isinstance(data, dict):
        for key, value in data.items():
            documents.append(
                Document(page_content=f"{key}: {value}")
            )

    return documents


def create_retriever(documents):
    """Create FAISS retriever using HuggingFace embeddings"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever()


def get_answer(query: str, retriever):
    """Retrieve relevant documents and return combined answer"""
    docs = retriever.invoke(query)
    raw_response = "\n".join(doc.page_content for doc in docs)

    # Format the response for better readability
    return format_response(raw_response)


def format_response(response: str) -> str:
    """Format raw response into user-friendly readable format"""
    formatted_parts = []

    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        if "pricing_plans:" in line:
            # Handle pricing plans
            plans_part = line.split("pricing_plans: ")[1]
            formatted_plans = format_pricing_plans(plans_part)
            formatted_parts.append("📋 Pricing Plans:\n" + formatted_plans)

        elif "policies:" in line:
            # Handle policies
            policies_part = line.split("policies: ")[1]
            formatted_policies = format_policies(policies_part)
            formatted_parts.append("📜 Policies:\n" + formatted_policies)

        else:
            formatted_parts.append(line)

    return "\n\n".join(formatted_parts)


def format_pricing_plans(plans_str: str) -> str:
    """Format pricing plans for readability"""
    try:
        # Clean up the string representation
        plans_str = plans_str.strip()

        # Handle the list format: [{'name': '...', 'price': '...', 'features': [...]}, ...]
        if plans_str.startswith("[{") and plans_str.endswith("}]"):
            plans_str = plans_str[1:-1]  # Remove outer brackets

            # Split by "}, {" to get individual plans (with quotes)
            plan_strings = []
            current_plan = ""
            brace_count = 0
            in_string = False
            string_char = None

            i = 0
            while i < len(plans_str):
                char = plans_str[i]

                if not in_string and char in ["'", '"']:
                    in_string = True
                    string_char = char
                elif in_string and char == string_char and (i == 0 or plans_str[i-1] != '\\'):
                    in_string = False
                    string_char = None
                elif not in_string and char == '{':
                    brace_count += 1
                elif not in_string and char == '}':
                    brace_count -= 1

                current_plan += char

                # Check for plan separator: }, {
                if not in_string and brace_count == 0 and i + 3 < len(plans_str):
                    if plans_str[i:i+4] == "}, {":
                        plan_strings.append(current_plan[:-2])  # Remove the }, part
                        current_plan = "{"
                        i += 2  # Skip the , {

                i += 1

            # Add the last plan
            if current_plan.strip():
                plan_strings.append(current_plan.strip())

            formatted_plans = []
            for plan_str in plan_strings:
                if plan_str.strip():
                    plan = parse_dict_string(plan_str.strip("{}"))
                    formatted_plan = format_single_plan(plan)
                    formatted_plans.append(formatted_plan)

            return "\n\n".join(formatted_plans)

    except Exception as e:
        print(f"Error formatting plans: {e}")
        return f"Error formatting plans: {plans_str}"

    return plans_str


def parse_dict_string(dict_str: str) -> dict:
    """Parse a string representation of a dictionary"""
    result = {}
    # Split by comma but be careful with nested structures
    parts = []
    current_part = ""
    in_list = False
    in_string = False
    string_char = None

    i = 0
    while i < len(dict_str):
        char = dict_str[i]

        if not in_string and char in ["'", '"']:
            in_string = True
            string_char = char
            current_part += char
        elif in_string and char == string_char:
            in_string = False
            string_char = None
            current_part += char
        elif not in_string and char == '[':
            in_list = True
            current_part += char
        elif not in_string and char == ']':
            in_list = False
            current_part += char
        elif not in_string and not in_list and char == ',':
            parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
        i += 1

    if current_part.strip():
        parts.append(current_part.strip())

    # Parse each key-value pair
    for part in parts:
        if ": " in part:
            key, value = part.split(": ", 1)
            key = key.strip().strip("'\"")
            value = value.strip()

            # Handle lists
            if value.startswith("[") and value.endswith("]"):
                # Parse list items
                list_content = value[1:-1]
                if list_content.strip():
                    items = [item.strip().strip("'\"") for item in list_content.split(",")]
                    result[key] = items
                else:
                    result[key] = []
            else:
                result[key] = value.strip("'\"")

    return result


def format_single_plan(plan: dict) -> str:
    """Format a single pricing plan cleanly"""
    lines = []
    lines.append(f"🏷️  Name: {plan.get('name', 'N/A')}")
    lines.append(f"💰 Price: {plan.get('price', 'N/A')}")
    lines.append("✨ Features:")

    features = plan.get("features", [])

    # Case 1: Proper Python list
    if isinstance(features, list):
        for feature in features:
            lines.append(f"- {feature}")

    # Case 2: String that looks like a list
    elif isinstance(features, str) and features.startswith("["):
        cleaned = features.strip("[]")
        for feature in cleaned.split(","):
            feature = feature.strip().strip("'").strip('"')
            lines.append(f"- {feature}")

    # Fallback
    else:
        lines.append(f"- {features}")

    return "\n".join(lines)




def format_policies(policies_str: str) -> str:
    """Format policies for readability"""
    try:
        # Clean up the string representation
        policies_str = policies_str.strip()

        if policies_str.startswith("{") and policies_str.endswith("}"):
            policies_str = policies_str[1:-1]  # Remove outer braces

            # Parse the policies dict
            policies = parse_dict_string(policies_str)

            formatted_policies = []
            for key, value in policies.items():
                clean_key = key.replace('_', ' ').title()
                formatted_policies.append(f"📝 {clean_key}: {value}")

            return "\n".join(formatted_policies)

    except Exception as e:
        return f"Error formatting policies: {policies_str}"

    return policies_str
