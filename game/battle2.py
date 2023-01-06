import time
import random
globalatk = {}
buzyusrs = {}
kdEnergy = {}
kdFire = {}
kdHeal = {}
kdRing = {}






async def giveMobSR(user):
    if user.progStatus == 2:

        checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
        if checkHlop:
            try:
                bot.send_message(user.user_id, "❤️❓ ⚡️{}/100 🍗{}/100\n🏭{}: К-{}\n\nВы отошли назад\nОсмотреться - /look_around".format(user.energy, user.eat, user.location, newnum))
            except:
                pass
        else:
            try:
                bot.send_message(user.user_id, "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭{}: К-{}\n\nВы отошли назад\nОсмотреться - /look_around".format(user.nowhp, user.hp, user.energy, user.eat, user.location, newnum))
            except:
                pass
    else:
        if user.location == 'Свалка SR':
            _random = random.randint(1, 100)
            nowProgLoc = user.progLoc
            _pl = nowProgLoc.split('|')
            num = _pl[1]
            newnum = int(num) + 1
            newProgLoc = "Свалка SR|{}".format(newnum)
            user.progLoc = newProgLoc
            if True:
                lastMob = 1758
                passed = 0
                while passed == 0:
                    randommob = random.randint(1, lastMob)
                    mob = await db.Monsters.get_or_none(id=randommob, battleStatus=0)
                    if mob:
                        passed = 1
                if mob:
                    checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
                    if checkHlop:
                        text = "❤️❓ ⚡️{}/100 🍗{}/100\n🏭Свалка SR: К-{}\n\nНа тебя вылез {}\nОсмотреться - /look_around".format(user.energy, user.eat, newnum, mob.name)
                    else:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Свалка SR: К-{}\n\nНа тебя вылез {}\nОсмотреться - /look_around".format(user.nowhp, user.hp, user.energy, user.eat, newnum, mob.name)
                    try:
                        await db.Users.filter(id=user.id).update(battleWith=mob.id, battleStatus=1, progLoc=user.progLoc)
                        await db.Monsters.filter(id=mob.id).update(battleStatus=1, battleWith=user.id)
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                        await bot.send_message(user.user_id, text, reply_markup=markup)
                    except:
                        pass
                else:
                    checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
                    if checkHlop:
                        text = "❤️❓ ⚡️{}/100 🍗{}/100\n🏭Свалка SR: К-{}\n\nОсмотреться вокруг /look_around".format(user.energy, user.eat, newnum)
                    else:                                    
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Свалка SR: К-{}\n\nОсмотреться вокруг /look_around".format(user.nowhp, user.hp, user.energy, user.eat, newnum)
                    await db.Users.filter(id=user.id).update(progStatus=0, progLoc=user.progLoc)
                    try:
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                        await bot.send_message(user.user_id, text, reply_markup=markup)
                    except:
                        pass
        elif user.location == 'Свалка SR2':
            _random = random.randint(1, 100)
            nowProgLoc = user.progLoc
            _pl = nowProgLoc.split('|')
            num = _pl[1]
            newnum = int(num) + 1
            newProgLoc = "Свалка SR2|{}".format(newnum)
            user.progLoc = newProgLoc
            if True:
                _lastMob = await db.Monsters.filter().order_by("-id").limit(1)
                lastMob = _lastMob[0].id
                passed = 0
                while passed == 0:
                    randommob = random.randint(1, lastMob)
                    mob = await db.Monsters.get_or_none(id=randommob, battleStatus=0)
                    if mob:
                        passed = 1
                if mob:
                    checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
                    if checkHlop:
                        text = "❤️❓ ⚡️{}/100 🍗{}/100\n🏭Свалка SR2: К-{}\n\nНа тебя вылез {}\nОсмотреться - /look_around".format(user.energy, user.eat, newnum, mob.name)
                    else:
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Свалка SR2: К-{}\n\nНа тебя вылез {}\nОсмотреться - /look_around".format(user.nowhp, user.hp, user.energy, user.eat, newnum, mob.name)
                    try:
                        await db.Users.filter(id=user.id).update(battleWith=mob.id, battleStatus=1, progLoc=user.progLoc)
                        await db.Monsters.filter(id=mob.id).update(battleStatus=1, battleWith=user.id)
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                        await bot.send_message(user.user_id, text, reply_markup=markup)
                    except:
                        pass
                else:
                    checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
                    if checkHlop:
                        text = "❤️❓ ⚡️{}/100 🍗{}/100\n🏭Свалка SR2: К-{}\n\nОсмотреться вокруг /look_around".format(user.energy, user.eat, newnum)
                    else:                                    
                        text = "❤️{}/{} ⚡️{}/100 🍗{}/100\n🏭Свалка SR2: К-{}\n\nОсмотреться вокруг /look_around".format(user.nowhp, user.hp, user.energy, user.eat, newnum)
                    await db.Users.filter(id=user.id).update(progStatus=0, progLoc=user.progLoc)
                    try:
                        markup = InlineKeyboardMarkup()
                        markup.row_width = 2
                        markup.add(InlineKeyboardButton('Идти дальше', callback_data="navgo"))
                        await bot.send_message(user.user_id, text, reply_markup=markup)
                    except:
                        pass



async def dropForBot(user, mob):
    needMobs = ['🚜Оптимус Прайм', '⚜️Мидас', '🛸Собакен-кракен', '🥛Депрессивный Кефир', ' 🎅Священный покоритель проституток', '🎅Священный покоритель проституток', '🐡Рыбус-минус', '🧢Электрик', '🌑Живая cumенная рыба']
    itemsToDrop = ['Чип ОС', 'Чип ОЗ', 'Чип ОП', 'Урон+', 'Крит+', 'Здоровье+', 'Уклонение+', 'Защита+', 'Утилизация+', 'Удача+']
    text = "\n"
    droid = await db.Bot.get_or_none(idplayer=user.id, status__in=[1, 2]).first()
    if not droid:
        droid = await db.Bot.get_or_none(idplayer=user.id, status=0).first()
        if not droid: return
    rand = random.randint(1, 100)
    if rand <= 20:
        if mob.name in needMobs:
            await db.Users.filter(id=user.id).update(details=F('details') + 1)
            text = "\n1🔧"
    rand = random.randint(1, 100)
    if rand == 0:
        if mob.name in needMobs:
            item = random.choice(itemsToDrop)
            await db.addItemBoot(item, user)
    return text

