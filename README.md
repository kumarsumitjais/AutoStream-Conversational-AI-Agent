**AutoStream Conversational AI Agent**

**Project Overview**

This project implements a Conversational AI Agent for AutoStream, a SaaS-based AI video editing platform. The agent assists users by answering queries related to pricing, plans, and policies, identifying high-intent users, and collecting lead information in a structured manner.

****Key Features****

•    Intent Classification with confidence scoring

•    Retrieval-Augmented Generation (RAG) using FAISS and HuggingFace embeddings

•	 Stateful lead capture (name, email, platform)

•	 Email validation and duplicate lead prevention

•	 Mock API integration for CRM submission

•	 Restart conversation command

**Project Structure**

autostream_agent/
├── agent/

│   ├── graph.py

│   ├── intent.py

│   ├── rag.py

│   ├── state.py

│   ├── mock_api.py

│   ├── lead_store.py

│   └── validators.py

├── data/

│   └── knowledge_base.json

├── leads.json

├── main.py

├── requirements.txt

└── README.md

**How to Use the AutoStream Conversational AI Agent**

This guide explains how to set up, run, and interact with the AutoStream Conversational AI Agent — starting from virtual environment creation to exiting the application.

**1️⃣ Prerequisites**

Before starting, ensure you have:

Python 3.9 or higher

pip (Python package manager)

A terminal / command prompt

**2️⃣ Project Setup**

📁 Clone or Download the Project
git clone <repository-url>
cd autostream_agent


Or extract the provided ZIP/RAR file and navigate to the project directory.

**3️⃣ Create a Virtual Environment**

▶ Create venv

python -m venv venv

▶ Activate venv

*Windows*

venv\Scripts\activate


*macOS / Linux*

source venv/bin/activate


Once activated, your terminal will show:

(venv)

**4️⃣ Install Dependencies**

Install all required libraries using:

pip install -r requirements.txt


This installs:

LangGraph

LangChain

HuggingFace embeddings

FAISS

NumPy

Other required dependencies

**5️⃣ Run the Agent**

Start the conversational agent by running:

python main.py


You should see:

AutoStream Assistant is running. Type 'exit' to quit.

**6️⃣ Interacting with the Agent**

🗨️ Example Conversations

Greeting
You: hi
Agent: Hello! 😊 How can I help you with AutoStream today?

Pricing Inquiry
You: tell me about your plans
Agent: 📋 Pricing Plans:
       - Basic Plan ($29/month)
       - Pro Plan ($79/month)
       [Features and policies displayed]

High-Intent Subscription Flow

You: I want to subscribe to the Pro plan

Agent: That’s great! 🚀 May I know your name?

You: Alex

Agent: Please share your email address

You: alex@yahoo.com

Agent: Which platform do you create content for?

You: YouTube

Agent: ✅ Thanks! Your details have been recorded. Our team will contact you soon.


✔ Lead stored with timestamp
✔ Duplicate lead prevention applied
✔ Mock API submission executed

**7️⃣ Special Commands**
**🔄 Restart Conversation**

Resets the conversation state without deleting stored leads:

You: restart

Agent: 🔄 Conversation restarted. How can I help you today?

❌ Exit the Agent
You: exit

Agent: Goodbye! 👋

**8️⃣ Stored Data**

Lead data is saved in leads.json

Each record contains:

Name

Email

Platform

Selected plan

Timestamp

✅ End of Session

You have successfully:

Set up the virtual environment

Installed dependencies

Run the conversational agent

Completed an end-to-end interaction

Captured and stored lead details

Exited the application safely

**WhatsApp Integration (Conceptual)**
To integrate the agent with WhatsApp, the WhatsApp Business API can be used along with webhook-based message handling. Incoming user messages are sent by WhatsApp to a backend server (Flask/FastAPI) via webhooks. The backend forwards the message to the LangGraph agent while maintaining conversation state using the user’s phone number as a unique identifier. The agent processes the message, performs intent classification, RAG-based responses, and lead qualification. The generated response is then sent back to the user through the WhatsApp API. This architecture enables real-time, multi-turn conversations and safe lead capture on WhatsApp.

**Conclusion**

This project successfully demonstrates the design and implementation of a stateful Conversational AI agent for a SaaS platform like AutoStream. By combining intent classification, retrieval-augmented generation (RAG), and structured lead capture, the agent delivers accurate, context-aware, and user-friendly interactions.

The solution follows a modular and extensible architecture, making it easy to enhance or integrate with real-world systems such as CRM tools or messaging platforms like WhatsApp. Features such as confidence-based intent detection, semantic fallback, email validation, duplicate lead prevention, and mock API integration ensure both robustness and practical relevance.

Overall, this project meets all assignment requirements while showcasing best practices in conversational AI development, state management, and clean code design. It provides a solid foundation for building scalable, production-ready AI assistants in real-world SaaS applications.
This project fulfills all the assignment requirements and demonstrates a clean, stateful, and extensible conversational AI architecture. It effectively combines intent classification, retrieval-augmented generation, structured lead capture, and mock API integration, showcasing a practical and scalable approach to building real-world conversational systems.
