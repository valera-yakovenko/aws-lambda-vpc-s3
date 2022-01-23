import requests
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response["Body"].read()
        decoded_file_content = file_content.decode("utf-8")
        print("File content:")
        print(decoded_file_content)

        x = len(decoded_file_content.splitlines())
        print('Total number of lines in a file:', x)
        print("--------")
        print("Filtered range of id prefixes:")
        print(ip_counter())
        return decoded_file_content, ip_counter()
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e


def ip_counter():
    r = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
    c = r.json()
    dict_of_list = c["prefixes"]
    wave_one = list(filter(lambda item: item['region'] == 'eu-west-1', dict_of_list))
    wave_two = list(filter(lambda item: item['service'] == 'API_GATEWAY', wave_one))
    final_list = [i["ip_prefix"] for i in wave_two]
    return final_list
