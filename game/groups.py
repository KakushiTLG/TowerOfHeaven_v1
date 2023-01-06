class FractionActions(StatesGroup):
    deposit = State()
    frac_kick_reason = State()
    ad_text = State()
    player_award = State()
    clanCreation = State()
    clanAd = State()



async def nav_base(call, user):
    navWhere = call.data.split("_")
    nav = navWhere[2]
    frak = await db.Fraks.get_or_none(name=user.frak)
    if frak:
        if user.location != 'База клана':
            if user.location != 'Окрестности {}'.format(frak.name):
                return
            else:
                await db.Users.filter(id=user.id).update(location='База клана')
                await user.refresh_from_db()
        if nav == 'onsen':
            if frak.onsenLvl == 0:
                await bot.edit_message_text("К сожалению, лидер еще не выделил средства на постройку.", call.message.chat.id, call.message.message_id)
            else:
                await db.Users.filter(id=user.id).update(position='Источники')
                await bot.edit_message_text("Эх, как хорошо... В этих источниках уж точно нет ни мочи, ни, к сожалению, девиц, однако очень приятно вот так вот посидеть и помедитировать в горячей воде...\n\nВосстановление по {}%❤️/мин".format(frak.onsenLvl), call.message.chat.id, call.message.message_id)    
        elif nav == 'hotel':
            if frak.hotelLvl == 0:
                await bot.edit_message_text("К сожалению, лидер еще не выделил средства на постройку.", call.message.chat.id, call.message.message_id)
            else:
                await db.Users.filter(id=user.id).update(position='Собственная комната')
                await bot.edit_message_text("Вот что действительно неплохо в резиденции клана, так это комнаты. У каждого своя личная комната! Можно отдыхать сколько душа пожелает!\n\nВосстановление по {}⚡️/мин".format(frak.hotelLvl), call.message.chat.id, call.message.message_id)    
        elif nav == 'centr':
            await db.Users.filter(id=user.id).update(position='Сад')
            if frak.leader == user.id or frak.zam == user.id:
                await bot.edit_message_text("Ах, какое же прекрасное место! Вокруг ростут деревья, птички поют - это самый настоящий рай! А еще в этом месте решаются финансовые (и не только) вопросы клана.", call.message.chat.id, call.message.message_id)    
            else:
                await bot.edit_message_text("Ах, какое же прекрасное место! Вокруг ростут деревья, птички поют - это самый настоящий рай! А еще в этом месте можно подождать выплаты от лидера, или же через клерка внести деньги в фонд.", call.message.chat.id, call.message.message_id)    
            await asyncio.sleep(1)
            await grouppanel(call, user)
        elif nav == 'exitHeaven':
            await db.Users.filter(id=user.id).update(location='Хэвенбург', position='Площадь')
            await bot.edit_message_text("Собравшись с силами, двинулся в сторону Хэвенбурга...", call.message.chat.id, call.message.message_id)
        elif nav == 'exitTower':
            await db.Users.filter(id=user.id).update(location='Тропа к башне', progLoc='Тропа к башне|0', progStatus=1)
            await bot.edit_message_text("Собравшись с силами, двинулся в сторону башни...", call.message.chat.id, call.message.message_id)
        elif nav == 'security':
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('1', callback_data="frakSecurity_1"))
            markup.add(InlineKeyboardButton('2', callback_data="frakSecurity_2"))
            markup.add(InlineKeyboardButton('3', callback_data="frakSecurity_3"))
            markup.add(InlineKeyboardButton('4', callback_data="frakSecurity_4"))
            markup.add(InlineKeyboardButton('5', callback_data="frakSecurity_5"))
            await bot.edit_message_text("Выбери охраняемый квадрат.", call.message.chat.id, call.message.message_id, reply_markup=markup)

        elif nav == 'krazha':
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            fraks = await db.Fraks.filter(~Q(name=user.frak)).only('id', 'name', 'cooldown')
            for z in fraks:
                if z.cooldown >= int(time.time()):
                    pass
                else:
                    markup.add(InlineKeyboardButton('Налёт на {}'.format(z.name), callback_data="frakKrazha_{}".format(z.id)))
            markup.add(InlineKeyboardButton('Я передумал, мама, забери меня!', callback_data="nav_base_centr"))
            await bot.edit_message_text("Кого сегодня грабить будем?", call.message.chat.id, call.message.message_id, reply_markup=markup)



