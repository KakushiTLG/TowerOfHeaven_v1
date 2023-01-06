buzyUsrsPvP = {}



async def look_around(m, user):
    if m.from_user.id != m.chat.id:
        return

    user = await db.Users.get(user_id=m.from_user.id)
    needLoc = user.progLoc.split("|")[0]
    if needLoc != user.location:
        await m.answer("Ошибка.")
        return
    checkHlop = await db.Buffs.get_or_none(owner=user.id, status=1, type='hlopushka').first()
    if user.location in ['Город', 'Хэвенбург', 'Кавайня', 'Пустыня', 'Свалка', 'Экспедиция', 'Испытание сопряжения']:
        inventorySize = await db.getInventorySize(user)
        text = "❤️{}/{} ⚡️{}/100 🍗{}/100 📦{}/{}\n🏭{}\n\nВ этой локации можно использовать только стандартную навигацию.".format(user.nowhp, user.hp, user.energy, user.eat, inventorySize, user.inventorySizeMax, user.location)
        await m.answer(text)
        return
    if user.location == 'Свалка HD':
        inventorySize = await db.getInventorySize(user)
        text = "❤️❓ ⚡️{}/100 🍗{}/100 📦{}/{}\n🏭{}\n\nВ этой локации можно использовать только стандартную навигацию.".format(user.energy, user.eat, inventorySize, user.inventorySizeMax, user.location)
        await m.answer(text)
        return
    checkPlash = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=user.id)
    if checkPlash:
        inventorySize = await db.getInventorySize(user)
        text = "❤️{}/{} ⚡️{}/100 🍗{}/100 📦{}/{}\n🏭{}\n\nВы не сможете никого увидеть. Снимите плащ-невидимку".format(user.nowhp, user.hp, user.energy, user.eat, inventorySize, user.inventorySizeMax, user.location)
        await m.answer(text)
        return

    is_money_around = await db.MoneyDropLoc.filter(progLoc=user.progLoc)

    found_text = ['Проходя мимо, ты заметил поломанную дощечку и надпись на ней: "Здесь был публично унижен {}". Ты решил осмотреться, и не зря. В кусту ты нашел разодранный мешочек с {}💰',
                '"Эх, жаль деньги с неба не падают" - подумал ты, как вдруг на тебя упал тяжелый мешочек. Из содержимого - клочок бумаги с просьбой вернуть в случае утери {} и {}💰',
                'Внезапно, почтовая ворона Хэвенбурга села тебе на плечо, держа в клюве тряпичный мешочек. Внутри была записка:\n"Мои лазутчики притащили сокровища с полей сражений, решил как наставник поделиться с тобой. Ты давай, про меня не забывай, захаживай в бар как-нибудь, выпьем вместе, поручения дам тебе новые. Жду тебя, короче.\nТвой, Охранник."\n\nЕще, в мешочке оказалось {1}💰. Ты дал вороне кусочек сыра и она улетела.']
    found_zero = ['Ты увидел мешочек лежавший на траве. В таких обычно хранится... "хранится ЗОЛОТО!" - подумал ты, помчавшись за ним на радостях. В мешочке ты обнаружил сквозную... "..ДЫРУ!" - снова подумал ты, проклиная {}',
                'Твое внимание привлекло что-то сверкающее на земле. "Что это там? Золотая монета?" - такая мысль пронеслась у тебя в голове. Улыбка на лице пропала после того, как ты проверил монету "на зуб". Шоколадная конфетка в золотой обертке и в форме монетки поломалась от твоего укуса. Отчаявшись, ты решил ее съесть, но быстро выплюнул от горечи ее вкуса.\nТеперь тебе грустно...']
    found_text_kavaynya = 'Ты увидел кровь на снегу. Подойдя ближе, разглядел алую надпись: "Здесь был публично унижен {}". Рядом, в сугробе ты нашел намокший мешочек с {}💰'
    found_text_metro = 'Ты заметил чей-то кошелёк в луже радиактивной непонятной жидкости. К счастью, ты уже довольно долго обитаешь в Хэвэнбурге, чтобы узнать, что это кошелёк {}. Внутри было {}💰'
    
    if is_money_around:

        money_around = is_money_around[0]
        user.money += money_around.amount
        await user.save()
        
        if user.progLoc.startswith('Заснеженный лес'):
            await m.answer(found_text_kavaynya.format(money_around.username, money_around.amount))
        elif user.progLoc.startswith('Туннели метро'):
            await m.answer(found_text_metro.format(money_around.username, money_around.amount))
        elif money_around.amount == 0:
            res = random.choice(found_zero)
            await m.answer(res.format(money_around.username))
        else:
            res = random.choice(found_text)
            await m.answer(res.format(money_around.username, money_around.amount))
        await money_around.delete()
        await asyncio.sleep(1)

    nowProgLoc = user.progLoc
    _pl = nowProgLoc.split('|')
    num = _pl[1]
    users = await db.Users.filter(~Q(id=user.id), progLoc=user.progLoc, location=user.location)
    inventorySize = await db.getInventorySize(user)
    if checkHlop:
        text = "❤️❓ ⚡️{}/100 🍗{}/100 📦{}/{}\n🏭{}: К-{}\n\nСписок игроков рядом:\n".format(user.energy, user.eat, inventorySize, user.inventorySizeMax, user.location, num)
    else:
        text = "❤️{}/{} ⚡️{}/100 🍗{}/100 📦{}/{}\n🏭{}: К-{}\n\nСписок игроков рядом:\n".format(user.nowhp, user.hp, user.energy, user.eat, inventorySize, user.inventorySizeMax, user.location, num)
    pp = await db.getpp(user)
    minstats = int((pp) * 0.7)
    maxstats = int((pp) * 1.3)
    greenZoneMin = int((pp) * 0.7)
    greenZoneMax = int((pp) * 0.84)
    yellowZoneMin = int((pp) * 0.85)
    yellowZoneMax = int((pp) * 1.14)
    redZoneMin = int((pp) * 1.15)
    redZoneMax = int((pp) * 1.3)
    count = 0
    for z in users:
        checkViagra = await db.Inventory.exists(name='ВиАгро', active=3, idplayer=z.id)
        checkViagra2 = await db.Inventory.exists(name='ВиАгро', active=4, idplayer=z.id)
        checkHlop = await db.Buffs.get_or_none(owner=z.id, status=1, type='hlopushka').first()
        checkPlash = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=z.id)
        if checkPlash and not checkHlop and not checkViagra2 and not checkViagra: 
            pass
        else:
            ppEnemy = await db.getpp(z)
            minstatsEnemy = int((ppEnemy) * 0.7)
            maxstatsEnemy = int((ppEnemy) * 1.3)
            if int(ppEnemy) >= minstats and int(ppEnemy) <= maxstats or checkHlop:
                if int(pp) >= minstatsEnemy and int(pp) <= maxstatsEnemy or checkHlop:
                    text += "\n{} - /interact_{}".format(z.username, z.id)
                    count += 1
    if count == 0:
        text += "К сожалению, рядом никого нет"
    await bot.send_message(m.chat.id, text)


