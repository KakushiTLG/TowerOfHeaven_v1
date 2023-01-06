
class GetQuantity(StatesGroup):
    restore = State()
    bamboo = State()
    geroin = State()
    boyara = State()
    viagra = State()
    sredne = State()
    big = State()
    ilovestas = State()
    restoreSmall = State()
    restoreMedium = State()
    koltGrav = State()



async def profile(m, user):
    if user:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        item1 = types.KeyboardButton('Профиль')
        item2 = types.KeyboardButton('Инвентарь')
        item4 = types.KeyboardButton('Навигация')
        markup.row(item1, item2)
        markup.row(item4)
        _itemAtk = user.lvl / 100
        if user.frak and user.frak != '':
            frak = await db.Fraks.get_or_none(name=user.frak).only('atk', 'leader', 'zam', 'name')
            if frak:
                _frakAtk = frak.atk / 100
            if frak and frak.leader == user.id: status = "Владелец клана {}".format(frak.name)
            elif frak and frak.zam == user.id: status = "Заместитель клана {}".format(frak.name)
            elif frak: status = "Участник клана {}".format(frak.name)
        else:
            _frakAtk = 0
            status = "Изгой"

        weapon = await db.Inventory.get_or_none(type='Оружие', idplayer=user.id, active=2).only('bonus').first()
        if weapon:
            _playerAtk = user.atk * (weapon.bonus / 100)
            playerAtk = int(_playerAtk + (user.atk * _frakAtk))
        else:
            playerAtk = user.atk * _frakAtk
            user.visualitem = "Кулаки - мои друзья"
        if user.lvl < 100:
            _needExp = int(user.lvl / 2) * 25
            needexp = int(user.lvl * 150) + _needExp
        elif user.lvl < 200:
            needexp = int(user.lvl * 150) * (user.lvl / 50)
        else:
            needexp = int(user.lvl * 150) * (user.lvl / 15)
        if needexp >= 10000:
            _needExp = needexp / 1000
            needExp = "{}k".format(round(_needExp, 2))
            if user.exp < 1000:
                userExp = user.exp
            else:
                _userExp = user.exp / 1000
                userExp = "{}k".format(round(_userExp, 2))
        else:
            needExp = needexp
            userExp = user.exp
        inventorySize = await db.getInventorySize(user)
        allItmsArmorPvP = await db.Inventory.filter(idplayer=user.id, active=2, atk_block__gt=0).only('atk_block')
        armorPvP = 0
        if allItmsArmorPvP:
            for i in allItmsArmorPvP:
                armorPvP += i.atk_block
        rand = random.randint(1, 100)
        text = ""
        if user.ban != 0 and user.ban != 2:
            timeToEndBan = int((user.banEnds - time.time()) / 86400)
            text += "\n⛔️*BANNED*⛔️\n\nВаш аккаунт был ограничен решением администрации по причине: ''{}'' на {}дн. \n\nЕсли вы не согласны с причиной блокировки, обратитесь к коммьюнити-менеджеру/разработчику по контактам, указанным на https://toh.fdu.su/team .\n\n".format(user.banreason, timeToEndBan)
        if user.badge:
            text += "{}\n".format(user.badge)
        text += "👤[{}](tg://user?id={})\n".format(user.username, user.user_id)
        text += "👥{}\n".format(status)
        if user.location == 'Город':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        elif user.location == 'Хэвенбург' or user.location == 'Кавайня' or user.location == 'Океанус' or user.location == 'Радар':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        else:
            text += "📡*{}*\n".format(user.location)
        text += "🔆{} (✨*{}/{}*)\n\n".format(user.lvl, userExp, needExp)
        checkHlop = await db.Buffs.exists(owner=user.id, status=1, type='hlopushka')
        if user.location != 'Свалка HD' and not checkHlop: text += "❤️{}/{}".format(user.nowhp, user.hp)
        else: text += "❤️❓"
        text += "🛡{}(⚔️{}%)\n".format(user.armor, armorPvP)
        text += "🔪{}(+{})\n".format(user.atk, int(playerAtk))
        text += "⚡️{}/100 🍗{}/100".format(user.energy, user.eat)
        pp = await db.getpp(user)
        if pp <= 0: pp = 0
        text += "\n💮{} pp (#{})\n\n".format(int(pp), user.ppTop)
        if user.location == 'Кавайня' or user.location == 'Заснеженный лес': text += "❄️{}/100\n".format(user.zamoroz)
        elif user.location == 'Океанус' or user.location == 'Окус Локус': text += "☁️{}/100\n".format(user.humidity)
        else: text += ""
        text += "\n💰{} 💎{} 🔘{}\n\n📦{}/{}".format(user.money, user.almaz, user.uppts, inventorySize, user.inventorySizeMax)
        if user.visualitem:
            text += "\n\n🗡Экипировано: {}\n\n".format(user.visualitem)
        text += "\n🆔 - {}\n".format(user.id)
        text += "\n\nРасширенный профиль - /profile"
        await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)



async def profileFull(m, user):
    if user:
        _itemAtk = user.lvl / 100
        if user.frak and user.frak != '':
            frak = await db.Fraks.get_or_none(name=user.frak)
            if frak:
                _frakAtk = frak.atk / 100
            if frak and frak.leader == user.id: status = "Владелец клана {}".format(frak.name)
            elif frak and frak.zam == user.id: status = "Заместитель клана {}".format(frak.name)
            elif frak: status = "Участник клана {}".format(frak.name)
        else:
            _frakAtk = 0
            status = "Изгой"
        weapon = await db.Inventory.get_or_none(name=user.item, idplayer=user.id, active=2).first()
        if weapon:
            _playerAtk = user.atk * (weapon.bonus / 100)
            checkBuff = await db.Buffs.get_or_none(owner=user.id, type='atk', status=1).first()
            if checkBuff:
                playerAtk = int(_playerAtk + (user.atk * (checkBuff.num / 100)) + (user.atk * _frakAtk))
            else:
                playerAtk = int(_playerAtk + (user.atk * _frakAtk))
        else:
            checkBuff = await db.Buffs.get_or_none(owner=user.id, type='atk', status=1).first()
            if checkBuff:
                playerAtk = int((user.atk * (checkBuff.num / 100)) + (user.atk * _frakAtk))
            else:
                playerAtk = user.atk * _frakAtk
            user.item = "Кулаки - мои друзья"
        if user.lvl < 100:
            _needExp = int(user.lvl / 2) * 25
            needexp = int(user.lvl * 150) + _needExp
        elif user.lvl < 200:
            needexp = int(user.lvl * 150) * (user.lvl / 50)
        else:
            needexp = int(user.lvl * 150) * (user.lvl / 15)
        if needexp >= 10000:
            _needExp = needexp / 1000
            needExp = "{}k".format(round(_needExp, 2))
            if user.exp < 1000:
                userExp = user.exp
            else:
                _userExp = user.exp / 1000
                userExp = "{}k".format(round(_userExp, 2))
        else:
            needExp = needexp
            userExp = user.exp
        inventorySize = await db.getInventorySize(user)
        allItmsArmorPvP = await db.Inventory.filter(idplayer=user.id, active=2, atk_block__gt=1).only('atk_block')
        armorPvP = 0
        if allItmsArmorPvP:
            for i in allItmsArmorPvP:
                armorPvP += i.atk_block
        rand = random.randint(1, 100)
        text = ""
        if user.ban != 0 and user.ban != 2:
            timeToEndBan = int((user.banEnds - time.time()) / 86400)
            text += "\n⛔️*BANNED*⛔️\n\nВаш аккаунт был ограничен решением администрации по причине: ''{}'' на {}дн. \n\nЕсли вы не согласны с причиной блокировки, обратитесь в /report. Чрезмерное использование репорта может повлечь бессрочную блокировку аккаунта и /report.\n\n".format(user.banreason, timeToEndBan)
            await bot.send_message(m.chat.id, text, parse_mode='markdown')
            return
        if user.badge:
            text += "{}\n".format(user.badge)
        text += "👤[{}](tg://user?id={})\n".format(user.username, user.user_id)
        if user.location == 'Город':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        elif user.location == 'Хэвенбург' or user.location == 'Кавайня' or user.location == 'Океанус' or user.location == 'Радар':
            text += "📡*{}*🏪*{}*\n".format(user.location, user.position)
        else:
            text += "📡*{}*\n".format(user.location)
        pp = await db.getpp(user)
        if pp <= 0: pp = 0
        text += "🔆{} (✨*{}/{}*)\n\n".format(user.lvl, userExp, needExp)
        checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
        if user.location != 'Свалка HD' and not checkHlop: text += "❤️{}/{}".format(user.nowhp, user.hp)
        else: text += "❤️❓"
        checkBuff = await db.Buffs.get_or_none(type='armor', owner=user.id, status=1).first()
        if checkBuff: user.armor += checkBuff.num
        text += "🛡{}(⚔️{}%)\n".format(user.armor, armorPvP)
        text += "🔪{}(+{})\n".format(user.atk, int(playerAtk))
        text += "⚡️{}/100 🍗{}/100".format(user.energy, user.eat)
        if user.location == 'Кавайня' or user.location == 'Заснеженный лес': text += "❄️{}\n".format(user.zamoroz)
        elif user.location == 'Океанус' or user.location == 'Окус Локус': text += "☁️{}\n".format(user.humidity)
        else: text += ""
        text += "\n💮{} pp (#{})\n\n".format(int(pp), user.ppTop)
        text += "💰{} 💎{} 🔘{}\n".format(user.money, user.almaz, user.uppts)
        if user.heavenCurrency > 0:
            text += "🔻{}".format(user.heavenCurrency)
        if user.kawaiCurrency > 0:
            text += "🧊{}".format(user.kawaiCurrency)
        if user.oceanCurrency > 0:
            text += "💧{}".format(user.oceanCurrency)
        if user.radarCurrency > 0:
            text += "♦️{}".format(user.radarCurrency)
        if user.metroCurrency > 0:
            text += "🗝{}".format(user.metroCurrency)
        text += "\n\n🗡Оружие: {} (/weapon)\n\n📦{}/{}\n".format(user.item, inventorySize, user.inventorySizeMax)
        checkHouse = await db.Houses.get_or_none(owner=user.id)
        if checkHouse:
            text += "\n🏚{} (/home)".format(checkHouse.name)
            if checkHouse.lvl >= 5:
                currentSize = await db.getHouseInventorySize(user)
                text += " (📦{}/{})\n".format(currentSize, checkHouse.inventory)
        text += "\n🤝{} ⭐️{}/5\n\n".format(user.tradecount, user.tradenum)
        text += "🆔 - {}".format(user.id)
        if user.booster >= int(time.time()):
            timeLeft = user.booster - int(time.time())
            if timeLeft <= 172800:
                timeleft = timeLeft / 3600
                boostLeft = "{}ч".format(round(timeleft, 2))
            else:
                timeleft = timeLeft / 86400
                boostLeft = "{}дн".format(int(timeleft))
            text += "\n\n⚡️Бустеры активны еще {}".format(boostLeft)
        checkBuff = await db.Buffs.exists(owner=user.id, status=1)
        if checkBuff:
            text += "\n\nАктивные баффы:"
            checkBuffs = await db.Buffs.filter(owner=user.id, status=1)
            for buff in checkBuffs:
                timeLeft = int((buff.timeEnd - int(time.time())) / 60)
                if buff.type == 'atk':
                    text += "\nАктивен бонус к 🔪Атаке. +{}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'creet':
                    text += "\nАктивен бонус к шансу 💢Крит урона. +{}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'uv':
                    text += "\nАктивен бонус к шансу 💨Уворота. {}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'armor':
                    text += "\nАктивен бонус к 🛡Броне. +{} ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'antiZamoroz':
                    text += "\nБонус сопротивления к ❄️Холоду {}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'antiHumidity':
                    text += "\nБонус сопротивления к ☁️Влажности {}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'electro':
                    text += "\nАктивен бонус к ⚡️Заряженному удару. +{}% ({} мин)".format(buff.num, timeLeft)
                elif buff.type == 'hlopushka':
                    text += "\nАктивен дебафф - Оглушение ({} мин)".format(timeLeft)
        await bot.send_message(m.chat.id, text, parse_mode='markdown')



#####################
#   SKILLS&BADGES   #
#####################

async def stats(m):
    if m.chat.id == m.from_user.id:
        await bot.send_message(m.chat.id, "Статистика переехала на http://toh.fdu.su/profile\n\nАвторизация с помощью /token")


async def badges(m, user):
    if m.chat.id == m.from_user.id:
        passLvl = 0
        passKiller = 0
        passPvp = 0
        passMoney = 0
        passTop1 = 0
        passTop2 = 0
        passTop3 = 0
        passKach = 0
        passProd = 0
        passSupporter = 0
        achs = await db.Ach.get(user_id=m.from_user.id)
        forKiller = achs.ubica.split("|")
        forPvp = achs.pvpsher.split("|")
        forProd = achs.prodavan.split("|")
        if user.lvl >= 100: passLvl = 1
        if int(forKiller[0]) >= 10000: passKiller = 1
        if int(forPvp[0]) >= 100: passPvp = 1
        if user.money >= 1000000: passMoney = 1
        if user.ppTop == 1: passTop1 = 1
        if user.ppTop == 2: passTop2 = 1
        if user.ppTop == 3: passTop3 = 1
        if user.atk + user.hp >= 2000: passKach = 1
        if int(forProd[0]) >= 1000: passProd = 1
        if user.supporter >= int(time.time()): passSupporter = 1
        text = "Доступные значки:\n"
        if passLvl == 1: text += "\n✴️Опытный✴️ - /set_badge_lvl"
        if passKiller == 1: text += "\n🪓Киллер🪓 - /set_badge_killer"
        if passPvp == 1: text += "\n🤼‍♂️Настораживающая музыка🤼‍♂️ - /set_badge_pvp"
        if passMoney == 1: text += "\n💸Миллионер💸 - /set_badge_millioner"
        if passTop1 == 1: text += "\n🥇Избранный🥇 - /set_badge_top1"
        if passTop2 == 1: text += "\n🥈Особенный🥈 - /set_badge_top2"
        if passTop3 == 1: text += "\n🥉Тёмная лошадка🥉 - /set_badge_top3"
        if passKach == 1: text += "\n💪Любитель качалки💪 - /set_badge_kach"
        if passProd == 1: text += "\n🤝Успешный продавец🤝 - /set_badge_prod"
        if passSupporter == 1: text += "\n♥️ToH supporter♥️ - /set_badge_supporter"
        if len(text) < 25: text += "\nДоступных значков пока нет. Возможно, в скором времени появится и ты сможешь украсить свой профиль титулом!"
        await bot.send_message(m.chat.id, text)


