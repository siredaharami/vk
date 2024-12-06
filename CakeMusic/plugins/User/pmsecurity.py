import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from CakeMusic import app, cdx, eor, vars
from CakeMusic.database.pmguard import *

# Path to the image for PM Security messages
PM_SECURITY_IMAGE = "https://files.catbox.moe/xwygzj.jpg"  # Update with the correct path

@app.on_message(cdx(["pm", "pmpermit", "pmguard"]) & filters.me)
async def pm_on_off(client, message):
    if len(message.command) < 2:
        return await eor(
            message,
            "Hey, What You Want To Do ?\n\nExample: `.pm on` | `.pm off`"
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


@app.on_message(cdx(["a", "approve"]) & filters.private & filters.me)
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


@app.on_message(cdx(["disallow", "disapprove"]) & filters.private & filters.me)
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


@app.on_message(cdx(["block"]) & filters.me)
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


@app.on_message(cdx(["unblock"]) & filters.me)
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
