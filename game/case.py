async def case(item, user):
    rand = random.randint(1, 100)
    if item.name == 'Маленький сундучок':
        armorset = ['Хоккейная маска', 'Кожаный нагрудник', 'Кожаные штаны', 'Берцы', 'Нижнее бельё Раскуловой']
        eat = ['Лучше не спрашивай', 'Большой хер огра', 'Малое зелье восстановления']
        last = 'Положительный тест на беременность'
    elif item.name == 'Шкатулка Кефира':
        armorset = ['Шляпа фокусника', 'Комбинезон сталкера', 'Нижнее бельё Раскуловой', 'Кросы адидас']
        eat = ['Лучше не спрашивай', 'Большой хер огра', 'Малое зелье восстановления']
        last = 'Детектор аномалий'
    elif item.name == 'Огромный сундук':
        armorset = ['Кепка адидас', 'Ночнушка Раскуловой', 'Нижнее бельё Раскуловой', 'Туфельки Раскуловой']
        eat = ['Лучше не спрашивай', 'Большой хер огра', 'Среднее зелье восстановления']
        last = 'Рецепт приготовления малого зелья восстановления'
    elif item.name == 'Ashot case':
        armorset = ['Кожаный шлем', 'Бронежилет', 'Спортивки адидас', 'Кожаные ботинки', 'Нижнее бельё Раскуловой']
        eat = ['Шаурма', 'Двойная шаурма']
        last = 'Рецепт приготовления среднего зелья восстановления'
    elif item.name == 'Опустошенный сундук':
        armorset = ['Горная шапка', 'Жилет скалолаза', 'Короткие шорты', 'Горные кроссовки', 'Нижнее бельё Раскуловой']
        eat = ['Он называет это "яблоко"']
        last = 'Детектор аномалий'
    elif item.name == 'Сундук щитоносцев':
        rand = random.randint(1, 100)
        if rand <= 22:
            winnerItem = 'Крышка от мусорника'
        elif rand <= 41:
            winnerItem = 'Покрышка со свалки'
        elif rand <= 57:
            winnerItem = 'Деревянный щит'
        elif rand <= 70:
            winnerItem = 'Щит охранника'
        elif rand <= 80:
            winnerItem = 'Щит покорителя Шаи-Хулуда'
        elif rand <= 88:
            winnerItem = 'Железный щит'
        elif rand <= 94:
            winnerItem = 'Щит бомжа'
        elif rand <= 99:
            winnerItem = 'Золотая покрышка'
        elif rand == 100:
            winnerItem = 'Щит верности Раскуловой'
        success = await db.addItem(winnerItem, user)
        name, size, bonus, atk_block, expires = await db.items(winnerItem, check=True)
        if success == False:
            item.active = 1
            await item.save()
            text = "У вас не хватает места в инвентаре."
            return text
        else:
            text = "Применив самые современные приспособления по вскрытию этих таинственных сундуков, ты наконец распахнул этот кейс. Точнее, то что от него осталось после монотонного битья молотком.\nВнутри ты нашёл{}".format(name)
        item.active = 0
        await item.save()
        await achprog(user, ach='cases')
        return text
    elif item.name == 'Амфора экстренной помощи':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Еда', callback_data="extraCase_eat"))
        markup.add(InlineKeyboardButton('Зелье здоровья', callback_data="extraCase_heal"))
        markup.add(InlineKeyboardButton('Свиток телепортации', callback_data="extraCase_tp"))
        text = "_Потерев эту штуковину, ты призвал джина, который предоставляет тебе три вещи на выбор совершенно бесплатно:_"
        user = await db.Users.get(id=item.idplayer)
        await bot.send_message(user.user_id, text, reply_markup=markup, parse_mode='markdown')
        text = "Потереть..."
        return text
    elif item.name == 'Аптечка':
        armorset = ['Колпак главврача', 'Халат главрача', 'Штаны главврача', 'Тапочки главврача']
        moneyBonus = random.randint(10, 35)
        user = await db.Users.get(id=item.idplayer)
        user.money += moneyBonus
        await user.save()
        armor = random.choice(armorset)
        success = await db.addItem(armor, user)
        name, size, bonus, atk_block, expires = await db.items(armor, check=True)
        if success == False:
            item.active = 1
            await item.save()
            text = "У вас не хватает места в инвентаре. Открыть аптечку не получится."
            return text
        else:
            text = "*Распахнув сумку с красным крестом, ты обнаружил*\n{}".format(name)
        item.active = 0
        await item.save()
        success = await db.addItem('Успокаивающее', user)
        name, size, bonus, atk_block, expires = await db.items('Успокаивающее', check=True)
        if success == False:
            item.active = 1
            await item.save()
            text += "У вас не хватает места в инвентаре. Открыть аптечку не получится."
            return text
        else:
            text += "\n{}".format(name)
        text += "\n💰{}".format(moneyBonus)
        item.active = 0
        await item.save()
        await achprog(user, ach='cases')
        return text
    elif item.name == 'Сун-дук':
        user = await db.Users.get(id=item.idplayer)
        armorset = ['Шлем из фольги', 'Майка из пакета', 'Модные штаны', 'НЕкроссовки']
        winnerItem = random.choice(armorset)
        success = await db.addItem(winnerItem, user)
        name, size, bonus, atk_block, expires = await db.items(winnerItem, check=True)
        if success == False:
            item.active = 1
            await item.save()
            text = "У вас не хватает места в инвентаре. Открыть сун-дук не получится."
            return text
        else:
            text = "Вы открыли сун-дук. Внутри вы нашли {}".format(name)
        item.active = 0
        await item.save()
        return text
    elif item.name == 'Схрон сталкера':
        if item.active != 1: return
        await item.delete()
        user = await db.Users.get(id=item.idplayer)
        if int(time.time()) >= item.expires:
            newHp = int(user.nowhp / 2)
            text = "Открыв сундук, на тебя дыхнуло облачко пыли... Радиационной. Увы, радиация разъела то что находилось внутри рюкзака\n\n- {}❤️".format(newHp)
            await db.Users.filter(id=user.id).update(nowhp=newHp)
        else:
            rand = random.randint(1, 100)
            if rand >= 80:
                randomItems = ['Палка-копалка', 'Камень обыкновенный', 'Кусок металлолома', 'Айрис', 'Каменный цветок', 'Ситенка', 'Камень Андриколь']
                item = random.choice(randomItems)
                randomLvl = random.randint(1, 4)
                success = await db.addArt(item, user, randomLvl)
                if success:
                    text = "Открыв схрон с помощью танцев с бубном и любимой работы молотком, внутри ты обнаружил {} {} уровня.".format(item, randomLvl)
                else:
                    newHp = int(user.nowhp / 2)
                    text = "Открыв сундук, на тебя дыхнуло облачко пыли... Радиационной. Увы, радиация разъела то что находилось внутри рюкзака\n\n- {}❤️".format(newHp)
                    await db.Users.filter(id=user.id).update(nowhp=newHp)
            else:
                success = await db.addItem('Детектор аномалий', user)
                if success == True:
                    text = "Открыв схрон с помощью танцев с бубном и любимой работы молотком, внутри ты обнаружил детектор аномалий."
                else:
                    newHp = int(user.nowhp / 2)
                    text = "Открыв сундук, на тебя дыхнуло облачко пыли... Радиационной. Увы, радиация разъела то что находилось внутри рюкзака\n\n- {}❤️".format(newHp)
                    await db.Users.filter(id=user.id).update(nowhp=newHp)
        return text
    item.active = 0
    await item.save()
    if rand <= 15:
        winnerItem = random.choice(armorset)
    elif rand > 15 and rand <= 30:
        winnerItem = random.choice(eat)
    elif rand > 30 and rand <= 40:
        winnerItem = last
    else:
        winnerItem = 'Ничего'
    user = await db.Users.get(id=item.idplayer)
    text = "Применив самые современные приспособления по вскрытию этих таинственных сундуков, ты наконец распахнул этот кейс. Точнее, то что от него осталось после монотонного битья молотком."
    if winnerItem != 'Ничего':
        success = await db.addItem(winnerItem, user)
        if success == False:
            item.active = 1
            await item.save()
            text = "У вас не хватает места в инвентаре. Открыть сундук не получится."
            return text
        name, size, bonus, atk_block, expires = await db.items(winnerItem, check=True)
        text += "\nВнутри сундука ты нашёл {}".format(name)
    else:
        await db.addItem('Останки героев', user, arg='1')
        text += "\nК сожалению, внутри ты ничего, полезного для себя, не обнаружил... Если тебе не нужны, конечно, останки от предыдущих ''героев'', что пошли на свалку."
    await achprog(user, ach='cases')
    return text






