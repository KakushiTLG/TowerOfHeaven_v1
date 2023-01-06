async def lobby(m, user):
    if m.chat.id == m.from_user.id:
        user = await db.Users.get_or_none(user_id=m.from_user.id)
        if user:
            if user.position == 'Телепорт Радара':
                checkLobby = await db.Lobby.get_or_none(player1=user.id)
                if not checkLobby:
                    checkLobby = await db.Lobby.get_or_none(player2=user.id)
                    if not checkLobby:
                        checkLobbies = await db.Users.filter(~Q(id=user.id), location='Радар', position='Телепорт Радара')
                        text = "Выберите кого хотите пригласить. Вы так же можете дождаться приглашения от другого игрока, просто стоя на месте.\n"
                        for z in checkLobbies:
                            text += "\n{} - /lobby_invite_{}".format(z.username, z.id)
                        await bot.send_message(m.chat.id, text)
                    else:
                        await bot.send_message(m.chat.id, "У тебя уже есть активное лобби. Покинуть /lobby_exit")
                else:
                    await bot.send_message(m.chat.id, "У тебя уже есть активное лобби. Покинуть /lobby_exit")
            else:
                await bot.send_message(m.chat.id, "Вам необходимо подойти к телепорту")

async def lobbyInvite(m, user): 
    if m.chat.id == m.from_user.id:
        if user:
            if user.position == 'Телепорт Радара':
                checkLobby = await db.Lobby.get_or_none(player1=user.id)
                if not checkLobby:
                    checkLobby = await db.Lobby.get_or_none(player2=user.id)
                    if not checkLobby:
                        checkLobby = await db.Lobby(player1=user.id)
                        await checkLobby.save()
                await checkLobby.refresh_from_db()
                userToInvite = m.text.replace("/lobby_invite_", "", 1)
                getUser = await db.Users.get_or_none(id=userToInvite)
                if getUser and getUser.location == 'Радар' and getUser.position == 'Телепорт Радара':
                    checkActiveLobbies1 = await db.Lobby.get_or_none(player1=getUser.id).first()
                    if checkActiveLobbies1:
                        await bot.send_message(m.chat.id, "У игрока уже есть активное лобби.")
                        return
                    checkActiveLobbies1 = await db.Lobby.get_or_none(player2=getUser.id).first()
                    if checkActiveLobbies1:
                        await bot.send_message(m.chat.id, "У игрока уже есть активное лобби")
                        return
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Принять приглашение', callback_data="lobbyJoin_{}".format(checkLobby.id)))
                    try:
                        await bot.send_message(getUser.user_id, "{} приглашает вас вступить в лобби для исследования Радара".format(user.username), reply_markup=markup)
                    except:
                        pass
                    await bot.send_message(m.chat.id, "Вы пригласили {} к себе в группу.".format(getUser.username))

async def lobbyExit(m, user): 
    if m.chat.id == m.from_user.id:
        if user and user.location == 'Радар' and user.position == 'Телепорт Радара':
            checkLobby = await db.Lobby.get_or_none(player1=user.id)
            if not checkLobby:
                checkLobby = await db.Lobby.get_or_none(player2=user.id)
                if not checkLobby:
                    await bot.send_message(m.chat.id, "Лобби не существует.")
            if checkLobby and checkLobby.player1 == user.id:
                getSecondPlayer = await db.Users.get_or_none(id=checkLobby.player2)
                if getSecondPlayer:
                    try:
                        await bot.send_message(getSecondPlayer.user_id, "Союзник распустил лобби.")
                    except:
                        pass
            else:
                if checkLobby:
                    getSecondPlayer = await db.Users.get_or_none(id=checkLobby.player1)
                    if getSecondPlayer:
                        try:
                            await bot.send_message(getSecondPlayer.user_id, "Союзник распустил лобби.")
                        except:
                            pass
            try:
                lobby = await db.Lobby.get_or_none(player1=user.id).first()
                await lobby.delete()
            except:
                pass
            try:
                lobby = await db.Lobby.get_or_none(player2=user.id).first()
                await lobby.delete()
            except:
                pass
            await bot.send_message(m.chat.id, "Вы распустили лобби.")
        else:
            await bot.send_message(m.chat.id, "Возникла ошибка. Возможно, вы не состоите в лобби либо же находитесь вне телепорта Радара.")


