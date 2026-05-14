"""NLP Service - Natural Language Processing for chatbot and intent understanding."""

import logging
import re
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class NLPService:
    """NLP service for travel-related conversations and intent recognition."""

    # Intent patterns
    INTENT_PATTERNS = {
        "ask_destination": [
            r"(where|which destination|should i go|best place)",
            r"(recommendation|suggest|where to)",
        ],
        "ask_budget": [
            r"(how much|cost|price|budget|expensive)",
            r"(afford|spend)",
        ],
        "ask_activity": [
            r"(what to do|activities|things to do|attraction)",
            r"(fun|entertainment)",
        ],
        "ask_accommodation": [
            r"(where to stay|hotel|accommodation|hostel)",
            r"(place to sleep|rooms)",
        ],
        "ask_transport": [
            r"(how to get|transport|flight|train|bus)",
            r"(travel to|reach)",
        ],
        "ask_food": [
            r"(eat|food|restaurant|cuisine|dining)",
            r"(taste|local food)",
        ],
        "ask_weather": [
            r"(weather|temperature|climate|rain|cold|hot)",
            r"(rainy|sunny)",
        ],
        "ask_duration": [
            r"(how long|days|weeks|duration)",
            r"(spend time)",
        ],
        "ask_group": [
            r"(group|together|friends|family|people)",
            r"(members|persons)",
        ],
        "greeting": [
            r"(hello|hi|hey|good morning|good evening)",
            r"(welcome|greetings)",
        ],
    }

    # Entity patterns
    ENTITY_PATTERNS = {
        "DESTINATION": [
            r"(paris|tokyo|bali|newyork|barcelona|london|dubai|singapore)",
            r"(france|japan|indonesia|usa|spain|uk|uae)",
        ],
        "BUDGET": [
            r"(\$?[\d,]+(\.\d+)?)",  # Currency amounts
        ],
        "DURATION": [
            r"(\d+)\s*(days?|weeks?|nights?)",
        ],
        "NUMBER": [
            r"(\d+)\s*(people|persons|group|members|friends)",
        ],
    }

    def __init__(self):
        """Initialize NLP service."""
        pass

    def process_message(self, message: str) -> Dict:
        """Process user message and extract intent and entities."""
        try:
            message_lower = message.lower().strip()

            # Detect intent
            intent = self.detect_intent(message_lower)

            # Extract entities
            entities = self.extract_entities(message_lower)

            # Generate response
            response = self.generate_response(intent, entities, message)

            return {
                "user_message": message,
                "intent": intent,
                "confidence": self._calculate_confidence(message_lower, intent),
                "entities": entities,
                "bot_response": response,
                "suggestions": self._get_suggestions(intent, entities),
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "user_message": message,
                "intent": "unknown",
                "confidence": 0.0,
                "entities": {},
                "bot_response": "I'm not sure how to help with that. Could you rephrase?",
                "suggestions": [],
            }

    def detect_intent(self, message: str) -> str:
        """Detect user intent from message."""
        try:
            for intent, patterns in self.INTENT_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, message, re.IGNORECASE):
                        return intent

            return "general_inquiry"

        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            return "unknown"

    def extract_entities(self, message: str) -> Dict:
        """Extract entities from message."""
        try:
            entities = {}

            # Extract destinations
            destinations = []
            for pattern in self.ENTITY_PATTERNS.get("DESTINATION", []):
                matches = re.findall(pattern, message, re.IGNORECASE)
                destinations.extend(matches)
            if destinations:
                entities["destinations"] = list(set(destinations))

            # Extract budget
            budget_matches = re.findall(self.ENTITY_PATTERNS["BUDGET"][0], message)
            if budget_matches:
                entities["budget"] = budget_matches[0][0]

            # Extract duration
            duration_matches = re.findall(self.ENTITY_PATTERNS["DURATION"][0], message)
            if duration_matches:
                entities["duration"] = {
                    "value": duration_matches[0][0],
                    "unit": duration_matches[0][1],
                }

            # Extract group size
            group_matches = re.findall(self.ENTITY_PATTERNS["NUMBER"][0], message)
            if group_matches:
                entities["group_size"] = group_matches[0][0]

            return entities

        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {}

    def generate_response(
        self, intent: str, entities: Dict, original_message: str
    ) -> str:
        """Generate response based on intent and entities."""
        try:
            responses = {
                "greeting": [
                    "Hello! 👋 I'm here to help you plan your perfect trip. What would you like to know about?",
                    "Hi there! 🌍 Let's plan an amazing journey together. What can I help you with?",
                ],
                "ask_destination": [
                    "I'd recommend checking out popular destinations based on your interests and budget. Where would you like to go?",
                    "There are many amazing places to explore! What's your travel style - adventure, relaxation, or cultural?",
                ],
                "ask_budget": [
                    f"Based on your preferences, typical costs range from $50-200 per day depending on your travel style.",
                    "Budget planning depends on accommodation, food, and activities. Tell me your travel style preference!",
                ],
                "ask_activity": [
                    "There are tons of activities available! What interests you most - adventure, culture, food, or relaxation?",
                    "I can suggest activities based on your destination and interests. Tell me more!",
                ],
                "ask_accommodation": [
                    "Accommodation options range from luxury hotels to budget hostels. What's your preference?",
                    "Would you prefer hotels, hostels, or vacation rentals? Let me know your budget!",
                ],
                "ask_transport": [
                    "I can help with transport suggestions. Where are you traveling from and to?",
                    "Transport options depend on your destination. Tell me more about your trip!",
                ],
                "ask_food": [
                    "Food is a great part of travel! Want recommendations for local cuisine or restaurants?",
                    "I'd love to suggest local food experiences. What cuisines do you enjoy?",
                ],
                "ask_weather": [
                    "Weather is important for planning! Which destination and season are you considering?",
                    "Let me check the typical weather for your chosen destination!",
                ],
                "ask_group": [
                    f"Planning for {entities.get('group_size', 'a')} person group? I can help optimize for group travel!",
                    "Group travel planning is important. Let's make sure everyone is happy!",
                ],
                "ask_duration": [
                    f"A {entities.get('duration', {}).get('value', 'few')} {entities.get('duration', {}).get('unit', 'day')} trip is great!",
                    "Trip duration affects budget and activity planning. Let's figure it out!",
                ],
                "general_inquiry": [
                    "I'm here to help with travel planning! Ask me about destinations, budgets, activities, or accommodations.",
                    "What aspect of your trip would you like to plan first?",
                ],
                "unknown": [
                    "I'm not sure I understand. Could you rephrase that?",
                    "I'm still learning! Can you tell me more about what you need?",
                ],
            }

            response_options = responses.get(intent, responses["unknown"])
            return (
                response_options[0]
                if response_options
                else "How can I help with your travel plans?"
            )

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Let me help you plan your trip!"

    def extract_travel_preferences(self, conversation_history: List[str]) -> Dict:
        """Extract travel preferences from conversation history."""
        try:
            preferences = {
                "destinations": [],
                "budget": None,
                "duration": None,
                "activities": [],
                "accommodation_type": None,
                "group_size": None,
                "travel_style": None,
            }

            for message in conversation_history:
                entities = self.extract_entities(message.lower())

                if "destinations" in entities:
                    preferences["destinations"].extend(entities["destinations"])

                if "budget" in entities:
                    preferences["budget"] = entities["budget"]

                if "duration" in entities:
                    preferences["duration"] = entities["duration"]

                if "group_size" in entities:
                    preferences["group_size"] = int(entities["group_size"])

                # Extract travel style
                if re.search(r"luxury|upscale|premium", message):
                    preferences["travel_style"] = "luxury"
                elif re.search(r"budget|cheap|affordable", message):
                    preferences["travel_style"] = "budget"
                else:
                    preferences["travel_style"] = "mid-range"

            return preferences

        except Exception as e:
            logger.error(f"Error extracting preferences: {str(e)}")
            return {}

    def get_chatbot_suggestions(self, context: Dict) -> List[str]:
        """Get chatbot suggestions based on context."""
        try:
            suggestions = []

            if not context.get("destination"):
                suggestions.append("Tell me your desired destination")
            else:
                suggestions.append(f"Learn more about {context['destination']}")

            if not context.get("budget"):
                suggestions.append("Share your budget")
            else:
                suggestions.append("Optimize budget allocation")

            if not context.get("activities"):
                suggestions.append("Browse activities")
            else:
                suggestions.append("More activity suggestions")

            suggestions.append("See accommodation options")

            return suggestions

        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return []

    def _calculate_confidence(self, message: str, intent: str) -> float:
        """Calculate confidence of intent detection."""
        if intent == "unknown":
            return 0.0

        confidence = 0.5

        # Increase confidence based on message length and clarity
        if len(message.split()) >= 3:
            confidence += 0.2

        # Check for multiple relevant keywords
        keywords = sum(
            1
            for pattern in self.INTENT_PATTERNS.get(intent, [])
            if re.search(pattern, message, re.IGNORECASE)
        )
        confidence += min(keywords * 0.1, 0.3)

        return min(confidence, 1.0)

    def _get_suggestions(self, intent: str, entities: Dict) -> List[str]:
        """Get follow-up suggestions based on intent."""
        suggestions = []

        if intent == "ask_destination":
            suggestions = [
                "Popular destinations",
                "Hidden gems",
                "Budget-friendly places",
            ]
        elif intent == "ask_budget":
            suggestions = ["Budget breakdown", "Money-saving tips", "Expense tracking"]
        elif intent == "ask_activity":
            suggestions = ["Adventure activities", "Cultural experiences", "Food tours"]
        elif intent == "ask_accommodation":
            suggestions = ["Luxury hotels", "Budget hostels", "Unique stays"]

        return suggestions
