# Remitly_Internship_2024

## Description

Remitly Internship 2024 exercise. The project verifies the input JSON file. 
Input JSON file is defined as AWS::IAM::Role Policy. 
Returns False if an input JSON file is not a valid AWS::IAM::Role Policy or if JSON Resource field contains
a single asterisk. Returns True otherwise.

## Installation

1. Clone the repository to your local machine using the following command:
```bash
git clone https://github.com/Mil0szK/Remitly_Internship_2024.git
```

2. Install the project dependencies, navigate to the project directory and run the following command:
```bash
pip install -r requirements.txt
```

## Usage
1. Put the JSON file you want to verify in the project directory.
2. Run the project using the following command:
```bash
python -m json_verifying <json_file_path>
```

## Testing
To run the tests, navigate to the project directory and run the following command:
```bash
python -m unittest tests.test_verifier
```

## License

[MIT](https://choosealicense.com/licenses/mit/)