async def frakKrazha(call, user):
    navWhere = call.data.split("_")
    nav = navWhere[1]
    frak = await db.Fraks.get_or_none(name=user.frak)
    selectedFrak = await db.Fraks.get_or_none(id=nav)
    if selectedFrak and user.location == 'База клана' and selectedFrak.cooldown <= int(time.time()):
        newProgLoc = "Окрестности {}|0".format(selectedFrak.name, nav)
        location = "Окрестности {}".format(selectedFrak.name)
        await db.Users.filter(id=user.id).update(progLoc=newProgLoc, location=location, progStatus=1)
        await bot.edit_message_text("Ты отправился в попытку ограбить всё что найдёшь у {}".format(selectedFrak.name), call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Возникла ошибка. Возможно у клана иммунитет либо же вы находитесь вне базы своей клана.", call.message.chat.id, call.message.message_id)

async def frakSecurity_(call, user):
    navWhere = call.data.split("_")
    nav = navWhere[1]
    frak = await db.Fraks.get_or_none(name=user.frak)
    if frak and user.location == 'База клана':
        newProgLoc = "Окрестности {}|{}".format(frak.name, nav)
        location = "Окрестности {}".format(frak.name)
        await db.Users.filter(id=user.id).update(progLoc=newProgLoc, location=location)
        await bot.edit_message_text("Через меня никто не пройдёт! С важным видом занимаешь нужный квадрат и приступаешь к патрулированию.\n⚠️Патрулирование базы - весьма ответственная задача. Если кто-то из другого клана решится на ограбление, вам предстоит сражаться с этим игроком в автоматическом режиме PvP.", call.message.chat.id, call.message.message_id)
    else:
        return

async def grouppanel(call, user):
    fraka = str(user.frak)
    frak = await db.Fraks.get(name=fraka)
    needExp = frak.lvl * 1000
    leader = await db.Users.get(id=frak.leader)
    zam = await db.Users.exists(id=frak.zam)
    frakplayers = await db.Users.filter(frak=frak.name).count()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if frak.lvl >= 8: maxPlayers = 10
    else: maxPlayers = frak.lvl + 2
    if zam:
        zam = await db.Users.get(id=frak.zam)
        text = "{}\n🏆{}🏆\n🥈{}🥈\n\n✳️Уровень: {}\n❇️Опыт: {}/{}\n💰Фонд: {}💰 {}💎\n👥Участников: {}/{}\n🔪Бонус атаки +{}%\n\n\n🟣{}\n🔴{}\n🔵{}\n🟢{}\n⭐️Бонус к силе: {}\nДебафф башни: {}%\n\n⛲️Источники {} уровня\n🏫Ночлег {} уровня".format(frak.name, leader.username, zam.username, frak.lvl, frak.exp, needExp, frak.fond, frak.fondKri, frakplayers, maxPlayers, frak.atk, frak.ametist, frak.rubin, frak.sapphire, frak.izumrud, frak.pvpBonus, frak.debuff, frak.onsenLvl, frak.hotelLvl)
    else:
        text = "{}\n🏆{}🏆\n\n✳️Уровень: {}\n❇️Опыт: {}/{}\n💰Фонд: {}💰 {}💎\n👥Участников: {}/{}\n🔪Бонус атаки +{}%\n\n\n🟣{}\n🔴{}\n🔵{}\n🟢{}\n⭐️Бонус к силе: {}\n Дебафф башни: {}%\n\n⛲️Источники {} уровня\n🏫Ночлег {} уровня".format(frak.name, leader.username, frak.lvl, frak.exp, needExp, frak.fond, frak.fondKri, frakplayers, maxPlayers, frak.atk, frak.ametist, frak.rubin, frak.sapphire, frak.izumrud, frak.pvpBonus, frak.debuff, frak.onsenLvl, frak.hotelLvl)
    if frak.cooldown >= int(time.time()):
        timeLeft = frak.cooldown - int(time.time())
        if timeLeft <= 172800:
            timeleft = timeLeft / 3600
            boostLeft = "{}ч".format(round(timeleft, 2))
        else:
            timeleft = timeLeft / 86400
            boostLeft = "{}дн".format(int(timeleft))
        text += "\n\n🛡Иммунитет кражи {}".format(boostLeft)
    sunday = await db.System.get(name='sunday')
    saturday = await db.System.get(name='saturday')
    if leader.id == user.id:
        markup.add(InlineKeyboardButton('Панель основателя', callback_data="fraka_panel"))
    if sunday.value == 1:
        markup.add(InlineKeyboardButton('Сдать предметы', callback_data="sunday"))
    if saturday.value == 1 and frak.saturday == 1:
        markup.add(InlineKeyboardButton('Телепорт к боссу', callback_data="saturday"))
    if user.id == frak.zam:
        markup.add(InlineKeyboardButton('IRTSoT', callback_data="frakapanel_irtst"))
        markup.add(InlineKeyboardButton('Наградить игрока', callback_data="frakapanel_award"))
    markup.add(InlineKeyboardButton('Взнос в фонд', callback_data="fraka_pay"))
    if user.id  != leader.id:
        markup.add(InlineKeyboardButton('Покинуть клан', callback_data="fraka_leave"))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)



