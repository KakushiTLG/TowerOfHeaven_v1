@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers and call.data.startswith('startstartBigCity'))
async def startstartCity(call):
    user = await db.Users.get(user_id=call.from_user.id)
    item = await db.Inventory(name='Большой город', type='Большой город', size=0, bonus=0, active=0, idplayer=user.id)
    await item.save()
    text = 'Попинав здешнего спящего бомжа, ты убедился в том что этот город — не глюк. Вонь от бомжа, кстати, тоже вполне реальная'
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    chat = call.message.chat.id
    await startBigCity(chat)
    await call.answer()

async def startBigCity(chat):
    text = "–__Чё происходит... Ты какого хера творишь?! Аа, видать будил меня, чтобы выпивкой угостить, ну конечно же! Не стесняйся, пойдём, я знаю отличный бар здесь рядом.\n\nСкажу по секрету — он здесь единственный, так что выбирать не приходится.__\n\nОн, обняв тебя одной рукой, потащил в известном ему направлении..."
    photo = open('/home/kakushigoto/megu/media/bomj.jpg', 'rb')
    await bot.send_photo(chat, photo, caption=text, parse_mode='markdown')
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Где мы находимся?', callback_data="startBigCity_1"))
    await bot.send_message(chat, "Чёт незнакома мне твоя физиономия, да и пинаешь ты слабовато по сравнению с местными. Надо думать, ты с той безымянной деревни, висящей на соплях, которую почему-то все ещё называют городом. Наверное, в память о былых временах.\n\nИ так, раз уж я пью тут за твой счёт, могу рассказать все чего твоя душа пожелает. Будь уверен, лучшего специалиста в области всего тут нет. Что тебя интересует?", parse_mode='markdown', reply_markup=markup)


@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers and call.data.startswith('startBigCity_'))
async def startBigCity_ans(call): 
    if (call.from_user.id != call.message.chat.id):
        # await call.answer()
        return

    quest = call.data.split('_')
    q = quest[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    text = call.message.text
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    if q == '1':
        markup.add(InlineKeyboardButton('Расскажи немного о городе', callback_data="startBigCity_2"))
        text = "\n''Что это за место?''\n_В столице нашей страны... Вернее того, что от неё осталось. Тут эдакие ''мирные воды'' на которых представители всех кланов могут отдохнуть  от сражений, ненависти и матюков._"
    elif q == '2':
        markup.add(InlineKeyboardButton('Есть ли организации, в которые я могу вступить?', callback_data="startBigCity_3"))
        text += "\n\n''Кланы?''\n_Мда, как всё запущено. Ладно, если вкратце: это разобщенные кучки народу, которые сражается за своё благополучие. Давай дальше._"
    elif q == '3':
        markup.add(InlineKeyboardButton('Расскажи о небесной башне', callback_data="startBigCity_4"))
        text += "\n\n''Есть ли организации, в которые я могу вступить?''\n_Да, ты можешь вступить в какую-нибудь клан и помогать ей разузнать больше про небесную башню. _"
    elif q == '4':
        markup.add(InlineKeyboardButton('Как заработать?', callback_data="startBigCity_5"))
        text += "\n\n''Башня?''\n_Ну, это легенда, о которой знать должен каждый! Ты вообще откуда взялся, раз не знаешь, что это?.. Ох, ладно. В общем, легенда гласит о том, что это башня, которая простирается в самое небо и, пройдя до самого верха, ты можешь увидеть весь наш мир, найти... эээ... древние свитки, в которых описано наше прошлое, и поговаривают, в них есть карта, которая приведёт тебя к драгоценностям, о которых ты даже и не мечтал..."
        text += "Вот поэтому все и цапаются между собой за право владеть башней. Хотя до сих пор никто внутри ничего так и не нашёл..._"
    elif q == '5':
        markup.add(InlineKeyboardButton('Окей, как попасть в эти твои "кланы"?', callback_data="startBigCity_6"))
        text += "\n\n''Как заработать?''\n_А как ты до этого себе на жизнь зарабатывал? Я смотрю, броня у тебя не так уж и плоха, оружие при себе есть, да и сам ты выглядишь не слабым._"
    elif q == '6':
        markup.add(InlineKeyboardButton('...', callback_data="startBigCity_7"))
        text += "\n\n''Окей, как попасть в эти твои ''кланы''? ''\n_Неужели ты хочешь в клан? ЭЙ, МУЖИКИ, ТУТ ЧЕЛОВЕКУ В КЛАН ВСТУПИТЬ ХОЧЕТСЯ, ЕСЛИ ВЫ ПОНИМАЕТЕ, О ЧЕМ Я..._"
    elif q == '7':
        text = "\n\n\nПосле внезапного удара по голове, все дальше было как в тумане. Ты проснулся спустя несколько часов с болью на левом жопном полушарии и без гроша в кармане. На вопрос о том, что случилось, бармен отвечал только то, что ты угощал всех выпивкой и вступил в клан 📚Академии📚...\n\nНа заднице была удобно выбита ссылка-приглашение в чат https://t.me/+fpUvTUZ0CHQ2MGUy\nБармен пожалел тебя и предложил пойти осмотреться в городе пока:\nВ твоём-то гадюшнике точно не было нормального ломбарда, бара да и прочих прелестей...\n"
        text += "\nТак же бармен посоветовал после осмотра города отправиться в Случайный Лес дабы понять какие тут монстры вокруг есть вообще...И дал немного еды.."
        await db.addItem("Лучше не спрашивай", user, arg='1')
        await db.addItem("Лучше не спрашивай", user, arg='1')
        await db.addItem("Лучше не спрашивай", user, arg='1')
        user = await addAch(user, ach='novichek')
        await db.Users.filter(id=user.id).update(location='Хэвенбург', position='Площадь', frak='📚Академия📚')
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode = 'markdown')
    await call.answer()
    if q == '7':
        newfrak = await db.Fraks.get(name="📚Академия📚").first()
        leader = await db.Users.get_or_none(id=newfrak.leader)
        if leader:
            text = "Новый игрок в академке\n[{}](tg://user?id={}) ({}) (@{})".format(user.username, user.user_id, user.id, call.from_user.username)
            try:
                await bot.send_message(leader.user_id, text, parse_mode='markdown')
            except:
                pass



