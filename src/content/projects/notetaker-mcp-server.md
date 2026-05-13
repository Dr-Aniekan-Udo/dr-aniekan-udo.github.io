---
title: "Notetaker Mcp Server"
repo: "Dr-Aniekan-Udo/Notetaker-MCP-Server"
category: "MLOps & Tools"
description: "MCP server with tools for manipulating notes and support for Claude desktop"
excerpt: "- This workflow is built for Claude using MCP server module"
thumbnail: "/default-thumbnail.svg"
githubUrl: "https://github.com/Dr-Aniekan-Udo/Notetaker-MCP-Server"
stars: 2
language: "Python"
featured: false
priority: 7
tags: []
---

# Notetaker Mcp Server

## Claude agent tool with MCP

- This workflow is built for Claude using [MCP server module](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file)
- The server connects to claude desktop and helps you to handle your notes seemlessly.
- A notebook.txt is authomatically added to your folder to store notes, when you run the project

### Available Components:
| **Components**  |**Type** |**Description** |
|-----------------|---------|-----------------|
|**add_note** | Tools | Add notes contents to your notebook. Content could be generated from claude|
|**read_all_notes** | Tools | Reads all the from your your notebook|
|**read_latest_notes** | Tools | Reads the latest note added to your notebook|
|**read_indexed_notes** | Tools | Reads the note at the specified index to your notebook|
|**note_summary_prompt** | Prompt | Prompt the LLM to return your the summary of your note|
|**search_note_prompt** | Prompt | Prompt the LLm to search your note for information and returns the content and index of the note with the information|

### How to setup
- Install [``uv``](https://docs.astral.sh/uv/) for project management and package installation
- Install [``Claude Desktop``](https://claude.ai/download)
- Clone the repository
   ```bash
   git clone https://github.com/Dr-Aniekan-Udo/Notetaker-MCP-Server.git
   ```
- Enter the project folder
   ```bash
   cd Notetaker-MCP-Server
   ```
- Install dependencies
    ```bash
   uv sync
   ```
- Install the project to claude desktop
    ```bash
   uv run mcp install main.py
   ```
- Open Claude and have fun

- If MCP is connected:
 -> You should see tools in claude chat
 -> You should see attachment to use the resources and prompt (choose from integration)
- Check claude configuration:
<p>Go to <strong>files</strong> in claude, click <strong>setting</strong>, go to developer section click on <strong>edit configuration</strong>, open the json file with code and editor and ensure it's similar to the code below </p>

```
{
  "mcpServers": {
    "Demo": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\Users\\username\\"file path to project folder"\\main.py"
      ]
    }
  }
}
```
- Try this out in Claude:
 -> "Write a three line poem on Agriculture and add it to my note"
