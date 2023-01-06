class BottoStatus(StatesGroup):
    cmd = State()
    destroy = State()
    setPassword = State()
    hacking = State()



async def botProfile(m, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    errors = 0
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if not user: return 
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if droid.status == 1 and checkChip: status = "Полностью функционирует🟢"
    elif droid.status == 2 and checkChip: status = "Обнаружены системные ошибки⚠️"
    else: status = "Выведен из строя. Ремонт невозможен.🔴"
    atk = user.lvl * 1.5
    bonusAtk = 0
    checkBonusesToAtk = await db.BotInventory.filter(idbot=droid.id, active=2, type='Урон')
    if checkBonusesToAtk:
        for bonus in checkBonusesToAtk:
            bonusAtk += bonus.bonus
    fullAtk = int(atk * (bonusAtk / 100 + 1))
    """checkHpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='ЧИП ОЗ')
    if checkHpBar: hp = "{}/{}".format(droid.nowhp, droid.hp)
    else:
        hp = "UNKNOWN/{}".format(droid.hp)
        status = "Обнаружены системные ошибки⚠️"""
    needExp = droid.lvl * 1000
    checkExpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОП')
    if checkExpBar:
        expierence = "(✨{}/{})".format(droid.exp, needExp)
    else:
        expierence = "(✨UNKNOWN)"
        status = "Обнаружены системные ошибки⚠️"
    checkWeapon = await db.BotInventory.exists(type='Оружие', active=2, idbot=droid.id)
    if not checkWeapon: status = "Обнаружены системные ошибки⚠️"
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    text = f"""Бот-00{droid.id}-{droid.model}
Уровень: {droid.lvl}
Опыт: {expierence}
Статус: {status}
Атака: {fullAtk}
Слоты чипов: {inventorySize}/{inventorySizeMax}
🔧Детали: {droid.details}
"""
    if droid.status == 1 and checkChip: mainStatus = "OK"
    elif droid.status == 2 and checkChip: mainStatus = "Unstable"
    else: mainStatus = "Boot error"
    #checkChipHP = await db.BotInventory.exists(name='Чип ОЗ', active=2, idbot=droid.id)
    #if not checkChipHP: errors += 1
    checkChipEXP = await db.BotInventory.exists(name='Чип ОП', active=2, idbot=droid.id)
    if not checkChipEXP: errors += 1
    checkWeapon = await db.BotInventory.exists(type='Оружие', active=2, idbot=droid.id)
    if not checkWeapon: errors += 1
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100
    
    text += "\nLOG: Проверка системы..."
    text += f"\nLOG: Основная работоспособность - {mainStatus}"

    if errors == 0 and droid.status == 1 and checkChip:
        text += "\nLOG: Запуск системы..."
        text += f"\nLOG: Вторичная ОС - ошибок не обнаружено"
        text += "\nLOG: Диагностика завершена. Доступ к терминалу разрешен."
        markup.add(InlineKeyboardButton('Терминал', callback_data="botCMD"))
    elif errors > 0 and droid.status == 1 and checkChip:
        text += "\nLOG: Запуск системы..."
        text += f"\nLOG: Вторичная ОС - обнаружены ошибки!"
        if not checkChipEXP:
            text += f"\nLOG: Вторичная ОС - отсутствует чип ОП"
        #if not checkChipHP:
            #text += f"\nLOG: Вторичная ОС - отсутствует чип ОЗ"
        if inventorySizeMax - inventorySize < 5:
            text += f"\nLOG: Вторичная ОС - память нагружена"
        if not checkWeapon:
            text += f"\nLOG: Вторичная ОС - отсутствует оружие"
        text += "\nLOG: Диагностика завершена. Доступ к терминалу разрешен."
        markup.add(InlineKeyboardButton('Терминал', callback_data="botCMD"))
    elif droid.status == 2:
        text += "\nLOG: Запуск системы..."
        text += "\nLOG: Ошибка модуля поиска ошибок. Дальнейшая диагностика невозможна."
    else:
        text += "\nLOG: Ошибка запуска системы. Дальнейшая диагностика невозможна."
    await bot.send_message(m.chat.id, text, reply_markup=markup)


async def botProfileCallback(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    errors = 0
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if droid.status == 1 and checkChip: status = "Полностью функционирует🟢"
    elif droid.status == 2 and checkChip: status = "Обнаружены системные ошибки⚠️"
    else: status = "Выведен из строя. Ремонт невозможен.🔴"
    hp = droid.hp
    checkBonusesToHp = await db.BotInventory.filter(idbot=droid.id, active=2, type='Здоровье')
    for bonus in checkBonusesToHp:
        hp += bonus.bonus
    """checkHpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='ЧИП ОЗ')
    if checkHpBar: hp = "{}/{}".format(droid.nowhp, droid.hp)
    else:
        hp = "UNKNOWN/{}".format(droid.hp)
        status = "Обнаружены системные ошибки⚠️"""
    needExp = droid.lvl * 1000
    checkExpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОП')
    if checkExpBar:
        expierence = "(✨{}/{})".format(droid.exp, needExp)
    else:
        expierence = "(✨UNKNOWN)"
        status = "Обнаружены системные ошибки⚠️"
    checkWeapon = await db.BotInventory.exists(type='Оружие', active=2, idbot=droid.id)
    if not checkWeapon: status = "Обнаружены системные ошибки⚠️"
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100
    text = f"""Бот-00{droid.id}-{droid.model}
Уровень: {droid.lvl}
Опыт: {expierence}
Статус: {status}
Здоровье: {hp}
Слоты чипов: {inventorySize}/{inventorySizeMax}
🔧Детали: {droid.details}

"""
    if droid.status == 1 and checkChip: mainStatus = "OK"
    elif droid.status == 2 and checkChip: mainStatus = "Unstable"
    else: mainStatus = "Boot error"
    checkChipHP = await db.BotInventory.exists(name='Чип ОЗ', active=2, idbot=droid.id)
    if not checkChipHP: errors += 1
    #checkChipEXP = await db.BotInventory.exists(name='Чип ОП', active=2, idbot=droid.id)
    #if not checkChipEXP: errors += 1
    checkWeapon = await db.BotInventory.exists(type='Оружие', active=2, idbot=droid.id)
    if not checkWeapon: errors += 1
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100

    text += "\nLOG: Проверка системы..."
    text += f"\nLOG: Основная работоспособность - {mainStatus}"

    if errors == 0 and droid.status == 1 and checkChip:
        text += "\nLOG: Запуск системы..."
        text += f"\nLOG: Вторичная ОС - ошибок не обнаружено"
        text += "\nLOG: Диагностика завершена. Доступ к терминалу разрешен."
        markup.add(InlineKeyboardButton('Терминал', callback_data="botCMD"))
    elif errors > 0 and droid.status == 1 and checkChip:
        text += "\nLOG: Запуск системы..."
        text += f"\nLOG: Вторичная ОС - обнаружены ошибки!"
        if not checkChipEXP:
            text += f"\nLOG: Вторичная ОС - отсутствует чип ОП"
        #if not checkChipHP:
            #text += f"\nLOG: Вторичная ОС - отсутствует чип ОЗ"
        if inventorySizeMax - inventorySize < 5:
            text += f"\nLOG: Вторичная ОС - память нагружена"
        if not checkWeapon:
            text += f"\nLOG: Вторичная ОС - отсутствует оружие"
        text += "\nLOG: Диагностика завершена. Доступ к терминалу разрешен."
        markup.add(InlineKeyboardButton('Терминал', callback_data="botCMD"))
    elif droid.status == 2:
        text += "\nLOG: Запуск системы..."
        text += "\nLOG: Ошибка модуля поиска ошибок. Дальнейшая диагностика невозможна."
    else:
        text += "\nLOG: Ошибка запуска системы. Дальнейшая диагностика невозможна."
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def botCMD(call, user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(name='Чип ОС', active=2, idbot=droid.id)
    if droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 2:
        cmdPass = False
    else:
        cmdPass = False
    if cmdPass:
        text = f"BOT-00{droid.id}-{droid.model} terminal"
        text += "\n\nВведите запрос для системы. Для помощи введите help"
        await BottoStatus.cmd.set()
    else:
        text = "ОС: Доступ к терминалу запрещён"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

async def botCMDReturn(m, user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(name='Чип ОС', active=2, idbot=droid.id)
    if droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 2:
        cmdPass = False
    else:
        cmdPass = False
    if cmdPass:
        text = f"BOT-00{droid.id}-{droid.model} terminal"
        text += "\n\nВведите запрос для системы. Для помощи введите help"
        await BottoStatus.cmd.set()
    else:
        text = "ОС: Доступ к терминалу запрещён"
    await bot.send_message(m.chat.id, text)

@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=BottoStatus.cmd)
async def cmdBot(m, state=FSMContext):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if not user: return
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    errors = 0
    checkChip = await db.BotInventory.exists(name='Чип ОС', active=2, idbot=droid.id)
    if droid.status == 1 and checkChip: mainStatus = "OK"
    elif droid.status == 2 and checkChip: mainStatus = "Unstable"
    else: mainStatus = "Boot error"
    if droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 1 and checkChip:
        cmdPass = True
    elif droid.status == 2:
        cmdPass = False
    else:
        cmdPass = False
    if not cmdPass:
        text = "ОС: Доступ к терминалу запрещён"
    else:
        if m.text.lower() == 'help':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += """
`  help    `- выводит список доступных команд.
`  in      `- выводит весь инвентарь Бота.
`  eq      `- выводит все используемые чипы.
`  repair  `- запуск автоматического исправления ошибок.
`  gather  `- открыть меню сбора схем
`  log     `- выводит список логов Бота. Параметры:
`  log +10 `- выводит первые 10 строк.
`  log -10 `- выводит последние 10 строк.
`        `По умолчанию используется log -10.
`  bot `- закрывает терминал, открывает профиль.
`  passwd  `- смена пароля администратора.
`  destroy `- я хочу покончить со всем этим.
`  exit    `-  закрывает терминал."""
        elif m.text.lower() == 'exit':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nПодтверждаю закрытие терминала"
            await state.finish()
        elif m.text.lower() == 'in':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к просмотру инвентаря разрешен..."
        elif m.text.lower() == 'eq':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к просмотру снаряжения разрешен..."
        elif m.text.lower().startswith('log'):
            order = '+'
            limit = False
            if "+" in m.text or "-" in m.text:
                try:
                    d = m.text.split(" ")[1]
                    order = list(d)[0]
                    limit = list(d)[1]
                    if not limit: _limit = 10
                    try:
                        _limit = int(limit)
                    except:
                        print(limit)
                        _limit = 10
                    if int(_limit) > 100: _limit = 10
                    if order == '+':
                        botLogs = await db.BotLogs.filter(idbot=droid.id).order_by('-id').limit(_limit)
                    elif order == '-':
                        botLogs = await db.BotLogs.filter(idbot=droid.id).order_by('id').limit(_limit)
                except:
                    botLogs = await db.BotLogs.filter(idbot=droid.id).order_by("-id").limit(10)
            else:
                botLogs = await db.BotLogs.filter(idbot=droid.id).order_by("-id").limit(10)
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к журналу записи разрешен..."
            text += f"\n>{m.text}\n"
            if botLogs:
                for log in botLogs:
                    text += f"\nLOG: {log.text}"
            else:
                text += "\nLOG: NULL"
        elif m.text.lower() == 'destroy':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += f"\nВНИМАНИЕ! Эта операция приведёт к выведению из строя единицу BOT-00{droid.id}-{droid.model}"
            text += "\nЭтот процесс невозможно будет остановить или отменить."
            text += "\n\nВы уверены? (Y/n)"
            await state.finish()
            await BottoStatus.destroy.set()
        elif m.text.lower().startswith("/wear_"):
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к экипировке разрешен."
        elif m.text.lower().startswith("/unwear_"):
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к экипировке разрешен."
        elif m.text.lower() == 'bot':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к профилю разрешен."
            await state.finish()
        elif m.text.lower() == 'repair':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к модулю автоматического исправления ошибок разрешен."
        elif m.text.lower() == 'gather':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nПодключение к информационному серверу..."
        elif m.text.lower() == 'passwd':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nДоступ к смене пароля администратора разрешен."
        elif m.text.lower().startswith('/collect_'):
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nОтправка команды..."
        elif m.text.lower().startswith('/demotion_'):
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nОтправка команды..."
        else:
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nКоманда не распознана. Для помощи введите help"
    if m.text.lower() == 'help': await bot.send_message(m.chat.id, text, parse_mode='markdown')
    else: await bot.send_message(m.chat.id, text)
    await asyncio.sleep(1)
    if m.text.lower() == 'in': await botInventory(user)
    elif m.text.lower() == 'eq': await botPers(user)
    elif m.text.lower() == 'bot': await botProfile(m, user)
    elif m.text.lower() == 'repair': await botRepair(m, user)
    elif m.text.lower() == 'gather': await bottoShop(m, user)
    elif m.text.lower() == 'passwd': await changePass(m)
    elif m.text.lower().startswith("/wear_"): await botWear(m)
    elif m.text.lower().startswith("/unwear_"): await botUnwear(m)
    elif m.text.lower().startswith("/collect_"): await botBuy(m)
    elif m.text.lower().startswith("/demotion_"): await botDemotion(m)

@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=BottoStatus.destroy)
async def destroy(m, state=FSMContext):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if not user: return
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    errors = 0
    checkChip = await db.BotInventory.exists(name='Чип ОС', active=2, idbot=droid.id)
    if droid.status != 0 and checkChip:
        cmdPass = True
    else:
        cmdPass = False
    print(cmdPass)
    if not cmdPass:
        text = "ОС: Доступ к терминалу запрещён"
    else:
        if m.text == "Y":
            await state.finish()
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nЗапрошено уничтожение систем единицы..."
            msg = await bot.send_message(m.chat.id, text)
            await asyncio.sleep(1)
            text += "\nПолучение доступа..."
            msg1 = await bot.edit_message_text(text, msg.chat.id, msg.message_id)
            await asyncio.sleep(5)
            text += "\nДоступ получен, на выполнение операции выданы необходимые права."
            msg2 = await bot.edit_message_text(text, msg1.chat.id, msg1.message_id)
            await asyncio.sleep(1)
            text += "\nНачинаю процесс..."
            msg3 = await bot.edit_message_text(text, msg2.chat.id, msg2.message_id)
            await asyncio.sleep(1)
            text += "\nОтключение вторичной ОС..."
            msg4 = await bot.edit_message_text(text, msg3.chat.id, msg3.message_id)
            await asyncio.sleep(3)
            await bot.send_message(m.chat.id, "⚠️Внимание! Обнаружены ошибки в работе Бот-00{}-{}".format(droid.id, droid.model))
            await asyncio.sleep(1)
            text += "\nВторичная ОС отключена.\nУдаление вспомогательных данных..."
            msg5 = await bot.edit_message_text(text, msg4.chat.id, msg4.message_id)
            await asyncio.sleep(3)
            await bot.send_message(m.chat.id, "⚠️Внимание! Вторичная ОС Бот-00{}-{} повреждена. Необходима срочная замена чипов".format(droid.id, droid.model))
            await asyncio.sleep(7)
            text += "\nДанные удалены. Отключение основных служб..."
            msg6 = await bot.edit_message_text(text, msg5.chat.id, msg5.message_id)
            await asyncio.sleep(2)
            await bot.send_message(m.chat.id, "⚠️Внимание! Обнаружены ошибки первичной ОС у Бот-00{}-{}. Необходима немедленная перезагрузка.".format(droid.id, droid.model))
            await asyncio.sleep(3)
            text += "\nУдаление отключенных служб..."
            msg7 = await bot.edit_message_text(text, msg6.chat.id, msg6.message_id)
            await asyncio.sleep(5)
            text += "\nО̶̧̎с̶̞̉н̷̣̕о̷͚̂в̶͖̚н̶̬͝ы̴̝͛ӗ̴̧ ̸̹͝с̶̡̆л̸̩̒у̴͇̿ж̷͑ͅб̸̲̿ы̶̪̓ ̸̟͗о̶̡͗т̷̣̄к̷̡̈́л̶̦̔ю̸̲̀ч̶̛̱е̵̰͠н̷͇̂ы̷̛͕.̷̛͉"
            msg8 = await bot.edit_message_text(text, msg7.chat.id, msg7.message_id)
            await asyncio.sleep(5)
            text += "\nП̸̨̺͔̐̔̎͜е̸̪̾̽̚р̶̨̬̺͆͑ё̶͎̩́͜з̶̡̖̓̉а̴̡̟̣̅г̸͙̘̈̆̊̚р̷͙̒̅͝у̶͇́̐̈́з̶̰̘͆к̴̳̈́̎͗͂а̴͍͕̃ ̷̺̤̬̈́́̒̏О̷̙̲̞̳̄̒̉С̶̪̟̞͇̀̂́.̷̛͉̮ͅ.."
            msg9 = await bot.edit_message_text(text, msg8.chat.id, msg8.message_id)
            await db.Bot.filter(id=droid.id).update(status=0)
        elif m.text == 'n':
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += "\nПроцедура уничтожения отменена пользователем."
            await state.finish()
            await bot.send_message(m.chat.id, text)
        else:
            text = f"BOT-00{droid.id}-{droid.model} terminal"
            text += f"\nВНИМАНИЕ! Эта операция приведёт к выведению из строя единицы BOT-00{droid.id}-{droid.model}"
            text += "\nЭтот процесс невозможно будет остановить или отменить."
            text += "\n\nВы уверены? (Y/n)"
            await bot.send_message(m.chat.id, text)


async def botInventory(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100
    text = "Инвентарь Бот-00{}-{} ({}📦/{}📦)".format(droid.id, droid.model, inventorySize, inventorySizeMax)
    allInventory = await db.BotInventory.filter(idbot=droid.id, active=1)
    for item in allInventory:
        text += "\n{} | {} | {}📦 | /wear_{} (Разобрать /demotion_{})".format(item.name, item.descr, item.size, item.id, item.id)
    await bot.send_message(user.user_id, text)


async def botPers(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100
    text = "Используемые чипы Бот-00{}-{} ({}📦/{}📦)".format(droid.id, droid.model, inventorySize, inventorySizeMax)
    allInventory = await db.BotInventory.filter(idbot=droid.id, active=2)
    for item in allInventory:
        text += "\n{} | {} | {}📦 | /unwear_{}".format(item.name, item.descr, item.size, item.id)
    await bot.send_message(user.user_id, text)


async def botWear(m):
    await asyncio.sleep(1)
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.lower().replace('/wear_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
            if not droid:
                droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
                if not droid: return await m.answer("Бот отсутствует")
            item = await db.BotInventory.get_or_none(id=result).first()
            if item and item.idbot == droid.id:
                inventorySize = 0
                getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
                for itemInInv in getInventory:
                    inventorySize += itemInInv.size
                inventorySizeMax = 45 + (droid.lvl * 5)
                if inventorySizeMax > 100: inventorySizeMax = 100
                if inventorySize + item.size <= inventorySizeMax:
                    await db.BotInventory.filter(id=item.id).update(active=2)
                    await m.answer("{} успешно инициализирован ОС".format(item.name))
                else:
                    await m.answer("ОС: недостаточно оперативной памяти")
            else:
                await m.answer("ОС: неверный идентификатор чипа")


async def botUnwear(m):
    await asyncio.sleep(1)
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.lower().replace('/unwear_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
            if not droid:
                droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
                if not droid: return await m.answer("Бот отсутствует")
            item = await db.BotInventory.get_or_none(id=result).first()
            if item and item.idbot == droid.id:
                await db.BotInventory.filter(id=item.id).update(active=1)
                await m.answer("{} успешно извлечён из ОС".format(item.name))
            else:
                await m.answer("ОС: неверный идентификатор чипа")

async def botDemotion(m):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.lower().replace('/demotion_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
            if not droid:
                droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
                if not droid: return await m.answer("Бот отсутствует")
            item = await db.BotInventory.get_or_none(id=result).first()
            if item and item.idbot == droid.id and item.active != 0:
                await db.BotInventory.filter(id=item.id).update(active=0)
                profit = random.randint(20, 70)
                await db.Bot.filter(id=droid.id).update(details=F('details') + profit)
                await m.answer("{} успешно разобран. Получено: {} 🔧".format(item.name, profit))
            else:
                await m.answer("ОС: неверный идентификатор чипа")


async def botRepair(m, user):
    await asyncio.sleep(1)
    if m.chat.id != m.from_user.id: return
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    
    if not checkChip: return await m.answer("Чип ОС повреждён. Ремонт невозможен.")
    inventorySize = 0
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2).only('size')
    for item in getInventory:
        inventorySize += item.size
    inventorySizeMax = 45 + (droid.lvl * 5)
    if inventorySizeMax > 100: inventorySizeMax = 100

    text = ""
    checkHpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОЗ')
    if not checkHpBar:
        text += "\nОбнаружено отсутствие чипа ОЗ. Ищем подходящий..."
        checkChip = await db.BotInventory.get_or_none(idbot=droid.id, active=1, name='Чип ОЗ')
        if checkChip:
            text += "\nНайден подходящий чип. "
            if inventorySize + checkChip.size <= inventorySizeMax:
                checkChip.active = 2
                await checkChip.save()
                text += "Чип установлен. "
            else:
                text += "Чип не установлен - недостаточно оперативной памяти. "
        else:
            text += "\nПодходящего чипа не найдено.\nПредложение: приобрести чип у торговца чипами."

    checkExpBar = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОП')
    if not checkExpBar:
        text += "\nОбнаружено отсутствие чипа ОП. Ищем подходящий..."
        checkChip = await db.BotInventory.get_or_none(idbot=droid.id, active=1, name='Чип ОП')
        if checkChip:
            text += "\nНайден подходящий чип. "
            if inventorySize + checkChip.size <= inventorySizeMax:
                checkChip.active = 2
                await checkChip.save()
                text += "Чип установлен. "
            else:
                text += "Чип не установлен - недостаточно оперативной памяти. "
        else:
            text += "\nПодходящего чипа не найдено.\nПредложение: приобрести чип у торговца чипами."

    checkWeapon = await db.BotInventory.exists(type='Оружие', active=2, idbot=droid.id)
    if not checkWeapon: 
        text += "\nОбнаружено отсутствие чипа ОП. Ищем подходящий..."
        checkChip = await db.BotInventory.get_or_none(idbot=droid.id, active=1, type='Оружие')
        if checkChip:
            text += "\nНайдено подходящее оружие. "
            if inventorySize + checkChip.size <= inventorySizeMax:
                checkChip.active = 2
                await checkChip.save()
                text += "Оружие установлено. "
            else:
                text += "Оружие не установлено - недостаточно слотов памяти. "
        else:
            text += "\nПодходящего оружия не найдено.\nПредложение: найти оружие."

    if inventorySize + 5 >= inventorySizeMax:
        text += "\nОбнаружена загруженность оперативной памяти. Предложение: освободите память от лишних слотов"
    if text == "":
        text = "Модуль автоматического решения проблем не нашёл ошибок."
    await bot.send_message(m.chat.id, text)



async def bottoShop(m, user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if checkChip:
        text = """Информационный сервер вернул следующие схемы для возможности сбора:

Чип ОС. Извлечение означает смерть | 📦5 | 🔧 50 (/collect_1)
Чип ОП. Показывает опыт, необходимый для следующего уровня. | 📦3 | 🔧 60 (/collect_3)

Чипы атаки:
    Урон+ (повышает урон на 15🔪) | 📦5 | 🔧 125 (/collect_4)
    Урон++ (повышает урон на 30🔪) | 📦9 | 🔧 175 (/collect_5)
    Урон+++ (повышает урон на 50🔪) | 📦12 | 🔧 220 (/collect_6)
    Крит+ (повышает шанс крита на 3%) | 📦5 | 🔧 145 (/collect_7)
    Крит++ (повышает шанс крита на 6%) | 📦9 | 🔧 205 (/collect_8)
    Крит+++ (повышает шанс крита на 9%) | 📦12 | 🔧 250 (/collect_9)

Чипы защиты:
    Здоровье+ (повышает показатель хп бота на 3%) | 📦5 | 🔧 130 (/collect_10)
    Здоровье++ (повышает показатель хп бота на 6%) | 📦9 | 🔧 180 (/collect_11)
    Здоровье+++ (повышает показатель хп бота на на 9%) | 📦12 | 🔧 230 (/collect_12)
    Уклонение+ (повышает шанс уклонения на 3%) | 📦5 | 🔧 175 (/collect_13)
    Уклонение++ (повышает шанс уклонения на 6%) | 📦9 | 🔧 255 (/collect_14)
    Уклонение+++ (повышает шанс уклонения на 9%) | 📦12 | 🔧 325 (/collect_15)
    Защита+ (гарантированное поглощения +3%) | 📦5 | 🔧 150 (/collect_16)
    Защита++ (гарантированное поглощение +6%) | 📦9 | 🔧 225 (/collect_17)
    Защита+++ (гарантированное поглощение +9%) | 📦12 | 🔧 300 (/collect_18)

Прочие чипы:
    Удача+ (шанс выпадения Деталей +3%) | 📦5 | 🔧 150 (/collect_19)
    Удача++ (шанс выпадения Деталей +6%) | 📦9 | 🔧 225 (/collect_20)
    Удача+++ (шанс выпадения Деталей +9%) | 📦12 | 🔧 300 (/collect_21)

Чипы оружия:
    Лазерный выстрел (наносит 500% урона, КД - 10 минут) | 📦15 | 🔧 500 (/collect_22)

Чипы PvP:
    Уклон+ (повышает шанс уклонения на 3%) | 📦5 | 🔧 200 (/collect_23)
    Уклон++ (повышает шанс уклонения на 6%) | 📦9 | 🔧 350 (/collect_24)
    Уклон+++ (повышает шанс уклонения на 9%) | 📦12 | 🔧 475 (/collect_25)
    Удар+ (повышает урон на 3%) | 📦5 | 🔧 175 (/collect_26)
    Удар++ (повышает урон на 6%) | 📦9 | 🔧 300 (/collect_27)
    Удар+++ (повышает урон на 9%) | 📦12 | 🔧 425 (/collect_28)
    Вампиризм+ (повышает вампиризм на 3%) | 📦5 | 🔧 225 (/collect_29)
    Вампиризм++ (повышает вампиризм на 6%) | 📦9 | 🔧 450 (/collect_30)
    Вампиризм+++ (повышает вампиризм на 9%) | 📦12 | 🔧 600 (/collect_31)
    """
        await bot.send_message(m.chat.id, text)


async def botBuy(m):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if checkChip:
        whatBuy = m.text.split("_")[1]
        try:
            lot = int(whatBuy)
        except:
            return
        if lot == 1:
            name = 'Чип ОС'
            price = 50
        #elif lot == 2:
            #name = "Чип ОЗ"
            #price = 65
        elif lot == 3:
            name = "Чип ОП"
            price = 60
        elif lot == 4:
            name = "Урон+"
            price = 125
        elif lot == 5:
            name = "Урон++"
            price = 175
        elif lot == 6:
            name = "Урон+++"
            price = 220
        elif lot == 7:
            name = "Крит+"
            price = 145
        elif lot == 8:
            name = "Крит++"
            price = 205
        elif lot == 9:
            name = "Крит+++"
            price = 250
        elif lot == 10:
            name = "Здоровье+"
            price = 130
        elif lot == 11:
            name = "Здоровье++"
            price = 180
        elif lot == 12:
            name = "Здоровье+++"
            price = 230
        elif lot == 13:
            name = "Уклонение+"
            price = 175
        elif lot == 14:
            name = "Уклонение++"
            price = 255
        elif lot == 15:
            name = "Уклонение+++"
            price = 325
        elif lot == 16:
            name = "Защита+"
            price = 150
        elif lot == 17:
            name = "Защита++"
            price = 225
        elif lot == 18:
            name = "Защита+++"
            price = 300
        elif lot == 19:
            name = "Удача+"
            price = 150
        elif lot == 20:
            name = "Удача++"
            price = 225
        elif lot == 21:
            name = "Удача+++"
            price = 300
        elif lot == 22:
            name = "Лазерный выстрел"
            price = 500
        elif lot == 23:
            name = "Уклон+"
            price = 200
        elif lot == 24:
            name = "Уклон++"
            price = 350
        elif lot == 25:
            name = "Уклон+++"
            price = 475
        elif lot == 26:
            name = "Удар+"
            price = 175
        elif lot == 27:
            name = "Удар++"
            price = 300
        elif lot == 28:
            name = "Удар+++"
            price = 300
        elif lot == 29:
            name = "Вампиризм+"
            price = 225
        elif lot == 30:
            name = "Вампиризм++"
            price = 450
        elif lot == 31:
            name = "Вампиризм+++"
            price = 600
        else:
            return
        if droid.details >= price:
            success = await db.addItemBot(name, droid)
            if success:
                await db.Bot.filter(id=droid.id).update(details=F('details') - price)
                await bot.send_message(m.chat.id, "Чип {} успешно собран.".format(name))
            else:
                await bot.send_message(m.chat.id, "Не удалось собрать чип {}".format(name))
        else:
            await bot.send_message(m.chat.id, "Собрать чип не представляется возможным. Недостаточно 🔧Деталей")



async def changePass(m):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if checkChip:
        await BottoStatus.setPassword.set()
        await bot.send_message(m.chat.id, "Запущен процесс смены пароля администратора. Введите новый пароль. Он не должен превышать 10 символов.")



@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=BottoStatus.setPassword)
async def changingPassword(m, state=FSMContext):
    if len(m.text) > 10:
        await bot.send_message(m.chat.id, "Ошибка. Пароль не должен превышать 10 символов. Попробуйте еще раз.")
    else:
        await state.finish()
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
        if not droid:
            droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
            if not droid: return await m.answer("Бот отсутствует")
        checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
        if checkChip:
            await db.Bot.filter(id=droid.id).update(password=m.text)
            await bot.send_message(m.chat.id, "Новый пароль установлен успешно. Возвращаемся в консоль...")
            user = await db.Users.get_or_none(id=droid.idplayer)
            await botCMDReturn(m, user)

botsMasterPasswords = {}
hackPool = {}
hackKD = {}
@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers and call.data.startswith('hack_'))
async def hack(call):
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return await m.answer("Бот отсутствует")
    if call.from_user.id in hackKD and hackKD[call.from_user.id] >= int(time.time()):
        return await bot.edit_message_text(f"BOT-00{droid.id}-{droid.model}: Взлом временно недоступен", call.message.chat.id, call.message.message_id)
    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
    if checkChip:
        enemyBot = await db.Bot.get_or_none(id=call.data.split("_")[1])
        if enemyBot:
            enemyUser =  await db.Users.get_or_none(id=enemyBot.idplayer).first()
            if enemyUser.location == user.location and enemyUser.progLoc == user.progLoc:
                await bot.send_message(call.message.chat.id, f"BOT-00{droid.id}-{droid.model}: Инициализация процесса взлома...")
                rand = random.randint(0, 3)
                await asyncio.sleep(rand)
                masterPassword = db.ABC(5)
                if enemyBot.id in botsMasterPasswords:
                    del botsMasterPasswords[enemyBot.id]
                if droid.id in hackPool:
                    del hackPool[droid.id]
                hackPool[droid.id] = enemyBot.id
                hashedpass = ""
                hiddenpass = ""
                textForPlayer = ""
                symbolNum = 0
                botsMasterPasswords[enemyBot.id] = masterPassword
                print(masterPassword)
                for char in masterPassword:
                    rand = random.randint(1, 3)
                    hashedpass += db.ABC(rand)
                    hashedpass += char
                    hiddenpass += char
                    symbolNum += 1
                    rando = rand + 1
                    if hiddenpass == masterPassword:
                        textForPlayer += "{}".format(rando)
                    else:
                        textForPlayer += "{}-".format(rando)
                rand = random.randint(1, 3)
                hashedpass += db.ABC(rand)
                textForPlayer += "\n{}".format(hashedpass)
                await BottoStatus.hacking.set()
                await bot.send_message(call.message.chat.id, "Мастер-ключ спрятан в текущем шифре:\n\n{}\n\nВы так же можете ввести пароль администратора, если он у вас имеется. Для отмены взлома введите 'cancel'".format(textForPlayer))
            else:
                await bot.edit_message_text("Ошибка.", call.message.chat.id, call.message.message_id)
        else:
            await bot.send_message(call.message.chat.id, "Бот противника выведен из строя")

@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=BottoStatus.hacking)
async def hackingStep2(m, state=FSMContext):
    if m.text.lower() == 'cancel':
        await state.finish()
        await bot.send_message(m.chat.id, "Процесс взлома остановлен.")
    else:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
        if not droid:
            await bot.send_message(m.chat.id, "Процесс взлома остановлен.")
            await state.finish()
        else:
            enemyBot = await db.Bot.get_or_none(id=hackPool[droid.id], status__in=[1, 2]).first()
            if enemyBot:
                if enemyBot.id in botsMasterPasswords:
                    success = False
                    if m.text == enemyBot.password: success = True
                    elif m.text == botsMasterPasswords[enemyBot.id]: success = True
                    await state.finish()
                    if success:
                        hackKD[m.from_user.id] = int(time.time()) + 300
                        enemy = await db.Users.get_or_none(id=enemyBot.idplayer).first()
                        minDamage = int(enemy.hp * 0.1)
                        maxDamage = int(enemy.hp * 0.2)
                        damage = random.randint(minDamage, maxDamage)
                        if damage >= enemy.nowhp:
                            damage -= 1
                        maxStealed = int(enemyBot.details / 20)
                        stealed = random.randint(0, maxStealed)
                        await db.Users.filter(id=enemy.id).update(nowhp=F('nowhp') - damage)
                        if stealed > 0:
                            hackedTime = int(time.time()) + 600
                            await db.Bot.filter(id=enemyBot.id).update(details=F('details') - stealed, hackedTime=hackedTime)
                            await db.Bot.filter(id=droid.id).update(details=F('details') + stealed)
                            bonusText = "Получено {}🔧".format(stealed)
                            bonusEnemyText = "Потеряно {}🔧".format(stealed)
                        else:
                            bonusText = ""
                            bonusEnemyText = ""
                        await bot.send_message(m.chat.id, "Взлом завершен. Вражеский бот нанёс {}🔪 владельцу.\n{}".format(damage, bonusText))
                        try:
                            await bot.send_message(enemy.user_id, "Ваш бот был взломан. Ваш бот нанёс вам {}🔪\n{}".format(damage, bonusEnemyText))
                        except: pass
                    else:
                        await state.finish()
                        await bot.send_message(m.chat.id, "Взлом не удался. Мастер-ключ неверный. Взлом остановлен.")
                else:
                    await state.finish()
                    await bot.send_message(m.chat.id, "Этот бот не состоит в дуэли.")
            else:
                await state.finish()
                await bot.send_message(m.chat.id, "Бот противника выведен из строя.")


async def getDroidAtk(attacking):
    droid = await db.Bot.get_or_none(idplayer=attacking.id, status__in=[1, 2]).first()
    atk = 0
    if not droid:
        return atk
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Урон+', 'Урон++', 'Урон+++'])
    for item in getInventory:
        if item.name == 'Урон+': atk += 15
        elif item.name == 'Урон++': atk += 30
        elif item.name == 'Урон+++': atk += 50
    return atk

async def getDroidPvPAtk(attacking):
    droid = await db.Bot.get_or_none(idplayer=attacking.id, status__in=[1, 2]).first()
    atk = 0
    if not droid:
        return atk
    if droid.hackedTime >= int(time.time()): return atk
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Удар+', 'Удар++', 'Удар+++'])
    for item in getInventory:
        if item.name == 'Удар+': atk += 3
        elif item.name == 'Удар++': atk += 6
        elif item.name == 'Удар+++': atk += 9
    return atk

async def getDroidPvPUv(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    uv = 0
    if not droid:
        return uv
    if droid.hackedTime >= int(time.time()): return uv
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Уклон+', 'Уклон++', 'Уклон+++'])
    for item in getInventory:
        if item.name == 'Уклон+': uv += 3
        elif item.name  == "Уклон++": uv += 6
        elif item.name  == "Уклон+++": uv += 9
    return uv

async def getDroidPvPHeal(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    heal = 0
    if not droid:
        return heal
    if droid.hackedTime >= int(time.time()): return heal
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Вампиризм+', 'Вампиризм++', 'Вампиризм+++'])
    for item in getInventory:
        if item.name == 'Вампиризм+': heal += 3
        elif item.name  == "Вампиризм++": heal += 6
        elif item.name  == "Вампиризм+++": heal += 9
    return heal


async def getDroidCreet(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    creet = 0
    if not droid:
        return creet
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Крит+', 'Крит++', 'Крит+++'])
    for item in getInventory:
        if item.name == 'Крит+': creet += 3
        elif item.name  == "Крит++": creet += 6
        elif item.name  == "Крит+++": creet += 9
    return creet

async def getDroidUv(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    uv = 0
    if not droid:
        return uv
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Уклонение+', 'Уклонение++', 'Уклонение+++'])
    for item in getInventory:
        if item.name == 'Уклонение+': uv += 3
        elif item.name  == "Уклонение++": uv += 6
        elif item.name  == "Уклонение+++": uv += 9
    return uv

async def getDroidArmor(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    armor = 0
    if not droid:
        return armor
    getInventory = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Защита+', 'Защита++', 'Защита+++'])
    for item in getInventory:
        if item.name == 'Защита+': armor += 3
        elif item.name  == "Защита++": armor += 6
        elif item.name  == "Защита+++": armor += 9
    return armor

async def getDroidWeapon(user):
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    weapon = False
    if not droid:
        return weapon, weapon
    getWeapon = await db.BotInventory.filter(idbot=droid.id, active=2, name__in=['Лазерный выстрел'])
    weaponReady = False
    weaponIds = False
    if getWeapon:
        weaponReady = {}
        weaponIds = {}
        for item in getWeapon:
            weaponIds[item.id] = item.name
            if item.lastAtk <= int(time.time()):
                weaponReady[item.id] = True
            else:
                weaponReady[item.id] = False
    return weaponReady, weaponIds