async def set_badge(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/set_badge_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    if m.chat.id == m.from_user.id:
        user = await db.Users.get(user_id=m.from_user.id)
        achs = await db.Ach.get(user_id=m.from_user.id)
        forKiller = achs.ubica.split("|")
        forPvp = achs.pvpsher.split("|")
        forProd = achs.prodavan.split("|")
        if user.lvl >= 100 and result == 'lvl': badge = "✴️Опытный✴️"
        elif int(forKiller[0]) >= 10000 and result == 'killer': badge = "🪓Киллер🪓"
        elif int(forPvp[0]) >= 100 and result == 'pvp': badge = "🤼‍♂️Настораживающая музыка🤼‍♂️"
        elif user.money >= 1000000 and result == 'millioner': badge = "💸Миллионер💸"
        elif user.ppTop == 1 and result == 'top1': badge = "🥇Избранный🥇"
        elif user.ppTop == 2 and result == 'top2': badge = "🥈Особенный🥈"
        elif user.ppTop == 3 and result == 'top3': badge = "🥉Тёмная лошадка🥉"
        elif user.atk + user.hp >= 2000 and result == 'kach': badge = "💪Любитель качалки💪"
        elif int(forProd[0]) >= 1000 and result == 'prod': badge = "🤝Успешный продавец🤝"
        elif user.supporter >= int(time.time()) and result == 'supporter': badge = '♥️ToH supporter♥️'
        else:
            await bot.send_message(m.chat.id, "Такого значка не существует либо он вам недоступен.")
            return
        await db.Users.filter(id=user.id).update(badge=badge)
        await bot.send_message(m.chat.id, "Значок установлен в вашем профиле!")


async def getToken(m, user):
    if m.chat.id == m.from_user.id:
        user = await db.Users.exists(user_id=m.from_user.id)
        if user:
            user = await db.Users.get(user_id=m.from_user.id).first()
            if user.token and user.token != '':
                await bot.send_message(m.chat.id, "Используйте данный токен для авторизации на toh.fdu.su\n`{}`".format(user.token), parse_mode='markdown')
            else:
                newToken = db.ABC(20)
                await db.Users.filter(user_id=m.from_user.id).update(token=newToken)
                await bot.send_message(m.chat.id, "Используйте данный токен для авторизации на toh.fdu.su\n`{}`".format(newToken), parse_mode='markdown')

async def skills(m, user):
    if m.chat.id == m.from_user.id:
        user = await db.Users.exists(user_id=m.from_user.id)
        if user:
            user = await db.Users.get(user_id=m.from_user.id).first()
            text = "Твои доступные 🔘Очки прокачки: {}".format(user.uppts)
            #text += "\n\nГотовка - {}🔺".format(user.cooker)
            text += "\n\nВладение оружием - {}🔺".format(user.masterWeapon)
            text += "\n\nПьяная удача (автомат) - {}🔺".format(user.luckerAvtomat)
            text += "\n\nКарманная смекалка - {}🔺".format(user.skillInv)
            text += "\n\nКража - {}🔺".format(user.krazha)
            text += "\n\nАнти-кража - {}🔺".format(user.antikrazha)
            text += "\n\nРеакция PvP - {}🔺".format(user.reactionPvP)
            if user.uppts > 0:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Прокачка навыков', callback_data="skillsUp"))
                await bot.send_message(m.chat.id, text, reply_markup=markup)
            else:
                await bot.send_message(m.chat.id, text)

async def skillsUp(call):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    user = await db.Users.exists(user_id=call.from_user.id)
    if user:
        user = await db.Users.get(user_id=call.from_user.id).first()
        nameskills = {'masterWeapon': 'Владение оружием', 'luckerAvtomat': 'Пьяная удача (автомат)', 'skillInv': 'Карманная смекалка', 'krazha': 'Кража', 'antikrazha': 'Анти-кража', 'reactionPvP': 'Реакция PvP'}
        descr = {'masterWeapon': 'Навык владения оружием снижает количество необходимой энергии на использование особого навыка', 'luckerAvtomat': 'Навык пьяной удачи повышает шанс сорвать куш в автомате', 'skillInv': 'Навык карманной смекалки позволяет умещать больше вещей в инвентаре', 'krazha': 'Навык кражи позволяет воровать предметы у игроков', 'antikrazha': 'Навык анти-кражи расширяет лимит времени реакции на попытку кражи по отношению к вам.', 'reactionPvP': 'Навык реакции в PvP повышает время для возможности отразить нападение противника, по +5 секунд за уровень'}
        skills = {'masterWeapon': user.masterWeapon, 'luckerAvtomat': user.luckerAvtomat, 'skillInv': user.skillInv, 'krazha': user.krazha, 'antikrazha': user.antikrazha, 'reactionPvP': user.reactionPvP}
        prices = {}
        for z in skills:
            if skills[z] == 0: prices[z] = 1
            elif skills[z] == 1: prices[z] = 3
            elif skills[z] == 2: prices[z] = 6
            elif skills[z] == 3: prices[z] = 10
            elif skills[z] == 4: prices[z] = 15
            elif skills[z] == 5: prices[z] = 21
            elif skills[z] == 6: prices[z] = 28
            elif skills[z] == 7: prices[z] = 36
            elif skills[z] == 8: prices[z] = 45
            elif skills[z] == 9: prices[z] = 55
            else: skills[z] = 9999
        text = "Прокачка навыков:"
        for z in prices:
            text += "\n{} ({}) - {}🔘".format(nameskills[z], descr[z], prices[z])
            if int(prices[z]) <= user.uppts:
                markup.add(InlineKeyboardButton('Прокачать навык: {}'.format(nameskills[z]), callback_data="upSkill_{}".format(z)))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def upSkill(call):
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    skillToUp = _kach[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    user = await db.Users.exists(user_id=call.from_user.id)
    if user:
        user = await db.Users.get(user_id=call.from_user.id).first()
        nameskills = {'masterWeapon': 'Владение оружием', 'luckerAvtomat': 'Пьяная удача (автомат)', 'skillInv': 'Карманная смекалка', 'krazha': 'Кража', 'antikrazha': 'Анти-кража', 'reactionPvP': 'Реакция PvP'}
        skills = {'masterWeapon': user.masterWeapon, 'luckerAvtomat': user.luckerAvtomat, 'skillInv': user.skillInv, 'krazha': user.krazha, 'antikrazha': user.antikrazha, 'reactionPvP': user.reactionPvP}
        prices = {}
        for z in skills:
            if skills[z] == 0: prices[z] = 1
            elif skills[z] == 1: prices[z] = 3
            elif skills[z] == 2: prices[z] = 6
            elif skills[z] == 3: prices[z] = 10
            elif skills[z] == 4: prices[z] = 15
            elif skills[z] == 5: prices[z] = 21
            elif skills[z] == 6: prices[z] = 28
            elif skills[z] == 7: prices[z] = 36
            elif skills[z] == 8: prices[z] = 45
            elif skills[z] == 9: prices[z] = 55
            else: skills[z] = 9999
        if skillToUp == 'masterWeapon' and prices[skillToUp] <= user.uppts:
            user.masterWeapon += 1
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, masterWeapon=user.masterWeapon)
            text = "Ты успешно прокачал навык владения оружием"
        elif skillToUp == 'luckerAvtomat' and prices[skillToUp] <= user.uppts:
            user.luckerAvtomat += 1
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, luckerAvtomat=user.luckerAvtomat)
            text = "Ты успешно прокачал навык удачи в автомате"
        elif skillToUp == 'skillInv' and prices[skillToUp] <= user.uppts:
            user.skillInv += 1
            user.inventorySizeMax += 2
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, skillInv=user.skillInv, inventorySizeMax=user.inventorySizeMax)
            text = "Ты успешно прокачал навык карманной смекалки.\n+2📦"
        elif skillToUp == 'krazha' and prices[skillToUp] <= user.uppts:
            user.krazha += 1
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, krazha=user.krazha)
            text = "Ты успешно прокачал навык кражи"
        elif skillToUp == 'antikrazha' and prices[skillToUp] <= user.uppts:
            user.antikrazha += 1
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, antikrazha=user.antikrazha)
            text = "Ты успешно прокачал навык анти-кражи.\n+10 секунд к времени реакции"
        elif skillToUp == 'reactionPvP' and prices[skillToUp] <= user.uppts:
            user.reactionPvP += 1
            user.uppts -= prices[skillToUp]
            await db.Users.filter(id=user.id).update(uppts=user.uppts, reactionPvP=user.reactionPvP)
            text = "Ты успешно прокачал навык реакции PvP.\n+5 секунд к времени реакции"
        else:
            await bot.send_message(call.message.chat.id, "Неизвестная ошибка. Обратитесь в репорт\nSkill to up: {}".format(skillToUp))
            return
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


#################
#   INVENTORY   #
#################

async def inventory(m, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    inventorySize = await db.getInventorySize(user)

    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    count = {}
    size1 = {}
    sizes = {}

    
    if True:
        
        inventoryFastAccess = await db.InventoryFastAccess.filter(idplayer=user.id)
        text += "\nБыстрый доступ:"
        if inventoryFastAccess:
            text += "\n"
            _items = []
            for item in inventoryFastAccess: _items.append(item.name)
            if user.id not in db.inventorys:
                _getinv = 'getInv'
                await db.commitInventory(user, _getinv)

            for _item in db.inventorys[user.id]:
                if db.inventorys[user.id][_item]['active'] == 1:
                    if db.inventorys[user.id][_item]['name'] in _items:
                        item = {'id': _item, 'name': db.inventorys[user.id][_item]['name']}
                        if item['name'] in count:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] += 1
                            size1[item['name']] = size1[item['name']] + int(sizes[item['name']])
                        else:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] = 1
                            size1[item['name']] = int(size)
                            sizes[item['name']] = int(size)
                            markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item['id']))))

            for dict in count:
                name, size, bonus, atk_block, expires = await db.items(dict, check=True)
                text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
        else:
            text += "\nПредметы в быстром доступе отсутствуют. Добавить - /settings"
        markup.add(InlineKeyboardButton('🍔Еда', callback_data="inventory_eat"))
        markup.add(InlineKeyboardButton('🔩Расходники', callback_data="inventory_heals"))
        markup.add(InlineKeyboardButton('🛡Броня и оружие', callback_data="inventory_armor"))
        markup.add(InlineKeyboardButton('💍Прочее', callback_data="inventory_other"))
        check_a = await db.Inventory.exists(active=2, idplayer=user.id)
        if check_a:
            markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
        if user.lvl >= 35:
            markup.add(InlineKeyboardButton('Мешочек для хлама', callback_data="craftInv"))
        
        markup.add(InlineKeyboardButton('Обновить', callback_data="invRefresh"))


    else:
    
        inventory = await db.Inventory.filter(~Q(type='Растение'), ~Q(type='Крафт'), ~Q(name='Фильтры'), ~Q(name='Бустер'), idplayer=user.id, active=1).only('name', 'id')

        for item in inventory:
            if item.name in count:
                name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                count[item.name] += 1
                size1[item.name] = size1[item.name] + int(sizes[item.name])
            else:
                name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                count[item.name] = 1
                size1[item.name] = int(size)
                sizes[item.name] = int(size)
                if item.name != 'Котелок':
                    markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item.id))))
        for dict in count:
            name, size, bonus, atk_block, expires = await db.items(dict, check=True)
            text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
        check_kotelok = await db.Inventory.get_or_none(name='Котелок', idplayer=user.id, active=1).first()
        if check_kotelok:
            markup.add(InlineKeyboardButton('🥘Котелок', callback_data="invUse_{}".format(check_kotelok.id)))
        check_a = await db.Inventory.exists(active=2, idplayer=user.id)
        if check_a:
            markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
        if user.lvl >= 35:
            markup.add(InlineKeyboardButton('Мешочек для хлама', callback_data="craftInv"))
        checkBoosters = await db.Inventory.filter(name='Бустер', idplayer=user.id, active=1).only('lvl','id')
        if checkBoosters:
            for booster in checkBoosters:
                if booster.lvl == 730:
                    text += "\n⚡️Бустер 30дн"
                    markup.add(InlineKeyboardButton('⚡️Бустер 30дн',callback_data='invUse_{}'.format(booster.id)))
                else:
                    text += "\n⚡️Бустер {}ч".format(booster.lvl)
                    markup.add(InlineKeyboardButton('⚡️Бустер {}ч'.format(booster.lvl),callback_data='invUse_{}'.format(booster.id)))
    await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)




async def inv(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    inventorySize = await db.getInventorySize(user)

    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    count = {}
    size1 = {}
    sizes = {}

    
    if True:
        
        inventoryFastAccess = await db.InventoryFastAccess.filter(idplayer=user.id)
        text += "\nБыстрый доступ:"
        if inventoryFastAccess:
            text += "\n"
            _items = []
            for item in inventoryFastAccess: _items.append(item.name)
            if user.id not in db.inventorys:
                _getinv = 'getInv'
                await db.commitInventory(user, _getinv)

            for _item in db.inventorys[user.id]:
                if db.inventorys[user.id][_item]['active'] == 1:
                    if db.inventorys[user.id][_item]['name'] in _items:
                        item = {'id': _item, 'name': db.inventorys[user.id][_item]['name']}
                        if item['name'] in count:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] += 1
                            size1[item['name']] = size1[item['name']] + int(sizes[item['name']])
                        else:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] = 1
                            size1[item['name']] = int(size)
                            sizes[item['name']] = int(size)
                            markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item['id']))))

            for dict in count:
                name, size, bonus, atk_block, expires = await db.items(dict, check=True)
                text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
        else:
            text += "\nПредметы в быстром доступе отсутствуют. Добавить - /settings"
        markup.add(InlineKeyboardButton('🍔Еда', callback_data="inventory_eat"))
        markup.add(InlineKeyboardButton('🔩Расходники', callback_data="inventory_heals"))
        markup.add(InlineKeyboardButton('🛡Броня и оружие', callback_data="inventory_armor"))
        markup.add(InlineKeyboardButton('💍Прочее', callback_data="inventory_other"))
        check_a = await db.Inventory.exists(active=2, idplayer=user.id)
        if check_a:
            markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
        if user.lvl >= 35:
            markup.add(InlineKeyboardButton('Мешочек для хлама', callback_data="craftInv"))
        markup.add(InlineKeyboardButton('Обновить', callback_data="invRefresh"))

    else:
    
        inventory = await db.Inventory.filter(~Q(type='Растение'), ~Q(type='Крафт'), ~Q(name='Фильтры'), ~Q(name='Бустер'), idplayer=user.id, active=1).only('name', 'id')

        for item in inventory:
            if item.name in count:
                name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                count[item.name] += 1
                size1[item.name] = size1[item.name] + int(sizes[item.name])
            else:
                name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                count[item.name] = 1
                size1[item.name] = int(size)
                sizes[item.name] = int(size)
                markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item.id))))
        for dict in count:
            name, size, bonus, atk_block, expires = await db.items(dict, check=True)
            text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
        check_kotelok = await db.Inventory.get_or_none(name='Котелок', idplayer=user.id, active=1).first()
        if check_kotelok:
            markup.add(InlineKeyboardButton('🥘Котелок', callback_data="invUse_{}".format(check_kotelok.id)))
        check_a = await db.Inventory.exists(active=2, idplayer=user.id)
        if check_a:
            markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
        if user.lvl >= 35:
            markup.add(InlineKeyboardButton('Мешочек для хлама', callback_data="craftInv"))
        checkBoosters = await db.Inventory.filter(name='Бустер', idplayer=user.id, active=1).only('lvl','id')
        if checkBoosters:
            for booster in checkBoosters:
                if booster.lvl == 730:
                    text += "\n⚡️Бустер 30дн"
                    markup.add(InlineKeyboardButton('⚡️Бустер 30дн',callback_data='invUse_{}'.format(booster.id)))
                else:
                    text += "\n⚡️Бустер {}ч".format(booster.lvl)
                    markup.add(InlineKeyboardButton('⚡️Бустер {}ч'.format(booster.lvl),callback_data='invUse_{}'.format(booster.id)))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown', reply_markup=markup)


