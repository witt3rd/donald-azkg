#!/usr/bin/env env python3
"""Telegram Channel Reader - List channels and read messages by date.

This script uses Telethon to access your Telegram account and:
1. List all channels you have access to
2. Read one message from a specific channel since a given date/time

Requires:
- Telegram API credentials (api_id, api_hash) from https://my.telegram.org/auth
- Environment variables set in .env file
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from loguru import logger
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Channel, User

# Load environment variables
load_dotenv()


def get_credentials() -> tuple[int, str]:
    """Get Telegram API credentials from environment variables.

    Returns
    -------
    tuple[int, str]
        API ID and API hash.

    Raises
    ------
    ValueError
        If required environment variables are not set.
    """
    api_id_str = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id_str or not api_hash:
        raise ValueError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env file.\n"
            "Get these from https://my.telegram.org/auth"
        )

    try:
        api_id = int(api_id_str)
    except ValueError as e:
        raise ValueError(f"TELEGRAM_API_ID must be a number: {api_id_str}") from e

    return api_id, api_hash


async def list_channels(client: TelegramClient) -> list[dict[str, str | int]]:
    """List all channels accessible to the authenticated user.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.

    Returns
    -------
    list[dict[str, str | int]]
        List of channel information dictionaries with keys:
        - id: Channel ID
        - title: Channel name
        - username: Channel username (if available)
    """
    channels = []

    logger.info("Fetching your channels...")

    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Channel):
            channel_info = {
                "id": dialog.id,
                "title": dialog.title,
                "username": dialog.entity.username if dialog.entity.username else None,
            }
            channels.append(channel_info)
            logger.debug(f"Found channel: {channel_info}")

    logger.info(f"Found {len(channels)} channels")
    return channels


async def list_all_dialogs(client: TelegramClient) -> list[dict[str, str | int]]:
    """List all dialogs (conversations) accessible to the authenticated user.

    Includes private chats, groups, channels, and Saved Messages.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.

    Returns
    -------
    list[dict[str, str | int]]
        List of dialog information dictionaries with keys:
        - id: Dialog ID
        - name: Dialog name
        - type: Dialog type (Saved Messages, Private Chat, Group, Channel)
        - username: Username if available
    """
    dialogs = []
    me = await client.get_me()

    logger.info("Fetching all your conversations...")

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # Determine dialog type
        if isinstance(entity, User):
            if entity.id == me.id:
                dialog_type = "Saved Messages"
            else:
                dialog_type = "Private Chat"
        elif isinstance(entity, Channel):
            if hasattr(entity, 'megagroup') and entity.megagroup:
                dialog_type = "Group"
            elif hasattr(entity, 'broadcast') and entity.broadcast:
                dialog_type = "Channel"
            else:
                dialog_type = "Chat"
        else:
            dialog_type = "Chat"

        dialog_info = {
            "id": dialog.id,
            "name": dialog.name,
            "type": dialog_type,
            "username": entity.username if hasattr(entity, 'username') and entity.username else None,
        }
        dialogs.append(dialog_info)
        logger.debug(f"Found {dialog_type}: {dialog_info}")

    logger.info(f"Found {len(dialogs)} conversations")
    return dialogs


async def get_message_since(
    client: TelegramClient,
    channel_identifier: str | int,
    since_date: datetime,
) -> Optional[dict[str, str | datetime]]:
    """Get first message from channel since specified date.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.
    channel_identifier : str | int
        Channel username (e.g., '@channelname') or channel ID.
    since_date : datetime
        Retrieve first message after this date/time.

    Returns
    -------
    Optional[dict[str, str | datetime]]
        Message information with keys:
        - id: Message ID
        - date: Message timestamp
        - text: Message content
        - sender: Sender name
        Returns None if no messages found.

    Raises
    ------
    ValueError
        If channel not found or not accessible.
    """
    logger.info(
        f"Searching for first message in {channel_identifier} since {since_date}"
    )

    try:
        async for message in client.iter_messages(
            channel_identifier,
            offset_date=since_date,
            limit=1,
            reverse=True,  # Get oldest first (closest to since_date)
        ):
            message_info = {
                "id": message.id,
                "date": message.date,
                "text": message.text or "(no text content)",
                "sender": message.sender_id,
            }
            logger.info(f"Found message ID {message.id} from {message.date}")
            return message_info

        logger.warning(f"No messages found since {since_date}")
        return None

    except ValueError as e:
        raise ValueError(
            f"Could not access channel '{channel_identifier}'. "
            "Check that the channel exists and you have access to it."
        ) from e


async def authenticate_client(
    client: TelegramClient, phone: Optional[str] = None
) -> None:
    """Authenticate Telegram client with user credentials.

    Parameters
    ----------
    client : TelegramClient
        Telegram client to authenticate.
    phone : Optional[str]
        Phone number for authentication. If not provided, will be prompted.

    Raises
    ------
    SessionPasswordNeededError
        If 2FA is enabled (will prompt for password).
    """
    # Define callbacks for interactive prompts
    def phone_callback():
        return click.prompt("Phone number (with country code, e.g., +1234567890)", type=str)

    def code_callback():
        return click.prompt("Verification code", type=str)

    def password_callback():
        return click.prompt("2FA password", type=str, hide_input=True)

    # Start with appropriate phone parameter
    await client.start(
        phone=phone or phone_callback,
        code_callback=code_callback,
        password=password_callback
    )

    logger.info("Authentication successful")


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
def cli(verbose: bool) -> None:
    """Telegram Channel Reader - Access your Telegram channels programmatically.

    Requires TELEGRAM_API_ID and TELEGRAM_API_HASH in .env file.
    Get credentials from https://my.telegram.org/auth
    """
    if verbose:
        logger.add(lambda msg: print(msg, end=""), level="DEBUG")
    else:
        logger.add(lambda msg: print(msg, end=""), level="INFO")


@cli.command()
@click.option("--phone", "-p", help="Phone number (optional, will prompt if needed)")
def list_my_channels(phone: Optional[str]) -> None:
    """List all channels you have access to."""

    async def _list() -> None:
        api_id, api_hash = get_credentials()
        client = TelegramClient("telegram_session", api_id, api_hash)

        try:
            await authenticate_client(client, phone)
            channels = await list_channels(client)

            if not channels:
                click.echo("No channels found.")
                return

            click.echo("\nYour channels:")
            click.echo("-" * 80)
            for channel in channels:
                username = f"@{channel['username']}" if channel["username"] else "(no username)"
                click.echo(f"  ID: {channel['id']:12} | {username:20} | {channel['title']}")
            click.echo("-" * 80)
            click.echo(f"\nTotal: {len(channels)} channels")

        finally:
            await client.disconnect()

    asyncio.run(_list())


@cli.command()
@click.option("--phone", "-p", help="Phone number (optional, will prompt if needed)")
def list_dialogs(phone: Optional[str]) -> None:
    """List all conversations (private chats, groups, channels, Saved Messages)."""

    async def _list() -> None:
        api_id, api_hash = get_credentials()
        client = TelegramClient("telegram_session", api_id, api_hash)

        try:
            await authenticate_client(client, phone)
            dialogs = await list_all_dialogs(client)

            if not dialogs:
                click.echo("No conversations found.")
                return

            click.echo("\nAll your conversations:")
            click.echo("-" * 100)
            click.echo(f"{'ID':<15} | {'Type':<15} | {'Username':<20} | {'Name'}")
            click.echo("-" * 100)
            for dialog in dialogs:
                username = f"@{dialog['username']}" if dialog["username"] else "(no username)"
                click.echo(f"{dialog['id']:<15} | {dialog['type']:<15} | {username:<20} | {dialog['name']}")
            click.echo("-" * 100)
            click.echo(f"\nTotal: {len(dialogs)} conversations")

        finally:
            await client.disconnect()

    asyncio.run(_list())


@cli.command()
@click.argument("channel")
@click.option(
    "--since",
    "-s",
    required=True,
    help="Date/time in ISO format (e.g., 2025-10-01 or 2025-10-01T14:30:00)",
)
@click.option("--phone", "-p", help="Phone number (optional, will prompt if needed)")
def read_message(channel: str, since: str, phone: Optional[str]) -> None:
    """Read first message from CHANNEL since specified date.

    CHANNEL can be:
    - Channel username with @ (e.g., @channelname)
    - Channel ID as number (e.g., -1001234567890)

    Examples:
        telegram_channel_reader.py read-message @mychannel --since 2025-10-01
        telegram_channel_reader.py read-message -1001234567890 --since "2025-10-01T14:30:00"
    """

    async def _read() -> None:
        # Parse date
        try:
            since_date = datetime.fromisoformat(since)
        except ValueError as e:
            raise click.BadParameter(
                f"Invalid date format: {since}. Use ISO format like 2025-10-01 or 2025-10-01T14:30:00"
            ) from e

        # Parse channel identifier
        channel_id: str | int = channel
        if channel.lstrip("-").isdigit():
            channel_id = int(channel)

        api_id, api_hash = get_credentials()
        client = TelegramClient("telegram_session", api_id, api_hash)

        try:
            await authenticate_client(client, phone)
            message = await get_message_since(client, channel_id, since_date)

            if not message:
                click.echo(f"\nNo messages found in {channel} since {since_date}")
                return

            click.echo(f"\nFirst message since {since_date}:")
            click.echo("-" * 80)
            click.echo(f"Message ID: {message['id']}")
            click.echo(f"Date: {message['date']}")
            click.echo(f"Sender: {message['sender']}")
            click.echo(f"\nContent:\n{message['text']}")
            click.echo("-" * 80)

        finally:
            await client.disconnect()

    asyncio.run(_read())


if __name__ == "__main__":
    cli()
