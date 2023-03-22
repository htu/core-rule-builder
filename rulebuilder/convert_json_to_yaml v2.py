import io
import re
import json
import sys
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def convert_json_to_yaml(json_data, output_file=None, write_to_file=False):
    """
    Convert JSON data with comments to YAML, preserving the comments.

    :param json_data: The input JSON data as a string.
    :param output_file: An optional output file name. If not provided, the function will return the YAML data without writing it to a file.
    :param write_to_file: An optional boolean flag to decide whether to write the output to a file. If set to `True`, the output will be written to the specified file. Otherwise, the YAML data will be returned.
    :return: The YAML data if `write_to_file` is set to `False`.
    """

    # Initialize ruamel.yaml
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    # Load JSON data as a dictionary
    data = json.loads(json_data)
    re_pat = r"#\s+(\w+)" 

    # Create a CommentedMap to store the data with comments
    yaml_data = CommentedMap()
    first_key = None 
    for key, value in data.items():
        # print(f"1 - {key}: {value}")
        if key.startswith("# "):
            k1 = re.search(re_pat, key).group(1)
            v1 = str(k1) + ": " + value
            # print(f" . K1: {k1}")
            # if (k1 is None): 
            #     k1 = first_key
            # if k1 is None:
            #     k1 = key
            #     v1 = value  
            # else: 
            #     v1 = str(k1) + ": " + value
            # print(f"  - {k1}: {v1}\n  - {key}: {value}")
            yaml_data.yaml_set_comment_before_after_key(
                k1, before=v1, after=None)
            continue
        else: 
            if first_key is None: 
                first_key = key 

        yaml_data[key] = value

    if write_to_file and output_file:
        # Save the YAML data to a file
        with open(output_file, 'w') as outfile:
            yaml.dump(yaml_data, outfile)
    else:
        return yaml_data


if __name__ == "__main__":
    json_data = '''
    {
      "# name": "This is a comment for the name field",
      "name": "John",
      "# age": "This is a comment for the age field",
      "age": 30,
      "# city": "This is a comment for the city field",
      "city": "New York",
      "# Any": "Any comment1",
      "# any": "Any comment2"
    }
    '''
    yaml = YAML()

    # Test case 1: Write the output to a file
    convert_json_to_yaml(
        json_data, output_file='output.yml', write_to_file=True)

    # Test case 2: Get the YAML data without writing to a file
    yaml_data = convert_json_to_yaml(json_data)

    # Create an in-memory text stream
    text_stream = io.StringIO()

    # Dump the YAML data into the text stream
    yaml.dump(yaml_data, text_stream)

    # Reset the text stream position
    text_stream.seek(0)

    # Print the resulting YAML data
    for line in text_stream:
        print(line, end='')

    print(yaml_data)