async def interact_(m, user):
    if m.from_user.id != m.chat.id:
        return
    result = m.text.replace('/interact_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    enemy = await db.Users.exists(id=result)
    if enemy:
        z = await db.Users.get(id=result)
        if player.id == z.id: return
        needLoc = z.progLoc.split("|")[0]
        if needLoc != z.location:
            await m.answer("Ошибка.")
            return
        text = ""
        krazhaTime = 15 + (z.antikrazha * 10)
        attackTime = 10 + (z.reactionPvP * 5)
        pp = await db.getpp(player)
        minstats = int((pp) * 0.7)
        maxstats = int((pp) * 1.3)
        greenZoneMin = int((pp) * 0.7)
        greenZoneMax = int((pp) * 0.84)
        yellowZoneMin = int((pp) * 0.85)
        yellowZoneMax = int((pp) * 1.14)
        redZoneMin = int((pp) * 1.15)
        redZoneMax = int((pp) * 1.3)
        ppEnemy = await db.getpp(z)
        minstatsEnemy = int((ppEnemy) * 0.7)
        maxstatsEnemy = int((ppEnemy) * 1.3)
        checkHlop = await db.Buffs.get_or_none(owner=z.id, status=1, type='hlopushka').first()
        if int(pp) >= minstatsEnemy and int(pp) <= maxstatsEnemy or checkHlop:
            if int(ppEnemy) >= minstats and int(ppEnemy) <= maxstats or checkHlop:
                checkAnalyz = await db.Inventory.exists(name='Анализатор БМ', active=2, idplayer=player.id)
                checkViagra = await db.Inventory.exists(name='ВиАгро', active=3, idplayer=z.id)
                checkViagra2 = await db.Inventory.exists(name='ВиАгро', active=4, idplayer=z.id)
                if checkAnalyz:
                    checkAntiAnalyz = await db.Inventory.exists(name='Анти-анализатор БМ', active=2, idplayer=z.id)
                    if checkAntiAnalyz and not checkViagra2 and not checkViagra2:
                        chance = '❓'
                    else:
                        if z.atk + z.hp >= greenZoneMin and z.atk + z.hp <= greenZoneMax: chance = '🟢'
                        elif z.atk + z.hp >= yellowZoneMin and z.atk + z.hp <= yellowZoneMax: chance = '🟡'
                        elif z.atk + z.hp >= redZoneMin and z.atk + z.hp <= redZoneMax: chance = '🔴'
                        else: chance = '🟡'
                    if checkViagra or checkViagra2:
                        text += "\n<i>Игрок:</i> <b>{}</b>\n<i>Клан:</i> <b>{}</b>\n\n<i>Вероятность победы в PvP:</i> {}\n<b>🆙ВиАгро активны</b>\n<i>Время кражи:</i> <b>{} секунд</b>\n<i>Время атаки:</i> <b>{} секунд</b>\n\n<code>Выберите действие</code>".format(z.username, z.frak, chance, krazhaTime, attackTime)
                    else:
                        text += "\n<i>Игрок:</i> <b>{}</b>\n<i>Клан:</i> <b>{}</b>\n\n<i>Вероятность победы в PvP:</i> {}\n<i>Время кражи:</i> <b>{} секунд</b>\n<i>Время атаки:</i> <b>{} секунд</b>\n\n<code>Выберите действие</code>".format(z.username, z.frak, chance, krazhaTime, attackTime)
                else:
                    if checkViagra or checkViagra2:
                        text += "\n<i>Игрок:</i> <b>{}</b>\n<i>Клан:</i> <b>{}</b>\n\n<b>🆙ВиАгро активны</b>\n<i>Время кражи:</i> <b>{} секунд</b>\n<i>Время атаки:</i> <b>{} секунд</b>\n\n<code>Выберите действие</code>".format(z.username, z.frak, krazhaTime, attackTime)
                    else:
                        text += "\n\n<i>Игрок:</i> <b>{}</b>\n<i>Клан:</i> <b>{}</b>\n\n<i>Время кражи:</i> <b>{} секунд</b>\n<i>Время атаки:</i> <b>{} секунд</b>\n\n<code>Выберите действие</code>".format(z.username, z.frak, krazhaTime, attackTime)
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Атаковать', callback_data="newattack_{}".format(z.id)))
                if player.krazha >= 1: markup.add(InlineKeyboardButton('Обокрасть', callback_data="krazha_{}".format(z.id)))
                droid1 = await db.Bot.get_or_none(idplayer=player.id, status__in=[1, 2]).first()
                droid2 = await db.Bot.get_or_none(idplayer=z.id, status__in=[1, 2]).first()
                if droid1 and droid2:
                    if player.user_id in hackKD:
                        if hackKD[player.user_id] <= int(time.time()): markup.add(types.InlineKeyboardButton('Взлом', callback_data='hack_{}'.format(droid2.id)))
                    else: markup.add(types.InlineKeyboardButton('Взлом', callback_data='hack_{}'.format(droid2.id)))
                await bot.send_message(m.chat.id, text, reply_markup=markup, parse_mode='html')
    else:
        await bot.send_message(m.chat.id, 'Ошибка игрока')

time_to_rob = {}

async def krazha_(call, player):
    if call.message.chat.id == call.from_user.id:
        pass
    else:
        return
    do = call.data.split('_')
    result = do[1]
    enemy = await db.Users.get_or_none(id=result)
    if enemy and player.id == enemy.id: return
    if enemy:
        pass
    else:
        await bot.edit_message_text("Игрока не существует", call.message.chat.id, call.message.message_id)
        return

    enemy = await db.Users.get(id=result)

    if not time_to_rob.get(enemy.user_id) or time.time() > time_to_rob[enemy.user_id]['time'] + 60:
        pass
    elif time.time() < time_to_rob[enemy.user_id]['time'] + 60:
        await call.message.answer('Нет, лучше переждать еще чуток. Если идти прямо сейчас — заметят 100%-но!')
        return

    if player.frak in ['Эгида', 'Авангард Феникса', 'Небесные рыцари', 'Вавилон'] and player.frak == enemy.frak:
        await bot.edit_message_text("Стыдно красть у союзника!", call.message.chat.id, call.message.message_id)
        return

    if player.progLoc != enemy.progLoc:
        await call.message.edit_text('Потерял его из виду. Может, он уже ушел?')
        return

    checkPlashEnemy = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=enemy.id)
    if checkPlashEnemy:
        checkViagro = await db.Inventory.exists(name='ВиАгро', active=4, idplayer=enemy.id)
        checkViagro2 = await db.Inventory.exists(name='ВиАгро', active=3, idplayer=enemy.id)
        if checkViagro or checkViagro2: passPvp = 1
        else: passPvp = 0
    checkPlashPlayer = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=player.id)
    if checkPlashPlayer or checkPlashEnemy and passPvp == 0:
        await bot.edit_message_text("У вас или противника надет Плащ-невидимка.", call.message.chat.id, call.message.message_id)
        return
    if player.location == "Хэвенбург" or enemy.location == 'Хэвенбург' or player.location == 'Кавайня' or enemy.location == 'Кавайня' or player.location == 'Экспедиция' or enemy.location == 'Экспедиция':
        await bot.send_message(player.user_id, "Игрок уже покинул это место либо вы уже прошли мимо.")
        return
    pp = await db.getpp(player)
    ppEnemy = await db.getpp(enemy)
    minstatsEnemy = int((ppEnemy) * 0.7)
    maxstatsEnemy = int((ppEnemy) * 1.3)
    if int(pp) >= minstatsEnemy and int(pp) <= maxstatsEnemy:
        pass
    else:
        await bot.edit_message_text("Вы не можете драться с этим игроком", call.message.chat.id, call.message.message_id)
        return

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('👊Поймать вора!', callback_data="catch_robber_{}".format(player.id)))

    await call.message.edit_text(f'Ты решил обшарить карманы _{enemy.username}_. С какой же стороны подойти...', parse_mode='Markdown')
    try:
        await bot.send_message(enemy.user_id,
            'Пятой точкой ты почувствовал неладное. Кажется кто-то хочет тебя обокрасть! Поймай его скорее!',
            reply_markup=markup
                                )
    except:
        pass
    timeToSleep = 15 + enemy.antikrazha * 10
    time_to_rob[enemy.user_id] = {'time': timeToSleep + time.time(), 'is_catched': False}
    await asyncio.sleep(timeToSleep)

    if time_to_rob[enemy.user_id]['is_catched'] == True:
        await call.message.answer(f'Последнее что ты помнишь - это как тебя привязали к дереву, до тех пор пока не приехал Охранник. Он посадил тебя в карету и увез на допрос в Хэвенбург. Еще, ты обнаружил, что кто-то спер у тебя {int(player.money * 0.1)}💰')
        return

    if player.user_id == enemy.user_id:
        await bot.send_message(player.user_id, "Ну и что ты хотел у себя украсть?")
        buzyUsrsPvP[player.from_user.id] = 0
        return
    if player.location == enemy.location and player.progLoc == enemy.progLoc:
        pass
    else:
        await bot.send_message(player.user_id, "_Жертва скрылась из виду раньше, чем ты успел на него напасть._", parse_mode='Markdown')
        buzyUsrsPvP[player.user_id] = 0
        buzyUsrsPvP[enemy.user_id] = 0
        return
    base = ['Бумажный бургер',
            'Он называет это "яблоко"',
            'Хер огра',
            'Бывший сосед',
            'Консервы из палеозоя',
            'Малое зелье здоровья',
            'Шаурма',
            'Лучше не спрашивай',
            'Бывший сосед(поджаренный)',
            'Бывший сосед(замороженный)',
            'Большой хер огра',
            'Двойная шаурма',
            'Валентинка',
            'Среднее зелье здоровья',
            'Большое зелье здоровья',
            'Зелье восстановления',
            'Свиток телепортации',
            'Останки героев',
            'Цветок сакуры',
            'Роза',
            'RCA',
            'Одуванчик',
            'Ситень',
            'Снунец',
            'Багровая чешуя',
            'unweared_armor',
            'Опустошенный сундук',
            'Сундук щитоносцев',
            'Ашондук',
            'Аптечка',
            'Сун-дук',
            'Ashot case',
            'Огромный сундук',
            'Шкатулка Кефира',
            'Маленький сундучок',
            'Кофе',
            'Дрова',
            'gold',
            'Чешуйчатое снадобье',
            'Полотенце',
            'Багровая бомба',
            'Паучий афродизиак',
            'Бамбук для курения',
            'Настойка боярышника',
            'ВиАгро',
            'ГероИн',
            'weared_armor'
            ]
    to_rob = {
                1: base[0:7],
                2: base[0:15],
                3: base[0:17],
                4: base[0:26], 
                5: base[0:37],
                6: base[0:38],
                7: base[0:41],
                8: base[0:47],
                9: base[0:48],
                10: base[0:48]
                }

    available_items = to_rob[player.krazha]

    victim_inv = await db.Inventory.filter(~Q(active=0), idplayer=enemy.id).only('name')

    items_to_steal_not_unique = [x.name for x in victim_inv if x.name in available_items]
    uniqueize = set(items_to_steal_not_unique)
    items_to_steal = list(uniqueize)
    try:
        steal_item = random.choice(items_to_steal)
    except:
        await bot.send_message(player.user_id, "_Втихую открыв чужой рюкзак ты нашёл... Ничего. Кажется, тут нечего воровать..._", parse_mode='Markdown')
        return
    # check_item = await db.Inventory.filter(name=steal_item, idplayer=enemy.id).exists()
    await enemy.refresh_from_db()

    if steal_item == 'gold':
        await db.Users.filter(id=enemy.id).update(money=F('money') - int(F('money') * 0.5))
        await db.Users.filter(id=player.id).update(money=F('money') + int(enemy.money * 0.5))
        return

    if steal_item == 'weared_armor':
        armor = await db.Inventory.filter(active=2, idplayer=enemy.id, type='Броня')
        choice = random.choice(armor)

        inventorySize = await db.getInventorySize(player)
        size = await db.items(choice.name, check='size')

        if int(inventorySize) + int(size) > player.inventorySizeMax:                
            await call.message.answer(f'Ты хотел снять с {enemy.username} его {choice.name}, но у тебя не хватило места в инвентаре, чтобы унести это с собой. Лучше отойду в сторонку, пока меня не заметили...')
            return

        await db.Inventory.filter(name=choice.name, active=2, idplayer=enemy.id).update(active=1, idplayer=player.id)
        allArmor = await db.Inventory.filter(active=2, idplayer=enemy.id)
        newArmor = sum([item.bonus for item in allArmor])
        await db.Users.filter(id=enemy.id).update(armor=newArmor)

        await call.message.answer(f'Ты снял с {enemy.username} его {item_to_steal[0].name}. Сияешь как медный таз. Надо валить пока не заметили...')
        await asyncio.sleep(.05)
        try:
            await bot.send_message(enemy.user_id, f'Ты почувствовал дуновение ветерка в той части тела, где раньше был {item_to_steal[0].name}. Тебя обокрали!')
        except:
            pass
        return

    if steal_item == 'unweared_armor':
        armor = await db.Inventory.filter(active=1, idplayer=enemy.id, type='Броня')
        choice = random.choice(armor)

        inventorySize = await db.getInventorySize(player)
        size = await db.items(choice.name, check='size')

        if int(inventorySize) + int(size) > player.inventorySizeMax:                
            await call.message.answer(f'Ты хотел скомуниздить у {enemy.username} его {item_to_steal[0].name}, но у тебя не хватило места в инвентаре, чтобы унести это с собой. Лучше отойду в сторонку, пока меня не заметили...')
            return

        await db.Inventory.filter(name=choice.name, active=1, idplayer=enemy.id).limit(1).update(idplayer=player.id)
        allArmor = await db.Inventory.filter(active=2, idplayer=enemy.id)

        await call.message.answer(f'Повезло! Свистнул с его инвентаря {item_to_steal[0].name}. Счастья полные штаны. Надо валить пока не заметили...')
        await asyncio.sleep(.05)
        try:
            await bot.send_message(enemy.user_id, f'У тебя украли {item_to_steal[0].name}. Разиня!')
        except:
            pass
        return

    item_to_steal = await db.Inventory.filter(name=steal_item, active=1, idplayer=enemy.id).limit(1)

    inventorySize = await db.getInventorySize(player)
    size = await db.items(item_to_steal[0].name, check='size')

    if int(inventorySize) + int(size) > player.inventorySizeMax:                
        await call.message.answer(f'Ты хотел скомуниздить у {enemy.username} его {item_to_steal[0].name}, но у тебя не хватило места в инвентаре, чтобы унести это с собой. Лучше отойду в сторонку, пока меня не заметили...')
        return

    await db.Inventory.filter(name=item_to_steal[0].name, active=1, idplayer=enemy.id).limit(1).update(idplayer=player.id)

    await call.message.answer(f'Украл с его инвентаря {item_to_steal[0].name}. Надо валить пока не заметили...')
    await asyncio.sleep(.05)
    try:
        await bot.send_message(enemy.user_id, f'У тебя украли {item_to_steal[0].name}. Разиня!')
    except:
        pass

