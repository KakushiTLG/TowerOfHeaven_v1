async def shop(m1, m2, m3):
    do_work = await db.System.get(name='shop_work')
    if do_work == 0:
        await bot.edit_message_text('Вы подошли к магазину где стоял одинокий Ашот. \n_-Эй, Ашотик, брат, продай мне чё-нибудь\n-Пашёль нахуй_', m1, m3, parse_mode = 'markdown')
        return
    else:
        pass
    user = await db.Users.get(user_id=m1)
    text = 'Баланс: {}💰\n_Ты подходишь к невзрачному стеллажу с выцвевшим навесом. Ощущение, словно владелец бросает в ящики для продуктов все, что находит по пути сюда. Впрочем, вон тот фиолетовый плод выглядит аппетитно._'.format(user.money)
    counteat = 0
    countequip = 0
    countitem = 0
    shop = await db.Shop.filter(count__gt=0)
    for counts in shop:
        if counts.type == 'Еда':
            counteat += 1
        elif counts.type == 'Экипировка' or counts.type == 'Зелье':
            countequip += 1
        elif counts.type == 'Броня':
            countitem += 1
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if counteat > 0:
        markup.add(InlineKeyboardButton('🍕 Пища', callback_data="shop_eat"))
    else:
        markup.add(InlineKeyboardButton('🍕 Пища (отсутствует в продаже)', callback_data="return"))
    if countequip > 0:
        markup.add(InlineKeyboardButton('🧢 Экипировка', callback_data="shop_equip"))
    else:
        markup.add(InlineKeyboardButton('🧢 Экипировка (отсутствует в продаже)', callback_data="return"))
    if countitem > 0:
        markup.add(InlineKeyboardButton('🛡 Броня', callback_data="shop_item"))
    else:
        markup.add(InlineKeyboardButton('🛡 Броня (отсутствует в продаже)', callback_data="return"))
    usr = await db.Users.get(user_id=m1)
    if usr.location == 'Город':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
    elif usr.location == 'Хэвенбург':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
    elif usr.location == 'Кавайня':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_wintercity_centr"))
    await bot.edit_message_text(text, m1, m3, reply_markup=markup, parse_mode = 'markdown')


@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers and call.data.startswith('return'))
def ret(call): 
    return

