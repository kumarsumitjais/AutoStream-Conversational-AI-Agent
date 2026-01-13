from agent.graph import build_graph
from agent.rag import load_knowledge_base, create_retriever
from agent.state import AgentState


RESTART_COMMANDS = [
    "restart",
    "restart conversation",
    "start over",
    "reset",
    "new conversation"
]



documents = load_knowledge_base("data/knowledge_base.json")
retriever = create_retriever(documents)

graph = build_graph(retriever)

print("AutoStream Assistant is running. Type 'exit' to quit.\n")

state = AgentState()

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Agent: Goodbye! 👋")
        break

    # 🔄 RESTART CONVERSATION
    if user_input.lower() in RESTART_COMMANDS:
        state = AgentState()
        print("Agent: 🔄 Conversation restarted. How can I help you today?")
        continue

    state.user_input = user_input
    state_dict = graph.invoke(state)
    state = AgentState(**state_dict)

    print(
        f"DEBUG intent: {state.intent} "
        f"(confidence: {state.intent_confidence:.2f})"
    )
    print(f"Agent: {state.response}")
