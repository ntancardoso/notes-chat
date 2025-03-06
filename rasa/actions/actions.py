from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionSearchNotes(Action):
    def name(self) -> Text:
        return "action_search_notes"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.latest_message.get('text')
        response = requests.get(f"http://localhost:8000/notes/search/?query={query}")
        notes = response.json()
        
        if notes:
            answer = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
            dispatcher.utter_message(text=f"Here's what I found:\n{answer}")
        else:
            dispatcher.utter_message(text="I couldn't find any notes matching your query.")
        
        return []