async def _shop(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    armorOld = ['Кожаный шлем', 'Кожаный нагрудник', 'Кожаные штаны', 'Кожаные ботинки']
    sh = call.data.split('_')
    select = sh[1]
    if select == 'close':
        await db.Users.filter(id=user.id).update(position='Площадь')
        await bot.edit_message_text('Вы закрыли магазин.', call.message.chat.id, call.message.message_id)
        return
    elif select == 'eat':
        Type = 'Еда'
    elif select == 'equip':
        Type = 'Экипировка'
    elif select == 'item':
        Type = 'Броня'
    markup = InlineKeyboardMarkup(row_width=2)
    text = "Баланс: {}💰\n\nВыберите предмет для покупки: \n".format(user.money)
    shop = await db.Shop.filter(type=Type, count__gt=0)
    for item in shop:
        if Type == 'Броня' and item.name in armorOld:
            name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
            text += "\nx{} {} | {}💰".format(item.count, name, item.price)
            markup.add(InlineKeyboardButton('{}({}💰)'.format(name, item.price), callback_data="buy_{}".format(item.id)))
        elif Type != 'Броня':
            name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
            text += "\nx{} {} | {}💰".format(item.count, name, item.price)
            markup.add(InlineKeyboardButton('{}({}💰)'.format(name, item.price), callback_data="buy_{}".format(item.id)))        
    markup.add(InlineKeyboardButton('↩️ Вернуться', callback_data="backtoshop"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')


async def buy(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    sh = call.data.split('_')
    select = sh[1]
    item = await db.Shop.get(id=select)
    if item.count <= 0:
        text = "К сожалению, товар кончился."
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
        return
    name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
    if user.location == 'Город':
        pass
    else:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)
        return
    if user.money >= item.price:
        if item.name == 'Улучшенный рюкзак':
            check = await db.Inventory.exists(idplayer=user.id, name='Улучшенный рюкзак')
            if check:
                text = "_Покупка дополнительного рюкзака не поможет тебе унести больше!_"
                await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                return
        success = await db.addItem(item.name, user)
        await db.specialItems(name, user)
        if success == True:
            await db.Shop.filter(id=select).update(count=F('count') - 1)
            await db.Users.filter(id=user.id).update(money=F('money') - item.price)
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно приобретено: {}".format(item.name))                
            try:
                await logBot.send_message(tradeChat, "Игрок {} купил {} за {}💰".format(user.username, item.name, item.price))
            except:
                pass
            await achprog(user, ach='shopbuy')
            return
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нет места в рюкзаке")          
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Недостаточно золота")                



async def donateshop(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Предметы', callback_data="doshopItems"))
    markup.add(InlineKeyboardButton('Прочее', callback_data="doshopOther"))
    markup.add(InlineKeyboardButton('Обмен валюты', callback_data="doshopCurrency"))
    text = "Выберите категорию предметов:"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
shopStatus = {}


async def doshopItems(call, user):
    koltLeft = await db.System.get_or_none(name='koltLeft').first()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('🃏Пропуск элитного воина', callback_data="dshopbuy_bp"))
    markup.add(InlineKeyboardButton('📦Коробка с сюрпризом', callback_data="dshopbuy_lootbox1"))
    markup.add(InlineKeyboardButton('📦Коробка с карточками', callback_data="dshopbuy_lootbox2"))
    markup.add(InlineKeyboardButton('📦Коробка с рецептами', callback_data="dshopbuy_lootbox3"))
    markup.add(InlineKeyboardButton('🔷Осколок энергии', callback_data="dshopbuy_energyOsk"))
    markup.add(InlineKeyboardButton('🔥Осколок огня', callback_data="dshopbuy_fireOsk"))
    markup.add(InlineKeyboardButton('🔷Камень энергии', callback_data="dshopbuy_energyCum"))
    markup.add(InlineKeyboardButton('🍯Горшок лепрекона', callback_data="dshopbuy_leprekon"))
    markup.add(InlineKeyboardButton('🌿Карманная дриада', callback_data="dshopbuy_driada"))
    markup.add(InlineKeyboardButton('🟧Осколок эфира', callback_data="dshopbuy_etherium"))
    markup.add(InlineKeyboardButton('🎟Билет на тот свет', callback_data="dshopbuy_bilet"))
    markup.add(InlineKeyboardButton('🎣Весьма непростая удочка', callback_data="dshopbuy_udochka"))
    if koltLeft.value >= 1:
        markup.add(InlineKeyboardButton('🗡Кольт', callback_data="dshopbuy_kolt"))
        markup.add(InlineKeyboardButton('🗡Золотой кольт', callback_data="dshopbuy_goldkolt"))
    checkTp = await db.Inventory.exists(name='Пятый сектор', idplayer=user.id)
    if not checkTp: markup.add(InlineKeyboardButton('📜Свиток телепорта на пятый сектор пирамиды', callback_data="dshopbuy_fifthSector"))
    markup.add(InlineKeyboardButton('Назад', callback_data="donateshop"))
    text = "\n\n🃏Пропуск элитного воина (300💎). Позволяет получить больше наград с пропуска испытаний."
    text += "\n\n📦Коробка с сюрпризом (75💎) | Внутри лежит 🔥Осколок Огня, 🔶Амулет здоровья, 🚥Анти-анализатор БМ, 👘Плащ-невидимка, 🧩Кусок паззла, 🟧Осколок эфира или 🟦Осколок льда!"
    text += "\n\n📦Коробка с карточками (200💎) | Внутри лежит: 🔷Камень энергии, 🍯Горшок лепрекона или 🌿Карманная дриада"
    text += "\n\n📦Коробка с рецептом (50💎) | Попытайте удачу и достаньте изнутри один из рецептов для котелка!"
    text += "\n\n🔷Осколок энергии (225💎). Позволяет пассивно восстанавливать каждую минуту 5⚡️, если энергия выше 5⚡️, но не выше 70⚡️"
    text += "\n\n🔥Осколок огня (150💎). Благодаря специальной ауре, после вашей атаки монстры начинают гореть из-за чего получают дополнительно 5% (10% в Кавайне) от собственного максимального здоровья"
    text += "\n\n🔷Камень энергии (550💎). Позволяет пассивно восстанавливать каждую минуту 7⚡️"
    text += "\n\n🍯Горшок лепрекона (525💎). При проигрыше в PvE и смерти от голода монеты не тратятся, однако с монстров можно получить 65% монет."
    text += "\n\n🌿Карманная дриада (475💎). Удваивает выпадение цветов"
    text += "\n\n🟧Осколок эфира (200💎). В конце битвы с монстром восстанавливает ♥️, равное количеству убитых монстров, умноженному на 1.5 (счётчик каждые 5 минут падает на 1)"
    text += "\n\n🎟Билет на тот свет (10💎). Позволяет телепортироваться к месту последней смерти"
    text += "\n\n🎣Весьма непростая удочка (1050💎). Позволяет ловить самую лучшую рыбу в Пруду с высоким шансом."
    if not checkTp: text += "\n\n📜Свиток телепорта на пятый сектор пирамиды (300💎). Позволяет телепортироваться в пятый сектор песчаной пирамиды."
    if koltLeft.value >= 1:
        text += "\n\n🔥Эксклюзив (осталось {})\n\n🗡Кольт (750💎). В отличии от обычного оружия, его атака наносит меньше урона, но есть шанс нанести до 6 выстрелов за ход. Особый навык позволяет с большим шансом нанести большее количество выстрелов за ход. Если кольт смог выстрелить 6 раз за ход, он наносит дополнительный Крит в размере 500% атаки. При покупке так же получается бонус +5📦".format(koltLeft.value)
        text += "\n\n🗡Золотой кольт (1050💎). Элитная вариация обычного кольта. Дополнительной особенностью является возможность нанесения собственной гравировки на оружие, которую будет видеть поверженный противник при поражении в PvP. При покупке так же получается бонус +5📦"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def doshopOther(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    donateinv = await db.Inventory.filter(name='Донат инв', idplayer=user.id).count()
    priceDonateInv = 25 * (donateinv + 1)
    if priceDonateInv > 75:
        priceDonateInv = 75
    skillsReset = await db.Inventory.filter(name='Сброс навыков', idplayer=user.id).count()
    priceSkillsReset = 100 * (skillsReset + 1)
    markup.add(InlineKeyboardButton('+5📦', callback_data="dshopbuy_1"))
    markup.add(InlineKeyboardButton('+200📦(🥘)', callback_data="dshopbuy_kotelokLimit"))
    markup.add(InlineKeyboardButton('Смена названия оружия', callback_data="dshopbuy_7"))
    markup.add(InlineKeyboardButton('Сменить никнейм', callback_data="dshopbuy_4"))
    markup.add(InlineKeyboardButton('⚡️Бустеры', callback_data="dshopbuy_8"))
    #markup.add(InlineKeyboardButton('⚡️Бустеры Котоми', callback_data="dshopbuy_kotomiBoost"))
    markup.add(InlineKeyboardButton('Сброс навыков', callback_data="dshopbuy_skillsReset"))
    markup.add(InlineKeyboardButton('♥️ToH supporter', callback_data="dshopbuy_supporter"))
    markup.add(InlineKeyboardButton('Назад', callback_data="donateshop"))
    text = "+5📦({}💎). Можно купить и расширить инвентарь на 5📦. Стартовая цена - 25💎(+25 каждый раз, до 75💎 за 5📦)".format(priceDonateInv)
    text += "\n+200📦(🥘)(50💎). Можно купить и расширить инвентарь котелка на 200📦"
    text += "\n\nСмена никнейма(50💎). Вы можете сменить свой никнейм, если предыдущий вас не устраивает (или нет)"
    text += "\n\n⚡️Бустеры. Включается режим быстрого перемещения в локациях (перемещение занимает минуту, количество получаемого опыта и золота повышено на 25%)"
    #text += "\n\n⚡️Бустеры Котоми(25💎). На сутки количество получаемого опыта Котоми удваивается."
    text += "\n\nСброс навыков ({}💎). Позволяет сбросить все /skills с возвратом 🔘 (Кроме карманной смекалки)".format(priceSkillsReset)
    text += "\n\n♥️ToH supporter (500💎). Набор включает в себя х1📦Коробка с карточками, +5📦, 15 дней ⚡️Бустеров и титул в профиле ♥️ToH supporter♥️ на месяц"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def doshopCurrency(call, user):
    text = "Обмен 💎 на валюту городов\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text += "\nПокупка 🔻 (Курс - 1💎=3🔻)"
    markup.add(InlineKeyboardButton('Покупка 🔻', callback_data="dshopbuy_9"))
    if user.lvl >= 15:
        text += "\nПокупка 🧊 (Курс - 1💎=45🧊)"
        markup.add(InlineKeyboardButton('Покупка 🧊', callback_data="dshopbuy_10"))
    if user.lvl >= 35:
        text += "\nПокупка ♦️ (Курс - 1💎=1♦️)"
        markup.add(InlineKeyboardButton('Покупка ♦️', callback_data="dshopbuy_11"))
    if user.lvl >= 50:
        text += "\nПокупка 💧 (Курс - 1💎=1💧)"
        markup.add(InlineKeyboardButton('Покупка 💧', callback_data="dshopbuy_12"))
    if user.lvl >= 75:
        text += "\nПокупка 🗝 (Курс - 1💎=3🗝)"
        markup.add(InlineKeyboardButton('Покупка 🗝', callback_data="dshopbuy_13"))
    markup.add(InlineKeyboardButton('Назад', callback_data="donateshop"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def dshopbuy(call, user):
    sh = call.data.split('_')
    select = sh[1]
    donateinv = await db.Inventory.filter(name='Донат инв', idplayer=user.id).count()
    priceDonateInv = 25 * (donateinv + 1)
    if priceDonateInv > 75:
        priceDonateInv = 75
    if select == '1':
        if user.almaz >= priceDonateInv:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - priceDonateInv,
                                                        inventorySizeMax=F('inventorySizeMax') + 5)
            await db.Inventory.create(name='Донат инв', type='Донат', size=0, bonus=0, active=0, idplayer=user.id)
            await bot.edit_message_text("Вы успешно приобрели +5📦", call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл +5📦".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '2':
        markup = InlineKeyboardMarkup(row_width=2)
        if user.almaz >= 50:
            text = "Выберите новую группировку"
            if user.frak != 'Вавилон':
                markup.add(InlineKeyboardButton('Вавилон', callback_data="donateSelectFrak_1"))
            if user.item != 'Небесные рыцари':
                markup.add(InlineKeyboardButton('Небесные рыцари', callback_data="donateSelectFrak_2"))
            if user.item != 'Эгида':
                markup.add(InlineKeyboardButton('Эгида', callback_data="donateSelectFrak_5"))
            if user.item != 'Авангард Феникса':
                markup.add(InlineKeyboardButton('Авангард Феникса', callback_data="donateSelectFrak_4"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '3':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 50:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50)
            text = "Выберите новое оружие"
            if user.item != 'Меч':
                markup.add(InlineKeyboardButton('Меч', callback_data="donateSelectItem_mech"))
            if user.item != 'Пистолет с ножом':
                markup.add(InlineKeyboardButton('Пистолет с ножом', callback_data="donateSelectItem_pistol"))
            if user.item != 'Копьё':
                markup.add(InlineKeyboardButton('Копьё', callback_data="donateSelectItem_kopie"))
            if user.item != 'Катана':
                markup.add(InlineKeyboardButton('Катана', callback_data="donateSelectItem_katana"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
            return
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '4':
        if user.almaz >= 50:
            await logBot.send_message(tradeChat, "Игрок {} приобрёл смену никнейма".format(user.username))
            await bot.send_message(call.message.chat.id, "Назови своё имя, путник.")
            shopStatus[call.from_user.id] = 'reg_nick'
            text = "Начался процесс смены никнейма..."
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50)
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '5':
        if user.almaz >= 5:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 5)
            success = await db.addItem('Амфора экстренной помощи', user)
            text = "Вы успешно приобрели 🏺Амфора экстренной помощи"
            await logBot.send_message(tradeChat, "Игрок {} приобрёл Амфору экстренной помощи".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'lootbox1':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 75:
            await logBot.send_message(tradeChat, "Игрок {} приобрёл Коробку с сюрпризом".format(user.username))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 75)
            text = "Вы успешно приобрели 📦Коробку с сюрпризом. Смотрим что внутри..."
            await opendonatecase(user)
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'lootbox2':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 200:
            await logBot.send_message(tradeChat, "Игрок {} приобрёл Коробку с карточками".format(user.username))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 200)
            text = "Вы успешно приобрели 📦Коробку с карточками. Открыть её можно в инвентаре."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            await db.addItem('Коробка с карточками', user, arg='a')
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'lootbox3':
        if user.almaz >= 50:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50)
            await bot.edit_message_text("Вы успешно приобрели 📦Коробку с рецептом. Смотрим что внутри...", call.message.chat.id, call.message.message_id)
            await opendonatecaseRecipy(user)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл Коробку с рецептом".format(user.username))
        else:
            text = "У тебя не хватает 💎"
    elif select == '7':
        if user.almaz >= 45:
            await logBot.send_message(tradeChat, "Игрок {} приобрёл смену оружия".format(user.username))
            await bot.send_message(call.message.chat.id, "Назови имя своего оружия")
            shopStatus[call.from_user.id] = 'change_weaponName'
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 45)
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '8':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('1 час', callback_data="buyBooster_1h"))
        markup.add(InlineKeyboardButton('3 часа', callback_data="buyBooster_3h"))
        markup.add(InlineKeyboardButton('5 часов', callback_data="buyBooster_5h"))
        markup.add(InlineKeyboardButton('12 часов', callback_data="buyBooster_12h"))
        markup.add(InlineKeyboardButton('24 часа', callback_data="buyBooster_24h"))
        markup.add(InlineKeyboardButton('30 дней', callback_data="buyBooster_30d"))
        text = "Выберите срок, на который хотите приобрести ⚡️Бустеры.\n1 час - 10💎\n3 часа - 20💎\n5 часов - 30💎\n12 часов - 50💎\n24 часа - 65💎\n30 дней - 900💎"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif select == 'bilet':
        if user.almaz >= 5:
            success = await db.addItem('Билет на тот свет', user)
            if success == True:
                await db.Users.filter(id=user.id).update(almaz=F('almaz') - 5)
                await bot.edit_message_text('Вы успешно приобрели 🎟Билет на тот свет.', call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("У вас не хватает места в инвентаре. Покупка отменена", call.message.chat.id, call.message.message_id)
            return
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == '9':
        await bot.edit_message_text("Введите количество кристаллов, которое вы желаете потратить на 🔻. Курс - 1💎=3🔻. Для отмены - ''Отмена''", call.message.chat.id, call.message.message_id)
        shopStatus[call.from_user.id] = 'exchangeCheshuya'
    elif select == '10':
        await bot.edit_message_text("Введите количество кристаллов, которое вы желаете потратить на 🧊. Курс - 1💎=45🧊. Для отмены - ''Отмена''", call.message.chat.id, call.message.message_id)
        shopStatus[call.from_user.id] = 'exchangeSosun'
    elif select == '11':
        await bot.edit_message_text("Введите количество кристаллов, которое вы желаете потратить на ♦️. Курс - 1💎=1♦️. Для отмены - ''Отмена''", call.message.chat.id, call.message.message_id)
        shopStatus[call.from_user.id] = 'exchangeRadar'
    elif select == '12':
        await bot.edit_message_text("Введите количество кристаллов, которое вы желаете потратить на 💧. Курс - 1💎=1💧. Для отмены - ''Отмена''", call.message.chat.id, call.message.message_id)
        shopStatus[call.from_user.id] = 'exchangeOcus'
    elif select == '13':
        await bot.edit_message_text("Введите количество кристаллов, которое вы желаете потратить на 🗝. Курс - 1💎=3🗝. Для отмены - ''Отмена''", call.message.chat.id, call.message.message_id)
        shopStatus[call.from_user.id] = 'exchangeMetro'

    elif select == 'kotelokLimit':
        if user.almaz >= 50:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, kotelokLimit=F('kotelokLimit') + 200)
            await bot.edit_message_text("Вы успешно приобрели +200📦(🥘)", call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл +200📦(🥘)".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'supporter':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 500:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 500)
            await bot.edit_message_text("Покупаем...", call.message.chat.id, call.message.message_id)
            await db.addBoost(user, lvl=360)
            if user.supporter >= time.time(): await db.Users.filter(id=user.id).update(booster=F('booster') + 2592000)
            else: await db.Users.filter(id=user.id).update(supporter=time.time() + 2592000)
            await db.addItem('Коробка с карточками', user, arg='a')
            await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 5)
            await bot.send_message(user.user_id, "Покупка набора ToH supporter завершена. Вы можете поставить титул через команду /badges")
            await logBot.send_message(tradeChat, "Игрок {} приобрёл саппортер".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'bp':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 300:
            if user.bpStatus == 0:
                await db.Users.filter(id=user.id).update(almaz=F('almaz') - 300, bpStatus=1)
                await bot.edit_message_text("Покупаем...", call.message.chat.id, call.message.message_id)
                goldAward = 0
                healAward = 0
                boostAward = 0
                finalAward = ""
                for i in range(0, user.bpLvl):
                    goldAward += 700
                    if i % 2 == 0:
                        for z in range(0, 4):
                            await db.addItem('Зелье восстановления', user, arg='1')
                            healAward += 1
                    if i in [5, 10, 15, 20, 25]: #ну или можно 1, 50, 100
                        await db.addBoost(user, lvl=6)
                        boostAward += 6
                    if i == 25:
                        finalAward = " 1🌿 5🔘 5+5📜 2 🪙Монета возвышения"
                        await db.Users.filter(id=user.id).update(uppts=F('uppts') + 5)
                        for i in range(0, 5):
                            await db.addItem('Свиток башни', user, arg='1')
                        for i in range(0, 5):
                            await db.addItem('Туннельный свиток', user, arg='1')
                        await db.addItem('Карманная дриада', user, arg='1')
                        await db.Inventory(name='Монета возвышения', idplayer=user.id, active=6, bonus=0, size=0, type='Прочее', atk_block=0, expires=0, count=0, lvl=0)
            else:
                await bot.edit_message_text("У вас уже куплен пропуск на этот сезон", call.message.chat.id, call.message.message_id)
                return
            await db.Users.filter(id=user.id).update(money=F('money') + goldAward)
            await bot.edit_message_text("Вы успешно приобрели 🃏Пропуск элитного воина.\nПолученные награды:\n{}💰 {}🧪 {}⚡️ 1🪙\n{}".format(goldAward, healAward, boostAward, finalAward), call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл платный БП".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'kotomiBoost':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 25:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 25)
            await bot.edit_message_text("Покупаем...", call.message.chat.id, call.message.message_id)
            checkIvent = await db.Ivent.exists(idplayer=user.id)
            if checkIvent:
                ivent = await db.Ivent.get(idplayer=user.id).first()
                if ivent.booster >= time.time(): await db.Ivent.filter(idplayer=user.id).update(booster=F('booster') + 86400)
                else: await db.Ivent.filter(id=ivent.id).update(booster=time.time() + 86400)
                await bot.send_message(user.user_id, "Вы приобрели ⚡️Бустеры Котоми на 24 часа.")
                await logBot.send_message(tradeChat, "Игрок {} приобрёл бустеры Котоми".format(user.username))
            else:
                await bot.edit_message_text("Вы не учавствуете в ивенте", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'fifthSector':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        await bot.edit_message_text("Недоступно", call.message.chat.id, call.message.message_id)
        if user.almaz >= 300:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 300)
            await bot.edit_message_text("Вы успешно приобрели 📜Свиток телепорта на пятый сектор пирамиды", call.message.chat.id, call.message.message_id)
            await db.addItem('Пятый сектор', user, arg='a')
            await db.Inventory.filter(name='Пятый сектор', idplayer=user.id).update(active=0)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 📜Свиток телепорта на пятый сектор пирамиды".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'energyOsk':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 225:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 225)
            await bot.edit_message_text("Вы успешно приобрели 🔷Осколок энергии", call.message.chat.id, call.message.message_id)
            await db.addItem('Осколок энергии', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🔷Осколок энергии".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'fireOsk':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 150:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 150)
            await bot.edit_message_text("Вы успешно приобрели 🔥Осколок огня", call.message.chat.id, call.message.message_id)
            await db.addItem('Осколок огня', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🔥Осколок огня".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'energyCum':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 550:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 550)
            await bot.edit_message_text("Вы успешно приобрели 🔷Камень энергии", call.message.chat.id, call.message.message_id)
            await db.addItem('Камень энергии', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🔷Камень энергии".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'leprekon':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 525:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 525)
            await bot.edit_message_text("Вы успешно приобрели 🍯Горшок лепрекона", call.message.chat.id, call.message.message_id)
            await db.addItem('Горшок лепрекона', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🍯Горшок лепрекона".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'driada':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.almaz >= 475:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 475)
            await bot.edit_message_text("Вы успешно приобрели 🌿Карманная дриада", call.message.chat.id, call.message.message_id)
            await db.addItem('Карманная дриада', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🌿Карманная дриада".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'skillsReset':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        skillsReset = await db.Inventory.filter(name='Сброс навыков', idplayer=user.id).count()
        priceSkillsReset = 100 * (skillsReset + 1)
        if user.almaz >= priceSkillsReset:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - priceSkillsReset)
            skills = {'masterWeapon': user.masterWeapon, 'luckerAvtomat': user.luckerAvtomat, 'krazha': user.krazha, 'antikrazha': user.antikrazha, 'reactionPvP': user.reactionPvP}
            prices = {}
            rewardedSkillsPts = 0
            for z in skills:
                while skills[z] > 0:
                    if skills[z] == 1: prices[z] = 1
                    elif skills[z] == 2: prices[z] = 3
                    elif skills[z] == 3: prices[z] = 6
                    elif skills[z] == 4: prices[z] = 10
                    elif skills[z] == 5: prices[z] = 15
                    elif skills[z] == 6: prices[z] = 21
                    elif skills[z] == 7: prices[z] = 28
                    elif skills[z] == 8: prices[z] = 36
                    elif skills[z] == 9: prices[z] = 45
                    elif skills[z] == 10: prices[z] = 55
                    else: skills[z] = 0
                    skills[z] -= 1
                    rewardedSkillsPts += prices[z]
            await db.Users.filter(id=user.id).update(masterWeapon=0, luckerAvtomat=0, krazha=0, antikrazha=0, reactionPvP=0, uppts=F('uppts') + rewardedSkillsPts)
            newItem = await db.Inventory(name='Сброс навыков', idplayer=user.id, active=0, type='Прочее', size=0, bonus=0, atk_block=0, expires=0)
            await newItem.save()
            await bot.edit_message_text("Вы успешно приобрели сброс навыков. Вам возвращено {}🔘".format(rewardedSkillsPts), call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} сбросил навыки за {}💎. Получено {}🔘".format(user.username, priceSkillsReset, rewardedSkillsPts))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    elif select == 'kolt':
        koltLeft = await db.System.get_or_none(name='koltLeft').first()
        if koltLeft.value >= 1:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            if user.almaz >= 750:
                await db.Users.filter(id=user.id).update(almaz=F('almaz') - 750, inventorySizeMax=F('inventorySizeMax') + 5)
                await bot.edit_message_text("Вы успешно приобрели 🗡Кольт и +5📦", call.message.chat.id, call.message.message_id)
                await db.addItem('Кольт', user, arg='a')
                await logBot.send_message(tradeChat, "Игрок {} приобрёл 🗡Кольт и +5📦".format(user.username))
                await db.System.filter(name='koltLeft').update(value=F('value') - 1)
            else:
                await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Отсутствует в продаже.", call.message.chat.id, call.message.message_id)
    elif select == 'goldkolt':
        koltLeft = await db.System.get_or_none(name='koltLeft').first()
        if koltLeft.value >= 1:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            if user.almaz >= 1050:
                await db.Users.filter(id=user.id).update(almaz=F('almaz') - 1050, inventorySizeMax=F('inventorySizeMax') + 5)
                await bot.edit_message_text("Вы успешно приобрели 🗡Золотой кольт и +5📦", call.message.chat.id, call.message.message_id)
                await db.addItem('Золотой кольт', user, arg='a')
                await logBot.send_message(tradeChat, "Игрок {} приобрёл 🗡Золотой кольт и +5📦".format(user.username))
                await db.System.filter(name='koltLeft').update(value=F('value') - 1)
            else:
                await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Отсутствует в продаже.", call.message.chat.id, call.message.message_id)

    elif select == 'udochka':
        if user.almaz >= 1050:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 1050)
            await bot.edit_message_text("Вы успешно приобрели 🎣Весьма непростая удочка", call.message.chat.id, call.message.message_id)
            await db.addItem('Весьма непростая удочка', user, arg='a')
            await logBot.send_message(tradeChat, "Игрок {} приобрёл 🎣Весьма непростая удочка".format(user.username))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Отсутствует в продаже.", call.message.chat.id, call.message.message_id)







@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='exchangeSosun')
async def changerToSosun(m):
    try:
        value = int(m.text)
    except:
        shopStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы ввели не число. Покупка отменена.")
        return
    if value > 0:
        user = await db.Users.get(user_id=m.from_user.id)
        await bot.send_message(user.user_id, "Начался процесс обмена. Пожалуйста, подождите...")
        if user.almaz >= value:
            await bot.send_message(kakushigoto, "Игрок {} обменивает {} кристаллов на снунцы".format(user.id, value))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            newValue = value * 45
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') + newValue)
            await bot.send_message(user.user_id, 'Вы успешно обменяли {}💎 на {}🧊'.format(value, newValue))
            await bot.send_message(kakushigoto, "Обмен завершён.")
            shopStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз. Покупка отменена.")
        shopStatus[m.from_user.id] = None

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='exchangeCheshuya')
async def exchangeCheshuya(m):
    try:
        value = int(m.text)
    except:
        shopStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы ввели не число. Покупка отменена.")
        return
    if value > 0:
        user = await db.Users.get(user_id=m.from_user.id)
        await bot.send_message(user.user_id, "Начался процесс обмена. Пожалуйста, подождите...")
        if user.almaz >= value:
            await bot.send_message(kakushigoto, "Игрок {} обменивает {} кристаллов на Чешую".format(user.id, value))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            newValue = value * 3
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') + newValue)
            await bot.send_message(user.user_id, 'Вы успешно обменяли {}💎 на {}🔻'.format(value, newValue))
            await bot.send_message(kakushigoto, "Обмен завершён.")
            shopStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз. Покупка отменена.")
        shopStatus[m.from_user.id] = None

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='exchangeOcus')
async def exchangeOcus(m):
    try:
        value = int(m.text)
    except:
        shopStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы ввели не число. Покупка отменена.")
        return
    if value > 0:
        user = await db.Users.get(user_id=m.from_user.id)
        await bot.send_message(user.user_id, "Начался процесс обмена. Пожалуйста, подождите...")
        if user.almaz >= value:
            await bot.send_message(kakushigoto, "Игрок {} обменивает {} кристаллов на Ситень".format(user.id, value))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            newValue = value
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') + newValue)
            await bot.send_message(user.user_id, 'Вы успешно обменяли {}💎 на {}💧'.format(value, newValue))
            await bot.send_message(kakushigoto, "Обмен завершён.")
            shopStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз. Покупка отменена.")
        shopStatus[m.from_user.id] = None

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='exchangeRadar')
async def exchangeRadar(m):
    try:
        value = int(m.text)
    except:
        shopStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы ввели не число. Покупка отменена.")
        return
    if value > 0:
        user = await db.Users.get(user_id=m.from_user.id)
        await bot.send_message(user.user_id, "Начался процесс обмена. Пожалуйста, подождите...")
        if user.almaz >= value:
            await bot.send_message(kakushigoto, "Игрок {} обменивает {} кристаллов на Рюмбы".format(user.id, value))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            newValue = value
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') + newValue)
            await bot.send_message(user.user_id, 'Вы успешно обменяли {}💎 на {}♦️'.format(value, newValue))
            await bot.send_message(kakushigoto, "Обмен завершён.")
            shopStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз. Покупка отменена.")
        shopStatus[m.from_user.id] = None

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='exchangeMetro')
async def exchangeRadar(m):
    try:
        value = int(m.text)
    except:
        shopStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Вы ввели не число. Покупка отменена.")
        return
    if value > 0:
        user = await db.Users.get(user_id=m.from_user.id)
        await bot.send_message(user.user_id, "Начался процесс обмена. Пожалуйста, подождите...")
        if user.almaz >= value:
            await bot.send_message(kakushigoto, "Игрок {} обменивает {} кристаллов на Ключи".format(user.id, value))
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            newValue = value * 3
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') + newValue)
            await bot.send_message(user.user_id, 'Вы успешно обменяли {}💎 на {}🗝'.format(value, newValue))
            await bot.send_message(kakushigoto, "Обмен завершён.")
            shopStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз. Покупка отменена.")
        shopStatus[m.from_user.id] = None



async def buyBooster(call, user):
    sh = call.data.split('_')
    f = sh[1]
    if f == '1h':
        if user.almaz >= 10:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 10)
            await db.addBoost(user, lvl=1)
            text = "Вы приобрели ⚡️Бустер на час. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    elif f == '3h':
        if user.almaz >= 20:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 20)
            await db.addBoost(user, lvl=3)
            text = "Вы приобрели ⚡️Бустер на 3 часа. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    elif f == '5h':
        if user.almaz >= 30:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 30)
            await db.addBoost(user, lvl=5)
            text = "Вы приобрели ⚡️Бустер на 5 часов. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    elif f == '12h':
        if user.almaz >= 50:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50)
            await db.addBoost(user, lvl=12)
            text = "Вы приобрели ⚡️Бустер на 12 часов. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    elif f == '24h':
        if user.almaz >= 65:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 65)
            await db.addBoost(user, lvl=24)
            text = "Вы приобрели ⚡️Бустер на 24 часа. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    elif f == '30d':
        if user.almaz >= 900:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 900)
            await db.addBoost(user, lvl=730)
            text = "Вы приобрели ⚡️Бустер на 1 месяц. Используйте его в своём инвентаре."
        else: text = "У вас не хватает 💎"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='change_weaponName')