async def catch_robber(call):
    robber_id = call.data.split('catch_robber_')[1]

    if time.time() > time_to_rob[call.from_user.id]['time']:
        await call.message.edit_text('Поздно ты, однако, спохватился...')
        return

    time_to_rob[call.from_user.id]['is_catched'] = True

    robber = await db.Users.get(id=robber_id)
    newMoney = int(robber.money * 0.9)
    await db.Users.filter(id=robber_id).update(location='Хэвенбург', money=newMoney)
    await db.Users.filter(user_id=call.from_user.id).update(money=F('money') + int(robber.money * 0.1))

    await call.message.edit_text(f'Ты поймал ворюгу! Отшлепал <i>{robber.username}</i> по попе и привязал бедолагу к дереву. Отправил первой же попавшейся вороной заявление в полицию Хэвенбурга.\n\nА еще, ты забрал у него часть денег. Вышло около {int(robber.money * 0.1)}💰', parse_mode='HTML')



buzyUsrsPvP = {}


poslaniya = {}
poslaniyaUserStatus = {}
async def poslanie(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    if user.almaz > 0:
        pass
    else:
        await bot.edit_message_text("У вас нет 💎", call.message.chat.id, call.message.message_id)
        return
    nav = call.data.split('_')
    navWho = nav[1]
    poslaniya[call.from_user.id] = navWho
    text = "Введите текст послания"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    poslaniyaUserStatus[call.from_user.id] = 'poslaniye'

@dp.message_handler(lambda m: poslaniyaUserStatus and m.from_user.id in poslaniyaUserStatus and poslaniyaUserStatus[m.from_user.id]=='poslaniye')
async def poslanie_go(m):
    user = await db.Users.get(user_id=m.from_user.id)
    if user.almaz > 0:
        try:
            await bot.send_message(poslaniya[m.from_user.id], 'Почтовая ворона города Хэвенбург прислала письмо от {}:\n\n"_{}_"'.format(user.username, m.text), parse_mode='markdown')
            user.almaz -= 1
            await user.save()
            await m.answer("Послание успешно отправлено!")
        except:
            await m.answer("Послание отправить не удалось.")
    else:
        await bot.send_message(m.chat.id, "У вас нет 💎")
    poslaniyaUserStatus[m.from_user.id] = None





# async def pvptp(call):
#     await db.Users.filter(user_id=call.from_user.id).update(location='Хэвенбург', position='Площадь')
#     await call.message.edit_text('Вы успешно телепортировались в город.')

async def newattack_(call, player):
    if call.message.chat.id == call.from_user.id:
        pass
    else:
        return
    do = call.data.split('_')
    attacking = do[1]

    enemy = await db.Users.get_or_none(id=attacking)
    if enemy.id == player.id: return
    if not enemy:
        await bot.edit_message_text("Игрока не существует.", call.message.chat.id, call.message.message_id)
        return

    playerFrak = None
    if player.frak:
        playerFrak = await db.Fraks.get_or_none(name=player.frak).first()
        if enemy.frak:
            enemyFrak = await db.Fraks.get_or_none(name=enemy.frak).first()

    if playerFrak and player.frak == enemy.frak:
        await bot.edit_message_text("Нельзя драться со своим союзником!", call.message.chat.id, call.message.message_id)
        return

    checkPlashEnemy = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=enemy.id)
    if checkPlashEnemy:

        checkViagro = await db.Inventory.exists(Q(Q(active=4), Q(active=3), join_type='OR'), name='ВиАгро', idplayer=enemy.id)
        
        if checkViagro:
            passPvp = 1
        else:
            passPvp = 0

    checkPlashPlayer = await db.Inventory.exists(name='Плащ-невидимка', active=2, idplayer=player.id)
    checkHlop = await db.Buffs.get_or_none(owner=enemy.id, status=1, type='hlopushka').first()

    if checkHlop: passPvp = 1
    if checkPlashPlayer or checkPlashEnemy and passPvp == 0:
        await bot.edit_message_text("У Вас или у противника надет Плащ-невидимка.", call.message.chat.id, call.message.message_id)
        return


    ppPlayer = await db.getpp(player)
    ppEnemy = await db.getpp(enemy)
    minstatsEnemy = int((ppEnemy) * 0.7)
    maxstatsEnemy = int((ppEnemy) * 1.3)
    minstats = int((ppPlayer) * 0.7)
    maxstats = int((ppPlayer) * 1.3)
    if int(ppEnemy) >= minstats and int(ppEnemy) <= maxstats or checkHlop:
        if int(ppPlayer) >= minstatsEnemy and int(ppPlayer) <= maxstatsEnemy or checkHlop:
            pass
        else:
            await bot.edit_message_text("Вы не можете драться с этим игроком - силы неравны!", call.message.chat.id, call.message.message_id)
            return
    else:
        await bot.edit_message_text("Вы не можете драться с этим игроком - силы неравны!", call.message.chat.id, call.message.message_id)
        return

    try:
        if buzyUsrsPvP[call.from_user.id] and buzyUsrsPvP[call.from_user.id] == 1:
            await bot.edit_message_text("Вы уже заняты подготовкой к другой битве.", call.message.chat.id, call.message.message_id)
            return
    except:
        pass

    try:
        if buzyUsrsPvP[enemy.user_id] and buzyUsrsPvP[enemy.user_id] == 1:
            await bot.edit_message_text("Игрок уже участвует в битве.", call.message.chat.id, call.message.message_id)
            return
    except:
        pass

    if player.zamoroz >= 100 and player.location == 'Заснеженный лес':
        await call.message.edit_text('🥶Х-холодрыга какая! Согреться бы сначала...')
        return
    elif player.humidity >= 100 and player.location == 'Окус Локус':
        await call.message.edit_text(f'🥵Может не сейчас? Даже ходить трудно, а {player.visualitem} так вообще в руках не удержу...')
        return

    if player.location == enemy.location and player.progLoc == enemy.progLoc and player.location != 'Кавайня' and player.location != 'Хэвенбург':
        await bot.edit_message_text("_Ты решил нажиться на чужом разбитом хлебале. Тебе понадобится некоторое время..._", call.message.chat.id, call.message.message_id, parse_mode='markdown')
        buzyUsrsPvP[call.from_user.id] = 1
        buzyUsrsPvP[enemy.user_id] = 1

        react_kb = types.InlineKeyboardMarkup()
        btns = [types.InlineKeyboardButton('Отбиться!', callback_data='counterattack')]

        alert = ''

        if enemy.zamoroz >= 100 and enemy.location == 'Заснеженный лес':
            alert = '🥶Ты не можешь сейчас драться, а времени отогреться уже нет...'
            del btns[0]
        elif enemy.humidity >= 100 and enemy.location == 'Окус Локус':
            alert = '🥵Ты не можешь сейчас драться, а времени вытереться нет...'
            del btns[0]

        has_tp = await db.Inventory.get_or_none(active=1, name='Свиток телепортации', idplayer=enemy.id).first()
        if has_tp:
            btns.append(types.InlineKeyboardButton('Телепортироваться', callback_data=f'invUsing_{has_tp.id}'))

        react_kb.add(*btns)
        try:
            enemy_msg = await bot.send_message(enemy.user_id,
                                    f"_Заиграла настораживающая музыка и появилось ощущение, словно кто-то готовится напасть на тебя._\n*{alert}*",
                                    parse_mode='markdown',
                                    reply_markup=react_kb
                                    )
        except:
            pass

        await db.Users.filter(id=enemy.id).update(battleStatus=2, progStatus=0, battleWith=player.id)
        await db.Users.filter(id=player.id).update(battleStatus=2, progStatus=0, battleWith=enemy.id)

        await db.DuelPool.create(
                                agressor=player.user_id,
                                defender=enemy.user_id,
                                current_turn='agressor',
                                react_until=time.time()+11,
                                duel_location=player.location
                                )
        awaitTime = int(12 + enemy.reactionPvP)
        await asyncio.sleep(awaitTime) # 10 +1 sec in reserve

        # oneshot if enemy hasn't reset freezing/humidity

        if enemy.zamoroz >= 100 and enemy.location == 'Заснеженный лес':
            battle_log = f'Ход 1. 🔵{enemy.username} не успел парировать первый удар! 🔴{player.username} наносит фатальный урон по замерезшему бедняге 🔵{enemy.username}.'
            await close_pool_by_loose(  
                                        call,
                                        enemy_msg,
                                        player,
                                        enemy,
                                        'victim',
                                        battle_log
                                        )
            return
        elif enemy.humidity >= 100 and enemy.location == 'Окус Локус':
            battle_log = f'Ход 1. 🔵{enemy.username} не успел парировать первый удар! 🔴{player.username} наносит фатальный урон по 🔵{enemy.username} пока тот, шатался из стороны в сторону из-за жары. Ели попал!'
            await close_pool_by_loose(  
                                        call,
                                        enemy_msg,
                                        player,
                                        enemy,
                                        'victim',
                                        battle_log
                                        )
            return

        pool = await db.DuelPool.filter(agressor=player.user_id).first()

        post_sleep_kb = types.InlineKeyboardMarkup()
        post_sleep_kb.add(types.InlineKeyboardButton('Атаковать', callback_data='queue_attack'))
        plusBattleLog = None
        if pool.current_turn == 'defender':

            enemy_atk = await count_dmg(player, 1, 'defender', enemy)

            if enemy_atk == 0:
                temp_log = f'Ход 1. Атака 🔴{player.username} из засады не удалась - он был повален на землю! 🔵{enemy.username} пытается нанести смертельный удар, но бот 🔴{player.username} помогает увернуться.'
            else:
                healed = await getDroidPvPHeal(enemy)
                if healed > 0:
                    heal = enemy_atk * (healed / 100)
                    plusBattleLog = f"\n🔵{enemy.username} восстанавливает вампиризмом бота {heal}❤️\n"
                    await db.Users.filter(id=enemy.id).update(nowhp=F('nowhp') + heal)


                temp_log = f'Ход 1. Атака 🔴{player.username} из засады не удалась - он был повален на землю! 🔵{enemy.username} наносит смертельную рану {enemy_atk}💔.'
                if plusBattleLog: temp_log += plusBattleLog
            if player.nowhp - enemy_atk <= 0:
                await close_pool_by_loose(
                                            call,
                                            enemy_msg,
                                            player,
                                            enemy,
                                            'agressor',
                                            temp_log
                                            )
                return
            else:
                remain_player_hp = f'У 🔴{player.username} осталось {player.nowhp - enemy_atk}❤️, его ход следующий.'

            await db.Users.filter(id=player.id).update(nowhp=F('nowhp') - enemy_atk)
            battle_log = f'Ход 1. Атака 🔴{player.username} из засады не удалась - он был повален на землю! 🔵{enemy.username} наносит {enemy_atk}💔\n{remain_player_hp}'
            
            await db.DuelPool.filter(agressor=player.user_id).update(
                                                                    react_until=time.time() + 10,
                                                                    battle_log=battle_log,
                                                                    current_turn='agressor'
                                                                    )
            try:
                await bot.edit_message_text(battle_log,
                                        enemy_msg.chat.id,
                                        enemy_msg.message_id)
            except:
                pass
            await asyncio.sleep(.05)
            try:
                await call.message.edit_text(battle_log, reply_markup=post_sleep_kb)
            except:
                pass
                
        elif pool.current_turn == 'agressor':
            # player_atk = player.atk + player.atk * 0.2
            player_atk = await count_dmg(enemy, 1, 'agressor', player)
            plusBattleLog = None
            
            if player_atk == 0:
                temp_log = f'Ход 1. 🔵{enemy.username} не успел парировать первый удар! 🔴{player.username} не смог нанести удар 🔵{enemy.username} - его спасает бот.'
            else:
                healed = await getDroidPvPHeal(player)
                if healed > 0:
                    heal = player_atk * (healed / 100)
                    plusBattleLog = f"\n🔴{player.username} восстанавливает вампиризмом бота {heal}❤️\n"
                    await db.Users.filter(id=player.id).update(nowhp=F('nowhp') + heal)

                temp_log = f'Ход 1. 🔵{enemy.username} не успел парировать первый удар! 🔴{player.username} наносит смертельную рану {player_atk}💔'
                if plusBattleLog: temp_log += plusBattleLog
            if enemy.nowhp - player_atk <= 0:
                await close_pool_by_loose(
                                            call,
                                            enemy_msg,
                                            player,
                                            enemy,
                                            'victim',
                                            temp_log
                                            )
                return
            else:
                remain_enemy_hp = f'У 🔵{enemy.username} осталось {enemy.nowhp - player_atk}❤, его ход следующий.'
            await db.Users.filter(id=enemy.id).update(nowhp=F('nowhp') - player_atk)
            battle_log = f'Ход 1. 🔵{enemy.username} не успел парировать первый удар! 🔴{player.username} наносит критический урон {player_atk}💔\n{remain_enemy_hp}'
            
            await db.DuelPool.filter(agressor=player.user_id).update(
                                                                    react_until=time.time() + 10,
                                                                    battle_log=battle_log,
                                                                    current_turn='defender'
                                                                    )
            try:
                await bot.edit_message_text(battle_log,
                                        enemy_msg.chat.id,
                                        enemy_msg.message_id,
                                        reply_markup=post_sleep_kb)
            except:
                pass
            await asyncio.sleep(.05)
            try:
                await call.message.edit_text(battle_log)
            except:
                pass
        await pool.refresh_from_db()

        await sleep_again(player.user_id, call, enemy_msg, 2)


    else:
        await bot.edit_message_text("Игрок уже покинул это место либо вы уже прошли мимо.", call.message.chat.id, call.message.message_id)
        buzyUsrsPvP[call.from_user.id] = 0
        buzyUsrsPvP[enemy.user_id] = 0