async def nav_bigcity(call, user): 
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
        if (str(user.location) == "Хэвенбург") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Хэвенбург":
            text = "Ты находишься вне города."
        elif int(user.hp) <= int(user.nowhp):
            text = "_Послушай... Источники нужны для того, чтобы исцеляться, а не приходить сюда каждый раз только если бабу охота!_"
        elif str(user.position) == newPos:
            text = "Ты занимаешься *CENSORED*\nИсцеление проходит постепенно, нужно немного подождать"
        else:
            text = "Ошибка определителя. Location {} \n Hp/nowhp {}/{}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением в /report".format(str(user.location), str(user.nowhp), str(user.hp), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
    elif navWhere == "hotel":
        checkFrak = await db.Fraks.exists(name=user.frak)
        if checkFrak:
            await bot.edit_message_text("К сожалению, отель вам недоступен. Воспользуйтесь ночлегом на базе клана.", call.message.chat.id, call.message.message_id)
            return
        newPos = "Отель"
        if (str(user.location) == "Хэвенбург") and (str(user.position) != newPos):
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
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await call.answer()
            return
        elif str(user.location) != "Хэвенбург":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
    elif navWhere == "centr":
        newPos = "Площадь"
        if user.location == "Хэвенбург":
            pass
        else:
            text = "Вы находитесь вне города."
            await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
            await call.answer()
            return
        newPos = "Площадь"
        user.position = newPos
        await user.save()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_bigcity_kachalka"), InlineKeyboardButton('🏦Ломбард', callback_data="nav_bigcity_lombard"))
        markup.add(InlineKeyboardButton('⚖️Трейды', callback_data="nav_bigcity_trades"), InlineKeyboardButton('🥃Бар', callback_data="nav_bigcity_bar"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_bigcity_onsen"), InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_bigcity_raskul"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_bigcity_hotel"), InlineKeyboardButton('👨🏾‍🦳Бомж', callback_data="nav_bigcity_skupshik"))
        markup.add(InlineKeyboardButton('👺Драконоборец', callback_data="defShop"), InlineKeyboardButton('📋Доска ДВП', callback_data='dvp'))
        markup.add(InlineKeyboardButton('😈Дом Адского', callback_data="nav_bigcity_hns"))
        markup.add(InlineKeyboardButton('🏜Покинуть город', callback_data="nav_bigcity_exit"))
        text = "Площадь как площадь. Ведь площадь она и в Хэвенбурге площадь, верно? Знаешь как выглядят площади, так вот наша площадь практически такая же, как и все площади, что ты видел до неё. В общем, площадь, которая выглядит как площадь — вот она, наша площадь Хэвенбурга."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await call.answer()
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Случайный лес"
                if user.location != "Хэвенбург":
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города", parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return

                user.location = newLocation
                user.progStatus = 1
                user.battleStatus = 0
                user.progLoc = 'Случайный лес|0'
                await user.save()

                text = "Вы отправились в Случайный лес"
                await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            elif navg == 'clanBase':
                checkGroup = await db.Fraks.get_or_none(name=user.frak).first()
                if checkGroup:
                    if user.location != "Хэвенбург":
                        await bot.send_message(call.message.chat.id, "Вы находитесь вне города", parse_mode='markdown')
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                        return
                    if checkGroup.underAtk >= int(time.time()):
                        user.location = "Окрестности Хэвенбурга"
                        user.progStatus = 1
                        user.battleStatus = 0
                        user.progLoc = 'Окрестности Хэвенбурга|0'
                        await user.save()

                        text = "Вы отправились к базе клана."
                    else:
                        user.location = 'База клана'
                        user.progStatus = 0
                        await user.save()

                        text = "Вы телепортировались к базе клана."

                    await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
            elif navg == 'tower':
                newLocation = "Тропа к башне"
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Вы не можете идти в башню.", parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                if user.frak != '' and user.frak != None:
                    frak = await db.Fraks.get_or_none(name=user.frak).first()
                    if frak:
                        user.location = newLocation
                        user.progStatus = 1
                        user.battleStatus = 0
                        user.progLoc = 'Тропа к башне|0'
                        await user.save()
                        text = "Вы отправились к Небесной башне"
                        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                    await call.answer()
                    return
            elif navg == 'olimp':
                try:
                    navgg = nav[4]
                    if user.location == "Хэвенбург":
                        pass
                    else:
                        await bot.send_message(call.message.chat.id, "Вы находитесь вне города", parse_mode='markdown')
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                        return
                    if navgg:
                        if navgg == '1': user.progLoc = 'Песчаная пирамида|0'
                        elif navgg == '2': user.progLoc = 'Песчаная пирамида|20'
                        elif navgg == '3': user.progLoc = 'Песчаная пирамида|40'
                        elif navgg == '4': user.progLoc = 'Песчаная пирамида|60'
                        elif navgg == '5': user.progLoc = 'Песчаная пирамида|70'
                        newLocation = "Песчаная пирамида"
                        user.location = newLocation
                        user.progStatus = 1
                        user.battleStatus = 0
                        await user.save()
                        text = "Вы телепортировались в Песчаную пирамиду"
                        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                        await call.answer()
                        return
                except:
                    text = "Выберите, куда телепортироваться."
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Первый сектор', callback_data="nav_bigcity_exit_olimp_1"))
                    sectors = await db.Inventory.filter(name__in=['Первый сектор', 'Второй сектор', 'Третий сектор', 'Пятый сектор'], idplayer=user.id).only('name')
                    _sectors = []
                    for sector in sectors:
                        _sectors.append(sector.name)
                    if "Первый сектор" in _sectors: markup.add(InlineKeyboardButton('Второй сектор', callback_data="nav_bigcity_exit_olimp_2"))
                    if "Второй сектор" in _sectors: markup.add(InlineKeyboardButton('Третий сектор', callback_data="nav_bigcity_exit_olimp_3"))
                    if "Третий сектор" in _sectors: markup.add(InlineKeyboardButton('Четвёртый сектор', callback_data="nav_bigcity_exit_olimp_4"))
                    if "Пятый сектор" in _sectors: markup.add(InlineKeyboardButton('Пятый сектор', callback_data="nav_bigcity_exit_olimp_5"))
                    await bot.send_message(call.message.chat.id, text, reply_markup=markup)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
            elif navg == 'ko4at':
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                if user.lvl >= 15:
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Доступ в Кавайню откроется на 15м уровне", parse_mode='markdown')
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                user = await addAch(user, ach='novichek2')
                await bot.edit_message_text("Телепортируемся...", call.message.chat.id, call.message.message_id)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                checkKawai = await db.Inventory.exists(name='Кавайня гайд', idplayer=user.id)
                if checkKawai:
                    await bot.send_message(call.message.chat.id, "Вы телепортировались в Кавайню.")
                    await call.answer()
                else:
                    newItem = await db.Inventory(name='Кавайня гайд', idplayer=user.id, type='Other', active=0, size=0, bonus=0)
                    await newItem.save()
                    await bot.send_message(call.message.chat.id, "Кавайня - город, в котором тоже есть чем заняться. Правда, на протяжении всего года, тут морозит похлеще чем где-либо. Монстры тут имеют какие-то Снунцы, которые можно обменивать в городе на различные улучшения. Однако не всё так просто - необходимо следить за своим уровнем заморозки, иначе, замёрзнув, ты уже ничего не сможешь добиться в своей жизни. Благо тут в ходу ходят дрова, с которых можно устроить себе костерок дабы согреться, да и броня тут тёплая.")
                user.location = 'Кавайня'
                await user.save()
                return
            elif navg == 'oceanus':
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await call.answer()
                    return
                oceanus = await db.Inventory.exists(name='Портал в Океанус', idplayer=user.id)
                if user.lvl >= 50 and oceanus:
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Доступ в Океанус открывается на 50 уровне, при условии что вы очистили весь Заснеженный лес")
                    await call.answer()
                    return
                user = await addAch(user, ach='novichek4')
                await bot.edit_message_text("Телепортируемся...", call.message.chat.id, call.message.message_id)
                checkKawai = await db.Inventory.exists(name='Океанус гайд', idplayer=user.id)
                if checkKawai:
                    await bot.send_message(call.message.chat.id, "Вы телепортировались в Океанус")
                    await call.answer()
                else:
                    newItem = await db.Inventory(name='Океанус гайд', idplayer=user.id, type='Other', active=0, size=0, bonus=0)
                    await newItem.save()
                    await bot.send_message(call.message.chat.id, "Океанус - городок не более привлекательнее вечно мёрзлой Кавайни, однако тут в ходу более развитая броня которая еще и защищает вас от повышенной влажности, которая накапливается в организме и не даёт двигаться.")
                    await call.answer()
                user.location = 'Океанус'
                await user.save()
                return
            elif navg == 'expds':
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await call.answer()
                    return
                if user.lvl >= 25:
                    await expeds(call, user)
                else:
                    await bot.send_message(call.message.chat.id, 'Доступ к экспедициям откроется на 25 уровне.')
            
            elif navg == 'SR':
                if user.lvl < 30:
                    newLocation = "Свалка SR"
                    if user.location == "Хэвенбург":
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

            elif navg == 'radar':
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await call.answer()
                    return
                radar1 = await db.Inventory.exists(name='Портал в Радар1', idplayer=user.id)
                radar3 = await db.Inventory.exists(name='Портал в Радар3', idplayer=user.id)
                if user.lvl >= 35 and radar1 and radar3:
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Доступ в Радар открывается на 35 уровне, при условии что вы прошли все Случайный и Заснеженный лес.")
                    await call.answer()
                    return
                user = await addAch(user, ach='novichek3')
                await bot.edit_message_text("Телепортируемся...", call.message.chat.id, call.message.message_id)
                checkKawai = await db.Inventory.exists(name='Радар гайд', idplayer=user.id)
                if checkKawai:
                    await bot.send_message(call.message.chat.id, "Вы телепортировались в Радар")
                    await call.answer()
                else:
                    newItem = await db.Inventory(name='Радар гайд', idplayer=user.id, type='Other', active=0, size=0, bonus=0)
                    await newItem.save()
                    await bot.send_message(call.message.chat.id, "Радар напоминает больше село - настолько тут всё выглядит бедно и расшатано что можно смело сомневаться в том что отсюда можно получить хоть какие-то деньги. В любом случае, посмотреть стоит, а там уже решать...")
                    await call.answer()
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    text = "-О, а вот и ты!\n\nОбернувшись, увидел знакомое лицо. Неужели охранник с бара решил выйти со своего гадюшника?\n\n-_В общем, смотри, у меня мало времени так что быстрый экскурс. Вон там площадь, привычные заведения для тебя все есть. За углом Табервам... Да, Табервам. Это муж Табернам"
                    text += "\nОни столько лет были разделены из-за закрытого города... Эх, грустная история... В общем, выходить и зачищать местность вокруг необходимо двум людям сразу, иначе тебя просто быстро порвут на тряпки. Монстры тут дикие, гораздо дальше от башни чем Океанус, в конце концов..."
                    text += "\nЖители Радара, может, и бедняки еще те, но на награды не скупятся - у них есть немало интересных вещичек из которых можно собирать артефакты. А, собирать артефакты из хлама что тебе дадут можно будет на площади, у Сыча. Там разберешься сам, всё просто. Ну и броня, аха, как же без неё!"
                    text += "Зная твой фетиш на новую броню, тут для тебя открывается весьма интересная картина - конечно же тут есть новая броня, конечно же ты её сможешь получить за ♦️Рюмбы. Я думаю, мне не стоит рассказывать откуда их можно достать, смекаешь? Ладненько, вроде я тебе быстренько всё обьяснил, пора и честь знать!_"
                    text += "\n\nС этими словами охранник пошёл к телепорту. В последнюю секунду, перед тем как исчезнуть, он повернул лицо в твою сторону, подмигнул и сказал: «Береги задницу!»"
                    await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                user.location = 'Радар'
                await user.save()
                return
            elif navg == 'metro':
                if user.location == "Хэвенбург":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, 'Вы находитесь вне города', parse_mode='markdown')
                    await call.answer()
                    return
                metro1 = await db.Inventory.exists(name='Портал в Метро1', idplayer=user.id)
                if user.lvl >= 100 and metro1:
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Доступ в Метро открывается на 100 уровне, при условии что вы прошли весь Океанус")
                    await call.answer()
                    return
                user = await addAch(user, ach='novichek5')
                await bot.edit_message_text("Телепортируемся...", call.message.chat.id, call.message.message_id)
                checkKawai = await db.Inventory.exists(name='Метро гайд', idplayer=user.id)
                if checkKawai:
                    await bot.send_message(call.message.chat.id, "Вы телепортировались в Метро")
                    await call.answer()
                else:
                    newItem = await db.Inventory(name='Метро гайд', idplayer=user.id, type='Other', active=0, size=0, bonus=0)
                    await newItem.save()
                    await bot.send_message(call.message.chat.id, "Метро - это даже не город, это... метро. Жители города периодически подвергаются нападениям монстров из туннелей, а самым авторитетным тут считается охотник, имеющий как можно больше 🗝Ключей, ведь это является главной валютой Метро, а еще они имеются у монстров, что делает тебя крутым в глазах населения.")
                    await call.answer()
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    text = "-Добро пожаловать в Метро!\n\nОбернувшись, увидел знакомое лицо. Неужели охранник с бара решил выйти со своего гадюшника? Стоп, где-то я это уже слышал...\n\n"
                    text += "\n-_Слыхал я про это местечко... Тут, конечно, не сахар, но где в нашем мире вообще хорошо? Везде эти монстры, постоянно какие-то проблемы... Ну тут все посерьёзнее, увы."
                    text += "\nРаньше здесь была ядерная война, кругом радиация, воздух отравлен, так что вне Метро... Кстати, давай уточню - есть Метро, вот эта станция, а есть метро - остальная часть. Так вот... Вне станции без противогаза и фильтров тут много не навоюешь, сразу сляжешь, так что не забудь зайти к Сидоровичу, местному торговцу, у него можно приобрести много штучек - противогаз, фильтры, броню..."
                    text += "\nПротивогаз я тебе не достану, а вот немного фильтров у меня для тебя есть - как для старого друга, ха!_"
                    text += "\n\nС этими словами охранник вложил в твою ладонь фильтры и развернулся в сторону телепорта. В последнюю секунду, перед тем как исчезнуть, он повернул лицо в твою сторону, подмигнул и сказал: «Береги задницу!»"
                    text += "\n\nПолучено: х2 🕳Фильтры"
                    await db.addItem('Фильтры', user, arg='1')
                    await db.addItem('Фильтры', user, arg='1')
                    await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
                user.location = 'Метро'
                await user.save()
                return
            else:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                if user.frak != '' and user.frak != None:
                    frak = await db.Fraks.get_or_none(name=user.frak).first()
                    if frak:
                        markup.add(InlineKeyboardButton('База клана', callback_data="nav_bigcity_exit_clanBase"))
                text = "Случайный лес - место для новичков. Здесь можно разжиться и цветами для котелка и свитками, да и вообще тут монстры слабенькие, а вещей падает будь здоров.\n\nПесчаная пирамида - место для тех, кто уже запасся ресурсами. Сама пирамида большая, делится на несколько секторов. Больше золота, меньше вещей."
                markup.add(InlineKeyboardButton('Случайный лес', callback_data="nav_bigcity_exit_1"))
                markup.add(InlineKeyboardButton('Идти к башне', callback_data="nav_bigcity_exit_tower"))
                markup.add(InlineKeyboardButton('Песчаная пирамида', callback_data="nav_bigcity_exit_olimp"))
                if user.lvl > 10:
                    markup.add(InlineKeyboardButton('Заснеженная кавайня', callback_data="nav_bigcity_exit_ko4at"))
                    text += "\n\nЗаснеженная Кавайня - зимний город. Легко замёрзнуть, но сам город более развит своими технологиями."
                if user.lvl > 20:
                    text += "\n\nЭкспедиции - помоги Хэвенбургу! Отправься в разведку близлежащей местности, а мы тебе заплатим голдишком."
                    markup.add(InlineKeyboardButton('Экспедиции', callback_data="nav_bigcity_exit_expds"))
                if user.lvl < 30:
                    text += "\n\nСвалка SR - уникальное место. Огромное количество монстров не даёт передышки, однако количество получаемого опыта и золота снижено на 15%. Впрочем, всё это компенсируется гарантированным наличием свитков и зелий у каждого монстра, так что дефицита с ними не будет."
                    markup.add(InlineKeyboardButton('🆕Свалка SR🆕', callback_data="nav_bigcity_exit_SR"))
                if user.lvl > 30:
                    text += "\n\nРадар - гиблое место. Поговаривают что она похожа на ''Чернобыльскую Зону''. Хрен его знает что это, но в одиночку туда лучше не ходить."
                    markup.add(InlineKeyboardButton('Радар', callback_data="nav_bigcity_exit_radar"))
                if user.lvl > 45:
                    text += "\n\nОкеанический город место не из приятных. Чересчур высокая влажность воздуха, но люди умудряются там выживать - местная броня позволяет."
                    markup.add(InlineKeyboardButton('Океанический город', callback_data="nav_bigcity_exit_oceanus"))
                if user.lvl > 95:
                    text += "\n\nМетро - город опасностей и кринжа. Посмотри сам?"
                    markup.add(InlineKeyboardButton('🆕Метро🆕', callback_data="nav_bigcity_exit_metro"))
                await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти:", reply_markup=markup)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            if user.frak != '' and user.frak != None:
                frak = await db.Fraks.get_or_none(name=user.frak).first()
                if frak:
                    markup.add(InlineKeyboardButton('База клана', callback_data="nav_bigcity_exit_clanBase"))
            text = "Случайный лес - место для новичков. Здесь можно разжиться и цветами для котелка и свитками, да и вообще тут монстры слабенькие, а вещей падает будь здоров.\n\nПесчаная пирамида - место для тех, кто уже запасся ресурсами. Сама пирамида большая, делится на несколько секторов. Больше золота, меньше вещей."
            markup.add(InlineKeyboardButton('Случайный лес', callback_data="nav_bigcity_exit_1"))
            markup.add(InlineKeyboardButton('Идти к башне', callback_data="nav_bigcity_exit_tower"))
            markup.add(InlineKeyboardButton('Песчаная пирамида', callback_data="nav_bigcity_exit_olimp"))
            if user.lvl > 10:
                markup.add(InlineKeyboardButton('Заснеженная кавайня', callback_data="nav_bigcity_exit_ko4at"))
                text += "\n\nЗаснеженная Кавайня - зимний город. Легко замёрзнуть, но сам город более развит своими технологиями."
            if user.lvl > 20:
                text += "\n\nЭкспедиции - помоги Хэвенбургу! Отправься в разведку близлежащей местности, а мы тебе заплатим голдишком."
                markup.add(InlineKeyboardButton('Экспедиции', callback_data="nav_bigcity_exit_expds"))
            if user.lvl < 30:
                text += "\n\nСвалка SR - уникальное место. Огромное количество монстров не даёт передышки, однако количество получаемого опыта и золота снижено на 15%."
                markup.add(InlineKeyboardButton('🆕Свалка SR🆕', callback_data="nav_bigcity_exit_SR"))
            if user.lvl > 30:
                text += "\n\nРадар - гиблое место. Поговаривают что она похожа на ''Чернобыльскую Зону''. Хрен его знает что это, но в одиночку туда лучше не ходить."
                markup.add(InlineKeyboardButton('Радар', callback_data="nav_bigcity_exit_radar"))
            if user.lvl > 45:
                text += "\n\nОкеанический город место не из приятных. Чересчур высокая влажность воздуха, но люди умудряются там выживать - местная броня позволяет."
                markup.add(InlineKeyboardButton('Океанический город', callback_data="nav_bigcity_exit_oceanus"))
            if user.lvl > 95:
                text += "\n\nМетро - город опасностей и кринжа. Посмотри сам?"
                markup.add(InlineKeyboardButton('🆕Метро🆕', callback_data="nav_bigcity_exit_metro"))
            await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти:", reply_markup=markup)
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
        await call.answer()
    elif navWhere == "bar":
        checkitem = await db.Inventory.exists(name='Первый заход в бар', idplayer=user.id)
        if checkitem:
            text = "Подходя к тёмному зданию, над которым висит закопченная табличка, ты едва смог прочесть ''Бар''. О, так это тот самый бар, в котором тебе сделали татуировку на заднице."
            text += "\n\n\nЗайдя в бар, ты увидел лежащего возле выхода бомжа, вонь от которого выедала глаза, у барной стойки стоит охранник, которого ты спас от страшной операции лишения задницы, сидящий на стульчике человек в чёрном плаще, справа от него чёрный от уличной грязи игровой автомат, как их тут принято называть, на деле же - коробка с отверстием под монеты, и, собственно говоря, самого бармена, рыжие усы которого были больше его головы. Кажется, ты уже видел такие усы у одного из прохожих с надписью на лбу ''ПГТ Д.Ураков''"
        else:
            await db.addItem('Первый заход в бар', user, arg='1')
            checkitem = await db.Inventory.get(name='Первый заход в бар', idplayer=user.id).first()
            checkitem.active = 0
            await checkitem.save()
            text = "В темном переулке ты вдруг запнулся о тело знакомого бомжа, от вони которого защипало глаза.\n Отвернувшись и промакнув слезы обрывком белья Раскуловой ты увидел едва мерцающую надпись ''БАР'' над покосившейся дверью в стене напротив. В памяти всплывает диалог про выбор кланы, клеймо на заднице знакомо заныло...\n\nТак тааак... Хрустнув пальцами в кулаке, ты решительно входишь в покосившуюся дверь бара."
            text += "\n\nВнутри ты сразу поймал на себе изучающий взгляд человека в черном плаще, развалившегося на стуле за дальним столиком в компании полупустого стакана с желтоватой жидкостью.\nЗа стойкой возвышается ухмыляющийся бармен, вечно натирающий своим полотенцем один и тот же бокал для вина (вина в этом заведении никогда не бывало поэтому бокал не пользуется спросом).\n\nНемного потеряв решимость навалять за клеймо (в отсутствии подозреваемых) ты прошел к стойке, где видишь старого знакомого - это же охранник, чью задницу ты спас от неминуемой ампутации!"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Заказать выпить (20💰)', callback_data="bar_drink"))
        if user.lvl >= 7:
            markup.add(InlineKeyboardButton('Подойти к охраннику', callback_data="bar_ohr"))
        markup.add(InlineKeyboardButton('Сыграть на деньги', callback_data="bar_coin"))
        markup.add(InlineKeyboardButton('Игровой автомат', callback_data="bar_avto"))
        markup.add(InlineKeyboardButton('Кланы', callback_data="bar_clans"))
        markup.add(InlineKeyboardButton('Суббота', callback_data="bar_otrh"))
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await call.answer()
    elif navWhere == "trades":
        location = "Хэвенбург"
        position = "Место обмена"
        if user.location == location and user.position in ['Площадь', 'Место обмена']:
            await db.Users.filter(id=user.id).update(position='Место обмена')
        else:
            text = "Вы находитесь не на площади."
            await bot.send_message(call.message.chat.id, text)
            await call.answer()
            return
        if user.lvl < 5:
            text = "Трейды доступны с 5 уровня."
            await bot.send_message(call.message.chat.id, text)
            await call.answer()
            return
        else:
            pass
        result = await db.Users.filter(~Q(user_id=call.from_user.id), location=location, position=position)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for dict in result:
            markup.add(InlineKeyboardButton('{} ({}⭐️)'.format(dict.username, dict.tradenum), callback_data="trade_{}".format(dict.id)))
        text = "Выберите игрока, с которым хотите обменяться."
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интересное, чем тот мусор из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Поддержка игры', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предметы', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Недвижимость', callback_data="JiAlley"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await call.answer()
        return
    elif navWhere == "skupshik":
        checkQuest = await db.Quests.get_or_none(name='Скупщик. Знакомство', idplayer=user.id).first()
        if checkQuest and checkQuest.status == 2:
            text = "Стоит, значит, возле фонтана солидного вида бомж, к которому подойти не страшно. Поманив тебя пальцем, пытается купить у тебя всякий редкий хлам."
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Продажа хлама', callback_data="bomjsell"))
            if user.scenario == 1 and user.scenarioStatus >= 1:
                checkMap = await db.Inventory.exists(name='Документ DSFB-4', idplayer=user.id, active=1)
                if checkMap:
                    markup.add(InlineKeyboardButton('Спросить о DSFB-4', callback_data="scenarioFirst"))
            elif user.scenario == 2 and user.scenarioStatus == 2:
                markup.add(InlineKeyboardButton('Предупредить о переводе', callback_data="scenarioFirst"))
            elif user.scenario == 2 and user.scenarioStatus == 4:
                markup.add(InlineKeyboardButton('Спросить о переводе', callback_data="scenarioFirst"))
            elif user.scenario == 3:
                markup.add(InlineKeyboardButton('Задание: Универсальное оружие', callback_data="scenarioFirst"))
            elif user.scenario == 4 and user.scenarioStatus == 1: return await bot.edit_message_text("Подходя к обычному местоположению бомжа, никого не находишь...", call.message.chat.id, call.message.message_id)
            elif user.scenario == 4 and user.scenarioStatus == 2:
                await bot.edit_message_text("Подходя к бомжу, удивился. А бомжик-то другой! Это уже точно не тот, с которым ты постоянно раньше общался! Спросив о прошлом, этот ответил, мол, тот сгинул и никто его не видел, вот он и занял его место.\n\nСитуация усложняется, теперь единственная ниточка к Кларе - её муж, который, по слухам, отправился в Кавайню...", call.message.chat.id, call.message.message_id)
                await db.Users.filter(id=user.id).update(scenario=5, scenarioStatus=0)
                return
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await call.answer()
            return
        elif checkQuest and checkQuest.status == 1:
            checkItem = await db.Inventory.get_or_none(name='Положительный тест на беременность', idplayer=user.id, active=1).first()
            if checkItem:
                checkItem.active = 0
                await checkItem.save()
                await bot.send_message(call.message.chat.id, "Подходя к бомжу, протягиваешь ему пластинку.\n-Фу, мог бы и мочу с неё смыть! Или ты только что сам туда поссал? Хм, вроде нет... Ладно, спасибо...\n⚠️Квест выполнен\nНаграда: Доступ к скупщику + 1000💰")
                await db.Users.filter(id=user.id).update(money=F('money') + 1000)
                checkQuest.status = 2
                await checkQuest.save()
            else:
                await bot.send_message(call.message.chat.id, "Ну и чего ты пришёл? Давай быстрее приноси мне тест, уже не терпится...")
        else:
            plusText = await giveQuest(user, 'Скупщик. Знакомство')
            text = "Стоит, значит, возле фонтана солидного вида бомж, к которому подойти не страшно. Поманив тебя пальцем, пытается уломать тебя принести ему 🌡Положительный тест на беременность - дескать, хочет прикольнуться над своей женой, ей уже восьмой десяток идёт... Лично ты офигел от этого, но было бы неплохо заручиться репутацией.{}".format(plusText)
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "raskul":
        checkQuest = await db.Quests.get_or_none(name='Богиня Хэвенбурга', idplayer=user.id).first()
        if checkQuest and checkQuest.status==2 or user.lvl < 10:

            text = "Вы зашли внутрь здания и оказались в Аукционном доме Раскуловой.\n\nТут вы можете выставить свои предметы на продажу, либо же приобрести предметы других игроков"
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
            elif user.location == 'Метро':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_centr"))
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
            await bot.edit_message_text("Подойдя к входной двери, охрана остановила тебя, спросив допуск. К счастью, мимо проходила весьма сексуальная пышная девица, которая заинтересовалась тобой, отвела в сторону и предложила обмен - ты ей приносишь нижнее бельё, а она открывает тебе доступ к этому заведению. Конечно же ты согласился.\n-Кстати, можешь называть меня Раскуловой. Жду тебя внутри с одеждой.{}".format(plusText), call.message.chat.id, call.message.message_id)

    elif navWhere == 'hns':
        text = "🆕Открылось новое заведение от легендарного уничтожителя всех времён и народов - Адского... Сами-знаете-кого. Адский порядком устал косить монстров, поэтому решил заняться бизнесом - и вот, он представляет своё игровое заведение!"
        text += "\n\nПрятки - собирается пять человек. Из них одному достаётся цель - найти на местности других четверых и победить, а четверым - задание выжить во что бы то ни стало. Попробуем?"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Начать поиск', callback_data="partyHS_join"))
        markup.add(InlineKeyboardButton('ТОП-10', callback_data="partyHS_top"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif navWhere == 'toshen':
        text = "Шоколадная фабрика ТОшеН проводит небольшой интерактив в честь Дня Святого Валентина и предлагает каждому жителю Хэвенбурга заказать шоколад для своей второй половинки!"
        text += "\n\nСтоимость удовольствия - 500💰"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        #markup.add(InlineKeyboardButton('Сделать заказ', callback_data="toshen_create"))
        markup.add(InlineKeyboardButton('Общий список заказчиков', callback_data="toshen_all"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

class ToshenCreate(StatesGroup):
    create = State()

async def toshen_(call, user):
    #if call.data.split("_")[1] == 'create':
        #if user.money >= 500:
            #inventorySize = await db.getInventorySize(user)
            #if inventorySize + 1 > user.inventorySizeMax:
                #return await bot.edit_message_text("Нет места в инвентаре", call.message.chat.id, call.message.message_id)
            #await db.Users.filter(id=user.id).update(money=F('money') - 500)
            #await ToshenCreate.create.set()
            #await bot.edit_message_text("Введите текст записки, которую собираетесь поместить в шоколадку. Если записка не нужна - /cancel", call.message.chat.id, call.message.message_id)
        #else:
            #await bot.edit_message_text("У вас не хватает денег", call.message.chat.id, call.message.message_id)
    if call.data.split("_")[1] == 'all':
        allUsers = await db.IventArena.filter()
        text = "Список заказчиков валентинок:\n"
        for usr in allUsers:
            _usr = await db.Users.get_or_none(id=usr.idplayer).first()
            text += f"\n{_usr.username} - {usr.count} шт."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@dp.message_handler(state=ToshenCreate.create)
async def create_toshen(m: types.Message, state=FSMContext):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if m.text.lower() == '/cancel':
        expires = int(time.time()) + 2592000
        newItem = await db.Inventory.create(name="Валентинка", active=1, idplayer=user.id, size=1, type="Еда", expires=expires)
        await bot.send_message(m.chat.id, "Валентинка готова! Спасибо что пользуетесь услугами ТОшеН")
        await state.finish()
        await db.commitInventory(user, newItem)
        intop = await db.IventArena.get_or_none(idplayer=user.id)
        if intop:
            await db.IventArena.filter(id=intop.id).update(count=F("count") + 1)
        else:
            await db.IventArena.create(idplayer=user.id, count=1)
    else:
        if len(m.text) >= 255:
            await bot.send_message(m.chat.id, "Записка должна быть небольшой и иметь меньше 255 символов.")
        else:
            expires = int(time.time()) + 2592000
            newItem = await db.Inventory.create(name="Валентинка", descr=m.text, active=1, idplayer=user.id, size=1, type="Еда", expires=expires)
            await bot.send_message(m.chat.id, "Валентинка готова! Спасибо что пользуетесь услугами ТОшеН")
            await state.finish()
            await db.commitInventory(user, newItem)
        intop = await db.IventArena.get_or_none(idplayer=user.id)
        if intop:
            await db.IventArena.filter(id=intop.id).update(count=F("count") + 1)
        else:
            await db.IventArena.create(idplayer=user.id, count=1)



async def expeds(call, user):
    award12h = user.lvl * 50 + 1000
    award6h = user.lvl * 21 + 500
    award3h = user.lvl * 10 + 250
    award1h = user.lvl * 4 + 100
    checkHome = await db.Houses.get_or_none(owner=user.id)
    if checkHome:
        text = """Экспедиции - уникальная возможность исследования локаций которая может приглянуться каждому. Во время экспедиций нужно следить за своим здоровьем, но данный вид деятельности уникален тем что экспедиции проводятся в местах без монстров. Ниже перечислены все виды и награды экспедиций.

        Часовая экспедиция - ~{}💰, x1 🍗, ~1-3✨🏚
        Трёхчасовая экспедиция - ~{}💰, x2 🍗, ~3-9✨🏚
        Шестичасовая экспедиция - ~{}💰, x2 🍗, ~9-35✨🏚
        Двенадцатичасовая экспедиция - ~{}💰, x4 🍗, ~18-50✨🏚

    Выберите время экспедиции. Денежная награда с экспедиций зависит от вашего уровня.
    ⚠️Внимание. Если вы откажетесь от экспедиции до её окончания, награды получены не будут!
    Отказаться от экспедиции вы можете, использовав свиток телепортации.
    """.format(award1h, award3h, award6h, award12h)
    else:
        text = """Экспедиции - уникальная возможность исследования локаций которая может приглянуться каждому. Во время экспедиций нужно следить за своим здоровьем, но данный вид деятельности уникален тем что экспедиции проводятся в местах без монстров. Ниже перечислены все виды и награды экспедиций.

        Часовая экспедиция - ~{}💰, x1 🍗
        Трёхчасовая экспедиция - ~{}💰, x2 🍗
        Шестичасовая экспедиция - ~{}💰, x2 🍗
        Двенадцатичасовая экспедиция - ~{}💰, x4 🍗

    Выберите время экспедиции. Денежная награда с экспедиций зависит от вашего уровня.
    ⚠️Внимание. Если вы откажетесь от экспедиции до её окончания, награды получены не будут!
    Отказаться от экспедиции вы можете, использовав свиток телепортации.
    """.format(award1h, award3h, award6h, award12h)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('1 час', callback_data="expedition_1"))
    markup.add(InlineKeyboardButton('3 часа', callback_data="expedition_2"))
    markup.add(InlineKeyboardButton('6 часов', callback_data="expedition_4"))
    markup.add(InlineKeyboardButton('12 часов', callback_data="expedition_3"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def expedition_(call, user):
    btl = call.data.split('_')
    do = btl[1]
    if do == '1': timeEnd = int(time.time()) + 3600 # 1 h
    if do == '2': timeEnd = int(time.time()) + 10800 # 3 h
    if do == '3': timeEnd = int(time.time()) + 43200 # 12 h
    if do == '4': timeEnd = int(time.time()) + 21600 # 6 h
    if user.location == 'Хэвенбург':
        newExpedition = await db.Expeditions(idplayer=user.id, timeEnd=timeEnd, expType=do)
        await newExpedition.save()
        user.location = 'Экспедиция'
        await user.save()
        await bot.edit_message_text("Вы успешно отправились в экспедицию.", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)

@dp.message_handler(lambda m:m.text and m.text.startswith('/kach_'))
async def bigkach(m): 
    try:
        await dp.throttle(str(m.from_user.id), rate=1)
    except exceptions.Throttled:
        return
    if (m.from_user.id == m.chat.id):
        pass
    else:
        return
    result = m.text.replace('/kach_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    user = await db.Users.get(user_id=m.from_user.id)
    if user.location in ['Город', 'Хэвенбург', 'Радар', 'Океанус', 'Кавайня', 'Метро']:
        pass
    else:
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if user.location == 'Хэвенбург': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
    elif user.location == 'Кавайня': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_wintercity_centr"))
    elif user.location == 'Океанус': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_oceanus_centr"))
    elif user.location == 'Радар': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_radar_centr"))
    elif user.location == 'Метро': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_metro_centr"))
    elif user.location == 'Город': markup.add(InlineKeyboardButton('Выйти', callback_data="nav_city_centr"))
    if result == 'atk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if (user.money - needAtk) >= 0:
            user.atk = user.atk + 1
            user.money = user.money - needAtk
            await db.Users.filter(id=user.id).update(money=user.money, atk=user.atk)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needAtk
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(needAtk))
            if needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +1 атаки".format(user.username))
            await achprog(user, ach='kachalka')
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + 1)
        else:
            await bot.send_message(m.chat.id, "У вас не хватает денег", reply_markup=markup)    
    elif result == 'halfatk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if user.money > needAtk:
            money = int(user.money / 2)
            needMoney = 0
            count = 0
            while money > needAtk:
                needAtk = int(3 * ((atk - 4) / 2))
                money -= needAtk
                needMoney += needAtk
                atk += 1
                count += 1
            user.atk = atk
            user.money = user.money - needMoney
            await db.Users.filter(id=user.id).update(money=user.money, atk=user.atk)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needMoney
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Вы улучшили атаку на {} ед.\n\nТекущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(count), str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(_needAtk))
            if _needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if _needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +{} атаки".format(user.username, count))
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + count)
    elif result == 'fullatk':
        atk = user.atk
        needAtk = int(3 * ((atk - 4) / 2))
        if user.money > needAtk:
            money = user.money
            needMoney = 0
            count = 0
            while money > needAtk:
                needAtk = int(3 * ((atk - 4) / 2))
                money -= needAtk
                needMoney += needAtk
                atk += 1
                count += 1
            user.atk = atk
            user.money = user.money - needMoney
            await db.Users.filter(id=user.id).update(money=user.money, atk=user.atk)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needMoney
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Вы улучшили атаку на {} ед.\n\nТекущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(count), str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(_needAtk))
            if _needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if _needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +{} атаки".format(user.username, count))
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + count)
    elif result == 'hp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if (user.money - needHp) >= 0:
            user.hp = user.hp + 1
            user.nowhp = user.nowhp + 1
            user.money = user.money - needHp
            await db.Users.filter(id=user.id).update(hp=user.hp, nowhp=user.nowhp, money=user.money)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needHp
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(hp), str(user.atk), str(user.money))
            text = "Текущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(_needAtk))
            if _needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if _needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +1 хп".format(user.username))
            await achprog(user, ach='kachalka')
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + 1)
        else:
            await bot.send_message(m.chat.id, "У вас не хватает денег", reply_markup=markup)          
    elif result == 'halfhp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.money > needHp:
            money = user.money / 2
            needMoney = 0
            count = 0
            while money > needHp:
                needHp = int(3 * ((hp - 9) / 2))
                money -= needHp
                needMoney += needHp
                hp += 1
                count += 1
            user.hp = hp
            user.nowhp = user.hp
            user.money = user.money - needMoney
            await db.Users.filter(id=user.id).update(hp=user.hp, nowhp=user.nowhp, money=user.money)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needMoney
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Вы улучшили здоровье на {} ед.\n\nТекущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(count), str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(_needAtk))
            if _needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if _needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +1 хп".format(user.username))
            await achprog(user, ach='kachalka')
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + 1)
    elif result == 'fullhp':
        hp = user.hp
        needHp = int(3 * ((hp - 9) / 2))
        if user.money > needHp:
            money = user.money
            needMoney = 0
            count = 0
            while money > needHp:
                needHp = int(3 * ((hp - 9) / 2))
                money -= needHp
                needMoney += needHp
                hp += 1
                count += 1
            user.hp = hp
            user.nowhp = user.hp
            user.money = user.money - needMoney
            await db.Users.filter(id=user.id).update(hp=user.hp, nowhp=user.nowhp, money=user.money)
            await achprog(user, ach='kachalka')
            if user.quest == 'Качок' and user.questStatus == 1:
                quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                quest.progress += needMoney
                await quest.save()
            atk = user.atk
            hp = user.hp
            _needAtk = int(3 * ((atk - 4) / 2))
            _needHp = int(3 * ((hp - 9) / 2))
            halfmoney = int(user.money / 2)
            text = "Вы улучшили здоровье на {} ед.\n\nТекущее здоровье: {}\nТекущая атака: {}\nБаланс: {}💰\n\n".format(str(count), str(hp), str(user.atk), str(user.money))
            text += "\nУлучшить навык +1 💢Атака - {}💰 /kach_atk".format(str(_needAtk))
            if _needAtk * 2 < halfmoney:
                text += "\nУлучшить навык 💢Атака на {}💰 /kach_halfatk".format(str(halfmoney))
                if _needAtk * 4 < user.money:
                    text += "\nУлучшить навык 💢Атака на {}💰 /kach_fullatk".format(str(user.money))
            text += "\n\nУлучшить навык +1 ❤️Здоровье - {}💰 /kach_hp".format(str(_needHp))
            if _needHp * 2 < halfmoney:
                text += "\nУлучшить ❤️Здоровье на {}💰 /kach_halfhp".format(str(halfmoney))
                if _needHp * 4 < user.money:
                    text += "\nУлучшить ❤️Здоровье на {}💰 /kach_fullhp".format(user.money)
            await bot.send_message(m.chat.id, text, reply_markup=markup)
            closeLog = -1001305857653
            await logBot.send_message(closeLog, "{} купил +1 хп".format(user.username))
            await achprog(user, ach='kachalka')
            if await db.Referals.exists(idplayer=user.id):
                await db.Referals.filter(idplayer=user.id).update(uppedStats=F('uppedStats') + 1)