async def invRefresh(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    inventorySize = await db.getInventorySize(user)

    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    count = {}
    size1 = {}
    sizes = {}

    
    if True:
        _getinv = 'getInv'
        await db.commitInventory(user, _getinv)

        inventoryFastAccess = await db.InventoryFastAccess.filter(idplayer=user.id)
        text += "\nБыстрый доступ:"
        if inventoryFastAccess:
            text += "\n"
            _items = []
            for item in inventoryFastAccess: _items.append(item.name)

            for _item in db.inventorys[user.id]:
                if db.inventorys[user.id][_item]['active'] == 1:
                    if db.inventorys[user.id][_item]['name'] in _items:
                        item = {'id': _item, 'name': db.inventorys[user.id][_item]['name']}
                        if item['name'] in count:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] += 1
                            size1[item['name']] = size1[item['name']] + int(sizes[item['name']])
                        else:
                            name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                            count[item['name']] = 1
                            size1[item['name']] = int(size)
                            sizes[item['name']] = int(size)
                            markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item['id']))))

            for dict in count:
                name, size, bonus, atk_block, expires = await db.items(dict, check=True)
                text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])
        else:
            text += "\nПредметы в быстром доступе отсутствуют. Добавить - /settings"
        markup.add(InlineKeyboardButton('🍔Еда', callback_data="inventory_eat"))
        markup.add(InlineKeyboardButton('🔩Расходники', callback_data="inventory_heals"))
        markup.add(InlineKeyboardButton('🛡Броня и оружие', callback_data="inventory_armor"))
        markup.add(InlineKeyboardButton('💍Прочее', callback_data="inventory_other"))
        check_a = await db.Inventory.exists(active=2, idplayer=user.id)
        if check_a:
            markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
        if user.lvl >= 35:
            markup.add(InlineKeyboardButton('Мешочек для хлама', callback_data="craftInv"))
        markup.add(InlineKeyboardButton('Обновить', callback_data="invRefresh"))
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Обновлено")
    await bot.send_message(call.message.chat.id, text, parse_mode='markdown', reply_markup=markup)



async def inventory_(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    inventorySize = await db.getInventorySize(user)

    text = "🎒*Инвентарь* (📦{}/{})\n".format(inventorySize, user.inventorySizeMax)
    count = {}
    size1 = {}
    sizes = {}
    if user.id not in db.inventorys:
        if call.data.split("_")[1] == 'eat':
            _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки"]
            inventory = await db.Inventory.filter(type__in=_types, idplayer=user.id, active=1).only("name", "id")
        elif call.data.split("_")[1] == 'heals':
            _types = ["Зелье", "Сундук", "Хлам", "Экипировка"]
            inventory = await db.Inventory.filter(type__in=_types, idplayer=user.id, active=1).only("name", "id")
        elif call.data.split("_")[1] == 'armor':
            _types = ["Броня", "Оружие"]
            inventory = await db.Inventory.filter(type__in=_types, idplayer=user.id, active=1).only("name", "id")
        elif call.data.split("_")[1] == 'other':
            _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки", "Броня", "Оружие", 
            "Зелье", "Сундук", "Хлам", "Экипировка"]
            inventory = await db.Inventory.filter(~Q(type__in=_types), idplayer=user.id, active=1).only("name", "id")


        if inventory:
            for item in inventory:
                if item.name in count:
                    name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                    count[item.name] += 1
                    size1[item.name] = size1[item.name] + int(sizes[item.name])
                else:
                    if item.name != "Бустер":
                        name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
                        count[item.name] = 1
                        size1[item.name] = int(size)
                        sizes[item.name] = int(size)
                        markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(item.id))))
                    else:
                        itm = await db.Inventory.get(id=item.id).first()
                        markup.add(InlineKeyboardButton('⚡️Бустер ({}ч)'.format(itm.lvl), callback_data="invUse_{}".format(str(item.id))))
            for dict in count:
                name, size, bonus, atk_block, expires = await db.items(dict, check=True)
                text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])

        else:
            text += "\nПредметы отсутствуют"
    else:
        if call.data.split("_")[1] == 'eat':
            _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки"]
        elif call.data.split("_")[1] == 'heals':
            _types = ["Зелье", "Сундук", "Хлам", "Экипировка"]
        elif call.data.split("_")[1] == 'armor':
            _types = ["Броня", "Оружие"]
        elif call.data.split("_")[1] == 'other':
            _types = ["Еда", "Ингредиент готовки", "Редкий ингредиент готовки", "Особый ингредиент готовки", "Броня", "Оружие", 
            "Зелье", "Сундук", "Хлам", "Экипировка"]
        inventory = {}
        for _item in db.inventorys[user.id]:
            if db.inventorys[user.id][_item]['active'] == 1:
                item = {'id': _item, 'name': db.inventorys[user.id][_item]['name'], 'type': db.inventorys[user.id][_item]['type']}
                if call.data.split("_")[1] == 'other':
                    if item['type'] not in _types:
                        inventory[_item] = {'id': _item, 'name': db.inventorys[user.id][_item]['name'], 'type': db.inventorys[user.id][_item]['type']}
                else:
                    if item['type'] in _types:
                        inventory[_item] = {'id': _item, 'name': db.inventorys[user.id][_item]['name'], 'type': db.inventorys[user.id][_item]['type']}
        if inventory:
            for _item in inventory:
                item = inventory[_item]
                if item['name'] in count:
                    name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                    count[item['name']] += 1
                    size1[item['name']] = size1[item['name']] + int(sizes[item['name']])
                else:
                    if item['name'] != "Бустер":
                        name, size, bonus, atk_block, expires = await db.items(item['name'], check=True)
                        count[item['name']] = 1
                        size1[item['name']] = int(size)
                        sizes[item['name']] = int(size)
                        markup.add(InlineKeyboardButton('{}'.format(str(name)), callback_data="invUse_{}".format(str(_item))))
                    else:
                        itm = await db.Inventory.get(id=_item).first()
                        markup.add(InlineKeyboardButton('⚡️Бустер ({}ч)'.format(itm.lvl), callback_data="invUse_{}".format(str(itm.id))))
            for dict in count:
                name, size, bonus, atk_block, expires = await db.items(dict, check=True)
                text += "\nх{} {} 📦{}".format(count[dict], name, size1[dict])

        else:
            text += "\nПредметы отсутствуют"



    markup.add(InlineKeyboardButton('В инвентарь', callback_data="inv"))

    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown', reply_markup=markup)