async def changename_weapon(m):
    await db.Users.filter(user_id=m.from_user.id).update(visualitem=m.text)
    await bot.send_message(m.chat.id, "Готово!")
    shopStatus[m.from_user.id] = None


async def donateSelectItem(call, user):
    sh = call.data.split('_')
    f = sh[1]
    if f == 'mech':
        item = "Меч"
    elif f == 'pistol':
        item = "Пистолет с ножом"
    elif f == 'katana':
        item = "Катана"
    elif f == 'kopie':
        item = "Копьё"
    await user.refresh_from_db()
    checkWeapon = await db.Inventory.exists(name=item, idplayer=user.id)
    if checkWeapon:
        await bot.edit_message_text("Увы, такое оружие тебе уже выдавалось.", call.message.chat.id, call.message.message_id)
        return
    success = await db.addItem(item, user)
    if success:
        await bot.edit_message_text("Новое оружие - всегда хорошо!", call.message.chat.id, call.message.message_id)
        await logBot.send_message(tradeChat, "[АРСЕНАЛ] Игрок {} взял {}".format(user.username, item))
    else:
        await bot.edit_message_text("Новое оружие - всегда хорошо!.. Было бы место...", call.message.chat.id, call.message.message_id)

async def donateSelectFrak(call, user):
    sh = call.data.split('_')
    f = sh[1]
    fraksIdChats = {'Небесные рыцари': -1001467052649, 'Вавилон': -1001196802578, 'Эгида': -1001321956949, 'Авангард Феникса': -1001320424099}
    if user.frak != 'Вавилон' and user.frak != 'Небесные рыцари' and user.frak != 'Авангард Феникса' and user.frak != 'Грязное небо' and user.frak != 'Эгида':
        try:
            await bot.kick_chat_member(fraksIdChats[user.frak], call.from_user.id)
        except:
            pass
    if f == '1':
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, frak="Вавилон")
        await user.refresh_from_db(fields=['frak'])
        link = 'https://t.me/joinchat/R1XCEpHn9JeFp0Q5'
    elif f == '2':
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, frak="Небесные рыцари")
        await user.refresh_from_db(fields=['frak'])
        link = 'https://t.me/joinchat/V3FyacqbIgbb6oP0'
    elif f == '3':
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, frak="Грязное небо")
        await user.refresh_from_db(fields=['frak'])
        link = 'https://t.me/joinchat/Kd-6VBY61CSikVObkJdJJQ'
    elif f == '4':
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, frak="Авангард Феникса")
        await user.refresh_from_db(fields=['frak'])
        link = 'https://t.me/joinchat/ArRWh0UMj5BiNDVi'
    elif f == '5':
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 50, frak="Эгида")
        await user.refresh_from_db(fields=['frak'])
        link = "https://t.me/joinchat/Tst2VTk3ix8IZlJW"
    await logBot.send_message(tradeChat, "Игрок {} сменил группировку на {}".format(user.username, user.frak))
    await bot.edit_message_text("Вы успешно сменили группировку на {}\nСсылка-приглашение в чат группировки {}".format(user.frak, link), call.message.chat.id, call.message.message_id)

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='reg_nick')
async def change_nick(m):
    global nicks
    txt = await nick_parser(m.text, reg=True)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.row(item1, item2)
    await bot.send_message(m.chat.id, 'Твоё имя - {}?'.format(txt), reply_markup=markup)
    nicks[m.from_user.id] = txt
    shopStatus[m.from_user.id] = 'reg_nick_1'

@dp.message_handler(lambda m: shopStatus and m.from_user.id in shopStatus and shopStatus[m.from_user.id]=='reg_nick_1')
async def change_nick_1(m):
    global nicks
    if m.text == "Да":
        checknick = await db.Users.exists(username=nicks[m.from_user.id])
        if checknick:
            checknick = await db.Users.get(username=nicks[m.from_user.id]).first()
            if checknick.username == nicks[m.from_user.id] and checknick.user_id != m.from_user.id:
                await bot.send_message(m.chat.id, "К сожалению, такого героя мы уже знаем. Может, тебя зовут как-нибудь еще?\nЕсли это сообщение вылазит слишком часто, обратитесь в /report")
                shopStatus[m.from_user.id] = 'reg_nick'
                return
        await db.Users.filter(user_id=m.from_user.id).update(username=nicks[m.from_user.id])
        shopStatus[m.from_user.id] = None
        await user.refresh_from_db()
        await profile(m, user)
    elif m.text == "Нет":
        await bot.send_message(m.chat.id, "Тогда назови своё настоящее имя!")
        shopStatus[m.from_user.id] = 'reg_nick'



async def shopsell(call, user):
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Смотрим что можно продать...") 
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if user.location == 'Хэвенбург' and user.position == 'Площадь' or user.location == 'Город' and user.position == 'Площадь' or user.location == 'Кавайня' and user.position == 'Площадь':
        pass
    else:
        await bot.edit_message_text("Вы находитесь вне площади", call.message.chat.id, call.message.message_id)
        return
    inventory = await db.Inventory.filter(~Q(type="Растение"), idplayer=user.id, active=1)
    text = "Выберите предмет на продажу:\n\n"
    passed = 0
    for item in inventory:
        checkShop = await db.Shop.filter(name=item.name).order_by('-id').limit(1)
        if checkShop:
            for z in checkShop:
                price = int(z.price / 3)
                text += "{} - {}💰 /lombard_sell_{}\n".format(item.name, price, item.id)
            passed = 1
    if passed == 0:
        text = "Ну и что это ты мне принёс? Еще бы консервных банок насобирал! Мне такой хлам не нужен!"
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(call.message.chat.id, text[x:x+4096])
    else:
        await bot.send_message(call.message.chat.id, text)


async def backtoshop(call, user):
    m1 = call.from_user.id
    m2 = call.message.chat.id
    m3 = call.message.message_id
    await shop(m1, m2, m3)

@dp.message_handler(lambda m:m.text and m.text.startswith('/lombard_sell_'))
async def lombardsell(m):
    result = m.text.replace('/lombard_sell_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    itemId = result
    item = await db.Inventory.get_or_none(id=itemId)
    if item:
        items = await db.Inventory.filter(name=item.name, idplayer=item.idplayer, active=1).count()
        if items > 1:
            coinUserStatus[m.from_user.id] = 'sellItem_{}'.format(item.id)
            await bot.send_message(m.chat.id, "У тебя x{} {}. Введи количество продаваемых предметов.".format(items, item.name))
            return
    user = await db.Users.get(user_id=m.from_user.id)
    if user.location != 'Хэвенбург' and user.location != 'Кавайня' and user.location != 'Город':
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    if not item or item.active != 1 or item.idplayer != user.id:
        text = "Ошибка. Предмета не существует"
        await bot.send_message(m.chat.id, text)
        return
    else:
        await db.Inventory.filter(id=itemId).delete()
        checkShop = await db.Shop.filter(name=item.name).order_by('-id').limit(1)
        if checkShop:
            for z in checkShop:
                price = int(z.price / 3)
        await db.Users.filter(id=user.id).update(money=F('money') + int(price))
        checkInSell = await db.Shop.filter(name=item.name).order_by('-count').limit(1)
        await db.Shop.filter(id=checkInSell[0].id).update(count=F('count') + 1)
        text = "Вы успешно продали {} за {}💰\n".format(item.name, price)
        await logBot.send_message(tradeChat, "[ЛОМБАРД] Игрок {} продал {} за {}💰".format(user.username, item.name, price))
        await achprog(user, ach='lombarder')
        await bot.send_message(m.chat.id, text)




@dp.message_handler(lambda m: coinUserStatus and m.from_user.id == m.chat.id and m.from_user.id in coinUserStatus and coinUserStatus[m.from_user.id] and coinUserStatus[m.from_user.id].startswith('sellItem_'))
async def lombardSellStep2(m):
    user = await db.Users.get(user_id=m.from_user.id)
    _itemId = coinUserStatus[m.from_user.id].split("_")
    itemId =  _itemId[1]
    if not itemId:
        coinUserStatus[m.from_user.id] = None
    item = await db.Inventory.get_or_none(id=itemId)
    if not item:
        coinUserStatus[m.from_user.id] = None
    coinUserStatus[m.from_user.id] = None
    success = 0
    checkOther = await db.Inventory.filter(name=item.name, active=1, idplayer=item.idplayer).count()
    try:
        count = int(m.text)
    except:
        await bot.send_message(m.chat.id, "Ты ввёл не число. Действие отменено")
        return
    if count > 0:
        pass
    else:
        await bot.send_message(m.chat.id, "Ошибка")
        return
    if count > checkOther: count = checkOther 
    items = await db.Inventory.filter(name=item.name, idplayer=item.idplayer, active=1).limit(count)
    success = 0
    price = 0
    profit = 0
    for x in items:
        if user.location != 'Хэвенбург' and user.location != 'Кавайня' and user.location != 'Город':
            await bot.send_message(m.chat.id, "Вы находитесь вне города")
            return
        if not item or item.active != 1 or item.idplayer != user.id:
            text = "Ошибка. Предмета не существует"
            await bot.send_message(m.chat.id, text)
            return
        else:
            itm = await db.Inventory.get(id=x.id)
            await itm.delete()
            checkShop = await db.Shop.filter(name=x.name).order_by('-id').limit(1)
            if checkShop:
                for z in checkShop:
                    price = int(z.price / 3)
            await db.Users.filter(id=user.id).update(money=F('money') + int(price))
            checkInSell = await db.Shop.filter(name=item.name).order_by('-count').limit(1)
            await db.Shop.filter(id=checkInSell[0].id).update(count=F('count') + 1)
            success += 1
            profit += price
            await achprog(user, ach='lombarder')
    await bot.send_message(m.chat.id, "Ты успешно продал х{} {} и получил {}💰".format(success, item.name, profit))
    await logBot.send_message(tradeChat, "[ЛОМБАРД] Игрок {} продал x{} {} за {}💰".format(user.username, success, item.name, profit))






###############
#   СКУПЩИК   #
###############
async def bomjsell(call, user):
    if user.location == 'Хэвенбург' and user.position == 'Площадь':
        pass
    else:
        await bot.edit_message_text("Вы находитесь вне площади", call.message.chat.id, call.message.message_id)
        return
    inventory = await db.Inventory.filter(idplayer=user.id, active=1, type='Хлам')
    text = "Выберите предмет на продажу:\n\n"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    passed = 0
    for item in inventory:
        if item.name == 'Перо ястреба':
            pass
        else:
            passed = 1
            name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
            text += "{}\n".format(name)
            markup.add(InlineKeyboardButton('Продать {}'.format(name), callback_data="bomj_sell_{}".format(item.id)))
    if passed == 0:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вам нечего предложить")
        return                
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)


async def bomj_sell(call, user):
    sh = call.data.split('_')
    itemId = sh[2]
    item = await db.Inventory.exists(id=itemId)
    if item:
        item = await db.Inventory.get(id=itemId)
    else:
        await bot.edit_message_text("Ошибка. Предмета не существует.", call.message.chat.id, call.message.message_id)
        return
    if item.active != 1:
        text = "Ошибка. Предмета не существует"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        return
    else:
        await db.Inventory.filter(id=itemId).delete()
        price = random.randint(20, 55)
        await db.Users.filter(id=user.id).update(money=F('money') + int(price))
        if user.quest == 'Поставщик':
            quest = await db.tempQuest.filter(user_id=user.user_id, quest=user.quest, status=0)
            if quest:
                await db.tempQuest.filter(id=quest[0].id).update(progress=F('progress') + 1)
        text = "Вы успешно продали {} за {}💰".format(item.name, price)
        await achprog(user, ach='skupshik')
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
        await logBot.send_message(tradeChat, "[СКУПЩИК] Игрок {} продал скупщику {} за {}💰".format(user.username, item.name, price))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown', reply_markup=markup)









#####################
#      uniqShop     #
#####################