@dp.callback_query_handler(lambda call: call.data.startswith('lobbyJoin_'))
async def lobbyJoin_(call): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    nav = call.data.split('_')
    navWhere = nav[1]
    user = await db.Users.get(user_id=call.from_user.id)
    checkLobby = await db.Lobby.get_or_none(id=navWhere)
    if checkLobby and not checkLobby.player2:
        checkLobby.player2 = user.id
        checkLobby.position = 1
        await checkLobby.save()
        await bot.edit_message_text("Вы приняли приглашение. Ожидаем выбора уровня исследования от приглашающего и начинаем исследование.\nПокинуть лобби /lobby_exit", call.message.chat.id, call.message.message_id)
        getLeader = await db.Users.get(id=checkLobby.player1)
        try:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Первый уровень', callback_data="startRadar_1"))
            markup.add(InlineKeyboardButton('Второй уровень', callback_data="startRadar_2"))
            markup.add(InlineKeyboardButton('Третий уровень', callback_data="startRadar_3"))
            markup.add(InlineKeyboardButton('Четвёртый уровень', callback_data="startRadar_4"))
            markup.add(InlineKeyboardButton('Пятый уровень', callback_data="startRadar_5"))
            markup.add(InlineKeyboardButton('Шестой уровень', callback_data="startRadar_6"))
            markup.add(InlineKeyboardButton('Седьмой уровень', callback_data="startRadar_7"))
            markup.add(InlineKeyboardButton('Восьмой уровень', callback_data="startRadar_8"))
            markup.add(InlineKeyboardButton('Девятый уровень', callback_data="startRadar_9"))
            markup.add(InlineKeyboardButton('Десятый уровень', callback_data="startRadar_10"))
            await bot.send_message(getLeader.user_id, "Игрок {} принял ваше приглашение. Выберите уровень исследования.\n⚠️Повышение уровня исследования усиливает монстров и повышает награды с успешного прохождения.".format(user.username), reply_markup=markup)
        except:
            await checkLobby.delete()
            await bot.edit_message_text("Не удалось отправить сообщение лидеру лобби. Лобби распущено.", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Приглашение устарело", call.message.chat.id, call.message.message_id)


async def startRadar(call, user):
    nav = call.data.split('_')
    selected = nav[1]
    checkLobby = await db.Lobby.get_or_none(player1=user.id)
    if checkLobby and checkLobby.lvl == 0:
        player2 = await db.Users.get_or_none(id=checkLobby.player2)
        if user.radarKD >= int(time.time()):
            leftTime = int((user.radarKD - int(time.time())) / 60)
            await bot.edit_message_text("Ты еще вымотан прошлым походом. Давай отдохнём минут {} и пойдём...".format(leftTime), call.message.chat.id, call.message.message_id)
            try:
                await bot.send_message(player2.user_id, "Твой союзник все еще уставший.")
            except:
                pass
            return
        if player2.radarKD >= int(time.time()):
            leftTime = int((player2.radarKD - int(time.time())) / 60)
            await bot.edit_message_text("Твой союзник все еще уставший", call.message.chat.id, call.message.message_id)
            try:
                await bot.send_message(player2.user_id, "Ты еще вымотан прошлым походом. Давай отдохнём минут {} и пойдём...".format(leftTime))
            except:
                pass
            return
        await db.Lobby.filter(id=checkLobby.id).update(lvl=int(selected), position=0)
        await db.Users.filter(id=user.id).update(location='Исследование Радара')
        await db.Users.filter(id=checkLobby.player2).update(location='Исследование Радара')
        try:
            await bot.send_message(player2.user_id, "Исследование Радара начинается...")
            await bot.edit_message_text("Исследование Радара начинается", call.message.chat.id, call.message.message_id)
            await radarAll()
        except:
            pass
    else:
        await bot.edit_message_text("Лобби не найдено", call.message.chat.id, call.message.message_id)


async def nav_radar(call, user): 
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
        if (str(user.location) == "Радар") and (int(user.hp) > int(user.nowhp)) and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            text = "_Ну теперь то я точно отдохну в прекрасных источниках с прекрасными девушками! Не зря же я истоптал всю сраную пустыню и потерял столько золота._\n\n\nА потом ты закончил фантазировать и вошёл на территорию, так называемых, горячих источников.\n\nНичего необычного, куча ванн соединённых между собой протекающим трубами, по которым течёт вода."
        elif str(user.location) != "Радар":
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
        if (str(user.location) == "Радар") and (str(user.position) != newPos):
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
        elif str(user.location) != "Радар":
            text = "Ты находишься вне города."
        elif str(user.position) == newPos:
            text = "Ты уже находишься в отеле."
        else:
            text = "Ошибка определителя. \nLocation {}\n nowPos/newPos {}/{}\n\nОбратитесь с этим сообщением и скрином профиля к разработчику @kakushigoto".format(str(user.location), str(user.position), str(newPos))
        await bot.send_message(call.message.chat.id, text)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "shop":
        newPos = "Магазин"
        if (str(user.location) == "Радар") and (str(user.position) != newPos):
            user.position = newPos
            await user.save()
            await goToShop(call)
        elif str(user.location) != "Радар":
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
        if user.location == "Радар":
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
        markup.add(InlineKeyboardButton('🏋‍♂Качалка', callback_data="nav_radar_kachalka"), InlineKeyboardButton('🕺Табервам', callback_data="nav_radar_tabervam"))
        markup.add(InlineKeyboardButton('⛲️Источники', callback_data="nav_radar_onsen"), InlineKeyboardButton('👩‍💼Раскулова', callback_data="nav_radar_raskul"))
        markup.add(InlineKeyboardButton('🏫Отель', callback_data="nav_radar_hotel"), InlineKeyboardButton('🧛🏻‍♂️Сыч', callback_data='sich'))
        markup.add(InlineKeyboardButton('Исследование Радара', callback_data="nav_radar_exit"))
        text = "Площадь как площадь. Ведь площадь она и в Хэвенбурге площадь, верно? Знаешь как выглядят площади, так вот наша площадь практически такая же, как и все площади, что ты видел до неё. В общем, площадь, которая выглядит как площадь — вот она, наша площадь Радара."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='markdown')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif navWhere == "exit":
        try:
            navg = nav[3]
            if navg == '1':
                newLocation = "Телепорт Радара"
                if user.location == "Радар":
                    pass
                else:
                    await bot.send_message(call.message.chat.id, "Вы находитесь вне города")
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    return
                user.position = "Телепорт Радара"
                await user.save()
                text = "В одиночку выходить за пределы города опасно, нужно найти союзника с помощью /lobby"
                await bot.send_message(call.message.chat.id, text)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            elif navg == '2':
                if user.location == 'Радар':
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
                markup.add(InlineKeyboardButton('Выйти из города', callback_data="nav_radar_exit_1"))
                markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_radar_exit_2"))
                await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти\nОкрестности Радара - очень дикое место, которое кишит монстрами. Желательно в одиночку туда не ходить... (/lobby)", reply_markup=markup)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Выйти из города', callback_data="nav_radar_exit_1"))
            markup.add(InlineKeyboardButton('Хэвенбург', callback_data="nav_radar_exit_2"))
            await bot.send_message(call.message.chat.id, "Выберите куда хотите пойти\nОкрестности Радара - очень дикое место, которое кишит монстрами. Желательно в одиночку туда не ходить...", reply_markup=markup)
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
        markup.add(InlineKeyboardButton('Выйти'.format(needHp), callback_data="nav_radar_centr"))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        await call.answer()
    elif navWhere == "lombard":
        text = "Ломбард — место элитное, но не менее мерзкое, чем все, что ты видел до него и, вероятно, увидишь после. Здесь можно приобрести нечто более интереснее того мусора из обычного магазина. И да, ''Ломбард'' — это всего лишь название, не более.\nВаш баланс: {}💎".format(str(user.almaz))
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Поддержка игры', callback_data="donate_start"))
        markup.add(InlineKeyboardButton('Магазин 💎', callback_data="donateshop"))
        markup.add(InlineKeyboardButton('Продать предмет', callback_data="shopsell"))
        markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_centr"))
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
            elif user.location == 'Радар':
                markup.add(InlineKeyboardButton('Назад', callback_data="nav_radar_centr"))
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

        else:
            plusText = await giveQuest(user, 'Богиня Хэвенбурга')
            await bot.edit_message_text("Подойдя к входной двери, охрана остановила тебя, спросив допуск. К счастью, мимо проходила весьма сексуальная девица, которая заинтересовалась тобой, отвела в сторону и предложила обмен - ты ей приносишь нижнее бельё, а она открывает тебе доступ к этому заведению. Конечно же ты согласился.\n-Кстати, можешь называть меня Раскуловой. Жду тебя внутри с одеждой.{}".format(plusText), call.message.chat.id, call.message.message_id)
    elif navWhere == 'tabervam':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Выйти', callback_data="nav_radar_centr"))
        checkFinishIvent = await db.Inventory.exists(idplayer=user.id, name='Письмо для Табервама', active=0)
        if checkFinishIvent or user.lvl < 50:
            await radarshop(call, user)
            return
        checkFinishIvent = await db.Inventory.exists(idplayer=user.id, name='Письмо для Табервама', active=1)
        if checkFinishIvent:
            text = "Получив письмо, Табервам со слезами на глазах поблагодарил тебя, а так же пообещал что для тебя ценники теперь на 20% дешевле, выбирай что хочешь!\n\nПолучено: 100🧿"
            await db.Users.filter(id=user.id).update(shmekli=F('shmekli') + 100)
            await db.Inventory.filter(idplayer=user.id, name='Письмо для Табервама').update(active=0)
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            text = "Подойдя к 🕺Табервам, представился и ляпнул что знаком с его женой. Кажется, это было ошибкой. Тебя немедленно засыпали вопросами и попросили передать ей письмо, так как, кроме наёмников, с Радара никого не выпускают. За это тебе предложили скидку, так что отказываться было грехом...\n\n⚠️Дополнительное задание - передать письмо Табернам\nПолучено: ✉️Письмо для Табернам"
            checkIvent = await db.Inventory.exists(idplayer=user.id, name='Письмо для Табернам', active=1)
            if not checkIvent:
                await db.addItem('Письмо для Табернам', user, arg='1')
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)




