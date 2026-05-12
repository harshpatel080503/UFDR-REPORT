from typing import List, Dict

def get_tools_schema() -> List[Dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "CreateTicket",
                "description": "MANDATORY TOOL: Call this if the user asks for information (suspects, dates, files) that is NOT present in the provided forensic report or initial logs. Do NOT speculate or invent answers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Specific detail that is missing (e.g., 'No data for user Y on Jan 12')."
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "default": "medium"
                        }
                    },
                    "required": ["summary"]
                }
            }
        }
    ]
