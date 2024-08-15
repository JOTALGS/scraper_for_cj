import os
import json

def main():
    # Define the paths
    data_file = './cjproducts/data_dictionary.json'
    image_directory = './cjproducts/'

    # Load the dictionary from the JSON file
    with open(data_file, 'r') as file:
        data = json.load(file)

    # Iterate through the dictionary and check image existence
    keys_to_remove = []
    for key, value in data.items():
        if value['image'] is None:
            keys_to_remove.append(key)
        else:
            image_path = os.path.join(image_directory, value['image'])
            print(os.path.exists(image_path))
            if not os.path.isfile(image_path):
                keys_to_remove.append(key)

    print(keys_to_remove)
    # Remove the entries with missing images
    for key in keys_to_remove:
        del data[key]

    # Save the updated dictionary back to the JSON file
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

    print("Updated dictionary saved.")

if __name__ == '__main__':
    main()