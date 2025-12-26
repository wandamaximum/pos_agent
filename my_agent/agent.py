from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv
from .mock_data import mock_raw_materials, mock_menu_items
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.models.lite_llm import LiteLlm # For multi-model support

import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

load_dotenv()
 
# AGENT_MODEL = "gemini-2.0-flash-lite"
AGENT_MODEL = "gpt-4o-mini"


def get_menu_item(menu: str) -> dict:
    menu_normilized = menu.lower()
    for key, data in mock_menu_items.items():
        if menu_normilized in key:
            enriched_data = data.copy()
            inventory_info = {}
            for ing in data.get("ingredients", []):
                if ing in mock_raw_materials:
                    inventory_info[ing] = mock_raw_materials[ing]
            enriched_data["inventory_status"] = inventory_info
            return enriched_data
    return {
        "status": "error",
        "error_message": f"Could not find any item matching `{menu_normilized}`"
    }



def get_all_menu() -> dict:
    """Returns the full menu with ingredient and inventory status."""
    full_menu_report = {}
    
    for item_name, data in mock_menu_items.items():
        enriched_data = data.copy()
        inventory_info = {}
        
        # Check stock for each ingredient in this menu item
        for ing in data.get("ingredients", []):
            if ing in mock_raw_materials:
                inventory_info[ing] = mock_raw_materials[ing]
        
        enriched_data["inventory_status"] = inventory_info
        full_menu_report[item_name] = enriched_data
        
    return full_menu_report


def get_item_production_capacity(menu: str) -> dict:
    """Calculates how many units of a menu item can be made based on current stock."""
    menu_normalized = menu.lower().strip()
    
    # 1. Find the menu item
    target_item = None
    item_display_name = ""
    for key, data in mock_menu_items.items():
        if menu_normalized in key.lower():
            target_item = data
            item_display_name = key
            break
            
    if not target_item:
        return {"error": f"Could not find item matching '{menu}'"}

    ingredients = target_item.get("ingredients", [])
    if not ingredients:
        return {"item": item_display_name, "max_capacity": "Unknown (no ingredients listed)"}

    # 2. Calculate capacity based on stock
    # Formula: floor(current_stock / quantity_required_per_unit)
    # Assuming quantity_required is 1 for this mock logic; 
    # if your mock_menu_items has specific quantities, use those instead.
    
    capacities = []
    for ing in ingredients:
        stock_level = mock_raw_materials.get(ing, 0)
        # Assuming each menu item uses 1 unit of the ingredient
        capacities.append(stock_level) 

    max_can_make = min(capacities) if capacities else 0

    return {
        "item": item_display_name,
        "max_capacity": max_can_make,
        "bottlenecks": [ing for ing in ingredients if mock_raw_materials.get(ing, 0) == max_can_make]
    }

# -----------------------------
# Shared SessionService
# -----------------------------
session_service = InMemorySessionService()

# -----------------------------
# Runner
# -----------------------------

APP_NAME = "Inventory_agent"
root_agent = Agent(
    model=LiteLlm(model=AGENT_MODEL),
    name="Inventory_agent",
    description="Provides inventory info about a menu item",
    instruction="""You are the Smart POS Inventory Assistant. 
                    When a user asks about a menu item, you MUST call 'get_menu_item'. 
                    if user ask about all men, you MUST CALL 'get_all_menu'.
                    if user ask about the capacity of an menu, you must call 'get_item_production_capacity'
                    Once you receive the data, summarize the ingredients and inventory status 
                    clearly for the user. If the item is not found, explain why.""",
    tools=[get_menu_item,get_all_menu,get_item_production_capacity]
)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# -----------------------------
# Call agent function
# -----------------------------
async def call_agent(query: str, runner, user_id: str, session_id: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response = "Agent did not produce final response"

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
      
        elif event.actions and event.actions.escalate:
            final_response = f"Agent escalated: {event.error_message or 'No specific message'}"
            break

    return final_response
