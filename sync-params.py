import boto3

def check_parameter_existence(parameter_name):
    ssm_client = boto3.client('ssm')
    try:
        response = ssm_client.get_parameter(Name=parameter_name)
        return True
    except ssm_client.exceptions.ParameterNotFound:
        return False

def update_parameter(parameter_name, parameter_value):
    ssm_client = boto3.client('ssm')
    response = ssm_client.put_parameter(
        Name=parameter_name,
        Value=parameter_value,
        Type='String',
        Overwrite=True
    )
    print(f"Parameter '{parameter_name}' updated in Parameter Store.")

def read_properties_file(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                properties[key.strip()] = value.strip()
    return properties

def translate_key_to_parameter_path(key):
    return "/app/" + key.replace('.', '/')

def stage_properties_as_parameters(properties_file_path):
    properties = read_properties_file(properties_file_path)
    for key, value in properties.items():
        parameter_name = translate_key_to_parameter_path(key)
        if check_parameter_existence(parameter_name):
            ssm_client = boto3.client('ssm')
            response = ssm_client.get_parameter(Name=parameter_name)
            existing_value = response['Parameter']['Value']
            if existing_value != value:
                update_parameter(parameter_name, value)
            else:
                print(f"Parameter '{parameter_name}' already up to date.")
        else:
            update_parameter(parameter_name, value)

# Usage example
properties_file_path = 'path/to/properties/file.properties'
stage_properties_as_parameters(properties_file_path)
