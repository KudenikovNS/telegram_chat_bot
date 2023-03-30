import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добрый день! Вы можете задать мне вопрос.")

@dp.message_handler()
async def send(message: types.Message):
    try:
        if not message.text.endswith("?"):
            message.text += "?"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["You:"]
        )
        await message.answer(response['choices'][0]['text'])
    except Exception as e:
        print("An error occurred while processing the message: ", e)
        await message.answer("Произошла ошибка при обработке вашего запроса. Попробуйте еще раз позднее.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
