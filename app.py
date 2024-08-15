import os
import logging
import requests
from botbuilder.core import BotFrameworkAdapter, TurnContext, BotFrameworkAdapterSettings
from botbuilder.schema import Activity, ActivityTypes
from aiohttp import web
import aiohttp

# Initialize the bot adapter Hardcoded credentials, USE KEY VAULT
settings = BotFrameworkAdapterSettings(app_id="x", app_password="x")
adapter = BotFrameworkAdapter(settings)

# Hardcoded Token, USE KEY VAULT
DATABRICKS_TOKEN = "x"

async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    
    async def turn_handler(turn_context: TurnContext):
        if activity.type == ActivityTypes.message:
            try:
                response = await query_llama3_model(turn_context.activity.text)
            except Exception as e:
                logging.error(f"Error in query_llama3_model: {e}")
                response = "Error querying the model."
            await turn_context.send_activity(Activity(type=ActivityTypes.message, text=response))
    
    await adapter.process_activity(activity, auth_header, turn_handler)
    return web.Response(status=200)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, host=host, port=port)

async def query_llama3_model(user_input):
    url = "https://x"
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error calling the model" 