# Google Tasks MCP plugin

Connect Google Tasks to a ChatGPT Project through a private MCP server. List tasks,
create tasks and subtasks, edit titles, notes and dates, and complete or reopen tasks.
Google Tasks stays the source of truth; changes are read during conversations.
This server does not perform background synchronization or update Project memory.

## Setup

Run these commands from the repository root using Python 3.10 or later:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
mkdir -m 700 -p .secrets
```

The lock file contains the versions used for local verification. Recreate the
virtual environment after moving or cloning the repository.

### Authorize Google Tasks

1. Create or select a project in Google Cloud Console.
2. Enable the Google Tasks API and configure the OAuth consent screen.
3. Create an OAuth client with application type **Desktop app**. If the app is in
   testing mode, add your Google account as a test user.
4. Download the OAuth client JSON to `.secrets/client_secret.json`.
5. Run the command below and sign in to the intended Google account.

```sh
.venv/bin/python server.py --authorize
```

The server requests Google Tasks read/write access. Tokens are saved locally in
`.secrets/token.json`. If authorization expires, run the command again.
Never commit credentials or paste them into chats.

See [Google’s setup guide](https://developers.google.com/workspace/tasks/quickstart/python).

### Connect to ChatGPT

For ChatGPT web, connect this private stdio server through an
[OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels).
Tunnel access requires the appropriate Platform and ChatGPT workspace permissions
and a runtime API key. The MCP server itself does not use an OpenAI API key.

The server command, when run from the repository root, is:

```sh
.venv/bin/python server.py
```

Configure the launcher’s working directory to the repository root. If it requires
absolute paths, resolve them locally rather than storing machine-specific paths
in this repository:

```sh
# Executable for the local launcher:
printf '%s/.venv/bin/python\n' "$PWD"
# Script argument for the local launcher:
printf '%s/server.py\n' "$PWD"
```

Follow the tunnel setup guide, then in ChatGPT Plugins add a custom MCP server,
choose **Tunnel**, and create and install the private plugin. Keep the tunnel
client running. The local stdio server has no additional authentication layer;
restrict the tunnel and plugin to your own account. Do not publicly expose or
share this single-user connection.

Where supported, local ChatGPT Work or Codex can instead launch the server using
STDIO through Settings → MCP servers. Use the Python executable and script as
separate fields and set the working directory, or resolve their absolute paths
locally as above. Local MCP configuration does not install a ChatGPT web plugin.
See [MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

### Use it in a Project

Open a conversation in your ChatGPT Project and select the installed plugin where
available. Adapt [PROJECT-INSTRUCTIONS.md](PROJECT-INSTRUCTIONS.md) into your
Project instructions. Start with “List my Google Tasks task lists” to verify the
connection before requesting changes.

For private preferences or local paths, keep a local `PRIVATE-INSTRUCTIONS.md`;
this filename is ignored by Git. Account and workspace settings determine which
connection options are available.

## Tools

| Tool | Purpose |
| --- | --- |
| `list_task_lists` | Read task lists, following pagination tokens. |
| `list_tasks` | Read tasks, optionally including completed and hidden tasks. |
| `get_task` | Read a task by its ID. |
| `create_task` | Create a task with optional notes, date and parent task. |
| `update_task` | Edit fields, clear notes or a date, complete or reopen a task. |

Google Tasks API dates contain calendar dates, not reminder times. Recurrence,
timed reminders, deletion and bulk replacement are not implemented. Your computer
and tunnel must be running for the local tunnel connection to work. If a creation
request has an uncertain outcome, check existing tasks before retrying.

## Verification

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Local tests cover MCP tool discovery, pagination arguments, partial edits, date
handling and validation. Real Google access and ChatGPT connectivity require your
own authorization and installation; local tests do not establish end-to-end access.

## Repository hygiene

Commit source, tests, dependency files and public documentation. `.gitignore`
excludes `.venv/`, `.secrets/`, Python caches, local macOS metadata and
`PRIVATE-INSTRUCTIONS.md`. Ignoring a file does not untrack a previously committed
file; check `git status` before committing.

To disconnect, remove the ChatGPT connection and tunnel, revoke the application's
access in your Google account, and remove local credentials when no longer needed.
