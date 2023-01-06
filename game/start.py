registrationStatus = {}
reg_text = "Поздравляем с успешной регистрацией! Советуем вступить в чат новичков, где опытные менторы помогут освоиться в игре и помогут с развитием в игре (https://t.me/TowerOfHeaven_SCFNP), а так же - в новостной канал (https://t.me/TowerOfHeaven), чтобы быть в курсе всех обновлений.\nДля удачного начала игры советуем прочитать гайд от игрока - https://telegra.ph/Tower-of-Heaven-07-14-2\nЕсли вдруг потеряете гайд, воспользуйтесь командой /help\nПриятной игры."
refcodes = {}


class Rega(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()




async def register_new_user(call, choosed_weapon, refcodes):
    if call.from_user.id in refcodes:
        checkref = await db.Users.exists(user_id=refcodes[call.from_user.id])
        if checkref:
            pass
        else:
            refcodes[call.from_user.id] = 702528084
    else:
        refcodes[call.from_user.id] = 702528084
    await db.Users.filter(user_id=refcodes[call.from_user.id]).update(eat=F('eat') + 1000)
    checkref = await db.Users.get(user_id=refcodes[call.from_user.id])
    if call.from_user.username:
        user = db.Users(username=call.from_user.username, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0, regDate=time.time(), money=1000)
    else:
        user = db.Users(username=call.from_user.first_name, user_id=call.from_user.id, ref=refcodes[call.from_user.id], ban=0, regDate=time.time(), money=1000)
    if user:
        user.item = choosed_weapon
        await user.save()
        await db.addItem(choosed_weapon, user)
        await db.Inventory.filter(name=choosed_weapon, idplayer=user.id).update(active=2)
        try:
        	await bot.send_message(checkref.user_id, 'По твоей ссылке зарегистрировался {}. +1000🍗'.format(user.username))
        except:
        	pass
        await bot.edit_message_text('Готово!', call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, "Назови своё имя, путник.\n\n`Длина имени не должна превышать 20 символов. Запрещены пустые имена, имена с эмодзи и ''глитч''-символами`", parse_mode='markdown')
        await db.Referals.create(idplayer=user.id, refer=refcodes[call.from_user.id])
async def nick_parser(text, reg=True):
    count = 0
    txt = text
    symbols = 'qwertyuiopasdfghjklzxcvbnm'
    symbols += 'йёцукенгшщзхъфывапролджэячсмитьбю'
    symbols += '1234567890'
    _space = False
    nick = ""
    for symbol in txt:
        count += 1
        if count >= 20:
            return nick
        if symbol in ' ' and not _space and reg:
            _space = True
        elif symbol.lower() not in symbols:
            txt = txt.replace(symbol, "")
        else:
            _space = False
        nick += symbol
    return nick

async def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


@dp.message_handler(commands=['start'])
async def start(m):
    try:
        await dp.throttle(str(m.from_user.id), rate=2)
    except exceptions.Throttled:
        return
    if m.from_user.id == m.chat.id and m.from_user.id not in bannedUsers:
        pass
    else:
        return
    checkplayer = await db.Users.exists(user_id=m.from_user.id)
    if checkplayer:
        user = await db.Users.get(user_id=m.from_user.id)
        checkAchs = await db.Ach.exists(user_id=m.from_user.id)
        if not checkAchs: 
            newAch = await db.Ach(user_id=m.from_user.id)
            await newAch.save()
        await profile(m, user)
        return
    else:
        unique_code = await extract_unique_code(m.text)
        await logBot.send_message(tradeChat, "New user: @{} \n{}\nRef {}".format(m.from_user.username, m.from_user.id, unique_code))
        await logBot.send_message(leadersChannel, "New user: @{} \n{}\nRef {}".format(m.from_user.username, m.from_user.id, unique_code))
        if not unique_code:
            unique_code = 702528084
        elif unique_code == 'otorhin':
            unique_code = 1175149001
        elif unique_code == 'yourbadapple':
            unique_code = 164964738
        elif unique_code == 'genshinb':
            unique_code = 370226611
        elif unique_code == 'howyourbot':
            unique_code = 1072026915
        elif unique_code == 'mobimes':
            unique_code = 1072026915
        refcodes[m.from_user.id] = unique_code
        text = "Приветствую тебя, дорогой странник. Перед началом, советую выбрать оружие. Выбирай с умом..."
        text += "\n\nПистолет с ножом - связка, имеющая неплохой потенциал. Основным оружием служит нож, но в любой момент можно отскочить от противника и выстрелить в него, нанеся критический урон.\nОсобая способность: Выстрел. Способность наносит критический урон 150% (15% шанс нанести 175% урона)"
        text += "\n\nКопьё - отличное оружие, позволяющее наносить связки быстрых ударов. Одно из самых первых видов оружий мира, дошедших до нашего времени. Возможно кто-то из твоих предков убивал таким динозавров, а ты пошел по его стопам.\nОсобая способность: Серия ударов. Способность наносит три удара по 30% урона (шанс нанести 100% урона каждую атаку 30%)"
        text += "\n\nКатана – похожий на саблю японский меч с изогнутым клинком, заточенный с одной стороны. Режущая часть сделана из нескольких видов стали, она одновременно прочная и острая, долго держит заточку. Доселе неизвестна технология изготовления, также как и где же эта Япония..\nОсобая способность: Рубящий удар. Возможность убить монстра с одного удара с шансом в 20%"
        text += "\n\nМеч - полуторный прямой клинок заточенный с двух сторон, гарда сделана в форме креста. Таким можно наносить глубокие и болезненные порезы!\nОсобая способность: Выпад. Наносит 30% от максимального хп моба (25% шанс нанести 50% от максимального хп моба)"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Катана', callback_data="registration_select_katana"))
        markup.add(InlineKeyboardButton('Меч', callback_data="registration_select_mech"))
        markup.add(InlineKeyboardButton('Пистолет с ножом', callback_data="registration_select_pistol"))
        markup.add(InlineKeyboardButton('Копьё', callback_data="registration_select_kopie"))
        await bot.send_message(m.chat.id, text, reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data.startswith('registration_select_'))
async def reg(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    item = do[2]
    global refcodes
    checkUsers = await db.Users.exists(user_id=call.from_user.id)
    if checkUsers:
        await bot.edit_message_text("Error", call.message.chat.id, call.message.message_id)
        return
    try:
        if refcodes[call.from_user.id]:
            pass
        a = int(refcodes[call.from_user.id])
    except:
        refcodes[call.from_user.id] = 702528084
    checkref = await db.Users.exists(user_id=refcodes[call.from_user.id])
    if checkref:
        pass
    else:
        refcodes[call.from_user.id] = 702528084
        checkref = await db.Users.get(user_id=refcodes[call.from_user.id])
        checkref.eat += 100
        await checkref.save()

    if item == 'katana':
        await register_new_user(call, "Катана", refcodes)
        
    elif item == 'mech':
        await register_new_user(call, "Меч", refcodes)

    elif item == 'pistol':
        await register_new_user(call, "Пистолет с ножом", refcodes)

    elif item == 'kopie':
        await register_new_user(call, "Копьё", refcodes)

    registrationStatus[call.from_user.id] = 'reg_nick'
    add = await db.Ach(user_id=call.from_user.id)
    await add.save()
    await bot.edit_message_text("Очень хорошо.. Теперь введи своё имя, чтобы мы знали как к тебе обращаться...", call.message.chat.id, call.message.message_id)

async def goToTutor(m):
    user = await db.Users.get(user_id=m.from_user.id).first()
    markup = InlineKeyboardMarkup(row_width=2)
    text = """`Очнувшись от запаха дерьма, перемешанным с нашатырём (и не поймёшь, от чего пришёл в себя), ты увидел над собой человека в грязном, пошарпанном наряде, который можно охарактеризовать только одним словом - тряпки. Заметив твоё пробуждение, мужчина отложил чёрную вату, от которой несло нашатырём и тебе осталось только вдыхать удивительные ароматы дерьма, которым несло от твоего, наверное, спасителя.`
    -Слава богу ты очнулся. Помнишь вообще как тебя зовут?
`Ты назвал  своё имя`
    -А еще что-то помнишь?
`Покачав головой, которая, кстати, почему-то болела, ты заодно мельком осмотрел палатку в которой находился`
    -Ну, не переживай. Если имя помнишь, да и руки-ноги целы, значит жизнь продолжается! Я тебе так скажу - скорее всего ты из Хэвенбурга - пока местные бомжи тебя до конца не обобрали, ты выглядел вполне прилично, а так наряжаются только ребята оттуда.
`"Хэвенбург? Впервые слышу" - погрузившись в раздумья, пытаешься что-то вспомнить, но от этого легче не становится. Тем временем, мужчина продолжает говорить...`
    -...вернуться сможешь через пустыню, но для начала тебе бы приодеться, а то так в трусах и будешь идти? Учти, у нас тут не курорт, жара адская, да и город окружен всякой нечистью от которой тебе либо прятаться либо уничтожать. Вот что я тебе посоветую. Вот тебе немного денег, купи себе хоть что-то из одежды, ну и {}. Больше нет, извиняй, сам бы приоделся. 
Одёжка продаётся у Ашота на площади, это вот выйдешь с палатки и просто топай по прямой. А еще желательно наведываться регулярно к охраннику, у выхода из города, у него можно неплохо подзаработать. Ну всё, чего расселся? Давай, проваливай! Приоденешься и вали с нашего гадюшника пока тебя опять бомжи не разодрали.
    Получено: 500💰, {}""".format(user.item, user.item)
    await bot.send_message(m.chat.id, text, parse_mode='markdown')
    await asyncio.sleep(10)
    await profile(m, user)
    await asyncio.sleep(3)
    text2 = """Выйдя из палатки, нетвёрдым шагом направился по прямой. ''Чёрт его знает что происходит, но, надеюсь, меня попустит...'', - думал ты про себя. Тем временем твоему взору открылась площадь этого гадюшника. Иначе это и не назовёшь. Что же, посмотрим...

    Главная площадь - гордость этого города: кучка построек, начиная с качалки и заканчивая ларьком с мусором, в аккурат расставлены вокруг разбитого в труху фонтана с табличкой «Ремонт»\nПосреди площади висит стенд с обьявлениями."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Пройти обучение', callback_data="startTutor"))
    markup.add(InlineKeyboardButton('Отказаться', callback_data="stopTutor"))
    await bot.send_message(m.chat.id, text2, parse_mode='markdown')
    await asyncio.sleep(2)
    await bot.send_message(m.chat.id, "⚠️Перед началом игры рекомендуется пройти небольшое обучение", reply_markup=markup)
nicks = {}

@dp.message_handler(lambda m: registrationStatus and m.from_user.id in registrationStatus and registrationStatus[m.from_user.id]=='reg_nick')
async def reg_nick(m):
    if m.from_user.id != m.chat.id: return
    global nicks
    txt = await nick_parser(m.text, reg=True)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.row(item1, item2)
    await bot.send_message(m.chat.id, 'Твоё имя - {}?'.format(txt), reply_markup=markup)
    nicks[m.from_user.id] = txt
    registrationStatus[m.from_user.id] = 'reg_nick_1'

@dp.message_handler(lambda m: registrationStatus and m.from_user.id in registrationStatus and registrationStatus[m.from_user.id]=='reg_nick_1')
async def reg_nick_1(m):
    global nicks
    if m.text == "Да":
        checknick = await db.Users.exists(username=nicks[m.from_user.id])
        if checknick:
            checknick = await db.Users.get(username=nicks[m.from_user.id]).first()
            if checknick.username == nicks[m.from_user.id] and checknick.user_id != m.from_user.id:
                await bot.send_message(m.chat.id, "К сожалению, такого героя мы уже знаем. Может, тебя зовут как-нибудь еще?\nЕсли это сообщение вылазит слишком часто, обратитесь в /report")
                registrationStatus[m.from_user.id] = 'reg_nick'
                return
        user = await db.Users.get(user_id=m.from_user.id).first()
        user.username = nicks[m.from_user.id]
        await user.save()
        registrationStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы можете получить еще один бонус! \nВступите в группу обсуждения игры ( @TowerOfHeaven_chat ) и получите бонус!")
        if user.location == 'Город' and user.lvl == 1 and user.exp == 0:
            await goToTutor(m)
    elif m.text == "Нет":
        await bot.send_message(m.chat.id, "Тогда назови своё настоящее имя!")
        registrationStatus[m.from_user.id] = 'reg_nick'


@dp.callback_query_handler(lambda call: call.data.startswith('stopTutor'))
async def stopTutor(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    await bot.edit_message_text("Приятной игры!", call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith('startTutor'))
async def startTutor(call):
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    await bot.edit_message_text("Отлично. Начнём?", call.message.chat.id, call.message.message_id)
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    if user:
        await bot.send_message(tradeChat, "{} ({}) начал обучение.".format(user.username,user.id))
        await asyncio.sleep(1)
        text = f"""
👤{user.username}
👥Изгой
📡Город🏪Площадь
🔆1 (✨0/150)

❤️20/20🛡0(⚔️0%)
🔪20(+0)
⚡️100/100 🍗100/100
💮5 pp (#0)

💰500 💎0 🔘5

📦0/10
🆔 - {user.id}
        """
    await bot.send_message(call.message.chat.id, text)
    await asyncio.sleep(2)
    text = """
Это твой профиль. Город-Площадь - текущее местоположение. Ниже указан уровень (первый) и прогресс в виде опыта.
После этого идёт строки с твоими характеристиками. ❤️ обозначает здоровье, 🛡 - броню. 3ед брони поглощают 1ед урона. ⚔️ - блокировка урона в PvP
🔪20 - твоя чистая атака. В скобках указан бонус который зависит от оружия и его прокачки, а так же других факторов, которые не присутствуют на начальных этапах игры.
⚡️ - твои силы. Чем выше сила, тем выше урон в битве. Выше 90 единиц урон равняется показателям, указанным в профиле. 
🍗 - твоя сытость. Сила пополняется за счёт сытости, поэтому кушать полезно. 
💰 - это золото. 💎 - это кристаллы, донат валюта. 🔘 - это очки прокачки. За их счёт можно прокачивать различные бонусы в /skills
📦0/10 - заполненность инвентаря.
    """
    await bot.send_message(call.message.chat.id, text)
    await asyncio.sleep(10)
    text = """
Основное время в игре уделяется PvE. В мире полно монстров которых необходимо истребить. За убийство монстра тебе полагается награда в виде 💰Золота и ✨Опыта.
Чем сильнее монстр, тем выше награду ты получаешь. Иногда с монстров может выпасть какой-нибудь предмет поэтому желательно следить за заполненностью инвентаря.
Сами монстры находятся у окраин городов и чем дальше находится город и, естественно, ты от города - тем сильнее сами монстры.
На старте игры советую посетить охранника ворот у выхода из города - у него есть несколько заданий, которые помогут лучше освоиться и понять определенные игровые механики. Ну и 💰Золота за это он тоже немного даст.

Основными командами в игре являются "Профиль", "Навигация" и "Инвентарь". В Навигации на Площади текущего города есть небольшие подсказки по игровому процессу, советую обращать на них внимание :)


Приятной игры!"""
    await bot.send_message(call.message.chat.id, text)




async def startBonus(m, user):
    if user and user.lvl <= 4:
        if user.coupon == 0:
            timeBoost = int(time.time()) + 36000
            if user.booster >= int(time.time()): await db.Users.filter(id=user.id).update(booster=F('booster') + 36000, money=F('money') + 500, coupon=1)
            else: await db.Users.filter(id=user.id).update(booster=timeBoost, money=F('money') + 500, coupon=1)
            await bot.send_message(m.chat.id, "Поздравляем с получением стартового бонуса!\n⚡️10ч Бустеры (увеличивают награду с монстра)\n500💰\n\nПриятной игры!")
            await logBot.send_message(tradeChat, "{} ({}) забрал стартовый бонус".format(user.username, user.id))
        else:
            await bot.send_message(m.chat.id, "Ты уже получал этот бонус.")




@dp.callback_query_handler(lambda call: call.data.startswith('newclanjoin'))
async def newclanjoin(call):
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    if user:
        if user.frak:
            checkFrak = await db.Fraks.get_or_none(name=user.frak).first()
            if checkFrak:
                return await bot.edit_message_text("К сожалению, вступить в Академию можно только новичкам, не состоящим в другом клане", call.message.chat.id, call.message.message_id)
        if user.atk + user.hp > 1000:
            return await bot.edit_message_text("К сожалению, вступить в Академию можно только новичкам", call.message.chat.id, call.message.message_id)
        await db.Users.filter(id=user.id).update(frak="📚Академия📚")
        await bot.edit_message_text("Отлично. Я тебя записал. Держи ссылку-приглашение в чат клана\nhttps://t.me/+fpUvTUZ0CHQ2MGUy", call.message.chat.id, call.message.message_id)
        frak = await db.Fraks.get_or_none(id=0).first()
        leader = await db.Users.get_or_none(id=frak.leader).first()
        text = "Новый игрок в академке\n[{}](tg://user?id={}) ({}) (@{})".format(user.username, user.user_id, user.id, call.from_user.username)
        try:
            await bot.send_message(leader.user_id, text, parse_mode='markdown')
        except:
            pass










@dp.message_handler(commands=['help'])
async def help(m):
    try:
        await dp.throttle(str(m.from_user.id), rate=1)
    except exceptions.Throttled:
        return
    global __ver__
    await m.answer("Tower of Heaven v.{}\nКанал игры (новости) - @TowerOfHeaven\nГруппа обсуждения игры - @TowerOfHeaven_chat\nПомощь администрации - /report\n\nДругие источники:\nГайд от игрока (устаревший) - https://telegra.ph/Tower-of-Heaven-07-14-2\nВаш универсальный помощник в мире башни - @Helper_ToH_bot\nВики от игрока - @TowerOfHeaven_wiki".format(__ver__))