async def counter_attack(call): # function handling first reaction of defender
    pool = await db.DuelPool.get(defender=call.from_user.id).only('react_until', 'agressor').distinct()
    agressor = await db.Users.get(user_id=pool.agressor).only('username')

    if time.time() > pool.react_until:
        await call.message.edit_text('Вы проспали первый удар! Противник наносит критический урон!')
        return

    who_is_next = random.randint(1, 100)

    if who_is_next in range(1, 71):
        await db.DuelPool.filter(defender=call.from_user.id).update(current_turn='defender')
        await call.message.edit_text(f'Вы не дали {agressor.username} застать Вас врасплох и даже повалили его на землю!')
    else:
        await call.message.edit_text(f'Вы заметили {agressor.username}, но не успели увернуться от оглушающего удара - вы на земле!')

async def queue_attack(call): # all other reactions
    pool = await db.DuelPool.get_or_none(Q(defender=call.from_user.id) | Q(agressor=call.from_user.id))
    
    if not pool:
        await call.message.edit_text('Не помню, чтобы я с ним сейчас дрался...')
        return

    if time.time() > pool.react_until:
        await call.message.edit_text('Вы проспали удар! Противник наносит критический урон!')
        return

    # if pool.current_turn == 'agressor':
    #     to_bonk = await db.Users.get(user_id=pool.agressor).only('username')
    #     await db.DuelPool.filter(defender=pool.defender).update(current_turn='defender')
    #     await call.message.edit_text(f'Сейчас как дам этому {to_bonk.username} по бошке!')

    # elif pool.current_turn == 'defender':
    #     await db.DuelPool.filter(defender=pool.defender).update(current_turn='agressor')

    if pool.agressor == call.from_user.id:
        to_bonk = await db.Users.get(user_id=pool.defender).only('username')
    else:
        to_bonk = await db.Users.get(user_id=pool.agressor).only('username')

    await db.DuelPool.filter(id=pool.id).update(is_reacted=1)
    await call.message.edit_text(f'Сейчас как дам этому {to_bonk.username} по бошке!')

