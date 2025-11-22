def export_results(results, log_file_path):
    import json
    import os

    # Ensure the log directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Export results to a JSON file
    with open(log_file_path, 'w') as log_file:
        json.dump(results, log_file, indent=4)

def export_logs(logs, log_file_path):
    # Ensure the log directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Export logs to a text file
    with open(log_file_path, 'w') as log_file:
        for log in logs:
            log_file.write(f"{log}\n")