async def navgo(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    user.progStatus = 1
    await user.save()
    await bot.edit_message_text("Вы отправились в исследование дальше.", call.message.chat.id, call.message.message_id)
    if user.location == "Свалка SR":
        await asyncio.sleep(5)
        await user.refresh_from_db()
        await giveMobSR(user)


async def navstop(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    user.progStatus = 0
    await user.save()
    await bot.edit_message_text("Ты остановился и топчешься на месте.", call.message.chat.id, call.message.message_id)

async def navback(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    if user.location in ['Первый этаж башни', 'Второй этаж башни', 'Третий этаж башни', 'Четвёртый этаж башни']:
        user.progStatus = 2
        await user.save()
        await bot.edit_message_text("Пафосно развернувшись на 180°, ты пошёл обратно.", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Доступно только в башне", call.message.chat.id, call.message.message_id)
        return


bartext = ['Можно попасть в гробницу, если на К-35  тебе не помешает злобная эльфийка', 'Если ты здоров, то идти в источники нет нужды, но я люблю поглазеть на голых девиц😏', 
            'После К-40 ничего нет. Вот такие дела, а теперь заплати за меня, я нищеброд.', 'Eсли сожрать 🥒Большой хер огра он восстановит твою шкалу голода, но мне кажется тут есть какой-то подтекст белого цвета...',
            'Эй ты! Да, ты голодранец, попробуй продать что-то в 🏦Ломбард и может тебе хватит денег чтобы прикрыть свой голый зад.', 'Йоу, ох и нажрался же я сегодня, в 🏪Магазине у Ашота лучший выбор алкоголя, а ещё он варит 🧪зелья здоровья. Но тебе они не помогут, тебя и так никто не нападёт, из жалости конечно...',
            'С Новым Годом! Или не новым, пёс его знает. Я всегда теряю контроль когда вижу 👩‍💼Раскулову. У неё кстати тут есть свой бизнес, она пропускает тебя на Арену всего за 30 монет, только приходи здоровенький, не позорься!', 
            'Слушай, у тебя не будет пару 🥒Херов огра долгануть? Нет? А жаль... Но если захочешь с кем-то поделится то приходи в ⚖️Трейды и выбирай с кем хочешь обменяться', 'Йоу, а ты секси! Не не не, я не подкатываю, упаси бог. Хотя если вдруг ты захочешь кхм-кхм или просто восстановить ⚡️ то заходи в 🏫Отель, там не дорого, всего 5 монет и царская конура твоя!',
            'Как оно? Видел того 👨🏽‍🦳Бомжа на улице? Говорят он скупает всякую дрянь, даже 🌡тест на беременность твоей сестры возьмёт! Откуда я знаю про сестру? Нуууу... Мне пора в общем...', 'Привет, это конечно не моё дело, но выглядишь ты хуже сутулой собаки😬 Ты бы в 🏋️‍♂️Качалку что-ли сходил, приведи уже себя в форму бля, 💢Атаку и ❤️Здоровье ж качать можно.',
            'Здарова братиш, мне тут один хмырь по пьяни проговорился что в 🏦Ломбарде всего за 50💎 можно купить какую-то чудо коробку!', 'Уххх, ну и набрался же я сегодня, ща блевану! Нет, не блевану. Или блевану. Короче, слушай пока не блеванул. Все охотятся за этими 🎟Бесплатными путёвками на свалку, а они на самом деле пустышки! Их только тому 👨🏽‍🦳Бомжу продавать и то хрен знает купит ли. А вот теперь я точно бл *звуки блевания*',
            'Шо ты тут? Ништяк? Ну это кайф конечно, слушай а ты когда нибудь забывал взять с собой 📜Свиток телепортации?  Да, да, да, я тоже иногда забываю, но если зайти в 🏦Ломбард и купить 🏺Амфору экстренной помощи за 5💎 можно будет достать его оттуда, как кролика! Представляешь?', 'Я оборванец? Нееее браток, это я Люцифера👹 встретил. Кажется эта падла мне почки отбила. Мой тебе совет, увидишь эту нечисть, беги без оглядки!',
            'Пссс. Эй ты, тебя часом не достали в твоей фракции? Я знаю одно местечко, там можно перебить штам на жопе, да, срать ты не сможешь пару дней, но зато новая фракция! Так вот идёшь в 🏦Ломбард и просишь там Смену кланы всего за 50💎 тебя перештампуют и будешь как новенький!',
            'Браток, а чего это ты зелье в зубах таскаешь? у тебя что-ли в 🎒рюкзаке места нет? Понимаю, лан помогу тебе немного. Есть тут один умелец карманы на рюкзак пришивать живёт он в 🏦Ломбарде, заходишь туда и просишь +5📦 и тебе за умеренную плату нашьют целых 5 карманов!',
            'Йо, братик. А чего ты такой худой, а? Опять 🍗еду дома забыл? Ну ты село конечно, ору. Крч лови варик как поднять 🍗еды. Двигай в 🏦Ломбард, там скажешь что от меня и дашь 5💎 тебе отсыпят 1к 🍗хавки!!! Ток ты смотри, не хавай потом, а то лопнешь!',
            'Честно говоря дружочек, я тебя не уважаю. Ходишь тут, рыскаешь где не надо. Вломить бы тебе, да рука на животное не поднимается...', 'Привет! Как сам? Как здоровье? Как жена? А детишки как? Скажи погода хорошая? А ты Лавовый куб видел когда-то? А куда в лесу уже доходишь? Ну ладно, мне пора! Было приятно поболтать!', 'Уйди, не до тебя сейчас.', 'А ты знаешь что в нашем мире самое тяжёлое? Вот и  я не знаю...', 'Был уже в Дурке? Очень тебе советую!',
            'Слушай, я раньше этого никому не говорил, но я обожаю ссать с Небесной башни на головы тех кто внизу ждёт🤣. А ты чего мокрый такой?', 'Ла-ла-ла, жу-жу-жу, я с тобою не дружу. Отсядь пожалуйста...', 'Что было раньше, Крипер или Хэдкраб?', 'Я люблю розовых фламинго и киви. Спасибо что выслушал, мне это было нужно.', 'Если злую собаку превратить в Сильвану, получится злая сука, ахахахахаха...', 'АУФ Братишка! *вы решили пересесть от прокаженного*', 'О-о-о-о-о Зеленоглазоееее таксиии притормози, притормози! .... Чего уставился? Проваливай!',
            'Ты в курсе что за нами следят? Я вот вчера свою байку увидел на канале в Телеграм. Ох уж этот Дуров...', 'А ты знал что бывает не только Адский пёс, но и Адский Дрочила?', 'Видел вчера в Пирамиде двух близняшек, так вот, у меня не встал. У мужиков такое бывает, один разок из пяти...', 'На самом деле я не в смокинге, а в спортивках. Извини уж за такой наёб.', 'Видел вчера петуха, хотел было его пнуть, подхожу ближе, а это @kakushigoto. Но я всё равно пнул, уж больно обнову хочется...',
            'Знаешь как расшифровывается ФОО? Форум Окультивных Ондатр.', 'Когда я был маленьким, мама говорила что я стану великим человеком. И вот я вырос и всё что у меня есть, этот бар. Ну и ты конечно, заметь, теперь ты не пустое место.', 'Смотри, вот Люцифера мы видели в Пирамиде, Тебя в Лесу, меня в баре. А Бога нет🌚', 'Вижу ты куришь. Мамка мало лупила в детстве что-ли?',
            'Ох ты и оделся. Но смущает лишь одно, гей парады - проводить запрещено.', 'Здесь слова не понимают, здесь боятся острых слов. Здесь с почётом принимают тех кто вовсе без голов.', 'Ну и на кой ты сюда пришёл? Я тебе что, генератор смешных фраз? Любишь использовать людей в своих целях? Относишься как к должному? А ну пшёл отсюда, хап тьфу тебе в глаз', 'Ох братан, ты как? А я вот дерьмово, хотел увидеться с девушкой, спрашиваю, "Когда?" А она говорит, "Скоро". Ну я такой немного не понял и говорю, "Это же не ответ" . И знаешь что она мне сказала? "Ну да". Ну я и прикопал её в лесу...',
            'Вот скажи мне, тебе нравятся секасные лысые мужики? Мне вот да, особенно если они делают крутые штуки из 🧊Снунцев. Ты как надумаешь заходи к 🧑‍🦲Лысому из Бруzzерс. Только там с 20. Не вздумай соваться раньше, извращуга!', 'Говорят в Кавайне можно говорить " Ня! Кавай😊" и не отхватить по лицу. Но это не точно.',
            'Слуууушай, помнишь же 👩‍💼Раскулову? У меня до сих пор стояк. Так вот к чему это я, она теперь открыла свою торговую площадку, заходи, может купишь себе чего, а то как @renanv...', 'Говорят в Кавайне есть такой же 🌲Случайный лес, только ❄️Заснеженный. Кажется в нас пропадает дух оригинальности...', 'А ты уже слышал про новые шмотки для холодной погоды? Ты не поверишь но 🩳Летние шорты защищают от холода лучше всего. Целых 52🛡, да ещё и -5%❄️ в придачу, а стоят всего 🧊 2375',
            'Валеееера это ты? Не узнал что-ли? Это же я, 👨🏾‍🦳Бомж! Так вот, ты прикинь, у меня теперь есть 🛡Самонагревающаяся покрышка, а это +40🛡 и -15%❄️ почти как на теплотрассе у ⛲️Источников. Я её честно реквизировал, но ты можешь купить всего за 🧊 2500', 'Уже видел новый кусок ДВП в Кавайне? Говорят он знает сколько у кого 🧊Снунцев. Куедемоны, или куебесы, не иначе!', 'Ты водишь!', 'О, это ты мне пивка купил? Спасибо, братиш)', 'Мне кажется в ❄️Заснеженном лесу холодно, одевайся потеплее и ☕️Кофейку не забудь!']


async def bar(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    bar = _kach[1]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if user.location not in ['Хэвенбург', 'Кавайня']:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)
        return
    if bar == 'drink':
        checkQuest = await db.Quests.get_or_none(name='Я просто хотел выпить...', idplayer=user.id).first()
        if checkQuest and checkQuest.status == 2:
            if user.money >= 20:
                user.money -= 20
                await user.save()
            else:
                await bot.edit_message_text('Проваливай отсюда, бомжара очередной!', call.message.chat.id, call.message.message_id)
                return
            randtext = random.choice(bartext)
            text = "Вы взяли себе ещё бокал, а тот стремный человек в чёрном смокинге снова начал вам рассказывать\n"
            text += "_{}_".format(randtext)
            markup.add(InlineKeyboardButton('Заказать выпить (20💰)', callback_data="bar_drink"))
            markup.add(InlineKeyboardButton('Подойти к охраннику', callback_data="bar_ohr"))
            markup.add(InlineKeyboardButton('Сыграть на деньги', callback_data="bar_coin"))
            
            if user.location == 'Кавайня':
                markup.add(InlineKeyboardButton('х3 ставки', callback_data="bar_jackpot"))
            
            markup.add(InlineKeyboardButton('Игровой автомат', callback_data="bar_avto"))
            markup.add(InlineKeyboardButton('Кланы', callback_data="bar_clans"))
            markup.add(InlineKeyboardButton('Выйти', callback_data="nav_bigcity_centr"))
            await achprog(user, ach='alcohol')
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        elif checkQuest and checkQuest.status == 1:
            if user.uppts >= 1:
                await db.Users.filter(id=user.id).update(uppts=F('uppts') - 1)
                checkQuest.status = 2
                await checkQuest.save()
                await bot.send_message(call.message.chat.id, "Гууууд... Ну, дружок, добро пожаловать в бар!\n⚠️Задание выполнено. Потеряно: 1🔘\nОткрыт доступ к выпивке.")
            else:
                await bot.send_message(call.message.chat.id, "Бармен, увидев тебя, спросил как там дела с твоим 🔘Очком. Увы, у тебя с этим были небольшие трудности...")
        else:
            plusText = await giveQuest(user, "Я просто хотел выпить...")
            await bot.edit_message_text("-Эх, щас бы пивка... Бармен, налей мне!\nБармен, стоявший за стойкой, обернулся. Ох, какая же это была глыба! Метра две, не меньше!\nСначала тебя удивил голос... Писклявый голос 15летней девочки...\nСлыш, дружок, я тебя впервые вижу. У нас заведено платить вступительные, так что с тебя 1 🔘Очко прокачки. Потом поговорим.{}".format(plusText), call.message.chat.id, call.message.message_id)


    elif bar == 'ohr':
        if user.scenario == 5 and user.scenarioStatus == 0:
            await scenarioSecond(call,user)
        else:
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
            if user.lvl >= 7:
                text, status = await questsglobal(user)
                if status != 0:
                    markup.add(InlineKeyboardButton('Сменить задание (200💰)', callback_data="quest_change"))
            else:
                text = "Тебе сюда нельзя, проходи, не задерживайся!"
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif bar == 'coin':
        games = await db.Coin.filter(~Q(player1=user.id), status=1)
        text = "Выберите игру:\n"
        if games:
            for z in games:
                playervs = await db.Users.get(id=z.player1)
                text += "\n{} - {}{} /play_coin_{}".format(playervs.username, z.bet, z.valute, z.id)
        else:
            text += "\nАктивных игр сейчас нет, но ты можешь создать свою!"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Создать игру', callback_data="coin_start"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return
    elif bar == 'avto':
        CommisionFond = await db.System.get(name='fondGame')
        user = await db.Users.get(user_id=call.from_user.id)
        text = "\nБаланс: {}💰\n\nПодойдя к автомату, бармен торжественно проговорил:\n_Если тебе повезёт, то за 50💰 ты сможешь выиграть целых {}💰. Но не думай, что всё так просто, всё зависит от твоей удачи!_".format(user.money, CommisionFond.value)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Начать игру', callback_data="bar_avtoStart"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
        try:
            await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        except:
            pass
    elif bar == 'avtoStart':
        CommisionFond = await db.System.get(name='fondGame')
        BuzyAvtomat = await db.System.get(name='buzyAvto')
        if BuzyAvtomat.value == 0:
            user = await db.Users.get(user_id=call.from_user.id)
            await db.System.filter(name='buzyAvto').update(value=1)
            if user.money >= 50:
                user.money -= 50
                await db.Users.filter(id=user.id).update(money=F('money') - 50)
                await db.System.filter(name='fondGame').update(value=F('value') + 35)
                await db.System.filter(name='HeavenFondGold').update(value=F('value') + 15)
                text = "\nБаланс: {}💰\nТекущий куш: {}💰.\nВы бросаете монетку...".format(user.money, CommisionFond.value)
                rand = random.randint(1, 1000)
                if rand <= user.luckerAvtomat + 5:
                    await logBot.send_message(tradeChat, "Игрок {} сорвал куш в автомате в размере {}💰".format(user.username, CommisionFond.value))
                    await bot.send_message(-1001345068459, "Игрок {} сорвал куш в автомате в размере {}💰".format(user.username, CommisionFond.value))
                    text += "\n\nВнезапно бар содрогнулся - это бармен достал из-под стойки мешок с деньгами, торжественно поздравляя тебя с победой. В мешке оказалось {}💰".format(CommisionFond.value)
                    await db.Users.filter(id=user.id).update(money=F('money') + CommisionFond.value)
                    await achprog(user, ach='igrovoiAvtomat')
                    await db.System.filter(name='fondGame').update(value=0)
                else:
                    text += "\nБросив монетку, ничего не произошло. Может стоит попробовать еще раз?"
            else:
                text = "\nПодойдя к автомату, бармен рассмеялся и сказал что ставка для игры непосильна для такого бомжа как ты. Тебе нужно иметь 50💰"
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Сыграть еще раз', callback_data="bar_avtoStart"))
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
            try:
                await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
            except:
                pass
            BuzyAvtomat.value = 0
            await BuzyAvtomat.save()
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Автомат сейчас занят другим посетителем.")
            return

    elif bar == 'jackpot':
        games = await db.CoinJackpot.filter(winner=-1)
        text = "Выберите игру:\n"
        if games:
            for z in games:
                if z.player1 != user.id:
                    if z.player2:
                        if z.player2 != user.id:
                            player1 = await db.Users.get(id=z.player1)
                            player2 = await db.Users.get(id=z.player2)
                            text += "\n{} + {} - {}💰 /play_tCoin_{}".format(player1.username, player2.username, z.bet, z.id)
                        else:
                            text += "\nВаша игра #{}. Ставка: {}💰".format(z.id, z.bet)
                    else:
                        player1 = await db.Users.get(id=z.player1)
                        text += "\n{} - {}💰 /play_tCoin_{}".format(player1.username, z.bet, z.id)
                else:
                    text += "\nВаша игра #{}. Ставка: {}💰".format(z.id, z.bet)
        else:
            text += "\nАктивных игр сейчас нет, но ты можешь создать свою!"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Создать игру', callback_data="coinJackpot"))
        if user.location == 'Хэвенбург':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
        elif user.location == 'Кавайня':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_bar"))
        elif user.location == 'Радар':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_bar"))
        elif user.location == 'Метро':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_bar"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return

    elif bar == 'clans':
        clans = await db.Fraks.filter()
        clansCount = await db.Fraks.filter(id__gte=2).count()
        text = "В мире зарегистрировано {} кланов. Список и информация о каждом:\n\n".format(clansCount)
        for clan in clans:
            if clan.id not in [1, 0]:
                text += "\n{} - /clanInfo_{}".format(clan.name, clan.id)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if user.lvl >= 75:
            markup.add(InlineKeyboardButton('Создать свой клан', callback_data="createClan"))
        if user.location == 'Хэвенбург':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
        elif user.location == 'Кавайня':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_bar"))
        elif user.location == 'Радар':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_bar"))
        elif user.location == 'Метро':
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_metro_bar"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        return

    elif bar == "otrh":
        fondMoney = await db.System.get(name='HeavenFondGold')
        fondKri = await db.System.get(name='HeavenFondKri')
        otrh_phare = ["Чо смотришь, гони бабло",
                        "Нет бабла и нет субботы",
                        "Поддержи фонд ленивого зайца",
                        "Хочу кучу бабла, которую не смогу перепрыгнуть"]
        phare = random.choice(otrh_phare)

        text = "Кажется ты зашел в кабинет какого-то плохого человека"
        text += '\nПока он повернут к тебе спиной, ты видишь как он смотрит на большой монитор'
        text += ' на котором было написано:'
        text += f'\n\n{fondMoney.value}/25000000💰\n1000/1000💎\n'
        text +='\n\nПока ты смотрел на этот монитор, человек уже повернулся к тебе и сказал:'
        text += f'\n-{phare}'
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Внести 💰', callback_data="otrh_pasd_gold"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return


class OtrhPasd(StatesGroup):
    gold = State()

async def otrh_pasd(call, user):
    if call.data.split("_")[2] == 'gold':
        await OtrhPasd.gold.set()
        await bot.edit_message_text(f"Введи сумму, которую желаешь внести\nУ тебя {user.money}💰", call.message.chat.id, call.message.message_id)
    else:
        await OtrhPasd.kri.set()
        await bot.edit_message_text(f"Введи сумму, которую желаешь внести\nУ тебя {user.almaz}💎", call.message.chat.id, call.message.message_id)
    pass

@dp.message_handler(state=OtrhPasd.gold)
async def otrh_pasd_gold(m: types.Message, state=FSMContext):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if m.text.isdigit() and user:
        if user.money >= int(m.text) and int(m.text) > 0:
            await db.Users.filter(id=user.id).update(money=F('money') - int(m.text))
            await db.System.filter(name='HeavenFondGold').update(value=F('value') + int(m.text))
            await logBot.send_message(tradeChat, f"Игрок {user.username} засубботил {m.text}💰")
            await bot.send_message(1175149001, f"Игрок {user.username} засубботил {m.text}💰")
            await m.answer("Готово!")
        else:
            await m.answer("Ошибка")
    else:
        await m.answer("Ошибка")
    await state.finish()
    

coinUserStatus = {}

async def coinJackpot(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    allBetsFromUser = await db.CoinJackpot.filter(winner=-1, player1=user.id).count()
    allBetsFromUser1 = await db.CoinJackpot.filter(winner=-1, player1=user.id).count()
    allBetsFromUser2 = await db.CoinJackpot.filter(winner=-1, player2=user.id).count()
    allBetsFromUser3 = await db.CoinJackpot.filter(winner=-1, player2=user.id).count()
    if allBetsFromUser + allBetsFromUser1 + allBetsFromUser2 + allBetsFromUser2 + allBetsFromUser3 > 5:
        await bot.send_message(call.message.chat.id, "Вы можете создавать не больше 5 ставок")
    else:
        commision = await db.System.get(name='commisionCoinTriple')
        text = "Введите сумму ставки. У вас {}💰\n\nКомиссия на тройной коин составляет {}%".format(user.money, commision.value)
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
        coinUserStatus[call.from_user.id] = 'coinJackpot'

@dp.message_handler(lambda m: coinUserStatus and m.from_user.id == m.chat.id and m.from_user.id in coinUserStatus and coinUserStatus[m.from_user.id]=='coinJackpot')
async def coinBetJackpot(m):
    user = await db.Users.get(user_id=m.from_user.id)
    coinUserStatus[m.from_user.id] = None
    if user.location != 'Кавайня':
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    try:
        if int(m.text) >= 100:
            if user.money >= int(m.text):
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                allBetsFromUser = await db.CoinJackpot.filter(winner=-1, player1=user.id).count()
                allBetsFromUser1 = await db.CoinJackpot.filter(winner=-1, player1=user.id).count()
                allBetsFromUser2 = await db.CoinJackpot.filter(winner=-1, player2=user.id).count()
                allBetsFromUser3 = await db.CoinJackpot.filter(winner=-1, player2=user.id).count()
                if allBetsFromUser + allBetsFromUser1 + allBetsFromUser2 + allBetsFromUser2 + allBetsFromUser3 > 5:
                    await bot.send_message(call.message.chat.id, "Вы можете создавать не больше 5 ставок")
                    return
                timeEnd = int(time.time()) + 604800
                game = await db.CoinJackpot(player1=user.id, bet=int(m.text), winner=-1, fond=int(m.text), timeEnd=timeEnd)
                await game.save()
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_wintercity_bar"))
                commision = await db.System.get(name='commisionCoinTriple')
                await db.Users.filter(id=user.id).update(money=F("money") - game.bet)
                await bot.send_message(m.chat.id, "Вы успешно создали игру #{} на {}💰".format(game.id, game.bet))
            else:
                await bot.send_message(m.chat.id, "У вас не хватает денег")
        else:
            await bot.send_message(m.chat.id, "Сумма ставки должна быть не менее 100💰.")
    except:
        await bot.send_message(m.chat.id, "Скорее всего, вы ввели сумму не в цифрах. Попробуйте создать игру заново.")






async def coinStart(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    allBetsFromUser = await db.Coin.filter(status=1, player1=user.id).count()
    allBetsFromUser1 = await db.Coin.filter(status=0, player1=user.id).count()
    if allBetsFromUser + allBetsFromUser1 > 5:
        await bot.send_message(call.message.chat.id, "Вы можете создавать не больше 5 ставок")
    else:
        commision = await db.System.get(name='commisionCoin')
        commisionKri = await db.System.get(name='commisionCoinKri')
        text = "Введите сумму ставки. У вас {}💰 {}💎".format(user.money, user.almaz)
        await bot.send_message(call.message.chat.id, text, parse_mode='markdown')
        coinUserStatus[call.from_user.id] = 'stavka'

@dp.message_handler(lambda m: coinUserStatus and m.from_user.id == m.chat.id and m.from_user.id in coinUserStatus and coinUserStatus[m.from_user.id]=='stavka')
async def coinBet(m):
    user = await db.Users.get(user_id=m.from_user.id)
    coinUserStatus[m.from_user.id] = None
    if user.location != 'Хэвенбург':
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    try:
        if int(m.text) >= 100:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            games = await db.Coin.filter(player1=user.id, status=0).count()
            if games > 5:
                await bot.send_message(m.chat.id, "Нельзя создавать так много игр")
                return
            game = await db.Coin(player1=user.id, bet=int(m.text), status=0)
            await game.save()
            markup.add(InlineKeyboardButton('💰', callback_data="coinBet_{}_gold".format(game.id)))
            markup.add(InlineKeyboardButton('💎', callback_data="coinBet_{}_almaz".format(game.id)))
            markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
            commision = await db.System.get(name='commisionCoin')
            commisionKri = await db.System.get(name='commisionCoinKri')
            await bot.send_message(m.chat.id, "Выберите валюту игры. Комиссия на игры на 💰 составляет {}%, а на 💎 - {}%".format(commision.value, commisionKri.value), reply_markup=markup)
        else:
            await bot.send_message(m.chat.id, "Сумма ставки должна быть не менее 100💰.")
    except:
        await bot.send_message(m.chat.id, "Скорее всего, вы ввели сумму не в цифрах. Попробуйте создать игру заново.")

async def coinBetSelectValute(call, user):
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    gameId = _kach[1]
    valute = _kach[2]
    game = await db.Coin.exists(id=gameId)
    if not game:
        await bot.edit_message_text("Создавай игру заново, тут ашипка", call.message.chat.id, call.message.message_id)
        return
    game = await db.Coin.get(id=gameId)
    if valute == 'gold':
        if user.money >= game.bet:
            game.valute = '💰'
            game.status = 1
            game.timeEnd = int(time.time()) + 604800
            await game.save()
            user.money -= game.bet
            await user.save()
            await bot.edit_message_text("Вы создали игру #{} на {}💰".format(game.id, game.bet), call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("У вас не хватает 💰", call.message.chat.id, call.message.message_id)
    elif valute == 'almaz':
        if user.almaz >= game.bet:
            game.valute = '💎'
            game.status = 1
            game.timeEnd = int(time.time()) + 604800
            await game.save()
            user.almaz -= game.bet
            await user.save()
            await bot.edit_message_text("Вы создали игру #{} на {}💎".format(game.id, game.bet), call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m:m.text and m.text.startswith('/play_coin_'))
async def playCoin(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    res = m.text.replace('/play_coin_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    user = await db.Users.get(user_id=m.from_user.id)
    game = await db.Coin.exists(id=res)
    if game:
        game = await db.Coin.get(id=res)
    if game and game.status == 1:
        player1 = await db.Users.get(id=game.player1)
        if user.location == 'Хэвенбург' or user.location == "Кавайня":
            pass
        else:
            await bot.send_message(m.chat.id, "Вы находитесь вне города.")
            return
        if m.from_user.id != player1.user_id:
            if game.valute == '💰' and user.money >= game.bet:
                user.money -= game.bet
                await user.save()
                game.player2 = user.id
                game.status = 2
                await game.save() 
                commision = await db.System.get(name='commisionCoin')
                fondGame = int(game.bet * 2 - ((game.bet + game.bet) * (commision.value / 100 )))
                CommisionFond = await db.System.get(name='fondGame')
                CommisionFond.value += int(game.bet + game.bet) - fondGame
                await CommisionFond.save()
                rand = random.randint(0, 100)
                if rand >= 50:
                    user.money += fondGame
                    await user.save()
                    if user.quest == 'Азартный путник' and user.questStatus == 1:
                        quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                        quest.progress += 1
                        await quest.save()
                    await achprog(user, ach='stavochnik')
                    await achprog(player1, ach='stavochnik')
                    try:
                        await bot.send_message(m.chat.id, "Вы вышли победителем в игре #{} против игрока {}\nСтавка: {}💰".format(game.id, player1.username, game.bet))
                        await bot.send_message(player1.user_id, "Вы проиграли в игре #{} против игрока {}\nСтавка: {}💰".format(game.id, user.username, game.bet))
                    except:
                        pass
                    await logBot.send_message(tradeChat, "[БАР] GameId: {}\n {} выиграл {}💰 у {}".format(game.id, user.username, fondGame, player1.username))
                else:
                    player1.money += fondGame
                    await player1.save()
                    if player1.quest == 'Азартный путник' and player1.questStatus == 1:
                        quest = await db.tempQuest.get(user_id=player1.user_id, quest=player1.quest, status=0).first()
                        quest.progress += 1
                        await quest.save()
                    await achprog(user, ach='stavochnik')
                    await achprog(player1, ach='stavochnik')
                    try:
                        await bot.send_message(m.chat.id, "Вы проиграли в игре #{} против игрока {}\nСтавка: {}💰".format(game.id, player1.username, game.bet))
                        await bot.send_message(player1.user_id, "Вы вышли победителем в игре #{} против игрока {}\nСтавка: {}💰".format(game.id, user.username, game.bet))
                    except:
                        pass
                    await logBot.send_message(tradeChat, "[БАР] GameId: {}\n{} выиграл {}💰 у {}".format(game.id, player1.username, fondGame, user.username))
            elif game.valute == '💎' and user.almaz >= game.bet:
                user.almaz -= game.bet
                await user.save()
                game.player2 = user.id
                game.status = 2
                await game.save()
                commision = await db.System.get(name='commisionCoinKri')
                fondGame = int(game.bet * 2 - ((game.bet + game.bet) * (commision.value / 100 )))
                HeavenFondKri = await db.System.get(name='HeavenFondKri')
                HeavenFondKri.value += int(game.bet + game.bet) - fondGame
                await HeavenFondKri.save()
                rand = random.randint(0, 100)
                if rand >= 50:
                    user.almaz += fondGame
                    await user.save()
                    if user.quest == 'Азартный путник' and user.questStatus == 1:
                        quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                        quest.progress += 1
                        await quest.save()
                    await achprog(user, ach='stavochnik')
                    await achprog(player1, ach='stavochnik')
                    try:
                        await bot.send_message(m.chat.id, "Вы вышли победителем в игре #{} против игрока {}\nСтавка: {}💎".format(game.id, player1.username, game.bet))
                        await bot.send_message(player1.user_id, "Вы проиграли в игре #{} против игрока {}\nСтавка: {}💎".format(game.id, user.username, game.bet))
                    except:
                        pass
                    await logBot.send_message(tradeChat, "[БАР] GameId: {}\n {} выиграл {}💎 у {}".format(game.id, user.username, fondGame, player1.username))
                else:
                    player1.almaz += fondGame
                    await player1.save()
                    if player1.quest == 'Азартный путник' and player1.questStatus == 1:
                        quest = await db.tempQuest.get(user_id=player1.user_id, quest=player1.quest, status=0).first()
                        quest.progress += 1
                        await quest.save()
                    await achprog(user, ach='stavochnik')
                    await achprog(player1, ach='stavochnik')
                    try:
                        await bot.send_message(m.chat.id, "Вы проиграли в игре #{} против игрока {}\nСтавка: {}💎".format(game.id, player1.username, game.bet))
                        await bot.send_message(player1.user_id, "Вы вышли победителем в игре #{} против игрока {}\nСтавка: {}💎".format(game.id, user.username, game.bet))
                    except:
                        pass
                    await logBot.send_message(tradeChat, "[БАР] GameId: {}\n{} выиграл {}💎 у {}".format(game.id, player1.username, fondGame, user.username))
            else:
                await bot.send_message(m.chat.id, "У вас не хватает {}".format(game.valute))
        else:
            await bot.send_message(m.chat.id, "Нельзя участвовать в своей же игре.")
    else:
        await bot.send_message(m.chat.id, "Игры не существует")


@dp.message_handler(lambda m:m.text and m.text.startswith('/play_tCoin_'))
async def playTCoin(m):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    res = m.text.replace('/play_tCoin_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    user = await db.Users.get(user_id=m.from_user.id)
    print(res)
    game = await db.CoinJackpot.exists(id=int(res))
    if game:
        game = await db.CoinJackpot.get(id=int(res)).first()
    if game and game.winner == -1:
        player1 = await db.Users.get(id=game.player1)
        if user.location == 'Кавайня':
            pass
        else:
            await bot.send_message(m.chat.id, "Вы находитесь вне города.")
            return
        if m.from_user.id != player1.user_id:
            if user.money >= game.bet:
                user.money -= game.bet
                await user.save()
                if game.player2:
                    if user.id == game.player2:
                        await bot.send_message(m.chat.id, "Ты уже участвуешь в этой игре")
                        return
                    game.player3 = user.id
                    game.status = 2
                    await game.save() 
                    commision = await db.System.get(name='commisionCoinTriple')
                    fondGame = int(game.bet * 3 - ((game.bet + game.bet + game.bet) * (commision.value / 100 )))
                    CommisionFond = await db.System.get(name='fondGame')
                    CommisionFond.value += int(game.bet + game.bet + game.bet) - fondGame
                    await CommisionFond.save()
                    rand = random.randint(0, 100)                        
                    if rand <= 33:
                        player1 = await db.Users.get(id=game.player1).first()
                        player2 = await db.Users.get(id=game.player2).first()
                        user.money += fondGame
                        await user.save()
                        game.winner = user.id
                        await game.save()
                        if user.quest == 'Азартный путник' and user.questStatus == 1:
                            quest = await db.tempQuest.get(user_id=user.user_id, quest=user.quest, status=0).first()
                            quest.progress += 1
                            await quest.save()
                        await achprog(user, ach='stavochnik')
                        await achprog(player1, ach='stavochnik')
                        await achprog(player2, ach='stavochnik')
                        try:
                            await bot.send_message(m.chat.id, "Вы вышли победителем в игре #{} против {} и {}\nСтавка: {}💰".format(game.id, player1.username, player2.username, game.bet))
                            await bot.send_message(player1.user_id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, winner.username, game.bet))
                            await bot.send_message(player2.user_id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, winner.username, game.bet))
                        except:
                            pass
                        await logBot.send_message(tradeChat, "[ЭЛИТНЫЙ БАР] GameId: {}\n {} выиграл {}💰".format(game.id, user.username, fondGame))
                    elif rand <= 66:
                        player1 = await db.Users.get(id=game.player1).first()
                        winner = await db.Users.get(id=game.player2).first()
                        winner.money += fondGame
                        await winner.save()
                        game.winner = winner.id
                        await game.save()
                        if winner.quest == 'Азартный путник' and winner.questStatus == 1:
                            quest = await db.tempQuest.get(user_id=winner.user_id, quest=winner.quest, status=0).first()
                            quest.progress += 1
                            await quest.save()
                        await achprog(user, ach='stavochnik')
                        await achprog(winner, ach='stavochnik')
                        await achprog(player1, ach='stavochnik')
                        try:
                            await bot.send_message(winner.user_id, "Вы вышли победителем в игре #{} против {} и {}\nСтавка: {}💰".format(game.id, player1.username, user.username, game.bet))
                            await bot.send_message(player1.user_id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, winner.username, game.bet))
                            await bot.send_message(m.chat.id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, winner.username, game.bet))
                        except:
                            pass
                        await logBot.send_message(tradeChat, "[ЭЛИТНЫЙ БАР] GameId: {}\n{} выиграл {}💰".format(game.id, winner.username, fondGame))
                    else:
                        winner = await db.Users.get(id=game.player1).first()
                        player2 = await db.Users.get(id=game.player2).first()
                        winner.money += fondGame
                        await winner.save()
                        game.winner = player1.id
                        await game.save()
                        if winner.quest == 'Азартный путник' and winner.questStatus == 1:
                            quest = await db.tempQuest.get(user_id=winner.user_id, quest=player1.quest, status=0).first()
                            quest.progress += 1
                            await quest.save()
                        await achprog(user, ach='stavochnik')
                        await achprog(winner, ach='stavochnik')
                        await achprog(player1, ach='stavochnik')
                        try:
                            await bot.send_message(winner.user_id, "Вы вышли победителем в игре #{} против {} и {}\nСтавка: {}💰".format(game.id, player2.username, user.username, game.bet))
                            await bot.send_message(player2.user_id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, user.username, game.bet))
                            await bot.send_message(m.chat.id, "Победителем в игре тройной ставки #{} вышел {}\nСтавка: {}💰".format(game.id, winner.username, game.bet))
                        except:
                            pass
                        await logBot.send_message(tradeChat, "[ЭЛИТНЫЙ БАР] GameId: {}\n{} выиграл {}💰".format(game.id, winner.username, fondGame))
                else:
                    print("pass 2 else")
                    game.player2 = user.id
                    game.fond += game.bet
                    await game.save()
                    await bot.send_message(m.chat.id, "Вы присоединились к игре #{} со ставкой в {}💰. Ожидайте результата".format(game.id,game.bet))
            else:
                await bot.send_message(m.chat.id, "В карманах пусто, где взять деньги - всем известно! Иди фармить!")
        else:
            await bot.send_message(m.chat.id, "Нельзя участвовать в своей же игре.")
    else:
        await bot.send_message(m.chat.id, "Игры не существует")




async def dunjgo(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    _kach = call.data.split('_')
    kach = _kach[1]
    if kach == 'grob':
        if user.location == 'Случайный лес' and user.progLoc == 'Случайный лес|35':
            user.location = 'Лесная гробница'
            user.progLoc = 'Лесная гробница|1'
            user.progStatus = 1
            text = "Вы направились в лесную гробницу"
            await user.save()
            await scenario(user)
        else:
            text = "Вы уже прошли развилку"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
