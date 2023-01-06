async def navigation(m, user):
    #tp[m.from_user.id] = 2

    markup = InlineKeyboardMarkup(row_width=2)

    go_further = InlineKeyboardButton('Идти дальше', callback_data="navgo")
    go_further2 = InlineKeyboardButton('Остановиться', callback_data="navstop")
    go_back = InlineKeyboardButton('Идти назад', callback_data="navback")
    end_fishing = InlineKeyboardButton('Закончить рыбалку', callback_data="endFishing")

    clanBase_onsen = InlineKeyboardButton('⛲️Источники', callback_data="nav_base_onsen")
    clanBase_centr = InlineKeyboardButton('🏡Сад', callback_data="nav_base_centr")
    clanBase_hotel = InlineKeyboardButton('🏫Ночлег', callback_data="nav_base_hotel")
    clanBase_exitToHeaven = InlineKeyboardButton('🐾Путь в Хэвенбург', callback_data="nav_base_exitHeaven")
    clanBase_exitToTower = InlineKeyboardButton('🐾Путь к башне', callback_data="nav_base_exitTower")
    clanBase_security = InlineKeyboardButton('🛡Охрана базы', callback_data="nav_base_security")
    clanBase_krazha = InlineKeyboardButton('👣Налёт на клан', callback_data="nav_base_krazha")


    healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen")
    shop_go = InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop")
    hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel")
    centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr")
    gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_city_kachalka")
    arsenal_go = InlineKeyboardButton('⚔️Арсенал', callback_data="nav_city_arsenal")
    leaveTown = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start")
    lombard_go = InlineKeyboardButton('🏦Ломбард', callback_data="nav_city_lombard")

    heaven_healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen")
    heaven_hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel")
    heaven_centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr")
    heaven_gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_bigcity_kachalka")
    heaven_raskulova_go = InlineKeyboardButton("👩‍💼Раскулова", callback_data="nav_bigcity_raskul")
    heaven_lombard_go = InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard")
    heaven_trades_go = InlineKeyboardButton('⚖️Трейды', callback_data="nav_bigcity_trades")
    heaven_pub_go = InlineKeyboardButton('🥃Бар', callback_data="nav_bigcity_bar")
    heaven_dragonshop_go = InlineKeyboardButton('👺Драконоборец', callback_data="defShop")
    heaven_bomj_go = InlineKeyboardButton('👨🏾‍🦳Бомж', callback_data="nav_bigcity_skupshik")
    heaven_arsenal_go = InlineKeyboardButton('⚔️Арсенал', callback_data="nav_bigcity_arsenal")
    heaven_doska = InlineKeyboardButton('📋Доска ДВП', callback_data="dvp")
    #heaven_doska = InlineKeyboardButton('🏭Тошен', callback_data="nav_bigcity_toshen")
    heaven_hideSeek = InlineKeyboardButton('😈Дом Адского', callback_data="nav_bigcity_hns")
    leaveHeaven = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit")

    winter_healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_wintercity_onsen")
    winter_hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_wintercity_hotel")
    winter_gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_wintercity_kachalka")
    winter_bar_go = InlineKeyboardButton('🥃Элитный бар', callback_data="nav_wintercity_bar")
    winter_brazzzershop_go = InlineKeyboardButton('👨‍🦲Лысый из Брузерс', callback_data="wintershop")
    winter_centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_wintercity_centr")
    winter_printer_go = InlineKeyboardButton('📠Принтер', callback_data="nav_wintercity_printer")
    winter_osved_go = InlineKeyboardButton('👨‍🚀Осведомитель', callback_data="nav_wintercity_osved")
    leaveWinter = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_wintercity_exit")


    ocean_healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_oceanus_onsen")
    ocean_hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_wintercity_hotel")
    ocean_gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_oceanus_kachalka")
    ocean_shop_go = InlineKeyboardButton('🧕Табернам', callback_data="nav_oceanus_tabernam")
    ocean_centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_oceanus_centr")
    ocean_fish_go = InlineKeyboardButton('👨‍🦱Фишелов', callback_data="nav_oceanus_fishelov")
    leaveocean = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_oceanus_exit")
    
    radar_healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_radar_onsen")
    radar_hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_radar_hotel")
    radar_gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_radar_kachalka")
    radar_shop_go = InlineKeyboardButton('🕺Табервам', callback_data="nav_radar_tabervam")
    radar_alchemy_go = InlineKeyboardButton('🧛🏻‍♂️Сыч', callback_data="sich")
    radar_centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_radar_centr")
    leaveradar = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_radar_exit")
    

    metro_healer_go = InlineKeyboardButton('⛲️Источники', callback_data="nav_metro_onsen")
    metro_hotel_go = InlineKeyboardButton('🏫Отель', callback_data="nav_metro_hotel")
    metro_gym_go = InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_metro_kachalka")
    metro_shop_go = InlineKeyboardButton('👴Сидорович', callback_data="nav_metro_sidor")
    metro_centre_go = InlineKeyboardButton('🏣Площадь', callback_data="nav_metro_centr")
    leavemetro = InlineKeyboardButton('🏜Покинуть город', callback_data="nav_metro_exit")


    camp_npc1 = InlineKeyboardButton('🧕Аделаида', callback_data="camp_npc_1")
    camp_npc2 = InlineKeyboardButton('👷🏽‍♀️Муждан', callback_data="camp_npc_2")
    camp_npc3 = InlineKeyboardButton('🧕Клара', callback_data="camp_npc_3")
    camp_npc4 = InlineKeyboardButton('👳🏼‍♀️Нуббито', callback_data="camp_npc_4")
    camp_npc5 = InlineKeyboardButton('👳🏼Антонио', callback_data="camp_npc_5")
    camp_npc6 = InlineKeyboardButton('👳🏼‍♂️Старикашка', callback_data="camp_npc_6")
    camp_npc7 = InlineKeyboardButton('👨🏻‍🌾Урыл', callback_data="camp_npc_7")


    if user.location == 'Неизвестный лагерь':
        markup.add(camp_npc1, camp_npc2)
        markup.add(camp_npc3, camp_npc4)
        markup.add(camp_npc5, camp_npc6)
        markup.add(camp_npc7)
        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)

    elif user.location == "Город":
        if user.position in ["Ворота", "Источники"]:
            markup.add(healer_go)
            markup.add(shop_go)
            markup.add(hotel_go)
            markup.add(centre_go)
            markup.add(leaveTown)

        elif user.position == "Магазин":
            markup.add(shop_go)
            markup.add(healer_go)
            markup.add(hotel_go)
            markup.add(centre_go)
            markup.add(leaveTown)

        elif user.position == "Отель":
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(healer_go)
            markup.add(shop_go)
            markup.add(centre_go)
            markup.add(leaveTown)

        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(healer_go)
            markup.add(shop_go)
            markup.add(centre_go)
            markup.add(leaveTown)

        elif user.position == "Площадь":
            markup.add(gym_go)
            markup.add(healer_go)
            markup.add(shop_go)
            markup.add(hotel_go)
            markup.add(arsenal_go)
            markup.add(lombard_go)
            markup.add(leaveTown)

        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)

    elif user.location == 'Большой город':
        return

    elif user.location == 'Хэвенбург':

        if user.position == "Ворота":
            markup.add(heaven_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(heaven_hotel_go)
            markup.add(heaven_centre_go)
            markup.add(leaveHeaven)

        elif user.position == "Источники":
            markup.add(heaven_raskulova_go)
            markup.add(heaven_hotel_go)
            markup.add(heaven_centre_go)
            markup.add(leaveHeaven)

        elif user.position == "Отель":
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(heaven_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(heaven_centre_go)
            markup.add(leaveHeaven)

        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(heaven_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(heaven_centre_go)
            markup.add(leaveHeaven)

        elif user.position in ["Площадь", "Бар"]:
            markup.add(heaven_gym_go, heaven_lombard_go)
            markup.add(heaven_trades_go, heaven_pub_go)
            markup.add(heaven_healer_go, heaven_raskulova_go)
            markup.add(heaven_hotel_go, heaven_bomj_go)
            markup.add(heaven_dragonshop_go, heaven_doska)
            markup.add(heaven_hideSeek)
            markup.add(leaveHeaven)

        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)

    elif user.location == 'Кавайня':

        if user.position == "Ворота":
            markup.add(heaven_raskulova_go)
            markup.add(winter_healer_go)
            markup.add(winter_hotel_go)
            markup.add(winter_centre_go)
            markup.add(leaveWinter)

        elif user.position == "Источники":
            markup.add(heaven_raskulova_go)
            markup.add(winter_hotel_go)
            markup.add(winter_centre_go)
            markup.add(leaveWinter)

        elif user.position == "Отель":            
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(winter_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(winter_centre_go)
            markup.add(leaveWinter)

        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(winter_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(winter_centre_go)
            markup.add(leaveWinter)

        elif user.position == "Площадь":
            markup.add(winter_gym_go, heaven_lombard_go)
            markup.add(winter_healer_go, heaven_raskulova_go)
            markup.add(winter_hotel_go, winter_brazzzershop_go)
            markup.add(winter_bar_go, winter_printer_go)
            print(user.scenario)
            print(user.scenarioStatus)
            if user.scenario == 5 and user.scenarioStatus in [1, 2, 4, 5, 7, 8, 9, 10, 11]:
                markup.add(winter_osved_go)
            markup.add(leaveWinter)

        elif user.position == "Магазин":
            markup.add(heaven_raskulova_go)
            markup.add(winter_hotel_go)
            markup.add(winter_centre_go)
            markup.add(leaveWinter)

        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)

    elif user.location == 'Океанус':
        
        if user.position == "Источники":
            markup.add(heaven_raskulova_go)
            markup.add(ocean_healer_go)
            markup.add(ocean_centre_go)
            markup.add(leaveocean)

        elif user.position == "Отель":
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(ocean_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(ocean_centre_go)
            markup.add(leaveocean)
        
        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(ocean_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(ocean_centre_go)
            markup.add(leaveocean)

        elif user.position == "Площадь":
            markup.add(ocean_gym_go, ocean_fish_go)
            markup.add(ocean_healer_go, ocean_shop_go)
            markup.add(ocean_hotel_go, heaven_raskulova_go)
            markup.add(leaveocean)

        elif user.position == "Магазин":
            markup.add(heaven_raskulova_go)
            markup.add(ocean_hotel_go)
            markup.add(ocean_centre_go)
            markup.add(leaveocean)
        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return
        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)


    elif user.location == 'Радар':
        
        if user.position == "Источники":
            markup.add(heaven_raskulova_go)
            markup.add(radar_healer_go)
            markup.add(radar_centre_go)
            markup.add(leaveradar)

        elif user.position == "Отель":
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(radar_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(radar_centre_go)
            markup.add(leaveradar)
        
        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(radar_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(radar_centre_go)
            markup.add(leaveradar)

        elif user.position == "Площадь":
            markup.add(radar_gym_go, heaven_raskulova_go)
            markup.add(radar_healer_go, radar_shop_go)
            markup.add(radar_hotel_go, radar_alchemy_go)
            markup.add(leaveradar)
        
        elif user.position == "Телепорт Радара":
            markup.add(radar_gym_go, heaven_raskulova_go)
            markup.add(radar_healer_go, radar_shop_go)
            markup.add(radar_hotel_go, radar_alchemy_go)
            markup.add(leaveradar)

        elif user.position == "Магазин":
            markup.add(heaven_raskulova_go)
            markup.add(radar_hotel_go)
            markup.add(radar_centre_go)
            markup.add(leaveradar)
        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)

    elif user.location == 'Метро':
        
        if user.position == "Источники":
            markup.add(heaven_raskulova_go)
            markup.add(metro_healer_go)
            markup.add(metro_centre_go)
            markup.add(leavemetro)

        elif user.position == "Отель":
            priceHotel = int(user.lvl * 2)
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(metro_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(metro_centre_go)
            markup.add(leavemetro)
        
        elif user.position in ["Номер в отеле", "Эконом-номер", "Премиум-номер"]:
            markup.add(metro_healer_go)
            markup.add(heaven_raskulova_go)
            markup.add(metro_centre_go)
            markup.add(leavemetro)

        elif user.position == "Площадь":
            markup.add(metro_gym_go, heaven_raskulova_go)
            markup.add(metro_healer_go, metro_shop_go)
            markup.add(metro_hotel_go)
            markup.add(leavemetro)
        
        elif user.position == "Магазин":
            markup.add(heaven_raskulova_go)
            markup.add(metro_hotel_go)
            markup.add(metro_centre_go)
            markup.add(leavemetro)
        else:
            await db.Users.filter(id=user.id).update(position='Площадь')
            await bot.send_message(m.chat.id, "Возникла ошибка. Попробуйте еще раз")
            return

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode = 'markdown', reply_markup=markup)

    
    elif user.location == 'База клана':
        markup.add(clanBase_onsen)
        markup.add(clanBase_hotel)
        markup.add(clanBase_centr)
        markup.add(clanBase_security)
        markup.add(clanBase_exitToHeaven)
        markup.add(clanBase_exitToTower)
        markup.add(clanBase_krazha)

        text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
        await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)
    
    elif user.location.startswith('Окрестности'):
        getFrak = user.location.replace('Окрестности ', '', 1)
        frak = await db.Fraks.get_or_none(name=str(getFrak))
        if frak and user.frak == frak.name:
            markup.add(clanBase_onsen)
            markup.add(clanBase_hotel)
            markup.add(clanBase_centr)
            markup.add(clanBase_security)
            markup.add(clanBase_exitToHeaven)
            markup.add(clanBase_exitToTower)
            markup.add(clanBase_krazha)
            text = "📡 *Местоположение* \n{}: {}\n\n`Навигация`:".format(user.location, user.position)
            await bot.send_message(m.chat.id, text, parse_mode='markdown', reply_markup=markup)
    elif user.location == 'Экспедиция':
        getExpd = await db.Expeditions.exists(idplayer=user.id)
        if getExpd:
            getExpd = await db.Expeditions.get(idplayer=user.id).first()
            nowTime = int(time.time())
            timeEnd = getExpd.timeEnd
            _timeleft = int((timeEnd - nowTime) / 60)
            if _timeleft > 60:
                hours = int(_timeleft / 60)
                timeleft = "{} часов".format(hours)
            else:
                timeleft = "{} минут".format(_timeleft)
            await bot.send_message(m.chat.id, "До конца вашей экспедиции осталось {}".format(timeleft))

    elif user.location == 'Первый этаж башни' or user.location == 'Второй этаж башни' or user.location == 'Третий этаж башни' or user.location == 'Четвёртый этаж башни':
        markup.add(go_further)
        markup.add(go_back)
        await bot.send_message(m.chat.id, "📡Местоположение \n{}.📡\n\nОсмотреться /look_around".format(user.location), reply_markup=markup)

    elif user.location == "Пруд":
        markup.add(end_fishing)
        await bot.send_message(m.chat.id, "📡Местоположение \n{}.📡\n".format(user.location), reply_markup=markup)

    elif user.location != "Пустыня":
        markup.add(go_further)
        markup.add(go_further2)
        await bot.send_message(m.chat.id, "📡Местоположение \n{}.📡\n\nОсмотреться /look_around".format(user.location), reply_markup=markup)
    
    else:
        await bot.send_message(m.chat.id, "📡Местоположение \n{}.📡\n\nНавигация в этой локации недоступна. Вы можете телепортироваться в город, используя телепорт в инвентаре.".format(str(user.location)))





async def nav_location(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return

    nav = call.data.split('_')
    navWhere = nav[2]
    user.position = 'Площадь'
    await user.save()

    if navWhere == "start":
        text = ""
        if user.location != "Город":
            await bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            return
        if user.questId == 0:
            quest = "«Время душить змей»"
            user.questId = 1
            user.quest = "«Время душить змей»"
            user.questStatus = 1
            await user.save()
            text += "К вам подошёл охранник, стоявший у ворот и предложил заработать. Естественно, вы согласились\n\n'Эти шипящие шнурки меня вкрай достали, вся жопа в их укусах, скоро ампутировать придётся. Пойди-ка, истреби в округе пустыни этих тварей, пока мне её не ампутировали. Небольшим авансиком буду давать тебе 📜Свиток телепортации если ты вдруг забудешь, но пока ты первого уровня... А, не спрашивай о каком уровне идёт речь, понимающий всегда поймёт.'\n⚠️Получено задание: «Время душить змей»\nУсловия: Добыть 3 тушки питона\n"
        if user.nowhp > 1:
            inventorySize = await db.getInventorySize(user)
            if inventorySize < user.inventorySizeMax and user.lvl == 1:
                types = "Свиток телепортации"
                if await db.Inventory.exists(idplayer=user.id, active=1, name=types):
                    text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: 'Очередной смертник или новый герой?''"
                else:
                    text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: ''Очередной смертник или новый герой?''\nПолучено: 📜свиток телепортации"
                    await db.addItem('Свиток телепортации', user)
            else:
                text += "Проходя через широкую проржавевшую арку, в которой когда-то стояли массивные ворота, спасшие этот город не от одной напасти, ты услышал хриплый голос тусовавшегося тут бомжа: ''Очередной смертник или новый герой?''"
        else:
            text += "_Ну и куда ты собрался-то, ты едва на ногах стоишь! Вали отсюда, хых, герой_"
            await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
            return
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.progLoc == "Город|0":
            markup.add(InlineKeyboardButton('Исследовать пустыню', callback_data="nav_location_1"))
        else:
            markup.add(InlineKeyboardButton('Продолжить исследование', callback_data="nav_location_1"))
        checker1 = await db.Inventory.exists(name='Большой город', idplayer=user.id)
        if not checker1:
            if user.questId != 0:
                markup.add(InlineKeyboardButton('Подойти к охраннику', callback_data="nav_city_ohr"))
        if user.lvl < 30:
            markup.add(InlineKeyboardButton('Идти на свалку', callback_data="nav_location_svalka"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return

    elif navWhere == 'svalka':
        if user.lvl < 30:
            newLocation = "Свалка SR"
            if user.location == "Город":
                pass
            else:
                await bot.edit_message_text("Вы находитесь вне города.", call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
                return
            user.location = newLocation
            user.progStatus = 1
            await user.save()
            text = "Свалка - уникальное место. Только здесь монстров настолько много что их не нужно искать - они сами к вам придут! Однако в этом и минус - тут есть весьма сильные монстры, одолеть которых может быть сложно, поэтому новички сюда обычно не суются. Поэтому - если ты вдруг передумал, еще не поздно использовать 📜Свиток телепортации"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            await asyncio.sleep(30)
            await user.refresh_from_db()
            await giveMobSR(user)
        return
    else:
        result = await db.Locations.exists(id=1)
        if result:
            result = await db.Locations.get(id=1)
        if not result:
            text = "Ошибка определения отправления - не существует такой локации"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if user.progLoc == "Город|0":
            user.ProgLoc = "Пустыня|0".format(result.name)
            user.location = 'Пустыня'
            user.progStatus = 1
            await user.save()
            text = "Вы успешно отправились исследовать локацию *{}*\nНа выходе из города красуется табличка - *ДО ХЭВЕНБУРГА 15 МИНУТ ХОДЬБЫ*\n\nВ пустыне каждую минуту персонаж двигается на 1👣 вперёд. На каждом 👣 есть шанс встретить монстра, с которым необходимо драться. В битве главное следить за своим показателем здоровья и оценивать шансы на победу против монстра. В случае опасности есть возможность использовать 📜свиток телепортации, нажав на соответствующую кнопку в битве.".format(result.name)
        else:
            if user.location == result.prev or user.location == "Город" or user.location == "Свалка" and result.name == "Пустыня":
                user.progLoc = "{}|1".format(result.name)
                user.location = result.name
                user.progStatus = 1
                await user.save()
                text = "Вы успешно отправились исследовать локацию *{}*".format(str(result.name))
            else:
                text = "Сообщение устарело"
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)





async def nav_city(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return

    nav = call.data.split('_')
    navWhere = nav[2]
    if navWhere == "onsen":
        newPos = "Источники"
        
        if (str(user.location) == "Город") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            if int(user.lvl <= 1):
                text = "_Пар нежно обволакивал голые тела молодых девиц, отдыхающих в этих божественных источниках. Как только они увидели тебя, сразу же поманили пальцем и указали на специально выделенное для тебя местечко в горячей воде между двумя не менее горячими дамами..._\n\n\nИменно так ты себе представлял горячие источники, пока не увидел кучу ржавых корыт соединённых одной сплошной трубой, проводящей желтоватую тёплую воду.\nИсцеление проходит постепенно, нужно немного подождать"
            else:
                text = "Ты снова пришёл в старое место, где увидел кучу ржавых корыт соединённых одной сплошной трубой, проводящей желтоватую тёплую воду.\nИсцеление проходит постепенно, нужно подождать пару минут."
            
            await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
            return

        elif str(user.location) != "Город":
            text = "Ты находишься вне города."
        elif int(user.hp) <= int(user.nowhp):
            text = "_Ну и на кой ты сюда с полным здоровьем припёрся? А ну брысь отсюда! И чтоб здоровым не возвращался!_"
        elif str(user.position) == newPos:
            text = "Ты уже находишься в горячих источниках.\nИсцеление проходит постепенно, нужно немного подождать"
        else:
            text = "Ошибка определителя. Location {} \n Hp/nowhp {}/{}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.nowhp), str(user.hp), str(user.position), str(newPos))
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
    elif navWhere == "hotel":
        newPos = "Отель"
        if (str(user.location) == "Город") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            priceHotel = int(user.lvl * 2)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            priceHotelMin = int(user.lvl / 2)
            markup.add(InlineKeyboardButton('Отдыхать в премиум-номере - 💰{}'.format(priceHotel), callback_data="hotel_premium"))
            markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotelMin), callback_data="hotel_start"))
            markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="hotel_return"))
            text = '_На ресепшене чуть ли не засыпает некий небритый мужик, зал пустой и всем своим видом показывающий, что уборщица сюда не заходила с момента постройки сего здания._ Мужик воскликнул: "КТО СПИТ? Я НЕ СПЛЮ! ПОДХОДИ, СПРАШИВАЙ, НЕ СТЕСНЯЙСЯ." и принялся делать вид, что он что-то делает.Чего тебе надобно, приятель?"'
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
            return
        elif str(user.location) != "Город":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Город") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            await goToShop(call, user)
        elif str(user.location) != "Город":
            text = "Вы находитесь вне города"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        elif str(user.position) == newPos:
            text = "Вы уже в магазине."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
            await goToShop(call, user)
    elif navWhere == "centr":
        newPos = "Площадь"
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return

        newPos = "Площадь"
        user.position = newPos
        await user.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_city_kachalka"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_city_onsen"))
        markup.add(InlineKeyboardButton('🏪Магазин', callback_data="nav_city_shop"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_city_hotel"))
        markup.add(InlineKeyboardButton('⚔️Арсенал', callback_data="nav_city_arsenal"))
        markup.add(InlineKeyboardButton('🏦Ломбард', callback_data="nav_city_lombard"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        texts = ["В 🏋‍♂Качалке ты можешь прокачать свои характеристики 💢Атаки и ❤️Здоровья", "⛲️Источники помогут тебе бесплатно восстановить ❤️Здоровье",
        "В 🏪Магазине ты можешь приобрести много полезных вещей", "🏫Отель сохранит тебя от голодной смерти если ты не можешь играть", "Если твоё оружие по каким-то причинам тебе не нравится, в ⚔️Арсенале есть запасное!",
        "В 🏦Ломбарде можно продавать ненужные вещи", "Перед выходом из города убедись что у тебя есть 📜Свиток телепортации!", "У ворот города стоит охранник который найдёт для тебя способ подзаработать и обьяснить некоторые игровые механики",
        "Следи за энергией - чем она меньше тем меньше урона ты наносишь! Восполнить энергию можно в Отеле, выпив кофе или съев еды.", "Осторожно, не ешь жёлтый снег и просроченную еду!", "Будучи в биве с монстром, следи за своим показателем ❤️Здоровья!",
        "Главный монстр Пустыни - Шаи-Хулуд. Если ты его встретил и у тебя остались незаконченные дела в этом городе - лучше вернуться. Обратного пути больше не будет."]
        randomtext = random.choice(texts)
        text = "Главная площадь - гордость этого города: кучка построек, начиная с качалки и заканчивая ларьком с мусором, в аккурат расставлены вокруг разбитого в труху фонтана с табличкой «Ремонт»\nПосреди площади висит стенд с обьявлениями. Твоё внимание привлекло одно из них:\n_{}_".format(randomtext)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')
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
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_city_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await call.answer()
    elif navWhere == 'arsenal':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        passed = 0
        checkWeapon1 = await db.Inventory.exists(name='Меч', idplayer=user.id)
        if not checkWeapon1:
            markup.add(InlineKeyboardButton('Меч', callback_data="donateSelectItem_mech"))
            passed = 1
        checkWeapon1 = await db.Inventory.exists(name='Катана', idplayer=user.id)
        if not checkWeapon1:
            markup.add(InlineKeyboardButton('Катана', callback_data="donateSelectItem_katana"))
            passed = 1
        checkWeapon1 = await db.Inventory.exists(name='Пистолет с ножом', idplayer=user.id)
        if not checkWeapon1:
            markup.add(InlineKeyboardButton('Пистолет с ножом', callback_data="donateSelectItem_pistol"))
            passed = 1
        checkWeapon1 = await db.Inventory.exists(name='Копьё', idplayer=user.id)
        if not checkWeapon1:
            markup.add(InlineKeyboardButton('Копьё', callback_data="donateSelectItem_kopie"))
            passed = 1
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
        if passed == 1:
            await bot.edit_message_text("Арсенал - место халявы. Тут ты можешь менять своё оружие чтобы выбрать то, которое больше нравится. Выбирай с умом, по одному виду оружия на человека!", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            await bot.edit_message_text("Увы, всё что мог, ты отсюда уже забрал", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif navWhere == "ohr":
        if user.questId == 1 and user.questStatus == 1:
            name = "Тушка питона"
            res = await db.Inventory.filter(idplayer=user.id, name=name, active=1)
            if res:
                count = 0
                for dict in res:
                    count += 1
                if count >= 3:
                    q = await db.Inventory.filter(name=name, idplayer=user.id).update(active=0)
                    user.money = user.money + 100
                    user.questStatus = 1
                    quest = "«Доставщик»"
                    user.questId = 2
                    user.quest = quest
                    await user.save()
                    text = "Подойдя к охраннику, протягиваете ему скользские и противные тушки питонов. Он удовлетворённо кивнул и дал вам 100💰.\n\nСразу же после этого он начал просить тебя принести ему перьев для подушки, которые можно получить с 🦅Ястребов, ''Хватит пяти штук...''\n"
                    await bot.send_message(call.message.chat.id, text)
                    return
                else:
                    text = "Подойдя к охраннику, он фыркнул:\n'Так и думал, что ты - самая натуральная зелень, которая ни на что не способна... Проваливай отсюда'\n\nВаша задача - добыть три тушки питона."
                    await bot.send_message(call.message.chat.id, text)
                    return
            else:
                text = "Подойдя к охраннику, он фыркнул:\n'Так и думал, что ты - самая натуральная зелень, которая ни на что не способна... Проваливай отсюда'\n\nВаша задача - добыть три тушки питона."
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                return
        elif user.questId == 2 and user.questStatus == 1:
            name = "Перо ястреба"
            res = await db.Inventory.filter(idplayer=user.id, name=name, active=1)
            if res:
                count = 0
                for dict in res:
                    count += 1
                if count >= 5:
                    q = await db.Inventory.filter(name=name, idplayer=user.id).update(active=0)
                    user.money = user.money + 350
                    quest = "«Варись зелька большая и маленькая»"
                    user.questId = 4
                    user.quest = quest
                    user.questStatus = 3
                    await user.save()
                    text = "Подойдя к охраннику, достаёте мешок с перьями. Он кинулся вас целовать, но вы мягко его отодвинули, попросив оплату. Кивнул, он дал вам 350💰.\n'Я твой должник, спасибо тебе, родной!'\nПрактически сразу же он принял серьёзное выражение лица, обьясняя что недавно пропал один из его сменщиков и попросил тебя поискать его в пустыне... или то, что от него осталось.\n"
                    await bot.send_message(call.message.chat.id, text)
                    return
                else:
                    text = "Подойдя к охраннику, он покачал головой:\n'Боюсь, еще мало... Принеси побольше!'"
                    await bot.send_message(call.message.chat.id, text)
                    return
            else:
                text = "Подойдя к охраннику, он покачал головой:\nЯ же попросил 5 перьев... Принеси, а?"
                await bot.send_message(call.message.chat.id, text)
                return
        elif user.questId == 3 and user.questStatus == 1:
            name = "Кошелёк падшего героя"
            res = await db.Inventory.exists(idplayer=user.id, name=name, active=1)
            if res:
                res = await db.Inventory.get(idplayer=user.id, name=name, active=1)
                res.active = 0
                await res.save()
                user.money = user.money + 500
                user.questStatus = 0
                user.questStatus = 4
                await user.save()
                text = "Подойдя к охраннику, ты отдал ему кошелёк. Охранник проверил его и дал тебе 500💰.\n-Жаль парня... Ладно, ты всё-равно молодец. Спасибо тебе."
                await bot.send_message(call.message.chat.id, text)
                await asyncio.sleep(3)
                text = """`⚠️Важный сюжетный ход`

    Охранник вдруг покачал головой: 'Что же, теперь наши пути расходятся. Я увольняюсь и хочу заняться своим делом. Я тут в соседнем городе присмотрел заведение одно, можешь искать меня там. Надеюсь, мы еще увидимся! Береги себя.'
Тем не менее, я считаю что тебе здесь больше нечего делать. Если хочешь хорошей жизни, а не гнить с бомжами вокруг, советую тебе направляться в Хэвенбург. Там и технологии лучше, и заработать проще. За пустыней находится этот город, там поймёшь по месту. И да, будь осторожнее, после пустыни много камней."""
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')

                await bot.send_message(call.message.chat.id, "Ну что же, вроде я тебе всё рассказал что хотел. Удачи тебе, {}. Еще увидимся...".format(user.username))
                return
            else:
                text = "Подойдя к охраннику, он поинтересовался:\n'Ну что, ты нашёл кошелёк того парня?'"
                await bot.send_message(call.message.chat.id, text)
                return
        else:
            text = "Подойдя к постоянному месту охранника, ты никого не обнаружил."
            await bot.send_message(call.message.chat.id, text)
            return
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Купить 💎', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_city_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return




async def kach(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    if kach == 'atk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        if (user.money - needAtk) >= 0:
            user.atk = user.atk + 1
            user.money = user.money - needAtk
            await user.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            text = "💢Атака: улучшено до {} за {}💰\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(atk), str(needAtk), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="kach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="kach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await achprog(user, ach='kachalka')
        else:
            text = "Вам не хватает денег."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif kach == 'hp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.location == "Город":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
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
            text = "❤️Здоровье: улучшено до {} за {}💰\nБаланс: {}💰\nУлучшить навык 💢Атака - {}💰\nУлучшить навык ❤️Здоровье - {}💰".format(str(hp), str(needHp), str(user.money), str(_needAtk), str(_needHp))
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Прокачать атаку ({}💰)'.format(_needAtk), callback_data="kach_atk"))
            markup.add(InlineKeyboardButton('Прокачать здоровье ({}💰)'.format(_needHp), callback_data="kach_hp"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await achprog(user, ach='kachalka')
        else:
            text = "Вам не хватает денег."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


hotelUsers = {}

#HOTEL
async def hotel(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    hotel = call.data.split('_')
    hotelDo = hotel[1]
    if hotelDo == "start":
        newPos = "Эконом-номер"
        priceHotel = user.lvl / 2
        if (str(user.position) == "Отель") and (int(user.money) >= priceHotel):
            user.money = user.money - priceHotel
            user.position = newPos
            await user.save()
            text = "_Дяденька взял плату и метнул в тебя уже немного проржавевший ключ._\nЗайдя в свой номер, ты решил отдохнуть..."
        elif str(user.position) != "Отель":
            text = "Ты находишься вне отеля."
        elif int(user.money) < priceHotel:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="У тебя нет денег") 
            return               
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\nMoney {}\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos), str(user.money))
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
    elif hotelDo == "premium":
        newPos = "Премиум-номер"
        priceHotel = user.lvl * 2
        if (str(user.position) == "Отель") and (int(user.money) >= priceHotel):
            user.money = user.money - priceHotel
            user.position = newPos
            await user.save()
            text = "_Дяденька взял плату и метнул в тебя уже немного проржавевший ключ._\nЗайдя в свой номер, ты решил отдохнуть..."
        elif str(user.position) != "Отель":
            text = "Ты находишься вне отеля."
        elif int(user.money) < priceHotel:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="У тебя нет денег") 
            return               
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\nMoney {}\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos), str(user.money))
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
    else:
        priceHotel = user.lvl / 2 
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Отдыхать в эконом-номере - 💰{}'.format(priceHotel), callback_data="hotel_start"))
        markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_city_centr"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_location_start"))
        text = "Вы находитесь в отеле города. Доступные варианты навигации:"
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)


async def bighotel(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    hotel = call.data.split('_')
    hotelDo = hotel[1]
    if hotelDo == "start":
        newPos = "Номер в отеле"
        priceHotel = user.lvl * 3
        if (str(user.position) == "Отель") and (int(user.money) >= priceHotel):
            user.money = user.money - priceHotel
            user.position = newPos
            await user.save()
            text = "_Дяденька взял плату и метнул в тебя уже немного проржавевший ключ._\nЗайдя в свой номер, ты решил отдохнуть..."
        elif str(user.position) != "Отель":
            text = "Ты находишься вне отеля."
        elif int(user.money) < priceHotel:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="У тебя нет денег") 
            return               
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\nMoney {}\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos), str(user.money))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Отдыхать в номере - 💰5', callback_data="hotel_start"))
        markup.add(InlineKeyboardButton('🏣Площадь', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text("Вы находитесь в отеле города. Доступные варианты навигации:", call.message.chat.id, call.message.message_id, reply_markup=markup)






async def goToShop(call, user): 
    name = 'shop_work'
    result = await db.System.get(name=name)
    if int(result.value) == 1:
        text = "_Ты подходишь к невзрачному стеллажу с выцвевшим навесом. Ощущение, словно владелец бросает сюда весь мусор, который только находит на близлежащей свалке. Впрочем, некоторые товары кажутся почти новыми._"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    else:
        text = '_Вы подошли к магазину где стоял одинокий Ашот. \n-Эй, Ашотик, брат, продай мне чё-нибудь\n-Пашёль нахуй_'
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
        return
    m1 = call.from_user.id
    m2 = call.message.chat.id
    m3 = call.message.message_id
    if user.lvl != 1:
        await shop(m1, m2, m3)
    else:
        await asyncio.sleep(5)
        await shop(m1, m2, m3)

        ############
        #  TRADES  #
        ############

async def trade(call, result): 
    tr = call.data.split('_')
    tradeWith = tr[1]
    location = "Город"
    position = "Место обмена"
    usr = await db.Users.get(user_id=call.from_user.id)
    idplayer = result.id
    if result.location == location and result.position == position or result.location == 'Хэвенбург' and result.position == position:
        pass
    else:
        text = "Вы находитесь не на площади."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    res = await db.Users.get(id=tradeWith)
    if res.location == result.location and res.position == result.position:
        pass
    else:
        text = "Игрок находится вне площади."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    if res.lvl < 3:
        text = "У игрока нет 3 уровня для принятия трейда."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    result = await db.Inventory.filter(active=1, idplayer=idplayer)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    count = {}
    size1 = {}
    text = "Выбери предмет для обмена с игроком *{}*\n\n⭐️Уровень доверия игрока: {}/5 \nОн совершил {} обменов.".format(res.username, res.tradenum, res.tradecount)
    for dict in result:
        if dict.name == "Тушка питона" or dict.name == 'Перо ястреба' or dict.name == 'Котелок' or dict.type == 'Растение' or dict.type == 'Сюжетка':
            pass
        elif dict.name == 'Бустер':
            markup.add(InlineKeyboardButton('⚡️Бустер {}ч'.format(dict.lvl), callback_data="tradewith_{}_{}".format(tradeWith, dict.id)))
        else:
            if dict.name in count:
                name, size, bonus, atk_bloc, expiresk = await db.items(dict.name, check=True)
                count[dict.name] += 1
                size1[dict.name] = size1[dict.name] + int(size)
            else:
                name, size, bonus, atk_block, expires = await db.items(dict.name, check=True)
                count[dict.name] = 1
                size1[dict.name] = int(size)
                markup.add(InlineKeyboardButton('{}'.format(name), callback_data="tradewith_{}_{}".format(tradeWith, dict.id)))
    if usr.location == 'Хэвенбург':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_bigcity_centr"))
    elif usr.location == 'Город':
        markup.add(InlineKeyboardButton('↩️Вернуться', callback_data="nav_city_centr"))
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(call.message.chat.id, text[x:x+4096], reply_markup=markup)
    else:
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)

    await call.answer()



async def tradewith(call, result): 
    if (call.from_user.id == call.from_user.id):
        pass
    else:
        return
    tr = call.data.split('_')
    tradeWith = tr[1]
    tradeItem = tr[2]
    location = "Город"
    position = "Место обмена"
    if result.location == location and result.position == position or result.location == 'Хэвенбург' and result.position == position:
        pass
    else:
        text = "Вы находитесь вне области обмена."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    res = await db.Users.get(id=tradeWith)
    tradeWithId = res.user_id
    if res.location == result.location and res.position == result.position:
        pass
    else:
        text = "Игрок находится вне области обмена."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    item = await db.Inventory.get(id=tradeItem)
    if item.active == 0:
        text = "Предмет отсутствует в вашем инвентаре."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    newTrade = await db.Trades(fromP=result.id, toP=tradeWith, item=tradeItem, status=2)
    await newTrade.save()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Принять', callback_data="trades_confirmfirst_{}".format(newTrade.id)))
    markup.add(InlineKeyboardButton('Отклонить', callback_data="trades_cancel_{}".format(newTrade.id)))
    markup.add(InlineKeyboardButton('Изменить трейд', callback_data="trades_edit_{}".format(newTrade.id)))
    try:
        name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
        await bot.send_message(tradeWithId, "*Новое предложение обмена*\n\n Игрок *{}* предлагает:\n{}\n\nВыберите действие.".format(result.username, name), reply_markup=markup, parse_mode = 'markdown')
        text = "✅ Предложение на обмен #{} успешно отправлено \n{}➡️{}\n\nОжидайте решения второй стороны.".format(newTrade.id, item.name, res.username)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    except:
        res.position = "Номер в отеле"
        text = "Игрок заблокировал бота. Трейд отменён."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await res.save()

    await call.answer()



async def trading(call, user): 
    st = call.data.split('_')
    do = st[1]
    tradeid = st[2]
    if user.location not in ['Хэвенбург', 'Город'] and user.position != 'Место обмена':
        return
    if do == 'confirm':
        trade = await db.Trades.get(id=tradeid)
        trade.status = 3
        await trade.save()
        item = await db.Inventory.get(id=trade.item)
        itemreturn = await db.Inventory.exists(id=trade.itemreturn)
        if itemreturn:
            itemreturn = await db.Inventory.get(id=trade.itemreturn)
        fromP = await db.Users.get(id=trade.fromP)
        toP = await db.Users.get(id=trade.toP)
        text = "*Обмен #{} принят*. \n\nОжидание подтверждения второго пользователя.".format(trade.id)
        await bot.send_message(toP.user_id, "Обмен #{}\nВы отдаёте: {}\nВы получаете: {}\nПодтвердить обмен /trade_accept_{}\nОтклонить обмен /trade_cancel_{}".format(trade.id, itemreturn.name, item.name, trade.id, trade.id))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif do == 'cancel':
        player1 = await db.Users.get(user_id=call.from_user.id)
        text = "Вы отклонили обмен."
        trade = await db.Trades.get(id=tradeid)
        trade.status = 0
        await trade.save()
        if trade.itemreturn != None:
            player2 = await db.Users.get(id=trade.toP)
            await bot.send_message(player2.user_id, "Обмен #{} был отклонён".format(trade.id))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        else:
            player2 = await db.Users.get(id=trade.fromP)
            await bot.send_message(player2.user_id, "Обмен #{} был отклонён".format(trade.id), parse_mode = 'markdown')
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')
    elif do == 'edit':
        player = await db.Users.get(user_id=call.from_user.id)
        result = await db.Trades.get(id=tradeid)
        res = await db.Users.get(id=result.fromP)
        inv = await db.Inventory.filter(idplayer=player.id, active=1)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        text = "Выберите, что хотите предложить игроку {} взамен\nУровень доверия игрока - {}/5 , он совершил {} обменов.".format(res.username, res.tradenum, res.tradecount)
        for dict in inv:
            if dict.name == 'Ситень' or dict.name == "Тушка питона" or dict.name == 'Перо ястреба' or dict.name == 'Снунец' or dict.name == 'Котелок' or dict.type == 'Растение' or dict.name == 'Багровая чешуя' or dict.type == 'Сюжетка' or dict.name == 'Странная заготовка':
                pass
            else:
                name, size, bonus, atk_block, expires = await db.items(dict.name, check=True)
                markup.add(InlineKeyboardButton('{}'.format(name), callback_data="tradecon_{}_{}".format(tradeid, dict.id)))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif do == 'confirmfirst':
        result = await db.Trades.get(id=tradeid)
        player1 = await db.Inventory.get(id=result.item)
        player1user = await db.Users.get(id=player1.idplayer)
        player2user = await db.Users.get(id=result.toP)
        if player1.active == 1 and player1.idplayer == result.fromP:
            inventorySize = await db.getInventorySize(player2user)
            if inventorySize + 1 > player2user.inventorySizeMax:
                await bot.send_message(player2user.user_id, "Ваш инвентарь переполнен, вы не можете принять трейд.")
                return
            player1.idplayer = result.toP
            text = "Обмен завершен."
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1', callback_data="tradestar_2_{}_1".format(tradeid)))
            markup.add(InlineKeyboardButton('2', callback_data="tradestar_2_{}_2".format(tradeid)))
            markup.add(InlineKeyboardButton('3', callback_data="tradestar_2_{}_3".format(tradeid)))
            markup.add(InlineKeyboardButton('4', callback_data="tradestar_2_{}_4".format(tradeid)))
            markup.add(InlineKeyboardButton('5', callback_data="tradestar_2_{}_5".format(tradeid)))
            await bot.send_message(player1user.user_id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup)
            result.status = 1
            tradeResult = await db.Trades.get(id=tradeid)
            _fromP = await db.Users.get(id=tradeResult.fromP)
            fromP = _fromP.username
            _toP = await db.Users.get(id=tradeResult.toP)
            toP = _toP.username
            player1user.tradecount += 1
            await player1user.save()
            _toP.tradecount += 1
            await _toP.save()
            await db.commitInventory(_fromP, player1)
            await db.commitInventory(_toP, player1)
            itemresult = await db.Inventory.get(id=tradeResult.item)
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{}\nПредмет: {}".format(tradeResult.id, fromP , toP, itemresult.name))
        else:
            text = "Какого-то предмета уже не существует. Обмен отклонён"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            result.status = 0
        await result.save()
        await player1.save()
        await player1user.save()
    await call.answer()



async def tradecon(call, user): 
    tr = call.data.split('_')
    tradeid = tr[1]
    tradeItem = tr[2]
    location = "Город"
    position = "Площадь"
    r = await db.Trades.get(id=tradeid)
    tradeWith = r.fromP
    nameitem = await db.Inventory.get(id=r.item)
    r.itemreturn = tradeItem
    await r.save()
    result = await db.Users.get(id=r.toP)
    res = await db.Users.get(id=tradeWith)
    tradeWithId = res.user_id
    item = await db.Inventory.get(id=tradeItem)
    if item.active == 0:
        text = "Предмет отсутствует в вашем инвентаре."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Принять', callback_data="trades_confirm_{}".format(tradeid)))
    markup.add(InlineKeyboardButton('Отклонить', callback_data="trades_cancel_{}".format(tradeid)))
    name, size, bonus, atk_block, expires = await db.items(item.name, check=True)
    returnname, returnsize, returnbonus, atk_block, expires = await db.items(nameitem.name, check=True)
    await bot.send_message(tradeWithId, "{} отправил встречное предложение обмена #{}: \n\nЕго {} взамен на ваше {}\n\nВыберите действие.".format(result.username, r.id, name, returnname), reply_markup=markup)
    text = "✅ Встречное предложение успешно отправлено \n{}➡️{}\nОжидайте решения второй стороны.".format(name, res.username)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    await call.answer()


@dp.message_handler(lambda m:m.text and m.text.startswith('/trade_cancel_'))
async def tradecancel(m):
    tradeid = m.text.replace('/trade_cancel_', '', 1).replace('@MeguNext_bot', '', 1)
    result = await db.Trades.get(id=tradeid)
    user1 = await db.Users.get(id=result.fromP)
    user2 = await db.Users.get(id=result.toP)
    if m.from_user.id == user1.user_id:
        result.status = 0
        await result.save()
        await bot.send_message(m.from_user.id, "Вы отклонили обмен")

@dp.message_handler(lambda m:m.text and m.text.startswith('/trade_accept_'))
async def tradeaccept(m):
    tradeid = m.text.replace('/trade_accept_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    result = await db.Trades.get(id=tradeid)
    if result.itemreturn == None:
        result.itemreturn = 0
    player1 = await db.Inventory.get(id=result.item)
    player1user = await db.Users.get(id=player1.idplayer)
    if player1user.location == 'Хэвенбург' or player1user.location == 'Город':
        pass
    else:
        await bot.send_message(player1user.user_id, "Вы находитесь вне города, трейд принять невозможно")
        await bot.send_message(m.chat.id, "Трейдер находится вне города")
        return
    player2 = await db.Users.get(id=result.fromP)
    player2user = await db.Users.get(id=player2.id)
    if player2 and player2.location == 'Хэвенбург' or player2 and player2.location == 'Город':
        pass
    else:
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    if result.itemreturn == 0:
        async def player2(result):
            idplayer = result.toP
            active = 1
        await player2(result)
    else:
        player2 = await db.Inventory.get(id=result.itemreturn)
    checkLot = await db.Raskul.exists(item=result.item)
    if checkLot:
        checkLot = await db.Raskul.filter(item=result.item).update(status=0)
    checkLot = await db.Raskul.filter(item=result.itemreturn).update(status=0)
    if player1.active == 1 and player1.idplayer == result.fromP:
        if player2.active == 1 and player2.idplayer == result.toP:
            inv1 = await db.Inventory.get(id=result.item)
            inv1.idplayer = result.toP
            await inv1.save()

            if result.itemreturn == 0:
                pass
            else:
                inv2 = await db.Inventory.get(id=result.itemreturn)
                inv2.idplayer = result.fromP
                await inv2.save()
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1', callback_data="tradestar_1_{}_1".format(tradeid)))
            markup.add(InlineKeyboardButton('2', callback_data="tradestar_1_{}_2".format(tradeid)))
            markup.add(InlineKeyboardButton('3', callback_data="tradestar_1_{}_3".format(tradeid)))
            markup.add(InlineKeyboardButton('4', callback_data="tradestar_1_{}_4".format(tradeid)))
            markup.add(InlineKeyboardButton('5', callback_data="tradestar_1_{}_5".format(tradeid)))
            await bot.send_message(m.chat.id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup)
            player2 = await db.Users.get(id=result.fromP)
            markup2 = InlineKeyboardMarkup()
            markup.row_width = 2
            markup2.add(InlineKeyboardButton('1', callback_data="tradestar_2_{}_1".format(tradeid)))
            markup2.add(InlineKeyboardButton('2', callback_data="tradestar_2_{}_2".format(tradeid)))
            markup2.add(InlineKeyboardButton('3', callback_data="tradestar_2_{}_3".format(tradeid)))
            markup2.add(InlineKeyboardButton('4', callback_data="tradestar_2_{}_4".format(tradeid)))
            markup2.add(InlineKeyboardButton('5', callback_data="tradestar_2_{}_5".format(tradeid)))
            await bot.send_message(player2.user_id, "Обмен #{} завершен. Оцените обмен по пятибальной шкале.".format(result.id), reply_markup=markup2)
            tradeResult = await db.Trades.get(id=tradeid)
            _fromP = await db.Users.get(id=tradeResult.fromP)
            _toP = await db.Users.get(id=tradeResult.toP)
            await db.commitInventory(_fromP, inv2)
            await db.commitInventory(_fromP, inv1)
            await db.commitInventory(_toP, inv2)
            await db.commitInventory(_toP, inv1)
            fromP = _fromP.username
            toP = _toP.username
            _fromP.tradecount += 1
            _toP.tradecount += 1
            await _fromP.save()
            await _toP.save()
            __item = await db.Inventory.get(id=tradeResult.item)
            __itemret = await db.Inventory.get(id=tradeResult.itemreturn)
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{}\nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, __item.name, __itemret.name))
            tradeResult.status = 1
            await tradeResult.save()
            await achprog(_fromP, ach='trader')
            await achprog(_toP, ach='trader')
        else:
            trade = await db.Trades.get(id=tradeid)
            trade.status = 0
            await trade.save()
            await bot.send_message(m.chat.id, "Какого-то предмета уже не существует. Обмен отклонён")
    else:
        result.status = 0
        await result.save()
        await bot.send_message(m.chat.id, "Какого-то предмета уже не существует. Обмен отклонён")





