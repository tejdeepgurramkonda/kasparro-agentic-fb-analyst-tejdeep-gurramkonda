import os
import sys

# Map of OLD message start to NEW message
# Git passes the file containing the old commit message.
# We read it to identify which commit we are on, then replace content.

message_map = {
    "feat: Implement foundation (config, logging, llm_client, data) (AI-Assisted)": "Implement foundation (config, logging, llm_client, data)",
    "All schemas, agents, and prompt templates are implemented (AI-Assisted)": "All schemas, agents, and prompt templates are implemented",
    "feat: Implement Orchestrator and CLI (AI-Assisted)": "Implement Orchestrator and CLI"
}

file_path = sys.argv[1]

with open(file_path, 'r') as f:
    content = f.read().strip()

# Find matching new message
new_message = None
for old_start, msg in message_map.items():
    if content.startswith(old_start):
        new_message = msg
        break

if new_message:
    with open(file_path, 'w') as f:
        f.write(new_message)
