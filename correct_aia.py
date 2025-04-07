import json
import zipfile
import os

def extract_scm_from_aia(aia_file_path, screen_name):
    """
    Extracts the .scm file for the specified screen from the .aia file.
    """
    with zipfile.ZipFile(aia_file_path, 'r') as zip_ref:
        # Construct the path to the .scm file inside the .aia archive
        scm_file_path = f"{screen_name}.aia"
        for file_name in zip_ref.namelist():
            if file_name.endswith(".scm"):
                zip_ref.extract(file_name, "outcome")
                return os.path.join("outcome", file_name)
    raise FileNotFoundError(f"{screen_name}.scm not found in the .aia file.")

# Function to extract JSON data from a .scm file
def extract_json_from_scm(file_path):
    """
    Reads a .scm file, extracts the JSON content, and parses it into a Python dictionary.
    Assumes the JSON content starts from the third line and ends before the last line.
    
    Args:
        file_path (str): Path to the .scm file.
    
    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Skip the first two lines and the last line
        json_str = ''.join(lines[2:-1])
        return json.loads(json_str)

# Function to validate and score JSON data based on predefined corrections
def correct_json_data(json_data):
    """
    Validates the JSON data by comparing it to a set of predefined corrections.
    Calculates a score based on how many corrections match the components in the JSON data.
    
    Args:
        json_data (dict): JSON data extracted from the .scm file.
    
    Returns:
        tuple: The original JSON data and the calculated score as a percentage.
    """
    # Predefined corrections to validate against
    corrections = [
        {"$Type": "Button", "Image": "kitty.png"},
        {"$Type": "Label", "Text": "pet the kitty"},
        {"$Type": "Sound", "Source": "meow.mp3"},
        {"$Type": "Player", "Source": "meow.mp3"}
    ]
    score = 0  # Initialize the score
    total_items = len(corrections)  # Total number of corrections

    # Iterate through components in the JSON data
    for component in json_data["Properties"]["$Components"]:
        # Check if the component matches any of the corrections
        for correction in corrections:
            if all(item in component.items() for item in correction.items()):
                score += 1  # Increment the score for each match

    # Return the original JSON data and the score as a percentage
    return json_data, (score / total_items) * 100

# Main script execution
if __name__ == "__main__":
    aia_file_path = 'Hello_Purr.aia'  # Path to the .aia file
    screen_name = '*.scm'       # Name of the screen to process

    #try:
        # Step 1: Extract the .scm file from the .aia archive
    try:
        scm_file_path = extract_scm_from_aia(aia_file_path, screen_name)
    except FileNotFoundError as e:
        print(e)
        exit(1)  # Stop the process if no .scm file is found

    """  # Step 2: Extract JSON data from the .scm file
    json_data = extract_json_from_scm(scm_file_path)
    
    # Step 3: Validate and score the JSON data
    corrected_json_data, score = correct_json_data(json_data)
    
    # Step 4: Print the corrected JSON data in a formatted way
    print(json.dumps(corrected_json_data, indent=2))
    
    # Step 5: Print the score as a percentage
    print(f"Score: {score}%")
finally:
    # Clean up temporary files
    import shutil
    if os.path.exists("temp"):
        shutil.rmtree("temp") """