async def defShop(call, user):
    checkQuest = await db.Quests.get_or_none(name='Хрен с горы', idplayer=user.id)
    count = user.heavenCurrency
    if checkQuest and checkQuest.status == 2:
        
        donateinv = await db.Inventory.exists(name='Ивент инвентарь', idplayer=user.id)
        kotelok = await db.Inventory.exists(name='Котелок', idplayer=user.id, active=1)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        text = """👺Драконоборец – он же хрен с горы (буквально). Таинственный незнакомец, прибывший, как он говорит, с близлежащих гор, где охота на чешую виверн перестала приносить должной выгоды.

    Собственно, потому он и здесь, готов слепить из твоих чешуек что-нибудь полезное, а часть из них отправить себе в карман в качестве платы.

    —Что? Зачем мне столько чешуек? А тебя колышет? Либо обменивайся, либо проваливай.
    У вас {}🔻

    Ассортимент:
    🧢Колючая маска | +41🛡 | 🔻51
    🦺Багровый жилет | +57🛡 | 🔻58
    👖Багровые поножи | +50🛡 | 🔻55
    🥾Ботинки с шипами | +37🛡 | 🔻48
    🛡Щит-крыло | +36🛡 | 🔻54
    🧫Чешуйчатое снадобье | ❤️+40 (можно сверх лимита) | 🔻10
    🧨Багровая бомба | 20%🔪 по всем находящимся на квадрате игрокам| 🔻13""".format(count)
        if donateinv:
            pass
        else:
            text += "\n\n+3📦. Можно купить и расширить инвентарь | 🔻135"
            markup.add(InlineKeyboardButton('+3📦', callback_data="defshBuy_1"))
        if kotelok:
            pass
        else:
            text += "\n🥘Котелок | Позволяет варить зелья и не только | 🔻10"
            markup.add(InlineKeyboardButton('🥘Котелок', callback_data="defshBuy_9"))
        text += "\n📦Коробка с сюрпризом | Внутри лежит 🔥Осколок Огня, 🔶Амулет здоровья, 🚥Анти-анализатор БМ, 👘Плащ-невидимка, 🧩Кусок паззла, 🟧Осколок эфира или 🟦Осколок льда! | 🔻250"
        markup.add(InlineKeyboardButton('🧢Колючая маска', callback_data="defshBuy_2"))
        markup.add(InlineKeyboardButton('🦺Багровый жилет', callback_data="defshBuy_3"))
        markup.add(InlineKeyboardButton('👖Багровые поножи', callback_data="defshBuy_4"))
        markup.add(InlineKeyboardButton('🥾Ботинки с шипами', callback_data="defshBuy_5"))
        markup.add(InlineKeyboardButton('🛡Щит-крыло', callback_data="defshBuy_6"))
        markup.add(InlineKeyboardButton('🧫Чешуйчатое снадобье', callback_data="defshBuy_7"))
        markup.add(InlineKeyboardButton('🧨Багровая бомба', callback_data="defshBuy_8"))
        markup.add(InlineKeyboardButton('📦Коробка с сюрпризом', callback_data="defshBuy_10"))
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')

    elif checkQuest and checkQuest.status == 1:
        if count > 0:
            await bot.edit_message_text("Принёс ты, значит, драконоборцу эту чешую. Понюхав её и лизнув, он произнёс:\n-Окей, твой товар не палёнка. Это хорошо, но если ты вдруг мне принесёшь что-то не то, тебе не поздоровится, понял?\n⚠️Задание выполнено. Получен доступ к 👺Драконоборцу + 500💰", call.message.chat.id, call.message.message_id)
            checkQuest.status = 2
            await checkQuest.save()
            await db.Users.filter(id=user.id).update(money=F('money') + 500)
        else:
            await bot.edit_message_text("Подойдя к драконоборцу, он послал тебя подальше. Если быть точнее, то принести ему товар дабы убедиться что ты не очередной кидала с Авито.", call.message.chat.id, call.message.message_id)
    
    else:
        plusText = await giveQuest(user, 'Хрен с горы')
        await bot.edit_message_text("👺Драконоборец - как красиво звучит! Хотя видок у него стрёмный... Больше напоминает какого-то гопника. С ходу он начал тебе заливать:\n-Короче, я с тобой в игрушки играть не буду. Даёшь товар, я тебе даю броню. Но для начала давай убедимся что ты не суёшь мне паль...{}".format(plusText), call.message.chat.id, call.message.message_id)

async def defshBuy(call, user):
    sh = call.data.split('_')
    item = sh[1]
    if user.location != 'Хэвенбург':
        await bot.edit_message_text("Вы находитесь вне Хэвенбурга")
        return
    countIvent = user.heavenCurrency
    count = countIvent
    donateinv = await db.Inventory.exists(name='Ивент инвентарь', idplayer=user.id)
    try:
        if usesUsrs and usesUsrs[user.id] == 1:
            await bot.edit_message_text("Ваш заказ еще готовится.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
            await defshopBuyGo(user, item, count, donateinv, countIvent, call)
    except:
        await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        await defshopBuyGo(user, item, count, donateinv, countIvent, call)


async def defshopBuyGo(user, item, count, donateinv, countIvent, call):
    usesUsrs[user.id] = 1
    count = user.heavenCurrency
    if item == '1':
        if user.heavenCurrency >= 125:
            if donateinv:
                text = "Для тебя этот товар больше не продается."
            else:
                await db.Inventory.create(name='Ивент инвентарь', active=0, size=0, type='Ивент', bonus=0, idplayer=user.id)
                await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 3, heavenCurrency=F('heavenCurrency') - 125)
                text = "Ты приобрёл +3📦"
        else:
            text = "У тебя не хватает 🔻"
    elif item == '2':
        if count >= 51:
            item = await db.Inventory.create(name='Колючая маска', active=1, size=1, type='Броня', bonus=41, idplayer=user.id, atk_block=2)
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 51)
            text = "Ты обменял 🔻 на 🧢Колючая маска"
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🔻"
    elif item == '3':
        if count >= 58:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 58)
            item = await db.Inventory.create(name='Багровый жилет', active=1, size=2, type='Броня', bonus=57, idplayer=user.id, atk_block=2)
            text = "Ты обменял 🔻 на 🦺Багровый жилет"
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🔻"
    elif item == '4':
        if count >= 55:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 55)
            text = "Ты обменял 🔻 на 👖Багровые поножи"
            addItem = await db.Inventory.create(name='Багровые поножи', active=1, size=1, type='Броня', bonus=50, idplayer=user.id, atk_block=2)
            await db.commitInventory(user, addItem)
        else:
            text = "У тебя не хватает 🔻"
    elif item == '5':
        if count >= 48:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 48)
            text = "Ты обменял 🔻 на 🥾Ботинки с шипами"
            item = await db.Inventory.create(name='Ботинки с шипами', active=1, size=1, type='Броня', bonus=37, idplayer=user.id, atk_block=2)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🔻"
    elif item == '6':
        if count >= 54:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 54)
            text = "Ты обменял 🔻 на 🛡Щит-крыло"
            item = await db.Inventory.create(name='Щит-крыло', active=1, size=3, type='Броня', bonus=36, idplayer=user.id)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🔻"
    elif item == '7':
        if count >= 10:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 10)
            item = await db.Inventory.create(name='Чешуйчатое снадобье', active=1, size=1, type='Зелье', bonus=40, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🔻 на 🧫Чешуйчатое снадобье"
        else:
            text = "У тебя не хватает 🔻"
    elif item == '8':
        if count >= 13:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 13)
            item = await db.Inventory.create(name='Багровая бомба', active=1, size=1, type='Экипировка', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🔻 на 🧨Багровая бомба"
        else:
            text = "У тебя не хватает 🔻"
    elif item == '9':
        if count >= 10:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 10)
            item = await db.Inventory.create(name='Котелок', active=1, size=2, type='Экипировка', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🔻 на 🥘Котелок"
        else:
            text = "У тебя не хватает 🔻"
    elif item == '10':
        if count >= 250:
            await db.Users.filter(id=user.id).update(heavenCurrency=F('heavenCurrency') - 250)
            text = "Ты обменял 🔻 на 📦Коробку с сюрпризом. Смотрим что внутри..."
            await bot.send_message(call.message.chat.id, text)
            await opendonatecase(user)
            usesUsrs[user.id] = 0
            return
        else:
            text = "У тебя не хватает 🔻"
    await bot.send_message(call.message.chat.id, text)
    usesUsrs[user.id] = 0

async def winterShop(call, user):
    checkQuest = await db.Quests.get_or_none(name='Мастер на все руки', idplayer=user.id).first()
    if checkQuest and checkQuest.status == 2:
        donateinv = await db.Inventory.exists(name='Ивент инвентарь 2', idplayer=user.id)
        count = user.kawaiCurrency
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        text = """_Лавочка лысего! Предложение этого сезона:
    🧢Шапка-ушанка | + 45🛡 -10%❄️ | 🧊 1550
    🧥АШуба | + 60🛡 -20%❄️ | 🧊 2450
    🩳Летние шорты | + 52🛡 -10%❄️ | 🧊 2175
    🥾Зимние калоши | + 45🛡 -15%❄️ | 🧊 1750 
    🛡Самонагревающаяся покрышка | + 40🛡 -20%❄️ | 🧊 2300
    Уже в продаже!_
    У вас {}🧊

    Дополнительный ассортимент:""".format(count)
        if donateinv:
            pass
        else:
            text += "\n\n+3📦. Можно купить и расширить инвентарь | 🧊 2025"
            markup.add(InlineKeyboardButton('+3📦', callback_data="wintershBuy_1"))
        text += "📦Коробка с карточками. Внутри лежит: 🔷Камень энергии, 🍯Горшок лепрекона или 🌿Карманная дриада | 🧊 9000"
        markup.add(InlineKeyboardButton('🧢Шапка-ушанка', callback_data="wintershBuy_2"))
        markup.add(InlineKeyboardButton('🧥АШуба', callback_data="wintershBuy_3"))
        markup.add(InlineKeyboardButton('🩳Летние шорты', callback_data="wintershBuy_4"))
        markup.add(InlineKeyboardButton('🥾Зимние калоши', callback_data="wintershBuy_5"))
        markup.add(InlineKeyboardButton('🛡Самонагревающаяся покрышка', callback_data="wintershBuy_6"))
        markup.add(InlineKeyboardButton('🧫Чешуйчатое снадобье', callback_data="wintershBuy_7"))
        markup.add(InlineKeyboardButton('+50📦(🥘)', callback_data="wintershBuy_kotelokLimit"))
        markup.add(InlineKeyboardButton('📦Коробка с карточками', callback_data="wintershBuy_9"))
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_wintercity_centr"))
        text += "\n🧫Чешуйчатое снадобье | ❤️+40 (можно сверх лимита) | 🧊 650"
        text += "\n+50📦(🥘) | Расширяет инвентарь котелка (лимит на каждый вид цветов) на 50📦 | 🧊 1000"
        #text += "\n🔮Погодный шар | Позволяет узнать прогноз погоды | 🧊 3500"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')


    elif checkQuest and checkQuest.status == 1:
        count = user.kawaiCurrency
        if count > 0:
            await bot.edit_message_text("Принёс ты, значит, Лысему этот снунец. Зачем-то он лизнул его и закинул в рот и... Застонал, судя по всему, от удовольствия. Что тут вообще происходит?\n-О да, мне нравится... Как же хорошо... Ладно, мне подходят твои Снунцы. Давай дальше.\n⚠️Задание выполнено. Потеряно: 1 🧊Снунец\nПолучен доступ к Лысому из Бруззерс + 750💰", call.message.chat.id, call.message.message_id)
            checkQuest.status = 2
            await checkQuest.save()
            await db.Users.filter(id=user.id).update(money=F('money') + 750, kawaiCurrency=F('kawaiCurrency') - 1)
        else:
            await bot.edit_message_text("Подойдя к Лысему, он послал тебя подальше. Если быть точнее, то в Заснеженный лес, где ты сможешь получить 🧊Снунцы. Какой-то он нервный...", call.message.chat.id, call.message.message_id)
    
    else:
        plusText = await giveQuest(user, 'Мастер на все руки')
        await bot.edit_message_text("Ах, какой мужчина! По голому торсу видно накачанное тело, а позади него висит много одежды с подписями на них - ''Сантехник'', ''Монтажник'', ''Доктор''... Ух ты, неужели этот человек чинит трубы, пока подключает интернет и лечит людей... Что?\n-Долго стоять будешь, не видишь, у меня вызов?.. А, стоп, так ты тут новенький? Интим или броня? Если броня, дай проверить твои 🧊Снунцы... Не знаешь что это? Мда уж.. Иди в лес, узнаешь из тысячи! {}".format(plusText), call.message.chat.id, call.message.message_id)



usesUsrs = {}
async def wintershopBuy(call, user):
    sh = call.data.split('_')
    item = sh[1]
    if user.location != 'Кавайня':
        await bot.edit_message_text("Вы находитесь вне Кавайни")
        return
    countIvent = user.kawaiCurrency
    count = countIvent
    try:
        if usesUsrs and usesUsrs[user.id] == 1:
            await bot.edit_message_text("Ваш заказ еще готовится.", call.message.chat.id, call.message.message_id)
        else:
            donateinv = await db.Inventory.exists(name='Ивент инвентарь 2', idplayer=user.id)
            await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
            await wintershopBuyGo(user, item, count, donateinv, countIvent, call)
    except:
        await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        donateinv = await db.Inventory.exists(name='Ивент инвентарь 2', idplayer=user.id)
        await wintershopBuyGo(user, item, count, donateinv, countIvent, call)


async def wintershopBuyGo(user, item, count, donateinv, countIvent, call):
    usesUsrs[user.id] = 1
    count = user.kawaiCurrency
    if item == '1':
        if count >= 2025:
            if donateinv:
                text = "Для тебя этот товар больше не продается."
            else:
                await db.Inventory.create(name='Ивент инвентарь 2', active=0, size=0, type='Ивент', bonus=0, idplayer=user.id)
                await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 3, kawaiCurrency=F('kawaiCurrency') - 2025)
                text = "Ты приобрёл +3📦"
        else:
            text = "У тебя не хватает Снунцов"
    elif item == '2':
        if count >= 1550:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 1550)
            item = await db.Inventory.create(name='Шапка-ушанка', active=1, size=1, type='Броня', bonus=45, idplayer=user.id, atk_block=4)
            await db.commitInventory(user, item)
            text = "Ты обменял 🧊 на 🧢Шапка-ушанка"
        else:
            text = "У тебя не хватает 🧊"
    elif item == '3':
        if count >= 2450:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 2450)
            item = await db.Inventory.create(name='АШуба', active=1, size=2, type='Броня', bonus=60, idplayer=user.id, atk_block=4)
            await db.commitInventory(user, item)
            text = "Ты обменял 🧊 на 🧥АШуба"
        else:
            text = "У тебя не хватает 🧊"
    elif item == '4':
        if count >= 2175:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 2175)
            text = "Ты обменял 🧊 на 🩳Летние шорты"
            item = await db.Inventory.create(name='Летние шорты', active=1, size=1, type='Броня', bonus=52, idplayer=user.id, atk_block=4)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🧊"
    elif item == '5':
        if count >= 1750:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 1750)
            text = "Ты обменял 🧊 на 🥾Зимние калоши"
            item = await db.Inventory.create(name='Зимние калоши', active=1, size=1, type='Броня', bonus=45, idplayer=user.id, atk_block=4)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🧊"
    elif item == '6':
        if count >= 2300:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 2300)
            text = "Ты обменял 🧊 на 🛡Самонагревающаяся покрышка"
            item = await db.Inventory.create(name='Самонагревающаяся покрышка', active=1, size=3, type='Броня', bonus=40, idplayer=user.id)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🧊"
    elif item == '7':
        if count >= 650:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 650)
            item = await db.Inventory.create(name='Чешуйчатое снадобье', active=1, size=1, type='Зелье', bonus=40, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🧊 на 🧫Чешуйчатое снадобье"
        else:
            text = "У тебя не хватает 🧊"
    elif item == '8':
        if count >= 3500:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 3500)
            item = await db.Inventory.create(name='Погодный шар', active=1, size=1, type='Экипировка', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🧊 на 🔮Погодный шар"
        else:
            text = "У тебя не хватает 🧊"
    elif item == '9':
        if count >= 9000:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 9000)
            await db.addItem('Коробка с карточками', user, arg='a')
            text = "Ты обменял 🧊 на 📦Коробку с карточками."
        else:
            text = "У тебя не хватает 🧊"
    elif item == 'kotelokLimit':
        if count >= 1000:
            await db.Users.filter(id=user.id).update(kawaiCurrency=F('kawaiCurrency') - 1000)
            await db.Users.filter(id=user.id).update(kotelokLimit=F('kotelokLimit') + 50)
            text = "Ты обменял 🧊 на +50📦(🥘)"
        else:
            text = "У тебя не хватает 🧊"
    await bot.send_message(call.message.chat.id, text)
    usesUsrs[user.id] = 0



