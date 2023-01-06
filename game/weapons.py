async def weaponLvlUpNeed(user, item, lvl):
    passFirst = 'None'
    passSecond = 'None'
    passThird = 'None'
    if item == 'Пистолет с ножом':
        needItem1 = "🔪"
        cNeedItem1 = 15 + 3 * lvl
        count = await db.Inventory.filter(name='Как ни странно, нож', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        needItem2 = "📏"
        cNeedItem2 = 15 + 3 * lvl 
        count = await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        needItem3 = "🔗"
        cNeedItem3 = 20 + 2 * lvl 
        count = await db.Inventory.filter(name='Мягкий металлолом', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True

    elif item == 'Копьё':
        needItem1 = "🩹"
        cNeedItem1 = 19 + 3 * lvl
        count = await db.Inventory.filter(name='Металлический наконечник', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        needItem2 = "🪓"
        cNeedItem2 = 20 + 3 * lvl 
        count = await db.Inventory.filter(name='Древковый элемент', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        needItem3 = "✒️"
        cNeedItem3 = 23 + 2 * lvl 
        count = await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True

    elif item == 'Катана':
        needItem1 = "✒️"
        cNeedItem1 = 23 + 2 * lvl
        count = await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        needItem2 = "🗡"
        cNeedItem2 = 13 + 3 * lvl 
        count = await db.Inventory.filter(name='Лезвие', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        needItem3 = "⛓"
        cNeedItem3 = 22 + 2 * lvl 
        count = await db.Inventory.filter(name='Заточки', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True
    
    elif item == 'Меч':
        needItem1 = "📏"
        cNeedItem1 = 15 + 3 * lvl
        count = await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        needItem2 = "🪓"
        cNeedItem2 = 19 + 3 * lvl 
        count = await db.Inventory.filter(name='Древковый элемент', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        needItem3 = "⛓"
        cNeedItem3 = 15 + 3 * lvl 
        count = await db.Inventory.filter(name='Заточки', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True

    elif item == 'Кинжал вампира':
        needItem1 = "🔪"
        cNeedItem1 = 18 + 3 * lvl
        count = await db.Inventory.filter(name='Как ни странно, нож', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        print(passFirst)
        needItem2 = "✒️"
        cNeedItem2 = 23 + 2 * lvl 
        count = await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        print(passSecond)
        needItem3 = "🩹"
        cNeedItem3 = 19 + 3 * lvl 
        count = await db.Inventory.filter(name='Металлический наконечник', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True
        print(passThird)
    
    elif item == 'Кольт' or item == 'Золотой кольт':
        needItem1 = "📏"
        cNeedItem1 = 15 + 3 * lvl
        count = await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).count()
        if count >= cNeedItem1: passFirst = True
        print(passFirst)
        needItem2 = "✒️"
        cNeedItem2 = 23 + 2 * lvl 
        count = await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).count()
        if count >= cNeedItem2: passSecond = True
        print(passSecond)
        needItem3 = "🔗"
        cNeedItem3 = 20 + 2 * lvl 
        count = await db.Inventory.filter(name='Мягкий металлолом', idplayer=user.id, active=6).count()
        if count >= cNeedItem3: passThird = True
        print(passThird)


    if lvl < 9:
        if passFirst == True and passSecond == True and passThird == True: passKach = True
        else: passKach = False
    else:
        count = await db.Inventory.filter(name='Монета возвышения', idplayer=user.id, active=6).count()
        if lvl >= 14:
            if count >= 4: passUp = True
            else: passUp = None
        else:
            if count >= lvl - 9: passUp = True
            else: passUp = None
        if passFirst == True and passSecond == True and passThird == True and passUp: passKach = True
        else: passKach = False
    return needItem1, needItem2, needItem3, cNeedItem1, cNeedItem2, cNeedItem3, passKach

async def weaponLvlUp(user, item, lvl):
    if item == 'Пистолет с ножом':
        cNeedItem1 = 15 + 3 * lvl
        await db.Inventory.filter(name='Как ни странно, нож', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 15 + 3 * lvl 
        await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).limit(cNeedItem2).update(active=0)
        cNeedItem3 = 20 + 2 * lvl 
        await db.Inventory.filter(name='Мягкий металлолом', idplayer=user.id, active=6).limit(cNeedItem3).update(active=0)

    elif item == 'Копьё':
        cNeedItem1 = 19 + 3 * lvl
        await db.Inventory.filter(name='Металлический наконечник', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 20 + 3 * lvl 
        await db.Inventory.filter(name='Древковый элемент', idplayer=user.id, active=6).limit(cNeedItem2).update(active=0)
        cNeedItem3 = 23 + 2 * lvl 
        await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).limit(cNeedItem3).update(active=0)

    elif item == 'Катана':
        cNeedItem1 = 23 + 2 * lvl
        await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 13 + 3 * lvl 
        await db.Inventory.filter(name='Лезвие', idplayer=user.id, active=6).limit(cNeedItem2).update(active=0)
        cNeedItem3 = 22 + 2 * lvl 
        await db.Inventory.filter(name='Заточки', idplayer=user.id, active=6).limit(cNeedItem3).update(active=0)
    
    elif item == 'Меч':
        cNeedItem1 = 15 + 3 * lvl
        await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 19 + 3 * lvl 
        await db.Inventory.filter(name='Древковый элемент', idplayer=user.id, active=6).limit(cNeedItem2).update(active=0)
        cNeedItem3 = 15 + 3 * lvl 
        await db.Inventory.filter(name='Заточки', idplayer=user.id, active=6).limit(cNeedItem3).update(active=0)

    elif item == 'Кинжал вампира':
        cNeedItem1 = 18 + 3 * lvl
        await db.Inventory.filter(name='Как ни странно, нож', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 23 + 2 * lvl 
        await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).limit(cNeedItem2).update(active=0)
        cNeedItem3 = 19 + 3 * lvl 
        await db.Inventory.filter(name='Металлический наконечник', idplayer=user.id, active=6).limit(cNeedItem3).update(active=0)

    elif item == 'Кольт' or item == 'Золотой кольт':
        cNeedItem1 = 15 + 3 * lvl
        await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem2 = 23 + 2 * lvl 
        await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)
        cNeedItem3 = 20 + 2 * lvl 
        await db.Inventory.filter(name='Мягкий металлолом', idplayer=user.id, active=6).limit(cNeedItem1).update(active=0)






    if lvl > 9:
        if lvl >= 14:
            needCoin = 4
        else:
            needCoin = lvl - 9
        await db.Inventory.filter(name='Монета возвышения', idplayer=user.id, active=6).limit(needCoin).update(active=0)
    name, size, bonus, atk_block, expires = await db.items(item, check=True)
    await db.Inventory.filter(name=item, idplayer=user.id, active=2).update(lvl=F('lvl') + 1, bonus=F('bonus') + bonus)


async def weapon(m, user):
    if m.chat.id == m.from_user.id:
        if user:
            item = await db.Inventory.get_or_none(type='Оружие', idplayer=user.id, active=2).first()
            if not item: return await bot.send_message(m.chat.id, "У тебя нет оружия.")
            message = await bot.send_message(m.chat.id, "Получаю информацию...")
            if item.name == 'Пистолет с ножом':
                needItem1 = '🔪 Как ни странно, нож'
                needItem2 = '📏 Линеечка'
                needItem3 = '🔗 Мягкий металлолом'
                itemDescr = "Пистолет с ножом - связка, имеющая неплохой потенциал. Основным оружием служит нож, но в любой момент можно отскочить от противника и выстрелить в него, нанеся критический урон.\nОсобая способность: Выстрел. Способность наносит критический урон 150% (15% шанс нанести 175% урона)"
            elif item.name == 'Копьё':
                needItem1 = '🩹 Металлический наконечник'
                needItem2 = '🪓 Древковый элемент'
                needItem3 = '✒️ Противовес'
                itemDescr = "Копьё - отличное оружие, позволяющее наносить связки быстрых ударов. Одно из самых первых видов оружий мира, дошедших до нашего времени. Возможно кто-то из твоих предков убивал таким динозавров, а ты пошел по его стопам.\nОсобая способность: Серия ударов. Способность наносит три удара по 30% урона (шанс нанести 100% урона каждую атаку 30%)"
            elif item.name == 'Катана':
                needItem1 = '✒️ Противовес'
                needItem2 = '🗡 Лезвие'
                needItem3 = '⛓ Заточки'
                itemDescr = "Катана – похожий на саблю японский меч с изогнутым клинком, заточенный с одной стороны. Режущая часть сделана из нескольких видов стали, она одновременно прочная и острая, долго держит заточку. Доселе неизвестна технология изготовления, также как и где же эта Япония..\nОсобая способность: Рубящий удар. Возможность убить монстра с одного удара с шансом в 20%"
            elif item.name == 'Меч':
                needItem1 = '📏 Линеечка'
                needItem2 = '🪓 Древковый элемент'
                needItem3 = '⛓ Заточки'
                itemDescr = "Меч - полуторный прямой клинок заточенный с двух сторон, гарда сделана в форме креста. Таким можно наносить глубокие и болезненные порезы!\nОсобая способность: Выпад. Наносит 30% от максимального хп моба (25% шанс нанести 50% от максимального хп моба)"
            elif item.name == 'Кинжал вампира':
                needItem1 = '🔪 Как ни странно, нож'
                needItem2 = '✒️ Противовес'
                needItem3 = '🩹 Металлический наконечник'
                itemDescr = "Кинжал — холодное оружие с коротким (до 40 сантиметров) прямым клинком. Подходит для метания.\nОсобая способность: Кровожадное метание. При метании кинжала наносится обычный урон и срабатывает эффект вампиризма - от 25% до 50% от нанесённого урона"
            elif item.name == 'Кольт':
                needItem1 = '📏 Линеечка'
                needItem2 = '✒️ Противовес'
                needItem3 = '🔗 Мягкий металлолом'
                itemDescr = "Кольт - шестизарядный револьвер, был изготовлен старой школой охотников на монстров. Изящное оружие с титановыми корпусом и рукоятью из неизвестного дерева наводит страх на любую нечисть. Говорят, для использования этого оружия нужна большая удача."
            elif item.name == 'Золотой кольт':
                needItem1 = '📏 Линеечка'
                needItem2 = '✒️ Противовес'
                needItem3 = '🔗 Мягкий металлолом'
                itemDescr = "Золотой Кольт - элитный шестизарядный револьвер, созданный старой школой охотников на монстров и лучшими ювелирами Хэвенбурга.  Изящное оружие с золотым корпусом и рукоятью из красного дерева могут иметь только величайшие из героев Небесной башни.  Гравировка на оружии даёт поверженным врагам хорошо понять, кому они имели честь проиграть."
            else:
                await bot.edit_message_text("Ты беззащитен. Ходишь голышом. Возьми в руки оружие!", m.chat.id, message.message_id)
                return
            countFirst = await db.Inventory.filter(name='Как ни странно, нож', idplayer=user.id, active=6).only('id').count()
            countSecond = await db.Inventory.filter(name='Линеечка', idplayer=user.id, active=6).only('id').count()
            countThird = await db.Inventory.filter(name='Металлический наконечник', idplayer=user.id, active=6).only('id').count()
            countFourth = await db.Inventory.filter(name='Мягкий металлолом', idplayer=user.id, active=6).only('id').count()
            countFifth = await db.Inventory.filter(name='Противовес', idplayer=user.id, active=6).only('id').count()
            countSixth = await db.Inventory.filter(name='Древковый элемент', idplayer=user.id, active=6).only('id').count()
            countSeventh = await db.Inventory.filter(name='Лезвие', idplayer=user.id, active=6).only('id').count()
            countEight = await db.Inventory.filter(name='Заточки', idplayer=user.id, active=6).only('id').count()
            countNinght = await db.Inventory.filter(name='Монета возвышения', idplayer=user.id, active=6).only('id').count()
            needItem1, needItem2, needItem3, cNeedItem1, cNeedItem2, cNeedItem3, passKach = await weaponLvlUpNeed(user, item.name, item.lvl)
            if item.lvl > 9:
                if item.lvl >= 14:
                    needCoins = 4
                else:
                    needCoins = item.lvl - 9
                plusText = "x{} 🪙 Монета возвышения".format(needCoins)
            else:
                plusText = ""
            text = """Ваше текущее оружие: {}

{}

🔆Уровень: {}
🔪Бонус к атаке: {}%

Необходимо для улучшения:
x{} {}
x{} {}
x{} {}
{}

Доступные материалы улучшения:
x{} 🔪 Как ни странно, нож
x{} 📏 Линеечка
x{} 🩹 Металлический наконечник
x{} 🔗 Мягкий металлолом
x{} ✒️ Противовес
x{} 🪓 Древковый элемент
x{} 🗡 Лезвие
x{} ⛓ Заточки
x{} 🪙 Монета возвышения""".format(user.item, itemDescr, item.lvl, item.bonus, cNeedItem1, needItem1, cNeedItem2, needItem2, cNeedItem3, needItem3, plusText, countFirst, countSecond, countThird, countFourth, countFifth, countSixth, countSeventh, countEight, countNinght)

            today = datetime.datetime.today().strftime('%A')
            if today == 'Monday': items = '🔪, 🩹'
            elif today == 'Tuesday': items = '🔗, ✒️'
            elif today == 'Wednesday': items = '🔪, 🪓'
            elif today == 'Thursday': items = '🗡, 📏'
            elif today == 'Friday': items = '🩹, ⛓'
            elif today == 'Saturday': items = '🔗, 🗡'
            elif today == 'Sunday': items = '✒️, 📏'
            text += "\n\nНаграды сегодняшнего испытания: {}".format(items)

            markup = InlineKeyboardMarkup()
            markup.row_width = 2

            if passKach:
                markup.add(InlineKeyboardButton('Повысить уровень оружия', callback_data="weaponUp"))
            markup.add(InlineKeyboardButton('Телепортация в испытание', callback_data="tpWeaponFarm"))
            await bot.edit_message_text(text, m.chat.id, message.message_id, reply_markup=markup)

async def weaponUp(call, user):
    item = await db.Inventory.get_or_none(type='Оружие', active=2, idplayer=user.id).first()
    if item:
        needItem1, needItem2, needItem3, cNeedItem1, cNeedItem2, cNeedItem3, passKach = await weaponLvlUpNeed(user, item.name, item.lvl)
        print(passKach)
        if passKach == True:
            await weaponLvlUp(user, item.name, item.lvl)
            await bot.edit_message_text("Ты успешно прокачал уровень оружия.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Возникла ошибка. Возможно, у тебя не хватает предметов улучшения", call.message.chat.id, call.message.message_id)


async def tpWeaponFarm(call, user):
    if user.location in ['Хэвенбург', 'Город', 'Кавайня', 'Океанус']:
        await db.Users.filter(id=user.id).update(location='Испытание оружия', progLoc='Испытание оружия|0', progStatus=1, battleStatus=0)
        await bot.edit_message_text("Телепортируемся и начинаем испытание...\n\n⚡️Испытание занимает 10 ходов, в каждом из которых вам придётся сразиться с монстром и победить его. Сражение проходит автоматически", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Необходимо находиться в городе", call.message.chat.id, call.message.message_id)