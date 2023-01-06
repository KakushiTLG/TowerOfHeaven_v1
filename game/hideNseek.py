activesSeekers = {}
kdSeekers = {}
async def partyHS(call, user):
    checkUserIvent = await db.Ivent.exists(idplayer=user.id)
    if not checkUserIvent:
        await db.Ivent.create(idplayer=user.id)
    if call.data.split("_")[1] == 'join':
        userid = str(user.id)
        lobby = await db.HideNseek.get_or_none(status=1).first()
        if lobby:
            if user.location == "Хэвенбург" and user.position == "Площадь":
                lobby.players[userid] = {'alive': 'True', 'coords': "0|0", 'kd': int(time.time()), 'username':  user.username}
                count = 0
                for cnt in lobby.players:
                    count += 1
                await bot.edit_message_text("Ты успешно зашёл в игру. Ожидай сбора игроков {}/5".format(count), call.message.chat.id, call.message.message_id)
                await lobby.save()
                if count >= 5:
                    await startHS(lobby)
        else:
            players = {userid: {'alive': 'True', 'coords': "0|0", 'kd': int(time.time()), 'username': user.username}}
            lobby = await db.HideNseek.create(players=players)
            await bot.edit_message_text("Ты успешно зашёл в игру. Ожидай сбора игроков 1/5", call.message.chat.id, call.message.message_id)
    elif call.data.split("_")[1] == 'top':
        top10 = await db.Ivent.filter().order_by('-pts').limit(10)
        text = "ТОП-10 игроков в прятки за всё время:\n"
        count = 0
        for usr in top10:
            count += 1
            _user = await db.Users.get_or_none(id=usr.idplayer).first()
            if _user:
                text += f"\n#{count} {_user.username} - {usr.pts} pts"        
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
async def createMarkupHideNSeek(lobby, user, arg=None):
    userid = str(user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    text = ""
    textbefore = "В игре:\n"
    HNS_map = ['1|1', '1|2', '1|3', '1|4', '2|1', '2|2', '2|3', '2|4', '3|1', '3|2', '3|3', '3|4', '4|1', '4|2', '4|3', '4|4']
    for position in HNS_map:
        greenZone = False
        redZone = False
        playerZone = False
        redKv = False
        cancelKv = False
        if arg:
            for player in lobby.players:
                if lobby.players[player]['alive'] == "True":
                    if player != str(lobby.seeker):
                        status = "🐭"
                    else:
                        status = "😈"
                    if lobby.players[player]['username'] not in textbefore:
                        textbefore += "\n{} - {}".format(lobby.players[player]['username'], status)
                if lobby.players[player]['alive'] and lobby.players[player]['coords'] == position:
                    if player == str(lobby.seeker):
                        redZone = True
                    else:
                        redKv = True
        elif lobby.status != 2:
            for player in lobby.players:
                if player != str(lobby.seeker):
                    status = "🐭"
                else:
                    status = "😈"
                if lobby.players[player]['username'] not in textbefore:
                    textbefore += "\n{} - {}".format(lobby.players[player]['username'], status)
                if lobby.players[player]['coords'] == position:
                    if player != str(lobby.seeker):
                        cancelKv = True
        else:
            for player in lobby.players:
                if lobby.players[player]['alive'] == "True":
                    if player != str(lobby.seeker):
                        status = "🐭"
                    else:
                        status = "😈"
                    if lobby.players[player]['username'] not in textbefore:
                        textbefore += "\n{} - {}".format(lobby.players[player]['username'], status)
                if not redZone:
                    if lobby.seeker != user.id:
                        if lobby.players[player]['alive'] and lobby.players[player]['coords'] == position:
                            if player == str(lobby.seeker):
                                redZone = True
                            elif player == str(user.id):
                                playerZone = True
                            elif player != str(lobby.seeker) and player != str(user.id):
                                greenZone = True
                    else:
                        if player == str(lobby.seeker) and lobby.players[player]['coords'] == position:
                            playerZone = True
        if position.split("|")[1] == '1':
            text += "\n"
        if not redZone and greenZone: text += "🟩"
        elif not redZone and playerZone: text += "👤"
        elif redZone: text += "😈"
        elif redKv: text += "🟥"
        elif cancelKv: text += "❌"
        else: text += "🔲"
    textbefore += "\nОсталось ходов у искателя: {}".format(lobby.lefttime)
    if lobby.players[userid]['alive'] == "True":

        buttons = []
        buttons.append([*[InlineKeyboardButton('⏺', callback_data="empty_code")] * 3])
        buttons.append([*[InlineKeyboardButton('⏺', callback_data="empty_code")] * 3])
        buttons.append([*[InlineKeyboardButton('⏺', callback_data="empty_code")] * 3])

        if int(lobby.players[userid]['coords'].split("|")[0]) > 1:
            buttons[0][1] = InlineKeyboardButton('⬆️', callback_data=f"joinHNS_{lobby.id}_up")

        if int(lobby.players[userid]['coords'].split("|")[0]) < 4:
            buttons[2][1] = InlineKeyboardButton('⬇️', callback_data=f"joinHNS_{lobby.id}_down")

        if int(lobby.players[userid]['coords'].split("|")[1]) < 4:
            buttons[1][2] = InlineKeyboardButton('➡️', callback_data=f"joinHNS_{lobby.id}_right")
            
        if int(lobby.players[userid]['coords'].split("|")[1]) > 1:
            buttons[1][0] = InlineKeyboardButton('⬅️', callback_data=f"joinHNS_{lobby.id}_left")

        if user.id != lobby.seeker:
            buttons.append([InlineKeyboardButton('Позвать искателя', callback_data=f"joinHNS_{lobby.id}_call")])

        for buter in buttons:
            markup.add(*buter)



    _text = "{}\n{}".format(textbefore, text)
    return markup, _text



async def startHS(lobby):
    lobby.status = 2
    players = []
    for player in lobby.players:
        spawnX = random.randint(1, 4)
        spawnY = random.randint(1, 4)

        spawnLocation = f"{spawnY}|{spawnX}"
        lobby.players[player]['coords'] = spawnLocation
        players.append(int(player))

    seeker = random.choice(players)
    lobby.seeker = seeker
    await lobby.save()
    for player in lobby.players:
        user = await db.Users.get_or_none(id=player).first()
        if user.id != seeker:
            markup, textMap = await createMarkupHideNSeek(lobby, user)
            try:
                await bot.send_message(user.user_id, "Игра началась! Ваша задача - выбрать место, в котором вы хотите спрятаться в ближайшие 30 секунд. Будьте осторожны с передвижениями - ваше движение по линии будет заметно для искателя.")
                await asyncio.sleep(.3)
                await bot.send_message(user.user_id, textMap, reply_markup=markup)
            except:
                pass
        else:
            pass
    user = await db.Users.get_or_none(id=seeker).first()
    if user.id == seeker:
        activesSeekers[user.id] = True
        try:
            await bot.send_message(user.user_id, "Игра началась! Вам досталась роль искателя. Задача - найти всех прячущихся игроков. Через 30 секунд вы сможете начать поиск.")
        except:
            pass
    await asyncio.sleep(30)
    activesSeekers[user.id] = False
    kdSeekers[lobby.id] = int(time.time() + 30)
    await lobby.refresh_from_db()
    try:
        markup, textMap = await createMarkupHideNSeek(lobby, user)
        await bot.send_message(user.user_id, "Время пряток кончилось, пора искать!\n\n")
        await asyncio.sleep(.3)
        await bot.send_message(user.user_id, textMap, reply_markup=markup)
    except:
        pass




async def joinHNS_(call, user):
    userid = str(user.id)
    lobbyId = call.data.split("_")[1]
    lobby = await db.HideNseek.get_or_none(id=lobbyId, status=2).first()
    if lobby:
        if user.id == lobby.seeker and user.id in activesSeekers and activesSeekers[user.id]:
            return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Твоё время еще не пришло...")
        if str(user.id) in lobby.players and lobby.players[userid]['alive'] == 'True':
            if lobby.players[userid]['kd'] > int(time.time()):
                lefttime = lobby.players[userid]['kd'] - int(time.time())
                if user.id == lobby.seeker:
                    return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Передвигаться можно раз в 5 секунд. Попробуй через {}".format(lefttime))
                else:
                    return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Передвигаться можно раз в 13 секунд. Попробуй через {}".format(lefttime))
            position = lobby.players[userid]['coords'].split("|")
            success = False
            if lobby.id in kdSeekers and kdSeekers[lobby.id] <= int(time.time()):
                await calculateWinHNS(lobby, user, arg='cooldown')
            if user.id != lobby.seeker:
                if call.data.split("_")[2] == 'up' and int(position[0]) > 1:
                    newY = int(position[0]) - 1
                    newPos = f"{newY}|{position[1]}"
                    lefttime = int(time.time()) + 13
                    success = True
                elif call.data.split("_")[2] == 'down' and int(position[0]) < 4:
                    newY = int(position[0]) + 1
                    newPos = f"{newY}|{position[1]}"
                    lefttime = int(time.time()) + 13
                    success = True
                elif call.data.split("_")[2] == 'left' and int(position[1]) > 1:
                    newX = int(position[1]) - 1
                    newPos = f"{position[0]}|{newX}"
                    lefttime = int(time.time()) + 13
                    success = True
                elif call.data.split("_")[2] == 'right' and int(position[1]) < 4:
                    newX = int(position[1]) + 1
                    newPos = f"{position[0]}|{newX}"
                    lefttime = int(time.time()) + 13
                    success = True
                elif call.data.split("_")[2] == 'call':
                    lefttime = int(time.time()) + 20
                    where = False
                    lobbyseeker = str(lobby.seeker)
                    seeker = await db.Users.get_or_none(id=lobby.seeker).first()
                    try:
                        await bot.send_message(seeker.user_id, f"Вдруг раздался дикий вопль. Кажется, это тебя там зовут.")
                    except:
                        pass
                    m, text = await createMarkupHideNSeek(lobby, user, arg='call')
                    markup, t = await createMarkupHideNSeek(lobby, seeker)
                    try:
                        await bot.send_message(seeker.user_id, text, reply_markup=markup)
                    except:
                        pass
                    for player in lobby.players:
                        if player != str(lobby.seeker):
                            usr = await db.Users.get_or_none(id=player).first()
                            try:
                                await bot.send_message(usr.user_id, f"{user.username} позвал искателя.")
                            except:
                                pass
                    lobby.players[userid]['kd'] = int(time.time() + 20)
                    await db.HideNseek.filter(id=lobby.id).update(players=lobby.players)
                    return

                else:
                    await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Возникла ошибка. Неправильное направление")
                
                if success:
                    lobby.players[userid]['coords'] = newPos
                    lobby.players[userid]['kd'] = int(time.time() + 13)
                    where = False
                    lobbyseeker = str(lobby.seeker)
                    seekerPos = lobby.players[lobbyseeker]['coords']
                    newPosX = int(newPos.split("|")[0])
                    newPosY = int(newPos.split("|")[1])
                    seekerPosX = int(seekerPos.split("|")[0])
                    seekerPosY = int(seekerPos.split("|")[1])
                    if int(newPos.split("|")[0]) == int(seekerPos.split("|")[0]):
                        if int(newPos.split("|")[1]) < int(seekerPos.split("|")[1]):
                            where = "Слева"
                        elif int(newPos.split("|")[1]) > int(seekerPos.split("|")[1]):
                            where = "Справа"
                    elif int(newPos.split("|")[1]) == int(seekerPos.split("|")[1]):
                        if int(newPos.split("|")[0]) < int(seekerPos.split("|")[0]):
                            where = "Сверху"
                        elif int(newPos.split("|")[0]) > int(seekerPos.split("|")[0]):
                            where = "Снизу"
                    seeker = await db.Users.get_or_none(id=lobby.seeker).first()
                    if where:
                        try:
                            await bot.send_message(seeker.user_id, f"Ты услышал шорох где-то {where}.")
                        except:
                            pass
                    if newPos == seekerPos:
                        lobby.players[userid]['alive'] = False
                        try:
                            await bot.send_message(seeker.user_id, f"Ага, а вот и {user.username} попался!")
                        except:
                            pass
                        try:
                            await bot.send_message(user.user_id, f"Ты угодил в лапы прямо к {seeker.username}")
                        except:
                            pass
                        await calculateWinHNS(lobby, user)
                await db.HideNseek.filter(id=lobby.id).update(players=lobby.players)
            else:
                kdSeekers[lobby.id] = int(time.time() + 30)
                if call.data.split("_")[2] == 'up' and int(position[0]) > 1:
                    newY = int(position[0]) - 1
                    newPos = f"{newY}|{position[1]}"
                    lefttime = int(time.time()) + 5
                    success = True
                elif call.data.split("_")[2] == 'down' and int(position[0]) < 4:
                    newY = int(position[0]) + 1
                    newPos = f"{newY}|{position[1]}"
                    lefttime = int(time.time()) + 5
                    success = True
                elif call.data.split("_")[2] == 'left' and int(position[1]) > 1:
                    newX = int(position[1]) - 1
                    newPos = f"{position[0]}|{newX}"
                    lefttime = int(time.time()) + 5
                    success = True
                elif call.data.split("_")[2] == 'right' and int(position[1]) < 4:
                    newX = int(position[1]) + 1
                    newPos = f"{position[0]}|{newX}"
                    lefttime = int(time.time()) + 5
                    success = True
                else:
                    await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Возникла ошибка. Неправильное направление")
                lobby.players[userid]['coords'] = newPos
                for player in lobby.players:
                    if player != str(user.id):
                        if lobby.players[player]['alive'] == 'True' and lobby.players[player]['coords'] == lobby.players[userid]['coords']:
                            thisPlayer = await db.Users.get_or_none(id=player).first()
                            try:
                                await bot.send_message(user.user_id, f"Опаньки, а вот и {thisPlayer.username} нашёлся!")
                            except:
                                pass
                            try:
                                await bot.send_message(thisPlayer.user_id, f"Не успев убежать, ты угодил прямо в лапы к {user.username}. Гейм овер, получается...")
                            except:
                                pass
                            lobby.players[player]['alive'] = False
                            await db.HideNseek.filter(id=lobby.id).update(players=lobby.players, lefttime=F('lefttime') - 1)
                            await calculateWinHNS(lobby, thisPlayer)
                            await lobby.refresh_from_db()
                markup, text = await createMarkupHideNSeek(lobby, user)
                try:
                    await bot.send_message(user.user_id, text, reply_markup=markup)
                except:
                    pass

                lobby.players[userid]['kd'] = int(time.time() + 5)
                await db.HideNseek.filter(id=lobby.id).update(players=lobby.players, lefttime=F('lefttime') - 1)
            if lobby.lefttime - 1 <= 0:
                await calculateWinHNS(lobby, user)
            else:
                for player in lobby.players:
                    if player != str(lobby.seeker):
                        user = await db.Users.get_or_none(id=player).first()
                        markup, text = await createMarkupHideNSeek(lobby, user)
                        try:
                            await bot.send_message(user.user_id, text, reply_markup=markup)
                        except:
                            pass
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Кажется, ты уже не участвуешь в игре. Дождись окончания.")
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Игра уже кончилась.")


async def calculateWinHNS(lobby, user, arg=None):
    userid = str(user.id)
    count = 0
    if arg and arg == 'cooldown':
        winner = "Игроки"
        await db.HideNseek.filter(id=lobby.id).update(status=4)
        for player in lobby.players:
            if str(lobby.seeker) != player:
                if lobby.players[player]['alive'] == "True":
                    await db.Ivent.filter(idplayer=player).update(pts=F('pts') + 10)
                    text = "Поздравляем с победой! Зачислено 10 pts"
                else:
                    await db.Ivent.filter(idplayer=player).update(pts=F('pts') + 10)
                    text = "Поздравляем с победой! Зачислено 10 pts"
                usr = await db.Users.get_or_none(id=player).first()
                try:
                    await bot.send_message(usr.user_id, text)
                except:
                    pass
            seeker = await db.Users.get_or_none(id=lobby.seeker).first()
            try:
                await bot.send_message(seeker.user_id, "Вы были AFK слишком долго, поэтому вам было зачислено поражение.")
            except:
                pass

    elif lobby.lefttime <= 0:
        winner = "Игроки"
        await db.HideNseek.filter(id=lobby.id).update(status=4)
        for player in lobby.players:
            if str(lobby.seeker) != player:
                if lobby.players[player]['alive'] == "True":
                    await db.Ivent.filter(idplayer=player).update(pts=F('pts') + 10)
                    text = "Поздравляем с победой! Зачислено 10 pts"
                else:
                    await db.Ivent.filter(idplayer=player).update(pts=F('pts') + 10)
                    text = "Поздравляем с победой! Зачислено 10 pts"
                usr = await db.Users.get_or_none(id=player).first()
                try:
                    await bot.send_message(usr.user_id, text)
                except:
                    pass
            seeker = await db.Users.get_or_none(id=lobby.seeker).first()
            try:
                await bot.send_message(seeker.user_id, "Ваши ходы кончились. Игра проиграна.")
            except:
                pass

    else:
        count = 0
        for usr in lobby.players:
            if lobby.players[usr]['alive'] == "True" and usr != str(lobby.seeker):
                count += 1
        if count > 0:
            pass
        else:
            await db.HideNseek.filter(id=lobby.id).update(status=3)
            seeker = await db.Users.get_or_none(id=lobby.seeker).first()
            await db.Ivent.filter(idplayer=seeker.id).update(pts=F('pts') + 10)
            text = "Поздравляем с победой! Зачислено 10 pts"
            try:
                await bot.send_message(seeker.user_id, text)
            except:
                pass
            for player in lobby.players:
                if str(lobby.seeker) != player:
                    await db.Ivent.filter(idplayer=player).update(pts=F('pts') + 1)
                    text = "Поражение! Зачислен 1 pts"
                    usr = await db.Users.get_or_none(id=player).first()
                    try:
                        await bot.send_message(usr.user_id, text)
                    except:
                        pass
    for user in lobby.players:
        usr = await db.Users.get_or_none(user_id=user).first()
        if usr and usr.quest == 'Пряточка' and usr.questStatus == 1:
            quest = await db.tempQuest.get(user_id=usr.user_id, quest=usr.quest, status=0).first()
            quest.progress += 1
            await quest.save()
