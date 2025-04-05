import json

def extract_json_from_scm(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        json_str = ''.join(lines[2:-1])
        return json.loads(json_str)

def correct_json_data(json_data):
    corrections = [
        {"$Type": "Button", "Image": "kitty.png"},
        {"$Type": "Label", "Text": "pet the kitty"},
        {"$Type": "Sound", "Source": "meow.mp3"}
    ]
    score = 0
    total_items = len(corrections)

    for component in json_data["Properties"]["$Components"]:
        for correction in corrections:
            if all(item in component.items() for item in correction.items()):
                score += 1

    return json_data, (score / total_items) * 100

file_path = 'Screen1.scm'
json_data = extract_json_from_scm(file_path)
corrected_json_data, score = correct_json_data(json_data)

print(json.dumps(corrected_json_data, indent=2))
print(f"Score: {score}%")