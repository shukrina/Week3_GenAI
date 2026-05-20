#!/bin/bash
extensions=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-toolsai.vscode-jupyter-powertoys "
    "charliermarsh.ruff"
    "ms-python.pylint"
    "george-alisson.html-preview-vscode"
    "ms-toolsai.jupyter"
    "foxundermoon.shell-format"
    "PKief.material-icon-theme"
    "aaron-bond.better-comments"
    "GitHub.vscode-github-actions"
    "GitHub.copilot"
    "GitHub.copilot-chat"
    "GitHub.vscode-pull-request-github"
)

for extension in "${extensions[@]}"; do
    code --install-extension "$extension"
done

###    # Let's add execute permissions for the file
###    chmod +x script.sh
###
###    # Now let's execute the script
###    ./install-extensions.sh