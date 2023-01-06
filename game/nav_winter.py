async def nav_wintercity(call, user): 
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
        if (str(user.location) == "Кавайня") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Кавайня":
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
        if (str(user.location) == "Кавайня") and (str(user.position) != newPos):
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
        elif str(user.location) != "Кавайня":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Кавайня") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            await goToShop(call)
        elif str(user.location) != "Кавайня":
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
        if user.location == "Кавайня":
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
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_wintercity_kachalka"), InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_wintercity_onsen"), InlineKeyboardButton('👨‍🦲Лысый из Брузерс', callback_data="wintershop"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_wintercity_hotel"), InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_wintercity_raskul"))
        markup.add(InlineKeyboardButton('🥃Элитный бар', callback_data="nav_wintercity_bar"), InlineKeyboardButton('📠Принтер', callback_data="nav_wintercity_printer"))
        if user.scenario == 5 and user.scenarioStatus in [1, 2, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15] or user.scenario == 6:
            markup.add(InlineKeyboardButton('👨‍🚀Осведомитель', callback_data="nav_wintercity_osved"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_wintercity_exit"))
        text = "Покрытые снегом крыши домов и деревья придают площади Кавайни настолько магический вид что невольно начинаешь верить в красоты природы. Еще и в окнах домиков видно тёплые огоньки, будто приглашающие тебя зайти внутрь и погреться... \n\n-Ха, тоже мне, красоты, - пробормотал ты, вспоминая игру ''64''..."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Заснеженный лес"
                if user.location == "Кавайня":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                user.location = newLocation
                user.progStatus = 1
                user.battleStatus = 0
                user.progLoc = 'Заснеженный лес|0'
                await user.save()
                text = "Вы отправились в Заснеженный лес"
                await bot.send_message(call.message.chat.id, text)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            elif navg == '2':
                if user.location == 'Кавайня':
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
            elif navg == 'hr':
                if user.location == 'Кавайня':
                    user.location = "Свалка HR"
                    user.progStatus = 1
                    user.battleStatus = 0
                    user.progLoc = 'Свалка HR|0'
                    await user.save()
                    text = "Вы отправились на Свалку HR"
                    await bot.send_message(call.message.chat.id, text)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
            elif navg == 'hd':
                if user.location == 'Кавайня':
                    user.location = "Свалка HD"
                    user.progStatus = 1
                    user.battleStatus = 0
                    user.progLoc = 'Свалка HD|0'
                    await user.save()
                    text = "Вы отправились на Свалку HD"
                    await bot.send_message(call.message.chat.id, text)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
            elif navg == 'fl':
                if user.location == 'Кавайня':
                    user.location = "Свалка FL"
                    user.progStatus = 1
                    user.battleStatus = 0
                    user.progLoc = 'Свалка FL|0'
                    await user.save()
                    text = "Вы отправились на Свалку FL"
                    await bot.send_message(call.message.chat.id, text)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Заснеженный лес', callback_data="nav_wintercity_exit_1"))
                markup.add(InlineKeyboardButton('Свалка HR', callback_data="nav_wintercity_exit_hr"))
                markup.add(InlineKeyboardButton('Свалка HD', callback_data="nav_wintercity_exit_hd"))
                markup.add(InlineKeyboardButton('Свалка FL', callback_data="nav_wintercity_exit_fl"))
                markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_wintercity_exit_2"))
                await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти\nЗаснеженный лес - стандартная локация Кавайни\n\nСвалка HR - каждый квадрат вам попадается случайный монстр, бьющий на 30% сильнее. +15%✨💰\nСвалка HD - каждый квадрат вам попадается случайный монстр, но вы не можете узнать показатель своего здоровья. +20%✨💰\nСвалка FL - каждый квадрат вам попадается случайный монстр, но вы не знаете его имени. +10%✨💰", reply_markup=markup)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Заснеженный лес', callback_data="nav_wintercity_exit_1"))
            markup.add(InlineKeyboardButton('Свалка HR', callback_data="nav_wintercity_exit_hr"))
            markup.add(InlineKeyboardButton('Свалка HD', callback_data="nav_wintercity_exit_hd"))
            markup.add(InlineKeyboardButton('Свалка FL', callback_data="nav_wintercity_exit_fl"))
            markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_wintercity_exit_2"))
            await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти\nЗаснеженный лес - стандартная локация Кавайни\n\nСвалка HR - каждый квадрат вам попадается случайный монстр, бьющий на 30% сильнее. +15%✨💰\nСвалка HD - каждый квадрат вам попадается случайный монстр, но вы не можете узнать показатель своего здоровья. +20%✨💰\nСвалка FL - каждый квадрат вам попадается случайный монстр, но вы не знаете его имени. +10%✨💰", reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "kachalka":
        atk = user.atk
        hp = user.hp
        needAtk = int(3 * ((atk - 4) / 2))
        needHp = int(3 * ((hp - 9) / 2))
        text = "Штанги из палок и покрышек, тренажёры из палок и покрышек, дверь в здание из палок и покрышек... Да чего уж таить — само здание тоже из палок и покрышек. Разве что табличка «Самые современные и технологичные тренажёры на любой вкус и цвет!» сделана не из покрышек\nУлучшить навык 💢Атака - {}💰 /kach_atk\nУлучшить навык ❤️Здоровье - {}💰 /kach_hp\n".format(str(needAtk), str(needHp))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_wintercity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Поддержка игры', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "raskul":
        checkQuest = await db.Quests.get_or_none(name='Богиня Хэвенбурга', idplayer=user.id).first()
        if checkQuest and checkQuest.status==2:

            text = "Удивившись, увидев старую знакомую (хотя для некоторых это - знакомый), вы зашли внутрь здания и оказались в Аукционном доме Раскуловой.\n\nТут вы можете выставить свои предметы на продажу, либо же приобрести предметы других игроков"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Покупка', callback_data="raskul_buy"))
            markup.add(InlineKeyboardButton('Продажа', callback_data="raskul_sell"))
            markup.add(InlineKeyboardButton('Мои лоты', callback_data="raskul_lots"))
            markup.add(InlineKeyboardButton('Рынок 💎', callback_data="raskul_kriMarket"))
            if user.location == "Хэвенбург":
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
            elif user.location == 'Кавайня':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_centr"))
            elif user.location == 'Океанус':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_oceanus_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await call.answer()

        elif checkQuest and checkQuest.status == 1:
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
        elif checkQuest and checkQuest.status == 2:
            await raskulova(call, user)

        else:
            plusText = await giveQuest(user, 'Богиня Хэвенбурга')
            await bot.edit_message_text("Подойдя к входной двери, охрана остановила тебя, спросив допуск. К счастью, мимо проходила весьма сексуальная девица, которая заинтересовалась тобой, отвела в сторону и предложила обмен - ты ей приносишь нижнее бельё, а она открывает тебе доступ к этому заведению. Конечно же ты согласился.\n-Кстати, можешь называть меня Раскуловой. Жду тебя внутри с одеждой.{}".format(plusText), call.message.chat.id, call.message.message_id)
    elif navWhere == "bar":
        checkQuest = await db.Quests.get_or_none(name='Элитный бар для элиты', idplayer=user.id).first()
        if checkQuest and checkQuest.status == 2:
            checkitem = await db.Inventory.exists(name='Первый заход в элитный бар', idplayer=user.id)
            if checkitem:
                text = "Подходя к светлому зданию, над которым висит позолоченная табличка, ты едва смог прочесть ''Бар''. О, даже сюда дошли... Ну, пора выпить!"
            else:
                await db.addItem('Первый заход в элитный бар', user, arg='1')
                checkitem = await db.Inventory.get(name='Первый заход в элитный бар', idplayer=user.id).first()
                checkitem.active = 0
                await checkitem.save()
                text = "Подходя к светлому зданию, над которым висит позолоченная табличка, ты едва смог прочесть ''Бар''. О, даже сюда дошли... Ну, пора выпить!"
                text += "\n\n\nЗайдя в бар, ты увидел нечто удивительное. Внутри... было чисто! Правда, видно старый автомат, как в Хэвенбурге, зато бармен другой... На деньги тут, гляжу, тоже играют и даже есть что-то новенькое - можно играть втроем? Неплохо... Стоп... ЭТОТ ОХРАННИК ПРЕСЛЕДУЕТ МЕНЯ?"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Заказать выпить (20💰)', callback_data="bar_drink"))
            markup.add(InlineKeyboardButton('Подойти к охраннику', callback_data="bar_ohr"))
            markup.add(InlineKeyboardButton('Двойные ставки', callback_data="bar_coin"))
            markup.add(InlineKeyboardButton('Тройные ставки', callback_data="bar_jackpot"))
            markup.add(InlineKeyboardButton('Игровой автомат', callback_data="bar_avto"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await call.answer()
        elif checkQuest and checkQuest.status == 1:
            count = user.kawaiCurrency
            if count >= 100:
                checkQuest.status = 2
                await checkQuest.save()
                await bot.edit_message_text("Отдав снунцы, охранники вдруг начали смотреть на тебя не как на грязь из-под ботинка и открыли дверь в бар. Вау!\n⚠️Получен доступ в 🥃Элитный бар + 1000 💰", call.message.chat.id, call.message.message_id)
                await db.Users.filter(id=user.id).update(money=F('money') + 1000, kawaiCurrency=F('kawaiCurrency') - 100)
            else:
                await bot.edit_message_text("Боюсь, без сотни снунцов сюда не зайти...", call.message.chat.id, call.message.message_id)
        else:
            plusText = await giveQuest(user, 'Элитный бар для элиты')
            await bot.edit_message_text("Подходя к бару, тебя остановила охрана... Неужели и тут за трусами бегать придётся...\nК счастью, нет. Вступительный взнос на посещение бара - 100🧊 Снунцов{}".format(plusText), call.message.chat.id, call.message.message_id)

    elif navWhere == 'printer':
        text = "📠Принтер - удивительное творение, привезённое из далёкого Осириса. Когда-то один из величайших путешественников нашёл этот механизм и продал за огромные деньги Кавайне. Теперь это местная достопримечательность, а что самое главное - механизм, позволяющий улучшать некоторые предметы или создавать новые."
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Создание предметов', callback_data="printer_create"))
        markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="printer_upgrade"))
        markup.add(InlineKeyboardButton('Вернуться на площадь', callback_data="nav_wintercity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif navWhere == 'osved':
        await scenarioSecond(call, user)


async def winterkach_(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    if kach == 'atk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if user.location == "Кавайня":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        if (user.money - needAtk) >= 0:
            user.atk = user.atk + 1
            user.money = user.money - needAtk
            await user.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(user.atk), str(user.money), str(_needAtk), str(_needHp))
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💢 Атака улучшена")                
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="winterkach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="winterkach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            closeLog = -1001305857653
            await bot.send_message(closeLog, "{} купил +1 атаки".format(user.username))
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не хватает золота")                
    elif kach == 'hp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.location == "Кавайня":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        if (user.money - needHp) >= 0:
            user.hp = user.hp + 1
            user.nowhp = user.nowhp + 1
            user.money = user.money - needHp
            await user.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(user.atk), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="winterkach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="winterkach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="❤️Здоровье улучшено")                
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            closeLog = -1001305857653
            await bot.send_message(closeLog, "{} купил +1 хп".format(user.username))
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не хватает золота")                




async def printer_(call, user):
    nav = call.data.split("_")[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if nav == 'upgrade':
        text = """Соединяя три одинаковых предметов, вы получаете повышение уровня основного. При выборе необходимого улучшения основным предметом выступает артефакт наивысшего уровня. При этом предметы не должны использоваться, а находиться в инвентаре.
Возможные улучшения на данный момент:

🔷Осколок энергии
🔷Камень энергии
🔥Осколок огня
🍯Горшок лепрекона
🔶Амулет здоровья
💍Кольцо всеотражения
🌿Карманная дриада
🟧Осколок эфира"""
        checkArt = await db.Inventory.filter(name='Осколок энергии', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🔷Осколок энергии', callback_data="upgradeArt_1"))
        
        checkArt = await db.Inventory.filter(name='Камень энергии', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🔷Камень энергии', callback_data="upgradeArt_2"))
        
        checkArt = await db.Inventory.filter(name='Осколок огня', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🔥Осколок огня', callback_data="upgradeArt_3"))
        
        checkArt = await db.Inventory.filter(name='Горшок лепрекона', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🍯Горшок лепрекона', callback_data="upgradeArt_4"))
        
        checkArt = await db.Inventory.filter(name='Амулет здоровья', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🔶Амулет здоровья', callback_data="upgradeArt_5"))
        
        checkArt = await db.Inventory.filter(name='Кольцо всеотражения', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 💍Кольцо всеотражения', callback_data="upgradeArt_6"))
        
        checkArt = await db.Inventory.filter(name='Карманная дриада', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🌿Карманная дриада', callback_data="upgradeArt_7"))
        
        checkArt = await db.Inventory.filter(name='Осколок эфира', idplayer=user.id, active=1).count()
        if checkArt >= 3:
            markup.add(InlineKeyboardButton('Улучшить: 🟧Осколок эфира', callback_data="upgradeArt_8"))
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))

    elif nav == "create":
        text = "Доступные рецепты:\n\n"
        text += "\n📜Свиток телепортации (Телепортирует в Хэвенбург) - Бумага + Чернила"
        checkItem1 = await db.Inventory.exists(name='Бумага', idplayer=user.id, active=1)
        checkItem2 = await db.Inventory.exists(name='Чернила', idplayer=user.id, active=1)
        if checkItem1 and checkItem2:
            markup.add(InlineKeyboardButton('Создать 📜Свиток телепортации', callback_data="createItem_1"))
        text += "\n🧪Зелье сопротивления холоду (повышает устойчивость на 20%) - Лёд + Ёмкость для жидкости"
        checkItem1 = await db.Inventory.exists(name='Лёд', idplayer=user.id, active=1)
        checkItem2 = await db.Inventory.exists(name='Ёмкость для жидкости', idplayer=user.id, active=1)
        if checkItem1 and checkItem2:
            markup.add(InlineKeyboardButton('Создать 🧪Зелье сопротивления холоду', callback_data="createItem_2"))
        text += "\n🧪Зелье сопротивления влажности (повышает устойчивость на 20%) - Телесные жидкости + Ёмкость для жидкости"
        checkItem1 = await db.Inventory.exists(name='Телесные жидкости', idplayer=user.id, active=1)
        checkItem2 = await db.Inventory.exists(name='Ёмкость для жидкости', idplayer=user.id, active=1)
        if checkItem1 and checkItem2:
            markup.add(InlineKeyboardButton('Создать 🧪Зелье сопротивления влажности', callback_data="createItem_3"))
        text += "\n🧪Зелье цепной молнии (С некоторым шансом оружие испускает заряд молнии и уничтожает монстра) - Немного магии + Ёмкость для жидкости"
        checkItem1 = await db.Inventory.exists(name='Немного магии', idplayer=user.id, active=1)
        checkItem2 = await db.Inventory.exists(name='Ёмкость для жидкости', idplayer=user.id, active=1)
        if checkItem1 and checkItem2:
            markup.add(InlineKeyboardButton('Создать 🧪Зелье цепной молнии', callback_data="createItem_4"))
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))

    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)




async def createItem_(call, user):
    nav = call.data.split("_")[1]
    if user.location == 'Кавайня':
        if nav == '1':
            checkItem1 = await db.Inventory.get_or_none(name='Бумага', idplayer=user.id, active=1).first()
            checkItem2 = await db.Inventory.get_or_none(name='Чернила', idplayer=user.id, active=1).first()
            if checkItem1 and checkItem2:
                checkItem1.active = 0
                checkItem2.active = 0
                await checkItem1.save()
                await checkItem2.save()
                success = await db.addItem('Свиток телепортации', user)
                text = "Ты успешно создал 📜Свиток телепортации!"
            else:
                text = "Убедись что у тебя хватает предметов! Необходимо: Бумага + Чернила"
        elif nav == '2':
            checkItem1 = await db.Inventory.get_or_none(name='Лёд', idplayer=user.id, active=1).first()
            checkItem2 = await db.Inventory.get_or_none(name='Ёмкость для жидкости', idplayer=user.id, active=1).first()
            if checkItem1 and checkItem2:
                checkItem1.active = 0
                checkItem2.active = 0
                await checkItem1.save()
                await checkItem2.save()
                success = await db.addItem('Зелье сопротивления холоду', user)
                text = "Ты успешно создал 🧪Зелье сопротивления холоду!"
            else:
                text = "Убедись что у тебя хватает предметов! Необходимо: Лёд + Ёмкость для жидкости"
        elif nav == '3':
            checkItem1 = await db.Inventory.get_or_none(name='Телесные жидкости', idplayer=user.id, active=1).first()
            checkItem2 = await db.Inventory.get_or_none(name='Ёмкость для жидкости', idplayer=user.id, active=1).first()
            if checkItem1 and checkItem2:
                checkItem1.active = 0
                checkItem2.active = 0
                await checkItem1.save()
                await checkItem2.save()
                success = await db.addItem('Зелье сопротивления влажности', user)
                text = "Ты успешно создал 🧪Зелье сопротивления влажности!"
            else:
                text = "Убедись что у тебя хватает предметов! Необходимо: Телесные жидкости + Ёмкость для жидкости"
        elif nav == '4':
            checkItem1 = await db.Inventory.get_or_none(name='Немного магии', idplayer=user.id, active=1).first()
            checkItem2 = await db.Inventory.get_or_none(name='Ёмкость для жидкости', idplayer=user.id, active=1).first()
            if checkItem1 and checkItem2:
                checkItem1.active = 0
                checkItem2.active = 0
                await checkItem1.save()
                await checkItem2.save()
                success = await db.addItem('Зелье цепной молнии', user)
                text = "Ты успешно создал 🧪Зелье цепной молнии!"
            else:
                text = "Убедись что у тебя хватает предметов! Необходимо: Телесные жидкости + Ёмкость для жидкости"
        else:
            text = "Странная ошибочка, попробуй еще раз!"
    else:
        text = "Ты находишься вне города"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('📠Принтер', callback_data="nav_wintercity_printer"))
    markup.add(InlineKeyboardButton('На площадь', callback_data="nav_wintercity_centr"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)



async def upgradeArt_(call, user):
    if user.location == 'Кавайня':
        nav = call.data.split("_")[1]
        items = {'1': 'Осколок энергии', '2': 'Камень энергии', '3': 'Осколок огня', '4': 'Горшок лепрекона', '5': 'Амулет здоровья', '6': 'Кольцо всеотражения', '7': 'Карманная дриада', '8': 'Осколок эфира'}
        if nav in items and items[nav]:
            checkArt = await db.Inventory.filter(name=items[nav], idplayer=user.id, active=1).count()
            if checkArt >= 3:
                allArts = await db.Inventory.filter(name=items[nav], idplayer=user.id, active=1).order_by('-lvl').limit(3)
                num = 0
                for z in allArts:
                    if num == 0:
                        nowLvl = z.lvl
                        await db.Inventory.filter(id=z.id).update(lvl=F('lvl') + 1)
                        num += 1
                    else:
                        await db.Inventory.filter(id=z.id).update(active=0)
                await bot.edit_message_text("Ты успешно повысил уровень предмета", call.message.chat.id, call.message.message_id)
            else:
                await bot.send_message(call.message.chat.id, "У тебя не хватает предметов.")
