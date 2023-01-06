async def JiAlley(call, user):
    text = """В Хэвенбурге построена Аллея Жи - небольшой спальный район города. Вы сможете приобрести себе один из нескольких видов домов.
    Каждый дом оснащён системой, аналогичной источникам и отелю. Также в доме будет отдельно выделенное место под складирование вещей которые вам в данный момент не нужны.
    После покупки своей недвижимости, вы сможете добывать материалы, необходимые для постройки улучшений своего дома, которые смогут давать вам различные бонусы.


    Cписок недвижимости и цены:

        ⛺️Дырявая палатка - 450K💰 или 350💎
        🏚Ветхий сарай - 750К💰 или 550💎
        🏡Домик на дереве - 1.5М💰 или 750 💎
        🏠Вроде.. обычный дом...? - 3М💰 или 1000 💎"""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    checkHome = await db.Houses.get_or_none(owner=user.id)
    if checkHome:
        if checkHome.name == 'Дырявая палатка':
            if checkHome.buyfor == 'money':
                price = 135000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 105
                valute = '💎'
        elif checkHome.name == 'Ветхий сарай':
            if checkHome.buyfor == 'money':
                price = 225000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 165
                valute = '💎'
        elif checkHome.name == 'Домик на дереве':
            if checkHome.buyfor == 'money':
                price = 300000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 225
                valute = '💎'
        elif checkHome.name == 'Пентхаус':
            if checkHome.buyfor == 'money':
                price = 450000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 300
                valute = '💎'
            
        text += "\n\nВы можете продать свою текущую недвижимость за {}{}".format(price, valute)
        markup.add(InlineKeyboardButton('Продать {}'.format(checkHome.name), callback_data="houseSell"))
    markup.add(InlineKeyboardButton('Купить ⛺️Дырявая палатка', callback_data="houseBuy_1"))
    markup.add(InlineKeyboardButton('Купить 🏚Ветхий сарай', callback_data="houseBuy_2"))
    markup.add(InlineKeyboardButton('Купить 🏡Домик на дереве', callback_data="houseBuy_3"))
    markup.add(InlineKeyboardButton('Купить 🏠Вроде.. обычный дом...?', callback_data="houseBuy_4"))
    markup.add(InlineKeyboardButton('Вернуться на площадь', callback_data="nav_bigcity_centr"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def houseSell(call, user):
    checkHome = await db.Houses.get_or_none(owner=user.id)
    if checkHome:
        if checkHome.name == 'Дырявая палатка':
            if checkHome.buyfor == 'money':
                price = 135000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 105
                valute = '💎'
        elif checkHome.name == 'Ветхий сарай':
            if checkHome.buyfor == 'money':
                price = 225000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 165
                valute = '💎'
        elif checkHome.name == 'Домик на дереве':
            if checkHome.buyfor == 'money':
                price = 500000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 225
                valute = '💎'
        elif checkHome.name == 'Пентхаус':
            if checkHome.buyfor == 'money':
                price = 1000000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 300
                valute = '💎'
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Я передумал', callback_data="JiAlley"))
        markup.add(InlineKeyboardButton('Я передумал', callback_data="JiAlley"))
        markup.add(InlineKeyboardButton('Я передумал', callback_data="JiAlley"))
        markup.add(InlineKeyboardButton('Продать {}'.format(checkHome.name), callback_data="HOUSESELLCONFIRM"))
        markup.add(InlineKeyboardButton('Я передумал', callback_data="JiAlley"))
        await bot.edit_message_text("Вы ТОЧНО хотите продать {} за {}{}? Отменить действие будет невозможно.".format(checkHome.name, price, valute), call.message.chat.id, call.message.message_id, reply_markup=markup)

async def HOUSESELLCONFIRM(call,user):
    checkHome = await db.Houses.get_or_none(owner=user.id)
    if checkHome:
        if checkHome.name == 'Дырявая палатка':
            if checkHome.buyfor == 'money':
                price = 135000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 105
                valute = '💎'
        elif checkHome.name == 'Ветхий сарай':
            if checkHome.buyfor == 'money':
                price = 225000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 165
                valute = '💎'
        elif checkHome.name == 'Домик на дереве':
            if checkHome.buyfor == 'money':
                price = 500000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 225
                valute = '💎'
        elif checkHome.name == 'Пентхаус':
            if checkHome.buyfor == 'money':
                price = 1000000
                valute = '💰'
            elif checkHome.buyfor == 'almaz':
                price = 300
                valute = '💎'
        await db.Houses.filter(id=checkHome.id).delete()
        if valute == '💎':
            await db.Users.filter(id=user.id).update(almaz=F('almaz') + price)
        else:
            await db.Users.filter(id=user.id).update(money=F('money') + price)
        await bot.edit_message_text("Недвижимость успешно продана.", call.message.chat.id, call.message.message_id)
        await logBot.send_message(tradeChat, "Игрок {} ({}) продал {} за {}{}".format(user.username, user.id, checkHome.name, price,valute))



async def houseBuy(call, user):
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[1]
    checkHome = await db.Houses.get_or_none(owner=user.id)
    if checkHome:
        await bot.edit_message_text("К сожалению, иметь можно только один дом",call.message.chat.id, call.message.message_id)
        return
    if navWhere == '1':
        try:
            valute = nav[2]
            if valute == 'gold':
                if user.money >= 450000:
                    user.money -= 450000
                    await db.Users.filter(id=user.id).update(money=user.money)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Дырявую палатку за голду".format(user.username, user.id))
                    newHouse = await db.Houses(name='Дырявая палатка', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='money')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку ⛺️Дырявой палатки! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
            elif valute == 'kri':
                if user.almaz >= 350:
                    user.almaz -= 350
                    await db.Users.filter(id=user.id).update(almaz=user.almaz)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Дырявую палатку за кристаллы".format(user.username, user.id))
                    newHouse = await db.Houses(name='Дырявая палатка', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='almaz')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку ⛺️Дырявой палатки! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
        except:
            print(call.data)
            leftTime = int((1624167556 - time.time()) / 86400)
            text = "Выберите валюту, которой желаете расплатиться. Сумма снимется с вашего счёта и вы получите свою недвижимость!"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('350К 💰', callback_data="houseBuy_1_gold"))
            markup.add(InlineKeyboardButton('350 💎', callback_data="houseBuy_1_kri"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    if navWhere == '2':
        try:
            valute = nav[2]
            if valute == 'gold':

                if user.money >= 750000:
                    user.money -= 750000
                    await db.Users.filter(id=user.id).update(money=user.money)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Ветхий сарай за голду".format(user.username, user.id))
                    newHouse = await db.Houses(name='Ветхий сарай', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='money')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏚Ветхий сарай! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
            elif valute == 'kri':
                if user.almaz >= 550:
                    user.almaz -= 550
                    await db.Users.filter(id=user.id).update(almaz=user.almaz)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Ветхий сарай за кристаллы".format(user.username, user.id))
                    newHouse = await db.Houses(name='Ветхий сарай', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='almaz')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏚Ветхий сарай! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
        except:
            print(call.data)
            leftTime = int((1624167556 - time.time()) / 86400)
            text = "Выберите валюту, которой желаете расплатиться. Сумма снимется с вашего счёта и вы получите свою недвижимость!"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('750К 💰', callback_data="houseBuy_2_gold"))
            markup.add(InlineKeyboardButton('550 💎', callback_data="houseBuy_2_kri"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


    if navWhere == '3':
        try:
            valute = nav[2]
            if valute == 'gold':
                if user.money >= 1500000:
                    user.money -= 1500000
                    await db.Users.filter(id=user.id).update(money=user.money)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Домик на дереве за голду".format(user.username, user.id))
                    newHouse = await db.Houses(name='Домик на дереве', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='money')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏡Домик на дереве! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
            elif valute == 'kri':
                if user.almaz >= 750:
                    user.almaz -= 750
                    await db.Users.filter(id=user.id).update(almaz=user.almaz)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Домик на дереве за кристаллы".format(user.username, user.id))
                    newHouse = await db.Houses(name='Домик на дереве', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='almaz')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏡Домик на дереве! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
        except:
            print(call.data)
            leftTime = int((1624167556 - time.time()) / 86400)
            text = "Выберите валюту, которой желаете расплатиться. Сумма снимется с вашего счёта и вы получите свою недвижимость!"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1.5М 💰', callback_data="houseBuy_3_gold"))
            markup.add(InlineKeyboardButton('750 💎', callback_data="houseBuy_3_kri"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    if navWhere == '4':
        try:
            valute = nav[2]
            if valute == 'gold':
                if user.money >= 3000000:
                    user.money -= 3000000
                    await db.Users.filter(id=user.id).update(money=user.money)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Пентхаус за голду".format(user.username, user.id))
                    newHouse = await db.Houses(name='Пентхаус', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='money')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏠Вроде.. обычный дом...?! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
            elif valute == 'kri':
                if user.almaz >= 1000:
                    user.almaz -= 1000
                    await db.Users.filter(id=user.id).update(almaz=user.almaz)
                    await logBot.send_message(tradeChat, "Игрок {} ({}) купил Пентхаус за кристаллы".format(user.username, user.id))
                    newHouse = await db.Houses(name='Пентхаус', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='almaz')
                    await newHouse.save()
                    await bot.edit_message_text("Поздравляем, вы оформили покупку 🏠Вроде.. обычный дом...?! Вот ваши ключи. Попасть в свой дом вы можете через универсальный телепорт в ключах.\n\nИспользуйте /home", call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("У вас недостаточно средств", call.message.chat.id, call.message.message_id)
        except:
            print(call.data)
            leftTime = int((1624167556 - time.time()) / 86400)
            text = "Выберите валюту, которой желаете расплатиться. Сумма снимется с вашего счёта и вы получите свою недвижимость!"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('3М💰', callback_data="houseBuy_4_gold"))
            markup.add(InlineKeyboardButton('1000 💎', callback_data="houseBuy_4_kri"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

kdTp = {}

async def myHouse(m, user):
    eliteHouses = ['Домик на дереве', 'Пентхаус']
    if m.chat.id != m.from_user.id: return
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    checkHouse = await db.Houses.exists(owner=user.id)
    if checkHouse:
        house = await db.Houses.get(owner=user.id)
        needExp = house.lvl * 100
        text = """{}. Владелец: {}

    🔆Уровень: {}
    Опыт: ✨{}/{}
    Материалы: {}🌳 {}🪨


⚡️Врата телепортации активированы""".format(house.name, user.username, house.lvl, house.exp, needExp, house.woods, house.stones)
        if user.location == 'Дом':
            text += "\n⚡️Аура восстановления активирована"
            markup.add(InlineKeyboardButton('Телепортация в Хэвенбург', callback_data="house_tpHeaven"))
        else:
            if house.name == 'Дырявая палатка': kdTime = 7200
            elif house.name == 'Ветхий сарай': kdTime = 3600
            elif house.name == 'Домик на дереве': kdTime = 1800
            else: kdTime = 0
            if m.from_user.id in kdTp and int(kdTp[m.from_user.id]) + kdTime >= int(time.time()):
                leftTime = (int(kdTp[m.from_user.id]) + kdTime - int(time.time())) / 60
                markup.add(InlineKeyboardButton('Телепортироваться домой (КД: {} мин)'.format(int(leftTime)), callback_data="house_tpHome"))
            else:
                markup.add(InlineKeyboardButton('Телепортироваться домой', callback_data="house_tpHome"))
        markup.add(InlineKeyboardButton('Улучшения', callback_data="house_upgrades"))
        if house.lvl < 5:
            text += "\n⚠️Склад (Позволяет хранить предметы в доме) станет доступен на 5 уровне"
        else:
            markup.add(InlineKeyboardButton('Склад', callback_data="house_inventory"))
        if house.lvl < 10 and house.name in eliteHouses: text += "\n⚠️Кухня, необходим 10 уровень" # Кухня
        elif house.lvl >= 10 and house.name in eliteHouses:
            markup.add(InlineKeyboardButton('Кухня', callback_data="Kitchen"))
        if house.lvl < 15 and house.name in eliteHouses: text += "\n⚠️Аура добытчика (Повышает получаемое золото с монстров) станет доступна на 15 уровне"
        
        if house.name == "Дырявая палатка" and house.lvl >= 5:
            markup.add(InlineKeyboardButton('Улучшить до 🏚Ветхий сарай', callback_data="house_upgrade"))
        elif house.name == "Ветхий сарай" and house.lvl >= 5:
            markup.add(InlineKeyboardButton('Улучшить до 🏡Домик на дереве', callback_data="house_upgrade"))
        elif house.name == "Домик на дереве" and house.lvl >= 5:
            markup.add(InlineKeyboardButton('Улучшить до 🏠Вроде.. обычный дом...?', callback_data="house_upgrade"))

        await bot.send_message(m.chat.id, text, reply_markup=markup)


async def house(call, user):
    eliteHouses = ['Домик на дереве', 'Пентхаус']
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    checkHouse = await db.Houses.exists(owner=user.id)
    if checkHouse:
        house = await db.Houses.get(owner=user.id)
        nav = call.data.split('_')
        navWhere = nav[1]
        if navWhere == 'tpHome':
            if house.name == 'Дырявая палатка': kdTime = 7200
            elif house.name == 'Ветхий сарай': kdTime = 3600
            elif house.name == 'Домик на дереве': kdTime = 1800
            else: kdTime = 0
            if call.from_user.id in kdTp and int(kdTp[call.from_user.id]) + kdTime >= int(time.time()):
                leftTime = (int(kdTp[call.from_user.id]) + kdTime - int(time.time())) / 60
                await bot.edit_message_text("Телепорт еще не готов. До возобновления {} мин".format(int(leftTime)), call.message.chat.id, call.message.message_id)
                return
            if call.from_user.id in buzyUsrsPvP and buzyUsrsPvP[call.from_user.id] == 1: return await bot.edit_message_text("Как можно использовать телепорт, требующий огромной концентрации, когда у тебя битва?!", call.message.chat.id, call.message.message_id)
            if user.quest == 'Искатель приключений' and user.questStatus == 1 and user.location != 'Песчаная пирамида':
                progSplit = user.progLoc.split("|")
                num = progSplit[1]
                quest = await db.tempQuest.get_or_none(user_id=user.user_id, quest=user.quest, status=0).first()
                if quest:
                    quest.progress += int(num)
                    await db.tempQuest.filter(user_id=user.user_id, quest=user.quest, status=0).update(progress=quest.progress)
            await db.Users.filter(id=user.id).update(location='Дом', battleStatus=0)
            kdTp[call.from_user.id] = int(time.time())
            await bot.edit_message_text("Вы успешно телепортировались к себе в дом", call.message.chat.id, call.message.message_id)
            needExp = house.lvl * 100
            text = """{}. Владелец: {}

        🔆Уровень: {}
        Опыт: ✨{}/{}
        Материалы: {}🌳 {}🪨


    ⚡️Врата телепортации активированы""".format(house.name, user.username, house.lvl, house.exp, needExp, house.woods, house.stones)
            text += "\n⚡️Аура восстановления активирована"
            markup.add(InlineKeyboardButton('Телепортация в Хэвенбург', callback_data="house_tpHeaven"))
            markup.add(InlineKeyboardButton('Улучшения', callback_data="house_upgrades"))
            if house.lvl < 5:
                text += "\n⚠️Склад (Позволяет хранить предметы в доме) станет доступен на 5 уровне"
            else:
                markup.add(InlineKeyboardButton('Склад', callback_data="house_inventory"))
            if house.lvl < 10 and house.name in eliteHouses: text += "\n⚠️Кухня, необходим 10 уровень" # Кухня
            elif house.lvl >= 10 and house.name in eliteHouses:
                markup.add(InlineKeyboardButton('Кухня', callback_data="Kitchen"))
            if house.lvl < 15 and house.name in eliteHouses: text += "\n⚠️Аура добытчика (Повышает получаемое золото с монстров) станет доступна на 15 уровне"
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)

        elif navWhere == 'tpHeaven':
            if call.from_user.id in buzyUsrsPvP and buzyUsrsPvP[call.from_user.id] == 1: return await bot.edit_message_text("Как можно использовать телепорт, требующий огромной концентрации, когда у тебя битва?!", call.message.chat.id, call.message.message_id)
            if user.location == 'Дом':
                if user.quest == 'Искатель приключений' and user.questStatus == 1 and user.location != 'Песчаная пирамида':
                    progSplit = user.progLoc.split("|")
                    num = progSplit[1]
                    quest = await db.tempQuest.get_or_none(user_id=user.user_id, quest=user.quest, status=0).first()
                    if quest:
                        quest.progress += int(num)
                        await db.tempQuest.filter(user_id=user.user_id, quest=user.quest, status=0).update(progress=quest.progress)
                await db.Users.filter(id=user.id).update(location='Хэвенбург', position='Площадь')
                await bot.edit_message_text("Вы успешно телепортировались на площадь Хэвенбурга", call.message.chat.id, call.message.message_id)
        elif navWhere == 'upgrades':
            text = "Улучшения дома. Доступные:" 
            needWoods = int(house.regenerate * 20) #Это для регенерации
            needStones = int(house.regenerate * 10) #Это для регенерации
            text += "\n\nАура восстановления ({} lvl) - {}🌳 {}🪨".format(house.regenerate, needWoods, needStones)
            if needWoods <= house.woods and needStones <= house.stones:
                markup.add(InlineKeyboardButton('Улучшить ауру восстановления', callback_data="home_upgrade_regenerate"))
            if house.lvl >= 5:
                needWoods = int(house.inventory * 25) #Это для инвентаря
                needStones = int(house.inventory * 35) #Это для инвентаря
                text += "\n\nСклад ({} lvl) - {}🌳 {}🪨".format(house.inventory, needWoods, needStones)
                if needWoods <= house.woods and needStones <= house.stones:
                    markup.add(InlineKeyboardButton('Улучшить склад', callback_data="home_upgrade_inventory"))
            if house.lvl >= 15 and house.name in eliteHouses:
                needWoods = int(house.plusGold * 25) #Это для бонуса голды
                needStones = int(house.plusGold * 35) #Это для бонуса голды
                text += "\n\nАура добытчика ({} lvl) - {}🌳 {}🪨".format(house.plusGold, needWoods, needStones)
                if needWoods <= house.woods and needStones <= house.stones:
                    markup.add(InlineKeyboardButton('Улучшить ауру добытчика', callback_data="home_upgrade_plusGold"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'inventory':
            currentSize = await db.getHouseInventorySize(user)
            text = "Склад. 📦{}/{}\n".format(currentSize, house.inventory)
            checkItem = await db.Inventory.exists(active=10, idplayer=user.id)
            if checkItem > 0:
                inventory = await db.Inventory.filter(idplayer=user.id, active=10)
                for z in inventory:
                    text += "\n{} - /inventory_take_{}".format(z.name, z.id)
            else:
                text += "Склад пока пустует. Выберите предмет из инвентаря, который хотите тут оставить."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'upgrade':
            text = "Улучшение дома обнулит текущий 🔆Уровень дома, имеющиеся материалы и улучшения, однако откроет новые возможности. Вы уверены?"
            markup.add(InlineKeyboardButton('Да', callback_data="houseUpgrade_yes"))
            markup.add(InlineKeyboardButton('Нет, отменить действие', callback_data="houseUpgrade_not"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)



async def houseUpgrade_(call, user):
    checkHouse = await db.Houses.exists(owner=user.id)
    if checkHouse:
        house = await db.Houses.get(owner=user.id)
        if call.data.split("_")[1] == 'yes':
            
            if house.name == "Дырявая палатка" and house.lvl >= 5:
                await logBot.send_message(tradeChat, "Игрок {} ({}) улучшил ⛺️Дырявая палатка до 🏚Ветхий сарай".format(user.username, user.id))
                newHouse = await db.Houses(name='Ветхий сарай', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='gold')
                await newHouse.save()
                await db.Houses.filter(id=house.id).delete()
                text = "Улучшение дома прошло успешно!"
            elif house.name == "Ветхий сарай" and house.lvl >= 5:
                await logBot.send_message(tradeChat, "Игрок {} ({}) улучшил 🏚Ветхий сарай до 🏡Домик на дереве".format(user.username, user.id))
                newHouse = await db.Houses(name='Домик на дереве', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='gold')
                await newHouse.save()
                await db.Houses.filter(id=house.id).delete()
                text = "Улучшение дома прошло успешно!"
            elif house.name == "Домик на дереве" and house.lvl >= 5:
                await logBot.send_message(tradeChat, "Игрок {} ({}) улучшил 🏡Домик на дереве до 🏠Пентхаус".format(user.username, user.id))
                newHouse = await db.Houses(name='Пентхаус', owner=user.id, arentLeft=500, woods=0, stones=0, lvl=1, exp=0, buyfor='gold')
                await newHouse.save()
                await db.Houses.filter(id=house.id).delete()
                text = "Улучшение дома прошло успешно!"
            else:
                text = "На данный момент улучшение дома недоступно. Возможно, дом уже максимально улучшен или у него нет 5 🔆Уровня?"

            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:

            await bot.edit_message_text("Действие отменено.", call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m:m.text and m.text.startswith('/inventory_take_'))
async def inventory_take_(m): 
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id)
        if user and user.location == "Дом":
            home = await db.Houses.get_or_none(owner=user.id)
            if home:
                itemId = m.text.replace("/inventory_take_", "", 1)
                checkItem = await db.Inventory.get_or_none(id=itemId)
                if checkItem and checkItem.active==10 and checkItem.idplayer==user.id:
                    size = await db.items(name=checkItem.name, check='size')
                    inventorySize = await db.getInventorySize(user)
                    if inventorySize + size <= user.inventorySizeMax:
                        await db.Inventory.filter(id=itemId).update(active=1)
                        await bot.send_message(m.chat.id, "Ты успешно забрал {} со склада.".format(checkItem.name))
                    else:
                        await bot.send_message(m.chat.id, "Не хватает места в инвентаре")


async def home(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    checkHouse = await db.Houses.exists(owner=user.id)
    if checkHouse:
        house = await db.Houses.get(owner=user.id)
        nav = call.data.split('_')
        navWhere = nav[1]
        if navWhere == 'upgrade':
            What = nav[2]
            if What == 'regenerate':
                if house.name == 'Дырявая палатка' and house.regenerate > 7:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Ветхий сарай' and house.regenerate > 10:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Домик на дереве' and house.regenerate > 15:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Пентхаус' and house.regenerate > 20:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                needWoods = int(house.regenerate * 20) #Это для регенерации
                needStones = int(house.regenerate * 10) #Это для регенерации
                if needWoods <= house.woods and needStones <= house.stones:
                    maxExp = int((house.lvl + house.regenerate) * 10)
                    minExp = int(house.lvl * 2)
                    randomExp = random.randint(minExp, maxExp)
                    if house.exp + randomExp > house.lvl * 100:
                        newExp = 0
                        newLvl = house.lvl + 1
                        toText = "+1 🔆"
                    else:
                        newExp = house.exp + randomExp
                        toText = "+{} ✨".format(randomExp)
                        newLvl = house.lvl
                    await db.Houses.filter(id=house.id).update(woods=F('woods') - needWoods, stones=F('stones') - needStones, regenerate=F('regenerate') + 1, exp=newExp, lvl=newLvl)
                    await bot.edit_message_text("Вы успешно улучшили систему регенерации в своём доме\n\n{}".format(toText), call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("Недостаточно материалов", call.message.chat.id, call.message.message_id)
            elif What == 'inventory':
                if house.name == 'Дырявая палатка' and house.inventory > 10:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Ветхий сарай' and house.inventory > 20:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Домик на дереве' and house.inventory > 30:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Пентхаус' and house.inventory > 50:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                needWoods = int(house.inventory * 25) #Это для инвентаря
                needStones = int(house.inventory * 35) #Это для инвентаря
                if needWoods <= house.woods and needStones <= house.stones:
                    maxExp = int((house.lvl + house.inventory) * 7)
                    minExp = int(house.lvl * 2)
                    randomExp = random.randint(minExp, maxExp)
                    if house.exp + randomExp > house.lvl * 100:
                        newExp = 0
                        newLvl = house.lvl + 1
                        toText = "+1 🔆"
                    else:
                        newExp = house.exp + randomExp
                        newLvl = house.lvl
                        toText = "+{} ✨".format(randomExp)
                    await db.Houses.filter(id=house.id).update(woods=F('woods') - needWoods, stones=F('stones') - needStones, inventory=F('inventory') + 1, exp=newExp, lvl=newLvl)
                    await bot.edit_message_text("Вы успешно улучшили склад в своём доме\n\n{}".format(toText), call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("Недостаточно материалов", call.message.chat.id, call.message.message_id)
            elif What == 'plusGold':
                if house.name == 'Дырявая палатка' and house.plusGold > 5:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Ветхий сарай' and house.plusGold > 10:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Домик на дереве' and house.plusGold > 15:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                elif house.name == 'Пентхаус' and house.plusGold > 20:
                    await bot.edit_message_text("К сожалению, данное улучшение для вашего типа дома больше недоступно.", call.message.chat.id, call.message.message_id)
                    return
                needWoods = int(house.plusGold * 25) #Это для бонуса голды
                needStones = int(house.plusGold * 35) #Это для бонуса голды
                if needWoods <= house.woods and needStones <= house.stones:
                    maxExp = int((house.lvl + house.plusGold) * 4)
                    minExp = int(house.lvl * 2)
                    randomExp = random.randint(minExp, maxExp)
                    if house.exp + randomExp > house.lvl * 100:
                        newExp = 0
                        newLvl = house.lvl + 1
                        toText = "+1 🔆"
                    else:
                        newExp = house.exp + randomExp
                        newLvl = house.lvl
                        toText = "+{} ✨".format(randomExp)
                    await db.Houses.filter(id=house.id).update(woods=F('woods') - needWoods, stones=F('stones') - needStones, plusGold=F('plusGold') + 1, exp=newExp, lvl=newLvl)
                    await bot.edit_message_text("Вы успешно улучшили ауру добытика\n\n{}".format(toText), call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("Недостаточно материалов", call.message.chat.id, call.message.message_id)



async def Kitchen(call, user):
    checkKitchenGuide = await db.Inventory.exists(name='Kitchen guide', idplayer=user.id)
    if not checkKitchenGuide:
        text = """Заходя на кухню:
        
        - КУХНЯ! Идеальное место для медитации и... готовки. Именно здесь создаются шедевры, которые завоёвывают страны, а иногда и весь мир!

Кто это говорит? Оглянувшись, замечаешь странное существо, сидящее в углу. ТЕНТА..?
    
    - Добро пожаловать к себе на кухню. Первое время ты будешь проклинать это место, но не переживай - это ненадолго. Предлагаю изучить азы готовки... Готов?

Ты кивнул, ожидая продолжения
    
    - Я научу тебя готовке, смотри внимательно.

Существо неистово машет щупальцами, добавляет не подписанные ингредиенты, показывает цыганские фокусы и блюдо готово.
    
    - Очень главное поднимать свой опыт готовки чтобы ты мог лучше управляться с готовкой и готовить еще больше вкуснейших блюд! Запомнил как делается это? 

Конечно же ты ничего не запомнил.
    
    - С таким хреновым учеником мне и делать тут нечего... В любом случае, вот. Это базовые рецепты блюд которые сможет сварганить даже трёхлетний ребёнок. Не теряй! Остальные сам разгадывай...

Испаряясь, старик успел бросить тебе Священный (во всяком случае, так было для тебя) листок и рецептами блюд.

⚠️Открыта кухня. Добывайте ингредиенты в локациях, покупайте у игроков и экспериментируйте!
⚠️Открыт навык готовки. Готовьте и набирайтесь опыта! Чем выше навык готовки тем лучше блюда вы сможете приготовить"""
        kitchenGuide = await db.Inventory(name='Kitchen guide', idplayer=user.id, type='Прочее', active=0)
        await kitchenGuide.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Взять яйца в кулак!', callback_data="Kitchen"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        await asyncio.sleep(15)
        newRecipy = await db.Recipes(name='Бульон курильщика', owner=user.id, source='kitchen')
        await newRecipy.save()
        newRecipy = await db.Recipes(name='Сашими', owner=user.id, source='kitchen')
        await newRecipy.save()
        newRecipy = await db.Recipes(name='Борщ', owner=user.id, source='kitchen')
        await newRecipy.save()
        newRecipy = await db.Recipes(name='Сила узбека', owner=user.id, source='kitchen')
        await newRecipy.save()
    else:
        text = "КУХЬНЯ! \n🌟Опыт готовки: {}\nДоступные рецепты (эффекты указаны за идеально приготвленные блюда, обычные дают в два раза меньше бонус):\n".format(user.cooker)
        allRecipies = await db.Recipes.filter(source='kitchen', owner=user.id)
        for recipe in allRecipies:
            if recipe.name == 'Бульон курильщика':
                text += "\n\nБульон курильщика. Последовательность приготовления: хабарик + телесные жидкости + любой ингредиент\nЭффект: восстанавливает 150 хп"
            elif recipe.name == 'Сашими':
                text += "\n\nСашими. Последовательность приготовления: Филе рыбы + лёд + любой ингредиент\nЭффект: восстанавливает 200 хп"
            elif recipe.name == 'Борщ':
                text += "\n\nБорщ. Последовательность приготовления: борщевик + прах + любой ингредиент\nЭффект: восстанавливает 250 хп"
            elif recipe.name == 'Сила узбека':
                text += "\n\nСила узбека. Последовательность приготовления: драугрские приправы + перемерзший рис + любой ингредиент\nЭффект: восстанавливает 300 хп"
            elif recipe.name == 'Пряная рыба с луком':
                text += "\n\n⭐️Пряная рыба с луком. Последовательность приготовления: филе рыбы + пряность + лук\nЭффект: восстанавливает 350 хп + дает 10% увеличение атаки (30 мин)"
            elif recipe.name == 'Манты с сюрпризом':
                text += "\n\n⭐️Манты с сюрпризом. Последовательность приготовления: прах + телесные жидкости + Съедобный CUMень\nЭффект: восстанавливает 350 хп + дает 10% увеличение защиты (30 мин)"
            elif recipe.name == 'Макарошки с кулером':
                text += "\n\n⭐️Макарошки с кулером. Последовательность приготовления: лед + соль + макароны\nЭффект: восстанавливает 350 хп + дает 5% увеличение шанса уклонения (30 мин)"
            elif recipe.name == 'Солевая сигарилла':
                text += "\n\n⭐️Солевая сигарилла. Последовательность приготовления: хабарик + соль + перо феникса\nЭффект: восстанавливает 350 хп + восстанавливает 350 хп + дает 5% увеличение шанса крит удара (30 мин)"
            elif recipe.name == 'Аль денте салат':
                text += "\n\n⭐️⭐️Аль денте салат. Последовательность приготовления: борщевик + кровь (не твоя) + шуба селедки\nЭффект: дает 30% увеличение атаки (60 мин)"
            elif recipe.name == 'Богатырский суп':
                text += "\n\n⭐️⭐️Богатырский суп. Последовательность приготовления: драугрские приправы + машинное масло + кошачья пыльца\nЭффект: дает 30% увеличения защиты (60 мин)"
            elif recipe.name == 'Онигири':
                text += "\n\n⭐️⭐️Онигири. Последовательность приготовления: перемерзший рис + CUMень + пот\nЭффект: дает 10% увеличение шанса уклонения (60 мин)"
            elif recipe.name == 'Собственно в соку':
                text += "\n\n⭐️⭐️Собственно в соку. Последовательность приготовления: телесные жидкости + акула без шубы + Пинус\nЭффект: дает 10% увеличение шанса крита удара (60 мин)"
            
            elif recipe.name == 'Подозрительная жидкость':
                text += "\n\n⭐️⭐️⭐️Подозрительная жидкость. Последовательность приготовления: чернила + фиолетовость + Сиф \nЭффект: дает 40% увеличение атаки + восстанавливает фулл хп (120 мин)"
            elif recipe.name == 'Зубная паста':
                text += "\n\n⭐️⭐️⭐️Зубная паста. Последовательность приготовления: макароны + Драконья чешуя + Немного магии\nЭффект: дает 40% увеличение защиты + восстанавливает фулл хп (120 мин)"
            elif recipe.name == 'Слёзы Сани':
                text += "\n\n⭐️⭐️⭐️Слёзы Сани. Последовательность приготовления: Лук + Саня + Водяной пистолет\nЭффект: дает 15% увеличение шанса уклонения + восстанавливает фулл хп (120 мин)"
            elif recipe.name == 'Жареный раком':
                text += "\n\n⭐️⭐️⭐️Жареный раком. Последовательность приготовления: Перо феникса + Рак + Ты\nЭффект: дает 15% увеличение шанса крита + восстанавливает фулл хп (120 мин)"
    
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Новая готовка', callback_data="kitchen_start"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)


async def kitchen_start(call, user):
    checkNow = await db.Crafts.exists(idplayer=user.id, active=1, type='kitchen')
    if checkNow:
        await db.Crafts.filter(idplayer=user.id, active=1).update(active=0)
    newCraft = await db.Crafts(idplayer=user.id, active=1, type='kitchen')
    await newCraft.save()
    inventory = await db.Inventory.filter(type__in=['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки'], idplayer=user.id, active=1).only('name', 'id')
    count = {}
    size1 = {}
    text = "Готовька!\nПервый предмет: (пусто)\nВторой предмет: (пусто)\nТретий предмет: (пусто)\n\nИнгредиенты в наличии:\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for item in inventory:
        if item.name in count:
            count[item.name] += 1
        else:
            count[item.name] = 1
            markup.add(InlineKeyboardButton('{}'.format(str(item.name)), callback_data="addKitchen_{}".format(str(item.id))))
    for dict in count:
        text += "\nх{} {}".format(count[dict], dict)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def addKitchen_(call, user):
    recipe = None
    itemId = call.data.split("_")[1]
    checkNow = await db.Crafts.exists(idplayer=user.id, active=1, type='kitchen')
    if checkNow:
        checkNow = await db.Crafts.get(idplayer=user.id, active=1, type='kitchen').first()
    else:
        checkNow = await db.Crafts(idplayer=user.id, active=1, type='kitchen')
        await checkNow.save()
    if not checkNow.firstItem:
        checkItem = await db.Inventory.get_or_none(id=itemId)
        if checkItem and checkItem.active == 1:
            checkNow.firstItem = checkItem.id
        else:
            await checkNow.delete()
            await bot.edit_message_text("Предмет не найден, кастрюли в сторону!", call.message.chat.id, call.message.message_id)
            return
    elif not checkNow.secondItem:
        checkItem = await db.Inventory.get_or_none(id=itemId)
        if checkItem and checkItem.active == 1:
            checkNow.secondItem = checkItem.id
        else:
            await checkNow.delete()
            await bot.edit_message_text("Предмет не найден, кастрюли в сторону!", call.message.chat.id, call.message.message_id)
            return
    else:
        checkItem = await db.Inventory.get_or_none(id=itemId)
        if checkItem and checkItem.active == 1:
            checkNow.thirdItem = checkItem.id
        else:
            await checkNow.delete()
            await bot.edit_message_text("Предмет не найден, кастрюли в сторону!", call.message.chat.id, call.message.message_id)
            return
        getFirstItem = await db.Inventory.get_or_none(id=checkNow.firstItem).first()
        getSecondItem = await db.Inventory.get_or_none(id=checkNow.secondItem).first()
        getThirdItem = await db.Inventory.get_or_none(id=checkNow.thirdItem).first()
        if getFirstItem and getFirstItem.active == 1 and getSecondItem and getSecondItem.active == 1 and getThirdItem and getThirdItem.active == 1:
            pass
        else:
            await bot.edit_message_text("Какого-то предмета не существует.", call.message.chat.id, call.message.message_id.id)
            return
        await bot.edit_message_text("Кастрюльки тарахтят, огонёк горит, что-то кипит...", call.message.chat.id, call.message.message_id)
        rand = 0
        if getFirstItem.name == 'Хабарик' and getSecondItem.name == 'Телесные жидкости':
            if user.cooker > 5:
                result = 'Бульон курильщика'
                recipe = 'Бульон курильщика'
                rarity = 0
            else:
                result = 'Нечто'
        
        elif getFirstItem.name == 'Филе рыбы' and getSecondItem.name == 'Лёд':
            if user.cooker > 10:
                result = 'Сашими'
                recipe = 'Сашими'
                rarity = 0
            else:
                result = 'Нечто'
        
        elif getFirstItem.name == 'Борщевик' and getSecondItem.name == 'Прах':
            if user.cooker > 15:
                result = 'Борщ'
                recipe = 'Борщ'
                rarity = 0
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Драугрские приправы' and getSecondItem.name == 'Перемерзший рис':
            if user.cooker > 20:
                result = 'Сила узбека'
                recipe = 'Сила узбека'
                rarity = 0
            else:
                result = 'Нечто'


        elif getFirstItem.name == 'Филе рыбы' and getSecondItem.name == 'Пряность' and getThirdItem.name == 'Лук':
            if user.cooker > 30:
                rand = random.randint(0, 100)
                num = user.cooker - 40
                if rand <= num: result = 'Идеальная пряная рыба с луком'
                else: result = 'Пряная рыба с луком'
                recipe = 'Пряная рыба с луком'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Прах' and getSecondItem.name == 'Телесные жидкости' and getThirdItem.name == 'Съедобный CUMень':
            if user.cooker > 40:
                rand = random.randint(0, 100)
                num = user.cooker - 50
                if rand <= num: result = 'Идеальные манты с сюрпризом'
                else: result = 'Манты с сюрпризом'
                recipe = 'Манты с сюрпризом'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Лёд' and getSecondItem.name == 'Соль' and getThirdItem.name == 'Макароны':
            if user.cooker > 50:
                rand = random.randint(0, 100)
                num = user.cooker - 60
                if rand <= num: result = 'Идеальные макарошки с кулером'
                else: result = 'Макарошки с кулером'
                recipe = 'Макарошки с кулером'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Хабарик' and getSecondItem.name == 'Соль' and getThirdItem.name == 'Перо феникса':
            if user.cooker > 60:
                rand = random.randint(0, 100)
                num = user.cooker - 70
                if rand <= num: result = 'Идеальная солевая сигарилла'
                else: result = 'Солевая сигарилла'
                recipe = 'Солевая сигарилла'
                rarity = 1
            else:
                result = 'Нечто'


        elif getFirstItem.name == 'Борщевик' and getSecondItem.name == 'Кровь (не твоя)' and getThirdItem.name == 'Шуба селедки':
            if user.cooker > 100:
                rand = random.randint(0, 100)
                num = user.cooker - 110
                if rand <= num: result = 'Идеальный аль денте салат'
                else: result = 'Аль денте салат'
                recipe = 'Аль денте салат'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Драугрские приправы' and getSecondItem.name == 'Машинное масло' and getThirdItem.name == 'Кошачья Пыльца':
            if user.cooker > 100:
                rand = random.randint(0, 100)
                num = user.cooker - 110
                if rand <= num: result = 'Идеальный богатырский суп'
                else: result = 'Богатырский суп'
                recipe = 'Богатырский суп'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Перемерзший рис' and getSecondItem.name == 'Съедобный CUMень' and getThirdItem.name == 'Пот':
            if user.cooker > 100:
                rand = random.randint(0, 100)
                num = user.cooker - 110
                if rand <= num: result = 'Идеальные онигири'
                else: result = 'Онигири'
                recipe = 'Онигири'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Телесные жидкости' and getSecondItem.name == 'Акула без шубы' and getThirdItem.name == 'Пинус':
            if user.cooker > 100:
                rand = random.randint(0, 100)
                num = user.cooker - 110
                if rand <= num: result = 'Идеальный собственно в соку'
                else: result = 'Собственно в соку'
                recipe = 'Собственно в соку'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Чернила' and getSecondItem.name == 'Фиолетовость' and getThirdItem.name == 'Сиф':
            if user.cooker > 200:
                rand = random.randint(0, 100)
                num = user.cooker - 210
                if rand <= num: result = 'Идеальная подозрительная жидкость'
                else: result = 'Подозрительная жидкость'
                recipe = 'Подозрительная жидкость'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Макароны' and getSecondItem.name == 'Драконья чешуя' and getThirdItem.name == 'Немного магии':
            if user.cooker > 300:
                rand = random.randint(0, 100)
                num = user.cooker - 310
                if rand <= num: result = 'Идеальная зубная паста'
                else: result = 'Зубная паста'
                recipe = 'Зубная паста'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Лук' and getSecondItem.name == 'Саня' and getThirdItem.name == 'Водяной пистолет':
            if user.cooker > 400:
                rand = random.randint(0, 100)
                num = user.cooker - 450
                if rand <= num: result = 'Идеальные слёзы Сани'
                else: result = 'Слёзы Сани'
                recipe = 'Слёзы Сани'
                rarity = 1
            else:
                result = 'Нечто'

        elif getFirstItem.name == 'Перо феникса' and getSecondItem.name == 'Рак' and getThirdItem.name == 'Ты':
            if user.cooker > 500:
                rand = random.randint(0, 100)
                num = user.cooker - 600
                if rand <= num: result = 'Идеальный жареный раком'
                else: result = 'Жареный раком'
                recipe = 'Жареный раком'
                rarity = 1
            else:
                result = 'Нечто'

        else:
            result = "Нечто"

        checkItem1 = await db.Inventory.get_or_none(id=getFirstItem.id, active=1).first()
        checkItem2 = await db.Inventory.get_or_none(id=getSecondItem.id, active=1).first()
        checkItem3 = await db.Inventory.get_or_none(id=getThirdItem.id, active=1).first()
        if checkItem1 and checkItem2 and checkItem3:
            pass
        else:
            return bot.edit_message_text("Ингридиент куда-то делся...", call.message.chat.id, call.message.message_id)
        success = await db.addItem(result, user, arg='1')

        if result == 'Нечто': plusCooker = 1
        elif rand and rand >= num or rarity == 0: plusCooker = 2
        elif rand and rand <= num: plusCooker = 3
        else: plusCooker = 2
        await db.Users.filter(id=user.id).update(cooker=F('cooker') + plusCooker)
        getFirstItem.active = 0
        getSecondItem.active = 0
        getThirdItem.active = 0
        await getFirstItem.save()
        await getSecondItem.save()
        await getThirdItem.save()
        checkNow.active = 2
        await checkNow.save()
        plusText = ""
        print(recipe)
        if recipe:
            print('passRecipeIf')
            checkRecipy = await db.Recipes.exists(name=recipe, owner=user.id, source='kitchen')
            if checkRecipy: pass
            else:
                print('passRecipeElse')
                newRecipy = await db.Recipes(name=recipe, owner=user.id, source='kitchen')
                await newRecipy.save()
                plusText = "\n\nДоступен новый рецепт."
        await asyncio.sleep(5)
        await bot.send_message(user.user_id, "Наконец, блюдо готово! С нетерпением открываешь крышку кастрюли и обнаруживаешь... {}!{}".format(result, plusText))
        await achprog(user, ach='kitchen')
        return
    await checkNow.save()
    firstItem = await db.Inventory.get_or_none(id=checkNow.firstItem)
    secondItem = await db.Inventory.get_or_none(id=checkNow.secondItem)
    thirdItem = await db.Inventory.get_or_none(id=checkNow.thirdItem)
    inventory = await db.Inventory.filter(type__in=['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки'], idplayer=user.id, active=1).only('name', 'id')
    count = {}
    size1 = {}
    text = "Готовька!\n"
    if firstItem:
        text += "Первый предмет: {}\n".format(firstItem.name)
    if secondItem:
        text += "Второй предмет: {}\n".format(secondItem.name)
    if thirdItem:
        text += "Третий предмет: {}\n".format(thirdItem.name)
    text += "\n\nИнгредиенты в наличии:\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for item in inventory:
        if item.name in count:
            count[item.name] += 1
        else:
            if checkNow.firstItem and item.id == checkNow.firstItem or checkNow.secondItem and item.id == checkNow.secondItem or checkNow.thirdItem and item.id == checkNow.thirdItem: pass
            else:
                count[item.name] = 1
                markup.add(InlineKeyboardButton('{}'.format(str(item.name)), callback_data="addKitchen_{}".format(str(item.id))))
    for dict in count:
        text += "\nх{} {}".format(count[dict], dict)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
