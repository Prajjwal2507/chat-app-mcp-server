from __future__ import annotations

from typing import Any, Optional
import os

import httpx
from fastmcp import FastMCP

API_BASE_URL = "https://new-chat-app-nx7q.onrender.com"

mcp = FastMCP("chat-app")
http_client = httpx.Client(
    base_url=API_BASE_URL,
    timeout=30.0,
    follow_redirects=True,
)


def _handle_response(response: httpx.Response) -> Any:
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if response.is_error:
        message = payload.get("message") or payload.get("error") or response.text
        raise RuntimeError(f"API request failed ({response.status_code}): {message}")

    return payload


@mcp.tool()
def auth_signup(full_name: str, email: str, password: str) -> dict[str, Any]:
    """Register a new user account with the chat backend."""
    response = http_client.post(
        "/api/auth/signup",
        json={"fullName": full_name, "email": email, "password": password},
    )
    return _handle_response(response)


@mcp.tool()
def auth_login(email: str, password: str) -> dict[str, Any]:
    """Log in to the chat backend and persist the JWT cookie for later calls."""
    response = http_client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return _handle_response(response)


@mcp.tool()
def auth_logout() -> dict[str, Any]:
    """Log out the current user by clearing the auth cookie."""
    response = http_client.post("/api/auth/logout")
    return _handle_response(response)


@mcp.tool()
def auth_check_session() -> dict[str, Any]:
    """Check whether the current session is valid and return the authenticated user."""
    response = http_client.get("/api/auth/check")
    return _handle_response(response)


@mcp.tool()
def auth_update_profile(profile_pic: str) -> dict[str, Any]:
    """Upload a new profile picture for the authenticated user."""
    response = http_client.put(
        "/api/auth/update-profile",
        json={"profilePic": profile_pic},
    )
    return _handle_response(response)


@mcp.tool()
def messages_get_contacts() -> list[dict[str, Any]]:
    """Fetch all users except the currently authenticated user."""
    response = http_client.get("/api/messages/contacts")
    return _handle_response(response)


@mcp.tool()
def messages_get_chats() -> list[dict[str, Any]]:
    """Fetch the list of chat partners for the authenticated user."""
    response = http_client.get("/api/messages/chats")
    return _handle_response(response)


@mcp.tool()
def messages_get_by_user(user_id: str) -> list[dict[str, Any]]:
    """Fetch conversation history between the authenticated user and the provided user ID."""
    response = http_client.get(f"/api/messages/{user_id}")
    return _handle_response(response)


@mcp.tool()
def messages_send(
    receiver_id: str,
    text: Optional[str] = None,
    image: Optional[str] = None,
) -> dict[str, Any]:
    """Send a message and immediately return the latest conversation state for the user pair."""
    payload: dict[str, Any] = {}
    if text is not None:
        payload["text"] = text
    if image is not None:
        payload["image"] = image

    if not payload:
        raise ValueError("At least one of 'text' or 'image' must be provided.")

    send_response = http_client.post(f"/api/messages/send/{receiver_id}", json=payload)
    sent_message = _handle_response(send_response)

    latest_messages = http_client.get(f"/api/messages/{receiver_id}")
    conversation = _handle_response(latest_messages)

    return {
        "sent_message": sent_message,
        "conversation": conversation,
        "message_count": len(conversation) if isinstance(conversation, list) else 0,
    }


if __name__ == "__main__":
    # Get port from environment variables (important for platforms like Render/Railway)
    port = int(os.environ.get("PORT", 8000))
    # Run the server with SSE transport instead of stdio
    mcp.run(transport="sse", host="0.0.0.0", port=port)
