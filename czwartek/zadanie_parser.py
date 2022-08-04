import csv
import json
from collections import namedtuple, defaultdict
from datetime import datetime
import logging

logging.basicConfig()

ValueWithData = namedtuple('ValueWithTime', 'ID Value Timestamp')  # Grouped data tuplce
fields_type = {'ID': int,
               'Value': float}


def csv_data_reader(path: str) -> dict:
    """
    Reads a csv file and converts it to a dictionary.

    Any exception will make the function return None

    :param path: path to source file with data
    :return: dictionary or None in case of failure
    """
    output_dict = defaultdict(lambda: {'Values': []})  # Default output dict structure
    try:
        with open(path) as f:
            csv_reader = csv.DictReader(f)
            try:
                Row = namedtuple('Row', csv_reader.fieldnames)
            except ValueError:
                logging.error('CSV headers have incorrect keys')
                return None

            for index, row in enumerate(csv_reader, 1):
                type_cast = {}
                try:
                    for key, value in row.items():
                        type_cast[key] = (lambda k, v: fields_type[k](v) if k in fields_type else v)(key, value)
                except KeyError:
                    logging.error(f'Key {key} was not found, csv not parsed')
                    return None
                except (ValueError, TypeError) as e:
                    logging.error(f'Conversion error in row "{index}", field "{key}": {e}')
                    return None

                # Convert the data into output format
                try:
                    type_cast = Row(**type_cast)
                    # get dict key or init it with default if it doesn't exist
                    temp_dict = output_dict[type_cast.Description]

                    temp_dict['Values'].append({
                        'ID': type_cast.ID,
                        'Value': type_cast.Value,
                        'Timestamp': datetime.strptime(type_cast.Timestamp, '%Y-%m-%d %H:%M:%S').strftime(
                            '%d-%m-%Y %H:%M:%S')
                    })
                except AttributeError as e:
                    logging.error(f'Missing Attribute in "Row" namedtuple: {e}')
                    return None
                except ValueError as e:
                    logging.error(f'Time conversion error in row "{index}", field "{key}": {e}')
                    return None

        return output_dict
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f'Unable to access file: {e}')


def json_writer(path: str, data: dict):
    """
    Writes grouped sensor data to JSON file

    :param path: path to output file
    :param data: grouped sensor reading data
    """
    try:
        output_json_string = json.dumps(data, indent=4)
        print(output_json_string)

        with open(path, 'w') as json_file:
            json.dump(output_json_string, json_file)
    except TypeError as e:
        logging.error(f'Could not convert to JSON: {e}')
    except (PermissionError, FileNotFoundError) as e:
        logging.error(f'Could not access {path}: {e}')


if __name__ == '__main__':
    grouped_data = csv_data_reader('input_data.csv')

    if grouped_data:
        # Data converted to json
        print('Success! Converting data to JSON...')
        json_writer('json_output.json', grouped_data)