async def tradestar(call, user): 
    st = call.data.split('_')
    p = st[1]
    trade = st[2]
    star = st[3]
    if p == "1":
        tradeResult = await db.Trades.get(id=trade)
        tradeResult.star = star
        await tradeResult.save()
        _fromP = await db.Users.get(id=tradeResult.fromP)
        fromP = _fromP.username
        _toP = await db.Users.get(id=tradeResult.toP)
        toP = _toP.username
        text = "Оценка отправлена."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        __item = await db.Inventory.get(id=tradeResult.item)
        try:
            __itemret = db.Inventory.get(id=tradeResult.itemreturn)
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, star, toP, __item.name, __itemret.name))
        except:
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}".format(tradeResult.id, fromP , toP, star, toP, __item.name))
    elif p == "2":
        tradeResult = await db.Trades.get(id=trade)
        tradeResult.star2 = star
        await tradeResult.save()
        _fromP = await db.Users.get(id=tradeResult.fromP)
        _toP = await db.Users.get(id=tradeResult.toP)
        fromP = _fromP.username
        toP = _toP.username
        text = "Оценка отправлена."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        __item = await db.Inventory.get(id=tradeResult.item)
        try:
            __itemret = await db.Inventory.get(id=tradeResult.itemreturn)
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}➡️{}".format(tradeResult.id, fromP , toP, star, fromP, __item.name, __itemret.name))
        except:
            await bot.send_message(tradeChat, "Обмен #{}\n{}➡️{} - {}⭐️ by {} \nПредмет: {}".format(tradeResult.id, fromP , toP, star, fromP, __item.name))


