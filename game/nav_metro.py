async def nav_metro(call, user): 
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
        if (str(user.location) == "Метро") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Метро":
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
        if (str(user.location) == "Метро") and (str(user.position) != newPos):
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
        elif str(user.location) != "Метро":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Метро") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            await goToShop(call)
        elif str(user.location) != "Метро":
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
        if user.location == "Метро":
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
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_metro_kachalka"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_metro_onsen"), InlineKeyboardButton('👴Сидорович', callback_data="nav_metro_sidor"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_metro_hotel"), InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_metro_raskul"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_metro_exit"))
        text = "Площадь как площадь. Ведь площадь она и в Хэвенбурге площадь, верно? Знаешь как выглядят площади, так вот наша площадь практически такая же, как и все площади, что ты видел до неё. В общем, площадь, которая выглядит как площадь — вот она, наша площадь Метро."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Туннели метро"
                if user.location == "Метро":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                user.location = newLocation
                user.progStatus = 1
                user.battleStatus = 0
                user.progLoc = 'Туннели метро|0'
                await user.save()
                text = "Вы отправились в туннели метро"
                await bot.send_message(call.message.chat.id, text)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            elif navg == '2':
                if user.location == 'Метро':
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
                markup.add(InlineKeyboardButton('Туннели метро', callback_data="nav_metro_exit_1"))
                markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_metro_exit_2"))
                await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти", reply_markup=markup)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Туннели метро', callback_data="nav_metro_exit_1"))
            markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_metro_exit_2"))
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
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_metro_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Поддержка игры', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "raskul":
        text = "Удивившись, увидев старую знакомую (хотя для некоторых это - знакомый), вы зашли внутрь здания и оказались в Аукционном доме Раскуловой.\n\nТут вы можете выставить свои предметы на продажу, либо же приобрести предметы других игроков"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Покупка', callback_data="raskul_buy"))
        markup.add(InlineKeyboardButton('Продажа', callback_data="raskul_sell"))
        markup.add(InlineKeyboardButton('Мои лоты', callback_data="raskul_lots"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == 'sidor':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_metro_centr"))
        #checkIvent = await db.Inventory.exists(idplayer=user.id, name='Письмо для Табернам', active=1)
        checkIvent = None # Заглушка
        if checkIvent: # if not checkIvent
            await db.Inventory.filter(name='Письмо для Табернам', idplayer=user.id).update(active=0)
            await db.addItem('Письмо для Табервама', user, arg='1')
            text = "-Короче, {}. Я тебя спас и в благородство играть не буду... Принесёшь мне пару 🎣Простых удочек, и мы в расчёте. Заодно покажу тебе свой ассортимент, уж поверь, не пожалеешь!".format(user.username)
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            await metroshop(call, user)
            return
