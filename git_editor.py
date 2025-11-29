import os
import sys

# Map of commit hash (short) to new message
# Note: In rebase -i, we only see the short hash.
# We need to be careful to match the correct lines.
commits_to_edit = {
    "4e32381": "Implement foundation (config, logging, llm_client, data)",
    "b836b7b": "All schemas, agents, and prompt templates are implemented",
    "1c82aaa": "Implement Orchestrator and CLI"
}

file_path = sys.argv[1]

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split()
    if len(parts) > 1 and parts[0] == 'pick':
        commit_hash = parts[1]
        # Check if this commit is one we want to edit
        # We check if the hash starts with our target hash (handling potential length diffs)
        matched = False
        for target_hash in commits_to_edit.keys():
            if commit_hash.startswith(target_hash) or target_hash.startswith(commit_hash):
                new_lines.append(line.replace('pick', 'reword', 1))
                matched = True
                break
        if not matched:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)
