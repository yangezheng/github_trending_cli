from pprint import pprint
from .github_api import get_api_root

def main():
    data = get_api_root()

    print(data)

if __name__ == "__main__":
    main()
