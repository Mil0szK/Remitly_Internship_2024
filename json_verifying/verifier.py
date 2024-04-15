import json
from pathlib import Path
from enum import Enum


class ErrorMessages(Enum):
    # Define error messages
    FILE_NOT_EXIST = "File does not exist."
    NOT_JSON_FILE = "File is not a JSON file."
    MISSING_STATEMENT = "Statement is missing in PolicyDocument."
    MISSING_REQUIRED_KEYS = "Required keys are missing."
    NOT_ALLOWED_KEYS = "Keys are not allowed."
    INVALID_RESOURCE = "Resource is invalid."
    MISSING_POLICY = "Policy is missing."
    INVALID_STATEMENT = "Statement is invalid."
    INVALID_POLICY = "Policy is invalid."
    MISSING_RESOURCE = "Resource is missing."


def load_json(file_path: str) -> dict:
    try:
        with open(file_path) as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                raise ValueError(ErrorMessages.NOT_JSON_FILE.value)
    except FileNotFoundError:
        raise ValueError(ErrorMessages.FILE_NOT_EXIST.value)


def check_required_keys(data: dict, required_keys: list) -> bool:
    if not all(key in data for key in required_keys):
        return False
    return True


def check_allows_keys(data: dict, allowed_keys: list) -> bool:
    for key in data:
        if key not in allowed_keys:
            return False
    return True


def is_valid_aws_policy(data: dict):
    required_keys = ["PolicyName", "PolicyDocument"]

    if not check_required_keys(data, required_keys):
        return ErrorMessages.MISSING_REQUIRED_KEYS.value

    if 'PolicyDocument' in data:
        required_keys = ["Version", "Statement"]
        allowed_keys = ["Version", "Statement", "Id"]
        if not check_required_keys(data['PolicyDocument'], required_keys):
            return ErrorMessages.MISSING_REQUIRED_KEYS.value
        if not check_allows_keys(data['PolicyDocument'], allowed_keys):
            return ErrorMessages.NOT_ALLOWED_KEYS.value
    else:
        return ErrorMessages.MISSING_POLICY.value

    if 'Statement' not in data['PolicyDocument']:
        return ErrorMessages.MISSING_STATEMENT.value
    for statement in data['PolicyDocument']['Statement']:
        if not check_required_keys(statement, ["Effect", "Action", "Resource"]):
            return ErrorMessages.MISSING_REQUIRED_KEYS.value
        if not check_allows_keys(statement,
                                 ["Effect", "Action", "Resource", "Condition", "Sid", "NotAction", "NotResource",
                                  "Principal", "NotPrincipal", "Version", "Statement"]):
            return ErrorMessages.NOT_ALLOWED_KEYS.value

    return True


def is_json_valid(json_file: str):
    json_path = Path(json_file)
    if not json_path.exists():
        return ErrorMessages.FILE_NOT_EXIST.value

    if json_path.suffix != ".json":
        return ErrorMessages.NOT_JSON_FILE.value

    data = load_json(json_file)

    if type(data) is not dict:
        return ErrorMessages.INVALID_POLICY.value

    if is_valid_aws_policy(data) != True:
        return ErrorMessages.INVALID_POLICY.value

    for statement in data['PolicyDocument']['Statement']:
        try:
            res_data = statement.get('Resource')
        except AttributeError:
            return ErrorMessages.MISSING_RESOURCE.value
        if isinstance(res_data, str):
            return res_data != "*"

        else:
            return ErrorMessages.INVALID_RESOURCE.value

    return True
