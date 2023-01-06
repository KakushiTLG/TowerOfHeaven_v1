async def bp(m, user):
    if m.chat.id == m.from_user.id:
        pass
    else:
        return
    timeEnd = 1651323469
    leftTime = int((timeEnd - time.time()) / 86400)
    text = "Пропуск испытаний - выполняйте задания у охранника бара и получайте вознаграждения! Главный приз\nх10 📜Свиток башни (Моментально перемещает вас на первый этаж башни, минуя тропу), x10 📜Туннельный свиток (Телепортирует в Город), х10 🎟Бесплатная путёвка на Свалку (SR2), а так же - 🪙Монеты возвышения оружия!\n\n🔆{}/25".format(user.bpLvl)
    allText = "👁‍🗨Пропуск рекрута: 17500💰 65🧪 260🦴 30⚡️ 5🔘 5+5📜 5🎟 2🎉 1 🪙Монета возвышения\n\n🃏Пропуск элитного воина: 35000💰 130🧪 260🦴 60⚡️ 10🔘 10+10📜 10🎟 5🎉 2 🪙Монета возвышения \n\n"
    if user.bpStatus == 0:
        text += "\n👁‍🗨Пропуск рекрута"
    else:
        text += "\n🃏Пропуск элитного воина"
    if user.bpStatus == 0:
        money = 700
        full_heal = 0
        kosti = 0
        boost = 0
        uppts = 0
        if user.bpLvl % 2 == 0:
            full_heal = 1
            kosti = 1
        if user.bpLvl in [5, 10, 15, 20, 24]: #ну или можно 1, 50, 100
            boost = 1
            uppts = 1
        textAward = "\n{}💰".format(money)
        if full_heal==1: textAward += " 5🧪"
        if kosti==1: textAward += " 20🦴"
        if boost==1: textAward += " 6⚡️"
        if uppts==1: textAward += " 1🔘"
        if user.bpLvl == 24: textAward += " 5🔘 5+5📜 5🎟 2🎉 1🪙"
        text += "\n\nНаграда за {} уровень: {}\n".format(user.bpLvl, textAward)
    money = 1400
    full_heal = 0
    kosti = 0
    boost = 0
    uppts = 0
    if user.bpLvl % 2 == 0:
        full_heal = 1
        kosti = 1
    if user.bpLvl in [5, 10, 15, 20, 24]: #ну или можно 1, 50, 100
        boost = 1
        uppts = 1
    textAward = "\n{}💰".format(money)
    if full_heal==1: textAward += " 10🧪"
    if kosti==1: textAward += " 10🦴"
    if boost==1: textAward += " 12⚡️"
    if uppts==1: textAward += " 1🔘"
    if user.bpLvl == 24: textAward += " 10🔘 10+10📜 10🎟 5🎉 2🪙"
    if user.bpStatus == 1:
        text += "\n\nНаграда за {} уровень: {}\n\nВсе награды: \n{}".format(user.bpLvl, textAward, allText)
    else:
        text += "\n\nНаграда за {} уровень с Пропуском элитного воина: {}\n\nПриобрести Пропуск элитного воина можно в ломбарде\n\nВсе награды: \n{}".format(user.bpLvl, textAward, allText)
    if user.bpLvl >= 25:
        text = "Пропуск испытаний - выполняйте квесты у охранника бара и получайте вознаграждения!\n🔆: {}/25\n\nВы успешно прошли испытания!\n\nВсе полученные вами награды: \n{}".format(user.bpLvl, allText)
    text += "\n\nДо окончания пропуска: {}дн.".format(leftTime)
    await bot.send_message(m.chat.id, text)



async def getAwardBp(user):
    if user.bpLvl < 25:
        pass
    else:
        textAward = ""
        return textAward
    if user.bpStatus == 0:
        await db.Users.filter(id=user.id).update(money=F('money') + 700)
        textAward = "Уровень пропуска испытаний повышен! Награда:\n700💰"
        if user.bpLvl % 2 == 0:
            textAward += " 5🧪 20🦴"
            await db.addItem('Зелье восстановления', user, arg='1')
            await db.addItem('Зелье восстановления', user, arg='1')
            await db.addItem('Зелье восстановления', user, arg='1')
            await db.addItem('Зелье восстановления', user, arg='1')
            await db.addItem('Зелье восстановления', user, arg='1')
            for i in range(0, 20):
                await db.addItem('Останки героев', user, arg='1')
        if user.bpLvl in [5, 10, 15, 20, 24]: #ну или можно 1, 50, 100
            await db.addBoost(user, lvl=6)
            textAward += " 6⚡️ 1🔘"
            await db.Users.filter(id=user.id).update(uppts=F('uppts') + 1)
        if user.bpLvl == 24: 
            for i in range(0, 5):
                await db.addItem('Свиток башни', user, arg='1')
            for i in range(0, 5):
                await db.addItem('Туннельный свиток', user, arg='1')
            for i in range(0, 5):
                await db.addItem('Бесплатная путёвка на свалку', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            newitem = await db.Inventory(name='Монета возвышения', idplayer=user.id, active=6, bonus=0, size=0, type='Прочее', atk_block=0, expires=0, count=0, lvl=0)
            await newitem.save()
            await db.Users.filter(id=user.id).update(uppts=F('uppts') + 5)
            textAward += " 5+5📜 5🔘 1🪙"
    else:
        await db.Users.filter(id=user.id).update(money=F('money') + 1400)
        textAward = "Уровень пропуска испытаний повышен! Награда:\n1400💰"
        if user.bpLvl % 2 == 0:
            for i in range(0, 10):
                await db.addItem('Зелье восстановления', user, arg='1')
            for i in range(0, 20):
                await db.addItem('Останки героев', user, arg='1')
            textAward += " 10🧪 20🦴"
        if user.bpLvl in [5, 10, 15, 20, 24]: #ну или можно 1, 50, 100
            await db.addBoost(user, lvl=12)
            await db.Users.filter(id=user.id).update(uppts=F('uppts') + 1)
            textAward += " 12⚡️ 1🔘"
        if user.bpLvl == 24:
            for i in range(0, 10):
                await db.addItem('Свиток башни', user, arg='1')
            for i in range(0, 10):
                await db.addItem('Туннельный свиток', user, arg='1')
            for i in range(0, 10):
                await db.addItem('Бесплатная путёвка на свалку', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            await db.addItem('Хлопушка', user, arg='1')
            newitem = await db.Inventory(name='Монета возвышения', idplayer=user.id, active=6, bonus=0, size=0, type='Прочее', atk_block=0, expires=0, count=0, lvl=0)
            await newitem.save()
            await db.commitInventory(user, newitem)
            newitem = await db.Inventory(name='Монета возвышения', idplayer=user.id, active=6, bonus=0, size=0, type='Прочее', atk_block=0, expires=0, count=0, lvl=0)
            await newitem.save()
            await db.commitInventory(user, newitem)
            await db.Users.filter(id=user.id).update(uppts=F('uppts') + 10)
            textAward += "10+10📜 10🎟 10🔘 2🪙"
    await db.Users.filter(id=user.id).update(bpLvl=F('bpLvl') + 1)
    textAward += "\n\nПодробнее /bp"
    return textAward