async def oceanshop(call, user):
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 3', idplayer=user.id)
    countIvent = user.oceanCurrency
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = """_В этом сезоне у Табернама вы можете приобрести следующие предметы:
🥽Очки | + 80🛡 -10%☁️ -8%⚔️ | 💧 120
🩱Купальник Раскуловой | + 90🛡 -25%☁️ -8%⚔️ | 💧 145
🩲Плавки | + 75🛡 -15%☁️ -8%⚔️ | 💧 125
🛶Дырявая лодка | + 65🛡 -25%☁️ -8%⚔️ | 💧 115
Уже в продаже!_
У вас {}💧

Дополнительный ассортимент:

🧻Полотенце | Позволяет сбивать влажность | 100 💰
""".format(countIvent)
    checkTp = await db.Inventory.exists(name='Пятый сектор', idplayer=user.id)
    if not checkTp:
        markup.add(InlineKeyboardButton('📜Свиток телепорта на пятый сектор пирамиды', callback_data="ocshBuy_9"))
        text += "\n📜Свиток телепорта на пятый сектор пирамиды | 💧 375"
    text += "\n🎣Простая удочка | Позволяет рыбачить в пруде Окус Локуса | 💧 150"
    if donateinv:
        pass
    else:
        text += "+4📦. Можно купить и расширить инвентарь | 💧 65"
        markup.add(InlineKeyboardButton('+4📦', callback_data="ocshBuy_1"))
    markup.add(InlineKeyboardButton('🥽Очки', callback_data="ocshBuy_2"))
    markup.add(InlineKeyboardButton('🩱Купальник Раскуловой', callback_data="ocshBuy_3"))
    markup.add(InlineKeyboardButton('🩲Плавки', callback_data="ocshBuy_4"))
    markup.add(InlineKeyboardButton('🛶Дырявая лодка', callback_data="ocshBuy_5"))
    markup.add(InlineKeyboardButton('🧻Полотенце', callback_data="ocshBuy_6"))
    markup.add(InlineKeyboardButton('🎣Простая удочка', callback_data="ocshBuy_8"))
    markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_oceanus_centr"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')

async def ocshopbuy(call, user):
    sh = call.data.split('_')
    item = sh[1]
    if user.location != 'Океанус':
        await bot.edit_message_text("Вы находитесь вне Океануса")
        return
    count = user.oceanCurrency
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 3', idplayer=user.id)
    try:
        if usesUsrs and usesUsrs[user.id] == 1:
            await bot.edit_message_text("Ваш заказ еще готовится.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
            await ochopBuyGo(user, item, count, donateinv, call)
    except:
        await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        await ochopBuyGo(user, item, count, donateinv, call)


async def ochopBuyGo(user, item, count, donateinv, call):
    usesUsrs[user.id] = 1
    count = user.oceanCurrency
    if item == '1':
        if count >= 65:
            if donateinv:
                text = "Для тебя этот товар больше не продается."
            else:
                await db.Inventory.create(name='Ивент инвентарь 3', active=0, size=0, type='Ивент', bonus=0, idplayer=user.id)
                await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 4, oceanCurrency=F('oceanCurrency') - 65)
                text = "Ты приобрёл +4📦"
        else:
            text = "У тебя не хватает 💧"
    elif item == '2':
        if count >= 120:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 120)
            item = await db.Inventory.create(name='Очки', active=1, size=1, type='Броня', bonus=80, idplayer=user.id, atk_block=8)
            await db.commitInventory(user, item)
            text = "Ты обменял 💧 на 🥽Очки"
        else:
            text = "У тебя не хватает 💧"
    elif item == '3':
        if count >= 145:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 145)
            item = await db.Inventory.create(name='Купальник Раскуловой', active=1, size=2, type='Броня', bonus=90, idplayer=user.id, atk_block=8)
            await db.commitInventory(user, item)
            text = "Ты обменял 💧 на 🩱Купальник Раскуловой"
        else:
            text = "У тебя не хватает 💧"
    elif item == '4':
        if count >= 125:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 125)
            text = "Ты обменял 💧 на 🩲Плавки"
            item = await db.Inventory.create(name='Плавки', active=1, size=1, type='Броня', bonus=75, idplayer=user.id, atk_block=8)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 💧"
    elif item == '5':
        if count >= 115:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 115)
            text = "Ты обменял 💧 на 🛶Дырявая лодка"
            item = await db.Inventory.create(name='Дырявая лодка', active=1, size=1, type='Броня', bonus=65, idplayer=user.id, atk_block=8)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 💧"
    elif item == '6':
        if user.money >= 100:
            success = await db.addItem('Полотенце', user)
            if success:
                await db.Users.filter(id=user.id).update(money=F('money') - 100)
                text = "Ты купил 🧻Полотенце"
            else:
                text = "У тебя не хватает места в инвентаре."
        else:
            text = "У тебя не хватает 💰"
    elif item == '8':
        if count >= 150:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 150)
            item = await db.Inventory.create(name='Простая удочка', active=1, size=2, type='Рыбалка', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 💧 на 🎣Простая удочка"
        else:
            text = "У тебя не хватает 💧"
    elif item == '9':
        if count >= 375:
            await db.Users.filter(id=user.id).update(oceanCurrency=F('oceanCurrency') - 375)
            item = await db.Inventory.create(name='Пятый сектор', active=0, size=0, type='Прочее', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 💧 на 📜Свиток телепорта на пятый сектор пирамиды"
        else:
            text = "У тебя не хватает 💧"
    await bot.send_message(call.message.chat.id, text)
    usesUsrs[user.id] = 0


async def radarshop(call, user):
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 4', idplayer=user.id)
    countIvent = user.radarCurrency
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = """_Табервам! И вашим и нашим! Лучшая броня, идеальная защита, и не только!
⛑Шлем усиленный | + 65🛡 -6%⚔️ | ♦️ 300
🧥Плащ-уящ | + 70🛡 -6%⚔️ | ♦️ 325
🩳Шортики | + 60🛡 -6%⚔️ | ♦️ 275
🥾Сталкерские ботинки | + 50🛡 -6%⚔️ | ♦️ 285
Уже в продаже!_
У вас {}♦️

Дополнительный ассортимент:

500🧿 | Используется у Сыча | 40♦️
""".format(countIvent)
    if donateinv:
        pass
    else:
        text += "+5📦. Можно купить и расширить инвентарь | ♦️ 200"
        markup.add(InlineKeyboardButton('+5📦', callback_data="radarBuy_1"))
    markup.add(InlineKeyboardButton('⛑Шлем усиленный', callback_data="radarBuy_2"))
    markup.add(InlineKeyboardButton('🧥Плащ-уящ', callback_data="radarBuy_3"))
    markup.add(InlineKeyboardButton('🩳Шортики', callback_data="radarBuy_4"))
    markup.add(InlineKeyboardButton('🥾Сталкерские ботинки', callback_data="radarBuy_5"))
    markup.add(InlineKeyboardButton('500🧿', callback_data="radarBuy_6"))
    markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_radar_centr"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')

async def radarBuy(call, user):
    sh = call.data.split('_')
    item = sh[1]
    if user.location != 'Радар':
        await bot.edit_message_text("Вы находитесь вне Радара")
        return
    count = user.radarCurrency
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 4', idplayer=user.id)
    try:
        if usesUsrs and usesUsrs[user.id] == 1:
            await bot.edit_message_text("Ваш заказ еще готовится.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
            await radarBuyGo(user, item, count, donateinv, call)
    except:
        await bot.edit_message_text("_Ща сделаю_\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        await radarBuyGo(user, item, count, donateinv, call)


async def radarBuyGo(user, item, count, donateinv, call):
    usesUsrs[user.id] = 1
    if item == '1':
        if count >= 200:
            if donateinv:
                text = "Для тебя этот товар больше не продается."
            else:
                await db.Inventory.create(name='Ивент инвентарь 4', active=0, size=0, type='Ивент', bonus=0, idplayer=user.id)
                await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 5, radarCurrency=F('radarCurrency') - 200)
                text = "Ты приобрёл +5📦"
        else:
            text = "У тебя не хватает ♦️"
    elif item == '2':
        if count >= 300:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 300)
            item = await db.Inventory.create(name='Шлем усиленный', active=1, size=1, type='Броня', bonus=65, idplayer=user.id, atk_block=6)
            await db.commitInventory(user, item)
            text = "Ты обменял ♦️ на ⛑Шлем усиленный"
        else:
            text = "У тебя не хватает ♦️"
    elif item == '3':
        if count >= 325:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 325)
            item = await db.Inventory.create(name='Плащ-уящ', active=1, size=2, type='Броня', bonus=70, idplayer=user.id, atk_block=6)
            await db.commitInventory(user, item)
            text = "Ты обменял ♦️ на 🧥Плащ-уящ"
        else:
            text = "У тебя не хватает ♦️"
    elif item == '4':
        if count >= 275:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 245)
            text = "Ты обменял ♦️ на 🩳Шортики"
            item = await db.Inventory.create(name='Шортики', active=1, size=1, type='Броня', bonus=60, idplayer=user.id, atk_block=6)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает ♦️"
    elif item == '5':
        if count >= 285:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 255)
            text = "Ты обменял ♦️ на 🥾Сталкерские ботинки"
            item = await db.Inventory.create(name='Сталкерские ботинки', active=1, size=1, type='Броня', bonus=50, idplayer=user.id, atk_block=6)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает ♦️"
    elif item == '6':
        if count >= 40:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 40, shmekli=F('shmekli') + 500)
            text = "Ты успешно обменял ♦️ на 500🧿"
        else:
            text = "У тебя не хватает ♦️"
    elif item == '8':
        if count >= 40:
            await db.Users.filter(id=user.id).update(radarCurrency=F('radarCurrency') - 40)
            await db.Users.filter(id=user.id).update(artSize=F('artSize') + 5)
            text = "Ты обменял ♦️ на +5📦 (Мешочек для хлама)"
        else:
            text = "У тебя не хватает ♦️"
    await bot.send_message(call.message.chat.id, text)
    usesUsrs[user.id] = 0


async def metroshop(call, user):
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 5', idplayer=user.id)
    countIvent = user.metroCurrency
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = """_Консервных банок нет, но есть кое-что поинтереснее:
🥽Шлем | + 95🛡 -10%⚔️ | 🗝 120
👕Костюм химзащиты | + 110🛡 -10%⚔️ | 🗝 145
🩳Шортики 2.0 | + 90🛡 -10%⚔️ | 🗝 125
🥾Противорадиационные ботинки | + 85🛡 -10%⚔️ | 🗝 115
Уже в продаже!_
У вас {}🗝

Дополнительный ассортимент:

🤿Противогаз | Жизненно необходим в Метро | 2000 💰
🕳Фильтры | Помогут прожить тебе на 5-К дольше | 1 🗝

""".format(countIvent)
    if donateinv:
        pass
    else:
        text += "+4📦. Можно купить и расширить инвентарь | 🗝 150"
        markup.add(InlineKeyboardButton('+4📦', callback_data="mtshBuy_1"))
    text += "\n🎣Непростая удочка | Позволяет рыбачить в пруде Окус Локуса | 🗝 150"
    text += "\n📦Коробка с рецептом | Попытайте удачу и достаньте изнутри один из рецептов для котелка! | 🗝 200"
    markup.add(InlineKeyboardButton('🥽Шлем', callback_data="mtshBuy_2"))
    markup.add(InlineKeyboardButton('👕Костюм химзащиты', callback_data="mtshBuy_3"))
    markup.add(InlineKeyboardButton('🩳Шортики 2.0', callback_data="mtshBuy_4"))
    markup.add(InlineKeyboardButton('🥾Противорадиационные ботинки', callback_data="mtshBuy_5"))
    markup.add(InlineKeyboardButton('🤿Противогаз', callback_data="mtshBuy_6"))
    markup.add(InlineKeyboardButton('🕳Фильтры', callback_data="mtshBuy_7"))
    markup.add(InlineKeyboardButton('🎣Непростая удочка', callback_data="mtshBuy_8"))
    markup.add(InlineKeyboardButton('📦Коробка с рецептом', callback_data="mtshBuy_9"))
    markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_metro_centr"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')

async def mtshBuy_(call, user):
    sh = call.data.split('_')
    item = sh[1]
    if user.location != 'Метро':
        await bot.edit_message_text("Вы находитесь вне Метро")
        return
    count = user.metroCurrency
    donateinv = await db.Inventory.exists(name='Ивент инвентарь 5', idplayer=user.id)
    try:
        if usesUsrs and usesUsrs[user.id] == 1:
            await bot.edit_message_text("Ваш заказ еще готовится.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("_Неплохо, хороший товар..._\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
            await mtshBuyGo(user, item, count, donateinv, call)
    except:
        await bot.edit_message_text("_Неплохо, хороший товар..._\n\nПодготовка покупки может занять некоторое время, пожалуйста, подождите.", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        await mtshBuyGo(user, item, count, donateinv, call)


async def mtshBuyGo(user, item, count, donateinv, call):
    usesUsrs[user.id] = 1
    count = user.metroCurrency
    if item == '1':
        if count >= 150:
            if donateinv:
                text = "Для тебя этот товар больше не продается."
            else:
                await db.Inventory.create(name='Ивент инвентарь 5', active=0, size=0, type='Ивент', bonus=0, idplayer=user.id)
                await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 4, metroCurrency=F('metroCurrency') - 150)
                text = "Ты приобрёл +4📦"
        else:
            text = "У тебя не хватает 🗝"
    elif item == '2':
        if count >= 120:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 120)
            item = await db.Inventory.create(name='Шлем', active=1, size=1, type='Броня', bonus=95, idplayer=user.id, atk_block=10)
            await db.commitInventory(user, item)
            text = "Ты обменял 🗝 на 🥽Шлем"
        else:
            text = "У тебя не хватает 🗝"
    elif item == '3':
        if count >= 145:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 145)
            item = await db.Inventory.create(name='Костюм химзащиты', active=1, size=2, type='Броня', bonus=110, idplayer=user.id, atk_block=10)
            await db.commitInventory(user, item)
            text = "Ты обменял 🗝 на 👕Костюм химзащиты"
        else:
            text = "У тебя не хватает 🗝"
    elif item == '4':
        if count >= 125:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 125)
            text = "Ты обменял 🗝 на 🩳Шортики 2.0"
            item = await db.Inventory.create(name='Шортики 2.0', active=1, size=1, type='Броня', bonus=90, idplayer=user.id, atk_block=10)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🗝"
    elif item == '5':
        if count >= 115:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 115)
            text = "Ты обменял 🗝 на 🥾Противорадиационные ботинки"
            item = await db.Inventory.create(name='Противорадиационные ботинки', active=1, size=1, type='Броня', bonus=85, idplayer=user.id, atk_block=10)
            await db.commitInventory(user, item)
        else:
            text = "У тебя не хватает 🗝"
    elif item == '6':
        if user.money >= 2000:
            success = await db.addItem('Противогаз', user)
            if success:
                await db.Users.filter(id=user.id).update(money=F('money') - 2000)
                text = "Ты купил 🤿Противогаз"
            else:
                text = "У тебя не хватает места в инвентаре."
        else:
            text = "У тебя не хватает 💰"
    elif item == '7':
        if count >= 1:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 1)
            await db.addItem('Фильтры', user, arg='1')
            text = "Ты обменял 🗝 на 🕳Фильтры"
        else:
            text = "У тебя не хватает 🗝"
    elif item == '8':
        if count >= 150:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 150)
            item = await db.Inventory.create(name='Непростая удочка', active=1, size=2, type='Рыбалка', bonus=0, idplayer=user.id)
            await db.commitInventory(user, item)
            text = "Ты обменял 🗝 на 🎣Непростая удочка"
        else:
            text = "У тебя не хватает 🗝"
    elif item == '9':
        if count >= 200:
            await db.Users.filter(id=user.id).update(metroCurrency=F('metroCurrency') - 200)
            await bot.edit_message_text("Вы успешно приобрели 📦Коробку с рецептом. Смотрим что внутри...", call.message.chat.id, call.message.message_id)
            await opendonatecaseRecipy(user)
            await logBot.send_message(tradeChat, "Игрок {} приобрёл в Метро Коробку с рецептом".format(user.username))
            usesUsrs[user.id] = 0
            return
        else:
            text = "У тебя не хватает 🗝"


    await bot.send_message(call.message.chat.id, text)
    usesUsrs[user.id] = 0










