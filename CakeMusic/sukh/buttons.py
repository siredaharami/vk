from pyrogram.types import InlineKeyboardButton

def paginate_plugins(page_n, plugin_dict, prefix, chat=None):
    from math import ceil
    
    # Create the inline keyboard buttons
    if not chat:
        plugins = sorted(
            [
                InlineKeyboardButton(
                    x.__NAME__,
                    callback_data="{}_plugin({})".format(prefix, x.__NAME__.lower())
                )
                for x in plugin_dict.values()
            ]
        )
    else:
        plugins = sorted(
            [
                InlineKeyboardButton(
                    x.__NAME__,
                    callback_data="{}_plugin({},{})".format(prefix, chat, x.__NAME__.lower())
                )
                for x in plugin_dict.values()
            ]
        )

    # Pagination
    COLUMN_SIZE = 3
    max_num_pages = ceil(len(plugins) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages
    pairs = list(zip(plugins[::COLUMN_SIZE], plugins[1::COLUMN_SIZE], plugins[2::COLUMN_SIZE]))
    if len(plugins) % COLUMN_SIZE != 0:
        pairs.append((plugins[-1],))
    pairs = pairs[modulo_page * COLUMN_SIZE: (modulo_page + 1) * COLUMN_SIZE]
    
    # Navigation Buttons
    return pairs + [
        (
            InlineKeyboardButton("❮", callback_data="{}_prev({})".format(prefix, modulo_page)),
            InlineKeyboardButton(" Oᴡɴᴇʀ ", url="tg://openmessage?user_id={}".format(app.me.id)),
            InlineKeyboardButton("❯", callback_data="{}_next({})".format(prefix, modulo_page))
        )
    ]
