import asyncio
from math import ceil
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Dict, List, Optional

from CakeMusic import bot


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_plugins(
    page_n: int, plugin_dict: Dict[str, object], prefix: str, chat: Optional[Union[str, int]] = None
) -> InlineKeyboardMarkup:
    """
    Paginate plugins into a grid of InlineKeyboardButtons.
    Args:
        page_n (int): Current page number.
        plugin_dict (dict): Dictionary containing plugins with '__NAME__' attribute.
        prefix (str): Prefix used in callback data.
        chat (Optional[Union[str, int]]): Optional chat ID for callback data.

    Returns:
        InlineKeyboardMarkup: Paginated InlineKeyboardMarkup object.
    """
    # Generate plugin buttons
    plugins = sorted(
        [
            EqInlineKeyboardButton(
                plugin.__NAME__,
                callback_data=f"{prefix}_plugin({chat},{plugin.__NAME__.lower()})"
                if chat
                else f"{prefix}_plugin({plugin.__NAME__.lower()})",
            )
            for plugin in plugin_dict.values()
        ]
    )

    # Group plugins into rows of 3 buttons
    pairs = [plugins[i : i + 3] for i in range(0, len(plugins), 3)]

    # Calculate pagination
    COLUMN_SIZE = 3
    total_pages = ceil(len(pairs) / COLUMN_SIZE)
    current_page = page_n % total_pages

    # Slice for the current page
    page_pairs = pairs[current_page * COLUMN_SIZE : (current_page + 1) * COLUMN_SIZE]

    # Add navigation buttons if there are multiple pages
    if len(pairs) > COLUMN_SIZE:
        page_pairs.append(
            [
                EqInlineKeyboardButton(
                    "❮", callback_data=f"{prefix}_prev({current_page})"
                ),
                EqInlineKeyboardButton(
                    "✯ Owner ✯", url=f"tg://openmessage?user_id={bot.me.id}"
                ),
                EqInlineKeyboardButton(
                    "❯", callback_data=f"{prefix}_next({current_page})"
                ),
            ]
        )

    return InlineKeyboardMarkup(page_pairs)
