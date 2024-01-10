def load_config(file_path):
    """Util function to load config data from yaml files.

    Args:
        file_path: A string for the name of the yaml file.

    Returns:
        A dictionary with all config data parsed from yaml file.
    """
    with open(f'mysql/{file_path}', 'r') as yaml_file:
        lines = yaml_file.readlines()

    config = {}

    for ind, line in enumerate(lines):
        if ind != 0:
            key, value = map(str.strip, line.split(":"))
            config[key] = value

    return config