###############
#  RASKULOVA  #
###############
lotEditors = {}
lotUserStatus = {}


async def raskulova(call, user): 
    if True:
        checkQuest = await db.Quests.get_or_none(name='Богиня Хэвенбурга', idplayer=user.id).first()
        if checkQuest and checkQuest.status == 1:
            checkItem = await db.Inventory.get_or_none(~Q(active=0), name='Нижнее бельё Раскуловой', idplayer=user.id).first()
            if checkItem and checkItem.active == 1:
                text = "Горячая дама Раскулова, увидев тебя, сразу же подбежала, остановила твою пламенную речь и повела в коморку. Оказавшись в тёмном помещении, глядя на сексуальные движения девушки, ты почувствовал нечто странное в области паха...\n-Ну что, принёс?\nДрожащими руками ты достал из рюкзака нижнее бельё и отдал его девушке. Раскулова взяла бельё и сразу же её поведение изменилось...\n-Всё, вали отсюда, тупой мужлан. Могли бы сначала позабавиться, но ты вообще намёков не понимаешь...\nПришлось выйти за дверь..."
                text += "\n⚠️Задание выполнено. Награда: доступ в Аукционный дом Раскуловой + 500💰"
                await db.Users.filter(id=user.id).update(money=F('money') + 500)
                checkItem.active = 0
                checkQuest.status = 2
                await checkItem.save()
                await checkQuest.save()
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            elif checkItem and checkItem.active == 2:
                text = "Войдя в помещение, ты сразу же почувствовал весьма дурную атмосферу. Раскулова стояла вдалеке и сначала офигела с твоего вида, после повела в коморку. Оказавшись в тёмном помещении, ты почувствовал странное головокружение и последним, что ты услышал, были слова Раскуловой\n-Ненавижу вас, тупых фетишистов, не всех война убила...\n\nПришёл в себя ты уже на площади."
                text += "\n⚠️Задание выполнено. Награда: доступ в Аукционный дом Раскуловой"
                checkItem.active = 0
                checkQuest.status = 2
                await checkItem.save()
                await checkQuest.save()
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("Зайдя внутрь, к тебе подошла Раскулова и спросила что там по делу. Увы, ты не нашёл что ей ответить. Тебя выпроводили за дверь.", call.message.chat.id, call.message.message_id)
            return
        elif checkQuest and checkQuest.status == 2:
            pass
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    texts = ['Сверяем лоты...', 'Уточняем детали...', 'Проверяем информацию...']
    notifText = random.choice(texts)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=notifText) 
    if user.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)
        return
    markup = InlineKeyboardMarkup(row_width=2)
    _kach = call.data.split('_')
    kach = _kach[1]
    if kach == 'buy':
        text = "Аукционный дом Раскуловой приветствует вас! Выберите категорию предметов:"
        markup.add(InlineKeyboardButton('🍔Еда', callback_data="raskulselecttype_eat"))
        markup.add(InlineKeyboardButton('🔩Расходники', callback_data="raskulselecttype_heals"))
        markup.add(InlineKeyboardButton('🛡Броня', callback_data="raskulselecttype_armor"))
        markup.add(InlineKeyboardButton('💍Прочее', callback_data="raskulselecttype_other"))
        markup.add(InlineKeyboardButton('📨Автопокупка', callback_data="raskul_autobuylist"))
        return await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif kach == 'sell':
        allItems = await db.Inventory.filter(idplayer=user.id, active=1)
        commision = await db.System.get(name='commisionRaskulova')
        text = 'Выберите вещь для продажи. Коммисия Раскуловой составляет {}%:'.format(commision.value)
        zapr = ['Обломок синего камня', 'RCA', 'Цветок сакуры', 'Роза', 'Одуванчик', 'Останки героев', 'Перо ястреба', 'Тушка питона', 'Котелок', 'Кошелёк падшего героя']
        asdasd = []
        for z in allItems:
            if str(z.name) not in zapr and str(z.name) not in asdasd:
                if z.type in ['Артефакт', 'Оружие'] or z.name == 'Бустер':
                    itm = await db.Inventory.filter(id=z.id).only('lvl')
                    text += "\n{} ({}) - /raskulova_sell_{}".format(z.name, itm[0].lvl, z.id)
                else:
                    text += "\n{} - /raskulova_sell_{}".format(z.name, z.id)
                    asdasd.append(str(z.name))
    elif kach == 'lots':
        allLots = await db.Raskul.filter(~Q(status=0), owner=user.id)
        text = "Список ваших лотов:\n"
        for z in allLots:
            text += "\nЛот #{}. {} - {}{}".format(z.id, z.name, z.price, z.valute)
            markup.add(InlineKeyboardButton('Лот #{}'.format(z.id), callback_data="lot_select_{}".format(z.id)))
    elif kach == 'refresh':
        lotCheck = _kach[2]
        lot = await db.Raskul.exists(id=lotCheck)
        if lot:
            lot = await db.Raskul.get(id=lotCheck)
        if lot and lot.status != 0:
            item = await db.Inventory.get(id=lot.item)
            seller = await db.Users.get(id=item.idplayer)
            lots = await db.Raskul.filter(~Q(status=0), name=item.name).order_by('price').limit(30)
            lotMin = await db.Raskul.filter(name=item.name).order_by('price').limit(1)
            lotMax = await db.Raskul.filter(name=item.name).order_by('-price').limit(1)
            text = "Информация по {}:".format(item.name)
            for x in lotMin:
                text += "\nМинимальная цена: {}{}".format(x.price, x.valute)
            for x in lotMax:
                text += "\nМаксимальная цена: {}{}\nСписок текущих предложений:\n".format(x.price, x.valute)
            for z in lots:
                if item.type in ['Артефакт', 'Оружие'] or item.name == 'Бустер':
                    itm = await db.Inventory.filter(id=z.item).only('lvl')
                    text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm[0].lvl, z.price, z.valute, z.id)
                elif item.type in ['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки', 'Еда']:
                    itm = await db.Inventory.filter(id=z.item).only('expires')
                    leftTime = (itm[0].expires - time.time()) / 3600
                    if leftTime > 0:
                        text += "\n{} (🦴{}ч) - {}{}. Купить - /raskulova_buy_{}".format(z.name, round(leftTime, 2), z.price, z.valute, z.id)
                    else:
                        text += "\n{} (Просроченное) - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
                else:
                    text += "\n{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
            lastOrder = await db.RaskulAutoBuy.filter(name=item.name, status=1).order_by('-price').limit(1)
            plusText = ""
            if lastOrder:
                plusText = "\n\nНа этот предмет есть активные ордеры на автопокупку. Максимальная цена автопокупки составляет {}{}".format(lastOrder[0].price, lastOrder[0].valute)

        elif lot.status == 0:
            item = await db.Inventory.get(id=lot.item)
            lots = await db.Raskul.filter(~Q(status=0), name=lot.name).order_by('price').limit(30)
            lotMin = await db.Raskul.filter(name=lot.name).order_by('price').limit(1)
            lotMax = await db.Raskul.filter(name=lot.name).order_by('-price').limit(1)
            text = "Информация по {}:".format(lot.name)
            for x in lotMin:
                text += "\nМинимальная цена: {}{}".format(x.price, x.valute)
            for x in lotMax:
                text += "\nМаксимальная цена: {}{}\nСписок текущих предложений:\n".format(x.price, x.valute)
            for z in lots:
                if item.type in ['Артефакт', 'Оружие']:
                    itm = await db.Inventory.filter(id=z.item).only('lvl')
                    text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm[0].lvl, z.price, z.valute, z.id)
                elif item.type in ['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки', 'Еда']:
                    itm = await db.Inventory.get_or_none(id=z.item).only('expires')
                    if itm:
                        leftTime = (itm.expires - time.time()) / 3600
                        if leftTime > 0:
                            text += "\n{} (🦴{}ч) - {}{}. Купить - /raskulova_buy_{}".format(z.name, round(leftTime, 2), z.price, z.valute, z.id)
                        else:
                            text += "\n{} (Просроченное) - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
                else:
                    text += "\n{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
            lastOrder = await db.RaskulAutoBuy.filter(name=item.name, status=1).order_by('-price').limit(1)
            plusText = ""
            if lastOrder:
                plusText = "\n\nНа этот предмет есть активные ордеры на автопокупку. Максимальная цена автопокупки составляет {}{}".format(lastOrder[0].price, lastOrder[0].valute)

        else:
            text = "Ошибка. Попробуйте еще раз."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Обновить информацию', callback_data="raskul_refresh_{}".format(lot.id)))
        markup.add(InlineKeyboardButton('Запрос на автопокупку', callback_data="raskul_autobuy_{}".format(lot.id)))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return
    elif kach == 'kriMarket':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        allLots = await db.KriMarket.exists(status=1, count__gt=1)
        if allLots:
            allLots = await db.KriMarket.filter(status=1, count__gt=1).order_by("priceForOne")
            text = ""
            if not allLots:
                text = "На данный момент предложений нет. Заходите позже!"
            else:
                for lot in allLots:
                    text += f"\n{lot.count} - {lot.priceForOne}💰/1💎. Купить - /raskulova_kriBuy_{lot.id}"
        else:
            text = "На данный момент предложений нет. Заходите позже!"
        markup.add(InlineKeyboardButton('Продать 💎', callback_data="kriMarket_sell"))
    
    elif kach == 'autobuy':
        lotCheck = _kach[2]
        lot = await db.Raskul.get_or_none(id=lotCheck).first()
        if lot:
            lotEditors[user.user_id] = lot.id
            lotUserStatus[user.user_id] = 'autobuy'
            text = "Вы хотите приобрести {} автоматически - введите цену автопокупки. Для отмены отправьте любое сообщение, кроме цифр.\n⚠️Если у вас не будет хватать средств на момент появления лота, удовлетворяющего ваш запрос - предмет приобретён не будет.".format(lot.name)
            return await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            return

    elif kach == 'autobuylist':
        lots = await db.RaskulAutoBuy.filter(owner=user.id, status=1)
        if lots:
            text = "Активные ордеры:\n"
            for lot in lots:
                text += "\n{} - {}{} (/raskulova_cancel_{})".format(lot.name, lot.price, lot.valute, lot.id)
        else:
            text = "Активные ордеры отсутствуют."


    if user.location == "Хэвенбург":
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
    elif user.location == 'Кавайня':
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_centr"))
    elif user.location == 'Океанус':
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
    elif user.location == 'Радар':
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_centr"))
    elif user.location == 'Метро':
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_centr"))
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(call.message.chat.id, text[x:x+4096])
    else:
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)

lotPrice = {}


class KriBuy(StatesGroup):
    lot = State()


async def raskulova_kriBuy_(m, user):
    lotId = m.text.replace("/raskulova_kriBuy_", "@TowerOfHeaven_bot", 1)
    lot = await db.KriMarket.get_or_none(id=lotId, status=1, count__gt=0)
    if lot:
        await KriBuy.lot.set(lot=lot.id)
        await bot.send_message(m.chat.id, f"Хорошо. Теперь выбери количество для покупки!\nДоступно: {lot.count}💎\nСтоимость за 💎 - {lot.priceForOne}\nУ тебя {user.money} 💰")
    else:
        await m.answer("Предложение устарело.")


@dp.message_handler(state=KriBuy.lot)
async def kriBuyLot(message: types.Message, state=FSMContext):
    if m.text.isdigit():
        if int(m.text) > 0:
            _lot = await state.get_data()
            lotId = _lot['lot']
            lot = await db.KriMarket.get_or_none(id=lotId, status=1, count__gt=0)
            if lot and lot.count > 0:
                seller = await db.Users.get_or_none(id=lot.seller).first()
                user = await db.Users.get_or_none(user_id=m.from_user.id).first()
                for i in range(1, int(m.text) + 1):
                    currentMoneyBuyer = user.money
                    currentKriBuyer = user.almaz
                    currentKriSeller = seller.almaz
                    currentMoneySeller = seller.money
                    currentKriLot = lot.count
                    priceForOne = lot.price
                    if currentMoneyBuyer >= priceForOne:
                        if currentKriLot > 0 and currentKriSeller > 0:
                            currentMoneyBuyer -= priceForOne
                            currentKriBuyer += 1
                            currentKriLot -= 1
                            currentKriSeller -= 1
                            success += 1
                            profit += priceForOne
                            text += "\n{} - ✅".format(i)
                        else:
                            text += "\n{} - ❌ (OOS)".format(i)
                            await db.KriMarket.filter(id=lot.id).update(status=0)
                    else:
                        text += "\n{} - ❌ (NM)".format(i)
                commision = await db.System.get(name='commisionKriMarket')
                realProfit = profit - int(profit * (commision.value / 100))
                currentMoneySeller += realProfit
                await db.Users.filter(id=user.id).update(almaz=currentKriBuyer, money=currentMoneyBuyer)
                await db.Users.filter(id=seller.id).update(almaz=currentKriSeller, money=currentMoneySeller)
                if currentKriLot > 0:
                    await db.KriMarket.filter(id=lot.id).update(count=currentKriLot)
                else:
                    await db.KriMarket.filter(id=lot.id).update(count=currentKriLot, status=0)
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                await logBot.send_message(tradeChat, text)
                try:
                    await bot.send_message(seller.user_id, "У вас приобрели {}💎 за {}💰".format(success, realProfit))
                except:
                    pass
            else: await m.answer("Предложение устарело.")
        else: await m.answer("Нужно вводить положительное число.")
    else: await m.answer("Нужно вводить число.")
    await state.finish()







