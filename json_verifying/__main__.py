from json_verifying.verifier import is_json_valid
import argparse


def main():
    parse = argparse.ArgumentParser(prog="json_verifying", description="Verify JSON files")
    parse.add_argument("json_file", help="Path to the JSON file")
    args = parse.parse_args()

    result = is_json_valid(args.json_file)
    if result == True:
        print(f"File {args.json_file} is a valid JSON file.")
        return True
    elif result == False:
        print(f"File {args.json_file} is valid, but contains '*' in Resource.")
        return False
    else:
        print(f"File {args.json_file} is not a valid JSON file.")
        return True


if __name__ == "__main__":
    main()
