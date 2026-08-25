
# Chat App MCP Server
> **Purpose** – This repository hosts the **Model Context Protocol (MCP) server** for my real‑time chat application.  
It bridges AI agents (e.g., Claude Desktop) to the chat backend, letting them authenticate, fetch contacts/chats, read message history, and send messages—all in real‑time.

### 📚 Main Chat‑App Repository
**https://github.com/Prajjwal2507/chat-app-pegion**

## 📦 How to Configure Claude Desktop

> **TL;DR** – Add the JSON snippet below to your Claude Desktop configuration and restart the app.

### 1️⃣ Open the Config File

1. Open **Claude Desktop**.
2. Click the **hamburger menu (☰)** in the top‑left corner → **Settings**.
3. In the left sidebar, click **"Developer"** (under *Desktop app*).
4. Click the **"Edit Config"** button — this opens your `claude_desktop_config.json` file in your default code editor.

### 2️⃣ Paste the MCP Server Entry

Add (or replace) the `"chat-app"` object inside the `"mcpServers"` dictionary:

```json
{
  "mcpServers": {
    "chat-app": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://chat-app-mcp-server.onrender.com/sse"
      ]
    }
  }
}
```

> **Note:** If the file already contains other servers, just add the new `"chat-app"` block alongside them — keep the surrounding braces and commas correct.

### 3️⃣ Kill & Restart Claude Desktop

You **must** fully quit Claude (not just close the window) so it reloads the config.

**Windows (PowerShell):**
```powershell
Stop-Process -Name "Claude" -Force
```

**Windows (CMD):**
```cmd
taskkill /IM Claude.exe /F
```

**macOS (Terminal):**
```bash
pkill -x "Claude"
```

Then relaunch Claude Desktop from the Start menu / Applications folder.

### 4️⃣ Verify & Use

The plug icon will now show the available tools. Try these example prompts:
- *"Claude, **log in** to my chat app with email `john@example.com` and password `••••`."*
- *"Claude, **list my contacts**."*
- *"Claude, **send** a message to Keshav saying 'Hey, how are you?'"*

---

## 🛠️ Skills & Technologies Demonstrated

| Category | Tools / Libraries |
|----------|-------------------|
| **MCP Framework** | **FastMCP**, **HTTPX**, **Python 3.12** |
| **Real‑time Sync** | **Socket.io** (WebSocket broadcasting) |
| **Deployment** | **Render** (public HTTPS endpoint) + **UptimeRobot** (keep‑alive ping) |
| **Security** | **Arcjet** (rate‑limiting & bot protection) |
| **Frontend** | **Vite + React**, **Zustand**, **React‑Hot‑Toast** |
| **Version Control** | **Git**, **GitHub** |
| **Testing / CI** | **UptimeRobot** (prevent Render cold‑starts) |

### 🌐 Live Demo UI
**https://new-chat-app-inky.vercel.app/**

### 📚 Main Chat‑App Repository
**https://github.com/Prajjwal2507/chat-app-pegion**