async def about_craft(m):
    text = "Улучшение предметов. Система, позволяющая улучшать специальные предметы из которых можно ковать артефакты. Использовав пять предметов одного уровня появляется возможность получить один случайный предмет, из данного набора, уровнем выше."
    text += "Список предметов можно увидеть в специальном отделении рюкзака, а сами характеристики предметов перечислены ниже:"
    text += """\n\nПалка-копалка; (+1% доп урона)
Камень обыкновенный; (+1% крит урона)
Кусок металлолома; (+1% армора)
Айрис; (+1% шанс крит урона)
Каменный цветок; (+1% анти-эффект (заморозка/влажность/итд))
Ситенка; (+1% шанс использовать навык без затрат энергии)
Камень андриколь (+1 вампиризм)
Каждый новый уровень повышает показатель бонуса на 1%
Артефакты создаются из предметов с помощью специальных позиций на столе. При соблюдении условий игрок получает артефакт в инвентарь и может надеть его в специальный слот."""
    await bot.send_message(m.chat.id, text)

async def about_gacha(m):
    text = "Торговец Сыч способен призвать случайный предмет, подходящий для улучшения и крафта артефактов. Различие призываемых предметов может быть в уровне."
    text += "\nШанс получения предмета 1-2 уровня: 60%"
    text += "\nШанс получения предмета 3-4 уровня: 20%"
    text += "\nШанс получения предмета 5-6 уровня: 9%"
    text += "\nШанс получения предмета 7-8 уровня: 5%"
    text += "\nШанс получения предмета 9-10 уровня: 3%"
    text += "\nШанс получения предмета 10+ уровня: 2%"
    text += "\nШанс получения случайного артефакта: 1%*"
    text += "\n\n* - возможность получить случайный артефакт (Артефакты, получаемые с улучшения предметов/🔷Камень энергии/🔶Амулет здоровья/💍Кольцо всеотражения и другие) или 🗡Кинжал вампира, а так же гарантированный артефакт/предмет 10+ уровня за каждые 100 попыток при условии, что за эти 100 попыток не выпало ни одного артефакта/предмета 9+ уровня."
    await bot.send_message(m.chat.id, text)




