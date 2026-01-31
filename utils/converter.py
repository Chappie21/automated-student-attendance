import json
import re

def convertToList(data: str) -> list:
    try:
        start_index = data.find('[')
        end_index = data.rfind(']') + 1
        
        if start_index == -1 or end_index == 0:
            print("No JSON list found in the response.")
            return []

        json_str = data[start_index:end_index]
        
        return json.loads(json_str) 
    except Exception as e:
        print(f"Error on convert to array: {e}")
        return []