async def count_dmg(defender, step, turn, attacking):

    if attacking.energy > 90: EnergyAtk = 1
    elif attacking.energy in range(81, 91): EnergyAtk = 0.97
    elif attacking.energy in range(71, 81): EnergyAtk = 0.9
    elif attacking.energy in range(61, 71): EnergyAtk = 0.83
    elif attacking.energy in range(51, 61): EnergyAtk = 0.75
    elif attacking.energy in range(41, 51): EnergyAtk = 0.66
    elif attacking.energy in range(31, 41): EnergyAtk = 0.57
    elif attacking.energy in range(21, 31): EnergyAtk = 0.48
    elif attacking.energy in range(11, 21): EnergyAtk = 0.35
    elif attacking.energy in range(1, 11): EnergyAtk = 0.29
    else: EnergyAtk = 0.2
    playerAtk = int((attacking.atk * 0.8)  * EnergyAtk)

    bonusAtk = await getDroidAtk(attacking)
    if bonusAtk > 0:
        newPlayerAtk = playerAtk * (bonusAtk / 100 + 1)
        playerAtk = int(newPlayerAtk)


    if step == 1 and turn == 'agressor':
        weared = await db.Inventory.filter(idplayer=defender.id, type='Броня', active=2).only('atk_block')


        block_bonus = sum([x.atk_block for x in weared]) / 100

        if block_bonus == 0:
            return playerAtk


        getBonusAtk = await getDroidPvPAtk(attacking)
        getBonusUv = await getDroidPvPUv(defender)
        if getBonusUv > 0:
            rand = random.randint(1, 100)
            if rand <= getBonusUv:
                final_attack = 0
                return int(final_attack)
        if getBonusAtk > 0:
            final_attack = (playerAtk + (playerAtk * (getBonusAtk / 100))) - (playerAtk + playerAtk * 0.2) * block_bonus
        
        else:
            final_attack = playerAtk - (playerAtk + playerAtk * 0.2) * block_bonus

        return int(final_attack)

    elif step == 1 and turn == 'defender':
        weared = await db.Inventory.filter(idplayer=defender.id, type='Броня', active=2).only('atk_block')

        block_bonus = sum([x.atk_block for x in weared]) / 100

        if block_bonus == 0:
            return playerAtk


        getBonusAtk = await getDroidPvPAtk(attacking)
        
        getBonusUv = await getDroidPvPUv(defender)
        if getBonusUv > 0:
            rand = random.randint(1, 100)
            if rand <= getBonusUv:
                final_attack = 0
                return int(final_attack)
        
        if getBonusAtk > 0:
            final_attack = (playerAtk + (playerAtk * (getBonusAtk / 100))) - playerAtk * block_bonus

        else:
            final_attack = playerAtk - playerAtk * block_bonus

        return int(final_attack)

    weared = await db.Inventory.filter(idplayer=defender.id, type='Броня', active=2).only('atk_block')

    block_bonus = sum([x.atk_block for x in weared]) / 100

    if block_bonus == 0:
        return playerAtk

    final_attack = playerAtk - playerAtk * block_bonus

    return int(final_attack)


