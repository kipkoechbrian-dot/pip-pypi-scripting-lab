import argparse
from datetime import datetime
import requests

def fetch_data():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return {}

def generate_log(log_data=None):
    if log_data is None:
        log_data = ["User logged in", "User updated profile", "Report exported"]
        
    if not isinstance(log_data, list):
        raise TypeError("Log data must be a list")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automating Python Projects CLI Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add-task", help="Simulate adding a task")
    add_parser.add_argument("name", help="Name of the task")
    
    complete_parser = subparsers.add_parser("complete-task", help="Simulate completing a task")
    complete_parser.add_argument("name", help="Name of the task")
    
    args = parser.parse_args()
    
    post = fetch_data()
    api_title = post.get("title", "No title found")
    print("Fetched Post Title:", api_title)
    
    if args.command == "add-task":
        custom_entries = [f"Add task command executed for: {args.name}", f"Context: {api_title}"]
        generate_log(custom_entries)
    elif args.command == "complete-task":
        custom_entries = [f"Complete task command executed for: {args.name}"]
        generate_log(custom_entries)
    else:
        generate_log()