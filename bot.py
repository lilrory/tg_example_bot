import asyncio
import logging

from random2 import randint
from aiogram import Bot, Dispatcher, types, F
from aiogram import html
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.utils.markdown import hide_link
from config_reader import config


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher()


#
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    link1 = '<a href="https://mastergroosha.github.io/aiogram-3-guide/">книге</a>'
    link2 = '<a href="https://github.com/MasterGroosha">Groosha</a>'
    await message.answer(
        f'Привет! Бот написан в качестве примера по {link1} от {link2}.\n'
        'В разработке использовался aiogram 3.0.0b7.\n'
        'Ниже представлены команды:\n'
        '/my_links\n'
        '/start\n'
        '/test\n'
        '/test1\n'
        '/test2\n'
        '/answer\n'
        '/reply\n'
        '/dice\n'
        '/darts\n'
        '/name\n'
        '/images\n'
        '/hidden_link\n'
        '/button\n'
        '/reply_builder\n'
        '/special_buttons\n'
        '/random\n'
    )



@dp.message(Command('test1'))
async def cmd_test1(message: types.Message):
    await message.reply('test 1')


async def cmd_test2(message: types.Message):
    await message.reply('test2')


@dp.message(Command('answer'))
async def cmd_answer(message: types.Message):
    await message.answer('это просто ответ')


@dp.message(Command('reply'))
async def cmd_reply(message: types.Message):
    await message.reply('это ответ с "ответом"')


@dp.message(Command('dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji='🎲')
    
    
@dp.message(Command('darts'))
async def cmd_darts(message: types.Message):
    await message.answer_dice(emoji='🎯')


@dp.message(Command('test'))
async def any_message(message: types.Message):
    await message.answer('Hello, <b>world</b>!', parse_mode='HTML')
    await message.answer('Hello, *world*\!', parse_mode=None)


@dp.message(Command('name'))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}")
    else:
        await message.answer('Укажите имя после комадны /name')


@dp.message(Command('images'))
async def upload_photo(message: types.Message):
    file_ids = []
    with open('images/buffer_emulatore.jpg', 'rb') as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
            image_from_buffer.read(),
            filename='image from buffer.jpg'
            ),
            caption='Изображение из буфера'
        )
        file_ids.append(result.photo[-1].file_id)

    image_from_url = URLInputFile('https://picsum.photos/seed/picsum/400/300')
    result = await message.answer_photo(
        image_from_url,
        caption='Изображение по ссылке'
    )
    file_ids.append(result.photo[-1].file_id)

    image_from_pc = FSInputFile('images/image_from_pc.jpg')
    reslut = await message.answer_photo(
        image_from_pc,
        caption='Изображение от компьютера'
    )
    file_ids.append(reslut.photo[-1].file_id)


@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f'/tmp/{message.photo[-1].file_id}.jpg'
    )


@dp.message(F.sticker)
async def download_sticker(message: types.Message, bot: Bot):
    await bot.download(
        message.sticker,
        destination=f'/tmp/{message.sticker.file_id}.webp'
    )


@dp.message(Command('hidden_link'))
async def cmd_hidden_link(message: types.Message):
    await message.answer(
        f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
        f"Документация Telegram: *существует*\n"
        f"Пользователи: *не читают документацию*\n"
        f"Груша:"
    )

#обычные кнопки
@dp.message(Command('button'))
async def cmd_button(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='С пюре'),
            types.KeyboardButton(text='Без пюре')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите способ подачи'
    )
    await message.answer('Как подать котлеты?', reply_markup=keyboard)


@dp.message(F.text.lower() == 'с пюре')
async def with_puree(message: types.Message):
    await message.reply('Отличный выбор!', reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == 'без пюре')
async def without_puree(message: types.Message):
    await message.reply('Так невкусно!', reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command('reply_builder'))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        'Выбери число:',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

#специальные кнопки
@dp.message(Command('special_buttons'))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Запросить геолокацию', request_location=True),
        types.KeyboardButton(text='Запросить контакт', request_contact=True)
    )

    builder.row(types.KeyboardButton(
        text='Создать викторину',
        request_poll=types.KeyboardButtonPollType(type='quiz')
        )
    )

    builder.row(types.KeyboardButton(
        text='Выбрать премиум пользователя',
        request_user=types.KeyboardButtonRequestUser(
        request_id=1,
        user_is_premium=True
            )
        ),
        types.KeyboardButton(
        text='Выбрать супергруппы с форумами',
        request_chat=types.KeyboardButtonRequestChat(
        request_id=2,
        chat_is_channel=False,
        chat_is_forum=True
            )
        )
    )
    await message.answer(
        'Выберите действие:',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )


@dp.message(F.chat_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )


@dp.message(Command('my_links'))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='Мой GitHub',
        url='https://github.com//lilrory')
    )
    user_id = 5946765150
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text='Dev',
            url=f'tg://user?id={user_id}')
        )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


@dp.message(Command('random'))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Нажми на меня',
        callback_data='random_value'
    ))
    await message.answer(
        'Нажмите на кнопку, чтобы бот отправил число от 1 до 10',
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == 'random_value')
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        'Спасибо, что воспользовались ботом',
        show_alert=True
    )


async def main():
    await dp.start_polling(bot)

dp.message.register(cmd_test2, Command('test2'))


if __name__=="__main__":
    asyncio.run(main())