async def sleep_again(agr_id, call, enemy_msg, step):
    await asyncio.sleep(11) # 10 +1 sec in reserve

    pool = await db.DuelPool.get(agressor=agr_id)

    if step == 20: # if battle lasts too long
        await bot.edit_message_text('Боги наблюдающие за битвой зазевались от скуки. Вы лишились жизни в этой долгой схватке.',
                                    enemy_msg.chat.id,
                                    enemy_msg.message_id)
        await asyncio.sleep(.05)
        await call.message.edit_text('Боги наблюдающие за битвой зазевались от скуки. Вы лишились жизни в этой долгой схватке.')

        await db.Users.filter(user_id__in=[pool.agressor, pool.defender]).update(
                                                    nowhp=1,
                                                    battleStatus=0,
                                                    progStatus=1,
                                                    location='Хэвенбург')
        await db.DuelPool.filter(id=pool.id).delete()
        return

    player = await db.Users.get(user_id=pool.agressor)
    enemy = await db.Users.get(user_id=pool.defender)

    if player.location != pool.duel_location or enemy.location != pool.duel_location:
        await db.DuelPool.filter(id=pool.id).delete()
        await db.Users.filter(id__in=[player.id, enemy.id]).update(battleStatus=0, battleWith=0, progStatus=1)
        await call.message.edit_text(f'{pool.battle_log}\n\n Дуэлянт сбежал? Или, быть может погиб по другой причине? Ты решил пойти дальше.')
        buzyUsrsPvP[player.user_id] = 0
        buzyUsrsPvP[enemy.user_id] = 0
        return


    post_sleep_kb = types.InlineKeyboardMarkup()
    post_sleep_kb.add(types.InlineKeyboardButton('Атаковать', callback_data='queue_attack'))
    if pool.current_turn == 'defender' and pool.is_reacted:

        # enemy_atk = enemy.atk

        enemy_atk = await count_dmg(player, step, 'defender', enemy)
        plusBattleLog = None
        if enemy_atk == 0:
            battle_log = f'{pool.battle_log}\n\nХод {step}. 🔵{enemy.username} не смог нанести урон 🔴{player.username} - бот помогает увернуться.\n'
        else:
            healed = await getDroidPvPHeal(enemy)
            if healed > 0:
                heal = player_atk * (healed / 100)
                plusBattleLog = f"\n🔵{enemy.username} восстанавливает вампиризмом бота {heal}❤️\n"
                await db.Users.filter(id=enemy.id).update(nowhp=F('nowhp') + heal)

            if player.nowhp - enemy_atk <= 0:
                await close_pool_by_loose(
                                            call,
                                            enemy_msg,
                                            player,
                                            enemy,
                                            'agressor',
                                            pool.battle_log
                                            )
                return

            else:
                remain_player_hp = f'У 🔴{player.username} осталось {player.nowhp - int(enemy_atk)}❤️, его ход следующий.'

            await db.Users.filter(id=player.id).update(nowhp=F('nowhp') - int(enemy_atk))
            battle_log = f'{pool.battle_log}\n\nХод {step}. 🔵{enemy.username} наносит {enemy_atk}💔\n{remain_player_hp}\n'
            if plusBattleLog: battle_log += plusBattleLog
        
        await db.DuelPool.filter(agressor=player.user_id).update(
                                                                react_until=time.time() + 10,
                                                                battle_log=battle_log,
                                                                is_reacted=0,
                                                                current_turn='agressor'
                                                                )
        await bot.edit_message_text(battle_log,
                                    enemy_msg.chat.id,
                                    enemy_msg.message_id)
        await asyncio.sleep(.05)
        await call.message.edit_text(battle_log, reply_markup=post_sleep_kb)
    
    elif pool.current_turn == 'defender' and not pool.is_reacted:

        battle_log = f'{pool.battle_log}\n\nХод {step}. 🔵{enemy.username} зазевался и был оглушен, снова атакует 🔴{player.username}!'

        await db.DuelPool.filter(agressor=player.user_id).update(
                                                                react_until=time.time() + 10,
                                                                battle_log=battle_log,
                                                                current_turn='agressor'
                                                                )

        await bot.edit_message_text(battle_log,
                                    enemy_msg.chat.id,
                                    enemy_msg.message_id)
        await asyncio.sleep(.05)
        await call.message.edit_text(battle_log, reply_markup=post_sleep_kb)

    if pool.current_turn == 'agressor' and pool.is_reacted:
        # player_atk = player.atk

        player_atk = await count_dmg(enemy, step, 'agressor', player)
        plusBattleLog = None
        if player_atk == 0:
            battle_log = f'{pool.battle_log}\n\nХод {step}. 🔴{player.username} не смог нанести урон 🔵{enemy.username} - бот помогает увернуться.\n'
        else:
            healed = await getDroidPvPHeal(player)
            if healed > 0:
                heal = player_atk * (healed / 100)
                plusBattleLog = f"\n🔴{player.username} восстанавливает вампиризмом бота {heal}❤️\n"
                await db.Users.filter(id=player.id).update(nowhp=F('nowhp') + heal)
            if enemy.nowhp - player_atk <= 0:
                await close_pool_by_loose(
                                            call,
                                            enemy_msg,
                                            player,
                                            enemy,
                                            'victim',
                                            pool.battle_log
                                            )
                return
            else:
                remain_enemy_hp = f'У 🔵{enemy.username} осталось {enemy.nowhp - player_atk}❤️, его ход следующий.'
            await db.Users.filter(id=enemy.id).update(nowhp=F('nowhp') - player_atk)
            battle_log = f'{pool.battle_log}\n\nХод {step}. 🔴{player.username} наносит {player_atk}💔\n{remain_enemy_hp}'
            if plusBattleLog: battle_log += plusBattleLog
        await db.DuelPool.filter(agressor=player.user_id).update(
                                                                react_until=time.time() + 10,
                                                                battle_log=battle_log,
                                                                is_reacted=0,
                                                                current_turn='defender'
                                                                )
        await bot.edit_message_text(battle_log,
                                    enemy_msg.chat.id,
                                    enemy_msg.message_id,
                                    reply_markup=post_sleep_kb)
        await asyncio.sleep(.05)
        await call.message.edit_text(battle_log)

    elif pool.current_turn == 'agressor' and not pool.is_reacted:
        battle_log = f'{pool.battle_log}\n\nХод {step}. 🔴{player.username} зазевался и был оглушен, снова атакует 🔵{enemy.username}!'

        await db.DuelPool.filter(agressor=player.user_id).update(
                                                                react_until=time.time() + 10,
                                                                battle_log=battle_log,
                                                                current_turn='defender'
                                                                )

        await bot.edit_message_text(battle_log,
                                    enemy_msg.chat.id,
                                    enemy_msg.message_id,
                                    reply_markup=post_sleep_kb)
        await asyncio.sleep(.05)
        await call.message.edit_text(battle_log)
        
    await sleep_again(player.user_id, call, enemy_msg, step+1)

