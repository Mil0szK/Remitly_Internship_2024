import unittest
from pathlib import Path
import json
from json_verifying.verifier import load_json, check_required_keys, check_allows_keys, is_valid_aws_policy, is_json_valid, ErrorMessages


class TestErrorMessages(unittest.TestCase):
    def test_error_messages(self):
        self.assertEqual(ErrorMessages.FILE_NOT_EXIST.value, "File does not exist.")
        self.assertEqual(ErrorMessages.NOT_JSON_FILE.value, "File is not a JSON file.")
        self.assertEqual(ErrorMessages.MISSING_STATEMENT.value, "Statement is missing in PolicyDocument.")
        self.assertEqual(ErrorMessages.MISSING_REQUIRED_KEYS.value, "Required keys are missing.")
        self.assertEqual(ErrorMessages.NOT_ALLOWED_KEYS.value, "Keys are not allowed.")
        self.assertEqual(ErrorMessages.INVALID_RESOURCE.value, "Resource is invalid.")
        self.assertEqual(ErrorMessages.MISSING_POLICY.value, "Policy is missing.")
        self.assertEqual(ErrorMessages.INVALID_STATEMENT.value, "Statement is invalid.")
        self.assertEqual(ErrorMessages.INVALID_POLICY.value, "Policy is invalid.")
        self.assertEqual(ErrorMessages.MISSING_RESOURCE.value, "Resource is missing.")


class TestJsonVerifier(unittest.TestCase):
    def test_check_required_keys(self):
        required_keys = ["PolicyName", "PolicyDocument"]
        data = load_json("tests/data/valid_policy.json")
        self.assertEqual(check_required_keys(data, required_keys), True)

        data = load_json("tests/data/missing_required_keys.json")
        self.assertEqual(check_required_keys(data['PolicyDocument'], required_keys), False)

        required_keys = ["Effect", "Action", "Resource"]
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertEqual(check_required_keys(statement, required_keys), True)

        data = load_json("tests/data/missing_required_keys.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertEqual(check_required_keys(statement, required_keys), False)

    def test_check_allows_keys(self):
        allowed_keys = ["Effect", "Action", "Resource", "Condition", "Sid", "NotAction", "NotResource", "Principal",
                        "NotPrincipal", "Version", "Statement"]
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertEqual(check_allows_keys(statement, allowed_keys), True)

        data = load_json("tests/data/invalid_allows_keys.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertEqual(check_allows_keys(statement, allowed_keys), False)

    def test_is_valid_aws_policy(self):
        data = load_json("tests/data/valid_policy.json")
        self.assertEqual(is_valid_aws_policy(data), True)
        data = load_json("tests/data/invalid_policy.json")
        self.assertEqual(is_valid_aws_policy(data), ErrorMessages.MISSING_REQUIRED_KEYS.value)

    def test_is_json_valid(self):
        self.assertEqual(is_json_valid("tests/data/valid_policy.json"), True)
        self.assertEqual(is_json_valid("tests/data/invalid_policy.json"), ErrorMessages.INVALID_POLICY.value)

    def test_load_json(self):
        data = load_json("tests/data/valid_policy.json")
        self.assertIsInstance(data, dict)

    def test_check_required_keys_no_keys(self):
        required_keys = []
        data = load_json("tests/data/valid_policy.json")
        self.assertEqual(check_required_keys(data, required_keys), True)

    def test_check_allows_keys_no_keys(self):
        allowed_keys = []
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertEqual(check_allows_keys(statement, allowed_keys), False)

    def test_is_valid_aws_policy_invalid(self):
        data = load_json("tests/data/invalid_policy.json")
        self.assertEqual(is_valid_aws_policy(data), ErrorMessages.MISSING_REQUIRED_KEYS.value)

    def test_json_file_not_exist(self):
        self.assertEqual(is_json_valid("tests/data/does_not_exist.json"), ErrorMessages.FILE_NOT_EXIST.value)

    def test_json_file_not_json(self):
        self.assertEqual(is_json_valid("tests/data/valid_policy.txt"), ErrorMessages.NOT_JSON_FILE.value)

    def test_json_valid_but_with_asterisk(self):
        self.assertEqual(is_json_valid("tests/data/valid_but_with_asterisk.json"), False)