async def fraka(call, user): 
    if (call.from_user.id != call.message.chat.id):
        return

    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if user.location == 'База клана' and user.position == 'Сад':
        if navWhere == "pay":
            await bot.edit_message_text("Введите сумму (валюта выбирается позже) для вклада в фонд клана. У вас {}💰 {}💎\nДля отмены, нажмите кнопку ''Отменить''.".format(user.money, user.almaz), call.message.chat.id, call.message.message_id)
            await FractionActions.deposit.set()
        elif navWhere == "panel":
            if fraka.leader == user.id:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('IRTSoT', callback_data="frakapanel_irtst"))
                markup.add(InlineKeyboardButton('Выгнать игрока', callback_data="frakapanel_kick"))
                markup.add(InlineKeyboardButton('Рекламная кампания', callback_data="frakapanel_ads"))
                markup.add(InlineKeyboardButton('Наградить игрока', callback_data="frakapanel_award"))
                markup.add(InlineKeyboardButton('Прокачка бонусов', callback_data="frakapanel_kach"))
                markup.add(InlineKeyboardButton('Назначение заместителя', callback_data="frakapanel_zam"))
                markup.add(InlineKeyboardButton('Передать права владения', callback_data="frakapanel_changeLead"))
                markup.add(InlineKeyboardButton('Продлить иммунитет на 12ч (15💎)', callback_data="frakapanel_immunity"))
                await bot.edit_message_text("Выберите действие", call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                return
        elif navWhere == 'leave':
            if fraka.leader != user.id:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(InlineKeyboardButton('Нет', callback_data="fraka_leaveNo"))
                markup.add(InlineKeyboardButton('Нет', callback_data="fraka_leaveNo"))
                markup.add(InlineKeyboardButton('Да', callback_data="fraka_leaveYes"))
                markup.add(InlineKeyboardButton('Нет', callback_data="fraka_leaveNo"))
                markup.add(InlineKeyboardButton('Нет', callback_data="fraka_leaveNo"))
                await bot.edit_message_text("Ты уверен?", call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'leaveNo':
            await bot.edit_message_text("Хорошо, сообщи если передумаешь.", call.message.chat.id, call.message.message_id)
        elif navWhere == 'leaveYes':
            if fraka.leader != user.id:
                await db.Users.filter(id=user.id).update(frak="", location='Хэвенбург', position='Площадь')
                await bot.edit_message_text("Ты покинул клан.", call.message.chat.id, call.message.message_id)
                try:
                    await bot.send_message(leader.user_id, f"Игрок {user.username} принял решение покинуть клан.")
                except:
                    pass
            else:
                await bot.edit_message_text("Лидер не может покинуть собственный клан, они же без тебя будут грустить!", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Необходимо зайти в сад для работы с кланом", call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=FractionActions.deposit, content_types=types.ContentTypes.TEXT)
async def vznosFrak(m, state=FSMContext):
    user = await db.Users.get(user_id=m.from_user.id)
    fraka = await db.Fraks.get(name=user.frak)

    if m.text.lower() == 'отменить':
        await m.answer("Действие отменено")
        await state.finish()
        return

    if not m.text.isdigit():
        await m.answer('Введите число.')
        return

    value = int(m.text)
    if value and value > 0:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton('💰', callback_data="vsnosFrak_{}_gold".format(value)))
        markup.add(InlineKeyboardButton('💎', callback_data="vsnosFrak_{}_almaz".format(value)))
        await m.answer("Выберите валюту:", reply_markup=markup)
        await state.finish()



async def frac_deposit(call, user): 
    if user.location != 'База клана' and user.position != 'Сад':
        await bot.edit_message_text("Здесь нет возможности внести взнос.", call.message.chat.id, call.message.message_id)
        return
    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    value = int(nav[1])
    valute = nav[2]
    if valute == 'gold':
        if user.money >= value:
            newFond = fraka.fond + value
            await db.Fraks.filter(name=user.frak).update(fond=newFond)
            await db.Users.filter(id=user.id).update(money=F('money') - value)
            await bot.edit_message_text("Вы успешно внесли {}💰 в фонд".format(value), call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} ({}) внёс {}💰 в фонд {}".format(user.username, user.id, value, user.frak))
        else:
            await bot.edit_message_text("У вас не хватает 💰", call.message.chat.id, call.message.message_id)
    elif valute == 'almaz':
        if user.almaz >= value:
            newFond = fraka.fondKri + value
            await db.Fraks.filter(name=user.frak).update(fondKri=newFond)
            await db.Users.filter(id=user.id).update(almaz=F('almaz') - value)
            await bot.edit_message_text("Вы успешно внесли {}💎 в фонд".format(value), call.message.chat.id, call.message.message_id)
            await logBot.send_message(tradeChat, "Игрок {} ({}) внёс {}💎 в фонд {}".format(user.username, user.id, value, user.frak))
        else:
            await bot.edit_message_text("У вас не хватает 💎", call.message.chat.id, call.message.message_id)


@dp.message_handler(commands=['tstats'])
async def irtst(m):
    user = await db.Users.get_or_none(user_id=m.from_user.id)
    if user:
        if user.frak:
            frak = await db.Fraks.get(name=user.frak)
            if frak.leader == user.id or frak.zam == user.id: 
                users = await db.Users.filter(frak=user.frak, location__in=['Тропа к башне', 'Первый этаж башни', 'Второй этаж башни', 'Третий этаж башни', 'Четвёртый этаж башни'])
                text = "In Real Time Stats of Tower\n"
                if users:
                    for z in users:
                        text += "\n[{}](tg://user?id={}) - {} ({}🔪 {}/{}❤️)".format(z.username, z.user_id, z.location, z.atk, z.nowhp, z.hp)
                else:
                    text += "\nВ башне сейчас никого"
                await bot.send_message(m.chat.id, text, parse_mode='markdown')


@dp.callback_query_handler(lambda call: call.from_user.id == call.message.chat.id and call.data.startswith('frakapanel_'))
async def frakapanel(call, state=FSMContext): 

    user = await db.Users.get(user_id=call.from_user.id)
    if user.location != 'База клана' and user.position != 'Сад':
        await bot.edit_message_text("Здесь нет возможности работы с кланом.", call.message.chat.id, call.message.message_id)
        return
    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if fraka.leader == user.id or fraka.zam == user.id:
        markup = InlineKeyboardMarkup(row_width=2)
        if navWhere == 'kick' and len(nav) > 2:
            kicking = int(nav[2])
            await state.update_data(player_to_kick=kicking)
            userToKick = await db.Users.get(id=kicking)
            if userToKick.frak == user.frak:
                text = 'Введите причину изгнания {}. Если вы ошиблись игроком, отправьте "Отменить".'.format(userToKick.username)
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                # bot.register_next_step_handler(gg, kickingFromFrak)
                await FractionActions.frac_kick_reason.set()
                return

        elif navWhere == 'kick' and len(nav) == 2:
            players = await db.Users.filter(~Q(id=fraka.leader), frak=user.frak)
            text = "Выберите игрока, которого хотите изгнать из клана:\n"
            for z in players:
                text += "\n[{}](tg://user?id={})".format(z.username, z.user_id)
                markup.add(InlineKeyboardButton('{}'.format(z.username), callback_data="frakapanel_kick_{}".format(z.id)))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')
        
        elif navWhere == 'ads':
            text = "Рекламная кампания.\nТекст рекламы:\n\n{}".format(fraka.adText)
            markup.add(InlineKeyboardButton('Сменить текст', callback_data="frakapanel_changeAdText"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

        elif navWhere == 'changeAdText':
            await bot.edit_message_text("Введите новый рекламный текст. Обратите внимание на то, что количество символов не должно превышать 150 знаков и смена рекламного текста стоит 20000💰, которые списываются с фонда клана. Отмена действия - написать ''Отменить''", call.message.chat.id, call.message.message_id)
            #bot.register_next_step_handler(gg, newTextForFrak)
            await FractionActions.ad_text.set()
            return

        elif navWhere == 'award' and len(nav) > 2:
            awarding = nav[2]
            userToAward = await db.Users.get(id=awarding)
            if userToAward.frak == user.frak:
                await state.update_data(player_award_id=awarding)
                text = 'Введите сумму награды для игрока {}.'.format(userToAward.username)
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                #bot.register_next_step_handler(gg, awardingFromFrak)
                await FractionActions.player_award.set()
                return
        elif navWhere == 'award' and len(nav) == 2:
            players = await db.Users.filter(frak=user.frak)
            text = "Выберите игрока, которого желаете наградить:"
            for z in players:
                text += "\n[{}](tg://user?id={})".format(z.username, z.user_id)
                markup.add(InlineKeyboardButton('{}'.format(z.username), callback_data="frakapanel_award_{}".format(z.id)))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='markdown')
        
        elif navWhere == 'irtst':
            users = await db.Users.filter(frak=user.frak)
            text = "In Real Time Stats of Tower\n"
            if users:
                for z in users:
                    if z.location in ['Тропа к башне', 'Первый этаж башни', 'Второй этаж башни', 'Третий этаж башни', 'Четвёртый этаж башни']:
                        text += "\n[{}](tg://user?id={}) - {} ({}🔪 {}/{}❤️)".format(z.username, z.user_id, z.location, z.atk, z.nowhp, z.hp)
            else:
                text += "\nВ башне сейчас никого"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')

        elif navWhere == 'kach':
            pricesForArmor = fraka.armor * 5 #ametist
            pricesForCreet = fraka.creet * 5 #rubin
            pricesForAtk = fraka.atk * 5 #sapphire
            priceForAnti = await priceToUpFrak(fraka, param='anti')
            priceForHotel = await priceToUpFrak(fraka, param='hotelLvl')
            priceForOnsen = await priceToUpFrak(fraka, param='onsenLvl')
            qw = priceForAnti.split("|")
            if qw[0] == 'Ametist': qname = "🟣"
            elif qw[0] == 'Rubin': qname = '🔴'
            elif qw[0] == 'Izumrud': qname = '🟢'
            elif qw[0] == 'Sapphire': qname = '🔵'
            elif qw[0] == 'Gold': qname = '💰'
            qwe = priceForHotel.split("|")
            if qw[0] == 'Ametist': qname = "🟣"
            elif qw[0] == 'Rubin': qname = '🔴'
            elif qw[0] == 'Izumrud': qname = '🟢'
            elif qw[0] == 'Sapphire': qname = '🔵'
            elif qw[0] == 'Gold': qname = '💰'
            qwer = priceForOnsen.split("|")
            if qw[0] == 'Ametist': qname = "🟣"
            elif qw[0] == 'Rubin': qname = '🔴'
            elif qw[0] == 'Izumrud': qname = '🟢'
            elif qw[0] == 'Sapphire': qname = '🔵'
            elif qw[0] == 'Gold': qname = '💰'
            text = "Текущие бонусы от клана:\n\n"
            if frak.lvl > frak.atk: text += "Бонус к атаке: + {}% | {}🔵".format(fraka.atk, pricesForAtk)
            else: text += "Бонус к атаке: + {}% | max".format(fraka.atk)
            if frak.lvl > frak.armor: text += "Бонус к броне: + {}% | {}🟣".format(fraka.armor, pricesForArmor)
            else: text += "Бонус к броне: + {}% | max".format(fraka.armor)
            if frak.lvl > frak.creet: text += "Бонус к криту: + {}% | {}🔴".format(fraka.creet, pricesForCreet)
            else: text += "Бонус к криту: + {}% | max".format(fraka.creet)
            if qw[1]: text += "\nАнти-грабёж: {}% | {}{}".format(fraka.anti, qw[1], qname)
            else: text += "\nАнти-грабёж: {}% | max".format(fraka.anti)
            if qwer[1]: text += "\nИсточники: {}% | {}{}".format(fraka.onsenLvl, qwer[1], qname)
            else: text += "\nИсточники: {}% | max".format(fraka.onsenLvl)
            if qwe[1]: text += "\nНочлег: {}% | {}{}".format(fraka.hotelLvl, qwe[1], qname)
            else: text += "\nНочлег: {}% | max".format(fraka.hotelLvl)
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Повысить бонус к атаке', callback_data="groupBonusKach_atk"))
            markup.add(InlineKeyboardButton('Повысить бонус к броне', callback_data="groupBonusKach_armor"))
            markup.add(InlineKeyboardButton('Повысить бонус к криту', callback_data="groupBonusKach_creete"))
            markup.add(InlineKeyboardButton('Повысить навык анти-грабежа', callback_data="groupBonusKach_anti"))
            markup.add(InlineKeyboardButton('Улучшить источники', callback_data="groupBonusKach_onsen"))
            markup.add(InlineKeyboardButton('Улучшить комнаты', callback_data="groupBonusKach_hotel"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'zam':
            markup = InlineKeyboardMarkup(row_width=2)
            users = await db.Users.filter(~Q(id=user.id), frak=user.frak)
            text = "Выбор заместителя клана. Заместитель может пользоваться IRTSoT и фондом."
            for x in users:
                markup.add(InlineKeyboardButton('{}'.format(x.username), callback_data="zamSet_{}".format(x.id)))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'changeLead':
            markup = InlineKeyboardMarkup(row_width=2)
            users = await db.Users.filter(~Q(id=user.id), frak=user.frak)
            text = "Выбор нового владельца клана."
            for x in users:
                markup.add(InlineKeyboardButton('{}'.format(x.username), callback_data="leadSet_{}".format(x.id)))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif navWhere == 'immunity':
            if fraka.fondKri >= 15:
                if fraka.cooldown >= int(time.time()):
                    await db.Fraks.filter(id=fraka.id).update(fondKri=F('fondKri') - 15, cooldown=F('cooldown') + 43200)
                else:
                    cooldown = int(time.time()) + 43200
                    await db.Fraks.filter(id=fraka.id).update(fondKri=F('fondKri') - 15, cooldown=cooldown)
                await bot.edit_message_text("Вы продлили иммунитет анти-кражи на 12 часов", call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("В фонде недостаточно кристаллов", call.message.chat.id, call.message.message_id)

async def zamSet_(call, user):

    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if user.id == fraka.leader:
        usr = await db.Users.exists(id=navWhere)
        if usr:
            usr = await db.Users.get(id=navWhere)
            if usr and usr.frak == fraka.name:
                await db.Fraks.filter(id=fraka.id).update(zam=usr.id)
                try:
                    await bot.send_message(usr.user_id, "Вы были назначены заместителем клана {}".format(frak.name))
                except:
                    pass
                await bot.edit_message_text("Вы успешно назначили {} заместителем.".format(usr.username), call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)

async def leadSet_(call, user):

    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if user.id == fraka.leader:
        usr = await db.Users.exists(id=navWhere)
        if usr:
            usr = await db.Users.get(id=navWhere)
            if usr and usr.frak == fraka.name:
                await db.Fraks.filter(id=fraka.id).update(leader=usr.id)
                try:
                    await bot.send_message(usr.user_id, "Вы были назначены новым владельцем клана {}".format(frak.name))
                except:
                    pass
                await bot.edit_message_text("Вы успешно назначили {} новым владельцем клана.".format(usr.username), call.message.chat.id, call.message.message_id)
            else:
                await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Ошибка", call.message.chat.id, call.message.message_id)


async def sunday(call, user):
    fraka = await db.Fraks.get(name=user.frak)
    sunday = await db.System.get(name='sunday')
    if user.location == 'База клана' and sunday.value == 1:
        checkItems = await db.Inventory.exists(name='Обломок синего камня', idplayer=user.id, active=1)
        if checkItems:
            count = await db.Inventory.filter(name='Обломок синего камня', idplayer=user.id, active=1).count()
            await db.Inventory.filter(name='Обломок синего камня', idplayer=user.id, active=1).update(active=0)
            await bot.edit_message_text("Ты внёс x{} Обломок синего камня".format(count), call.message.chat.id, call.message.message_id)
            await db.Temp.filter(user_id=user.frak).update(count=F('count') + count)
        else:
            await bot.edit_message_text("У тебя нет Обломок синего камня ", call.message.chat.id, call.message.message_id)



async def groupBonusKach_(call, user): 
    if (call.from_user.id == call.message.chat.id):
        pass
    else:
        return
    fraka = await db.Fraks.get(name=user.frak)
    nav = call.data.split('_')
    navWhere = nav[1]
    if user.id == fraka.leader:
        if navWhere == 'atk':
            if fraka.lvl > fraka.atk:
                need = fraka.atk * 5
                if fraka.sapphire >= need:
                    await db.Fraks.filter(name=fraka.name).update(atk=F('atk') + 1, sapphire=F('sapphire') - need)
                    text = "Приобретено."
                else:
                    text = "Недостаточно ресурсов."
            else:
                text = "Недоступно."
        elif navWhere == 'armor':
            if fraka.lvl > fraka.armor:
                need = fraka.armor * 5
                if fraka.ametist >= need:
                    await db.Fraks.filter(name=fraka.name).update(armor=F('armor') + 1, ametist=F('ametist') - need)
                    text = "Приобретено."
                else:
                    text = "Недостаточно ресурсов."
            else:
                text = "Недоступно."
        elif navWhere == 'creet':
            if fraka.lvl > fraka.creet:
                need = fraka.creet * 5
                if fraka.rubin >= need:
                    await db.Fraks.filter(name=fraka.name).update(creet=F('creet') + 1, rubin=F('rubin') - need)
                    text = "Приобретено."
                else:
                    text = "Недостаточно ресурсов."
            else:
                text = "Недоступно."
        elif navWhere == 'anti':
            priceForAnti = await priceToUpFrak(fraka, param='anti')
            qw = priceForAnti.split("|")
            value = int(qw[1])
            if fraka.fond >= value:
                await db.Fraks.filter(name=fraka.name).update(fond=F('fond') - value, anti=F('anti') + 1)
                text = "Приобретено."
            else:
                text = "Не хватает ресурсов."
        elif navWhere == 'onsen':
            priceForAnti = await priceToUpFrak(fraka, param='onsenLvl')
            qw = priceForAnti.split("|")
            value = int(qw[1])
            if fraka.fond >= value:
                await db.Fraks.filter(name=fraka.name).update(fond=F('fond') - value, onsenLvl=F('onsenLvl') + 1)
                text = "Приобретено."
            else:
                text = "Не хватает ресурсов."
        elif navWhere == 'hotel':
            priceForAnti = await priceToUpFrak(fraka, param='hotelLvl')
            qw = priceForAnti.split("|")
            value = int(qw[1])
            if fraka.fond >= value:
                await db.Fraks.filter(name=fraka.name).update(fond=F('fond') - value, hotelLvl=F('hotelLvl') + 1)
                text = "Приобретено."
            else:
                text = "Не хватает ресурсов."
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=FractionActions.ad_text, content_types=types.ContentTypes.TEXT)
async def newTextForFrak(m, state=FSMContext):
    user = await db.Users.get(user_id=m.from_user.id)
    fraka = await db.Fraks.get(name=user.frak)
    if m.text.lower() == 'отменить':
        await m.answer("Действие отменено")
        await state.finish()
        return

    if user.id == fraka.leader:
        if fraka.fond >= 20000:
            await db.Fraks.filter(name=fraka.name).update(adText=m.text, fond=F('fond') - 20000)
            await m.answer("Вы успешно сменили текст", reply_markup=types.ReplyKeyboardRemove())
        else:
            await m.answer("В фонде не хватает 💰", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=FractionActions.frac_kick_reason, content_types=types.ContentTypes.TEXT)
async def kickingFromFrak(m, state=FSMContext):

    if m.text.lower() == 'отменить':
        await m.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return

    data = await state.get_data()

    user = await db.Users.get(user_id=m.from_user.id)
    fraka = await db.Fraks.get(name=user.frak)
    check = 0
    userToKick = await db.Users.get(id=data['player_to_kick'])
    if userToKick.frak == fraka.name:
        await db.Users.filter(id=userToKick.id).update(frak='')
        await db.Fraks.filter(name=fraka.name).update(players=F('players') - 1)
        check = 1
        try:
            await bot.send_message(userToKick.user_id, "Вы были исключены из клана по решению её лидера. Причина:\n{}".format(m.text))
        except:
            pass
        try:
            await bot.kick_chat_member(groupid, userToKick.user_id)
        except:
            pass
        await bot.send_message(tradeChat, "Игрок {} был исключён из клана {}".format(userToKick.username, fraka.name))
        await bot.send_message(m.chat.id, "Вы успешно исключили игрока из клана", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    if check == 0:
        await m.answer("Произошла ошибка. Попробуйте еще раз", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return


@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=FractionActions.player_award, content_types=types.ContentTypes.TEXT)
async def awardingFromFrak(m, state=FSMContext):

    if not m.text.isdigit():
        await m.answer('Введите число.')
        return

    user = await db.Users.get(user_id=m.from_user.id)
    fraka = await db.Fraks.get(name=user.frak)
    check = 0
    data = await state.get_data()
    userToAward = await db.Users.get(id=data['player_award_id'])
    if userToAward.frak == fraka.name:
        if int(m.text) and fraka.fond >= int(m.text) and int(m.text) > 0:
            await db.Users.filter(id=userToAward.id).update(money=F('money') + int(m.text))
            await db.Fraks.filter(name=fraka.name).update(fond=F('fond') - int(m.text), limitFond=F('limitFond') + int(m.text))
            check = 1
            try:
                await bot.send_message(userToAward.user_id, "Вы были вознаграждены лидером вашего клана в размере {}💰".format(m.text))
            except:
                pass
            await bot.send_message(m.chat.id, "Вы успешно наградили участника {} в размере {}💰".format(userToAward.username, m.text))
            await bot.send_message(tradeChat, "ВЫПЛАТА ОТ ФРАКЦИИ {} ИГРОКУ {}({}) В РАЗМЕРЕ {}💰".format(fraka.name, userToAward.username, userToAward.id, m.text))
            await state.finish()
        else:
            await m.answer("Произошла ошибка. Число указано неверно, либо в фонде клана недостаточно 💰")
            await state.finish()
            return
    if check == 0:
        await m.answer("Произошла ошибка. Попробуйте еще раз")

@dp.message_handler(commands=['frak_award'])
async def frak_award(m):

    command = m.text.replace('/frak_award', '', 1).split(':')
    user = await db.Users.get(user_id=m.from_user.id)
    if user.location != 'База клана' and user.position != 'Сад':
        await bot.send_message(m.chat.id, "Отсюда нет возможности управлять кланом")
        return
    playerToAward = command[0]
    try:
        sumToAward = int(command[1])
    except:
        await bot.send_message(m.from_user.id, "Сумма указана не в числе")
        return
    frak = await db.Fraks.get(name=user.frak)
    if frak.leader == user.id or frak.zam == user.id:
        player = await db.Users.get(id=playerToAward)
        if sumToAward > 0 and sumToAward <= frak.fondKri and player.frak == frak.name:
            await db.Fraks.filter(name=frak.name).update(fondKri=F('fondKri') - int(sumToAward))
            await db.Users.filter(id=player.id).update(almaz=F('almaz') + int(sumToAward))
            await bot.send_message(m.from_user.id, "Вы наградили {} в размере {}💎".format(player.username, sumToAward))
            try:
                await bot.send_message(player.user_id, "Вы были вознаграждены лидером вашего клана в размере {}💎".format(sumToAward))
            except:
                pass
            await bot.send_message(tradeChat, "ВЫПЛАТА ОТ ФРАКЦИИ {} ИГРОКУ {}({}) В РАЗМЕРЕ {}💎".format(frak.name, player.username, player.id, m.text))
        else:
            await bot.send_message(m.from_user.id, "Ошибка зачисления.")
    else:
        return

@dp.callback_query_handler(lambda call: call.from_user.id == call.message.chat.id and call.data.startswith('tower_'))
async def tower_(call): 
    user = await db.Users.get(user_id=call.from_user.id)
    nav = call.data.split('_')
    navWhere = nav[1]
    if user.battleStatus == 2: return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Во время PvP особо не побегаешь...")                
    if navWhere == "1":
        if user.location == 'Второй этаж башни' and user.progLoc == 'Второй этаж башни|0' and user.nowhp > 0:
            # user.location = 'Первый этаж башни'
            # user.progLoc = 'Первый этаж башни|5'
            # user.progStatus = 1
            await db.Users.filter(id=user.id).update(location='Первый этаж башни',
                                                    progLoc='Первый этаж башни|5',
                                                    progStatus=1)
            text = "Вы перешли на первый этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "2":
        if user.location == 'Первый этаж башни' and user.progLoc == 'Первый этаж башни|5' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Второй этаж башни',
                                                    progLoc='Второй этаж башни|0',
                                                    progStatus=1)
            text = "Вы перешли на второй этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        elif user.location == 'Третий этаж башни' and user.progLoc == 'Третий этаж башни|0' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Второй этаж башни',
                                                    progLoc='Второй этаж башни|5',
                                                    progStatus=1)
            text = "Вы перешли на второй этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "3":
        if user.location == 'Второй этаж башни' and user.progLoc == 'Второй этаж башни|5' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Третий этаж башни',
                                                    progLoc='Третий этаж башни|0',
                                                    progStatus=1)
            text = "Вы перешли на третий этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        if user.location == 'Четвёртый этаж башни' and user.progLoc == 'Четвёртый этаж башни|0' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Третий этаж башни',
                                                    progLoc='Третий этаж башни|5',
                                                    progStatus=1)
            text = "Вы перешли на третий этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "4":
        if user.location == 'Третий этаж башни' and user.progLoc == 'Третий этаж башни|5' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Четвёртый этаж башни',
                                                    progLoc='Четвёртый этаж башни|0',
                                                    progStatus=1)
            text = "Вы перешли на четвёртый этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "5":
        if user.location == 'Четвёртый этаж башни' and user.progLoc == 'Четвёртый этаж башни|5' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Пятый этаж башни',
                                                    progLoc='Пятый этаж башни|0',
                                                    progStatus=1)
            text = "Вы перешли на пятый этаж башни"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    elif navWhere == "6":
        if user.location == 'Пятый этаж башни' and user.progLoc == 'Пятый этаж башни|13' and user.nowhp > 0:
            await db.Users.filter(id=user.id).update(location='Шестой этаж башни',
                                                    progLoc='Шестой этаж башни|0',
                                                    progStatus=1)
            text = "Вы перешли на шестой этаж башни пипец это как вообще"
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    else:
        text = "Недоступно. Обратитесь в /report"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