@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='autobuy')
async def lotAutoBuy(m):
    try:
        price = int(m.text)
    except:
        lotUserStatus[m.from_user.id] = None
        lotEditors[m.from_user.id] = None
        return
    _lot = lotEditors[m.from_user.id]
    lot = await db.Raskul.get_or_none(id=_lot)
    if lot:
        lotEditors[m.from_user.id] = lot.id
        lotUserStatus[m.from_user.id] = 'autobuy2'
        lotPrice[m.from_user.id] = price
        await bot.send_message(m.chat.id, "Введите желаемое количество предметов.")

@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='autobuy2')
async def lotAutoBuy2(m):
    _lot = lotEditors[m.from_user.id]
    lot = await db.Raskul.get_or_none(id=_lot)
    user = await db.Users.get_or_none(user_id=m.from_user.id)
    if lot and user:
        try:
            count = int(m.text)
        except:
            lotUserStatus[m.from_user.id] = None
            lotEditors[m.from_user.id] = None
            return
        cnt = await db.RaskulAutoBuy.filter(name=lot.name, owner=user.id, status=1).only('id').count()
        if cnt + count > 50:
            await bot.send_message(m.chat.id, "Максимальное количество ордеров на один предмет - 50. Мы создадим ровно столько, сколько сможем.")
        await bot.send_message(m.chat.id, "Ваш ордер на покупку размещён. В случае успешного выполнения, ожидайте уведомления.")
        for i in range(0, count):
            if cnt + i < 50:
                await db.RaskulAutoBuy.create(price=lotPrice[user.user_id], name=lot.name, owner=user.id)
        lotUserStatus[m.from_user.id] = None
        lotEditors[m.from_user.id] = None
    else:
        lotUserStatus[m.from_user.id] = None
        lotEditors[m.from_user.id] = None 



async def raskulselecttype_(call, user):
    markup = InlineKeyboardMarkup(row_width=2)
    if call.data.split("_")[1] == 'eat':
        _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки"]
        allItems = await db.Raskul.filter(type__in=_types, status=1).order_by("price")
    elif call.data.split("_")[1] == 'heals':
        _types = ["Зелье", "Сундук", "Хлам", "Экипировка"]
        allItems = await db.Raskul.filter(type__in=_types, status=1).order_by("price")
    elif call.data.split("_")[1] == 'armor':
        _types = ["Броня", "Оружие"]
        allItems = await db.Raskul.filter(type__in=_types, status=1).order_by("price")
    elif call.data.split("_")[1] == 'other':
        _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки", "Броня", "Оружие", 
        "Зелье", "Сундук", "Хлам", "Экипировка"]
        allItems = await db.Raskul.filter(~Q(type__in=_types), status=1).order_by("price")
    text = "Ваш баланс: {}💰 {}💎. Доступные лоты в данной категории:".format(user.money, user.almaz)
    itms = []
    vipItems = await db.Raskul.filter(status=2, type__in=_types)
    for z in vipItems:
        text += "\n🔝{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
    count = 0
    for z in allItems:
        if str(z.name) in itms:
            pass
        else:
            count += 1
            itms.append(z.name)
            text += "\n{} - от {}{}. /raskulova_select_{}".format(z.name, z.price, z.valute, z.id)
    markup.add(InlineKeyboardButton('Вернуться назад', callback_data="raskul_buy"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


@dp.message_handler(lambda m:m.text and m.text.startswith('/raskulova_cancel_'))
async def raskulova_cancel_(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/raskulova_cancel_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    if player.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    lot = await db.RaskulAutoBuy.exists(id=result)
    if lot:
        pass
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз.")
        return
    lot = await db.RaskulAutoBuy.get(id=result)
    if lot and lot.status != 0:
        await db.RaskulAutoBuy.filter(id=lot.id).delete()
        await m.answer("Ордер удалён.")













async def lotEdit(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    if user.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    lotId = _kach[2]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    lot = await db.Raskul.exists(id=lotId)
    if lot:
        lot = await db.Raskul.get(id=lotId)
    if kach == 'editPrice':
        if lot and lot.owner == user.id:
            text = "Лот #{}\nПродажа {} за {}{}. Введите новую цену.".format(lot.id, lot.name, lot.price, lot.valute)
            await bot.send_message(call.message.chat.id, text)
            lotEditors[user.user_id] = lot.id
            lotUserStatus[user.user_id] = 'editPrice'
        else:
            await bot.send_message(call.message.chat.id, "Лота не существует либо он вам не принадлежит")
    elif kach == 'close':
        if lot and lot.owner == user.id:
            await db.Raskul.filter(id=lotId).update(status=0)
            await db.Inventory.filter(id=lot.item).update(active=1)
            await bot.send_message(call.message.chat.id, "Вы удалили лот")
        else:
            await bot.send_message(call.message.chat.id, "Лота не существует либо он вам не принадлежит")
    elif kach == 'select':
        if lot and lot.owner == user.id:
            text = "Лот #{}\nПродажа {} за {}{}. Выберите действие.".format(lot.id, lot.name, lot.price, lot.valute)
            markup.add(InlineKeyboardButton('Убрать с продажи', callback_data="lot_close_{}".format(lot.id)))
            #markup.add(InlineKeyboardButton('Изменить цену', callback_data="lot_editPrice_{}".format(lot.id)))
            if user.location == "Хэвенбург":
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
            elif user.location == 'Кавайня':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_centr"))
            elif user.location == 'Океанус':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
            elif user.location == 'Радар':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_centr"))
            elif user.location == 'Метро':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        else:
            await bot.send_message(call.message.chat.id, "Лота не существует либо он вам не принадлежит")

@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='editPrice')
async def lotEditPrice(m):
    try:
        newPrice = int(m.text)
        if newPrice >= 100000: return await m.answer("Ошибка. Попробуйте еще раз.")
    except:
        lotUserStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Ошибка. Попробуйте еще раз")
        return
    if newPrice and newPrice > 0:
        lot = await db.Raskul.get(id=lotEditors[m.from_user.id])
        user = await db.Users.get(user_id=m.from_user.id).first()
        oldPrice = lot.price
        oldCommision = int(lot.price * 0.1)
        newCommision = int(newPrice * 0.1)
        comm = oldCommision - newCommision
        if user.money - newCommision > 0:
            if lot.valute == '💰':
                await db.Users.filter(user_id=m.from_user.id).update(money=F('money') + comm)
            elif lot.valute == '💎':
                await db.Users.filter(user_id=m.from_user.id).update(almaz=F('almaz') + comm)
        else:
            await bot.send_message(m.chat.id, "У вас не хватает средств на оплату коммисии Раскуловой.")
            lotUserStatus[m.from_user.id] = None
            return
        await db.Raskul.filter(id=lot.id).update(price=newPrice)
        await lot.refresh_from_db(fields=['price'])
        await bot.send_message(m.chat.id, "Вы успешно изменили лот #{}, выставив новую цену в размере {}{}".format(lot.id, lot.price, lot.valute))
        lotUserStatus[m.from_user.id] = None
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Возможно, цена указана неправильно.")
        lotUserStatus[m.from_user.id] = None

@dp.message_handler(lambda m:m.text and m.text.startswith('/raskulova_select_'))
async def raskulova_select(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/raskulova_select_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    if player.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    lot = await db.Raskul.exists(id=result)
    if lot:
        pass
    else:
        await bot.send_message(m.chat.id, "Произошла ошибка. Попробуйте еще раз.")
        return
    lot = await db.Raskul.get(id=result)
    item = await db.Inventory.get(id=lot.item)
    if lot and lot.status != 0:
        seller = await db.Users.get(id=item.idplayer)
        lots = await db.Raskul.filter(~Q(status=0), name=item.name).order_by('price').limit(30)
        lotMin = await db.Raskul.filter(name=item.name).order_by('price').limit(1)
        lotMax = await db.Raskul.filter(name=item.name).order_by('-price').limit(1)
        text = "Информация по {}:".format(item.name)
        for x in lotMin:
            text += "\nМинимальная цена: {}{}".format(x.price, x.valute)
        for x in lotMax:
            if x.price > 50000:
                x.price = '♾'
            text += "\nМаксимальная цена: {}{}\nСписок текущих предложений:\n".format(x.price, x.valute)
        for z in lots:
            if item.type in ['Артефакт', 'Оружие'] or item.name == 'Бустер':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm[0].lvl, z.price, z.valute, z.id)
            elif item.type in ['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки', 'Еда']:
                itm = await db.Inventory.filter(id=z.item).only('expires')
                leftTime = (int(itm[0].expires) - time.time()) / 3600
                if leftTime > 0:
                    text += "\n{} (🦴{}ч) - {}{}. Купить - /raskulova_buy_{}".format(z.name, round(leftTime, 2), z.price, z.valute, z.id)
                else:
                    text += "\n{} (Просроченное) - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
            else:
                text += "\n{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
    elif lot.status == 0:
        lots = await db.Raskul.filter(~Q(status=0), name=lot.name).order_by('price').limit(30)
        text = "\nСписок текущих предложений:\n"
        for z in lots:
            if item.type in ['Артефакт', 'Оружие'] or item.name == 'Бустер':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm[0].lvl, z.price, z.valute, z.id)
            elif item.type in ['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки', 'Еда']:
                itm = await db.Inventory.filter(id=z.item).only('expires')
                leftTime = (result.expires - time.time()) / 3600
                if leftTime > 0:
                    text += "\n{} (🦴{}ч) - {}{}. Купить - /raskulova_buy_{}".format(z.name, round(leftTime, 2), z.price, z.valute, z.id)
                else:
                    text += "\n{} (Просроченное) - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
            elif item.name == 'Противогаз':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}/100) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm.bonus, z.price, z.valute, z.id)
            elif item.name == 'Фильтры':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm.bonus, z.price, z.valute, z.id)
            else:
                text += "\n{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Обновить информацию', callback_data="raskul_refresh_{}".format(lot.id)))
    markup.add(InlineKeyboardButton('Запрос на автопокупку', callback_data="raskul_autobuy_{}".format(lot.id)))
    await bot.send_message(m.chat.id, text, reply_markup=markup)



@dp.message_handler(lambda m:m.text and m.text.startswith('/raskulova_buy_'))
async def raskulova_buy(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/raskulova_buy_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    if player.ban == 1: return
    if player.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    lot = await db.Raskul.exists(id=result)
    if lot: 
        lot = await db.Raskul.get(id=result)
        item = await db.Inventory.get(id=lot.item)
    if lot and lot.status != 0:
        item = await db.Inventory.get(id=lot.item)
        seller = await db.Users.get(id=item.idplayer)
        if item.idplayer != lot.owner:
            await bot.send_message(m.chat.id, "Лота больше не существует.")
            await db.Raskul.filter(id=lot.id).update(status=0)
            return
        if item.idplayer == player.id:
            await bot.send_message(m.chat.id, "Вы не можете купить свой же предмет.")
            return
        try:
            await dp.throttle(str(player.user_id), rate=1)
        except exceptions.Throttled:
            return
        if item.active == 3:
            if lot.valute == '💎':
                if player.almaz >= lot.price:
                    inventorySize = await db.getInventorySize(player)
                    if inventorySize + item.size > player.inventorySizeMax:
                        await bot.send_message(m.chat.id, "У вас не хватает места в инвентаре")
                        return
                    
                    commision = await db.System.get(name='commisionRaskulova')
                    cost = lot.price - int(lot.price * (commision.value / 100)) + int(lot.price * 0.1)
                    await db.Users.filter(id=player.id).update(almaz=F('almaz') - lot.price)
                    await db.Users.filter(id=seller.id).update(almaz=F('almaz') + cost)
                    await db.Inventory.filter(id=lot.item).update(idplayer=player.id, active=1)
                    await db.Raskul.filter(id=result).update(status=0)
                else:
                    await bot.send_message(m.chat.id, "У вас не хватает {}".format(lot.valute))
                    return
            else:
                if player.money >= lot.price:
                    inventorySize = await db.getInventorySize(player)
                    if inventorySize + item.size > player.inventorySizeMax:
                        await bot.send_message(m.chat.id, "У вас не хватает места в инвентаре")
                        return
                    
                    commision = await db.System.get(name='commisionRaskulova')
                    cost = lot.price - int(lot.price * (commision.value / 100)) + int(lot.price * 0.1)
                    await db.Users.filter(id=player.id).update(money=F('money') - lot.price)
                    await db.Users.filter(id=seller.id).update(money=F('money') + cost)
                    await db.Inventory.filter(id=lot.item).update(idplayer=player.id, active=1)
                    await db.Raskul.filter(id=result).update(status=0)
                else:
                    await bot.send_message(m.chat.id, "У вас не хватает {}".format(lot.valute))
                    return
            await db.Raskul.filter(item=lot.item).update(status=0)
            await bot.send_message(m.chat.id, "Вы успешно приобрели {} за {}{}".format(item.name, lot.price, lot.valute))
            if seller.quest == 'Продаван' and seller.questStatus == 1:
                quest = await db.tempQuest.get(user_id=seller.user_id, quest=seller.quest, status=0).first()
                await db.tempQuest.filter(id=quest.id).update(progress=F('progress') + 1)
            await achprog(seller, ach='prodavan')
            try:
                await bot.send_message(seller.user_id, "У вас приобрели {} за {}{}".format(item.name, lot.price, lot.valute))
            except:
                pass
            await logBot.send_message(tradeChat, "{} приобрел у {} {} за {}{}".format(player.username, seller.username, item.name, lot.price, lot.valute))
            item.active = 1
            item.idplayer = player.id
            await db.commitInventory(player, item)
        else:
            await bot.send_message(m.chat.id, "Предмета не существует. Покупка отменена.")
            await db.Raskul.filter(id=lot.id).update(status=0)
    elif lot and lot.status == 0:
        lots = await db.Raskul.filter(~Q(status=0), name=lot.name).order_by('price').limit(30)
        lotMin = await db.Raskul.filter(name=lot.name).order_by('price').limit(1)
        lotMax = await db.Raskul.filter(name=lot.name).order_by('-price').limit(1)
        text = "Информация по {}:".format(lot.name)
        for x in lotMin:
            text += "\nМинимальная цена: {}{}".format(x.price, x.valute)
        for x in lotMax:
            text += "\nМаксимальная цена: {}{}\nСписок текущих предложений:\n".format(x.price, x.valute)
        for z in lots:
            if item.type in ['Артефакт', 'Оружие'] or item.name == 'Бустер':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm.lvl, z.price, z.valute, z.id)
            elif item.type in ['Ингредиент готовки', 'Особый ингредиент готовки', 'Легендарный ингредиент готовки', 'Еда']:
                itm = await db.Inventory.get(id=z.item).only('expires', 'bonus')
                leftTime = (itm.expires - time.time()) / 3600
                if leftTime > 0:
                    text += "\n{} (🦴{}ч) - {}{}. Купить - /raskulova_buy_{}".format(z.name, round(leftTime, 2), z.price, z.valute, z.id)
                else:
                    text += "\n{} (Просроченное) - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
            elif item.name == 'Противогаз':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}/100) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm.bonus, z.price, z.valute, z.id)
            elif item.name == 'Фильтры':
                itm = await db.Inventory.filter(id=z.item).only('lvl')
                text += "\n{} ({}) - {}{}. Купить - /raskulova_buy_{}".format(z.name, itm.bonus, z.price, z.valute, z.id)
            else:
                text += "\n{} - {}{}. Купить - /raskulova_buy_{}".format(z.name, z.price, z.valute, z.id)
