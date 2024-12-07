import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from CakeMusic import app, cdx, eor, vars
from CakeMusic.database.pmguard import *
from config import OWNER_ID

# Path to the image for PM Security messages
PM_SECURITY_IMAGE = "https://files.catbox.moe/xwygzj.jpg"  # Update with the correct path

@app.on_message(
    filters.command(["pm"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def pm_on_off(client, message):
    if len(message.command) < 2:
        return await eor(
            message,
            "Hey, What You Want To Do?\n\nExample: `.pm on` | `.pm off`"
        )
    aux = await eor(message, "Processing ...")
    query = message.text.split(None, 1)[1].lower()
    if query == "on":
        set_permit = await set_pm_permit(True)
        if set_permit:
            return await aux.edit("PM Permit Turned On!")
        return await aux.edit("PM Permit Already On!")
    elif query == "off":
        set_permit = await set_pm_permit(False)
        if set_permit:
            return await aux.edit("PM Permit Turned Off!")
        return await aux.edit("PM Permit Already Off!")


@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def pm_guard(client, message):
    """Handles incoming private messages when PM Guard is on."""
    is_pm_permit_on = await get_pm_permit()  # Check if PM Permit is enabled
    if not is_pm_permit_on:
        return  # PM Guard is turned off, do nothing

    user_id = message.from_user.id
    approved = await is_approved_user(user_id)  # Check if the user is approved

    if approved:
        return  # User is already approved, allow the message

    # Alert message for unapproved users
    warning_message = (
        "**🚨 Alert: PM Not Allowed 🚨**\n\n"
        "Hello! You are not approved to send me messages. "
        "Please wait for approval or stop messaging to avoid being blocked."
    )
    await message.reply(warning_message)

    # Optional: Store or increment warnings for the user (add your logic here)
    # For example, disconnect after 3 warnings:
    # if warnings >= 3:
    #     await client.block_user(user_id)

async def get_pm_permit():
    """Fetch the current PM Permit status."""
    # Replace with your database or config logic to fetch PM status
    return True  # Assuming it's enabled for now


@app.on_message(
    filters.command(["a"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def pm_approve(client, message):
    uid = message.chat.id
    permit = await add_approved_user(uid)
    if permit:
        await message.reply_photo(
            photo=PM_SECURITY_IMAGE,
            caption="User Approved for PM. 🚀"
        )
    else:
        await message.edit("This user is already approved.")
    await asyncio.sleep(2)
    return await message.delete()


@app.on_message(
    filters.command(["d"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def pm_disapprove(client, message):
    uid = message.chat.id
    permit = await del_approved_user(uid)
    if permit:
        await message.reply_photo(
            photo=PM_SECURITY_IMAGE,
            caption="User Disapproved for PM. ❌"
        )
    else:
        await message.edit("This user is not approved!")
    await asyncio.sleep(2)
    return await message.delete()


@app.on_message(
    filters.command(["block"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def block_user_func(client, message):
    user_id = message.chat.id if message.chat.type == ChatType.PRIVATE else (
        message.reply_to_message.from_user.id if message.reply_to_message else None
    )
    if not user_id:
        return await message.edit("Reply to a user message or use in private chat.")
    await client.block_user(user_id)
    await message.reply_photo(
        photo=PM_SECURITY_IMAGE,
        caption="User Blocked Successfully! 🚫"
    )


@app.on_message(
    filters.command(["unblock"], ".") & (filters.me | filters.user(OWNER_ID))
)
async def unblock_user_func(client, message):
    user_id = message.chat.id if message.chat.type == ChatType.PRIVATE else (
        message.reply_to_message.from_user.id if message.reply_to_message else None
    )
    if not user_id:
        return await message.edit("Reply to a user message or use in private chat.")
    await client.unblock_user(user_id)
    await message.reply_photo(
        photo=PM_SECURITY_IMAGE,
        caption="User Unblocked Successfully! ✅"
    )
    
