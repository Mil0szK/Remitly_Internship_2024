import json
from pathlib import Path


def load_json(file_path: str) -> dict:
    try:
        with open(file_path) as f:
            data = json.load(f)
    except ValueError:
        raise ValueError(f"File {file_path} is not in valid JSON format.")
    return data


def check_required_keys(data: dict, required_keys: list) -> bool:
    if not all(key in data for key in required_keys):
        print(f"Required keys are missing in {data}")
        return False
    return True


def check_allows_keys(data: dict, allowed_keys: list) -> bool:
    for key in data:
        if key not in allowed_keys:
            print(f"Key {key} is not allowed in {data}")
            return False
    return True


def is_valid_aws_policy(data: dict) -> bool:
    required_keys = ["PolicyName", "PolicyDocument"]

    if not check_required_keys(data, required_keys):
        return False

    if 'PolicyDocument' in data:
        required_keys = ["Version", "Statement"]
        allowed_keys = ["Version", "Statement", "Id"]
        if not check_required_keys(data['PolicyDocument'], required_keys):
            return False
        if not check_allows_keys(data['PolicyDocument'], allowed_keys):
            return False

    if 'Statement' in data['PolicyDocument']:
        required_keys = ["Effect", "Action", "Resource"]
        allowed_keys = ["Effect", "Action", "Resource", "Condition", "Sid", "NotAction", "NotResource", "Principal",
                        "NotPrincipal", "Version", "Statement"]
        for statement in data['PolicyDocument']['Statement']:
            if not check_required_keys(statement, required_keys):
                return False
            if not check_allows_keys(statement, allowed_keys):
                return False

    return True


def is_json_valid(json_file: str) -> bool:
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"File {json_file} does not exist.")
        return False

    if json_path.suffix != ".json":
        print(f"File {json_file} is not a JSON file.")
        return False

    data = load_json(json_file)

    if type(data) is not dict:
        print(f"File {json_file} does not contain a JSON object.")
        return False

    if not is_valid_aws_policy(data):
        return False

    for statement in data['PolicyDocument']['Statement']:
        res_data = statement.get('Resource')
        if isinstance(res_data, str) and res_data == "*":
            return False

    return True

