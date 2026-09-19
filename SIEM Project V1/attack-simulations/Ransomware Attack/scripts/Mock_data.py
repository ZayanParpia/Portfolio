import json
import os
import random
import string
import sys
from pathlib import Path


file_types = {
    ".txt": [
        "Company Meeting Notes",
        "Project Requirements",
        "Employee Notes",
        "Security Policy",
        "Important Information",
    ],
    ".csv": [
        "Employee Database",
        "Customer Records",
        "Financial Records",
        "Inventory",
    ],
    ".json": [
        "Application Config",
        "User Database",
        "System Settings",
        "API Configuration",
    ],
    ".log": [
        "Server Log",
        "Security Log",
        "Application Log",
        "Access Log",
    ],
}


def random_text(words=100):
    word_list = [
        "system", "security", "project", "account", "server",
        "database", "network", "employee", "customer", "access",
        "configuration", "application", "internal", "document"
    ]

    return " ".join(random.choice(word_list) for _ in range(words))


def random_csv():
    rows = [
        ["ID", "Name", "Department", "Status"],
    ]

    for i in range(random.randint(5, 20)):
        rows.append([
            i + 1,
            f"User_{random.randint(1000, 9999)}",
            random.choice(["IT", "Finance", "HR", "Security"]),
            random.choice(["Active", "Inactive", "Pending"])
        ])

    return "\n".join(",".join(map(str, row)) for row in rows)


def random_json():
    data = {
        "system_id": random.randint(10000, 99999),
        "environment": random.choice(["production", "development", "testing"]),
        "enabled": random.choice([True, False]),
        "settings": {
            "logging": True,
            "authentication": True,
            "max_connections": random.randint(10, 500)
        }
    }

    return json.dumps(data, indent=4)


def create_file(path):
    extension = path.suffix.lower()

    if extension == ".csv":
        content = random_csv()
    elif extension == ".json":
        content = random_json()
    else:
        content = random_text(random.randint(50, 200))

    path.write_text(content)


def main():
    # Set default target path
    default_path = Path.home() / "Documents"

    # Prompt user for export path
    target_input = input(f"Enter target export path [{default_path}]: ").strip()

    if target_input:
        # Expand ~ to home directory and resolve relative paths
        documents = Path(target_input).expanduser().resolve()
    else:
        documents = default_path

    documents.mkdir(parents=True, exist_ok=True)

    # Create random subdirectories
    directories = [
        "Finance",
        "HR",
        "Projects",
        "Security",
        "Backups",
        "Reports",
        "Internal",
    ]

    for directory in directories:
        (documents / directory).mkdir(exist_ok=True)

    # Create files
    for directory in directories:
        folder = documents / directory

        for _ in range(random.randint(5, 15)):
            extension = random.choice(list(file_types.keys()))
            name = random.choice(file_types[extension])

            random_number = random.randint(100, 9999)

            filename = f"{name.replace(' ', '_')}_{random_number}{extension}"
            filepath = folder / filename

            create_file(filepath)

    print(f"Created mock documents in: {documents}")


if __name__ == "__main__":
    main()