async def extraCase(call, idp): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    checkdonate = await db.Inventory.exists(name='Амфора экстренной помощи', active=1, idplayer=idp.id)
    if checkdonate:
        checkdonate = await db.Inventory.get(name='Амфора экстренной помощи', active=1, idplayer=idp.id).first()
        if use == 'tp':
            success = await db.addItem('Свиток телепортации', idp, arg='1')
        elif use == 'heal':
            success = await db.addItem('Зелье восстановления', idp, arg='1')
        elif use == 'eat':
            success = await db.addItem('Лучше не спрашивай', idp, arg='1')
        if success == True:
            text = "Ты сделал свой выбор\n_Джин послушно исполнил твою просьбу, а затем расстаял в воздухе вместе с амфорой. Рюкзак потяжелел_"
            await db.Inventory.filter(id=checkdonate.id).update(active=0)
        else:
            text = "Для начала, тебе стоит освободить инвентарь. После можешь выбрать снова"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Еда', callback_data="extraCase_eat"))
            markup.add(InlineKeyboardButton('Зелье здоровья', callback_data="extraCase_heal"))
            markup.add(InlineKeyboardButton('Свиток телепортации', callback_data="extraCase_tp"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
    else:
        text = "У вас уже нет амфоры"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')


async def opendonatecase(user): 
    items = ['🚥', '👘', '🔶', '🔥', '🧩', '👘', '🔶', '🧩', '🟦', '🟧']
    firstItem = '➖'
    secondItem = '➖'
    thirdItem = '➖'
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    gg = await bot.send_message(user.user_id, text)
    await asyncio.sleep(0.2)
    items = ['🚥', '👘', '🔶', '🔥', '🧩', '👘', '🔶', '🧩', '🟦', '🟧']
    firstItem = '➖'
    secondItem = '➖'
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    await asyncio.sleep(0.4)
    items = ['🚥', '👘', '🔶', '🔥', '🧩', '👘', '🔶', '🧩', '🟦', '🟧']
    secondItem = thirdItem
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    try:
        gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    except:
        pass
    await asyncio.sleep(0.6)
    items = ['🚥', '👘', '🔶', '🔥', '🧩', '🔶', '🧩', '🟦', '🟧']
    firstItem = secondItem
    secondItem = thirdItem
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    try:
        gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    except:
        pass
    await asyncio.sleep(0.8)
    items = ['👘', '🔶', '🔥', '🧩', '🔶', '🧩', '🟦', '🟧']
    firstItem = secondItem
    secondItem = thirdItem
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    try:
        gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    except:
        pass
    await asyncio.sleep(1)
    items = ['👘', '🔶', '🔥', '🧩', '🔶', '🧩', '🟦', '🟧']
    firstItem = secondItem
    secondItem = thirdItem
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    try:
        gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    except:
        pass
    await asyncio.sleep(1.5)
    items = ['👘', '🔶', '🔥', '🧩', '🔶', '🧩', '🟦', '🟧']
    firstItem = secondItem
    secondItem = thirdItem
    thirdItem = random.choice(items)
    text = "###########\n"
    text += "# [{}{}{}] #".format(firstItem, secondItem, thirdItem)
    text += "\n###########"
    try:
        gg = await bot.edit_message_text(text, user.user_id, gg.message_id)
    except:
        pass
    if secondItem == '🔥':
        newItem = await db.Inventory(name='Осколок огня', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🔥Осколок огня!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🔥Осколок огня".format(user.username))
    elif secondItem == '🚥':
        newItem = await db.Inventory(name='Анти-анализатор БМ', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🚥Анти-анализатор БМ!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🚥Анти-анализатор БМ".format(user.username))
    elif secondItem == '👘':
        newItem = await db.Inventory(name='Плащ-невидимка', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 👘Плащ-невидимка!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 👘Плащ-невидимку".format(user.username))
    elif secondItem == '🔷':
        newItem = await db.Inventory(name='Осколок энергии', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🔷Осколок энергии!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🔷Осколок энергии".format(user.username))
    elif secondItem == '🔶':
        newItem = await db.Inventory(name='Амулет здоровья', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🔶Амулет здоровья")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🔶Амулет здоровья".format(user.username))
    elif secondItem == '🧩':
        newItem = await db.Inventory(name='Кусок паззла', active=1, size=0, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, 'Внутри вы нашли 🧩Кусок паззла!')
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🧩Кусок паззла".format(user.username))
    elif secondItem == '🟦':
        newItem = await db.Inventory(name='Осколок льда', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🟦Осколок льда!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🟦Осколок льда".format(user.username))
    elif secondItem == '🟧':
        newItem = await db.Inventory(name='Осколок эфира', active=1, size=1, idplayer=user.id, type='Артефакт')
        await newItem.save()
        await bot.send_message(user.user_id, "Внутри вы нашли 🟧Осколок эфира!")
        await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с сюрпризом 🟧Осколок эфира".format(user.username))



async def opendonatecaseRecipy(user):
    items = ['Рецепт героИн', 'Рецепт бамбук', 'Рецепт боярышник', 'Рецепт ВиАгро', 'Рецепт паучий афродизиак', 'Рецепт бакин']
    rand = random.choice(items)
    checkRecipy = await db.Inventory.exists(name=rand, idplayer=user.id)
    if checkRecipy: newItem = await db.Inventory(name=rand, active=1, size=0, idplayer=user.id, type='Рецепт')
    else: newItem = await db.Inventory(name=rand, active=1, size=0, idplayer=user.id, type='Рецепт')
    await newItem.save()
    await bot.send_message(user.user_id, "Внутри вы нашли 📜{}".format(rand))
    await bot.send_message(tradeChat, "Игрок {} достал из 📦Коробки с рецептом {}".format(user.username, rand))

legendaryCaseActive = 0
legendaryCaseKvadrats = {}
legendaryCaseKvadratsOpened = []
legendaryCaseClosed = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}
async def legendaryCase(user, item):
    global legendaryCaseActive
    global legendaryCaseKvadrats
    global legendaryCaseKvadratsOpened
    if legendaryCaseActive == 0:
        legendaryCaseActive = 1
        legendaryCaseKvadrats = {}
        legendaryCaseKvadratsOpened = []
        item.active = 0
    else:
        await bot.send_message(user.user_id, "Сейчас кто-то уже открывает коробку. Пожалуйста, подождите...")
        return
    await bot.send_message(user.user_id, "Правила просты - нужно угадать 2 одинаковых предмета чтобы получить его. У вас есть три хода.")
    items = ['🔷', '🍯', '🌿']
    drops = {'🔷': 0, '🍯': 0, '🌿': 0}
    one = random.choice(items)
    drops[one] += 1
    two = random.choice(items)
    drops[two] += 1
    three = random.choice(items)
    drops[three] += 1
    if drops[three] >= 3 and three in items: items.remove(three)
    if drops[three] >= 3 and three in items: items.remove(three)
    if drops[three] >= 3 and three in items: items.remove(three)
    four = random.choice(items)
    drops[four] += 1
    if drops[four] >= 3 and four in items: items.remove(four)
    if drops[four] >= 3 and four in items: items.remove(four)
    if drops[four] >= 3 and four in items: items.remove(four)
    five = random.choice(items)
    drops[five] += 1
    if drops[five] >= 3 and five in items: items.remove(five)
    if drops[five] >= 3 and five in items: items.remove(five)
    if drops[five] >= 3 and five in items: items.remove(five)
    six = random.choice(items)
    drops[six] += 1
    if drops[six] >= 3 and six in items: items.remove(six)
    if drops[six] >= 3 and six in items: items.remove(six)
    if drops[six] >= 3 and six in items: items.remove(six)
    seven = random.choice(items)
    drops[seven] += 1
    if drops[seven] >= 3 and seven in items: items.remove(seven)
    if drops[seven] >= 3 and seven in items: items.remove(seven)
    if drops[seven] >= 3 and seven in items: items.remove(seven)
    eight = random.choice(items)
    drops[eight] += 1
    if drops[eight] >= 3 and eight in items: items.remove(eight)
    if drops[eight] >= 3 and eight in items: items.remove(eight)
    if drops[eight] >= 3 and eight in items: items.remove(eight)
    nine = random.choice(items)
    drops[nine] += 1
    karty = "" + one + two + three + "\n" + four + five + six + "\n" + seven + eight + nine
    legendaryCaseKvadrats['1'] = str(one)
    legendaryCaseKvadrats['2'] = str(two)
    legendaryCaseKvadrats['3'] = str(three)
    legendaryCaseKvadrats['4'] = str(four)
    legendaryCaseKvadrats['5'] = str(five)
    legendaryCaseKvadrats['6'] = str(six)
    legendaryCaseKvadrats['7'] = str(seven)
    legendaryCaseKvadrats['8'] = str(eight)
    legendaryCaseKvadrats['9'] = str(nine)
    text = "1️⃣ 2️⃣ 3️⃣\n4️⃣ 5️⃣ 6️⃣\n7️⃣ 8️⃣ 9️⃣"
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton('1', callback_data="donateKartochki_1"))
    markup.add(InlineKeyboardButton('2', callback_data="donateKartochki_2"))
    markup.add(InlineKeyboardButton('3', callback_data="donateKartochki_3"))
    markup.add(InlineKeyboardButton('4', callback_data="donateKartochki_4"))
    markup.add(InlineKeyboardButton('5', callback_data="donateKartochki_5"))
    markup.add(InlineKeyboardButton('6', callback_data="donateKartochki_6"))
    markup.add(InlineKeyboardButton('7', callback_data="donateKartochki_7"))
    markup.add(InlineKeyboardButton('8', callback_data="donateKartochki_8"))
    markup.add(InlineKeyboardButton('9', callback_data="donateKartochki_9"))
    await bot.send_message(user.user_id, text, reply_markup=markup)
    return item


async def donateKartochki(call, idp): 
    do = call.data.split('_')
    use = do[1]
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    global legendaryCaseKvadrats
    global legendaryCaseKvadratsOpened
    global legendaryCaseClosed
    global legendaryCaseActive
    if use in legendaryCaseKvadratsOpened:
        return
    else:
        legendaryCaseKvadratsOpened.append(use)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    drops = {'🔷': 'Камень энергии', '🍯': 'Горшок лепрекона', '🌿': 'Карманная дриада'}
    count = 0
    for z in legendaryCaseKvadratsOpened:
        count += 1
    if count == 3:
        _count = 0
        for z in legendaryCaseKvadratsOpened:
            _count += 1 #legendaryCaseKvadrats
            if _count == 1: # '🔷', '🍯', '🌿'
                if legendaryCaseKvadrats[z] == '🔷': one = 'Камень энергии'
                elif legendaryCaseKvadrats[z] == '🍯': one = 'Горшок лепрекона'
                elif legendaryCaseKvadrats[z] == '🌿': one = 'Карманная дриада'
            if _count == 2:
                if legendaryCaseKvadrats[z] == '🔷': two = 'Камень энергии'
                elif legendaryCaseKvadrats[z] == '🍯': two = 'Горшок лепрекона'
                elif legendaryCaseKvadrats[z] == '🌿': two = 'Карманная дриада'
            if _count == 3:
                legendaryCaseActive = 0
                if legendaryCaseKvadrats[z] == '🔷': three = 'Камень энергии'
                elif legendaryCaseKvadrats[z] == '🍯': three = 'Горшок лепрекона'
                elif legendaryCaseKvadrats[z] == '🌿': three = 'Карманная дриада'
                if one == two or one == three or two == three:
                    if one == two:
                        success = await db.addItem(one, idp, arg='go')
                        winner = one
                    elif two == three:
                        success = await db.addItem(two, idp, arg='go')
                        winner = two
                    elif one == three:
                        success = await db.addItem(one, idp, arg='go')
                        winner = one
                    await bot.send_message(call.message.chat.id, "Ты выиграл {}!".format(winner))
                    resultText = "Как всё было на самом деле:\n\n\n"
                    ___count = 0
                    for x in legendaryCaseKvadrats:
                        ___count += 1
                        if ___count == 4 or ___count == 7:
                            resultText += "\n{}".format(legendaryCaseKvadrats[x])
                        else:
                            resultText += "{}".format(legendaryCaseKvadrats[x])
                    await bot.send_message(tradeChat, "Игрок {} выиграл {}\n{}".format(idp.username, winner, resultText))
                else:
                    ___count = 0
                    await bot.send_message(call.message.chat.id, "Ты ничего не выиграл. В качестве утешительного приза ты получаешь 📦Коробку с сюрпризом")
                    await opendonatecase(idp)
                    resultText = "Как всё было на самом деле:\n\n\n"
                    for x in legendaryCaseKvadrats:
                        ___count += 1
                        if ___count == 4 or ___count == 7:
                            resultText += "\n{}".format(legendaryCaseKvadrats[x])
                        else:
                            resultText += "{}".format(legendaryCaseKvadrats[x])
                    await bot.send_message(call.message.chat.id, resultText)
                    await bot.send_message(tradeChat, "Игрок {}\n{}".format(idp.username, resultText))
                return
    else:
        ___count = 0
        text = ""
        for z in legendaryCaseKvadrats:
            ___count += 1
            if z in legendaryCaseKvadratsOpened:
                if ___count == 4 or ___count == 7:
                    text += "\n{}".format(legendaryCaseKvadrats[z])
                else:
                    text += "{}".format(legendaryCaseKvadrats[z])
            else:
                if ___count == 4 or ___count == 7:
                    text += "\n{}".format(legendaryCaseClosed[str(___count)])
                else:
                    text += "{}".format(legendaryCaseClosed[str(___count)])
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        ____count = 0
        for i in range(0, 9):
            ____count += 1
            if ____count in legendaryCaseKvadratsOpened:
                pass
            else:
                markup.add(InlineKeyboardButton('{}'.format(____count), callback_data="donateKartochki_{}".format(____count)))
        await bot.send_message(call.message.chat.id, "{}\n\nВыбирай еще".format(text), reply_markup=markup)