async def createClan(call, user):
    text = "Вы можете зарегистрировать свой клан, при условии наличия 75 уровня, а так же - оплатив государственный налог в размере 500000💰 и 500💎 (для игроков 200+ уровня бесплатно)."
    text += "\nИмея клан, вы сможете принимать заявки желающих вступить, управлять фондом клана, управлять призывом боссов, выбрать уполномоченного заместителя который сможет делать всё вышеупомянутое."
    text += "\n\nПосле создания, вы получите клан с 🛡Иммунитетом кражи в 2 недели, 🔪Бонусом атаки +20%"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if user.lvl >= 200 and user.id not in [2031, 723]:
        markup.add(InlineKeyboardButton('Зарегистрировать свой клан', callback_data="clanCreate"))
    elif user.lvl >= 75 and user.almaz >= 500 and user.money >= 500000:
        markup.add(InlineKeyboardButton('Зарегистрировать свой клан', callback_data="clanCreate"))
    markup.add(InlineKeyboardButton('Назад', callback_data="nav_bigcity_bar"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def clanCreate(call, user):
    if user.lvl >= 200:
        await FractionActions.clanCreation.set()
        await bot.edit_message_text("Введите название вашего будущего клана.\n⚠️Название должно иметь меньше 32 символов, запрещено использовать ненормативную лексику и слова сексуального характера, в противном случае клан будет удалён администрацией безвозвратно.", call.message.chat.id, call.message.message_id)
    elif user.lvl >= 75 and user.almaz >= 500 and user.money >= 500000:
        await db.Users.filter(id=user.id).update(almaz=F('almaz') - 500, money=F('money') - 500000)
        await FractionActions.clanCreation.set()
        await bot.edit_message_text("Введите название вашего будущего клана.\n⚠️Название должно иметь меньше 32 символов, запрещено использовать ненормативную лексику и слова сексуального характера, в противном случае клан будет удалён администрацией безвозвратно.", call.message.chat.id, call.message.message_id)


@dp.message_handler(state=FractionActions.clanCreation)
async def clanCreaction(m: types.Message, state=FSMContext):
    if len(m.text) <= 32:
        checkSame = await db.Fraks.get_or_none(name=m.text).first()
        if checkSame:
            await bot.send_message(m.chat.id, "К сожалению, клан с таким названием уже существует. Выберите новое.")
        else:
            kd = int(time.time()) + 1209600
            user = await db.Users.get_or_none(user_id=m.from_user.id).first()
            await db.Fraks.create(name=m.text, cooldown=kd, leader=user.id)
            await db.Users.filter(id=user.id).update(frak=m.text)
            await state.finish()
            await FractionActions.clanAd.set()
            await bot.send_message(m.chat.id, "Отлично. Теперь введите короткое описание клана, до 150 символов.")
    else:
        await bot.send_message(m.chat.id, "Название слишком длинное. Введите новое.\n⚠️Название должно иметь меньше 32 символов, запрещено использовать ненормативную лексику и слова сексуального характера, в противном случае клан будет удалён администрацией безвозвратно.")

@dp.message_handler(state=FractionActions.clanAd)
async def clanCreaction(m: types.Message, state=FSMContext):
    if len(m.text) <= 149:
        user = await db.Users.get_or_none(user_id=m.from_user.id).first()
        await db.Fraks.filter(name=user.frak).update(adText=m.text)
        await state.finish()
        await bot.send_message(m.chat.id, "Поздравляем с созданием собственного клана! Вы можете телепортироваться к базе своего клана через ворота Хэвенбурга.")
        await bot.send_message(tradeChat, f"Игрок {user.username} создал клан {user.frak}")
    else:
        await bot.send_message(m.chat.id, "Описание слишком длинное. Введите новое.\n⚠️Описание должно иметь меньше 150 символов, запрещено использовать ненормативную лексику и слова сексуального характера, в противном случае клан будет удалён администрацией безвозвратно.")


clansZayv = {}

@dp.message_handler(lambda m:m.text and m.text.startswith('/clanInfo_'))
async def clanInfo_(m):
    if m.chat.id != m.from_user.id: return
    user = await db.Users.get(user_id=m.from_user.id)
    result = m.text.replace('/clanInfo_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
    checkClan = await db.Fraks.get_or_none(id=result).first()
    if checkClan:
        if checkClan.name != user.frak:
            markup = InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(InlineKeyboardButton('Подать заявку на вступление', callback_data="joinClan_{}".format(checkClan.id)))
            leader = await db.Users.get_or_none(id=checkClan.leader).first()
            if leader:
                await m.answer("⚠️Подавая заявку на вступление в клан, лидер увидит ваши текущие характеристики\n\nКлан: {}.\nВладелец: {}\nКраткое описание: {}".format(checkClan.name, leader.username, checkClan.adText), reply_markup=markup)
            else:
                await m.answer("⚠️Подавая заявку на вступление в клан, лидер увидит ваши текущие характеристики\n\nКлан: {}.\nКраткое описание: {}".format(checkClan.name, checkClan.adText), reply_markup=markup)
        else:
            await m.answer("Ваш клан: {}. {}".format(checkClan.name, checkClan.adText))
    else:
        await m.answer("Такого клана не существует.")


async def joinClan_(call, user):
    if user.frak in ['', None]:
        checkClan = await db.Fraks.get_or_none(id=call.data.split("_")[1])
        if checkClan.name not in clansZayv: clansZayv[checkClan.name] = []
        if checkClan:
            if checkClan.name in clansZayv and user.id in clansZayv[checkClan.name]:
                return await bot.edit_message_text("Ты уже подавал заявку на вступление в этот клан недавно.", call.message.chat.id, call.message.message_id)
            leader = await db.Users.get_or_none(id=checkClan.leader)
            try:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                markup.add(InlineKeyboardButton('Принять заявку', callback_data="acceptClanJoin_{}".format(user.id)))
                markup.add(InlineKeyboardButton('Отклонить заявку', callback_data="declineClanJoin_{}".format(user.id)))
                await bot.send_message(leader.user_id, "⚠️Заявка на вступления в клан от {}.\nID: {}\n🔆: {}\n❤️: {}\n🔪: {}".format(user.username, user.id, user.lvl, user.hp, user.atk), reply_markup=markup)
            except:
                pass
            await bot.edit_message_text("Заявка на вступление в клан {} отправлена! Ожидайте решение лидера клана.".format(checkClan.name), call.message.chat.id, call.message.message_id)
            clansZayv[checkClan.name].append(user.id)
    else:
        await bot.edit_message_text("Кажется, вы уже состоите в клане", call.message.chat.id, call.message.message_id)

async def acceptClanJoin_(call, user):
    clan = await db.Fraks.get(name=user.frak).first()
    members = await db.Users.filter(frak=clan.name).count()
    if clan.lvl >= 8: maxPlayers = 10
    else: maxPlayers = clan.lvl + 2
    if members + 1 > maxPlayers:
        await bot.send_message(call.message.chat.id, "Не хватает слотов для участников клана.")
    else:
        member = await db.Users.get(id=call.data.split("_")[1]).first()
        if member.frak and member.frak != '':
            await bot.edit_message_text("Участник уже в другом клане.", call.message.chat.id, call.message.message_id)
        else:
            member.frak = clan.name
            await bot.edit_message_text("Участник принят в клан.", call.message.chat.id, call.message.message_id)
            await member.save()
            try:
                await bot.send_message(member.user_id, "Вы были приняты в клан {}!".format(clan.name))
            except:
                pass

async def declineClanJoin_(call, user):
    clan = await db.Fraks.get(name=user.frak).first()
    await bot.edit_message_text("Заявка отклонена.", call.message.chat.id, call.message.message_id)
    member = await db.Users.filter(id=call.data.split("_")[1]).first()
    try:
        await bot.send_message(member.user_id, "Клан {} отказал на вашу заявку на вступление в клан.".format(clan.name))
    except:
        pass





#async def saturday(call, user):
    #fraka = await db.Fraks.get(name=user.frak)
    #saturday = await db.System.get(name='saturday')
    #if user.location == 'База клана' and saturday.value == 1:
