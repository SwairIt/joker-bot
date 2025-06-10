from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin

from database.orm_query import orm_get_jokes, orm_get_joke, orm_add_joke, orm_update_joke, orm_delete_joke

from kbds.reply import get_keyboard
from kbds.inline import all_jokes_kbd


router = Router()
router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить анекдот",
    "Все анекдоты",
    placeholder="Выберите действие",
    sizes=(2,),
)


@router.message(StateFilter(None), Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer("Добро пожаловать, Админ. Выберите действие на клавиатуре", reply_markup=ADMIN_KB)



@router.message(StateFilter(None), F.text == "Все анекдоты")
async def all_jokes_cmd(message: types.Message, session: AsyncSession):
    try:
        jokes = await orm_get_jokes(session)
    except Exception as e:
        await message.answer("Ошибка при получении анекдотов.")
        return

    if not jokes:
        await message.answer("Анекдотов пока нет.")
        return

    for joke in await orm_get_jokes(session):
        await message.answer(
            f'<b>Название: {joke.name}</b>\n\n{joke.text}\nРейтинг: {joke.rating}',
            reply_markup=all_jokes_kbd(joke.id)
        )
    await message.answer("Все анекдоты ⏫")


@router.callback_query(StateFilter(None), F.data.startswith("delete_joke_"))
async def delete_joke_cmd(callback: types.CallbackQuery, session: AsyncSession):
    joke_id = int(callback.data.split('joke_')[-1])

    await orm_delete_joke(session=session, joke_id=joke_id)

    await callback.answer("Вы успешно удалили анекдот")
    await callback.message.delete()



############ FSM АДМИНКА #########################


class AddJoke(StatesGroup):
    name = State()
    text = State()
    rating = State()
    category = State()

    joke_for_change = None

    texts = {
        "AddJoke:name": "Введите название заново",
        "AddJoke:text": "Введите анекдот заново",
        "AddJoke:rating": "Введите рейтинг заново",
        "AddJoke:category": "Выберите категорию заново"
    }



@router.message(StateFilter(None), F.text.startswith("Добавить анекдот"))
async def add_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.answer("Введите название анекдота", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddJoke.name)


@router.callback_query(StateFilter(None), F.data.startswith("update_joke_"))
async def add_cmd(callback: types.Message, state: FSMContext, session: AsyncSession):
    joke_id = int(callback.data.split("joke_")[-1])

    joke_for_change = await orm_get_joke(session, int(joke_id))

    AddJoke.joke_for_change = joke_for_change

    await callback.answer("Вы изменяете анекдот")
    await callback.message.answer("Введите название анекдота")
    await state.set_state(AddJoke.name)


@router.message(StateFilter("*"), Command("отмена"))
@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddJoke.joke_for_change:
        AddJoke.joke_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@router.message(StateFilter("*"), Command("назад"))
@router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddJoke.name:
        await message.answer(
            'Предыдущего шага нет, или введите название товара или напишите "отмена"'
        )
        return

    previous = None
    for step in AddJoke.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddJoke.texts[previous.state]}"
            )
            return
        previous = step


@router.message(AddJoke.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "." and AddJoke.joke_for_change:
        await state.update_data(name=AddJoke.joke_for_change.name)
    else:
        if 0 >= len(message.text) >= 50:
            await message.answer("Название анекдота не должно превышать 50 символов\nили быть менее 1го символа. \n Введите заново")
            return
        await state.update_data(name=message.text)
    await message.answer("Введите сам анекдот")
    await state.set_state(AddJoke.text)


@router.message(AddJoke.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите название анекдота заново")


@router.message(AddJoke.text, F.text)
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and AddJoke.joke_for_change:
        await state.update_data(text=AddJoke.joke_for_change.text)
    else:
        if 14 >= len(message.text) >= 250:
            await message.answer(
                "Сам анекдот не должен превышать 250 символов\nИли быть менее 15 символов\nВведите заново"
            )
            return
        await state.update_data(text=message.text)

    await message.answer("Введите рейтинг анекдота")
    await state.set_state(AddJoke.rating)


@router.message(AddJoke.text)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания товара")


@router.message(AddJoke.rating, F.text)
async def add_rating(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and AddJoke.joke_for_change:
        await state.update_data(rating=AddJoke.joke_for_change.rating)
    elif message.text.isdigit():
        await state.update_data(rating=message.text)
    else:
        await message.answer("Введите число!")

    data = await state.get_data()
    try:
        if AddJoke.joke_for_change:
            await orm_update_joke(session, AddJoke.joke_for_change.id, data)
        else: 
            await orm_add_joke(session, data)
        await message.answer("Анекдот добавлен/изменен", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка: \n{str(e)}\nОбратитесь к программеру")
        await state.clear()

    AddJoke.joke_for_change = None    

        
@router.message(AddJoke.rating)
async def add_rating_2(message: types.Message, state: FSMContext):
    await message.answer("Введите число!")