userBets = {}

async def dvp(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if user.location == 'Хэвенбург':
        games = await db.Matches.filter(~Q(status=3)).order_by('-status')
        text = "ДОСКА ДВП - именно здесь ошиваются ставочники - самые элитные люди этого города. Здесь ты можешь делать ставки на какое-то игровое событие (и это необязательно может быть событие, связанное с нашим миром - возможно это чья-то фантазия) и, в случае победы, забрать себе бабки!\n\nВыбери событие:\n"
        tournaments = []
        if games:
            for game in games:
                if game.tournament and game.tournament not in tournaments:
                    tournaments.append(game.tournament)
                    counted = await db.Matches.filter(tournament=game.tournament).count()
                    markup.add(InlineKeyboardButton('{}'.format(game.tournament), callback_data="bets_{}".format(game.id)))
                    text += "\n{} - {} игр".format(game.tournament, counted)
        else:
            text = "ДОСКА ДВП - именно здесь ошиваются ставочники - самые элитные люди этого города. Здесь ты можешь делать ставки на какое-то игровое событие (и это необязательно может быть событие, связанное с нашим миром - возможно это чья-то фантазия) и, в случае победы, забрать себе бабки!\n\nУвы, пока тут никого и ничего нет"
        markup.add(InlineKeyboardButton('Активные ставки', callback_data="activeBets"))
        markup.add(InlineKeyboardButton('Вернуться на площадь', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)



async def bets_(call, user):
    if user.location == 'Хэвенбург':
        checkGame = await db.Matches.get_or_none(id=call.data.split('_')[1]).first()
        if checkGame and checkGame.status != 3:
            text = "⚠️В событии может присутствовать комиссия, которая делится между игроками, участвующих в событии⚠️\n\nСписок матчей:\n"
            games = await db.Matches.filter(~Q(status=3), tournament=checkGame.tournament).order_by('-status')
            for game in games:
                allbets = (game.w1sum + game.w2sum)
                kf_player1 = (allbets / game.w1sum) - ((allbets / game.w1sum) * (game.commision / 100))
                if kf_player1 <= 1: kf_player1 = 1.01
                kf_player2 = (allbets / game.w2sum) - ((allbets / game.w2sum) * (game.commision / 100))
                if kf_player2 <= 1: kf_player2 = 1.01
                if game.status == 2:
                    text += "\n⚠️LIVE⚠️\n[{}] {} vs {}\nx{} ({}💰) vs x{} ({}💰)\nПоставить: /bet_{}".format(game.tournament, game.p1, game.p2, round(kf_player1, 2), game.w1sum, round(kf_player2, 2), game.w2sum, game.id)
                elif game.status == 1:
                    text += "\n[{}] {} vs {}\nx{} ({}💰) vs x{} ({}💰)\nПоставить: /bet_{}".format(game.tournament, game.p1, game.p2, round(kf_player1, 2), game.w1sum, round(kf_player2, 2), game.w2sum, game.id)
        else:
            text = "К сожалению, запланированных событий нет :("
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Активные ставки', callback_data="activeBets"))
        markup.add(InlineKeyboardButton('Назад', callback_data="dvp"))
        markup.add(InlineKeyboardButton('Вернуться на площадь', callback_data="nav_bigcity_centr"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def match_(m, user):
    if m.chat.id != m.from_user.id: return
    result = m.text.replace('/match_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    game = await db.Matches.get_or_none(id=result)
    if game:
        allbets = (game.w1sum + game.w2sum)
        kf_player1 = (allbets / game.w1sum) - ((allbets / game.w1sum) * (game.commision / 100))
        if kf_player1 <= 1: kf_player1 = 1.01
        kf_player2 = (allbets / game.w2sum) - ((allbets / game.w2sum) * (game.commision / 100))
        if kf_player2 <= 1: kf_player2 = 1.01
        if game.status == 2:
            text = "⚠️LIVE⚠️\n[{}] {} vs {}\nx{} ({}💰) vs x{} ({}💰)".format(game.tournament, game.p1, game.p2, round(kf_player1, 2), game.w1sum, round(kf_player2, 2), game.w2sum)
        elif game.status == 1:
            text = "\n[{}] {} vs {}\nx{} ({}💰) vs x{} ({}💰)\nСтавка: /bet_{}".format(game.tournament, game.p1, game.p2, round(kf_player1, 2), game.w1sum, round(kf_player2, 2), game.w2sum, game.id)
        elif game.status == 3:
            text = "⚠️Match over⚠️\n[{}] {} vs {}\n🏆{}🏆".format(game.tournament, game.p1, game.p2, game.winner)
    else:
        text = "Матч не найден :("
    await bot.send_message(m.chat.id, text)


async def activeBets(call, user):
    user = await db.Users.get(user_id=call.from_user.id)
    allBets = await db.Bets.filter(idplayer=user.id)
    text = "Твои ставки:\n"
    if allBets:
        for bet in allBets:
            game = await db.Matches.get_or_none(id=bet.idmatch)
            if game and game.status != 3:
                if bet.winner == 'p1': winner = game.p1
                else: winner = game.p2
                text += "\n{}💰 на {} /match_{}".format(bet.summ, winner, bet.idmatch)
    else:
        text = "У тебя нет активных ставок."
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('К доске', callback_data="dvp"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def bet(m, user):
    if m.chat.id != m.from_user.id: return
    user = await db.Users.get(user_id=m.from_user.id)
    result = m.text.replace('/bet_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    game = await db.Matches.get_or_none(id=result)
    if game:
        if game.status == 1:
            text = "На кого ставим?\n\n{} vs {}".format(game.p1, game.p2)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('{}'.format(game.p1), callback_data="bet_{}_p1".format(game.id)))
            markup.add(InlineKeyboardButton('{}'.format(game.p2), callback_data="bet_{}_p2".format(game.id)))
            markup.add(InlineKeyboardButton('Отменить ставку', callback_data="dvp"))
        elif game.status == 2:
            text = "К сожалению, событие уже началось."
        else:
            text = "К сожалению, событие уже завершилось."
    else:
        text = "Такого события не существует."
    try:
        await bot.send_message(m.chat.id, text, reply_markup=markup)
    except:
        await bot.send_message(m.chat.id, text)


async def bet_(call, user):
    gameId = call.data.split("_")[1]
    winner = call.data.split("_")[2]
    user = await db.Users.get(user_id=call.from_user.id)
    game = await db.Matches.get_or_none(id=gameId)
    if game:
        if game.status == 1:
            text = "Сколько ставим? У тебя {}💰".format(user.money)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('50💰', callback_data="betDone_{}_{}_50".format(game.id, winner)), InlineKeyboardButton('100💰', callback_data="betDone_{}_{}_100".format(game.id, winner)))
            markup.add(InlineKeyboardButton('200💰', callback_data="betDone_{}_{}_200".format(game.id, winner)), InlineKeyboardButton('500💰', callback_data="betDone_{}_{}_500".format(game.id, winner)))
            markup.add(InlineKeyboardButton('1000💰', callback_data="betDone_{}_{}_1000".format(game.id, winner)), InlineKeyboardButton('2000💰', callback_data="betDone_{}_{}_2000".format(game.id, winner)))
            markup.add(InlineKeyboardButton('5000💰', callback_data="betDone_{}_{}_5000".format(game.id, winner)), InlineKeyboardButton('10000💰', callback_data="betDone_{}_{}_10000".format(game.id, winner)))
            markup.add(InlineKeyboardButton('Отменить ставку', callback_data="dvp"))
        elif game.status == 2:
            text = "К сожалению, событие уже началось."
        else:
            text = "К сожалению, событие уже завершилось."
    else:
        text = "Такого события не существует."
    try:
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    except:
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

async def betDone_(call, user):
    gameId = call.data.split("_")[1]
    winner = call.data.split("_")[2]
    bet = int(call.data.split("_")[3])
    user = await db.Users.get(user_id=call.from_user.id)
    game = await db.Matches.get_or_none(id=gameId)
    if game:
        if game.status == 1:
            if user.money >= bet:
                await db.Bets.create(idplayer=user.id, idmatch=gameId, summ=bet, winner=winner, status=1)
                await db.Users.filter(id=user.id).update(money=F('money') - bet)
                if winner == 'p1':
                    await db.Matches.filter(id=gameId).update(w1sum=F('w1sum') + bet)
                else:
                    await db.Matches.filter(id=gameId).update(w2sum=F('w2sum') + bet)
                text = "Ставка принята!"
            else:
                text = "Недостаточно 💰"
        elif game.status == 2:
            text = "К сожалению, событие уже началось."
        else:
            text = "К сожалению, событие уже завершилось."
    else:
        text = "Такого события не существует."
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



@dp.message_handler(commands=['ownaddmatch'])
async def ownaddmatch(m):
    if str(m.from_user.id) in owner or str(m.from_user.id) in devs:
        match = m.text.replace('/ownaddmatch ', '', 1).split(':')
        try: 
            print(match[3])
        except:
            await m.reply("/ownaddmatch Ивент:Игрок1:Игрок2:Коммисия")
            return
        newMatch = await db.Matches.create(tournament=match[0], p1=match[1], p2=match[2], commision=match[3], w1sum=1, w2sum=1, status=1)
        await m.reply("Было создано событие:\nИвент: {}\nИгрок 1: {}\nИгрок 2: {}\nКоммисия события: {}%".format(match[0], match[1], match[2], match[3]))

@dp.message_handler(commands=['ownmatches'])
async def ownmatches(m):
    if str(m.from_user.id) in owner or str(m.from_user.id) in devs:
        matches = await db.Matches.filter(~Q(status=3))
        text = "Запланированные события:\n"
        for match in matches:
            if match.status == 1: status = 'Запланировано'
            elif match.status == 2: status = 'Live'
            else: status = 'Неизвестно'
            text += "\nИвент: {}. {} vs {}. Статус: {} /owneditmatch_{}".format(match.tournament, match.p1, match.p2, status, match.id)
        await m.answer(text)


@dp.message_handler(lambda m:m.text and m.text.startswith('/owneditmatch_'))
async def owneditmatch_(m):
    if m.chat.id != m.from_user.id: return
    user = await db.Users.get(user_id=m.from_user.id)
    result = m.text.replace('/owneditmatch_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    game = await db.Matches.get_or_none(id=result)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if game:
        if game.status == 1: status = 'Запланировано'
        elif game.status == 2: status = 'Live'
        else: game = 'Неизвестно'
        text = "\nИвент: {}. {} vs {}. Статус: {}".format(game.tournament, game.p1, game.p2, status, game.id)
        allbets = (game.w1sum + game.w2sum)
        kf_player1 = (allbets / game.w1sum) - ((allbets / game.w1sum) * (game.commision / 100))
        if kf_player1 < 1: kf_player1 = 1.00
        kf_player2 = (allbets / game.w2sum) - ((allbets / game.w2sum) * (game.commision / 100))
        if kf_player2 < 1: kf_player2 = 1.00
        text += "\n\n[{}] {} vs {}\nx{} ({}💰) vs x{} ({}💰)".format(game.tournament, game.p1, game.p2, round(kf_player1, 2), game.w1sum, round(kf_player2, 2), game.w2sum)
        if game.status == 1:
            markup.add(InlineKeyboardButton('Отправить в LIVE', callback_data="editMatch_{}_status".format(game.id)))
        markup.add(InlineKeyboardButton('Победа {}'.format(game.p1), callback_data="editMatch_{}_p1Win".format(game.id)))
        markup.add(InlineKeyboardButton('Победа {}'.format(game.p2), callback_data="editMatch_{}_p2Win".format(game.id)))
        markup.add(InlineKeyboardButton('Возврат', callback_data="editMatch_{}_canceled".format(game.id)))
    else:
        text = "Матч не найден"
    await bot.send_message(m.chat.id, text, reply_markup=markup)



async def editMatch_(call, user):
    game = await db.Matches.get_or_none(id=call.data.split("_")[1])
    if game:
        await bot.edit_message_text("Обработка...", call.message.chat.id, call.message.message_id)
        if call.data.split("_")[2] == 'status':
            if game.status == 1:
                await db.Matches.filter(id=game.id).update(status=2)
                text = "Отправлено в LIVE"
                allBets = await db.Bets.filter(idmatch=game.id, status=1)
                for bet in allBets:
                    user = await db.Users.get_or_none(id=bet.idplayer)
                    try:
                        await bot.send_message(user.user_id, "Началось событие:\n[{}] {} vs {}".format(game.tournament, game.p1, game.p2))
                        await asyncio.sleep(.5)
                    except:
                        pass
        elif call.data.split("_")[2] == 'p1Win':
            allBets = await db.Bets.filter(idmatch=game.id, winner='p1', status=1)
            for bet in allBets:
                allbets = (game.w1sum + game.w2sum)
                kf_player1 = (allbets / game.w1sum) - ((allbets / game.w1sum) * (game.commision / 100))
                if kf_player1 <= 1: kf_player1 = 1.01
                award = int(bet.summ * kf_player1)
                await db.Users.filter(id=bet.idplayer).update(money=F('money') + award)
                user = await db.Users.get_or_none(id=bet.idplayer)
                try:
                    await bot.send_message(user.user_id, "Ваша ставка в матче {} vs {} победила. Поздравляем!\nЗачислено: {}💰".format(game.p1, game.p2, award))
                    await asyncio.sleep(1)
                except:
                    pass
            text = "Выигрыши розданы, событие закрыто."
            await db.Matches.filter(id=game.id).update(status=3, winner=game.p1)
            awardForPlayers = ((game.w1sum + game.w2sum) * game.commision / 200)
            player1 = await db.Users.get_or_none(username=game.p1)
            if player1:
                await db.Users.filter(id=player1.id).update(money=F('money') + awardForPlayers)
                try:
                    await bot.send_message(player1.user_id, "За ставки в вашей игре вам зачислено {}💰".format(awardForPlayers))
                except:
                    pass
            player2 = await db.Users.get_or_none(username=game.p2).first()
            if player2:
                await db.Users.filter(id=player2.id).update(money=F('money') + awardForPlayers)
                try:
                    await bot.send_message(player2.user_id, "За ставки в вашей игре вам зачислено {}💰".format(awardForPlayers))
                except:
                    pass
        elif call.data.split("_")[2] == 'p2Win':
            allBets = await db.Bets.filter(idmatch=game.id, winner='p2', status=1)
            for bet in allBets:
                allbets = (game.w1sum + game.w2sum)
                kf_player2 = (allbets / game.w2sum) - ((allbets / game.w2sum) * (game.commision / 100))
                if kf_player2 <= 1: kf_player2 = 1.01
                award = int(bet.summ * kf_player2)
                await db.Users.filter(id=bet.idplayer).update(money=F('money') + award)
                user = await db.Users.get_or_none(id=bet.idplayer)
                try:
                    await bot.send_message(user.user_id, "Ваша ставка в матче {} vs {} победила. Поздравляем!\nЗачислено: {}💰".format(game.p1, game.p2, award))
                    await asyncio.sleep(1)
                except:
                    pass
            await db.Matches.filter(id=game.id).update(status=3, winner=game.p2)
            awardForPlayers = ((game.w1sum + game.w2sum) * game.commision / 200)
            player1 = await db.Users.get_or_none(username=game.p1)
            if player1:
                await db.Users.filter(id=player1.id).update(money=F('money') + awardForPlayers)
                try:
                    await bot.send_message(player1.user_id, "За ставки в вашей игре вам зачислено {}💰".format(awardForPlayers))
                except:
                    pass
            player2 = await db.Users.get_or_none(username=game.p2).first()
            if player2:
                await db.Users.filter(id=player2.id).update(money=F('money') + awardForPlayers)
                try:
                    await bot.send_message(player2.user_id, "За ставки в вашей игре вам зачислено {}💰".format(awardForPlayers))
                except:
                    pass
            text = "Выигрыши розданы, событие закрыто."
        elif call.data.split("_")[2] == 'canceled':
            allBets = await db.Bets.filter(idmatch=game.id, winner__in=['p2', 'p1'], status=1)
            for bet in allBets:
                award = int(bet.summ)
                await db.Users.filter(id=bet.idplayer).update(money=F('money') + award)
                user = await db.Users.get_or_none(id=bet.idplayer)
                try:
                    await bot.send_message(user.user_id, "Ваша ставка в матче {} vs {} была возвращена.\nЗачислено: {}💰".format(game.p1, game.p2, award))
                    await asyncio.sleep(1)
                except:
                    pass
            await db.Matches.filter(id=game.id).update(status=3, winner='Игра отменена')
            text = "Ставки возвращены, событие закрыто."
        await bot.send_message(call.message.chat.id, text)