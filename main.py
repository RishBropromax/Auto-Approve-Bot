from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
import random, asyncio
from configs import cfg
    
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

ABOUT = """ 
βοΈ**About This Bot**βοΈ

π Commands : [Click Here](https://telegra.ph/Auto-Join-Reqvest-Accpet-Bot-Commads-12-24)
πBot created by @EmoBotDevolopers
π¦Source Code : [Click Here](https://github.com/RishBropromax/Auto-Approve-Bot)
βοΈFramework : [Pyrogram](docs.pyrogram.org)
π°Language : [Python](www.python.org)
π§βπ»Developer : @ImRishmika
πSupport : [Emo Bot Support](https://t.me/EmoBotSupport)

"""


gif = [
    'https://telegra.ph/file/c4ea3761bb73bab726334.jpg',
    'https://telegra.ph/file/c4ea3761bb73bab726334.jpg',
    'https://telegra.ph/file/c4ea3761bb73bab726334.jpg',
    'https://telegra.ph/file/c4ea3761bb73bab726334.jpg',
    'https://telegra.ph/file/c4ea3761bb73bab726334.jpg',
    'https://telegra.ph/file/d340fbf28f412487c5750.jpg',
    'https://telegra.ph/file/d340fbf28f412487c5750.jpg',
    'https://telegra.ph/file/d5becc3a7c18f619bcd22.png',
    'https://telegra.ph/file/d5becc3a7c18f619bcd22.png',
    'https://telegra.ph/file/d5becc3a7c18f619bcd22.png',
    'https://telegra.ph/file/d5becc3a7c18f619bcd22.png'
]


#βββββββββββββββββββββββββββββββββββββββββββββββ Main process βββββββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(kk.id,img, "**Hello {}!\nWelcome To {}\n I m Auto Approve Bot.**\n β‘οΈPowerd By @EmoBotDevolopers ".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    
 
#βββββββββββββββββββββββββββββββββββββββββββββββ About βββββββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_message(filters.command("about"))
async def help(bot, message):
  await message.reply_photo("https://telegra.ph/file/c4ea3761bb73bab726334.jpg",caption=ABOUT,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="</> ΡΠΌΟ Π²ΟΡ βΡΞ½ΟβΟΟΡΚΡ", url="t.me/EmoBotDevolopers")]]))

#βββββββββββββββββββββββββββββββββββββββββββββββ Start βββββββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_message(filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("π― Channel", url="https://t.me/EmoBotDevolopers"),
                        InlineKeyboardButton("π¬ Support", url="https://t.me/EmoBotSupport")
                    ],
                    [
                        InlineKeyboardButton("π§© Repo π§©", url="https://github.com/RishBropromax/Auto-Approve-Bot"),
                        InlineKeyboardButton("π» Devolopers π»", url="https://t.me/ImRishmika")
                    ],
                    [
                        InlineKeyboardButton("β Add me to your Chat β", url="https://t.me/emApprove_Bot?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://telegra.ph/file/d5becc3a7c18f619bcd22.png", caption="**π¦ Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n π° Powerd By [Emo Bot Devolopers](t.me/EmoBotSupport)**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    
        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("πββοΈ Start me private πββοΈ", url="https://t.me/emApprove_Bot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**π¦ Hello {}!\n Write me private for more details**".format(m.from_user.first_name), reply_markup=keyboar)
        print(m.from_user.first_name +" Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("π Check Again π", "chk")
                ]
            ]
        )
        await m.reply_text("**β οΈAccess Denied!β οΈ\n\nPlease Join @{} to use me.If you joined click check again button to confirm.** \n\n".format(cfg.FSUB), reply_markup=key)

#βββββββββββββββββββββββββββββββββββββββββββββββ callback βββββββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("π― Channel", url="https://t.me/EmoBotDevolopers"),
                        InlineKeyboardButton("π¬ Support", url="https://t.me/EmoBotSupport")
                    ],
                    [
                        InlineKeyboardButton("π§© Repo π§©", url="https://github.com/RishBropromax/Auto-Approve-Bot"),
                        InlineKeyboardButton("π» Devolopers π»", url="https://t.me/ImRishmika")
                    ],
                    [
                        InlineKeyboardButton("β Add me to your Chat β", url="https://t.me/emApprove_Bot?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**π¦ Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n π° Powerd By [Emo Bot Devolopers](t.me/EmoBotDevolopers)**".format(cb.from_user.mention, "https://t.me/EmoBotDevolopers"), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("πββοΈ You are not joined to channel join and try again. πββοΈ")

#βββββββββββββββββββββββββββββββββββββββββββββββ info βββββββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
π Chats Stats π
πββοΈ Users : `{xx}`
π₯ Groups : `{x}`
π§ Total users & groups : `{tot}` """)

#βββββββββββββββββββββββββββββββββββββββββββββββ Broadcast βββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`β‘οΈ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"βSuccessfull to `{success}` users.\nβ Faild to `{failed}` users.\nπΎ Found `{blocked}` Blocked users \nπ» Found `{deactivated}` Deactivated users. \n\n β οΈ Warning :- Don't Boardcast Everyday ")

#βββββββββββββββββββββββββββββββββββββββββββββββ Broadcast Forward βββββββββββββββββββββββββββββββββββββββββββββββ

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`β‘οΈ Fcast Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"βSuccessfull to `{success}` users.\nβ Faild to `{failed}` users.\nπΎ Found `{blocked}` Blocked users \nπ» Found `{deactivated}` Deactivated users.")

print("Starting..")
print("Checking Code Erorrs..!")
print("Bot Running..")
app.run()
