async def nav_oceanus(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[2]
    if navWhere == "onsen":
        checkFrak = await db.Fraks.exists(name=user.frak)
        if checkFrak:
            await bot.edit_message_text("К сожалению, источники вам недоступны. Воспользуйтесь ими на базе клана.", call.message.chat.id, call.message.message_id)
            return
        newPos = "Источники"
        if (str(user.location) == "Океанус") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Океанус":
            text = "Ты находишься вне города."
        elif int(user.hp) <= int(user.nowhp):
            text = "_Послушай... Источники нужны для того, чтобы исцеляться, а не приходить сюда каждый раз только если бабу охота!_"
        elif str(user.position) == newPos:
            text = "Ты занимаешься *CENSORED*\nИсцеление проходит постепенно, нужно немного подождать"
        else:
            text = "Ошибка определителя. Location {} \n Hp/nowhp {}/{}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением в /report".format(str(user.location), str(user.nowhp), str(user.hp), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "hotel":
        checkFrak = await db.Fraks.exists(name=user.frak)
        if checkFrak:
            await bot.edit_message_text("К сожалению, отель вам недоступен. Воспользуйтесь ночлегом на базе клана.", call.message.chat.id, call.message.message_id)
            return
        newPos = "Отель"
        if (str(user.location) == "Океанус") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('Уйти', callback_data="hotel_return"))
            text = '_«Отель» он же бывший бордель, закрытый из-за нехватки работниц, конечно, выглядит лучше после смены владельца и ремонта, однако  запах его прошлой жизни останется здесь ещё надолго_'
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        elif str(user.location) != "Океанус":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Океанус") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            await goToShop(call)
        elif str(user.location) != "Океанус":
            text = "Вы находитесь вне города"
            await bot.send_message(call.message.chat.id, text)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif str(user.position) == newPos:
            text = "Ты уже в магазине."
            await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await goToShop(call)
    elif navWhere == "centr":
        newPos = "Площадь"
        if user.location == "Океанус":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.send_message(call.message.chat.id, text)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        newPos = "Площадь"
        user.position = newPos
        await user.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_oceanus_kachalka"), InlineKeyboardButton("👨‍🦱Фишелов", callback_data="nav_oceanus_fishelov"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_oceanus_onsen"), InlineKeyboardButton('🧕Табернам', callback_data="nav_oceanus_tabernam"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_oceanus_hotel"), InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_oceanus_raskul"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_oceanus_exit"))
        text = "Площадь как площадь. Ведь площадь она и в Хэвенбурге площадь, верно? Знаешь как выглядят площади, так вот наша площадь практически такая же, как и все площади, что ты видел до неё. В общем, площадь, которая выглядит как площадь — вот она, наша площадь Океануса."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Окус Локус"
                if user.location == "Океанус":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                user.location = newLocation
                user.progStatus = 1
                user.battleStatus = 0
                user.progLoc = 'Окус Локус|0'
                await user.save()
                text = "Вы отправились в Окус Локус"
                await bot.send_message(call.message.chat.id, text)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            elif navg == '2':
                if user.location == 'Океанус':
                    user.location = "Хэвенбург"
                    user.position = "Площадь"
                    user.battleStatus = 0
                    await user.save()
                    await bot.send_message(call.message.chat.id, "Вы телепортировались в Хэвенбург")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
            else:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Окус Локус', callback_data="nav_oceanus_exit_1"))
                markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_oceanus_exit_2"))
                await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти", reply_markup=markup)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Окус Локус', callback_data="nav_oceanus_exit_1"))
            markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_oceanus_exit_2"))
            await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти", reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "kachalka":
        atk = user.atk
        hp = user.hp
        needAtk = int(3 * ((atk - 4) / 2))
        needHp = int(3 * ((hp - 9) / 2))
        halfmoney = int(user.money / 2)
        text = "Штанги из палок и покрышек, тренажёры из палок и покрышек, дверь в здание из палок и покрышек... Да чего уж таить — само здание тоже из палок и покрышек. Разве что табличка «Самые современные и технологичные тренажёры на любой вкус и цвет!» сделана не из покрышек"
        text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(needAtk))
        if needAtk * 2 < halfmoney:
            text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
            if needAtk * 4 < user.money:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
        text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(needHp))
        if needHp * 2 < halfmoney:
            text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
            if needHp * 4 < user.money:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_bigcity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Поддержка игры', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "raskul":
        text = "Удивившись, увидев старую знакомую (хотя для некоторых это - знакомый), вы зашли внутрь здания и оказались в Аукционном доме Раскуловой.\n\nТут вы можете выставить свои предметы на продажу, либо же приобрести предметы других игроков"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Покупка', callback_data="raskul_buy"))
        markup.add(InlineKeyboardButton('Продажа', callback_data="raskul_sell"))
        markup.add(InlineKeyboardButton('Мои лоты', callback_data="raskul_lots"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "kitchen":
        text = "Кухня - удивительное место в этом городке. Только здесь ты можешь сделать себе еду сам. Правда, пока это место закрыто, а вывеска гласит что оно готовится к открытию."
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == 'tabernam':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_oceanus_centr"))
        checkIvent = await db.Inventory.exists(idplayer=user.id, name='Письмо для Табернам', active=1)
        if checkIvent:
            await db.Inventory.filter(name='Письмо для Табернам', idplayer=user.id).update(active=0)
            await db.addItem('Письмо для Табервама', user, arg='1')
            text = "-О, сыночек, опять ты... Ну не надоело тебе старую бабушку трогать по пустякам? Опять пришёл просто ''прицениться''? Я и так знаю что ты не купишь у меня ничего кроме гребанных тряпок...\n\nТы протянул бабульке письмо и забыл следующие десять минут своей жизни...\nПридя в себя, в руке у тебя оказалось новое письмо и просьба передать его Таберваму..."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            await oceanshop(call, user)
            return
    elif navWhere == 'fishelov':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        checkFish = await db.Inventory.exists(idplayer=user.id, active=1, type='Рыба')
        if not checkFish: return await bot.edit_message_text("А, ну-ка, что у тебя там по улову, давай посмотрим? А, так ты ничего не принёс? Ну так дуй в Окус Локус, ищи там Пруд и лови рыбу, или чего ты мне тут на мозги капаешь?", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Тааак, посмотрим что тут у тебя...", call.message.chat.id, call.message.message_id)
            allFish = await db.Inventory.filter(idplayer=user.id, active=1, type="Рыба")
            profit = 0
            for fish in allFish:
                if fish.name in ["Карась", "Бычок", "Окунь", "Тарань", "Сом"]: profit += random.randint(100, 200)
                elif fish.name in ["Судак", "Язь", "Щука", "Пиранья", "Сопа"]: profit += random.randint(300, 500)
                elif fish.name in ["Красноперка", "Осетр", "Форель", "Лосось"]: profit += random.randint(1000, 2000)
            await db.Inventory.filter(idplayer=user.id, active=1, type="Рыба").update(active=0)
            await logBot.send_message(tradeChat, "Игрок {} ({}) продал рыбы на {}💰".format(user.username, user.id, profit))
            await db.Users.filter(id=user.id).update(money=F('money') + profit)
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_oceanus_centr"))
        await bot.send_message(call.message.chat.id, "Неплохо, мне нравится, хороший улов! Держи {}💰, ты хорошо потрудился. Будет улов - заходи еще!".format(profit), reply_markup=markup)



async def fishilka(call, user):
    if user.location == 'Окус Локус' and user.progLoc == 'Окус Локус|10':
        await db.Users.filter(id=user.id).update(location='Пруд', progStatus=0)
        checkUdochka = await db.Inventory.get_or_none(idplayer=user.id, type='Рыбалка', active=2).first()
        if checkUdochka:
            await bot.edit_message_text("Напевая песенку под нос, достал удочку, смастерил наживку с того что было и начал рыбачить...\n\nРыбалка - место для усидчивых и быстро реагирующих рыбаков. Чем лучше удочка, тем больше шанс словить рыбу, которую можно будет продать подороже у 👨‍🦱Рыболова. Если рыба клюнет, у тебя будет 10 секунд чтобы среагировать и подсечь.", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Увы, у тебя нет удочки в снаряжении. Надень её через инвентарь.\n\nРыбалка - место для усидчивых и быстро реагирующих рыбаков. Чем лучше удочка, тем больше шанс словить рыбу, которую можно будет продать подороже у 👨‍🦱Рыболова. Если рыба клюнет, у тебя будет 10 секунд чтобы среагировать и подсечь.", call.message.chat.id, call.message.message_id)


async def endFishing(call, user):
    if user.location == 'Пруд':
        await db.Users.filter(id=user.id).update(location='Окус Локус', progStatus=1)
        await bot.edit_message_text("Рыбалка окончена. Возвращаемся в Окус Локус...", call.message.chat.id, call.message.message_id)


async def catchFish(call, user):
    if user.location == 'Пруд':
        if call.message.date.timestamp() + 20 < int(time.time()): return await bot.edit_message_text("Клёв упущен!", call.message.chat.id, call.message.message_id)
        udochka = await db.Inventory.get_or_none(idplayer=user.id, type='Рыбалка', active=2).first()
        if udochka:
            if udochka.name == "Простая удочка":
                chance1 = 70
                chance2 = 100
                chance3 = 1000
            elif udochka.name == "Непростая удочка":
                chance1 = 60
                chance2 = 95
                chance3 = 100
            elif udochka.name == "Очень непростая удочка":
                chance1 = 50
                chance2 = 90
                chance3 = 100
            elif udochka.name == "Весьма непростая удочка":
                chance1 = 30
                chance2 = 80
                chance3 = 100

            rand = random.randint(0, 100)
            if rand <= chance1:
                fish = random.choice(["Карась", "Бычок", "Окунь", "Тарань", "Сом"])
                await db.Users.filter(id=user.id).update(fisher=F('fisher') + 1)
            elif rand <= chance2:
                fish = random.choice(["Судак", "Язь", "Щука", "Пиранья", "Сопа"])
                await db.Users.filter(id=user.id).update(fisher=F('fisher') + 2)
            elif rand <= chance3:
                fish = random.choice(["Красноперка", "Осетр", "Форель", "Лосось"])
                await db.Users.filter(id=user.id).update(fisher=F('fisher') + 3)

            success = await db.addItem(fish, user)
            name, size, bonus, atk_block, expires = await db.items(fish, check=True)
            if success:
                await bot.edit_message_text("Оп-па! А вот и улов! Да это же {}!".format(name), call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("Оп-па! А вот и улов! Да это же {}! Жаль, места в инвентаре не хватает, так бы и забрал...".format(name), call.message.chat.id, call.message.message_id)
            await achprog(user, ach='fishing')
            await logBot.send_message(tradeChat, f"Игрок {user.username} словил {name}")
        else:
            await bot.edit_message_text("Ну и куда? Без удочки-то? Что у тебя там клюнуло, вот скажи мне?", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Ну и куда? Что у тебя там клюнуло, вот скажи мне? Ты даже не возле Пруда!", call.message.chat.id, call.message.message_id)