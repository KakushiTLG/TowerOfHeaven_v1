async def parlament(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    checkPresident = await db.System.get(name='presidentId')
    user = await db.Users.get(user_id=m.from_user.id)
    if checkPresident.value == user.id:
        fondMoney = await db.System.get(name='HeavenFondGold')
        fondKri = await db.System.get(name='HeavenFondKri')
        text = "Городской фонд: {}💰 {}💎".format(fondMoney.value, fondKri.value)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Просмотр и смены коммисий', callback_data="parl_commisions"))
        await bot.send_message(m.chat.id, "Привет, Янукович. Пришло время попиздить денежку во благо золотого унитаза.\n{}".format(text), reply_markup=markup)

async def parl_commisions(call, user):
    if call.message.chat.id != call.from_user.id:
        return
    checkPresident = await db.System.get(name='presidentId')
    if checkPresident.value == user.id:
        barCoinGold = await db.System.get(name='commisionCoin')
        barCoinKri = await db.System.get(name='commisionCoinKri')
        raskulova = await db.System.get(name='commisionRaskulova')
        barCoinx3 = await db.System.get(name='commisionCoinTriple')
        text = "Список коммисий\n\nАвтомат: 15💰(⛔️)\n"
        text += "Ставки на 💰: {}%  =>  /changeCom_coinGold\n".format(barCoinGold.value)
        text += "Ставки на 💎: {}%  =>  /changeCom_coinKri\n".format(barCoinKri.value)
        text += "Продажа в Раскуловой: {}%  =>  /changeCom_raskulova\n".format(raskulova.value)
        text += "Ставки х3: {}% => /changeCom_coinTriple".format(barCoinx3.value)
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



async def changeCom_(m, user):
    if m.chat.id != m.from_user.id: return
    checkPresident = await db.System.get(name='presidentId')
    user = await db.Users.get(user_id=m.from_user.id)
    if checkPresident.value == user.id:
        result = m.text.replace('/changeCom_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
        values = result.split(" ")
        try:
            newValue = values[1]
        except:
            await bot.send_message(m.chat.id, "/changeCom_example number. Число должно быть положительным и не превышать 25%")
            return
        if int(newValue) >= 0 and int(newValue) <= 25:
            if values[0] == 'coinGold': await db.System.filter(name='commisionCoin').update(value=int(newValue))
            elif values[0] == 'coinKri': await db.System.filter(name='commisionCoinKri').update(value=int(newValue))
            elif values[0] == 'raskulova': await db.System.filter(name='commisionRaskulova').update(value=int(newValue))
            elif values[0] == 'coinTriple': await db.System.filter(name='commisionCoinTriple').update(value=int(newValue))
            else:
                return
            await bot.send_message(m.chat.id, "Новая коммисия установлена")
        else:
            await bot.send_message(m.chat.id, "/changeCom_example number. Число должно быть положительным и не превышать 25%")