async def close_pool_by_loose(call, vic_msg, agressor, victim, looser, battle_log):

    greenZoneMin = int((agressor.atk + agressor.hp) * 0.7)
    greenZoneMax = int((agressor.atk + agressor.hp) * 0.84)
    yellowZoneMin = int((agressor.atk + agressor.hp) * 0.85)
    yellowZoneMax = int((agressor.atk + agressor.hp) * 1.14)
    redZoneMin = int((agressor.atk + agressor.hp) * 1.15)
    redZoneMax = int((agressor.atk + agressor.hp) * 1.3)
    
    if victim.atk + victim.hp in range(greenZoneMin, greenZoneMax+1): 
        agr_bonus = 1
        vic_bonus = 10
    elif victim.atk + victim.hp in range(yellowZoneMin, yellowZoneMax+1): 
        agr_bonus = 4
        vic_bonus = 4
    elif victim.atk + victim.hp in range(redZoneMin, redZoneMax+1):
        agr_bonus = 10
        vic_bonus = 1
    else:
        agr_bonus = 3
        vic_bonus = 3

    if looser == 'agressor':

        mi = int(agressor.money * 0.1)
        ma = int(agressor.money * 0.25)
        goldAward = random.randint(mi, ma)

        remain_player_hp = f'Удар 🔵{victim.username} стал для 🔴{agressor.username} последним.'
        await db.Users.filter(id=agressor.id).update(nowhp=1,
                                                    money=F('money') - goldAward,
                                                    slava=F('slava') - vic_bonus,
                                                    battleStatus=0,
                                                    progStatus=1,
                                                    location='Хэвенбург',
                                                    battleWith=0)
        await db.DuelPool.filter(agressor=agressor.user_id).delete()
        await db.Users.filter(id=victim.id).update(money=F('money') + goldAward,
                                                    slava=F('slava') + vic_bonus,
                                                    battleStatus=0,
                                                    progStatus=1,
                                                    battleWith=0)

        await bot.edit_message_text(f'{battle_log}\n\n{remain_player_hp} \n\n Получено: {goldAward}💰 {vic_bonus}🌟.', vic_msg.chat.id, vic_msg.message_id)
        await asyncio.sleep(.05)
        checkVictimKolt = await db.Inventory.get_or_none(name='Золотой кольт', active=2, idplayer=victim.id).first()
        if checkVictimKolt and checkVictimKolt.descr:
            await call.message.edit_text(f'{battle_log}\n\n{remain_player_hp}. Ты очухался в городе, потеряв {goldAward}💰. Последнее что ты запомнил - медленно приближающееся дуло к твоей голове и гравировку на оружии...\n\n{checkVictimKolt.descr}')
        else:
            await call.message.edit_text(f'{battle_log}\n\n{remain_player_hp}. Ты очухался в городе, потеряв {goldAward}💰.')
        
        del buzyUsrsPvP[call.from_user.id]
        del buzyUsrsPvP[victim.user_id]

        await achprog(victim, ach='pvpsher')

        return

    elif looser == 'victim':

        mi = int(victim.money * 0.1)
        ma = int(victim.money * 0.25)
        goldAward = random.randint(mi, ma)

        remain_enemy_hp = f'Удар 🔴{agressor.username} стал для 🔵{victim.username} последним.'
        await db.Users.filter(id=victim.id).update(nowhp=1,
                                                    money=F('money') - goldAward,
                                                    slava=F('slava') - agr_bonus,
                                                    battleStatus=0,
                                                    location='Хэвенбург',
                                                    battleWith=0)
        await db.DuelPool.filter(agressor=agressor.user_id).delete()
        await db.Users.filter(id=agressor.id).update(money=F('money') + goldAward,
                                                        slava=F('slava') + agr_bonus,
                                                        battleStatus=0,
                                                        battleWith=0)

        checkAgrKolt = await db.Inventory.get_or_none(name='Золотой кольт', active=2, idplayer=agressor.id).first()
        if checkAgrKolt and checkAgrKolt.descr:
            await bot.edit_message_text(f'{battle_log}\n\n{remain_enemy_hp} Ты очухался в городе, потеряв {goldAward}💰.\n. Последнее что ты запомнил - медленно приближающееся дуло к твоей голове и гравировку на оружии...\n\n{checkAgrKolt.descr}', vic_msg.chat.id, vic_msg.message_id)
        else:
            await bot.edit_message_text(f'{battle_log}\n\n{remain_enemy_hp} Ты очухался в городе, потеряв {goldAward}💰.', vic_msg.chat.id, vic_msg.message_id)
        await asyncio.sleep(.05)
        await call.message.edit_text(f'{battle_log}\n\n{remain_enemy_hp} Получено: {goldAward}💰 {agr_bonus}🌟.')
        
        del buzyUsrsPvP[call.from_user.id]
        del buzyUsrsPvP[victim.user_id]

        await achprog(agressor, ach='pvpsher')
        return