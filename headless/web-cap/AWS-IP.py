import requests
import json


def get_aws_ip_range():
    """
    Get AWS IP ranges from AWS API
    """
    # print("Get AWS IP ranges")

    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    # print("Response: ", response)
    data = json.loads(response.text)

    return data


def main():
    """
    Main function
    """
    data = get_aws_ip_range()
    for x in data["prefixes"]:

        print(x["ip_prefix"])
    # print(len(data["prefixes"]))


if __name__ == "__main__":
    main()