async def craftInv(call, user):
    await bot.edit_message_text("Подсматриваем в мешочек, это займёт некоторое время...", call.message.chat.id, call.message.message_id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    inventorySize = await db.Inventory.filter(active=5, idplayer=user.id).count()
    text = "🎒*Мешочек для хлама* (📦{})\n".format(inventorySize)
    checkItems = await db.Inventory.exists(idplayer=user.id, active=5)
    if checkItems:
        if True:
            getItems = await db.Inventory.filter(idplayer=user.id, active=5).only('name', 'lvl').order_by('lvl')
            count = {}
            lvls = {}
            lastLvl = 0
            for z in getItems:
                if z.lvl != lastLvl:
                    lvls = {}
                    lastLvl = z.lvl
                if z.name in count and z.name in lvls:
                    pass
                else:
                    count[z.name] = 1
                    lvls[z.name] = z.lvl
                    _count = await db.Inventory.filter(idplayer=user.id, active=5, lvl=z.lvl, name=z.name).count()
                    text += "\nx{} {}({}ур)".format(_count, z.name, z.lvl)
    else:
        text += "\nК сожалению, у вас нет подходящих предметов..."
    check_a = await db.Inventory.exists(active=2, idplayer=user.id)
    if check_a:
        markup.add(InlineKeyboardButton('Снаряжение', callback_data="armorpers"))
    markup.add(InlineKeyboardButton('В инвентарь', callback_data="inv"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')



async def invUse(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    result = await db.Inventory.exists(id=use)
    if not result:
        return
    result = await db.Inventory.get(id=use).first()
    if user.location == 'Дом':
        checkhouse = await db.Houses.get_or_none(owner=user.id)
        if checkhouse and checkhouse.lvl > 4:
            markup.add(InlineKeyboardButton('Оставить на складе', callback_data="iveSklad_{}".format(str(use))))
    if result.type == 'Еда':
        if result.name == 'Валентинка':
            text = "💌Валентинка. С Днём Святого Валентина!"
        else:
            leftTime = (result.expires - time.time()) / 3600
            if leftTime >= 0:
                text = "{}\n+🦴{}сытости.\nВполне съедобно еще {}ч.\nСъесть?".format(str(result.name), str(result.bonus), round(leftTime, 2))
            else:
                text = "{}\n+🦴{}сытости.\nКажется, это уже далеко не съедобно...".format(str(result.name), str(result.bonus))
        markup.add(InlineKeyboardButton('Сьесть'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Хлам":
        text = "{}. \nСудя по всему, хлам. Может кому и пригодится...".format(str(result.name))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Зелье":
        text = "{}. Выпить зелье?".format(result.name)
        markup.add(InlineKeyboardButton('Выпить'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Котелок':
        oduvanchiki = user.oduvanchik
        rca = user.rca
        sakura = user.sakura
        roza = user.roza
        ostanki = await db.Inventory.filter(name='Останки героев', idplayer=result.idplayer, active=1).count()
        if sakura >= 10 and roza >= 8 and rca >= 8 and ostanki >= 3: markup.add(InlineKeyboardButton('Зелье восстановления', callback_data="varenie_restore"))
        if oduvanchiki >= 2 and rca >= 1: markup.add(InlineKeyboardButton('Среднее зелье здоровья', callback_data="varenie_sredne"))
        if oduvanchiki >= 1 and roza >= 1 and rca >= 1: markup.add(InlineKeyboardButton('Большое зелье здоровья', callback_data="varenie_big"))
        text = 'Котелок. Удивительная вещь - можешь приготовить себе борщ, можешь сварить неизвестные, но легендарные "Макароны". Но главное применение котелка - не варка бывшего соседа, как ни странно, а варение зелий.\nРецепты зелий выписаны на котелке.\n\nСреднее зелье здоровья: 2🌼 1🌷\nБольшое зелье здоровья: 1🌼 1🌷 1🌹\nЗелье восстановление: 10🌸 8🌷 8🌹 3🦴'
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name='Рецепт приготовления малого зелья восстановления', active=0)
        if checkRecipy:
            text += '\nМалое зелье восстановления: 5🌼 3🌷 3🌹 1🦴'
            if oduvanchiki >= 5 and roza >= 3 and rca >= 3 and ostanki >= 1: 
                markup.add(InlineKeyboardButton('Малое зелье восстановления', callback_data="varenie_restoreSmall"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name='Рецепт приготовления среднего зелья восстановления', active=0)
        if checkRecipy:
            text += '\nСреднее зелье восстановления: 8🌼 5🌷 5🌹 2🦴'
            if oduvanchiki >= 8 and roza >= 5 and rca >= 5 and ostanki >= 2: 
                markup.add(InlineKeyboardButton('Среднее зелье восстановления', callback_data="varenie_restoreMedium"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name='Рецепт бамбук', active=0)
        if checkRecipy:
            text += '\nБамбук для курения: 4🌼 2🌷 2🌹 1🌸'
            if oduvanchiki >= 4 and roza >= 2 and rca >= 2 and sakura >= 1: 
                markup.add(InlineKeyboardButton('Бамбук для курения', callback_data="varenie_bamboo"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name='Рецепт героИн', active=0)
        if checkRecipy:
            text += '\nГероИн: 10🦴'
            if ostanki >= 10: 
                markup.add(InlineKeyboardButton('ГероИн', callback_data="varenie_geroin"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name = 'Рецепт боярышник', active=0)
        if checkRecipy:
            text += '\nНастойка боярышника 90°: 6🌼 3🌷 2🌹 4🌸 2🦴'
            if oduvanchiki >= 6 and roza >= 3 and rca >= 2 and sakura >= 4 and ostanki >= 2: 
                markup.add(InlineKeyboardButton('Настойка боярышника', callback_data="varenie_boyara"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name = 'Рецепт ВиАгро', active=0)
        if checkRecipy:
            text += '\n💊ВиАгро: 35🌼 20🌹'
            if oduvanchiki >= 35 and roza >= 20: 
                markup.add(InlineKeyboardButton('ВиАгро', callback_data="varenie_viagra"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name = 'Рецепт паучий афродизиак', active=0)
        if checkRecipy:
            text += '\n🕸Паучий афродизиак: 10🌼 10🌷 10🌹 10🌸 5🦴'
            if oduvanchiki >= 10 and roza >= 10 and rca >= 10 and sakura >= 10 and ostanki >= 5: 
                markup.add(InlineKeyboardButton('Паучий афродизиак', callback_data="varenie_ilovestas"))
        checkRecipy = await db.Inventory.exists(idplayer=result.idplayer, name='Рецепт бакин', active=0)
        if checkRecipy:
            text += '\n💊Бакин: 3🌼 7🌷 2🌹 7🌸'
            if oduvanchiki >= 3 and roza >= 2 and rca >= 7 and sakura >= 7 : 
                markup.add(InlineKeyboardButton('Бакин', callback_data="varenie_bakin"))
        text += "\n\nЛимит на цветы: {}📦/вид\n{}🌼 {}🌷 {}🌹 {}🌸 {}🦴".format(user.kotelokLimit, oduvanchiki, rca, roza, sakura, ostanki)
        markup.add(InlineKeyboardButton('Вернуться в инвентарь', callback_data="inv"))
    elif result.type == "Сундук":
        text = "Сундук. Попытаться открыть?".format(result.name)
        markup.add(InlineKeyboardButton('Открыть'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Дрова':
        text = "Дрова. Можно разжечь костёр".format(result.name)
        markup.add(InlineKeyboardButton('Погреться', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Кофе':
        text = f"{result.name}. Восстанавливает 70⚡️. Выпить?"
        markup.add(InlineKeyboardButton('Выпить', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Артефакт":
        if result.name == 'Амулет здоровья':
            text = "{} ({}🔆). Позволяет пассивно восстанавливать каждую минуту 10%❤️ в обмен на 5⚡️. За каждый новый уровень количество восстанавливаемого здоровья увеличивается на 1%".format(result.name, result.lvl)
        elif result.name == 'Осколок энергии':
            text = "{} ({}🔆). Позволяет пассивно восстанавливать каждую минуту 5⚡️, если энергия выше 5⚡️, но не выше 70⚡️. За каждый новый уровень количество восстанавливаемой энергии увеличивается на 0.5⚡️".format(result.name, result.lvl)
        elif result.name == 'Осколок огня':
            text = "{} ({}🔆). Благодаря специальной ауре, после вашей атаки монстры начинают гореть из-за получают дополнительно 5% (10% в Заснеженном лесу) от собственного максимального здоровья. За каждый новый уровень урон повышается на 1%".format(result.name, result.lvl)
        elif result.name == 'Анализатор БМ':
            text = "{}. Работает в качестве оценщика шансов в PvP. Зелёный сектор - шанс на победу весьма велик. Желтый сектор - шансы примерно равны. Красный - вам придётся очень сильно постараться чтобы выиграть.".format(result.name)
        elif result.name == 'Анти-анализатор БМ':
            text = "{}. Скрывает для врага, имеющего ''Анализатор БМ'' шанс на победу против вас".format(result.name)
        elif result.name == 'Камень энергии':
            text = "{} ({}🔆). Позволяет пассивно восстанавливать каждую минуту 7⚡️. За каждый новый уровень количество восстанавливаемой энергии увеличивается на 2⚡️".format(result.name, result.lvl)
        elif result.name == 'Горшок лепрекона':
            text = "{} ({}🔆). При проигрыше в PvE и смерти от голода монеты не тратятся, однако с монстров можно получить 60% монет. За каждый новый уровень процент получаемого золота повышается на 3%".format(result.name, result.lvl)
        elif result.name == 'Карманная дриада':
            text = "{} ({}🔆). Удваивает выпадение цветов. За каждый новый уровень повышается шанс получения трёх цветков на 5%".format(result.name, result.lvl)
        elif result.name == 'Кольцо всеотражения':
            text = "{} ({}🔆). C шансом в 25% отражает атаку монстра в него самого. За каждый новый уровень кольца шанс отражения повышается на 2.5%".format(result.name, result.lvl)
        elif result.name == 'Осколок льда':
            text = "Осколок льда. С шансом в 20% каждый ход может нанести эффект холода на монстра - Эффект холода замораживает монстра из-за чего он (монстр) не может атаковать один ход, но получает на 25% меньше урона, во время заморозки."
        elif result.name == 'Осколок эфира':
            text = "Осколок эфира. В конце битвы с монстром восстанавливает ♥️, равное количеству убитых монстров, умноженному на {} (счётчик каждые 5 минут падает на 1, восстанавливает не более 50%♥️).".format(etheriumBonus)
        elif result.name == 'Сувенир с моря': #Мейн крит урон
            mainBuff = result.lvl
            secondBuff = int(result.lvl / 2)
            text = "{} ({}🔆)\nАртефакт.\n\nХарактеристики:\n+{}% Крит урона\n+{}% Доп урона\n+{}% шанс Крит удара".format(str(result.name), result.lvl, mainBuff, secondBuff, secondBuff)
        elif result.name == 'Квинтэссенция камня': #Мейн армор
            mainBuff = result.lvl
            secondBuff = int(result.lvl / 2)
            text = "{} ({}🔆)\nАртефакт.\n\nХарактеристики:\n+{}% Брони\n+{}% Доп урона\n+{}% Вампиризм".format(str(result.name), result.lvl, mainBuff, secondBuff, secondBuff)
        elif result.name == 'Камень-металлолом': #Мейн вампиризм
            mainBuff = result.lvl
            secondBuff = int(result.lvl / 2)
            text = "{} ({}🔆)\nАртефакт.\n\nХарактеристики:\n+{}% Вампиризм\n+{}% Крит урона\n+{}% Армора".format(str(result.name), result.lvl, mainBuff, secondBuff, secondBuff)
        elif result.name == 'Палка ярости': #Мейн дд
            mainBuff = result.lvl
            secondBuff = int(result.lvl / 2)
            text = "{} ({}🔆)\nАртефакт.\n\nХарактеристики:\n+{}% Доп урона".format(str(result.name), result.lvl, mainBuff)
        else:
            text = "{}. Действие неизвестно".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == "Броня":
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        if result.name == 'Железный щит':
            text = "{}. 5% шанс на блокирование удара монстра (⚔️ - {}%) Использовать?".format(name, atk_block)
        elif result.name == 'Щит бомжа':
            text = "{}. 10% шанс на блокирование удара монстра (⚔️ - {}%) Использовать?".format(name, atk_block)
        elif result.name == 'Золотая покрышка':
            text = "{}. 15% шанс на блокирование удара монстра (⚔️ - {}%) Использовать?".format(name, atk_block)
        elif result.name == 'Щит верности Раскуловой':
            text = "{}. 20% шанс на блокирование удара монстра (⚔️ - {}%) Использовать?".format(name, atk_block)
        else:
            text = "{}. +{}🛡 (⚔️ - {}%) Использовать?".format(name, bonus, atk_block)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Бамбук для курения':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. До конца неизвестно, как точно из обмельчённых и вывареных цветов получается что-то, похожее на никотин, но пусть будет так. В этом мире всё возможно. Вот так умельцы и варят, а потом заворачивают этот странный порошок в кусок газеты, чтобы покурить.\n\nКурение убивает. Восстанавливает 60⚡️, но взамен может украсть здоровье".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'ГероИн':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. Пыль героев ГероИн - именно так прозвали странную жидкость, которая варится с человеческих останков. Не рекомендуется злоупотреблять\n\nПосле употребления ты получаешь ускоренное перемещение на 10 минут, а так же случайный эффект".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Паучий афродизиак':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. \n\nПри принятии во внутрь делает тебя привлекательнее в глазах противоположного пола, но это тебе не поможет ведь в ТоХ нет секса. Но зато увеличивает агрессивность мобов в поле что приводит к увеличению их хп и атаки в два раз, и соответственно добычу с них. Действует 20 минут.".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Бакин':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. \n\nБакин можно назвать виагрой для мозга. После принятия, ты получаешь такой кайф - становишься умнее, ловчее и проворнее. Ну а на самом деле? Можешь идти назад.".format(result.name)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Полотенце':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. Помогает избавиться от высокой влажности, если вытереться".format(name)
        markup.add(InlineKeyboardButton('Вытереться'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Багровая бомба':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. Взрывчатка облепленная кучей раздробленной чешуи. Наносит урон по площади. Бросая под себя, нужно проявлять предельную осторожность.".format(result.name)
        markup.add(InlineKeyboardButton('Бросить под себя', callback_data="bomb_{}_1".format(str(use))))
        markup.add(InlineKeyboardButton('Бросить слабо', callback_data="bomb_{}_2".format(str(use))))
        markup.add(InlineKeyboardButton('Бросить сильно', callback_data="bomb_{}_3".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Билет на тот свет':
        name, size, bonus, atk_block, expires = await db.items(result.name, check=True)
        text = "{}. Позволяет телепортироваться к месту последней смерти (или телепортации)".format(result.name)
        markup.add(InlineKeyboardButton('Проколоть билетик', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'ВиАгро':
        text = "💊ВиАгро. Волшебная пилюля, улучшающая твои характеристики на 30% во время итогового рейда в башне (И снижает характеристики на 30% в PvP). После использования, с вас снимается эффект Плаща-невидимки (на всех локациях). После окончания рейда эффект таблетки исчезает."
        markup.add(InlineKeyboardButton('Выпить таблетку', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Кошелёк падшего героя':
        text = "Кошелёк падшего героя. Нужно отнести его охраннику, наверное речь тогда с ним шла об этом человеке."
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Свиток башни':
        text = "📜Свиток башни. Моментально перемещает вас в башню, минуя долгую прогулку по тропе."
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Туннельный свиток':
        text = "📜Туннельный свиток. Позволяет телепортироваться в стартовый город."
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Бесплатная путёвка на свалку':
        text = "🎟Бесплатная путёвка на свалку. Телепортирует на 15 минут на Свалку SR2"
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Карта заброшенного архива':
        text = "📜Карта заброшенного архива. Получена от старого деда который уверяет что в архиве находится полезная информация."
        markup.add(InlineKeyboardButton('Посмотреть'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Документ DSFB-4':
        text = "📜Документ DSFB-4. Получена внутри заброшенного архива. Сам документ написан на непонятном языке, только заголовок можно понять. Возможно, есть смысл поспрашивать в Хэвенбурге по поводу документа."
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Странная заготовка':
        text = "🔦Странная заготовка оружия Клары. Необходимо носить с собой чтобы зарядить её энергией.\n\nЗаряжено на 💡{}ед.".format(result.bonus)
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Письмо для Табернам':
        text = "✉️Письмо для Табернам от Табервама. Нужно отдать его Табернам."
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Письмо для Табервам':
        text = "✉️Письмо для Табервама от Табернам. Нужно отдать его Таберваму."
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == 'Ингредиент готовки':
        leftTime = (result.expires - time.time()) / 3600
        if leftTime >= 0:
            text = "{}\nИнгредиент готовки.\nВполне свежее еще {}ч.\n".format(str(result.name), round(leftTime, 2))
        else:
            text = "{}\nИнгредиент готовки.\nКажется, с этим уже ничего не приготовить...".format(str(result.name))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == 'Редкий ингредиент готовки':
        leftTime = (result.expires - time.time()) / 3600
        if leftTime >= 0:
            text = "{}\n⭐️⭐️Ингредиент готовки.\nВполне свежее еще {}ч.\n".format(str(result.name), round(leftTime, 2))
        else:
            text = "{}\n⭐️⭐️Ингредиент готовки.\nКажется, с этим уже ничего не приготовить...".format(str(result.name))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.type == 'Легендарный ингредиент готовки':
        leftTime = (result.expires - time.time()) / 3600
        if leftTime >= 0:
            text = "{}\n⭐️⭐️⭐️Ингредиент готовки.\nВполне свежее еще {}ч.\n".format(str(result.name), round(leftTime, 2))
        else:
            text = "{}\n⭐️⭐️⭐️Ингредиент готовки.\nКажется, с этим уже ничего не приготовить...".format(str(result.name))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    elif result.name == 'Бустер':
        text = "⚡️Бустер делает тебя выносливее, быстрее и лучше! (перемещение занимает минуту, количество получаемого опыта и золота повышено на 25%). Работает {}ч".format(result.lvl)
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Противогаз':
        allFilters = await db.Inventory.filter(name='Фильтры', bonus__gt=0, idplayer=user.id).only('bonus')
        filters = 0
        for z in allFilters: filters += z.bonus
        text = "Противогаз - сверх-необходимая штука в Метро. Без противогаза и фильтров в нём ты очень быстро задохнёшься.\nСостояние противогаза: {}/100\nТвоих фильтров хватит на {}-К".format(result.bonus, filters)
        markup.add(InlineKeyboardButton('Надеть', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.type == 'Рыбалка':
        text = "{}. Использовать?".format(result.name)
        markup.add(InlineKeyboardButton('Использовать', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == 'Хлопушка':
        text = "{}. Оглушает ближайших игроков на 10 минут (в т.ч. использующего хлопушку) - плащи перестают работать, здоровье не видно, в /look_around видно всех оглушенных".format(result.name)
        markup.add(InlineKeyboardButton('Хлопнуть!', callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    elif result.name == "Золотой кольт":
        if result.descr:
            text = "Золотой кольт. Элитная вариация обычного кольта. Дополнительной особенностью является возможность нанесения собственной гравировки на оружие, которую будет видеть поверженный противник при поражении в PvP\nНа рукояти выгравирован текст:\n\n{}".format(result.descr)
        else:
            text = "Золотой кольт. Элитная вариация обычного кольта. Дополнительной особенностью является возможность нанесения собственной гравировки на оружие, которую будет видеть поверженный противник при поражении в PvP"
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Нанести гравировку'.format(str(result.name)), callback_data="koltGrav_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
    else:
        text = "{}. \nИспользовать?".format(str(result.name))
        markup.add(InlineKeyboardButton('Использовать'.format(str(result.name)), callback_data="invUsing_{}".format(str(use))))
        markup.add(InlineKeyboardButton('Выбросить', callback_data="invDrop_{}".format(str(use))))
        markup.add(InlineKeyboardButton('В инвентарь', callback_data="inveClose"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


async def invDrop(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    result = await db.Inventory.get(id=use)
    checkOther = await db.Inventory.filter(name=result.name, active=1, idplayer=result.idplayer).count()
    if checkOther >= 2:
        text = "У тебя х{} {}. Введи количество которое хочешь выбросить".format(checkOther, result.name)
        coinUserStatus[call.from_user.id] = 'dropItem_{}'.format(result.id)
    else:
        if result.active == 2:
            if result.type == 'Броня':
                await db.Users.filter(id=result.idplayer).update(armor=F('armor') - result.bonus)
        result.active = 0
        await result.save()
        text = "Ты выбросил {}".format(result.name)
        await db.commitInventory(user, result)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
async def invSklad(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    if user.location == 'Дом':
        checkhouse = await db.Houses.get_or_none(owner=user.id)
        if checkhouse and checkhouse.lvl > 1:
            currentSize = await db.getHouseInventorySize(user)
            result = await db.Inventory.get(id=use)
            size = await db.items(result.name, check='size')
            if size + currentSize <= checkhouse.inventory:
                result.active = 10
                await result.save()
                text = "Ты оставил на складе {}".format(result.name)
            else:
                text = "На складе недостаточно места."
    else:
        text = "Ты находишься вне дома."
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m: coinUserStatus and m.from_user.id == m.chat.id and m.from_user.id in coinUserStatus and coinUserStatus[m.from_user.id] and coinUserStatus[m.from_user.id].startswith('dropItem_'))
async def InvDrop(m):
    user = await db.Users.get(user_id=m.from_user.id)
    _itemId = coinUserStatus[m.from_user.id].split("_")
    itemId =  _itemId[1]
    item = await db.Inventory.get(id=itemId)
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
    allItemsToDrop = await db.Inventory.filter(name=item.name, active=1, idplayer=user.id).limit(count)
    for i in allItemsToDrop:
        i.active = 0
        await i.save()
        await db.commitInventory(user, i)
    await bot.send_message(m.chat.id, "Ты выбросил х{} {}".format(count, item.name))


bombKD = {}
async def bomb_(call, user): 
    if user.id in bombKD and bombKD[user.id] > int(time.time()):
        await bot.edit_message_text("Ты еще не готов к использованию бомбы", call.message.chat.id, call.message.message_id)
        return
    if user.location == 'Хэвенбург' or user.location == 'Кавайня' or user.location == 'Океанус' or user.location == 'Город':
        await bot.edit_message_text("*Голос в голове* - Я слышал, за терракты в городе тебе делают неприятности с твоим ♂Ass♂", call.message.chat.id, call.message.message_id)
        return
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    sila = do[2]
    checkPlash = await db.Inventory.exists(name='Плащ-невидимка', idplayer=user.id, active=2)
    if checkPlash:
        await bot.edit_message_text("Из-за плаща ты не можешь бросить бомбу. Необходимо его снять.", call.message.chat.id, call.message.message_id)
        return
    item = await db.Inventory.get(id=use)
    result = await db.Inventory.get(name=item.name, idplayer=user.id, active=1).first()
    if result.active == 1 and result.idplayer == user.id:
        bombKD[user.id] = int(time.time()) + 60
        result.active = 0
        await db.commitInventory(user, result)
        progLoc = user.progLoc.split('|')
        _progLoc = progLoc[1]
        if sila == '1': attackTo = int(_progLoc)
        elif sila == '2': attackTo = int(_progLoc) + 1
        elif sila == '3': attackTo = int(_progLoc) + 2
        else: attackTo = int(_progLoc) + 1
        progLocAtk = "{}|{}".format(progLoc[0], attackTo)
        usrs = await db.Users.filter(location=user.location, progLoc=progLocAtk)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Отправить послание игроку (1💎)', callback_data="poslanie_{}".format(user.user_id)))
        for z in usrs:
            z.nowhp = int(z.nowhp) - int((z.hp) * 0.2)
            if z.nowhp <= 0:
                try:
                    if z.id != user.id:
                        wastedgold = int(z.money * 0.2)
                        await bot.send_message(z.user_id, "Звук падения чего-то тяжелого, сопровождающийся криком _Ложись!_ — последнее что ты слышал перед тем, как сотни крошечных, острых точно лезвие осколков пронзили твое тело во всех возможных и невозможных местах, спровоцировав разрывы тканей и сильнейшее жопное кровотечение. _WASTED_\nПотеряно: {}💰".format(wastedgold), reply_markup=markup, parse_mode='markdown')
                    else:
                        await bot.send_message(z.user_id, "Камика́дзе (яп. 神風 камикадзэ) – часть широкого японского термина токкотай, которым обозначали всех добровольцев-смертников.")
                except:
                    pass
                z.nowhp = z.hp
                z.location = 'Хэвенбург'
                z.position = 'Номер в отеле'
                z.money = int(z.money - (z.money * 0.2))
                await db.Users.filter(id=z.id).update(nowhp=z.hp, location='Хэвенбург', position='Номер в отеле', money=z.money, battleStatus=0)
            else:
                try:
                    await bot.send_message(z.user_id, "Звук падения чего-то тяжелого, сопровождающийся криком Ложись! — все, что ты слышал перед тем, как в тебя впились сотни осколков от брошенной каким-то мудаком гранаты. \n ¯\_(ツ)_/¯")
                except:
                    pass
            await db.Users.filter(id=z.id).update(nowhp=z.nowhp)
        await result.save()
        text = "Ты использовал {} и, наверное, кого-то задел. Стоит пойти проверить?".format(result.name)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



effectUsers = {}



async def invUsing(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    do = call.data.split('_')
    use = do[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    result = await db.Inventory.exists(id=use)
    if not result:
        return
    result = await db.Inventory.get_or_none(id=use)
    if user.battleStatus == 2:
        await bot.edit_message_text("У тебя не получится что-то использовать - вы дерётесь!", call.message.chat.id, call.message.message_id)
        return
    if result and result.active != 0 and user.id == result.idplayer:
        pass
    else:
        checkOther = await db.Inventory.exists(name=result.name, idplayer=user.id, active=1)
        if checkOther:
            result = await db.Inventory.get(name=result.name, idplayer=user.id, active=1).first()
        else:
            text = "Предмета не существует!"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
    if result.type == 'Еда' or result.name == 'Валентинка':
        text = await db.useEat(user, result)
    elif result.name  ==  'Свиток башни':
        if user.quest == 'Искатель приключений' and user.questStatus == 1 and user.location != 'Песчаная пирамида':
            progSplit = user.progLoc.split("|")
            num = progSplit[1]
            quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
            quest.progress += int(num)
            await db.tempQuest.filter(user_id=user.user_id, quest=user.quest, status=0).update(progress=quest.progress)
        if user.battleStatus == 1:
            mob = await db.Monsters.exists(id=user.battleWith)
            if mob:
                mob = await db.Monsters.get(id=user.battleWith)
                mob.battleStatus = 0
                mob.nowhp = mob.hp
                await db.Monsters.filter(id=user.battleWith).update(battleStatus=0, nowhp=mob.hp)
                user.battleStatus = 0
        result.active = 0
        user.location = 'Первый этаж башни'
        user.progLoc = 'Первый этаж башни|0'
        user.progStatus = 1
        user.position = 'Площадь'
        user.battleStatus = 0
        text = "Ты прочёл 📜Свиток башни"
        await db.Users.filter(id=user.id).update(location=user.location, position=user.position, battleStatus=0, progLoc=user.progLoc, progStatus=1)
    elif result.name == 'Туннельный свиток':
        result.active = 0
        user.location = 'Город'
        user.position = 'Площадь'
        await db.Users.filter(id=user.id).update(location=user.location, position=user.position, battleStatus=0)
        text = "Ты прочёл 📜Туннельный свиток"
    elif result.name == "Бесплатная путёвка на свалку":
        result.active = 0
        await result.save()
        user.location = "Свалка SR2"
        await db.Users.filter(id=user.id).update(location=user.location, battleStatus=0, progLoc="Свалка SR2|0", progStatus=1)
        await bot.edit_message_text("Начинается телепортация на Свалку SR2. Осторожнее, двери закрываются, монстры начинают наступление...", call.message.chat.id, call.message.message_id)
        await asyncio.sleep(10)
        await user.refresh_from_db()
        await giveMobSR(user)
        await asyncio.sleep(900)
        await user.refresh_from_db()
        if user.location == "Свалка SR2":
            await db.Users.filter(id=user.id).update(location="Хэвенбург")
            try:
                await bot.send_message(user.user_id, "Время действия путёвки кончилось.")
            except:
                pass
        text = "Успешно использовано"
    elif result.name == 'Свиток телепортации':
        if user.quest == 'Искатель приключений' and user.questStatus == 1 and user.location != 'Песчаная пирамида':
            progSplit = user.progLoc.split("|")
            num = progSplit[1]
            quest = await db.tempQuest.get_or_none(user_id=user.user_id, quest=user.quest, status=0).first()
            if quest:
                quest.progress += int(num)
                await db.tempQuest.filter(user_id=user.user_id, quest=user.quest, status=0).update(progress=quest.progress)
        if user.battleStatus == 1:
            mob = await db.Monsters.exists(id=user.battleWith)
            if mob:
                mob = await db.Monsters.get(id=user.battleWith)
                mob.battleStatus = 0
                mob.nowhp = mob.hp
                await db.Monsters.filter(id=user.battleWith).update(battleStatus=0, nowhp=mob.hp)
                user.battleStatus = 0
        result.active = 0
        checkgorod = await db.Inventory.exists(idplayer=user.id, name='Большой город')
        user.position = 'Площадь'
        user.battleStatus = 0
        text = "Ты прочёл 📜Свиток телепортации"
        await result.save()
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        if checkgorod:
            user.location = 'Хэвенбург'
            call.data = 'nav_bigcity_centr'
            await db.Users.filter(id=user.id).update(location=user.location, position=user.position, battleStatus=0)
            await nav_bigcity(call, user)
        else:
            user.location = 'Город'
            call.data = 'nav_city_centr'
            await db.Users.filter(id=user.id).update(location=user.location, position=user.position, battleStatus=0)
            await nav_city(call, user)
        return
    elif result.name == 'Кофе':
        result.active = 0
        user.zamoroz -= 25
        if user.zamoroz < 0:
            user.zamoroz = 0
        user.energy = user.energy + 70
        if user.energy > 100:
            user.energy = 100
        text = "Ты выпил ☕️Кофе. Удалось немного согреться и восстановить бодрость."
        await db.Users.filter(id=user.id).update(zamoroz=user.zamoroz, energy=user.energy)
    elif result.name == 'Бамбук для курения':
        result.active = 0
        user.energy = user.energy + 60
        user.nowhp = user.nowhp - int(user.hp / 3)
        if user.nowhp <= 0:
            text = "Ты решил присесть на земле и спокойной покурить, мечтая о вечном. К сожалению, после третьей затяжки вы начали задыхаться. Надпись ''Курение убивает'' оказалась не тупой шуткой Кефира."
            user.money = int(user.money / 2)
            await db.Users.filter(id=user.id).update(energy=100, nowhp=user.hp, location='Хэвенбург', position='Номер в отеле', money=user.money)
        else:
            text = "Ты решил присесть на земле и спокойно покурить, помечтав о вечном..."
            await db.Users.filter(id=user.id).update(energy=user.energy, nowhp=user.nowhp)
    elif result.name == 'ГероИн':
        if effectUsers and user.id in effectUsers and effectUsers[user.id] != None:
            await bot.edit_message_text("Пока что тебе хватит..", call.message.chat.id, call.message.message_id)
            return
        result.active = 0
        await result.save()
        if user.booster >= time.time(): user.booster += 600
        else: user.booster = time.time() + 600
        await db.Users.filter(id=user.id).update(booster=user.booster)
        text = "Применив легендарную пыль героев ''ГероИн'', Ты почувствовал как наплывает эйфория."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        effects = ['hp', 'atk', 'minushp']
        effect = random.choice(effects)
        usr = await db.Users.get(id=user.id)
        if effect == 'hp':
            usr.nowhp += 100
            await db.Users.filter(id=user.id).update(nowhp=usr.nowhp)
        elif effect == 'atk':
            buffs = [10, 20, 30, 40]
            plusAtk = random.choice(buffs)
            _timeEnd = int(time.time() + 600)
            newBuff = await db.Buffs(owner=usr.id, type='atk', num=plusAtk, status=1, timeEnd=_timeEnd)
            await newBuff.save()
            _buzyUsers[call.from_user.id] = 'free'
            effectUsers[usr.id] = None
        elif effect == 'minushp':
            usr.nowhp -= 50
            await db.Users.filter(id=user.id).update(nowhp=usr.nowhp)
        await db.commitInventory(user, result)
        return
    elif result.name == 'Настойка боярышника':
        result.active = 0
        await result.save()
        text = "Ты выпил настойку. Ноги подкашиваются..."
        usr = await db.Users.get(id=user.id)
        await db.Users.filter(id=user.id).update(progStatus=0)
        boyaraUsers[user.user_id] = 1
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        effectUsers[usr.id] = "boyara"
        _buzyUsers[call.from_user.id] = 'free'
        await asyncio.sleep(300)
        effectUsers[usr.id] = None
        user = await db.Users.get(id=usr.id)
        user.progStatus = 1
        user.battleStatus = 0
        boyaraUsers[user.user_id] = 0
        locations = ['Город', 'Пустыня', 'Случайный лес', 'Заснеженный лес', 'Песчаная пирамида', 'Лесная гробница', 'Окус Локус', 'Радар', 'Океанус', 'Пустыня', 'Случайный лес', 'Заснеженный лес', 'Песчаная пирамида', 'Лесная гробница', 'Окус Локус', 'Радар', 'Океанус']
        randomProgLoc = random.randint(0, 30)
        newLoc = random.choice(locations)
        user.progLoc = "{}|{}".format(newLoc, randomProgLoc)
        await db.Users.filter(id=user.id).update(progStatus=1, battleStatus=0, progLoc=user.progLoc, location=newLoc)
        await bot.send_message(user.user_id, "Тебя, наконец, отпустило от настойки. Оглянувшись, Ты оказался в {}".format(newLoc))
        await db.commitInventory(user, result)
        return
    elif result.name == 'Паучий афродизиак':
        result.active = 0
        await result.save()
        text = "Ты использовал 🕸Паучий афродизиак. Пришло время показать какой ты boss of the gym."
        user.psy = -10 # ОБЯЗАТЕЛЬНО ПЕРЕДЕЛАТЬ ПОД ЧТО-ТО ДРУГОЕ В БУДУЩЕМ
        await db.Users.filter(id=user.id).update(psy=user.psy)
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        effectUsers[user.id] = "paukiBlyat"
        await asyncio.sleep(1200)
        await db.Users.filter(id=user.id).update(psy=100)
        effectUsers[user.id] = None
        await bot.send_message(user.user_id, "Действие паучьего афродизиака кончилось.")
        await db.commitInventory(user, result)
        return
    elif result.name == 'Бакин':
        result.active = 0
        await result.save()
        text = "Ты использовал 💊Бакин. Ну что я могу сказать? Пора становиться злым гением и ловить тех кто сзади.."
        await db.Users.filter(id=user.id).update(progStatus=2)
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif result.name == 'Дрова':
        result.active = 0
        user.zamoroz = 0
        user.progStatus = 1
        await db.Users.filter(id=user.id).update(zamoroz=0, progStatus=1)
        await result.save()
        text = "Костёр помог тебе немного отмёрзнуть..."
    elif result.name == 'Полотенце':
        result.active = 0
        user.humidity = 0
        user.progStatus = 1
        await db.Users.filter(id=user.id).update(humidity=0, progStatus=1)
        await result.save()
        text = "Вытершись о полотенце тебе стало немного легче идти..."
    elif result.type == 'Зелье':
        if user.battleStatus == 2:
            text = "Ты не можешь пить зелье во время боя!"
        else:
            if result.name == 'Чешуйчатое снадобье':
                result.active = 0
                user.nowhp += 40
                await db.Users.filter(id=user.id).update(nowhp=user.nowhp)
                text = "Ты успешно использовал 🧫{}".format(result.name)
            elif result.name == 'Малое зелье восстановления':
                result.active = 0
                plusHp = user.hp * 0.35
                if user.nowhp + plusHp > user.hp: newHp = user.hp
                else: newHp = user.nowhp + plusHp
                await db.Users.filter(id=user.id).update(nowhp=newHp)
                text = "Ты выпил 🧪Малое зелье восстановления\n❤️{}/{}".format(int(newHp), user.hp)
            elif result.name == 'Среднее зелье восстановления':
                result.active = 0
                plusHp = user.hp * 0.5
                if user.nowhp + plusHp > user.hp: newHp = user.hp
                else: newHp = user.nowhp + plusHp
                await db.Users.filter(id=user.id).update(nowhp=newHp)
                text = "Ты выпил 🧪Среднее зелье восстановления\n❤️{}/{}".format(int(newHp), user.hp)
            elif result.name == 'Зелье восстановления':
                result.active = 0
                user.nowhp = user.hp
                text = "Ты выпил 🧪Зелье восстановления"
                await db.Users.filter(id=user.id).update(nowhp=user.hp)
            elif result.name == 'Зелье сопротивления холоду':
                timeEnd = int(time.time()) + 900
                newBuff = await db.Buffs(owner=result.idplayer, type='antiZamoroz', num=20, status=1, timeEnd=timeEnd)
                await newBuff.save()
                result.active = 0
                await result.save()
                text = "Ты выпил 🧪Зелье сопротивления холоду. Следить за статусом эффекта можно в /profile"
            elif result.name == 'Зелье сопротивления холоду':
                timeEnd = int(time.time()) + 900
                newBuff = await db.Buffs(owner=result.idplayer, type='antiHumidity', num=20, status=1, timeEnd=timeEnd)
                await newBuff.save()
                result.active = 0
                await result.save()
                text = "Ты выпил 🧪Зелье сопротивления влажности. Следить за статусом эффекта можно в /profile"
            elif result.name == 'Зелье цепной молнии':
                timeEnd = int(time.time()) + 600
                newBuff = await db.Buffs(owner=result.idplayer, type='electro', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()
                result.active = 0
                await result.save()
                text = "Ты выпил 🧪Зелье цепной молнии. Следить за статусом эффекта можно в /profile"
            else:
                result.active = 0
                user.nowhp = user.nowhp + result.bonus
                if user.nowhp > user.hp:
                    user.nowhp = user.hp
                await db.Users.filter(id=user.id).update(nowhp=user.nowhp)
                text = "Ты успешно использовал {}\n❤️{}/{}".format(result.name, int(user.nowhp), user.hp)
    elif result.type == 'Сундук':
        text = await case(result, user)
    elif result.type == 'Броня':
        user = await db.Users.get(user_id=call.from_user.id).first()
        text = await armoruse(call, use, result, user)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await db.cachedInventory(user, result)
        return
    elif result.name == 'Противогаз':
        user = await db.Users.get(user_id=call.from_user.id).first()
        text = await armoruse(call, use, result, user)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await db.cachedInventory(user, result)
        return
    elif result.type == 'Рыбалка':
        user = await db.Users.get(user_id=call.from_user.id).first()
        text = await armoruse(call, use, result, user)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await db.cachedInventory(user, result)
        return
    elif result.type == 'Оружие':
        user = await db.Users.get(user_id=call.from_user.id).first()
        text = await armoruse(call, use, result, user)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await db.cachedInventory(user, result)
        return
    elif result.type == 'Артефакт':
        user = await db.Users.get(user_id=call.from_user.id)
        text, result = await userart(call, use, result, user)
        await db.cachedInventory(user, result)

    elif result.name == 'Билет на тот свет':
        user = await db.Users.get(user_id=call.from_user.id)
        _newLoc = user.progLoc.split("|")
        newLoc = _newLoc[0]
        blackListLocs = ["База клана", "Исследование Радара", "Свалка SR2", "Испытание оружия"]
        if newLoc not in blackListLocs or not newLoc.startswith("Окрестности"):
            await db.Users.filter(id=user.id).update(location=newLoc, progStatus=1, battleStatus=0)
            result.active = 0
            await result.save()
            text = "Проколов и без того обколотый билетик, Ты потерял сознание. Очнувшись, осмотрелся и узнал местность. Это {}".format(newLoc)
        else:
            text = "Как бы ты не колол этот проклятый билетик, ничего так и не произошло. После того как ты исколол свои пальцы, ты убрал билет обратно"
    elif result.name == 'Улучшенный рюкзак':
        user = await db.Users.get(user_id=call.from_user.id)
        user.inventorySizeMax += 5
        await db.Users.filter(id=user.id).update(inventorySizeMax=user.inventorySizeMax)
        result.active = 0
        await result.save()
        text = "Ты использовал улучшенный рюкзак"
    elif result.name == 'ВиАгро':
        if result.active == 1:
            text = "Ты выпил таблетку 💊ВиАгро. Скорее всего, через минут 10 Ты почувствуешь так называемый ''движ в штанах'', но не волнуйся - это прямое указание организма ходить на рейд."
            await bot.send_message(call.message.chat.id, text)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            result.active = 3
            await result.save()
            await db.commitInventory(user, result)
            _buzyUsers[call.from_user.id] = 'free'
            await asyncio.sleep(600)
            result.active = 4
            await result.save()
            await bot.send_message(call.message.chat.id, "Наконец, ты почувствовал странное ощущение от таблетки. Теперь твоя волшебная палочка нацелена в сторону башни", reply_markup=markup, parse_mode='markdown')
            return
        else:
            text = "Ошибка"
    elif result.name == 'Коробка с карточками':
        if result.active == 1:
            item = await legendaryCase(user, result)
            text = "Вы открыли коробку..."
        else:
            text = "Недоступно."
    elif result.type == 'Рецепт':
        result.active = 0
        text = "Ты переписал надпись на бумажке с рецептом на котелок. Теперь эта грязная бумажка тебе не понадобится."
    elif result.name == 'Карта заброшенного архива':
        if result.active == 1:
            text = "Выглядит из рук вон плохо - сразу видно, что дед рисовал на скорую руку и особо не заморачивался..."
            photo = open('/home/kakushigoto/megu/media/mapArchive.png', 'rb')
            await bot.send_photo(call.message.chat.id, photo, caption=text)
    elif result.name == "Хлопушка":
        if result.active == 1 and user.location not in ["Хэвенбург", "Кавайня", "Метро", "Океанус", "Город", "Радар"]:
            result.active=0
            await result.save()
            await bot.edit_message_text("Взрываем хлопушку!", call.message.chat.id, call.message.message_id)
            currentPosition = int(user.progLoc.split("|")[1])
            minPos = currentPosition - 5
            maxPos = currentPosition + 5
            allPos = []
            for i in range(minPos, maxPos): allPos.append("{}|{}".format(user.progLoc.split("|")[0], i))
            allUsers = await db.Users.filter(progLoc__in=allPos, location=user.progLoc.split("|")[0])
            for usr in allUsers:
                timeEnd = int(time.time()) + 600
                await db.Buffs.create(owner=usr.id, type='hlopushka', num=0, status=1, timeEnd=timeEnd)
                try:
                    await bot.send_message(usr.user_id, "Кто-то недалеко взорвал хлопушку. Тебя оглушило!")
                except:
                    pass
            await db.commitInventory(user, result)
            return
        else:
            if user.location in ["Хэвенбург", "Кавайня", "Метро", "Океанус", "Город", "Радар"]:
                text = "Хлопушку можно использовать вне города."
            else:
                text = "Ошибка"
    elif result.name == 'Бустер':
        if result.active == 1:
            result.active = 0
            boostTime = result.lvl * 60 * 60
            if user.booster >= time.time(): await db.Users.filter(id=user.id).update(booster=F('booster') + boostTime)
            else: await db.Users.filter(id=user.id).update(booster=time.time() + boostTime)
            text = "⚡️Бустер успешно использован."
        else:
            text = "Кажется, он просрочен..."
    else:
        text = "Недоступно"
    await db.commitInventory(user, result)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Инвентарь', callback_data="inv"))
    await result.save()
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')




async def invClose(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    text = "Ты закрыл инвентарь. Ты так редко это делаешь..."
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


#################
# ARMOR & ARTS  #
#################
async def userart(call, use, res, user):
    if res.idplayer != user.id:
        text = "Произошла ошибочка"
        return text
    if res.name == 'Кусок паззла':
        if res.active == 1:
            res.active = 0
            user.atk += 10
            user.hp += 10
            await db.Users.filter(id=user.id).update(atk=user.atk, hp=user.hp)
            await res.save()
            text = "Не зная что делать с этим кусочком паззла, ты случайно сломал его. Внезапно, ты почувствовал лёгкость и головокружение, а вокруг паззла появилось странное свечение, которое разгоралось всё ярче и ярче. Когда свет пропал, паззла ты не обнаружил.\n+10🔪 + 10❤️"
        else:
            text = "Кусок паззла. Он сломан. Вряд ли с ним что-нибудь получится"
    elif res.name == 'Волшебные кости':
        text = "Ты просто... Бросил кости на пол, глядя на комбинацию. Но ничего не случилось. Пришлось их подобрать... Наверное, нужно их оставить до лучшего момента."
    elif res.name == 'Амулет здоровья':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Амулет здоровья', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother:
            text = "У тебя уже есть артефакт, который используется"
        else:
            text = "Ты надел 🔶Амулет здоровья"
            res.active = 2
            await res.save()
    elif res.name == 'Осколок энергии':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Осколок энергии', active=2)
        checkother2 = await db.Inventory.exists(idplayer=user.id, name='Камень энергии', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother or checkother2:
            text = "У тебя уже есть артефакт подобного типа, который используется"
        else:
            text = "Ты надел 🔷Осколок энергии"
            res.active = 2
            await res.save()
    elif res.name == 'Камень энергии':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Осколок энергии', active=2)
        checkother2 = await db.Inventory.exists(idplayer=user.id, name='Камень энергии', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother or checkother2:
            text = "У тебя уже есть артефакт подобного типа, который используется"
        else:
            text = "Ты надел 🔷Камень энергии"
            res.active = 2
            await res.save()
    elif res.name == 'Горшок лепрекона':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Горшок лепрекона', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother:
            text = "У тебя уже есть артефакт подобного типа, который используется"
        else:
            text = "Ты надел 🍯Горшок лепрекона"
            res.active = 2
            await res.save()
    elif res.name == 'Карманная дриада':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Карманная дриада', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother:
            text = "У тебя уже есть артефакт подобного типа, который используется"
        else:
            text = "Ты надел 🌿Карманная дриада"
            res.active = 2
            await res.save()
    elif res.name == 'Осколок огня':
        checkother3 = await db.Inventory.exists(idplayer=user.id, name='Осколок огня', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
        if checkother3:
            text = "У тебя уже есть артефакт, который используется"
        else:
            text = "Ты надел 🔥Осколок огня"
            res.active = 2
            await res.save()
    elif res.name == 'Плащ-невидимка':
        checkother = await db.Inventory.exists(idplayer=user.id, name='Плащ-невидимка', active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты успешно снял {}".format(res.name)
            return text, res
        if checkother:
            text = "У тебя уже есть артефакт, который используется"
        else:
            await bot.edit_message_text("Надеваем плащ, это займёт до минуты...", call.message.chat.id, call.message.message_id)
            await asyncio.sleep(60)
            text = "Ты надел Плащ-невидимку"
            res.active = 2
            await res.save()
    else:
        checkother = await db.Inventory.exists(idplayer=user.id, name=res.name, active=2)
        if res.active == 2:
            res.active = 1
            await res.save()
            text = "Ты снял {}".format(res.name)
        else:
            if checkother:
                text = "У тебя уже есть этот артефакт"
            else:
                if res.active == 1:
                    res.active = 2
                    await res.save()
                    text = "Ты надел {}".format(res.name)

    return text, res


async def armorpers(call, user):
    re = await db.Inventory.filter(idplayer=user.id, active=2)
    text = 'Снаряжение, что ты носишь:'
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for z in re:
        if z.type == 'Броня':
            name, bonus, size, atk_block, expires = await db.items(z.name, check=True)
            if atk_block and atk_block > 0:
                text += "\n{} | +{}🛡 (⚔️ {}%)".format(name, z.bonus, atk_block)
            else:
                text += "\n{} | +{}🛡".format(name, z.bonus)
        elif z.type == 'Артефакт':
            name, bonus, size, atk_block, expires = await db.items(z.name, check=True)
            text += "\n{} ({}🔆)".format(name, z.lvl)
        elif z.type == 'Оружие':
            name, bonus, size, atk_block, expires = await db.items(z.name, check=True)
            text += "\n{} ({}🔆)".format(name, z.lvl)
        elif z.name == 'Противогаз':
            name, bonus, size, atk_block, expires = await db.items(z.name, check=True)
            allFilters = await db.Inventory.filter(name='Фильтры', bonus__gt=0, idplayer=user.id).only('bonus')
            filters = 0
            for x in allFilters: filters += x.bonus
            text += "\n🤿Противогаз: {}/100 (🕳{})".format(z.bonus, filters)
        elif z.type == 'Рыбалка':
            name, bonus, size, atk_block, expires = await db.items(z.name, check=True)
            text += "\n{} ({}🔆)".format(name, z.lvl)
        markup.add(InlineKeyboardButton('Снять {}'.format(name), callback_data="invUsing_{}".format(z.id)))
    markup.add(InlineKeyboardButton('В инвентарь', callback_data="invClose"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def armoruse(call, use, result, user):
    head = ['head', 'Хоккейная маска', 'Кожаный шлем', 'Шляпа фокусника', 'Кепка адидас', 'Шлем из фольги', 'Колпак главврача', 'Колючая маска', 'Шапка-ушанка', 'Горная шапка', 'Очки', 'Шлем усиленный', 'Шлем']
    body = ['body', 'Кожаный нагрудник', 'Бронежилет', 'Комбинезон сталкера', 'Ночнушка Раскуловой', 'Майка из пакета', 'Халат главрача', 'Багровый жилет', 'АШуба', 'Жилет скалолаза', 'Купальник Раскуловой', 'Плащ-уящ', 'Костюм химзащиты']
    foot = ['foot', 'Кожаные штаны', 'Спортивки адидас', 'Нижнее бельё Раскуловой', 'Штаны Ашодас', 'Модные штаны', 'Штаны главврача', 'Багровые поножи', 'Летние шорты', 'Короткие шорты', 'Плавки', 'Чулки', 'Шортики', 'Шортики 2.0']
    shoes = ['shoes', 'Берцы', 'Кожаные ботинки', 'Кросы адидас', 'Туфельки Раскуловой', 'НЕкроссовки', 'Тапочки главврача', 'Ботинки с шипами', 'Зимние калоши', 'Горные кроссовки', 'Дырявая лодка', 'Сталкерские ботинки', 'Противорадиационные ботинки']
    armor = ['armor', 'Крышка от мусорника', 'Покрышка со свалки', 'Деревянный щит', 'Щит охранника', 'Щит покорителя Шаи-Хулуда', 'Железный щит', 'Щит бомжа', 'Золотая покрышка', 'Щит верности Раскуловой', 'Щит-крыло', 'Яйца Ренанва', 'Самонагревающаяся покрышка']
    weapon = ['weapon', 'Пистолет с ножом', 'Копьё', 'Катана', 'Меч', 'Кинжал вампира', 'Кольт', 'Золотой кольт']
    art = ['art', 'Сувенир с моря', 'Квинтэссенция камня', 'Камень-металлолом', 'Палка ярости']
    other =  ['other', 'Противогаз']
    fishing = ['fishing', 'Простая удочка', 'Непростая удочка', 'Очень непростая удочка', 'Весьма непростая удочка']

    if result.name in head:
        armor_type = head[0]
    elif result.name in body:
        armor_type = body[0]
    elif result.name in foot:
        armor_type = foot[0]
    elif result.name in shoes:
        armor_type = shoes[0]
    elif result.name in armor:
        armor_type = armor[0]
    elif result.name in weapon:
        armor_type = weapon[0]
    elif result.name in other:
        armor_type = other[0]
    elif result.name in fishing:
        armor_type = fishing[0]
    if result.idplayer != user.id:
        text = "Произошла какая-то ошибочка."
        return text
    if result.active == 1:
        weared = await db.Inventory.filter(~Q(id=result.id), idplayer=result.idplayer, active=2, type__in=['Броня', 'Оружие', 'Экипировка', 'Рыбалка'])
        for item in weared:
            if item.name in head:
                old_armor_type = head[0]
            elif item.name in body:
                old_armor_type = body[0]
            elif item.name in foot:
                old_armor_type = foot[0]
            elif item.name in shoes:
                old_armor_type = shoes[0]
            elif item.name in armor:
                old_armor_type = armor[0]
            elif item.name in weapon:
                old_armor_type = weapon[0]
            elif item.name in other:
                old_armor_type = other[0]
            elif item.name in fishing:
                old_armor_type = fishing[0]
            if old_armor_type == armor_type:
                if armor_type != 'weapon' and armor_type != 'other' and armor_type != 'fishing':
                    await db.Users.filter(id=user.id).update(armor=F('armor') - item.bonus)
                    await db.Users.filter(id=user.id).update(armor=F('armor') + result.bonus) 
                elif armor_type == 'art':
                    checkItem = await db.Inventory.exists(name=user.item, active=2, idplayer=user.id)
                    if not user.item or not checkItem:
                        text = "К сожалению, использовать артефакт без оружия не выйдет"
                        return text
                elif armor_type == 'weapon':
                    await db.Users.filter(id=user.id).update(item=result.name)
                await db.Inventory.filter(id=item.id).update(active=1)
                await db.Inventory.filter(id=result.id).update(active=2)
                text = f"Ты успешно надел {result.name} вместо {item.name}."
                return text
        result.active = 2

        if armor_type == 'weapon':
            await db.Users.filter(id=user.id).update(item=result.name)
        elif armor_type == 'other' or armor_type == 'fishing' or armor_type == 'art': pass
        else:
            await db.Users.filter(id=user.id).update(armor=F('armor') + result.bonus)
        await result.save()
        text = f"Ты успешно надел снаряжение."
    else:
        inventorySize = await db.getInventorySize(user)
        if result.size + inventorySize > user.inventorySizeMax:
            text = "Единственное куда ты можешь деть снаряжение - в зубы, но оно достаточно большое для этого"
        else:
            if result.type == 'Броня':
                result.active = 1
                user.armor = user.armor - result.bonus
                await result.save()
                await db.Users.filter(id=user.id).update(armor=F('armor') - result.bonus)
                text = "Ты успешно снял снаряжение."
            else:
                result.active = 1
                await result.save()

                text = "Перемещено в инвентарь."
    await db.cachedInventory(user, result)
    return text



#############################
#         BLACKLIST         #
#############################
async def itemsBlackList(m, user):
    if m.chat.id == m.from_user.id:
        text = "Чёрный список предметов помогает не подбирать предметы, находящиеся в нём. Для добавления предмета достаточно ввести команду /blacklistAdd Название предмета.\nСписок предметов в чёрном списке:\n\n"
        allItemsInBlackList = await db.BlacklistItems.filter(idplayer=user.id)
        if allItemsInBlackList:
            for item in allItemsInBlackList:
                text += "\n{} - /blacklistDelete_{}".format(item.name, item.id)
        else:
            text += "Чёрный список пуст."
        await bot.send_message(m.chat.id, text)

@dp.message_handler(lambda m:m.text and m.text.startswith('/blacklistDelete_'))
async def blDL_(m):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.replace('/blacklistDelete_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            checkItemInBlackList = await db.BlacklistItems.get_or_none(id=result)
            if checkItemInBlackList and checkItemInBlackList.idplayer == user.id:
                await bot.send_message(m.chat.id, "Из чёрного списка был убран предмет {}".format(checkItemInBlackList.name))
                await checkItemInBlackList.delete()

@dp.message_handler(lambda m:m.text and m.text.startswith('/blacklistAdd'))
async def blAdd(m):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.replace('/blacklistAdd ', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            check = await db.items(result, check='check')
            if check == True:
                checkAnotherItemInBlackList = await db.BlacklistItems.exists(idplayer=user.id, name=result)
                if checkAnotherItemInBlackList:
                    await bot.send_message(m.chat.id, "У тебя уже есть такой предмет в чёрном списке")
                else:
                    newItemToBlackList = await db.BlacklistItems(idplayer=user.id, name=result)
                    await newItemToBlackList.save()
                    await bot.send_message(m.chat.id, "Ты успешно добавил {} в чёрный список предметов".format(result))
            else:
                await bot.send_message(m.chat.id, "Такого предмета не существует")






async def koltGrav_(call, user):
    item = call.data.split("_")[1]
    checkItem = await db.Inventory.get_or_none(name="Золотой кольт", idplayer=user.id, active=1, id=item).first()
    if checkItem:
        await bot.edit_message_text("Введите текст для гравировки.", call.message.chat.id, call.message.message_id)
        await GetQuantity.koltGrav.set()
    else:
        return await bot.edit_message_text("Золотой кольт должен находиться в инвентаре", call.message.chat.id, call.message.message_id)


@dp.message_handler(state=GetQuantity.koltGrav)
async def koltGrav(message: types.Message, state=FSMContext):
    user = await db.Users.get_or_none(user_id=message.from_user.id).first()
    if user:
        checkItem = await db.Inventory.get_or_none(name="Золотой кольт", idplayer=user.id, active=1).first()
        if len(message.text) <= 200:
            checkItem.descr = message.text
            await checkItem.save()
            await bot.send_message(message.chat.id, "Готово!")
        else:
            await bot.send_message(message.chat.id, "Длина текста не должна превышать 200 символов")
    await state.finish()



################################
#    REFERAL O4KA I DONATE     #
################################

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
        # Выбор текста для подписи над результатами
    switch_text = "Пригласить друга в игру" \
        if len(query.query) == 0 \
        else "Не найдено ссылок по данному запросу. Добавить »»"
    ref_text = """
<i><b>Большое разнообразие локаций, бесчисленное количество монстров,  еженедельные клановые события и многое другое уже ждёт тебя в 
Tower of Heaven !</b></i>

🎁 <a href="http://t.me/TowerOfHeaven_bot?start={}">Присоединяйся</a>, и начинай свой путь с приятным стартовым бонусом  = )
    """
    results = []
    test = types.InlineQueryResultArticle(id='1', title="Пригласить друга в игру.",description="Кидает рекламный текст, с вашей реф.ссылкой",input_message_content=types.InputTextMessageContent(message_text=ref_text.format(query.from_user.id), parse_mode='HTML', disable_web_page_preview=True))
    results.append(test)

    await bot.answer_inline_query(query.id, results, cache_time=1)



async def refs(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return


    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('Поделиться ссылкой', url="tg://share?url=@TowerOfHeaven_bot&nbsp;&nbsp;ref"))
    result = await db.Users.filter(ref=m.from_user.id)
    count = 0
    textc = ""
    for dict1 in result:
        count += 1
        donatesum = int(dict1.donatesum * 0.1)
        textc += "{} - {}lvl. Доход: {}💎\n".format(dict1.username, dict1.lvl, donatesum)
    if count != 0:
        text = "Реферальная система:\nПри приглашении пользователя по специальной ссылке вы будете получать 💰 за каждый поднятый рефералом уровень по формуле [уровень * 5] + единоразовый бонус за регистрацию в виде 1000🍗.\nПри донате приглашенного вами пользователя вы получаете 10%💎 от суммы доната.\nВаша специальная ссылка для приглашения:\nhttps://t.me/TowerOfHeaven_bot?start={}\nСписок ваших рефералов и дохода с них:\n{}".format(str(m.from_user.id), textc)
        if len(text) > 4096:
            for x in range(0, len(text), 4096):
                await bot.send_message(m.chat.id, text[x:x+4096])
        else:
            await bot.send_message(m.chat.id, text)
    else:
        text = "Реферальная система:\nПри приглашении пользователя по специальной ссылке вы будете получать 💰 за каждый поднятый рефералом уровень по формуле [уровень * 5] + единоразовый бонус за регистрацию в виде 1000🍗.\nПри донате приглашенного вами пользователя вы получаете 10%💎 от суммы доната.\nВаша специальная ссылка для приглашения:\n<code>https://t.me/TowerOfHeaven_bot?start={}</code>\nУ вас нет рефералов в данный момент.".format(str(m.from_user.id))
        await m.answer(text, reply_markup=markup, parse_mode='html')




async def mypartn(m, user):
    if m.chat.id == m.from_user.id:
        re = await db.Users.get(user_id=m.from_user.id).first()
        if re.partner == 0: return await m.answer("Вы можете зарабатывать 30% от донатов ваших рефералов. Партнёрская программа может быть подключена любому пользователю который имеет рекламную площадку. Выводы на банковскую карту/донаты в другие игры/YooMoney\n\nДля подключения партнёрской программы и/или уточнения деталей обращайтесь в /report")
        result = await db.Users.filter(ref=m.from_user.id)
        count = 0
        zarabotok = 0
        textc = ""
        for dict in result:
            count += 1
            if re.partner == 1:
                zarabotok += int(dict.donatesumPartn * 0.3)
            elif re.partner == 2:
                zarabotok += int(dict.donatesumPartn * 0.5)
        text = "Ваша специальная ссылка для приглашения:\n`https://t.me/TowerOfHeaven_bot?start={}`\nПриглашено - {} чел.\nВсего заработано: {}руб.".format(str(m.from_user.id), count, zarabotok)
        await m.answer(text, parse_mode='markdown')




###############
#     API     #
###############

async def settings(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        await m.answer("Доступные настройки:\n\n/blacklist - настройка чёрного списка предметов\n/inv_fa - настройка быстрого доступа в инвентаре\n/api_settings - настройка API (для пользовательских ботов)\n/notif_settings - настройка уведомлений")


async def inv_fa(m, user):
    if m.chat.id == m.from_user.id:
        text = f"\nСписок предметов быстрого доступа помогает использовать предметы, не перемещаясь по разделам инвентаря. Для добавления предмета достаточно ввести команду /fastAccessAdd Название предмета.\n\nСписок предметов в быстром доступе:\n\n"
        allItemsInFastAccess = await db.InventoryFastAccess.filter(idplayer=user.id)
        if allItemsInFastAccess:
            for item in allItemsInFastAccess:
                text += "\n{} - /fastAccessDelete_{}".format(item.name, item.id)
        else:
            text += "Список пуст."
        await bot.send_message(m.chat.id, text)

@dp.message_handler(lambda m:m.text and m.text.startswith('/fastAccessDelete_'))
async def fastAccessDelete_(m):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.replace('/fastAccessDelete_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            checkItemInFastAccess = await db.InventoryFastAccess.get_or_none(id=result)
            if checkItemInFastAccess and checkItemInFastAccess.idplayer == user.id:
                await bot.send_message(m.chat.id, "Из списка быстрого доступа был убран предмет {}".format(checkItemInFastAccess.name))
                await checkItemInFastAccess.delete()

@dp.message_handler(lambda m:m.text and m.text.startswith('/fastAccessAdd '))
async def fastAccessAdd(m):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        if user and user.ban != 1:
            result = m.text.replace('/fastAccessAdd ', '', 1).replace('@TowerOfHeaven_bot', '', 1)
            check = await db.items(result, check='check')
            if check == True:
                checkAnotherItemInFastAccess = await db.InventoryFastAccess.exists(idplayer=user.id, name=result)
                if checkAnotherItemInFastAccess:
                    await bot.send_message(m.chat.id, "У тебя уже есть такой предмет в списке")
                else:
                    newItemInFastAccess = await db.InventoryFastAccess(idplayer=user.id, name=result)
                    await newItemInFastAccess.save()
                    await bot.send_message(m.chat.id, "Ты успешно добавил {} в список быстрого доступа".format(result))
            else:
                await bot.send_message(m.chat.id, "Такого предмета не существует")



async def notif_settings(m, user):
    if m.chat.id == m.from_user.id:
        checkSettings = await db.Notifications.get_or_none(idplayer=user.id).first()
        if not checkSettings:
            checkSettings = await db.Notifications(idplayer=user.id)
            await checkSettings.save()
        if checkSettings.hotel == 1: hotel = "✅"
        else: hotel = "❌"

        if checkSettings.onsen == 1: onsen = "✅"
        else: onsen = "❌"
        
        if checkSettings.eat == 1: eat = "✅"
        else: eat = "❌"

        if checkSettings.energy == 1: energy = "✅"
        else: energy = "❌"

        if checkSettings.loc_effects == 1: loc_effects = "✅"
        else: loc_effects = "❌"

        if checkSettings.regs == 1: regs = "✅"
        else: regs = "❌"

        if checkSettings.buffs == 1: buffs = "✅"
        else: buffs = "❌" 

    text = """Настройки уведомлений:

({}) /nf_hotel - Отель
({}) /nf_onsen - Источники
({}) /nf_eat - Еда
({}) /nf_energy - Энергия
({}) /nf_locEffects - Эффекты локаций
({}) /nf_regs - Регистрация рефералов
({}) /nf_buffs - Конец действия баффа""".format(hotel, onsen, eat, energy, loc_effects, regs, buffs)
    await m.answer(text)

async def nf_(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/nf_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    user = await db.Users.get(user_id=m.from_user.id).first()
    if user:
        checkSettings = await db.Notifications.get_or_none(idplayer=user.id).first()
        if not checkSettings:
            checkSettings = await db.Notifications(idplayer=user.id)
            await checkSettings.save()
        if result == 'hotel':
            if checkSettings.hotel == 0: checkSettings.hotel = 1
            else: checkSettings.hotel = 0
        elif result == 'onsen':
            if checkSettings.onsen == 0: checkSettings.onsen = 1
            else: checkSettings.onsen = 0
        elif result == 'eat':
            if checkSettings.eat == 0: checkSettings.eat = 1
            else: checkSettings.eat = 0
        elif result == 'energy':
            if checkSettings.energy == 0: checkSettings.energy = 1
            else: checkSettings.energy = 0
        elif result == 'locEffects':
            if checkSettings.loc_effects == 0: checkSettings.loc_effects = 1
            else: checkSettings.loc_effects = 0
        elif result == 'regs':
            if checkSettings.regs == 0: checkSettings.regs = 1
            else: checkSettings.regs = 0
        elif result == 'buffs':
            if checkSettings.buffs == 0: checkSettings.buffs = 1
            else: checkSettings.buffs = 0
        else:
            await m.answer("Возникла ошибка")
        await checkSettings.save()
        await m.answer("Done!")

async def usrSetApi(m, user):
    if m.chat.id != m.from_user.id: return
    apiBotsGet = await db.Api.filter(idplayer=user.id)
    text = "Настройки API:"
    if apiBotsGet:
        for z in apiBotsGet:
            if z.botStatus == 1:
                text += "\n@{} - Доступ разрешён (/s_api_{})".format(z.bot, z.id)
            else:
                text += "\n@{} - Доступ закрыт (/s_api_{})".format(z.bot, z.id)
    else:
        text += "\nНет активных разрешений"
    await bot.send_message(m.chat.id, text)

async def s_api(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    result = m.text.replace('/s_api_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    apiSet = await db.Api.exists(id=result)
    if apiSet:
        apiSet = await db.Api.get(id=result).first()
    if apiSet and apiSet.idplayer == user.id:
        if apiSet.botStatus == 1:
            apiSet.botStatus = 0
            await apiSet.save()
            await bot.send_message(m.chat.id, "Вы отключили доступ по API для бота @{}".format(apiSet.bot))
        elif apiSet.botStatus == 0:
            apiSet.botStatus = 1
            await apiSet.save()
            await bot.send_message(m.chat.id, "Вы включили доступ по API для бота @{}".format(apiSet.bot))
    else:
        return


#############
#  ALCHEMY  #
#############
async def varenie(call, user=None): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    if antiflood and call.from_user.id in antiflood and antiflood[call.from_user.id] == 'buzy':
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Кажется, ты уже варишь что-то... Если это не так, попробуй снова через 60 секунд.")
        await asyncio.sleep(60)
        antiflood[call.from_user.id] = None
        return
    antiflood[call.from_user.id] = 'buzy'
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    do = call.data.split('_')
    use = do[1]


    ostanki = await db.Inventory.filter(name='Останки героев', idplayer=user.id).count()
    oduvanchiki = user.oduvanchik
    rca = user.rca
    sakura = user.sakura
    roza = user.roza

    if oduvanchiki >= 2 and rca >= 1: passSredne = 1
    else: passSredne = 0
    if oduvanchiki >= 1 and roza >= 1 and rca >= 1: passBig =1
    else: passBig = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт бамбук', active=0)
    if oduvanchiki >= 4 and roza >= 2 and rca >= 2 and sakura >= 1 and checkRecipy: passBamboo = 1
    else: passBamboo = 0
    recipy = await db.Inventory.exists(name='Рецепт героИн', idplayer=user.id, active=0)
    if ostanki >= 10 and recipy: passGeroin = 1
    else: passGeroin = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт боярышник', active=0)
    if oduvanchiki >= 6 and roza >= 3 and rca >= 2 and sakura >= 4 and ostanki >= 2 and checkRecipy: passBoyara = 1
    else: passBoyara = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт ВиАгро', active=0)
    if oduvanchiki >= 35 and roza >= 20 and checkRecipy: passViagra = 1
    else: passViagra = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт паучий афродизиак', active=0)
    if oduvanchiki >= 10 and roza >= 10 and rca >= 10 and sakura >= 10 and ostanki >= 5 and checkRecipy: passPaukiblyat = 1
    else: passPaukiblyat = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт приготовления малого зелья восстановления', active=0)
    if oduvanchiki >= 5 and roza >= 3 and rca >= 3 and ostanki >= 1 and checkRecipy: passRestoreSmall = 1
    else: passRestoreSmall = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт приготовления среднего зелья восстановления', active=0)
    if oduvanchiki >= 8 and roza >= 5 and rca >= 5 and ostanki >= 2 and checkRecipy: passRestoreMedium = 1
    else: passRestoreMedium = 0
    if sakura >= 10 and roza >= 8 and rca >= 8 and ostanki >= 3: passRestore = 1
    else: passRestore = 0
    checkRecipy = await db.Inventory.exists(idplayer=user.id, name='Рецепт бакин', active=0)
    if oduvanchiki >= 3 and roza >= 7 and rca >= 2 and sakura >= 7 and checkRecipy: passBakin = 1
    else: passBakin = 0 



    if use == 'restore':
        if passRestore == 1:

            await call.message.answer('Сколько таких сварить? Если ты передумал, введи "отмена"')
            await GetQuantity.restore.set()
            return
        else:
            text = "У тебя не хватает ингредиентов."

    elif use == 'restoreSmall':
        if passRestoreSmall == 1:
            await call.message.answer('Сколько таких сварить? Если ты передумал, введи "отмена"')
            await GetQuantity.restoreSmall.set()
            return
        else:
            text = "У тебя не хватает ингредиентов."
    
    elif use == 'restoreMedium':
        if passRestoreSmall == 1:
            await call.message.answer('Сколько таких сварить? Если ты передумал, введи "отмена"')
            await GetQuantity.restoreMedium.set()
            return
        else:
            text = "У тебя не хватает ингредиентов."

    elif use == 'sredne':
        if passSredne == 1:
            await db.Users.filter(id=user.id).update(rca = F('rca') - 1, oduvanchik = F('oduvanchik') - 2)
            await db.addItem('Среднее зелье здоровья', user)
            text = "Ты успешно сварил 🧪Среднее зелье здоровья"
        else:
            text = "У тебя не хватает ингредиентов"

    elif use == 'big':
        if passBig == 1:
            await db.Users.filter(id=user.id).update(roza = F('roza') - 1, rca = F('rca') - 1, oduvanchik = F('oduvanchik') - 1)
            await db.addItem('Большое зелье здоровья', user)
            text = "Ты успешно сварил 🧪Большое зелье здоровья"
        else:
            text = "У тебя не хватает ингредиентов"

    elif use == 'bamboo':
        if passBamboo == 1:
            await db.Users.filter(id=user.id).update(sakura = F('sakura') - 1,
                                                    roza = F('roza') - 2,
                                                    rca = F('rca') - 2,
                                                    oduvanchik = F('oduvanchik') - 4)
            await db.addItem('Бамбук для курения', user)
            text = "Ты успешно приготовил 🚬Бамбук для курения"
        else:
            text = "У тебя не хватает ингредиентов."

    elif use == 'geroin':
        if passGeroin == 1:

            bones = await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(10).delete()
            await db.addItem('ГероИн', user)
            text = 'Ты успешно приготовил ГероИн'
        else:
            text = 'У тебя не хватает ингредиентов'

    elif use == 'boyara':
        if passBoyara == 1:
            await db.Users.filter(id=user.id).update(oduvanchik = F('oduvanchik') - 6, roza = F('roza') - 3, rca = F('rca') - 2, sakura = F('sakura') - 4)
            await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(2).delete()

            await db.addItem('Настойка боярышника', user)
            text = "Ты успешно приготовил 🍶Настойку боярышника"
        else:
            text = "У тебя не хватает ингредиентов"

    elif use == 'viagra':
        if passViagra == 1:
            await db.Users.filter(id=user.id).update(roza = F('roza') - 20, oduvanchik = F('oduvanchik') - 35)
            await db.addItem('ВиАгро', user)
            text = "Ты успешно приготовил 💊ВиАгро"
        else:
            text = "У тебя не хватает ингредиентов"

    elif use == 'bakin':
        if passBakin == 1:
            await db.Users.filter(id=user.id).update(oduvanchik = F('oduvanchik') - 3, roza = F('roza') - 2, rca = F('rca') - 7, sakura=F('sakura') - 7)
            await db.addItem('Бакин', user)
            text = "Ты успешно приготовил 💊Бакин"
        else:
            text = "У тебя не хватает ингредиентов"

    elif use == 'ilovestas':
        if passPaukiblyat == 1:
            await db.Users.filter(id=user.id).update(sakura = F('sakura') - 10,
                                                    roza = F('roza') - 10,
                                                    rca = F('rca') - 10,
                                                    oduvanchik = F('oduvanchik') - 10)
            await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(5).delete()
            await db.addItem('Паучий афродизиак', user)
            text = "Ты успешно приготовил 🕸Паучий афродизиак"
        else:
            text = "У тебя не хватает ингредиентов"
    antiflood[call.from_user.id] = 'free'
    # await user.save()
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('В инвентарь', callback_data="inv"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)



@dp.message_handler(state=GetQuantity.restore)
async def create_restore(message: types.Message, state=FSMContext):
    antiflood[message.from_user.id] = 'buzy'

    user = await db.Users.get(user_id=message.from_user.id)

    if message.text.lower() == 'отмена':
        await message.answer('Ок. не буду пока варить.')
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer('Введи число (положительное).')
        return

    if int(message.text) >= 50:
        await message.answer('Я устану столько варить... давай не больше 50, хотя бы. ')
        await state.finish()
        return

    if int(message.text) == 0:
        await message.answer('Вроде хотел сварить что-то, а вроде уже и не хочу...')
        await state.finish()
        return

    await message.answer('Начинаю варить...')

    requirements = {'sakura': 10, 'roza': 8, 'rca': 8, 'bones': 3}

    quantity = int(message.text)

    user_have_bones = await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).count()
    user_have_flowers = {'sakura': user.sakura, 'roza': user.roza, 'rca': user.rca, 'bones': user_have_bones}

    for x in requirements:
        requirements[x] *= quantity


    bool_dict = {item:bool(user_have_flowers[item] >= requirements[item]) for item in requirements}
    # await message.answer(bool_dict)
    if False in bool_dict.values():
        await message.answer(f'У тебя не хватает ингридиентов для такого количества, попробуй сварить поменьше.\n\nДля варки введенного тобой количества необходимо х{requirements["rca"]}🌷 x{requirements["roza"]}🌹 x{requirements["sakura"]}🌸 x{requirements["bones"]}🦴')
        await state.finish()
        return

    cannot_create = 0
    for i in range(1, quantity+1):
        success = await db.addItem('Зелье восстановления', user)
        if success == False:
            cannot_create += 1
        else:
            await db.Users.filter(id=user.id).update(sakura = F('sakura') - 10, roza = F('roza') - 8, rca = F('rca') - 8)

            await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(3).delete()

    quantity -= cannot_create
    text = f"Ты успешно сварил x{quantity}🧪Зелье восстановления."

    antiflood[message.from_user.id] = 'free'
    await message.answer(text)
    await state.finish()

@dp.message_handler(state=GetQuantity.restoreSmall)
async def create_restore(message: types.Message, state=FSMContext):
    antiflood[message.from_user.id] = 'buzy'

    user = await db.Users.get(user_id=message.from_user.id)

    if message.text.lower() == 'отмена':
        await message.answer('Ок. не буду пока варить.')
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer('Введи число (положительное).')
        return

    if int(message.text) > 50:
        await message.answer('Я устану столько варить... давай не больше 50, хотя бы. ')
        await state.finish()
        return

    if int(message.text) == 0:
        await message.answer('Вроде хотел сварить что-то, а вроде уже и не хочу...')
        await state.finish()
        return

    await message.answer('Начинаю варить...')

    requirements = {'oduvanchiki': 5, 'roza': 3, 'rca': 3, 'bones': 1}

    quantity = int(message.text)

    user_have_bones = await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).count()
    user_have_flowers = {'oduvanchiki': user.oduvanchik, 'roza': user.roza, 'rca': user.rca, 'bones': user_have_bones}

    for x in requirements:
        requirements[x] *= quantity


    bool_dict = {item:bool(user_have_flowers[item] >= requirements[item]) for item in requirements}
    # await message.answer(bool_dict)
    if False in bool_dict.values():
        await message.answer(f'У тебя не хватает ингридиентов для такого количества, попробуй сварить поменьше.\n\nДля варки введенного тобой количества необходимо х{requirements["oduvanchiki"]}🌼 x{requirements["roza"]}🌹 x{requirements["rca"]}🌷 x{requirements["bones"]}🦴')
        await state.finish()
        return

    cannot_create = 0
    for i in range(1, quantity+1):
        success = await db.addItem('Малое зелье восстановления', user)
        if success == False:
            cannot_create += 1
        else:
            await db.Users.filter(id=user.id).update(oduvanchik = F('oduvanchik') - 5, roza = F('roza') - 3, rca = F('rca') - 3)

            await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(1).delete()

    quantity -= cannot_create
    text = f"Ты успешно сварил x{quantity}🧪Малое зелье восстановления."

    antiflood[message.from_user.id] = 'free'
    await message.answer(text)
    await state.finish()
@dp.message_handler(state=GetQuantity.restoreMedium)
async def create_restore(message: types.Message, state=FSMContext):
    antiflood[message.from_user.id] = 'buzy'

    user = await db.Users.get(user_id=message.from_user.id)

    if message.text.lower() == 'отмена':
        await message.answer('Вроде хотел сварить что-то, а вроде уже и не хочу...')
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer('Введи число (положительное).')
        return

    if int(message.text) > 50:
        await message.answer('Я устану столько варить... давай не больше 50, хотя бы. ')
        await state.finish()
        return

    if int(message.text) == 0:
        await message.answer('Вроде хотел сварить что-то, а вроде уже и не хочу...')
        await state.finish()
        return

    await message.answer('Начинаю варить...')

    requirements = {'oduvanchiki': 8, 'roza': 5, 'rca': 5, 'bones': 2}

    quantity = int(message.text)

    user_have_bones = await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).count()
    user_have_flowers = {'oduvanchiki': user.oduvanchik, 'roza': user.roza, 'rca': user.rca, 'bones': user_have_bones}

    for x in requirements:
        requirements[x] *= quantity


    bool_dict = {item:bool(user_have_flowers[item] >= requirements[item]) for item in requirements}
    if False in bool_dict.values():
        await message.answer(f'У тебя не хватает ингридиентов для такого количества, попробуй сварить поменьше.\n\nДля варки введенного тобой количества необходимо х{requirements["oduvanchiki"]}🌼 x{requirements["roza"]}🌹 x{requirements["rca"]}🌷 x{requirements["bones"]}🦴')
        await state.finish()
        return

    cannot_create = 0
    for i in range(1, quantity+1):
        success = await db.addItem('Среднее зелье восстановления', user)
        if success == False:
            cannot_create += 1
        else:
            await db.Users.filter(id=user.id).update(oduvanchik = F('oduvanchik') - 8, roza = F('roza') - 5, rca = F('rca') - 5)

            await db.Inventory.filter(name='Останки героев', active=1, idplayer=user.id).limit(2).delete()

    quantity -= cannot_create
    text = f"Ты успешно сварил x{quantity}🧪Среднее зелье восстановления."

    antiflood[message.from_user.id] = 'free'
    await message.answer(text)
    await state.finish()
