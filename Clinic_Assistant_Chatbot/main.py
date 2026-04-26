from fastapi import FastAPI
from graph import compiled_graph
import re


# app = FastAPI()


# @app.post("/StartChat")
# async def StartChat(query: str):
#     result = compiled_graph.invoke({
#         "messages": [
#             {"role": "user", "content": query}
#         ]
#     })

#     final_message = result["messages"][-1]
#     return {"response": final_message["content"]}


# CLI fallback
if __name__ == "__main__":

    print("Chatbot is running. what brings you here today? (type 'exit' to quit)")

    conversation = {"messages": []}

    while True:
        query = input("You: ").strip().lower()

        if query in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye 👋")
            break

        conversation["messages"].append({
            "role": "user",
            "content": query
        })

        result = compiled_graph.invoke(conversation)

        conversation = result   # ✅ safer
        final_message = conversation["messages"][-1]

        # Clean up Chain_of_thoughts for better CLI display
        cleaned = re.sub(r"<think>.*?</think>", "",
                         final_message["content"], flags=re.DOTALL)
        print("\nAssistant:", cleaned.strip())