async def battleWin(result, location, text, er, call):
    gold, exp, sometext = await db.winner(result, location)
    text += "\nВы нанесли последний удар и монстр повалился на землю\n\nМонстр повержен\n\n Получено: 💰{} ✨{}\n{}".format(str(gold), str(exp), str(sometext))
    #plusText = await dropForBot(result, er)
    #text += plusText
    await db.Users.filter(id=result.id).update(battleStatus=0)
    await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
    if len(text) > 4096:
        l = len(text) + 1
        part_1 = text[0:l//2]
        part_2 = text[l//2:]

        await bot.send_message(call.message.chat.id, f'{part_1}')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, f'{part_2}')
    else:
        await bot.send_message(call.message.chat.id, text)
    loc = await db.Locations.get(name=result.location)
    progLoc = result.progLoc.split("|")
    kvadrat = progLoc[1]
    locShrines = loc.shrines.split(",")
    for z in locShrines:
        if z == kvadrat:
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Сделать подношение (150💰)', callback_data="shrineUse"))
            await bot.send_message(call.message.chat.id, "Недалеко от себя вы увидели ⛩Алтарь. Подойдя к нему, вы прочли надпись: \n''Пожертвуй 150💰 здешнему богу и получи его благословение''", reply_markup=markup)
    buzyusrs[call.from_user.id] = False
    await result.refresh_from_db()
    await scenario(result)
    await result.refresh_from_db()
    if result.location == "Свалка SR" or result.location == "Свалка SR2": await giveMobSR(result)
    return


async def calculate_armor(user):
    checkBuffArmor = await db.Buffs.get_or_none(type='armor', owner=user.id, status=1).first()
    if checkBuffArmor:
        armor = int((user.armor + checkBuffArmor.num) / 3) 
    else:
        armor = int(user.armor / 3)
    bonusArmor = await getDroidArmor(user)
    if bonusArmor > 0:
        newPlayerArmor = armor * (bonusArmor / 100 + 1)
        armor = int(newPlayerArmor)
    if result.frak != None and result.frak != "":
        frak = await db.Fraks.get(name=result.frak)
        frakArmor = frak.armor / 100
        armor += armor * frakArmor
    return armor

async def getEnergyAtk(user):
    if user.energy > 90: EnergyAtk = 1
    elif user.energy <= 90 and user.energy > 80: EnergyAtk = 0.97
    elif user.energy <= 80 and user.energy > 70: EnergyAtk = 0.9
    elif user.energy <= 70 and user.energy > 60: EnergyAtk = 0.83
    elif user.energy <= 60 and user.energy > 50: EnergyAtk = 0.75
    elif user.energy <= 50 and user.energy > 40: EnergyAtk = 0.66
    elif user.energy <= 40 and user.energy > 30: EnergyAtk = 0.57
    elif user.energy <= 30 and user.energy > 20: EnergyAtk = 0.48
    elif user.energy <= 20 and user.energy > 10: EnergyAtk = 0.35
    elif user.energy <= 10 and user.energy > 0: EnergyAtk = 0.29
    else: EnergyAtk = 0.2
    return EnergyAtk

async def getBattleAttack(result, er, EnergyAtk, call):
    bonusText = "\n"
    weapon = await db.Inventory.get_or_none(name=result.item, idplayer=result.id, active=2).first()
    _itemAtk = result.lvl / 100
    if result.frak != None and result.frak != "":
        frak = await db.Fraks.get(name=result.frak)
        frakAtk = frak.atk / 100
        frakCreet = frak.creet
    else:
        frakAtk = 0
        frakCreet = 0
    _playerAtk = 0
    if weapon:
        __playerAtk = int(result.atk * (weapon.bonus / 100))
        _playerAtk = __playerAtk + (result.atk * frakAtk)
        checkArts = await db.Inventory.get_or_none(name='Палка ярости', idplayer=result.id, active=2).first()
        if checkArts: 
            _playerAtk += int(result.atk * (checkArts.lvl / 100))
                
    checkBuffAtk = await db.Buffs.get_or_none(type='atk', owner=result.id, status=1).first()
    if checkBuffAtk:
        playerAtk = int(result.atk + (result.atk * (checkBuffAtk.num / 100) + (_playerAtk * EnergyAtk)))
    else:
        playerAtk = int(result.atk + _playerAtk * EnergyAtk)

    bonusAtk = await getDroidAtk(result)

    if not bonusAtk: bonusAtk = 0


    checkBuffCreet = await db.Buffs.get_or_none(type='creet', owner=result.id, status=1).first()
    if checkBuffCreet:
        rand = random.randint(1, 100)
        if rand <= checkBuffCreet.num:
            playerAtk *= 2
            
    bonusCreet = await getDroidCreet(result)
    rand = random.randint(1, 100)
    if rand <= bonusCreet:
        playerAtk *= 2
        droid = await db.Bot.get(idplayer=result.id, status__in=[1, 2]).first()
        await db.BotLogs.create(idbot=droid.id, text="Успешное срабатывание критического урона.")

    checkBuffElectro = await db.Buffs.get_or_none(type='electro', owner=result.id, status=1).first()
    if checkBuffElectro:
        rand = random.randint(1, 100)
        if rand <= checkBuffElectro.num:
            text = "\nНаконец, твое оружие выпустило мощный разряд электричества, от чего монстр повалился на землю..."
            await battleWin(result, result.location, text, er, call)
            playerAtk = "end"
            bonusAtk = 0
            plusPlayerAtk = 0
            return playerAtk, bonusAtk, plusPlayerAtk
    checkFireArt = await db.Inventory.get_or_none(name='Осколок огня', active=2, idplayer=result.id)
    if checkFireArt:
        if result.location == 'Заснеженный лес':
            plusBonus = 0.1 + checkFireArt.lvl / 100
            plusPlayerAtk = int(er.hp * plusBonus)
        else:
            plusBonus = 0.05 + checkFireArt.lvl / 100
            plusPlayerAtk = int(er.hp * plusBonus)
    else:
        plusPlayerAtk = 0
    if frakCreet > 0:
        if random.randint(1, 100) <= frakCreet:
            playerAtk *= 2
            bonusText += "Умение клана помогло тебе нанести критический урон!"
    return playerAtk, bonusAtk, plusPlayerAtk, bonusText


async def getBattleEventArmor(result, er, text, call, location):
    qwe = 0
    if result.id not in battleUserArmors or battleUserArmors[result.id] == None:
        checkarmor = []
        battleUserArmors[result.id] = []
        _checkarmor = await db.Inventory.filter(active=2, idplayer=result.id).only('name')
        for itm in _checkarmor:
            battleUserArmors[result.id].append(itm.name)
            checkarmor.append(itm.name)
    else:
        checkarmor = battleUserArmors[result.id]
    print(battleUserArmors)
    if checkarmor:
        r = random.randint(1, 100)
        for z in checkarmor:
            if z == 'Железный щит' and r <= 5:
                playerNewHp = int(result.nowhp)
                text += "\nВы отразили атаку монстра своим щитом"
                qwe = 1
            elif z == 'Щит бомжа' and r <= 10:
                playerNewHp = int(result.nowhp)
                text += "\nВы отразили атаку монстра своим щитом"
                qwe = 1
            elif z == 'Золотая покрышка' and r <= 15:
                playerNewHp = int(result.nowhp)
                text += "\nВы отразили атаку монстра своим щитом"
                qwe = 1
            elif z == 'Щит верности Раскуловой' and r <= 20:
                playerNewHp = int(result.nowhp)
                text += "\nВы отразили атаку монстра своим щитом"
                qwe = 1
            if qwe == 0:
                r = random.randint(1, 100)
                if z == 'Кольцо всеотражения':
                    ring = await db.Inventory.get_or_none(name='Кольцо всеотражения', idplayer=result.id, active=2).first()
                    if ring:
                        chance = 23 + int(ring.lvl * 2.5)
                        if "Щит верности Раскуловой" in checkarmor and chance >= 60: chance = 60
                        elif "Щит верности Раскуловой" not in checkarmor and chance >= 70: chance = 70
                        if r <= chance:
                            playerNewHp = int(result.nowhp)
                            damageMob = int(er.atk * 0.75)
                            text += "\nВ момент атаки монстра ваше 💍Кольцо всеотражения сработало и монстр получил {}💔".format(damageMob)
                            qwe = 1
                            er.nowhp -= (er.atk * 0.75)
                            if er.nowhp <= 0:
                                location = result.location
                                await battleWin(result, location, text, er, call)
                                qwe = 'False'
                                text = False
                                return qwe, text # False - битва окончена, остановить выполнение материнской функции
    return qwe, text

async def battleColdBuff(result, er):
    bonus = 0
    items = battleUserArmors[result.id]
    if "Шапка-ушанка" in items: bonus += 10
    if "АШуба" in items: bonus += 20
    if "Летние шорты" in items: bonus += 10
    if "Зимние калоши" in items: bonus += 15
    if "Самонагревающаяся покрышка" in items: bonus += 20
    check6 = await db.Buffs.get_or_none(type='antiZamoroz', owner=result.id, status=1)
    if check6: bonus += check6.num
    __plusZamoroz = int(er.atk / 20)
    plusZamoroz = int(__plusZamoroz - (__plusZamoroz * bonus / 100))
    await db.Users.filter(id=result.id).update(zamoroz = F('zamoroz') + plusZamoroz)
    await result.refresh_from_db(fields=['zamoroz'])
    return plusZamoroz

async def battleWaterBuff(result, er):
    bonus = 0
    items = battleUserArmors[result.id]
    if "Очки" in items: bonus += 10
    if "Купальник Раскуловой" in items: bonus += 25
    if "Плавки" in items: bonus += 15
    if "Дырявая лодка" in items: bonus += 25
    __plushumidity = er.atk / 20
    plusHumidity = int(__plushumidity - (__plushumidity * bonus / 100))
    await db.Users.filter(id=result.id).update(humidity = F('humidity') + plusHumidity)
    await result.refresh_from_db(fields=['humidity'])
    return plusHumidity


async def battleUseEnergy(call, user):
    if user.id in battleUserArmors:
        if "Осколок энергии" in battleUserArmors[user.id] or "Камень энергии" in battleUserArmors[user.id]:
            if user.id in kdEnergy and kdEnergy[user.id] < int(time.time()) or user.id not in kdEnergy:
                energyBonus = 50
                if energyBonus + user.energy >= 100: await db.Users.filter(id=user.id).update(energy=100)
                else: await db.Users.filter(id=user.id).update(energy=F('energy') + energyBonus)
                kdEnergy[user.id] = int(time.time()) + 900
                await user.refresh_from_db()
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы использовали артефакт энергии\n⚡️: {}".format(user.energy))
            else:
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Артефакт энергии еще не готов к использованию")
    else:
        battleUserArmors[user.id] = []
        _checkarmor = await db.Inventory.filter(active=2, idplayer=user.id)
        for itm in _checkarmor:
            battleUserArmors[user.id].append(itm.name)
        if "Осколок энергии" in battleUserArmors[user.id] or "Камень энергии" in battleUserArmors[user.id]:
            if user.id in kdEnergy and kdEnergy[user.id] < int(time.time()) or user.id not in kdEnergy:
                energyBonus = 50
                if energyBonus + user.energy >= 100: await db.Users.filter(id=user.id).update(energy=100)
                else: await db.Users.filter(id=user.id).update(energy=F('energy') + energyBonus)
                kdEnergy[user.id] = int(time.time()) + 900
                await user.refresh_from_db()
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы использовали артефакт энергии\n⚡️: {}".format(user.energy))
            else:
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Артефакт энергии еще не готов к использованию")

async def battleUseFire(call, user):
    if user.id in battleUserArmors:
        if "Осколок огня" in battleUserArmors[user.id]:
            if user.id in kdFire and kdFire[user.id] < int(time.time()) or user.id not in kdFire:
                er = await db.Monsters.get_or_none(id=user.battleWith).first()
                fireBonus = int(er.hp * 0.1)
                await db.Monsters.filter(id=user.battleWith).update(nowhp=F('nowhp') - fireBonus)
                kdFire[user.id] = int(time.time()) + 1200
                await user.refresh_from_db()
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы использовали артефакт огня\nМонстр получил урон {}🔥".format(fireBonus))
            else:
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Артефакт огня еще не готов к использованию")
    else:
        battleUserArmors[user.id] = []
        _checkarmor = await db.Inventory.filter(active=2, idplayer=user.id)
        for itm in _checkarmor:
            battleUserArmors[user.id].append(itm.name)
            if user.id in kdFire and kdFire[user.id] < int(time.time()) or user.id not in kdFire:
                er = await db.Monsters.get_or_none(id=user.battleWith).first()
                fireBonus = int(er.hp * 0.1)
                await db.Monsters.filter(id=user.battleWith).update(nowhp=F('nowhp') - fireBonus)
                kdFire[user.id] = int(time.time()) + 1200
                await user.refresh_from_db()
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы использовали артефакт огня\nМонстр получил урон {}🔥".format(fireBonus))
            else:
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Артефакт огня еще не готов к использованию")










async def battlestart(call, result): 
    btl = call.data.split('_')
    do = btl[1]
    text = str(call.message.text)
    if do == 'tpOff':
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="У вас нет возможности телепортироваться")
        return 
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Атакуем...") 
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    buzyusrs[call.from_user.id] = True
    er = await db.Monsters.exists(id=result.battleWith)
    if er:
        er = await db.Monsters.get(id=result.battleWith)
        if result.battleStatus == 1:
            pass
        else:
            print("error1")
            await bot.send_message(call.message.chat.id, "Битва с мобом окончена")
            buzyusrs[call.from_user.id] = False
            return
    else:
        print("error2")
        await bot.send_message(call.message.chat.id, "Битва с мобом окончена")
        await db.Users.filter(id=result.id).update(battleStatus=0)
        buzyusrs[call.from_user.id] = False
        return
    if do == 'tp':
        er = await db.Monsters.get(id=result.battleWith).first()
        q = result
        pIdName = "Свиток телепортации"
        o = await db.Inventory.exists(active=1, name=pIdName, idplayer=q.id)
        if o:
            pass
        else:
            res = result
            er = await db.Monsters.get(battleWith=res.id).first()
            playerNewHp = int(res.nowhp) - int(er.atk)
            await db.Users.filter(id=result.id).update(nowhp = F('nowhp') - int(er.atk))
            await result.refresh_from_db(fields=['nowhp'])
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if playerNewHp < 1:
                # money = int(res.money)
                loser = int(res.money * 0.5)
                remains_on_loc = int(loser * 0.3)
                checkgorod = await db.Inventory.get(idplayer=result.id, name='Большой город').first()
                if checkgorod:
                    # result.location = 'Хэвенбург'
                    await db.Users.filter(id=result.id).update(location='Хэвенбург')
                else:
                    # result.location = 'Город'
                    await db.Users.filter(id=result.id).update(location='Город')
                text += "Пытаясь вытащить 📜Свиток телепортации, враг всё же смог нанести тебе смертельный удар. За возрождение в городе снято {}💰".format(str(loser))
                await db.MoneyDropLoc.create(progLoc=result.progLoc, amount=remains_on_loc, username=result.username)
                # result.money = loser
                # result.battleStatus = 0
                # er.battleStatus = 0
                # er.nowhp = er.hp
                # result.nowhp = res.hp
                # result.energy = 100
                # result.eat = 100
                # result.progStatus = 1
                await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
                await db.Users.filter(id=result.id).update(money=loser,
                                                        battleStatus=0, energy=100,
                                                        nowhp = F('hp'), eat=100,
                                                        progStatus=1)
                await result.refresh_from_db()
                await er.refresh_from_db()
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
            else:
                text += "\nПытаясь вытащить 📜Свиток телепортации, враг всё же смог тебя зацепить, однако свитка ты не нашёл. Битва продолжается. \nУ вас осталось {}❤️\n----------".format(str(playerNewHp))
                # res.nowhp = playerNewHp
                # await res.save()
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                buzyusrs[call.from_user.id] = False
                return
        # result.battleStatus = 0
        await db.Users.filter(id=result.id).update(battleStatus=0)
        await result.refresh_from_db(fields=['battleStatus'])
        if result.quest == 'Искатель приключений' and result.questStatus == 1 and result.location != 'Песчаная пирамида':
            progSplit = result.progLoc.split("|")
            num = progSplit[1]
            quest_to_update = await db.tempQuest.filter(user_id=result.user_id, quest=result.quest, status=0).first()
            await db.tempQuest.filter(id=quest_to_update.id).update(progress = F('progress') + int(num))
        checkgorod = await db.Inventory.exists(idplayer=result.id, name='Большой город')
        if checkgorod:
            await db.Users.filter(id=result.id).update(location='Хэвенбург', position='Площадь')
        else:
            await db.Users.filter(id=result.id).update(location='Город', position='Площадь')
        # result.position = 'Площадь'
        ores = await db.Inventory.get(name=pIdName, active=1, idplayer=result.id).first()
        # await db.Inventory.filter(active=1, name=pIdName, idplayer=result.id).first().update(active=0)
        await db.Inventory.filter(id=ores.id).update(active=0)
        # await result.save()
        # await er.save()
        text += "\nВы успешно телепортировались в город."
        await bot.send_message(call.message.chat.id, text)
        buzyusrs[call.from_user.id] = False
    elif do == 'tpOff':
        return
    

    elif do == 'atk':
        droid = await db.Bot.get_or_none(idplayer=result.id, status__in=[1, 2]).first()
        if not droid: droid = await db.Bot.get_or_none(idplayer=result.id, status=0).first()
        result = await db.Users.get(user_id=call.from_user.id)
        location = result.location
        pName = result.username
        armor = await calculate_armor(result)
        
        er = await db.Monsters.get(id=result.battleWith).first()
        if result.location not in ['Свалка FL', 'Свалка HD', 'Свалка HR', 'Свалка SR', "Свалка SR2"]:
            if result.location != er.location:
                print("error3")
                await bot.send_message(call.message.chat.id, "Битва с мобом окончена")
                buzyusrs[call.from_user.id] = False
                return
        if (result.nowhp > 0) and (er.nowhp > 0):
            EnergyAtk = await getEnergyAtk(result)
            plusText = ""
            playerAtk, bonusAtk, plusPlayerAtk, bonusText = await getBattleAttack(result, er, EnergyAtk, call)
            if playerAtk == 'end': return
            if await db.Inventory.exists(name__in=["Кольт", "Золотой кольт"], idplayer=result.id, active=2):
                plusText += "\nРаскручиваем кольт...\n"
                if random.randint(1, 100) <= 90:
                    attack = playerAtk * 0.6
                    plusText += "Первый выстрел из кольта оказался успешным.\n"
                    if random.randint(1, 100) <= 65:
                        attack += playerAtk * 0.6
                        plusText += "Раскручивая барабан, делаешь второй выстрел и вновь попадаешь в цель.\n"
                        if random.randint(1, 100) <= 40:
                            attack += playerAtk * 0.6
                            plusText += "Почувствовав небольшую удачу, начинаешь пританцовывать, делая третий выстрел и вновь попадаешь!\n"
                            if random.randint(1, 100) <= 35:
                                attack += playerAtk * 0.6
                                plusText += "Удача точно на твоей стороне, четвертый выстрел прямо в цель! - уже прыгаешь вовсю как первобытный человек который впервые в жизни увидел огонь\n"
                                if random.randint(1, 100) <= 30:
                                    attack += playerAtk * 0.6
                                    plusText += "Я что сплю? Пятый выстрел! С такой удачей хоть в Осирис беги!\n"
                                    if random.randint(1, 100) <= 20:
                                        attack += playerAtk * 0.6
                                        plusText += "И последний выстрел тоже попал прямо в цель! Хорошая работа!\n"
                                    else:
                                        plusText += "А вот на последний выстрел ловкости не хватило - какая досада... Ну ничего, здесь и так очень сильно повезло!\n"
                                else:
                                    plusText += "Только ты подумал что спишь, так тут вместо выстрела послышался щелчок. Обидно\n"
                            else:
                                plusText += "На этом удача, видимо, кончилась, ведь послышался щелчок\n"
                        else:
                            plusText += "Почувствовав небольшую удачу, начинаешь пританцовывать, делая третий выстрел, но, увы и ах, на эот раз щелчок\n"
                    else:
                        plusText += "Раскручивая барабан, делаешь второй выстрел, но - удача точно от тебя отвернулась - послышался щелчок\n"
                else:
                    plusText += "Первый выстрел оказался разочарованием - очень сильно не повезло и по итогу... не судьба. Пришлось ударить монстра мизинцем\n"
                    attack = playerAtk * 0.3
                playerAtk = attack
            if bonusText: plusText += bonusText
            enemyNewHp = int(er.nowhp) - int(playerAtk)
            enemyNewHp -= int(plusPlayerAtk)

            if result.id in battleUserArmors and "Осколок льда" in battleUserArmors[result.id] and random.randint(1, 100) <= 20:
                newPlayerAtk = (playerAtk + plusPlayerAtk) * 0.75
                enemyNewHp = int(er.nowhp) - int(newPlayerAtk)
                qwe = 5
                text += "\nОсколок льда заморозил монстра."  
                playerNewHp = int(result.nowhp)
            else:
                qwe = 0

            await db.Monsters.filter(id=er.id).update(nowhp = enemyNewHp)
            await er.refresh_from_db(fields=['nowhp'])
            if result.location == 'Свалка HR':
                er.atk = int(er.atk * 1.35)
            # er.nowhp = enemyNewHp
            # await er.save()
            if enemyNewHp > 0:
                if qwe == 0:
                    qwe, _text = await getBattleEventArmor(result, er, text, call, location)
                    text = f"{_text}\n{plusText}"
                if qwe == 'False': return # Потому что битва уже закончилась
                elif qwe == 1: playerNewHp = int(result.nowhp)
                if qwe == 0:
                    checkBuffUv = await db.Buffs.get_or_none(owner=result.id, status=1, type='uv').first()
                    if checkBuffUv:
                        rand = random.randint(1, 100)
                        if rand <= checkBuffUv.num:
                            text += "\nТы смог увернуться от удара монстра"
                            qwe = 1
                            playerNewHp = int(result.nowhp)
                if qwe == 0:
                    bonusUv = await getDroidUv(result)
                    rand = random.randint(1, 100)
                    if rand <= bonusUv:
                        text += "\nБот помог тебе увернуться от атаки монстра"
                        await db.BotLogs.create(idbot=droid.id, text="Успешное срабатывание уворота.")
                        qwe = 1
                        playerNewHp = int(result.nowhp)

                if qwe == 0:
                    minAtk = int(er.atk * 0.9)
                    maxAtk = int(er.atk * 1.1)
                    mobAtk = random.randint(minAtk, maxAtk)
                    if mobAtk < armor:
                        armor = mobAtk - 1
                    elif mobAtk == armor:
                        armor = mobAtk - 1
                    if result.psy == -10:
                        playerNewHp = int(result.nowhp) + armor - int(mobAtk * 2)
                    else:
                        playerNewHp = int(result.nowhp) + armor - int(mobAtk)


                if result.location == 'Заснеженный лес':
                    plusZamoroz = await battleColdBuff(result, er)
                elif result.location == 'Окус Локус':
                    plusHumidity = await battleWaterBuff(result, er)
                elif result.location == 'Туннели метро':
                    await db.Inventory.filter(name='Противогаз', idplayer=result.id, active=2, bonus__gt=0).update(bonus=F('bonus') - 1)
                    checkDefender = await db.Inventory.get_or_none(name='Противогаз', idplayer=result.id, active=2).first()
                    if checkDefender and checkDefender.bonus <= 0:
                        text += "\nПротивогаз повреждён, нужна замена!"



                if droid:
                    checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
                    if droid.status == 1 and checkChip: passdroid = True
                    elif droid.status == 2 and checkChip: passdroid = True
                    else: passdroid = False
                    if passdroid:
                        droidAtk = result.lvl * 1.5
                        atkDroid = int(droidAtk + bonusAtk)
                        enemyNewHp = int(er.nowhp) - int(atkDroid)
                        await db.Monsters.filter(id=er.id).update(nowhp = enemyNewHp)
                        await er.refresh_from_db(fields=['nowhp'])
                        text += "\nБот нанёс {}🔪".format(atkDroid)
                        await db.BotLogs.create(idbot=droid.id, text="Бот нанёс {}🔪".format(atkDroid))
                if playerNewHp <= 0:
                    money = int(result.money)
                    if "Горшок лепрекона" in battleUserArmors[result.id]:
                        loser = money
                        text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: 0💰".format(str(loser))
                    else:
                        loser = int(money * 0.5)
                        remains_on_loc = int(loser * 0.3)
                        await db.MoneyDropLoc.create(progLoc=result.progLoc, amount=remains_on_loc, username=result.username)
                        text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                    checkgorod = await db.Inventory.exists(idplayer=result.id, name='Большой город')
                    if checkgorod:
                        await db.Users.filter(id=result.id).update(location='Хэвенбург')
                    else:
                        await db.Users.filter(id=result.id).update(location='Город')
                    await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
                    await db.Users.filter(id=result.id).update(money=loser,
                                                                battleStatus=0, nowhp = F('hp'),
                                                                eat=100, energy=100,
                                                                zamoroz=0, humidity=0,
                                                                progStatus=1)


                    await bot.send_message(call.message.chat.id, text)
                    buzyusrs[call.from_user.id] = False
                    return

                await db.Users.filter(id=result.id).update(nowhp=playerNewHp)
                await result.refresh_from_db(fields=['nowhp'])
                if not qwe:
                    qwe = 0
                checkHlop = await db.Buffs.get_or_none(owner=result.id, status=1, type='hlopushka').first()
                if checkHlop: playerNewHp = "❓"
                if plusPlayerAtk > 0 and qwe == 0:
                    if result.location == 'Заснеженный лес':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})(❄️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusZamoroz), str(playerNewHp))
                    elif result.location == 'Окус Локус':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})(☁️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusHumidity), str(playerNewHp))
                    elif result.location == 'Свалка HD':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor))
                    elif result.location == 'Свалка FL':
                        text += "\n{} ударил монстра {}(+{}🔥)💔\nМонстр ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(int(plusPlayerAtk)), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                    else:
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                elif plusPlayerAtk == 0 and qwe == 0:
                    if result.location == 'Заснеженный лес':
                       text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})(❄️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusZamoroz), str(playerNewHp))
                    elif result.location == 'Окус Локус':
                        text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})(☁️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusHumidity), str(playerNewHp))
                    elif result.location == 'Свалка HD':
                        text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor))
                    elif result.location == 'Свалка FL':
                        text += "\n{} ударил монстра {}💔\nМонстр ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                    else:
                        text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                elif plusPlayerAtk > 0 and qwe == 5:
                    if result.location == 'Заснеженный лес':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                    elif result.location == 'Окус Локус':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                    elif result.location == 'Свалка HD':
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name))
                    elif result.location == 'Свалка FL':
                        text += "\n{} ударил монстра {}(+{}🔥)💔\nМонстр оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(int(plusPlayerAtk)), str(playerNewHp))
                    else:
                        text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                elif plusPlayerAtk == 0 and qwe == 5:
                    if result.location == 'Заснеженный лес':
                       text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))
                    elif result.location == 'Окус Локус':
                        text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))
                    elif result.location == 'Свалка HD':
                        text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name))
                    elif result.location == 'Свалка FL':
                        text += "\n{} ударил монстра {}💔\nМонстр оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(playerNewHp))
                    else:
                        text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))

                else:
                    if result.location == 'Заснеженный лес':
                       text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                    elif result.location == 'Окус Локус':
                        text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                    elif result.location == 'Свалка HD':
                        text += "\n{} ударил {} {}💔\n\n----------".format(str(pName), str(er.name), str(int(playerAtk)))
                    elif result.location == 'Свалка FL':
                        text += "\n{} ударил монстра {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(playerNewHp))
                    else:
                        text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                randomSkill = random.randint(1, 100)
                if result.id in battleUserArmors and "Меч" in battleUserArmors[result.id]: #Начинается скрипт скиллов
                    if result.masterWeapon == 0 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Выпад 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 1 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Выпад 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 2 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Выпад 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 3 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Выпад 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 4 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Выпад 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 5 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Выпад 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 6 and result.energy >= 28: markup.add(InlineKeyboardButton('Особый навык: Выпад 28⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 7 and result.energy >= 26: markup.add(InlineKeyboardButton('Особый навык: Выпад 26⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 8 and result.energy >= 24: markup.add(InlineKeyboardButton('Особый навык: Выпад 24⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 9 and result.energy >= 22: markup.add(InlineKeyboardButton('Особый навык: Выпад 22⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.masterWeapon == 10 and result.energy >= 20: markup.add(InlineKeyboardButton('Особый навык: Выпад 20⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                elif result.id in battleUserArmors and "Пистолет с ножом" in battleUserArmors[result.id]:
                    if result.masterWeapon == 0 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Выстрел 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 1 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Выстрел 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 2 and result.energy >= 28: markup.add(InlineKeyboardButton('Особый навык: Выстрел 28⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 3 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Выстрел 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 4 and result.energy >= 26: markup.add(InlineKeyboardButton('Особый навык: Выстрел 26⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 5 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Выстрел 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 6 and result.energy >= 23: markup.add(InlineKeyboardButton('Особый навык: Выстрел 23⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 7 and result.energy >= 21: markup.add(InlineKeyboardButton('Особый навык: Выстрел 21⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 8 and result.energy >= 19: markup.add(InlineKeyboardButton('Особый навык: Выстрел 19⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 9 and result.energy >= 17: markup.add(InlineKeyboardButton('Особый навык: Выстрел 17⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.masterWeapon == 10 and result.energy >= 15: markup.add(InlineKeyboardButton('Особый навык: Выстрел 15⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                elif result.id in battleUserArmors and "Копьё" in battleUserArmors[result.id]:
                    if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 1 and result.energy >= 44: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 44⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 2 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 3 and result.energy >= 42: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 42⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 4 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 5 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 6 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 7 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 8 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 9 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.masterWeapon == 10 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                elif result.id in battleUserArmors and "Катана" in battleUserArmors[result.id]:
                    if result.masterWeapon == 0 and result.energy >= 50: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 50⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 1 and result.energy >= 48: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 48⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 2 and result.energy >= 46: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 46⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 3 and result.energy >= 44: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 44⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 4 and result.energy >= 42: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 42⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 5 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 6 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 7 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 8 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 9 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.masterWeapon == 10 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                elif result.id in battleUserArmors and "Кинжал вампира" in battleUserArmors[result.id]:
                    if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 1 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 2 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 3 and result.energy >= 39: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 39⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 4 and result.energy >= 37: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 37⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 5 and result.energy >= 35: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 35⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 6 and result.energy >= 33: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 33⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 7 and result.energy >= 31: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 31⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 8 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 9 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.masterWeapon == 10 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                elif result.id in battleUserArmors and "Кольт" in battleUserArmors[result.id] or result.id in battleUserArmors and "Золотой кольт" in battleUserArmors[result.id]:
                    if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 1 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 2 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 3 and result.energy >= 39: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 39⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 4 and result.energy >= 37: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 37⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 5 and result.energy >= 35: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 35⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 6 and result.energy >= 33: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 33⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 7 and result.energy >= 31: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 31⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 8 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 9 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    elif result.masterWeapon == 10 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                

                checkDroidWeaponReady, checkDroidWeaponIds = await getDroidWeapon(result) # Оружие бота
                if checkDroidWeaponReady:
                    for weapon in checkDroidWeaponReady:
                        if checkDroidWeaponReady[weapon] == True:
                            markup.add(InlineKeyboardButton('Бот: {}'.format(checkDroidWeaponIds[weapon]), callback_data="battle_botWeapon_{}".format(weapon)))
                        else:
                            markup.add(InlineKeyboardButton('Бот: {} (Недоступно)'.format(checkDroidWeaponIds[weapon]), callback_data="none"))
                
                if "Осколок энергии" in battleUserArmors[result.id] or "Камень энергии" in battleUserArmors[result.id]:
                    if result.id in kdEnergy and kdEnergy[result.id] < int(time.time()) or result.id not in kdEnergy:
                        energyBonus = 50
                        markup.add(InlineKeyboardButton('Экстренное использование 🔷 (+{}⚡️)'.format(energyBonus), callback_data="battleUseEnergy"))
                    else:
                        leftTime = int((kdEnergy[result.id] - int(time.time())) / 60)
                        markup.add(InlineKeyboardButton('🔷 (КД: {}мин)'.format(leftTime), callback_data="battleUseEnergy"))                    
                        pass
                if "Осколок огня" in battleUserArmors[result.id]:
                    if result.id in kdFire and kdFire[result.id] < int(time.time()) or result.id not in kdFire:
                        fireBonus = int(er.hp * 0.1)
                        markup.add(InlineKeyboardButton('Экстренное использование 🔥 (+{}🔪)'.format(fireBonus), callback_data="battleUseFire"))
                    else:
                        leftTime = int((kdFire[result.id] - int(time.time())) / 60)
                        markup.add(InlineKeyboardButton('🔥 (КД: {}мин)'.format(leftTime), callback_data="battleUseFire"))                    
                        pass
                pId = result.id
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
            else:
                await battleWin(result, location, text, er, call)
                return
        else:
            if (int(result.nowhp) <= 0):
                money = int(result.money)
                checkArt = await db.Inventory.exists(idplayer=result.id, name='Горшок лепрекона', active=2)
                if checkArt:
                    loser = money
                    text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: 0💰".format(str(loser))
                else:
                    loser = int(money * 0.5)
                    remains_on_loc = int(loser * 0.3)
                    await db.MoneyDropLoc.create(progLoc=result.progLoc, amount=remains_on_loc, username=result.username)
                    text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                checkgorod = await db.Inventory.exists(idplayer=result.id, name='Большой город')
                if checkgorod:
                    await db.Users.filter(id=result.id).update(location='Хэвенбург')
                else:
                    await db.Users.filter(id=result.id).update(location='Город')
                await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
                await db.Users.filter(id=result.id).update(money=loser,
                                                            battleStatus=0, nowhp = F('hp'),
                                                            eat=100, energy=100,
                                                            progStatus=1)
                await result.refresh_from_db()
                await er.refresh_from_db()
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}')
                else:
                    await bot.send_message(call.message.chat.id, text)
                buzyusrs[call.from_user.id] = False
            elif (int(er.nowhp) <= 0):
                await battleWin(result, location, text, er, call)
                return
    

    elif do == 'kazn':
        if result.masterWeapon == 0: needEnergy = 40
        elif result.masterWeapon == 1: needEnergy = 38
        elif result.masterWeapon == 2: needEnergy = 36
        elif result.masterWeapon == 3: needEnergy = 34
        elif result.masterWeapon == 4: needEnergy = 32
        elif result.masterWeapon == 5: needEnergy = 30
        elif result.masterWeapon == 6: needEnergy = 28
        elif result.masterWeapon == 7: needEnergy = 26
        elif result.masterWeapon == 8: needEnergy = 24
        elif result.masterWeapon == 9: needEnergy = 22
        elif result.masterWeapon == 10: needEnergy = 20

        if result.energy >= needEnergy:
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            location = result.location
            er = await db.Monsters.get(id=result.battleWith).first()
            fullHpMob = int(er.hp)
            needHpToSkill = int(fullHpMob * 0.3)
            rand = random.randint(1, 100)
            if rand <= 25:
                await weaponSkillUsed(result, success=True)
                needHpToSkill = int(fullHpMob * 0.5)
            else:
                await weaponSkillUsed(result)
            er.nowhp -= int(needHpToSkill)
            await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - int(needHpToSkill))
            await result.refresh_from_db(fields=['nowhp'])
            if (int(er.nowhp) <= 0):
                await battleWin(result, location, text, er, call)
                return
            else:
                # await er.save()
                text += "\nТы нанес {} урона выпадом.. Битва продолжается".format(str(needHpToSkill))
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]
                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
            await battleWin(result, location, text, er, call)
            return
        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if len(text) > 4096:
                l = len(text) + 1
                part_1 = text[0:l//2]
                part_2 = text[l//2:]

                await bot.send_message(call.message.chat.id, f'{part_1}')
                await asyncio.sleep(1)
                await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            buzyusrs[call.from_user.id] = False
    elif do == 'shoot':
        if result.masterWeapon == 0: needEnergy = 30
        elif result.masterWeapon == 1: needEnergy = 29
        elif result.masterWeapon == 2: needEnergy = 28
        elif result.masterWeapon == 3: needEnergy = 27
        elif result.masterWeapon == 4: needEnergy = 26
        elif result.masterWeapon == 5: needEnergy = 25
        elif result.masterWeapon == 6: needEnergy = 23
        elif result.masterWeapon == 7: needEnergy = 21
        elif result.masterWeapon == 8: needEnergy = 19
        elif result.masterWeapon == 9: needEnergy = 17
        elif result.masterWeapon == 10: needEnergy = 15
        
        if result.energy >= needEnergy:
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            location = result.location
            rand = random.randint(1, 100)
            if rand <= 15:
                shootAtk = int(result.atk * 1.75)
                await weaponSkillUsed(result, success=True)
            else:
                shootAtk = int(result.atk * 1.5)
                await weaponSkillUsed(result)
            er = await db.Monsters.get(id=result.battleWith).first()
            er.nowhp = er.nowhp - shootAtk
            await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - shootAtk)
            await er.refresh_from_db(fields=['nowhp'])
            if (int(er.nowhp) <= 0):
                await battleWin(result, location, text, er, call)
                return
            else:
                # await er.save()
                # await result.save()
                text += "\nТы нанес {} урона выстрелом. Битва продолжается".format(str(shootAtk))
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if len(text) > 4096:
                l = len(text) + 1
                part_1 = text[0:l//2]
                part_2 = text[l//2:]

                await bot.send_message(call.message.chat.id, f'{part_1}')
                await asyncio.sleep(1)
                await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            buzyusrs[call.from_user.id] = False

    elif do == 'oneshot':
        if result.masterWeapon == 0: needEnergy = 50
        elif result.masterWeapon == 1: needEnergy = 48
        elif result.masterWeapon == 2: needEnergy = 46
        elif result.masterWeapon == 3: needEnergy = 44
        elif result.masterWeapon == 4: needEnergy = 42
        elif result.masterWeapon == 5: needEnergy = 40
        elif result.masterWeapon == 6: needEnergy = 38
        elif result.masterWeapon == 7: needEnergy = 36
        elif result.masterWeapon == 8: needEnergy = 34
        elif result.masterWeapon == 9: needEnergy = 32
        elif result.masterWeapon == 10: needEnergy = 30

        if result.energy >= needEnergy:
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            location = result.location
            er = await db.Monsters.get(id=result.battleWith).first()
            kill = random.randint(1, 100)
            if kill <= 20:
                await weaponSkillUsed(result, success=True)
                await battleWin(result, location, text, er, call)
                return
            else:
                await weaponSkillUsed(result)
                # await result.save()
                text += "\nТы промахнулся"
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if len(text) > 4096:
                l = len(text) + 1
                part_1 = text[0:l//2]
                part_2 = text[l//2:]

                await bot.send_message(call.message.chat.id, f'{part_1}')
                await asyncio.sleep(1)
                await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif do == 'seriya':
        random1 = random.randint(1, 100)
        random2 = random.randint(1, 100)
        random3 = random.randint(1, 100)
        if result.masterWeapon == 0: needEnergy = 45
        elif result.masterWeapon == 1: needEnergy = 44
        elif result.masterWeapon == 2: needEnergy = 43
        elif result.masterWeapon == 3: needEnergy = 42
        elif result.masterWeapon == 4: needEnergy = 41
        elif result.masterWeapon == 5: needEnergy = 40
        elif result.masterWeapon == 6: needEnergy = 38
        elif result.masterWeapon == 7: needEnergy = 36
        elif result.masterWeapon == 8: needEnergy = 34
        elif result.masterWeapon == 9: needEnergy = 32
        elif result.masterWeapon == 10: needEnergy = 30

        if result.energy >= needEnergy:
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            er = await db.Monsters.get(id=result.battleWith).first()
            atk = int(result.atk)
            location = result.location
            newAtk = int(atk * 2)
            oldAtk = int(atk * 0.3)
            if random1 <= 30:
                # er.nowhp = er.nowhp - newAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - newAtk)
                text += "\nПервый удар: {} урона".format(str(newAtk))
                await weaponSkillUsed(result, success=True)
            else:
                # er.nowhp = er.nowhp - oldAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - oldAtk)
                text += "\nПервый удар: {} урона".format(str(oldAtk))
                await weaponSkillUsed(result)
            if random2 <= 30:
                # er.nowhp = er.nowhp - newAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - newAtk)
                text += "\nВторой удар: {} урона".format(str(newAtk))
                await weaponSkillUsed(result, success=True)
            else:
                # er.nowhp = er.nowhp - oldAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - oldAtk)
                text += "\nВторой удар: {} урона".format(str(oldAtk))
                await weaponSkillUsed(result)
            if random3 <= 30:
                # er.nowhp = er.nowhp - newAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - newAtk)
                text += "\nТретий удар: {} урона".format(str(newAtk))
                await weaponSkillUsed(result, success=True)
            else:
                # er.nowhp = er.nowhp - oldAtk
                await db.Monsters.filter(id=er.id).update(nowhp = F('nowhp') - oldAtk)
                text += "\nТретий удар: {} урона".format(str(oldAtk))
                await weaponSkillUsed(result)
            # await er.save()
            await er.refresh_from_db(fields=['nowhp'])
            if int(er.nowhp) > 0:
                text += "\nБитва продолжается"
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))

                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]

                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)                
                # await result.save()
                buzyusrs[call.from_user.id] = False
                return
            else:
                await battleWin(result, location, text, er, call)
                return
        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            buzyusrs[call.from_user.id] = False
    elif do == 'kinzhal':
        if result.masterWeapon == 0: needEnergy = 45
        elif result.masterWeapon == 1: needEnergy = 43
        elif result.masterWeapon == 2: needEnergy = 41
        elif result.masterWeapon == 3: needEnergy = 39
        elif result.masterWeapon == 4: needEnergy = 37
        elif result.masterWeapon == 5: needEnergy = 35
        elif result.masterWeapon == 6: needEnergy = 33
        elif result.masterWeapon == 7: needEnergy = 31
        elif result.masterWeapon == 8: needEnergy = 29
        elif result.masterWeapon == 9: needEnergy = 27
        elif result.masterWeapon == 10: needEnergy = 25

        if result.energy >= needEnergy:
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            location = result.location
            er = await db.Monsters.get(id=result.battleWith).first()
            await weaponSkillUsed(result)
            mobNewHp = er.nowhp - result.atk
            stilledHpMin = int(result.atk * 0.25)
            stilledHpMax = int(result.atk * 0.5)
            stilledHp = random.randint(stilledHpMin, stilledHpMax)
            newHpUser = result.nowhp + stilledHp
            if newHpUser > result.hp:
                text = "Метнув кинжал в монстра, нанёс ему {}💔. Благодаря вампиризму кинжала, ты восстановил своё здоровье до максимума.".format(result.atk)
                newHpUser = result.hp
            else:
                text = "Метнув кинжал в монстра, нанёс ему {}💔. Благодаря вампиризму кинжала, ты восстановил {}❤️".format(result.atk, stilledHp)
            await db.Users.filter(id=result.id).update(nowhp=newHpUser)
            if mobNewHp <= 0:
                await battleWin(result, location, text, er, call)
                buzyusrs[call.from_user.id] = False
                return
            else:
                await db.Monsters.filter(id=er.id).update(nowhp=mobNewHp)
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                if len(text) > 4096:
                    l = len(text) + 1
                    part_1 = text[0:l//2]
                    part_2 = text[l//2:]
                    await bot.send_message(call.message.chat.id, f'{part_1}')
                    await asyncio.sleep(1)
                    await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                    buzyusrs[call.from_user.id] = False
                    return
                else:
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)                

        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if len(text) > 4096:
                l = len(text) + 1
                part_1 = text[0:l//2]
                part_2 = text[l//2:]

                await bot.send_message(call.message.chat.id, f'{part_1}')
                await asyncio.sleep(1)
                await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif do == 'kolt':

        if result.masterWeapon == 0: needEnergy = 45
        elif result.masterWeapon == 1: needEnergy = 43
        elif result.masterWeapon == 2: needEnergy = 41
        elif result.masterWeapon == 3: needEnergy = 39
        elif result.masterWeapon == 4: needEnergy = 37
        elif result.masterWeapon == 5: needEnergy = 35
        elif result.masterWeapon == 6: needEnergy = 33
        elif result.masterWeapon == 7: needEnergy = 31
        elif result.masterWeapon == 8: needEnergy = 29
        elif result.masterWeapon == 9: needEnergy = 27
        elif result.masterWeapon == 10: needEnergy = 25

        if result.energy >= needEnergy:
            pName = result.username
            armor = await calculate_armor(result)
            er = await db.Monsters.get(id=result.battleWith).first()
            # result.energy -= needEnergy
            await db.Users.filter(id=result.id).update(energy= F('energy') - needEnergy)
            await result.refresh_from_db(fields=['energy'])
            EnergyAtk = await getEnergyAtk(result)
            plusText = ""
            playerAtk, bonusAtk, plusPlayerAtk, bonusText = await getBattleAttack(result, er, EnergyAtk, call)
            if playerAtk == 'end': return
            if await db.Inventory.exists(name__in=["Кольт", "Золотой кольт"], idplayer=result.id, active=2):
                plusText += "Раскручиваем кольт монеткой...\n"
                if random.randint(1, 100) <= 100:
                    attack = playerAtk * 0.6
                    plusText += "Первый выстрел из кольта оказался успешным.\n"
                    if random.randint(1, 100) <= 100:
                        attack += playerAtk * 0.6
                        plusText += "Раскручивая барабан, делаешь второй выстрел и вновь попадаешь в цель.\n"
                        if random.randint(1, 100) <= 60:
                            attack += playerAtk * 0.6
                            plusText += "Почувствовав небольшую удачу, начинаешь пританцовывать, делая третий выстрел и вновь попадаешь!\n"
                            if random.randint(1, 100) <= 45:
                                attack += playerAtk * 0.6
                                plusText += "Удача точно на твоей стороне, четвертый выстрел прямо в цель! - уже прыгаешь вовсю как первобытный человек который впервые в жизни увидел огонь\n"
                                if random.randint(1, 100) <= 40:
                                    attack += playerAtk * 0.6
                                    plusText += "Я что сплю? Пятый выстрел! С такой удачей хоть в Осирис беги!\n"
                                    if random.randint(1, 100) <= 30:
                                        attack += playerAtk * 5
                                        plusText += "И последний выстрел тоже попал прямо в цель! Хорошая работа! Критический урон сработал на славу\n"
                                    else:
                                        plusText += "А вот на последний выстрел ловкости не хватило - какая досада... Ну ничего, здесь и так очень сильно повезло!\n"
                                else:
                                    plusText += "Только ты подумал что спишь, так тут вместо выстрела послышался щелчок. Обидно\n"
                            else:
                                plusText += "На этом удача, видимо, кончилась, ведь послышался щелчок\n"
                        else:
                            plusText += "Почувствовав небольшую удачу, начинаешь пританцовывать, делая третий выстрел, но, увы и ах, на эот раз щелчок\n"
                    else:
                        plusText += "Раскручивая барабан, делаешь второй выстрел, но - удача точно от тебя отвернулась - послышался щелчок\n"
                else:
                    plusText += "Первый выстрел оказался разочарованием - очень сильно не повезло и по итогу... не судьба. Пришлось ударить монстра мизинцем\n"
                    attack = playerAtk * 0.3
                if bonusText: plusText += bonusText
                droid = await db.Bot.get_or_none(idplayer=result.id, status__in=[1, 2]).first()
                if not droid: droid = await db.Bot.get_or_none(idplayer=result.id, status=0).first()

                playerAtk = attack
                enemyNewHp = int(er.nowhp) - int(playerAtk)
                if result.id in battleUserArmors and "Осколок льда" in battleUserArmors[result.id] and random.randint(1, 100) <= 20:
                    newPlayerAtk = (playerAtk + plusPlayerAtk) * 0.75
                    enemyNewHp = int(er.nowhp) - int(newPlayerAtk)
                    qwe = 5
                    text += "\nОсколок льда заморозил монстра."  
                    playerNewHp = int(result.nowhp)
                else:
                    qwe = 0

                await db.Monsters.filter(id=er.id).update(nowhp = enemyNewHp)
                await er.refresh_from_db(fields=['nowhp'])
                if result.location == 'Свалка HR':
                    er.atk = int(er.atk * 1.35)
                # er.nowhp = enemyNewHp
                # await er.save()
                if enemyNewHp > 0:
                    if qwe == 0:
                        qwe, _text = await getBattleEventArmor(result, er, text, call, result.location)
                        text = f"{_text}\n{plusText}"
                    if qwe == 'False': return # Потому что битва уже закончилась
                    elif qwe == 1: playerNewHp = int(result.nowhp)
                    if qwe == 0:
                        checkBuffUv = await db.Buffs.get_or_none(owner=result.id, status=1, type='uv').first()
                        if checkBuffUv:
                            rand = random.randint(1, 100)
                            if rand <= checkBuffUv.num:
                                text += "\nТы смог увернуться от удара монстра"
                                qwe = 1
                                playerNewHp = int(result.nowhp)
                    if qwe == 0:
                        bonusUv = await getDroidUv(result)
                        rand = random.randint(1, 100)
                        if rand <= bonusUv:
                            text += "\nБот помог тебе увернуться от атаки монстра"
                            await db.BotLogs.create(idbot=droid.id, text="Успешное срабатывание уворота.")
                            qwe = 1
                            playerNewHp = int(result.nowhp)

                    if qwe == 0:
                        minAtk = int(er.atk * 0.9)
                        maxAtk = int(er.atk * 1.1)
                        mobAtk = random.randint(minAtk, maxAtk)
                        if mobAtk < armor:
                            armor = mobAtk - 1
                        elif mobAtk == armor:
                            armor = mobAtk - 1
                        if result.psy == -10:
                            playerNewHp = int(result.nowhp) + armor - int(mobAtk * 2)
                        else:
                            playerNewHp = int(result.nowhp) + armor - int(mobAtk)


                    if result.location == 'Заснеженный лес':
                        plusZamoroz = await battleColdBuff(result, er)
                    elif result.location == 'Окус Локус':
                        plusHumidity = await battleWaterBuff(result, er)
                    elif result.location == 'Туннели метро':
                        await db.Inventory.filter(name='Противогаз', idplayer=result.id, active=2, bonus__gt=0).update(bonus=F('bonus') - 1)
                        checkDefender = await db.Inventory.get_or_none(name='Противогаз', idplayer=result.id, active=2).first()
                        if checkDefender.bonus <= 0:
                            text += "\nПротивогаз повреждён, нужна замена!"



                    if droid:
                        checkChip = await db.BotInventory.exists(idbot=droid.id, active=2, name='Чип ОС')
                        if droid.status == 1 and checkChip: passdroid = True
                        elif droid.status == 2 and checkChip: passdroid = True
                        else: passdroid = False
                        if passdroid:
                            droidAtk = result.lvl * 1.5
                            atkDroid = int(droidAtk + bonusAtk)
                            enemyNewHp = int(er.nowhp) - int(atkDroid)
                            await db.Monsters.filter(id=er.id).update(nowhp = enemyNewHp)
                            await er.refresh_from_db(fields=['nowhp'])
                            text += "\nБот нанёс {}🔪".format(atkDroid)
                            await db.BotLogs.create(idbot=droid.id, text="Бот нанёс {}🔪".format(atkDroid))
                    if playerNewHp <= 0:
                        money = int(result.money)
                        if "Горшок лепрекона" in battleUserArmors[result.id]:
                            loser = money
                            text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: 0💰".format(str(loser))
                        else:
                            loser = int(money * 0.5)
                            remains_on_loc = int(loser * 0.3)
                            await db.MoneyDropLoc.create(progLoc=result.progLoc, amount=remains_on_loc, username=result.username)
                            text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                        checkgorod = await db.Inventory.exists(idplayer=result.id, name='Большой город')
                        if checkgorod:
                            await db.Users.filter(id=result.id).update(location='Хэвенбург')
                        else:
                            await db.Users.filter(id=result.id).update(location='Город')
                        await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
                        await db.Users.filter(id=result.id).update(money=loser,
                                                                    battleStatus=0, nowhp = F('hp'),
                                                                    eat=100, energy=100,
                                                                    zamoroz=0, humidity=0,
                                                                    progStatus=1)


                        await bot.send_message(call.message.chat.id, text)
                        buzyusrs[call.from_user.id] = False
                        return

                    await db.Users.filter(id=result.id).update(nowhp=playerNewHp)
                    await result.refresh_from_db(fields=['nowhp'])
                    if not qwe:
                        qwe = 0
                    checkHlop = await db.Buffs.get_or_none(owner=result.id, status=1, type='hlopushka').first()
                    if checkHlop: playerNewHp = "❓"
                    if plusPlayerAtk > 0 and qwe == 0:
                        if result.location == 'Заснеженный лес':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})(❄️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusZamoroz), str(playerNewHp))
                        elif result.location == 'Окус Локус':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})(☁️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusHumidity), str(playerNewHp))
                        elif result.location == 'Свалка HD':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor))
                        elif result.location == 'Свалка FL':
                            text += "\n{} ударил монстра {}(+{}🔥)💔\nМонстр ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(int(plusPlayerAtk)), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                        else:
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                    elif plusPlayerAtk == 0 and qwe == 0:
                        if result.location == 'Заснеженный лес':
                           text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})(❄️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusZamoroz), str(playerNewHp))
                        elif result.location == 'Окус Локус':
                            text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})(☁️{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(plusHumidity), str(playerNewHp))
                        elif result.location == 'Свалка HD':
                            text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor))
                        elif result.location == 'Свалка FL':
                            text += "\n{} ударил монстра {}💔\nМонстр ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                        else:
                            text += "\n{} ударил {} {}💔\n{} ударил {} {}💔(🛡{})\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(pName), str(mobAtk), str(armor), str(playerNewHp))
                    elif plusPlayerAtk > 0 and qwe == 5:
                        if result.location == 'Заснеженный лес':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                        elif result.location == 'Окус Локус':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                        elif result.location == 'Свалка HD':
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name))
                        elif result.location == 'Свалка FL':
                            text += "\n{} ударил монстра {}(+{}🔥)💔\nМонстр оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(int(plusPlayerAtk)), str(playerNewHp))
                        else:
                            text += "\n{} ударил {} {}(+{}🔥)💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(int(plusPlayerAtk)), str(er.name), str(playerNewHp))
                    elif plusPlayerAtk == 0 and qwe == 5:
                        if result.location == 'Заснеженный лес':
                           text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))
                        elif result.location == 'Окус Локус':
                            text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))
                        elif result.location == 'Свалка HD':
                            text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name))
                        elif result.location == 'Свалка FL':
                            text += "\n{} ударил монстра {}💔\nМонстр оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(playerNewHp))
                        else:
                            text += "\n{} ударил {} {}💔\n{} оказался заморожен осколком льда\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(er.name), str(playerNewHp))

                    else:
                        if result.location == 'Заснеженный лес':
                           text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                        elif result.location == 'Окус Локус':
                            text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                        elif result.location == 'Свалка HD':
                            text += "\n{} ударил {} {}💔\n\n----------".format(str(pName), str(er.name), str(int(playerAtk)))
                        elif result.location == 'Свалка FL':
                            text += "\n{} ударил монстра {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(int(playerAtk)), str(playerNewHp))
                        else:
                            text += "\n{} ударил {} {}💔\n\nУ вас осталось {}❤️\n----------".format(str(pName), str(er.name), str(int(playerAtk)), str(playerNewHp))
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                    randomSkill = random.randint(1, 100)
                    if result.id in battleUserArmors and "Меч" in battleUserArmors[result.id]: #Начинается скрипт скиллов
                        if result.masterWeapon == 0 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Выпад 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 1 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Выпад 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 2 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Выпад 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 3 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Выпад 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 4 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Выпад 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 5 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Выпад 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 6 and result.energy >= 28: markup.add(InlineKeyboardButton('Особый навык: Выпад 28⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 7 and result.energy >= 26: markup.add(InlineKeyboardButton('Особый навык: Выпад 26⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 8 and result.energy >= 24: markup.add(InlineKeyboardButton('Особый навык: Выпад 24⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 9 and result.energy >= 22: markup.add(InlineKeyboardButton('Особый навык: Выпад 22⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                        elif result.masterWeapon == 10 and result.energy >= 20: markup.add(InlineKeyboardButton('Особый навык: Выпад 20⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kazn"))
                    elif result.id in battleUserArmors and "Пистолет с ножом" in battleUserArmors[result.id]:
                        if result.masterWeapon == 0 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Выстрел 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 1 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Выстрел 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 2 and result.energy >= 28: markup.add(InlineKeyboardButton('Особый навык: Выстрел 28⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 3 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Выстрел 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 4 and result.energy >= 26: markup.add(InlineKeyboardButton('Особый навык: Выстрел 26⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 5 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Выстрел 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 6 and result.energy >= 23: markup.add(InlineKeyboardButton('Особый навык: Выстрел 23⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 7 and result.energy >= 21: markup.add(InlineKeyboardButton('Особый навык: Выстрел 21⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 8 and result.energy >= 19: markup.add(InlineKeyboardButton('Особый навык: Выстрел 19⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 9 and result.energy >= 17: markup.add(InlineKeyboardButton('Особый навык: Выстрел 17⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                        elif result.masterWeapon == 10 and result.energy >= 15: markup.add(InlineKeyboardButton('Особый навык: Выстрел 15⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_shoot"))
                    elif result.id in battleUserArmors and "Копьё" in battleUserArmors[result.id]:
                        if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 1 and result.energy >= 44: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 44⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 2 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 3 and result.energy >= 42: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 42⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 4 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 5 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 6 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 7 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 8 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 9 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                        elif result.masterWeapon == 10 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Серия ударов 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_seriya"))
                    elif result.id in battleUserArmors and "Катана" in battleUserArmors[result.id]:
                        if result.masterWeapon == 0 and result.energy >= 50: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 50⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 1 and result.energy >= 48: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 48⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 2 and result.energy >= 46: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 46⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 3 and result.energy >= 44: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 44⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 4 and result.energy >= 42: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 42⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 5 and result.energy >= 40: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 40⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 6 and result.energy >= 38: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 38⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 7 and result.energy >= 36: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 36⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 8 and result.energy >= 34: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 34⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 9 and result.energy >= 32: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 32⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                        elif result.masterWeapon == 10 and result.energy >= 30: markup.add(InlineKeyboardButton('Особый навык: Рубящий удар 30⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_oneshot"))
                    elif result.id in battleUserArmors and "Кинжал вампира" in battleUserArmors[result.id]:
                        if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 1 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 2 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 3 and result.energy >= 39: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 39⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 4 and result.energy >= 37: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 37⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 5 and result.energy >= 35: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 35⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 6 and result.energy >= 33: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 33⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 7 and result.energy >= 31: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 31⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 8 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 9 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                        elif result.masterWeapon == 10 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Кровожадное метание 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kinzhal"))
                    elif result.id in battleUserArmors and "Кольт" in battleUserArmors[result.id] or result.id in battleUserArmors and "Золотой кольт" in battleUserArmors[result.id]:
                        if result.masterWeapon == 0 and result.energy >= 45: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 45⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 1 and result.energy >= 43: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 43⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 2 and result.energy >= 41: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 41⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 3 and result.energy >= 39: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 39⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 4 and result.energy >= 37: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 37⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 5 and result.energy >= 35: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 35⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 6 and result.energy >= 33: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 33⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 7 and result.energy >= 31: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 31⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 8 and result.energy >= 29: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 29⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 9 and result.energy >= 27: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 27⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                        elif result.masterWeapon == 10 and result.energy >= 25: markup.add(InlineKeyboardButton('Особый навык: Счастливая монета 25⚡️ ({}⚡️)'.format(result.energy), callback_data="battle_kolt"))
                    

                    checkDroidWeaponReady, checkDroidWeaponIds = await getDroidWeapon(result) # Оружие бота
                    if checkDroidWeaponReady:
                        for weapon in checkDroidWeaponReady:
                            if checkDroidWeaponReady[weapon] == True:
                                markup.add(InlineKeyboardButton('Бот: {}'.format(checkDroidWeaponIds[weapon]), callback_data="battle_botWeapon_{}".format(weapon)))
                            else:
                                markup.add(InlineKeyboardButton('Бот: {} (Недоступно)'.format(checkDroidWeaponIds[weapon]), callback_data="none"))
                    
                    if "Осколок энергии" in battleUserArmors[result.id] or "Камень энергии" in battleUserArmors[result.id]:
                        if result.id in kdEnergy and kdEnergy[result.id] < int(time.time()) or result.id not in kdEnergy:
                            energyBonus = 50
                            markup.add(InlineKeyboardButton('Экстренное использование 🔷 (+{}⚡️)'.format(energyBonus), callback_data="battleUseEnergy"))
                        else:
                            leftTime = int((kdEnergy[result.id] - int(time.time())) / 60)
                            markup.add(InlineKeyboardButton('🔷 (КД: {}мин)'.format(leftTime), callback_data="battleUseEnergy"))                    
                            pass
                    if "Осколок огня" in battleUserArmors[result.id]:
                        if result.id in kdFire and kdFire[result.id] < int(time.time()) or result.id not in kdFire:
                            fireBonus = int(er.hp * 0.1)
                            markup.add(InlineKeyboardButton('Экстренное использование 🔥 (+{}🔪)'.format(fireBonus), callback_data="battleUseFire"))
                        else:
                            leftTime = int((kdFire[result.id] - int(time.time())) / 60)
                            markup.add(InlineKeyboardButton('🔥 (КД: {}мин)'.format(leftTime), callback_data="battleUseFire"))                    
                            pass
                    pId = result.id
                    if len(text) > 4096:
                        l = len(text) + 1
                        part_1 = text[0:l//2]
                        part_2 = text[l//2:]

                        await bot.send_message(call.message.chat.id, f'{part_1}')
                        await asyncio.sleep(1)
                        await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                        buzyusrs[call.from_user.id] = False
                        return
                    else:
                        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                        buzyusrs[call.from_user.id] = False
                        return
                else:
                    await battleWin(result, result.location, text, er, call)
                    return
            else:
                if (int(result.nowhp) <= 0):
                    money = int(result.money)
                    checkArt = await db.Inventory.exists(idplayer=result.id, name='Горшок лепрекона', active=2)
                    if checkArt:
                        loser = money
                        text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: 0💰".format(str(loser))
                    else:
                        loser = int(money * 0.5)
                        remains_on_loc = int(loser * 0.3)
                        await db.MoneyDropLoc.create(progLoc=result.progLoc, amount=remains_on_loc, username=result.username)
                        text += "\nСилы были неравны, но, к счастью некоторые монстры сражаются не только ради пищи, поэтому как только ты перестал развлекать своими движениями моба, тебя оставили в покое и позволили доползти до привала.\nПотеряно: {}💰".format(str(loser))
                    checkgorod = await db.Inventory.exists(idplayer=result.id, name='Большой город')
                    if checkgorod:
                        await db.Users.filter(id=result.id).update(location='Хэвенбург')
                    else:
                        await db.Users.filter(id=result.id).update(location='Город')
                    await db.Monsters.filter(id=er.id).update(battleStatus=0, nowhp = F('hp'))
                    await db.Users.filter(id=result.id).update(money=loser,
                                                                battleStatus=0, nowhp = F('hp'),
                                                                eat=100, energy=100,
                                                                progStatus=1)
                    await result.refresh_from_db()
                    await er.refresh_from_db()
                    if len(text) > 4096:
                        l = len(text) + 1
                        part_1 = text[0:l//2]
                        part_2 = text[l//2:]

                        await bot.send_message(call.message.chat.id, f'{part_1}')
                        await asyncio.sleep(1)
                        await bot.send_message(call.message.chat.id, f'{part_2}')
                    else:
                        await bot.send_message(call.message.chat.id, text)
                    buzyusrs[call.from_user.id] = False
                elif (int(er.nowhp) <= 0):
                    await battleWin(result, result.location, text, er, call)
                    return

        else:
            text += "\nУ тебя не хватает энергии. Битва продолжается."
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            if len(text) > 4096:
                l = len(text) + 1
                part_1 = text[0:l//2]
                part_2 = text[l//2:]

                await bot.send_message(call.message.chat.id, f'{part_1}')
                await asyncio.sleep(1)
                await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
            else:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)


    elif do == 'botWeapon':
        weapon = await db.BotInventory.get_or_none(id=call.data.split("_")[2]).first()
        droid = await db.Bot.get_or_none(id=weapon.idbot).first()
        if droid.status in [1, 2]:
            if weapon.lastAtk <= int(time.time()):
                if weapon.name == 'Лазерный выстрел':
                    atk = result.lvl * 1.5
                    bonusAtk = 0
                    checkBonusesToAtk = await db.BotInventory.filter(idbot=droid.id, active=2, type='Урон')
                    if checkBonusesToAtk:
                        for bonus in checkBonusesToAtk:
                            bonusAtk += bonus.bonus
                    fullAtk = int(atk * (bonusAtk / 100 + 1))
                    atk = int(fullAtk * 5)
                    er = await db.Monsters.get(id=result.battleWith).first()
                    er.nowhp -= atk
                    KDAtk = int(time.time()) + 600
                    await db.BotInventory.filter(id=weapon.id).update(lastAtk=KDAtk)
                    if int(er.nowhp) > 0:
                        text += "\nЛазерный выстрел бота нанёс {}🔪. Битва продолжается".format(atk)
                        markup = InlineKeyboardMarkup(row_width=2)
                        markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))

                        if len(text) > 4096:
                            l = len(text) + 1
                            part_1 = text[0:l//2]
                            part_2 = text[l//2:]

                            await bot.send_message(call.message.chat.id, f'{part_1}')
                            await asyncio.sleep(1)
                            await bot.send_message(call.message.chat.id, f'{part_2}', reply_markup=markup)
                        else:
                            await bot.send_message(call.message.chat.id, text, reply_markup=markup)                
                        # await result.save()
                        buzyusrs[call.from_user.id] = False
                        return
                    else:
                        await battleWin(result, result.location, text, er, call)
                        return
            else:
                text += "\nОружие не заряжено. Битва продолжается"
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
                await bot.send_message(call.message.chat.id, text, reply_markup=markup)                
        else:
            text += "\nОбнаружена неполадка бота. Битва продолжается"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton('Атаковать', callback_data="battle_atk"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)                
