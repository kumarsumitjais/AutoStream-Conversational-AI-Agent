from langgraph.graph import StateGraph, END
from agent import state
from agent.state import AgentState
from agent.intent import classify_intent
from agent.rag import get_answer
from agent.validators import is_valid_email
from agent.lead_store import save_lead, lead_exists, update_existing_lead
from agent.mock_api import submit_lead_to_crm






# --------------------------------------------------
# NODE 1: Detect Intent + Confidence (Memory Aware)
# --------------------------------------------------
def detect_intent(state: AgentState):
    # 🧠 Memory-aware intent bias
    if state.lead_step and state.lead_step != "done":
        return state

    # 🎯 Intent classification
    intent, confidence = classify_intent(state.user_input)
    state.intent = intent
    state.intent_confidence = confidence

    # 🎯 Detect selected plan from user input
    user_text = state.user_input.lower()
    if "basic" in user_text:
        state.selected_plan = "Basic Plan"
    elif "pro" in user_text:
        state.selected_plan = "Pro Plan"

    return state



# --------------------------------------------------
# NODE 2: Greeting Handler
# --------------------------------------------------
def handle_greeting(state: AgentState):
    state.response = "Hello! 😊 How can I help you with AutoStream today?"
    return state


# --------------------------------------------------
# NODE 3: Inquiry Handler (RAG)
# --------------------------------------------------
def handle_inquiry(state: AgentState):
    state.response = get_answer(state.user_input, handle_inquiry.retriever)
    return state


# --------------------------------------------------
# NODE 4: High-Intent / Lead Capture Handler
# --------------------------------------------------
def handle_high_intent(state: AgentState):
    from agent.validators import is_valid_email
    from agent.lead_store import save_lead, lead_exists, update_existing_lead

    # ✅ Already captured → polite acknowledgement
    if state.lead_captured:
        state.response = (
            "✅ Your interest has already been noted. "
            "Our team will reach out to you shortly.\n\n"
            "😊 Is there anything else I can help you with?"
        )
        return state

    # 🧠 STEP 0 → ask name
    if state.lead_step == "":
        state.lead_step = "name"
        state.response = "That’s great! 🚀 May I know your name?"
        return state

    # 🧠 STEP 1 → save name, ask email
    if state.lead_step == "name":
        state.name = state.user_input.strip()
        state.lead_step = "email"
        state.response = "Thanks! Could you please share your email address?"
        return state

    # 🧠 STEP 2 → validate + save email
    if state.lead_step == "email":
        email = state.user_input.strip()

        if not is_valid_email(email):
            state.response = (
                "❌ That doesn’t look like a valid email address.\n"
                "📧 Please enter a valid email (example: name@example.com)."
            )
            return state

        state.email = email
        state.lead_step = "platform"
        state.response = "Awesome! Which platform do you create content for?"
        return state

    # 🧠 STEP 3 → save platform, finalize
    if state.lead_step == "platform":
        state.platform = state.user_input.strip()

        if lead_exists(state.email):
            update_existing_lead(
                email=state.email,
                new_plan=state.selected_plan or None
            )
        else:
            lead_payload = {
                "name": state.name,
                "email": state.email,
                "platform": state.platform,
                "plan": state.selected_plan or "Not specified"
            }
            
            save_lead(**lead_payload)
            
            # 📡 MOCK API CALL
            submit_lead_to_crm(lead_payload)


        state.lead_step = "done"
        state.lead_captured = True
        state.response = (
            "✅ Thanks! Your details have been recorded. "
            "Our team will contact you soon.\n\n"
            "😊 Is there anything else I can help you with?"
        )
        return state





# --------------------------------------------------
# GRAPH BUILDER
# --------------------------------------------------
def build_graph(retriever):

    # Inject retriever safely (no lambda)
    handle_inquiry.retriever = retriever

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("greeting", handle_greeting)
    graph.add_node("inquiry", handle_inquiry)
    graph.add_node("high_intent", handle_high_intent)

    # Entry point
    graph.set_entry_point("detect_intent")

    # Conditional routing
    graph.add_conditional_edges(
        "detect_intent",
        lambda state: state.intent,
        {
            "greeting": "greeting",
            "inquiry": "inquiry",
            "high_intent": "high_intent",
        },
    )

    # End states
    graph.add_edge("greeting", END)
    graph.add_edge("inquiry", END)
    graph.add_edge("high_intent", END)

    return graph.compile()
