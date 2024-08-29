from aiogram import F, Router
from aiogram.types import Message 
from aiogram.filters import CommandStart, Command

import bot.keyboards as kb
import bot.database.requests as rq

import os
import dotenv

dotenv.load_dotenv()


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    
    user = await rq.get_user_by_tg_id(user_id)
    if not user:
        start_command = message.text
        referrer_id = start_command[7:]
        if referrer_id.isdigit() and int(referrer_id) != user_id:
            referrer_id = int(referrer_id)
            await rq.set_user(user_id, name, username, referrer_id)
            await rq.add_referral(referrer_id, user_id)

            user = await rq.get_user_by_tg_id(user_id)
            if user.referrer == 0:
                await rq.update_user_score(user_id, user.score + 5000)

                referrer = await rq.get_user_by_tg_id(referrer_id)
                await rq.update_user_score(referrer_id, referrer.score + 10000)

                try:
                    await message.bot.send_message(referrer_id, "*Похоже у вас новый друг!*", parse_mode="Markdown")
                    await message.answer(
                        f"*Приветственный бонус от {referrer.name} в размере 5000!*", 
                        parse_mode="Markdown"
                    )
                except:
                    pass
            else:
                await message.answer("Вы уже являетесь рефералом другого пользователя и не можете получить награду повторно.")
        else:
            await message.answer("Нельзя быть другом самому себе!" if str(referrer_id) == str(user_id) else "Неверный реферальный ID!")
            await rq.set_user(user_id, name, username, 0)

    await message.answer_sticker('CAACAgIAAxkBAAEMuE1mzezgwwZj8_RbzXAkhhAMBntz_QACKwwAAiIwWEvIROJY0qdhFDUE')
    await message.answer("*Начни майнить $NCOIN прямо сейчас!*", parse_mode="Markdown", reply_markup=kb.game)


@router.message(Command("admin"))
async def admin_cmd(message: Message) -> None:
    if message.from_user.id == os.getenv("ADMIN_ID"):
        await message.answer(
            f"*Hello, {message.from_user.first_name}, select an option.*",
            parse_mode="Markdown",
            reply_markup=kb.admin
        )


@router.message(Command("referral_link"))
async def referral_cmd(message: Message) -> None:
    link = f"http://t.me/ncrypto_tap_bot?start={message.from_user.id}"
    await message.answer(f"*Your ref-link: {link}*", parse_mode="Markdown")


@router.message(Command("info"))
async def info_cmd(message: Message) -> None:
    user = await rq.get_user_by_tg_id(message.from_user.id)

    referrals = []
    for ref_id in user.referrals:
        if ref_id is not None:
            referral = await rq.get_user_by_tg_id(ref_id)
            referrals.append(str(referral.name))

    user_data = f"Id: {user.tg_id}\nName: {user.name}\nUsername: {user.username}\nScore: {user.score}\nReferrals: {', '.join(map(str, referrals))}\nYou are a referral: {user.referrer}"

    await message.answer(f"*{user_data}*", parse_mode="Markdown")