usrsprogLocsShrines = {}
async def shrineUse(call, user): 
    bogs = ['святого Кефира', 'святого Херового огра', 'святого Путешественника', 'святого Покорителя башни', 'святой Мегумин', 'святой Котоми', 'святой МегуНекст', 'святого Карася']
    effects = ['booster', 'energy', 'heal', 'eat', 'sakura', 'oduvanchik', 'ostanki', 'roza', 'rca', 'tp']
    loc = await db.Locations.get_or_none(name=user.location).first()
    if not loc: return
    progLoc = user.progLoc.split("|")
    kvadrat = progLoc[1]
    locShrines = loc.shrines.split(",")
    shrine = 0
    rand = random.choice(bogs)
    randEffect = random.choice(effects)
    if user.user_id in usrsprogLocsShrines and usrsprogLocsShrines[user.user_id] == kvadrat:
        await bot.edit_message_text("Алтари не принимают пожертвования если ты им пользовался недавно", call.message.chat.id, call.message.message_id)
        return
    for z in locShrines:
        if z == kvadrat:
            usrsprogLocsShrines[user.user_id] = kvadrat
            if user.money >= 150:
                text = "Бросив монетки в ящик для пожертвований, ты помолился. Алтарь, построенный в честь {} придал тебе уверенности в твоём нелёгком путешествии и ".format(rand)
                user.money -= 150
                if randEffect == 'booster':
                    if user.booster >= time.time(): user.booster += 300
                    else: user.booster = time.time() + 300
                    text += "пять минут ⚡️Бустеров."
                elif randEffect == 'energy':
                    user.energy = 100
                    text += "зарядил тебя силой."
                elif randEffect == 'heal':
                    user.nowhp += 100
                    text += "лишнюю складку жира чтобы тебя было сложнее убить."
                elif randEffect == 'eat':
                    user.eat = 100
                    text += "избавил тебя от голода."
                elif randEffect == 'tp':
                    success = await db.addItem('Свиток телепортации', user, arg='1')
                    text += "📜Свиток телепортации."
                elif randEffect == 'oduvanchik':
                    user.oduvanchik += 10
                    text += "х10 🌼"
                elif randEffect == 'rca':
                    user.rca += 10
                    text += "х10 🌷"
                elif randEffect == 'roza':
                    user.roza += 10
                    text += "х10 🌹"
                elif randEffect == 'sakura':
                    user.sakura += 10
                    text += "х10 🌸"
                elif randEffect == 'ostanki':
                    success = await db.addItem('Останки героев', user, arg='1')
                    success = await db.addItem('Останки героев', user, arg='1')
                    text += "x2 🦴"
                await user.save()
                await call.answer()
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                randd = random.randint(1, 100)
                checkItem = await db.Inventory.get_or_none(idplayer=user.id, active=1, name='Документ DSFB-4')
                if randd <= 25 and user.location == 'Песчаная пирамида' and user.scenario == 2 and user.scenarioStatus == 1 and checkItem:
                    await scenario(user)
                return
            else:
                await bot.edit_message_text("У вас не нашлось нужного количества монет, поэтому вам пришлось пройти мимо", call.message.chat.id, call.message.message_id)
                await call.answer()
                return
    await bot.edit_message_text("Вы уже прошли мимо алтаря", call.message.chat.id, call.message.message_id)