raskulSell = {}
raskulCount = {}
"""@dp.message_handler(lambda m:m.text and m.text.startswith('/raskulova_sell_'))
async def raskulova_sell(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/raskulova_sell_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    item = await db.Inventory.exists(id=result)
    if item:
        item = await db.Inventory.get(id=result)
    zapr = ['Обломок синего камня', 'RCA', 'Цветок сакуры', 'Роза', 'Одуванчик', 'Останки героев', 'Перо ястреба', 'Тушка питона', 'Котелок', 'Снунец', 'Багровая чешуя']
    if item.active == 1 and item.name not in zapr:
        await bot.send_message(m.chat.id, "Вы собираетесь продать {}. Введите цену продажи. Если вы передумали, отправьте любое сообщение (не цифру)".format(item.name))
        raskulSell[m.from_user.id] = item.id
        lotUserStatus[player.user_id] = 'seller'"""
@dp.message_handler(lambda m:m.text and m.text.startswith('/raskulova_sell_'))
async def raskulova_sell(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/raskulova_sell_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    if player.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    if player.ban == 1: return
    item = await db.Inventory.exists(id=result)
    if item:
        item = await db.Inventory.get(id=result)
    else:
        await bot.send_message(m.chat.id, "Предмета не существует.")
        return
    zapr = ['Обломок синего камня', 'Ебушар', 'RCA', 'Цветок сакуры', 'Роза', 'Одуванчик', 'Останки героев', 'Перо ястреба', 'Тушка питона', 'Котелок', 'Снунец', 'Багровая чешуя', 'Ситень', 'Карта заброшенного архива', 'Документ DSFB-4', 'Странная заготовка']
    if item.active == 1 and item.name not in zapr:
        counts = await db.Inventory.filter(idplayer=player.id, active=1, name=item.name).count()
        lastOrder = await db.RaskulAutoBuy.filter(name=item.name, status=1).order_by('-price').limit(1)
        plusText = ""
        if lastOrder:
            plusText = "\n\nНа этот предмет есть активные ордеры на автопокупку. Максимальная цена автопокупки составляет {}{}".format(lastOrder[0].price, lastOrder[0].valute)
        print(counts)
        if counts > 1:
            await bot.send_message(m.chat.id, "Вы собираетесь продать {}. Введите количество продаваемых предметов. У вас {} таких же предметов. Учтите, что множественную продажу можно использовать только для лотов за 💰. Если вы передумали, отправьте любое сообщение (не цифру)\n\n{}".format(item.name, counts, plusText))
            raskulSell[m.from_user.id] = item.id
            lotUserStatus[player.user_id] = 'sell'
        else:
            await bot.send_message(m.chat.id, "Вы собираетесь продать {}. Введите сумму продажи. Если вы передумали, отправьте любое сообщение (не цифру)\n\n{}".format(item.name, plusText))
            raskulSell[m.from_user.id] = item.id
            lotUserStatus[player.user_id] = 'seller'

@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='sell')
async def raskulova_sell_step1(m):
    try:
        count = int(m.text)
    except:
        lotUserStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Продажа отменена")
        return
    if count > 0:
        pass
    else:
        return
    await bot.send_message(m.chat.id, "Введите фиксированную сумму продажи данных предметов. Обратите внимание что для публикации лота необходимо иметь на счету 10% от заявленной суммы, которые спишутся при публикации и вернутся при успешной продаже предмета. Если вы передумали, отправьте любое сообщение (не цифру)")
    raskulCount[m.from_user.id] = count
    lotUserStatus[m.from_user.id] = 'seller'

async def raskulova_sell_all(m, price):
    if price > 0:
        item = await db.Inventory.get(id=raskulSell[m.from_user.id])
        count = raskulCount[m.from_user.id]
        user = await db.Users.get(user_id=m.from_user.id)
        if user.location in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
            itemsToSell = await db.Inventory.filter(name=item.name, active=1, idplayer=user.id).count()
            itemsToSell = await db.Inventory.filter(name=item.name, active=1, idplayer=user.id).limit(count)
            for z in itemsToSell:
                checkLots = await db.Raskul.filter(~Q(status=0), owner=user.id).count()
                if checkLots < 10:
                    commision = int(price * 0.1)
                    if user.money >= commision:
                        await db.Users.filter(id=user.id).update(money=F('money') - commision)
                        await db.Raskul.create(name=z.name, item=z.id, price=price, owner=user.id, valute='💰', status=1, type=item.type)
                        await db.Inventory.filter(id=z.id).update(active=3)
                        await user.refresh_from_db()
                        z.active = 3
                        await db.commitInventory(user, z)
            await bot.send_message(m.chat.id, "Лоты были созданы.")
        else:
            await bot.send_message(m.chat.id, "Вы находитесь вне города.")
    lotUserStatus[m.from_user.id] = None
    raskulCount[m.from_user.id] = None
    raskulSell[m.from_user.id] = None

@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='seller')
async def raskulova_sell_step2(m):
    try:
        price = int(m.text)
    except:
        lotUserStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Продажа отменена")
        return
    if price > 0:
        pass
    else:
        return
    if m.from_user.id in raskulCount and raskulCount[m.from_user.id] != None and raskulCount[m.from_user.id] > 1:
        await raskulova_sell_all(m, price)
        return
    item = await db.Inventory.exists(id=raskulSell[m.from_user.id])
    if item:
        item = await db.Inventory.get(id=raskulSell[m.from_user.id])
    user = await db.Users.get(user_id=m.from_user.id)
    if user.location not in ['Хэвенбург', 'Кавайня', 'Океанус', 'Радар', 'Метро']:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    if item and item.active == 1 and item.idplayer == user.id:
        checkLot = await db.Raskul.exists(status=1, item=item.id)
        if checkLot:
            await bot.send_message(m.chat.id, "У вас уже опубликован лот с этим предметом")
            return
        checkCountLots = await db.Raskul.filter(status=1, owner=user.id).count()
        if checkCountLots < 10:
            newLot = await db.Raskul.create(name=item.name, item=item.id, status=0, price=price, owner=user.id, type=item.type)
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('💎', callback_data="lotValute_{}_almaz".format(newLot.id)))
            markup.add(InlineKeyboardButton('💰', callback_data="lotValute_{}_gold".format(newLot.id)))
            await bot.send_message(m.chat.id, "Лот создан. Пожалуйста, выберите валюту лота до публикации.", reply_markup=markup)
        else:
            await bot.send_message(m.chat.id, "Лимит на продажу - 10 штук.")
    else:
        await bot.send_message(m.chat.id, "Данной вещи не найдено в вашем инвентаре.")
    lotUserStatus[m.from_user.id] = None
    raskulCount[m.from_user.id] = None
    raskulSell[m.from_user.id] = None

async def lotValute_(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    lot = await db.Raskul.get(id=kach)
    if _kach[2] == 'almaz': valute = '💎'
    else: valute = '💰'
    if _kach[2] == 'gold' and user.money >= int(lot.price * 0.1):
        item = await db.Inventory.filter(id=lot.item).update(active=3)
        item = await db.Inventory.get(id=lot.item)
        await db.commitInventory(user, item)
        await db.Users.filter(id=user.id).update(money=F('money') - int(lot.price * 0.1))
    elif _kach[2] == 'almaz' and user.almaz >= int(lot.price * 0.1):
        item = await db.Inventory.filter(id=lot.item).update(active=3)
        item = await db.Inventory.get(id=lot.item)
        await db.commitInventory(user, item)
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - int(lot.price * 0.1))
    else:
        await bot.send_message(call.message.chat.id, 'У вас не хватает валюты для взноса при публикации лота')
        return
    await db.Raskul.filter(id=lot.id).update(valute=valute, status=1)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Опубликовать и закрепить(5💎)', callback_data="lotDone_{}_prem".format(lot.id)))
    markup.add(InlineKeyboardButton('Опубликовать без закрепления', callback_data="lotDone_{}".format(lot.id)))
    await bot.edit_message_text("Валюта выбрана. Вы так же можете закрепить лот.", call.message.chat.id, call.message.message_id, reply_markup=markup)


async def lotDone(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    lot = await db.Raskul.get(id=kach)
    q = None
    try:
        if _kach[2]:
            q = _kach[2]
            if user.almaz >= 5: 
                await db.Users.filter(id=user.id).update(almaz=F('almaz') - 5)
                await db.Raskul.filter(id=lot.id).update(status=2)
                await bot.edit_message_text("Лот закреплён.", call.message.chat.id, call.message.message_id)
            else:
                await bot.send_message(call.message.chat.id, "У вас не хватает 💎")
    except:
        await bot.edit_message_text("Лот опубликован.", call.message.chat.id, call.message.message_id)
    lotUserStatus[user.user_id] = None


async def krimarket(call, user):
    _kach = call.data.split('_')
    kach = _kach[1]
    if kach == 'sell':
        lotUserStatus[user.user_id] = 'kristallSell'
        commision = await db.System.get(name='commisionKriMarket')
        await bot.edit_message_text("Введите количество 💎, которое желаете продать. Коммисия Раскуловой составляет {}%".format(commision.value), call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='kristallSell')
async def kristallSell_step1(m):
    try:
        count = int(m.text)
    except:
        lotUserStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Продажа отменена")
        return
    if count > 0:
        pass
    else:
        lotUserStatus[m.from_user.id] = None
        return
    lotUserStatus[m.from_user.id] = 'kristallSell2'
    user = await db.Users.get(user_id=m.from_user.id).first()
    if user.almaz >= count:
        newLot = await db.KriMarket(allCount=count, status=0, seller=user.id, count=count)
        await newLot.save()
        await bot.send_message(m.chat.id, "Теперь введите стоимость за 1 💎")
    else:
        await bot.send_message(m.chat.id, "У вас не хватает 💎. У вас {}💎. Введите правильное количество".format(user.almaz))


@dp.message_handler(lambda m: lotUserStatus and m.from_user.id==m.chat.id and m.from_user.id in lotUserStatus and lotUserStatus[m.from_user.id]=='kristallSell2')
async def kristallSell_step2(m):
    try:
        price = int(m.text)
    except:
        lotUserStatus[m.from_user.id] = None
        await bot.send_message(m.chat.id, "Продажа отменена")
        return
    if price > 0:
        pass
    else:
        lotUserStatus[m.from_user.id] = None
        return
    user = await db.Users.get(user_id=m.from_user.id).first()
    checkLot = await db.KriMarket.get(status=0, seller=user.id).first()
    checkLot.priceForOne = price
    checkLot.status = 1
    await checkLot.save()
    await bot.send_message(m.chat.id, "Лот опубликован. При покупке вы получите уведомление.")
    lotUserStatus[user.user_id] = None



async def pizza_shop(m, user):
    text = """
Магазин 🍕ПИЗЗА🍕 (здесь не продают пиццу, здесь её покупают)! 🍕 - валюта, которую можно получить за активность (прохождение капчи/баг-репорты и т.д.).

У тебя {} 🍕

На что можно обменять?

🎟Билет на тот свет (2🍕). Позволяет телепортироваться к месту последней смерти
Смена никнейма(10🍕). Вы можете сменить свой никнейм, если предыдущий вас не устраивает (или нет)
+200📦(🥘)(10🍕). Можно купить и расширить инвентарь котелка на 200📦
♥️ToH supporter (50🍕). Набор включает в себя х1📦Коробка с карточками, +5📦, 15 дней ⚡️Бустеров и титул в профиле ♥️ToH supporter♥️ на месяц    
🎣Очень непростая удочка (50🍕). Позволяет ловить рыбу в Пруду

_Список будет дополняться..._
""".format(user.pizza)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('🎟Билет на тот свет', callback_data="pizzashop_1"))
    markup.add(InlineKeyboardButton('Смена никнейма', callback_data="pizzashop_2"))
    markup.add(InlineKeyboardButton('+200📦(🥘)', callback_data="pizzashop_3"))
    markup.add(InlineKeyboardButton('♥️ToH supporter', callback_data="pizzashop_4"))
    markup.add(InlineKeyboardButton('🎣Очень непростая удочка', callback_data="pizzashop_5"))
    await bot.send_message(m.chat.id, text, reply_markup=markup,parse_mode='markdown')

async def pizzashop(call, user):
    if call.data.split("_")[1] == '1':
        if user.pizza >= 2:
            success = await db.addItem('Билет на тот свет', user)
            if success == True:
                await db.Users.filter(id=user.id).update(pizza=F('pizza') - 2)
                await bot.edit_message_text('Вы успешно приобрели 🎟Билет на тот свет.', call.message.chat.id, call.message.message_id)
                await logBot.send_message(tradeChat, f"Игрок {user.username} ({user.id}) приобрёл в пиццашопе 🎟Билет на тот свет")
            else:
                await bot.edit_message_text("У вас не хватает места в инвентаре. Покупка отменена", call.message.chat.id, call.message.message_id)
            return
        else:
            await bot.edit_message_text("У вас не хватает 🍕", call.message.chat.id, call.message.message_id)
    elif call.data.split("_")[1] == '2':
        if user.pizza >= 10:
            await logBot.send_message(tradeChat, "Игрок {} ({}) приобрёл в пиццашопе смену никнейма".format(user.username, user.id))
            await bot.edit_message_text("Назови своё имя, путник.", call.message.chat.id, call.message.message_id)
            shopStatus[call.from_user.id] = 'reg_nick'
            await db.Users.filter(id=user.id).update(pizza=F('pizza') - 10)
    elif call.data.split("_")[1] == '3':
        if user.pizza >= 10:
            await db.Users.filter(id=user.id).update(pizza=F('pizza') - 10, kotelokLimit=F('kotelokLimit') + 200)
            await bot.edit_message_text('Вы успешно приобрели +200📦(🥘)', call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, f"Игрок {user.username} ({user.id}) приобрёл в пиццашопе +200📦(🥘)")
        else:
            await bot.edit_message_text("У вас не хватает 🍕", call.message.chat.id, call.message.message_id)
    elif call.data.split("_")[1] == '4':
        if user.pizza >= 50:
            await db.Users.filter(id=user.id).update(pizza=F('pizza') - 50)
            await bot.edit_message_text("Покупаем...", call.message.chat.id, call.message.message_id)
            await db.addBoost(user, lvl=360)
            if user.supporter >= time.time(): await db.Users.filter(id=user.id).update(booster=F('booster') + 2592000)
            else: await db.Users.filter(id=user.id).update(supporter=time.time() + 2592000)
            await db.addItem('Коробка с карточками', user, arg='a')
            await db.Users.filter(id=user.id).update(inventorySizeMax=F('inventorySizeMax') + 5)
            await bot.send_message(user.user_id, "Покупка набора ToH supporter завершена. Вы можете поставить титул через команду /badges")
            await logBot.send_message(tradeChat, "Игрок {} ({}) приобрёл в пиццашопе саппортер".format(user.username, user.id))
        else:
            await bot.edit_message_text("У вас не хватает 🍕", call.message.chat.id, call.message.message_id)
    elif call.data.split("_")[1] == '5':
        if user.pizza >= 50:
            success = await db.addItem('Очень непростая удочка', user)
            if success == True:
                await db.Users.filter(id=user.id).update(pizza=F('pizza') - 50)
                await bot.edit_message_text('Вы успешно приобрели 🎣Очень непростая удочка.', call.message.chat.id, call.message.message_id)
                await logBot.send_message(tradeChat, f"Игрок {user.username} ({user.id}) приобрёл в пиццашопе 🎣Очень непростая удочка")
            else:
                await bot.edit_message_text("У вас не хватает места в инвентаре. Покупка отменена", call.message.chat.id, call.message.message_id)
            return
        else:
            await bot.edit_message_text("У вас не хватает 🍕", call.message.chat.id, call.message.message_id)
