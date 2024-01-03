import tempfile


def convert_to_txt(file_path):
    # Convert file to temporary .txt format
    if not file_path.endswith(".txt"):
        with open(file_path, 'rb') as source_file:
            with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False, errors='ignore') as txt_file:
                txt_file.write(source_file.read().decode('utf-8', errors='ignore'))
                return txt_file.name
    else:
        return file_path


def read_text_from_file(file_path):
    with open(file_path, 'rb', errors='ignore') as file:
        return file.read()


def save_hash_to_file(hash_value, filename):
    # Open the file in write mode ('w') with append behavior
    with open(filename, 'w') as file:
        file.write(hash_value)