async def sich(call, user):
    if user.location == 'Радар':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
        markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
        text = "Ты когда-нибудь видел смесь еврея, азиата и темнокожего? Это Сыч, добро пожаловать. Мужик всю жизнь занимается улучшением предметов, а так же гачей.\n"
        text += "\nУлучшение предметов работает с категорией пригодной для крафта артефактов. Подробнее (/about_craft)"
        text += "\n\nПризыв. Баланс: {}🧿\nС помощью своей силы, Сыч призывает предметы, пригодные для улучшения. Подробнее (/about_gacha)".format(user.shmekli)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)



async def alchemy(call, user):
    if user.location == 'Радар':
        checkNow = await db.Crafts.exists(idplayer=user.id, active=1)
        if checkNow:
            await db.Crafts.filter(idplayer=user.id, active=1).update(active=0)
        newCraft = await db.Crafts(idplayer=user.id, active=1, type='craft')
        await newCraft.save()
        await bot.edit_message_text("Подготавлиемся к сбору, это займёт некоторое время...", call.message.chat.id, call.message.message_id)
        text = "Выберите нужные предметы для крафта.\n1 слот - пусто\n2 слот - пусто\n3 слот - пусто\n4 слот - пусто\n5 слот - пусто\n\n"
        checkItems = await db.Inventory.exists(idplayer=user.id, active=5)
        if checkItems:
            getItems = await db.Inventory.filter(idplayer=user.id, active=5).order_by('lvl').only('name','lvl','id')
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
                    text += "\nx{} {}({}ур) /add_craftItem_{}".format(_count, z.name, z.lvl, z.id)

        else:
            text += "\nК сожалению, доступных для улучшения предметов нет..."
            await newCraft.delete()
        if len(text) > 4096:
            l = len(text) + 1
            part_1 = text[0:l//2]
            part_2 = text[l//2:]

            await bot.send_message(call.message.chat.id, f'{part_1}')
            await asyncio.sleep(1)
            await bot.send_message(call.message.chat.id, f'{part_2}')
            return
        else:
            await bot.send_message(call.message.chat.id, text)
            return
    else:
        await bot.edit_message_text("Вы находитесь вне города", call.message.chat.id, call.message.message_id)

@dp.message_handler(lambda m:m.text and m.text.startswith('/add_craftItem_'))
async def craftAdd(m):
    try:
        await dp.throttle(str(m.from_user.id), rate=1)
    except exceptions.Throttled:
        return
    if m.from_user.id != m.chat.id:
        return
    result = m.text.replace('/add_craftItem_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get(user_id=m.from_user.id)
    if player.location != 'Радар':
        await bot.send_message(m.chat.id, "Вы находитесь вне города")
        return
    getCraft = await db.Crafts.get_or_none(idplayer=player.id, active=1)
    if getCraft:
        if not getCraft.firstItem: currentItem = 'first'
        elif not getCraft.secondItem: currentItem = 'second'
        elif not getCraft.thirdItem: currentItem = 'third'
        elif not getCraft.fourthItem: currentItem = 'fourth'
        elif not getCraft.fifthItem: currentItem = 'fifth'
        else:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
            markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
            await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
            return
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
        markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
        await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
        return
    item = await db.Inventory.get_or_none(id=result)
    if item:
        if item.active == 5 and item.idplayer == player.id:
            if currentItem == 'first': getCraft.firstItem = item.id
            elif currentItem == 'second': getCraft.secondItem = item.id
            elif currentItem == 'third': getCraft.thirdItem = item.id
            elif currentItem == 'fourth': getCraft.fourthItem = item.id
            elif currentItem == 'fifth': getCraft.fifthItem = item.id
            else:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
                markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
                await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
                return
            await db.Crafts.filter(id=getCraft.id).update(firstItem=getCraft.firstItem,
                        secondItem=getCraft.secondItem,
                        thirdItem=getCraft.thirdItem,
                        fourthItem=getCraft.fourthItem,
                        fifthItem=getCraft.fifthItem)
            if currentItem == 'fifth':
                firstItem = await db.Inventory.get_or_none(id=getCraft.firstItem)
                secondItem = await db.Inventory.get_or_none(id=getCraft.secondItem)
                thirdItem = await db.Inventory.get_or_none(id=getCraft.thirdItem)
                fourthItem = await db.Inventory.get_or_none(id=getCraft.fourthItem)
                fifthItem = await db.Inventory.get_or_none(id=getCraft.fifthItem)
                if firstItem.name == 'Камень обыкновенный' and secondItem.name == 'Айрис' and thirdItem == 'Камень обыкновенный' and fourthItem == 'Палка-копалка' and fifthItem == 'Палка-копалка':
                    randomItem = 'Сувенир с моря'
                    arg = item.lvl
                    success = await db.addArt(randomItem, player, arg)
                elif firstItem.name == 'Камень обыкновенный' and secondItem.name == 'Кусок металлолома' and thirdItem.name == 'Каменный цветок' and fourthItem.name == 'Ситенка' and fifthItem.name == 'Камень Андриколь':
                    randomItem = 'Квинтэссенция камня'
                    arg = item.lvl
                    success = await db.addArt(randomItem, player, arg)
                elif firstItem.name == 'Палка-копалка' and secondItem.name == 'Палка-копалка' and thirdItem.name == 'Палка-копалка' and fourthItem.name == 'Палка-копалка' and fifthItem.name == 'Палка-копалка':
                    randomItem = "Палка ярости"
                    arg = item.lvl
                    success = await db.addArt(randomItem, player, arg)
                elif firstItem.name == 'Камень Андриколь' and secondItem.name == 'Кусок металлолома' and thirdItem.name == 'Камень Андриколь' and fourthItem.name == 'Камень обыкновенный' and fifthItem.name == 'Камень Андриколь':
                    randomItem = "Камень-металлолом"
                    arg = item.lvl
                    success = await db.addArt(randomItem, player, arg)
                else:
                    randomItems = ['Палка-копалка', 'Камень обыкновенный', 'Кусок металлолома', 'Айрис', 'Каменный цветок', 'Ситенка', 'Камень Андриколь']
                    randomItem = random.choice(randomItems)
                    arg = item.lvl + 1
                    success = await db.addArt(randomItem, player, arg)
                q = 0
                if success:
                    for i in range(0, 5):
                        q += 1
                        if q == 1: needItem = getCraft.firstItem
                        elif q == 2: needItem = getCraft.secondItem
                        elif q == 3: needItem = getCraft.thirdItem
                        elif q == 4: needItem = getCraft.fourthItem
                        elif q == 5: needItem = getCraft.fifthItem
                        await db.Inventory.filter(id=needItem).update(active=0)
                    await bot.send_message(m.chat.id, "Шалтай-балтай, Вжух-Брух, Бам-дам, там-сям, силой величественных огров ты получил {} {} уровня".format(randomItem, arg))
                    await db.Crafts.filter(id=getCraft.id).update(active=2)
                    user = await achprog(player, ach='craft')
                    await logBot.send_message(tradeChat, "[КРАФТ] Игрок {} скрафтил {} {}ур".format(player.username, randomItem, arg))
                else:
                    await bot.send_message(m.chat.id, "Что-то пошло не так...")
            else:
                currentCraft = []
                if currentItem == 'first':
                    thisItem = 1
                elif currentItem == 'second':
                    thisItem = 2
                elif currentItem == 'third':
                    thisItem = 3
                elif currentItem == 'fourth':
                    thisItem = 4
                else:
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
                    markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
                    await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
                    return
                q = 0
                text = "Текущий крафт:\n"
                for i in range(0, thisItem):
                    q += 1
                    if q == 1:
                        itm = await db.Inventory.get_or_none(id=getCraft.firstItem)
                        currentCraft.append(itm.id)
                        text += "\nПервый слот - {} ({} уровень)".format(itm.name, itm.lvl)
                    elif q == 2:
                        itm = await db.Inventory.get_or_none(id=getCraft.secondItem)
                        if itm.id in currentCraft:
                            await db.Crafts.filter(idplayer=player.id).update(active=0)
                            await bot.send_message(m.chat.id, 'Возникла ошибка. Крафт отменен.')
                        else:
                            currentCraft.append(itm.id)
                        text += "\nВторой слот - {} ({} уровень)".format(itm.name, itm.lvl)
                    elif q == 3:
                        itm = await db.Inventory.get_or_none(id=getCraft.thirdItem)
                        if itm.id in currentCraft:
                            await db.Crafts.filter(idplayer=player.id).update(active=0)
                            await bot.send_message(m.chat.id, 'Возникла ошибка. Крафт отменен.')
                        else:
                            currentCraft.append(itm.id)
                        text += "\nТретий слот - {} ({} уровень)".format(itm.name, itm.lvl)
                    elif q == 4:
                        itm = await db.Inventory.get_or_none(id=getCraft.fourthItem)
                        if itm.id in currentCraft:
                            await db.Crafts.filter(idplayer=player.id).update(active=0)
                            await bot.send_message(m.chat.id, 'Возникла ошибка. Крафт отменен.')
                        else:
                            currentCraft.append(itm.id)
                        text += "\nЧетвёртый слот - {} ({} уровень)".format(itm.name, itm.lvl)
                text += "\n\nДобавить еще:"
                getItems = await db.Inventory.filter(idplayer=player.id, active=5, lvl=item.lvl).only('name','lvl','id')
                count = {}
                for z in getItems:
                    if z.id == getCraft.firstItem or z.id == getCraft.secondItem or z.id == getCraft.thirdItem or z.id == getCraft.fourthItem or z.id == getCraft.fifthItem:
                        pass
                    else:
                        if z.name in count:
                            pass
                        else:
                            count[z.name] = 1
                            _count = await db.Inventory.filter(idplayer=player.id, active=5, lvl=z.lvl, name=z.name).count()
                            text += "\nx{} {}({}ур) /add_craftItem_{}".format(_count, z.name, z.lvl, z.id)

                text += "\n\nОтменить крафт /cancel_craftItem"
                await bot.send_message(m.chat.id, text)
        else:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
            markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
            await db.Crafts.filter(id=getCraft.id).update(active=0)
            await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
            return
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
        markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
        await db.Crafts.filter(id=getCraft.id).update(active=0)
        await m.answer("Возникла ошибка. Пожалуйста, начните заново", reply_markup=markup)
        return



@dp.message_handler(lambda m:m.text and m.text.startswith('/cancel_craftItem'))
async def cancel_craftItem(m):
    if m.from_user.id != m.chat.id:
        return
    result = m.text.replace('/cancel_craftItem', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    player = await db.Users.get_or_none(user_id=m.from_user.id)
    if player:
        await db.Crafts.filter(idplayer=player.id).update(active=0)



async def gacha(call, user):
    randomItems = ['Палка-копалка', 'Камень обыкновенный', 'Кусок металлолома', 'Айрис', 'Каменный цветок', 'Ситенка', 'Камень Андриколь']
    if user.location == 'Радар':
        if user.shmekli >= 100:
            await db.Users.filter(id=user.id).update(shmekli=F('shmekli') - 100)
            randomer = random.randint(1, 1000)
            if user.gachaGarant < 100:
                if randomer <= 600:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется лунным светом, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(1, 2)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой земли ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = user.gachaGarant + 1
                    await gachaStat(status='None')

                elif randomer <= 800:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется лунным светом, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(3, 4)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой картошки ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = user.gachaGarant + 1
                    await gachaStat(status='None')

                elif randomer <= 890:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется весьма ярким лунным светом, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(5, 6)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой шашлыка из свинины ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = user.gachaGarant + 1
                    await gachaStat(status='None')

                elif randomer <= 940:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется весьма ярким лунным светом, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(7, 8)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой огров ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = user.gachaGarant + 1

                elif randomer <= 970:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется СТРАННЫМ ГОЛУБЫМ СИЯНИЕМ, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(9, 10)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой Кефира ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = 0
                    await gachaStat(status='lega')
                
                elif randomer <= 990:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется СТРАННЫМ ГОЛУБЫМ СИЯНИЕМ, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(10, 15)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой башни ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                    gachaGarant = 0
                    await gachaStat(status='lega')

                elif randomer <= 1000:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется ЯРКИМ ЗОЛОТЫМ СИЯНИЕМ, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItemChance = random.randint(1, 100)
                    if randomItemChance <= 90:
                        randomItems = ['Осколок энергии', 'Амулет здоровья', 'Кусок паззла', 'Анти-анализатор БМ', 'Кинжал вампира']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance <= 95:
                        randomItems = ['Горшок лепрекона', 'Карманная дриада', 'Кинжал вампира']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance <= 99:
                        randomItems = ['Камень энергии', 'Кинжал вампира']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance == 100:
                        randomItem = 'Кольцо всеотражения'
                    success = await db.addItem(randomItem, user, arg='1')
                    await bot.edit_message_text("Силой ИГРАТЕЛЕЙ В ТОХ ты получаешь {}!".format(randomItem), call.message.chat.id, call.message.message_id)
                    gachaGarant = 0
                    await gachaStat(status='lega')
            
            else:
                await gachaStat(status='garant')
                randomer = random.randint(1, 100)
                if randomer <= 90:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется СТРАННЫМ ГОЛУБЫМ СИЯНИЕМ, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItem = random.choice(randomItems)
                    lvl = random.randint(10, 15)
                    success = await db.addArt(randomItem, user, lvl)
                    await bot.edit_message_text("Силой башни ты получаешь {} {} уровня!".format(randomItem, lvl), call.message.chat.id, call.message.message_id)
                else:
                    await bot.edit_message_text("Начинаем призыв... Комната озаряется ЯРКИМ ЗОЛОТЫМ СИЯНИЕМ, Сыч взмахом руки закрывает двери на расстоянии и...", call.message.chat.id, call.message.message_id)
                    await asyncio.sleep(5)
                    randomItemChance = random.randint(1, 100)
                    if randomItemChance <= 90:
                        randomItems = ['Осколок энергии', 'Амулет здоровья', 'Кусок паззла', 'Анти-анализатор БМ']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance <= 95:
                        randomItems = ['Горшок лепрекона', 'Карманная дриада', 'Кинжал вампира']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance <= 99:
                        randomItems = ['Камень энергии', 'Кинжал вампира']
                        randomItem = random.choice(randomItems)
                    elif randomItemChance == 100:
                        randomItem = 'Кольцо всеотражения'
                    success = await db.addItem(randomItem, user, arg='1')
                    await bot.edit_message_text("Силой ИГРАТЕЛЕЙ В ТОХ ты получаешь {}!".format(randomItem), call.message.chat.id, call.message.message_id)
                gachaGarant = 0
            await db.Users.filter(id=user.id).update(gachaGarant=gachaGarant)
            user = await achprog(user, ach='gacha')
            await gachaRetry(call)
        else:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
            markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
            await bot.edit_message_text("К сожалению, у тебя не хватает 🧿. Ты можешь получить их с исследований Радара или же приобрести за ♦️.", call.message.chat.id, call.message.message_id, reply_markup=markup)



async def gachaRetry(call):
    user = await db.Users.get(user_id=call.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
    markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
    await bot.send_message(call.message.chat.id, "Баланс: {}🧿. Попробовать еще?".format(user.shmekli), reply_markup=markup)


async def buyGacha(call, user):
    __q = call.data.split("_")
    numPack = __q[1]
    if numPack == '1':
        if user.almaz >= 7:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 7, shmekli=F('shmekli') + 100)
            text = "Успешно приобретено: 100🧿"
        else:
            text = "Не хватает 💎"
    elif numPack == '2':
        if user.almaz >= 35:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 35, shmekli=F('shmekli') + 500)
            text = "Успешно приобретено: 500🧿"
        else:
            text = "Не хватает 💎"
    elif numPack == '3':
        if user.almaz >= 67:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 67, shmekli=F('shmekli') + 1000)
            text = "Успешно приобретено: 1000🧿"
        else:
            text = "Не хватает 💎"
    elif numPack == '4':
        if user.almaz >= 125:
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - 125, shmekli=F('shmekli') + 2000)
            text = "Успешно приобретено: 2000🧿"
        else:
            text = "Не хватает 💎"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Улучшение предметов', callback_data="alchemy"))
    markup.add(InlineKeyboardButton('Призыв (100🧿)', callback_data="gacha"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)






async def update_radar_kd(lobby):
    kdTime = int(time.time()) + 1800
    await db.Users.filter(id=lobby.player1).update(radarKD=kdTime)
    await db.Users.filter(id=lobby.player2).update(radarKD=kdTime)


async def event_winner(idp, call): # событие - монстр повержен
    sometext = ""
    player = await db.Users.get(id=idp.id)
    lobby = await db.Lobby.get(Q(player1=idp.id) | Q(player2=idp.id)).first()
    # peak_mob = await db.Lobby.get(id=idp.battleWith)

    # вклад в бой и рассчет награды
    if lobby.player1 == idp.id:
        if lobby.damage1 <= 0:
            await bot.send_message(call.message.chat.id, 'Ваш вклад в атаку - 0, вы cumалот.')
            await db.Lobby.filter(id=lobby.id).update(battleStatus=0)
            return
    elif lobby.player2 == idp.id:
        if lobby.damage2 <= 0:
            await bot.send_message(call.message.chat.id, 'Ваш вклад в атаку - 0, вы cumалот.')
            await db.Lobby.filter(id=lobby.id).update(battleStatus=0)
            return

    mob_hp = lobby.mobHp
    contrib_in_battle = 0
    if lobby.player1 == idp.id:
        contrib_in_battle = lobby.damage1 / mob_hp * 100
    else:
        contrib_in_battle = lobby.damage2 / mob_hp * 100
    
    rand = random.randint(1, 100)

    if idp.quest == 'Убийца' and idp.questStatus == 1:
        quest = await db.tempQuest.get(user_id=idp.user_id, quest=idp.quest, status=0)
        quest.progress += 1
        await quest.save()
    exp = 0

    text = lobby.battleLog
    text += "\n\nМонстр повержен!\n\n\n{}".format(str(sometext))
    await db.Lobby.filter(id=lobby.id).update(battleStatus=0)
    await db.Logivent.all().delete()
    await bot.send_message(idp.user_id, text, parse_mode='Markdown')
    await achprog(idp, ach='radar')
    await update_radar_kd(lobby)
    return



@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers and call.data.startswith('lobbybattle_atk'))
async def combo_fight(call):
    _q = call.data.split("_")
    q = _q[2]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    await bot.edit_message_text("{}\n\n\nВ АТАКУ!!!".format(call.message.text),call.message.chat.id, call.message.message_id, reply_markup=markup)
    await asyncio.sleep(9)
    checkMob = await db.Monsters.get(id=q).first()
    result = await db.Users.get(user_id=call.from_user.id)
    idp = result
    location = result.location
    pName = result.username
    lobby = await db.Lobby.get_or_none(Q(player1=result.id) | Q(player2=result.id)).first()
    if not lobby:
        await bot.send_message(call.message.chat.id, "Один из участников лобби покинул локацию. Исследование провалено.")
        return
    if checkMob.name != lobby.mobName: 
        await bot.edit_message_text("Эта битва уже кончилась!", call.message.chat.id, call.message.message_id)
        return
    # if result.location != er.location:
    #     await bot.send_message(call.message.chat.id, "Битва с мобом окончена")
    #     return
    checkplayer1 = await db.Users.get_or_none(id=lobby.player1)
    checkplayer2 = await db.Users.get_or_none(id=lobby.player2)
    if not checkplayer1 or not checkplayer2 or checkplayer1.location != checkplayer2.location:
        try:
            await lobby.delete()
        except:
            pass
        try:
            await db.Users.filter(id=checkplayer1.id).update(location='Радар')
        except:
            pass
        try:
            await db.Users.filter(id=checkplayer2.id).update(location='Радар')
        except:
            pass
        await bot.send_message(call.message.chat.id, "Один из участников лобби покинул локацию. Исследование провалено.")
        return
    if (result.nowhp > 0) and (lobby.mobHp > 0):
        if result.energy > 90: EnergyAtk = 1
        elif result.energy <= 90 and result.energy > 80: EnergyAtk = 0.97
        elif result.energy <= 80 and result.energy > 70: EnergyAtk = 0.9
        elif result.energy <= 70 and result.energy > 60: EnergyAtk = 0.83
        elif result.energy <= 60 and result.energy > 50: EnergyAtk = 0.75
        elif result.energy <= 50 and result.energy > 40: EnergyAtk = 0.66
        elif result.energy <= 40 and result.energy > 30: EnergyAtk = 0.57
        elif result.energy <= 30 and result.energy > 20: EnergyAtk = 0.48
        elif result.energy <= 20 and result.energy > 10: EnergyAtk = 0.35
        elif result.energy <= 10 and result.energy > 0: EnergyAtk = 0.29
        else: EnergyAtk = 0.2
        _itemAtk = result.lvl / 100

        if result.frak != None and result.frak != '':
            frak = await db.Fraks.get(name=result.frak)
            frakAtk = frak.atk / 100
        else:
            frakAtk = 0
        _playerAtk = 0
        weapon = await db.Inventory.get_or_none(name=result.item, idplayer=result.id, active=2).first()
        if weapon:
            __playerAtk = int(result.atk * (weapon.bonus / 100))
            _playerAtk = __playerAtk + (result.atk * frakAtk)
        checkBuffAtk = await db.Buffs.get_or_none(type='atk', owner=result.id, status=1).first()
        if checkBuffAtk:
            playerAtk = int(result.atk + (result.atk * (checkBuffAtk.num / 100) + (_playerAtk * EnergyAtk)))
        else:
            playerAtk = int(result.atk +_playerAtk * EnergyAtk)
        checkBuffCreet = await db.Buffs.get_or_none(type='creet', owner=result.id, status=1).first()
        if checkBuffCreet:
            rand = random.randint(0, 100)
            if rand <= checkBuffCreet.num:
                playerAtk *= 2
        
        playerAtkBefore = int(playerAtk * EnergyAtk)
        minAtk = int(playerAtkBefore * 0.9)
        maxAtk = int(playerAtkBefore * 1.1)
        playerAtk = random.randint(minAtk, maxAtk)
        
        if True:
            if await db.Inventory.exists(name__in=["Кольт", "Золотой кольт"], idplayer=result.id, active=2):
                if random.randint(1, 100) <= 90:
                    attack = playerAtk * 0.6
                    if random.randint(1, 100) <= 65:
                        attack += playerAtk * 0.6
                        if random.randint(1, 100) <= 40:
                            attack += playerAtk * 0.6
                            if random.randint(1, 100) <= 35:
                                attack += playerAtk * 0.6
                                if random.randint(1, 100) <= 30:
                                    attack += playerAtk * 0.6
                                    if random.randint(1, 100) <= 20:
                                        attack += playerAtk * 0.6
                else:
                    attack = playerAtk * 0.3
                playerAtk = int(attack)

        enemyNewHp = lobby.mobHp - playerAtk
        if enemyNewHp > 0:
        # lobby_player = await db.Lobby.get(player=result.id)
            if lobby.player1 == idp.id:
                p1_damage = playerAtk + lobby.damage1
                await db.Lobby.filter(id=lobby.id).update(damage1=p1_damage, mobHp=enemyNewHp)
            else:
                p2_damage = playerAtk + lobby.damage2
                await db.Lobby.filter(id=lobby.id).update(damage2=p2_damage, mobHp=enemyNewHp)
        
        if enemyNewHp <= 0:

            if lobby.player1 == idp.id:
                p1_damage = playerAtk + lobby.damage1 + enemyNewHp
                await db.Lobby.filter(id=lobby.id).update(damage1=p1_damage)
            else:
                p2_damage = playerAtk + lobby.damage2 + enemyNewHp
                await db.Lobby.filter(id=lobby.id).update(damage2=p2_damage)

            await event_winner(idp, call)
            return


        armor = int(result.armor / 3)
        text = ""
        checkarmor = await db.Inventory.filter(active=2, idplayer=result.id)
        if checkarmor:
            r = random.randint(1, 100)
            qwe = 0
            for z in checkarmor:
                if z.name == 'Железный щит' and r <= 5:
                    playerNewHp = int(result.nowhp)
                    text += "\nВы отразили атаку монстра своим щитом"
                    qwe = 1
                elif z.name == 'Щит бомжа' and r <= 10:
                    playerNewHp = int(result.nowhp)
                    text += "\nВы отразили атаку монстра своим щитом"
                    qwe = 1
                elif z.name == 'Золотая покрышка' and r <= 15:
                    playerNewHp = int(result.nowhp)
                    text += "\nВы отразили атаку монстра своим щитом"
                    qwe = 1
                elif z.name == 'Щит верности Раскуловой' and r <= 20:
                    playerNewHp = int(result.nowhp)
                    text += "\nВы отразили атаку монстра своим щитом"
                    qwe = 1
                
            if qwe == 0:
                checkBuffUv = await db.Buffs.get_or_none(owner=result.id, status=1, type='uv').first()
                if checkBuffUv:
                    rand = random.randint(0, 100)
                    if rand <= checkBuffUv.num:
                        text += "\nТы смог увернуться от удара монстра"
                        qwe = 1

            if qwe == 0:
                minAtk = int(lobby.mobAtk * 0.9)
                maxAtk = int(lobby.mobAtk * 1.1)
                mobAtk = random.randint(minAtk, maxAtk)
                if mobAtk < armor:
                    armor = mobAtk - 1
                elif mobAtk == armor:
                    armor = mobAtk - 1
                playerNewHp = int(result.nowhp) + armor - int(mobAtk)
            else:
                playerNewHp = int(result.nowhp)
        else:
            await radarMobCreet()
            rand = random.randint(0, 100)
            if rand <= 5:
                await radarMobCreet(success=True)
                lobby.mobAtk *= 2
            elif rand <= 13:
                await radarMobCreet(success=True)
                lobby.mobAtk *= 1.5
            minAtk = int(lobby.mobAtk * 0.9)
            maxAtk = int(lobby.mobAtk * 1.1)
            mobAtk = random.randint(minAtk, maxAtk)
            if mobAtk < armor:
                armor = mobAtk - 1
            elif mobAtk == armor:
                armor = mobAtk - 1
            playerNewHp = int(result.nowhp) + armor - int(mobAtk)


        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton('Атаковать', callback_data=call.data))
        randomSkill = random.randint(0, 100)
        # lobby_player = await db.Lobby.get(player=result.id)
        await lobby.refresh_from_db()

        # skill_int = lobby.skill_status
        dead = False
        if qwe == 0 and playerNewHp > 0:
            text += "\n{} нанёс удар {}🔪(🛡{}). У тебя осталось {}❤️".format(lobby.mobName, mobAtk, str(armor), playerNewHp)
        elif qwe == 0 and playerNewHp <= 0:
            text += f"\nПри попытке ударить {lobby.mobName} он резко заблокировал твою атаку и мощно контратаковал сплэшом. Очнулся ты уже в Радаре."
            dead = True
            await db.Users.filter(id=lobby.player1).update(location='Радар', position='Площадь', nowhp=5, eat=100, energy=100, money=F('money') / 2)
            await db.Users.filter(id=lobby.player2).update(location='Радар', position='Площадь', nowhp=5, eat=100, energy=100, money=F('money') / 2)
            await db.Users.filter(user_id=call.from_user.id).update(location='Радар', position='Площадь', nowhp=5, eat=100, energy=100)
            await lobby.delete()

        textForLog = "{}\n{} нанёс удар {}🔪. У монстра осталось {}❤️".format(lobby.battleLog, result.username, playerAtk, lobby.mobHp)
        if not dead:
            await db.Users.filter(id=result.id).update(nowhp=playerNewHp)
        await result.refresh_from_db()
        await db.Lobby.filter(id=lobby.id).update(battleLog=textForLog)
        if not dead:
            await bot.send_message(call.message.chat.id, "{}{}".format(textForLog, text), reply_markup=markup)
        else:
            await bot.send_message(call.message.chat.id, "{}{}".format(textForLog, text))
        return
    else:
        await event_winner(idp, call)
        return