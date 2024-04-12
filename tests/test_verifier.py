import unittest
from pathlib import Path
import json
from json_verifying.verifier import load_json, check_required_keys, check_allows_keys, is_valid_aws_policy, is_json_valid


class TestJsonVerifier(unittest.TestCase):
    def test_check_required_keys(self):
        required_keys = ["PolicyName", "PolicyDocument"]
        data = load_json("tests/data/valid_policy.json")
        self.assertTrue(check_required_keys(data, required_keys))

        data = load_json("tests/data/missing_required_keys.json")
        self.assertFalse(check_required_keys(data['PolicyDocument'], required_keys))

        required_keys = ["Effect", "Action", "Resource"]
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertTrue(check_required_keys(statement, required_keys))

        data = load_json("tests/data/missing_required_keys.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertFalse(check_required_keys(statement, required_keys))

    def test_check_allows_keys(self):
        allowed_keys = ["Effect", "Action", "Resource", "Condition", "Sid", "NotAction", "NotResource", "Principal",
                        "NotPrincipal", "Version", "Statement"]
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertTrue(check_allows_keys(statement, allowed_keys))

        data = load_json("tests/data/invalid_allows_keys.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertFalse(check_allows_keys(statement, allowed_keys))

    def test_is_valid_aws_policy(self):
        data = load_json("tests/data/valid_policy.json")
        self.assertTrue(is_valid_aws_policy(data))

        data = load_json("tests/data/invalid_policy.json")
        self.assertFalse(is_valid_aws_policy(data))

    def test_is_json_valid(self):
        self.assertTrue(is_json_valid("tests/data/valid_policy.json"))
        self.assertFalse(is_json_valid("tests/data/invalid_policy.json"))

    def test_load_json(self):
        data = load_json("tests/data/valid_policy.json")
        self.assertIsInstance(data, dict)

    def test_check_required_keys_no_keys(self):
        required_keys = []
        data = load_json("tests/data/valid_policy.json")
        self.assertTrue(check_required_keys(data, required_keys))

    def test_check_allows_keys_no_keys(self):
        allowed_keys = []
        data = load_json("tests/data/valid_policy.json")
        for statement in data['PolicyDocument']['Statement']:
            self.assertFalse(check_allows_keys(statement, allowed_keys))

    def test_is_valid_aws_policy_invalid(self):
        data = load_json("tests/data/invalid_policy.json")
        self.assertFalse(is_valid_aws_policy(data))

    def test_json_file_not_exist(self):
        self.assertFalse(is_json_valid("tests/data/does_not_exist.json"))

    def test_json_file_not_json(self):
        self.assertFalse(is_json_valid("tests/data/valid_policy.txt"))

