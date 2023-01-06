async def addAch(player, ach):
    achm = await db.Ach.get(user_id=player.user_id).first()
    text = "\n⚠️Получено достижение - "
    if ach == 'novichek':
        #achm.novichek = '1|1'
        #player.money += 500
        await db.Ach.filter(id=achm.id).update(novichek='1|1')
        await db.Users.filter(id=player.id).update(money=F('money') + 1000)
        text += '"Уже не новичок"\n+1000💰'
    elif ach == 'novichek2':
        if achm.novichek == '1|1':
            await db.Ach.filter(id=achm.id).update(novichek='2|2')
            await db.Users.filter(id=player.id).update(money=F('money') + 2500)
            text += '"Хэвен, милый Хэвен..."\n+2500💰'
    elif ach == 'novichek3':
        if achm.novichek == '2|2':
            await db.Ach.filter(id=achm.id).update(novichek='3|3')
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Kawai! (^ ω ^)"\n+5000💰'
    elif ach == 'novichek4':
        if achm.novichek == '3|3':
            await db.Ach.filter(id=achm.id).update(novichek='4|4')
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Опытный сталкер"\n+10000💰'
    elif ach == 'novichek5':
        if achm.novichek == '4|4':
            await db.Ach.filter(id=achm.id).update(novichek='5|5')
            await db.Users.filter(id=player.id).update(money=F('money') + 25000)
            text += '"Из огня да в полымя..."\n+25000💰'
    elif ach == 'trader':
        z = achm.trader.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            trader = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(trader=trader)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"Новый трейдер"\n+50💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            trader = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(trader=trader)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Трейдер со стажем"\n+100💰'
        elif int(z[0]) >= 10 and int(z[1]) == 2:
            trader = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(trader=trader)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Мастер трейдинга"\n+200💰'
    elif ach == 'kachalka':
        z = achm.kachalka.split("|")
        if int(z[0]) >= 50 and int(z[1]) == 0: 
            kachalka = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Качок"\n+200💰'
        elif int(z[0]) >= 100 and int(z[1]) == 1:
            kachalka = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Завсегдатай качалки"\n+500💰'
        elif int(z[0]) >= 200 and int(z[1]) == 2:
            kachalka = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Задрот качалки"\n+1000💰'
        elif int(z[0]) >= 1000 and int(z[1]) == 3:
            kachalka = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"kachalOчка это моя жизнь"\n+5000💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 4:
            kachalka = "{}|5".format(z[0])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
            await db.Users.filter(id=player.id).update(uppts=F('uppts') + 10)
            text += '"Слыш, это я тут качок"\n+10🔘'
    elif ach == 'shopbuy':
        z = achm.shopbuy.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            shopbuy = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(shopbuy=shopbuy)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"Знакомство с Ашотом"\n+50💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            shopbuy = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(shopbuy=shopbuy)
            await db.Users.filter(id=player.id).update(money=F('money') + 150)
            text += '"Любитель 24/7 Аshopа"\n+150💰'
        elif int(z[0]) >= 200 and int(z[1]) == 2:
            shopbuy = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(shopbuy=shopbuy)
            await db.Users.filter(id=player.id).update(money=F('money') + 400)
            text += '"Постоянный покупатель"\n+400💰'
        elif int(z[0]) >= 1000 and int(z[1]) == 3:
            shopbuy = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(shopbuy=shopbuy)
            await db.Users.filter(id=player.id).update(money=F('money') + 2000)
            text += '"Скупщик"\n+2000💰'
    elif ach == 'skupshik':
        z = achm.skupshik.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            skupshik = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(skupshik=skupshik)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"Встретились два скупщика"\n+50💰'
        elif int(z[0]) >= 10 and int(z[1]) == 1:
            skupshik = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(skupshik=skupshik)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Самое ценное - себе"\n+200💰'
        elif int(z[0]) >= 50 and int(z[1]) == 2:
            skupshik = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(skupshik=skupshik)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Хламовый магнат"\n+1000💰'
    elif ach == 'alcohol':
        z = achm.alcohol.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            alcohol = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(alcohol=alcohol)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"А у вас точно качественный алкоголь?"\n+50💰'
        elif int(z[0]) >= 10 and int(z[1]) == 1:
            alcohol = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(alcohol=alcohol)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Хорошая компания"\n+100💰'
        elif int(z[0]) >= 50 and int(z[1]) == 2:
            alcohol = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(alcohol=alcohol)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Любитель выпить"\n+500💰'
        elif int(z[0]) >= 100 and int(z[1]) == 3:
            alcohol = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(alcohol=alcohol)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Почётный алкоголик"\n+5000💰'
    elif ach == 'quest':
        z = achm.quest.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            quest = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(quest=quest)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"На побегушках"\n+50💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            quest = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(quest=quest)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Рыцарь здоровой задницы охранника"\n+200💰'
    elif ach == 'stavochnik':
        z = achm.stavochnik.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            stavochnik = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(stavochnik=stavochnik)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"Новый игрок"\n+50💰'
        elif int(z[0]) >= 10 and int(z[1]) == 1:
            stavochnik = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(stavochnik=stavochnik)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Игроман"\n+100💰'
        elif int(z[0]) >= 50 and int(z[1]) == 2:
            stavochnik = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(stavochnik=stavochnik)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Зависимый"\n+200💰'
    elif ach == 'igrovoiAvtomat':
        z = achm.igrovoiAvtomat.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            igrovoiAvtomat = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(igrovoiAvtomat=igrovoiAvtomat)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Удачливый малый"\n+500💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            igrovoiAvtomat = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(igrovoiAvtomat=igrovoiAvtomat)
            await db.Users.filter(id=player.id).update(money=F('money') + 2000)
            text += '"Нереальный везунчик"\n+2000💰'
        elif int(z[0]) >= 20 and int(z[1]) == 2:
            igrovoiAvtomat = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(igrovoiAvtomat=igrovoiAvtomat)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Миллионер"\n+5000💰'
    elif ach == 'lombarder':
        z = achm.lombarder.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            lombarder = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(lombarder=lombarder)
            await db.Users.filter(id=player.id).update(money=F('money') + 50)
            text += '"Ученик продаж"\n+50💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            lombarder = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(lombarder=lombarder)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Продавец со стажем"\n+200💰'
        elif int(z[0]) >= 20 and int(z[1]) == 2:
            lombarder = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(lombarder=lombarder)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Мастер продаж"\n+500💰'
        elif int(z[0]) >= 50 and int(z[1]) == 3:
            lombarder = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(lombarder=lombarder)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Легенда ломбарда"\n+1000💰'
    elif ach == 'ubica':
        z = achm.ubica.split("|")
        if int(z[0]) >= 500 and int(z[1]) == 0:
            ubica = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Убийца нечисти"\n+500💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 1:
            ubica = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Уничтожитель нечисти"\n+1000💰'
        elif int(z[0]) >= 5000 and int(z[1]) == 2:
            ubica = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
            await db.Users.filter(id=player.id).update(money=F('money') + 2000)
            text += '"Потрошитель нечисти"\n+2000💰'
        elif int(z[0]) >= 10000 and int(z[1]) == 3:
            ubica = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Главный страх нечисти"\n+10000💰'
        elif int(z[0]) >= 20000 and int(z[1]) == 4:
            ubica = "{}|5".format(z[0])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
            await db.Users.filter(id=player.id).update(money=F('money') + 20000)
            text += '"Решатель проблем с нечистью"\n+20000💰'
    elif ach == 'prohozhdenie':
        z = achm.prohozhdenie.split("|")
        if int(z[0]) >= 500 and int(z[1]) == 0:
            prohozhdenie = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(prohozhdenie=prohozhdenie)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Лесник"\n+100💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 1:
            prohozhdenie = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id.id).update(prohozhdenie=prohozhdenie)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Искатель приключений"\n+200💰'
    elif ach == 'pvpsher':
        z = achm.pvpsher.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            pvpsher = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(pvpsher=pvpsher)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Новичкам везёт"\n+100💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            pvpsher = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(pvpsher=pvpsher)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Подающий надежды"\n+500💰'
        elif int(z[0]) >= 20 and int(z[1]) == 2:
            pvpsher = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(pvpsher=pvpsher)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Стоящая внимания угроза"\n+1000💰'
        elif int(z[0]) >= 50 and int(z[1]) == 3:
            pvpsher = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(pvpsher=pvpsher)
            await db.Users.filter(id=player.id).update(money=F('money') + 2500)
            text += '"Вышибала"\n+2500💰' 
    elif ach == 'prodavan':
        z = achm.prodavan.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            prodavan = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(prodavan=prodavan)
            await db.Users.filter(id=player.id).update(money=F('money') + 200)
            text += '"Начинающий продавец"\n+100💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            prodavan = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(prodavan=prodavan)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Опытный продавец"\n+500💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            prodavan = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(prodavan=prodavan)
            await db.Users.filter(id=player.id).update(money=F('money') + 2500)
            text += '"Любимчик Раскуловой"\n+2500💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            prodavan = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(prodavan=prodavan)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Тот-у-кого-можно-купить-всё"\n+10000💰'
    elif ach == 'expds':
        z = achm.expds.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            expds = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(expds=expds)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Начинающий экспедитор"\n+100💰'
        elif int(z[0]) >= 5 and int(z[1]) == 1:
            expds = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(expds=expds)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Экспедитор со стажем"\n+500💰'
        elif int(z[0]) >= 50 and int(z[1]) == 2:
            expds = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(expds=expds)
            await db.Users.filter(id=player.id).update(money=F('money') + 2500)
            text += '"Фанат экспедиций"\n+2500💰'
        elif int(z[0]) >= 200 and int(z[1]) == 3:
            expds = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(expds=expds)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Экспедиции это моя жизнь"\n+10000💰'
    elif ach == 'cases':
        z = achm.cases.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            cases = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(cases=cases)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Разбиратель щепок"\n+100💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            cases = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(cases=cases)
            await db.Users.filter(id=player.id).update(money=F('money') + 500)
            text += '"Костевой магнат"\n+500💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            cases = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(cases=cases)
            await db.Users.filter(id=player.id).update(money=F('money') + 2500)
            text += '"Охотник за сундуками"\n+2500💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            cases = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(cases=cases)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Все сундуки - мои"\n+10000💰'
    elif ach == 'craft':
        z = achm.craft.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            craft = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(craft=craft)
            await db.Users.filter(id=player.id).update(shmekli=F('shmekli') + 50)
            text += '"Да здравствует стол волшебства!"\n+50🧿'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            craft = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(craft=craft)
            await db.Users.filter(id=player.id).update(shmekli=F('shmekli') + 100)
            text += '"Улучшатель 3000"\n+100🧿'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            craft = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(craft=craft)
            await db.Users.filter(id=player.id).update(shmekli=F('shmekli') + 1500)
            text += '"Сычер"\n+1500🧿'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            craft = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(craft=craft)
            await db.Users.filter(id=player.id).update(shmekli=F('shmekli') + 5000)
            text += '"ПАЛКА-КОПАЛКА"\n+5000🧿'
    elif ach == 'gacha':
        z = achm.gacha.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            gacha = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(gacha=gacha)
            await db.Users.filter(id=player.id).update(money=F('money') + 100)
            text += '"Молитвы? Что?"\n+100💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            gacha = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(gacha=gacha)
            await db.Users.filter(id=player.id).update(money=F('money') + 2000)
            text += '"Призывалец"\n+2000💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            gacha = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(gacha=gacha)
            await db.Users.filter(id=player.id).update(money=F('money') + 7500)
            text += '"ВСЕ АРТЕФАКТЫ МОИ"\n+7500💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            gacha = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(gacha=gacha)
            await db.Users.filter(id=player.id).update(money=F('money') + 25000)
            text += '"Повелитель призывов"\n+25000💰'
    elif ach == 'radar':
        z = achm.radar.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            radar = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(radar=radar)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Добро пожаловать в Радар!"\n+1000💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            radar = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(radar=radar)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Сталкерские замашки"\n+5000💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            radar = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(radar=radar)
            await db.Users.filter(id=player.id).update(money=F('money') + 15000)
            text += '"Прописка в Радаре"\n+15000💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            radar = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(radar=radar)
            await db.Users.filter(id=player.id).update(money=F('money') + 50000)
            text += '"Герой Радара"\n+50000💰'
    elif ach == 'kitchen':
        z = achm.kitchen.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            kitchen = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(kitchen=kitchen)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Добро пожаловать в КУХНЮ!"\n+1000💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            kitchen = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(kitchen=kitchen)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Борщ готовить буш"\n+5000💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            kitchen = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(kitchen=kitchen)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Силой пота и кухни..."\n+10000💰'
        elif int(z[0]) >= 2000 and int(z[1]) == 3:
            kitchen = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(kitchen=kitchen)
            await db.Users.filter(id=player.id).update(money=F('money') + 30000)
            text += '"Шеф-повар"\n+30000💰'
    elif ach == 'fishing':
        z = achm.fishing.split("|")
        if int(z[0]) >= 1 and int(z[1]) == 0:
            fishing = "{}|1".format(z[0])
            await db.Ach.filter(id=achm.id).update(fishing=fishing)
            await db.Users.filter(id=player.id).update(money=F('money') + 1000)
            text += '"Рыболов? Ламер"\n+1000💰'
        elif int(z[0]) >= 50 and int(z[1]) == 1:
            fishing = "{}|2".format(z[0])
            await db.Ach.filter(id=achm.id).update(fishing=fishing)
            await db.Users.filter(id=player.id).update(money=F('money') + 5000)
            text += '"Junior-рыболов"\n+5000💰'
        elif int(z[0]) >= 500 and int(z[1]) == 2:
            fishing = "{}|3".format(z[0])
            await db.Ach.filter(id=achm.id).update(fishing=fishing)
            await db.Users.filter(id=player.id).update(money=F('money') + 10000)
            text += '"Middle-рыболов"\n+10000💰'
        elif int(z[0]) >= 5000 and int(z[1]) == 3:
            fishing = "{}|4".format(z[0])
            await db.Ach.filter(id=achm.id).update(fishing=fishing)
            await db.Users.filter(id=player.id).update(money=F('money') + 20000)
            text += '"Сеньйор рыбак"\n+20000💰'
    await player.refresh_from_db()
    if len(text) >= 30:
        await bot.send_message(player.user_id, text)
    return player


async def achprog(user, ach):
    achm = await db.Ach.exists(user_id=user.user_id)
    if achm:
        achm = await db.Ach.get(user_id=user.user_id).first()
        if ach == 'trader':
            z = achm.trader.split("|")
            newProgress = int(z[0]) + 1
            trader = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(trader=trader)
        elif ach == 'kachalka':
            z = achm.kachalka.split("|")
            newProgress = user.atk + user.hp
            kachalka = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(kachalka=kachalka)
        elif ach == 'shopbuy':
            z = achm.shopbuy.split("|")
            newProgress = int(z[0]) + 1
            shopbuy = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(shopbuy=shopbuy)
        elif ach == 'skupshik':
            z = achm.skupshik.split("|")
            newProgress = int(z[0]) + 1
            skupshik = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(skupshik=skupshik)

        elif ach == 'alcohol':
            z = achm.alcohol.split("|")
            newProgress = int(z[0]) + 1
            alcohol = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(alcohol=alcohol)
        elif ach == 'quest':
            z = achm.quest.split("|")
            newProgress = int(z[0]) + 1
            quest = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(quest=quest)
        elif ach == 'stavochnik':
            z = achm.stavochnik.split("|")
            newProgress = int(z[0]) + 1
            stavochnik = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(stavochnik=stavochnik)
        elif ach == 'igrovoiAvtomat':
            z = achm.igrovoiAvtomat.split("|")
            newProgress = int(z[0]) + 1
            igrovoiAvtomat = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(igrovoiAvtomat=igrovoiAvtomat)
        elif ach == 'lombarder':
            z = achm.lombarder.split("|")
            newProgress = int(z[0]) + 1
            lombarder = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(lombarder=lombarder)
        elif ach == 'ubica':
            z = achm.ubica.split("|")
            newProgress = int(z[0]) + 1
            ubica = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(ubica=ubica)
        elif ach == 'prohozhdenie':
            z = achm.prohozhdenie.split("|")
            newProgress = int(z[0]) + 1
            prohozhdenie = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(prohozhdenie=prohozhdenie)
        elif ach == 'pvpsher':
            z = achm.pvpsher.split("|")
            newProgress = int(z[0]) + 1
            pvpsher = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(pvpsher=pvpsher)
        elif ach == 'prodavan':
            z = achm.prodavan.split("|")
            newProgress = int(z[0]) + 1
            prodavan = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(prodavan=prodavan)
        elif ach == 'expds':
            z = achm.expds.split("|")
            newProgress = int(z[0]) + 1
            prodavan = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(expds=prodavan)
        elif ach == 'cases':
            z = achm.cases.split("|")
            newProgress = int(z[0]) + 1
            cases = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(cases=cases)
        elif ach == 'craft':
            z = achm.craft.split("|")
            newProgress = int(z[0]) + 1
            craft = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(craft=craft)
        elif ach == 'gacha':
            z = achm.gacha.split("|")
            newProgress = int(z[0]) + 1
            gacha = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(gacha=gacha)
        elif ach == 'radar':
            z = achm.radar.split("|")
            newProgress = int(z[0]) + 1
            radar = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(radar=radar)
        elif ach == 'kitchen':
            z = achm.kitchen.split("|")
            newProgress = int(z[0]) + 1
            kitchen = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(kitchen=kitchen)
        elif ach == 'fishing':
            z = achm.fishing.split("|")
            newProgress = int(z[0]) + 1
            fishing = "{}|{}".format(newProgress, z[1])
            await db.Ach.filter(id=achm.id).update(fishing=fishing)
    else:
        await db.Ach.create(user_id=user.user_id)
    await addAch(user, ach)



async def achList(m, user):
    if user:
        user = await db.Users.get(user_id=m.from_user.id).first()
        text = "Открытые достижения:\n"
        achs = await db.Ach.exists(user_id=m.from_user.id)
        if achs:
            achs = await db.Ach.get(user_id=m.from_user.id).first()
            novichek = achs.novichek.split("|")
            if novichek[1] == '1': text += "\n🍀Уже не новичок"
            elif novichek[1] == '2': text += "\n🍀Хэвен, милый Хэвен..."
            elif novichek[1] == '3': text += "\n🥉Kawai! (^ ω ^)"
            elif novichek[1] == '4': text += "\n🥈Опытный сталкер"
            elif novichek[1] == '5': text += "\n🥇Из огня да в полымя..."
            trader = achs.trader.split("|")
            if trader[1] == '1': text += "\n🥉Новый трейдер"
            elif trader[1] == '2': text += "\n🥈Трейдер со стажем"
            elif trader[1] == '3': text += "\n🥇Мастер трейдинга"
            kachalka = achs.kachalka.split("|")
            if kachalka[1] == '1': text += "\n🍀Качок"
            elif kachalka[1] == '2': text += "\n🍀Завсегдатай качалки"
            elif kachalka[1] == '3': text += "\n🥉Задрот качалки"
            elif kachalka[1] == '4': text += "\n🥈kachalOчка это моя жизнь"
            elif kachalka[1] == '5': text += "\n🥇Слыш, я тут качок"
            shopbuy = achs.shopbuy.split("|")
            if shopbuy[1] == '1': text += "\n🍀Знакомство с Ашотом"
            elif shopbuy[1] == '2': text += "\n🥉Любитель 24/7 Аshopа"
            elif shopbuy[1] == '3': text += "\n🥈Постоянный покупатель"
            elif shopbuy[1] == '4': text += "\n🥇Скупщик"
            skupshik = achs.skupshik.split("|")
            if skupshik[1] == '1': text += "\n🥉Встретились два скупщика"
            elif skupshik[1] == '2': text += "\n🥈Самое ценное - себе"
            elif skupshik[1] == '3': text += "\n🥇Хламовый магнат"
            alcohol = achs.alcohol.split("|")
            if alcohol[1] == '1': text += "\n🍀А у вас точно качественный алкоголь?"
            elif alcohol[1] == '2': text += "\n🥉Хорошая компания"
            elif alcohol[1] == '3': text += "\n🥈Любитель выпить"
            elif alcohol[1] == '4': text += "\n🥇Почётный алкоголик"
            quest = achs.quest.split("|")
            if quest[1] == '1': text += "\n🥈На побегушках"
            elif quest[1] == '2': text += "\n🥇Рыцарь здоровой задницы охранника"
            stavochnik = achs.stavochnik.split("|")
            if stavochnik[1] == '1': text += "\n🥉Новый игрок"
            elif stavochnik[1] == '2': text += "\n🥈Игроман"
            elif stavochnik[1] == '3': text += "\n🥇Зависимый"
            igrovoiAvtomat = achs.igrovoiAvtomat.split("|")
            if igrovoiAvtomat[1] == '1': text += "\n🥉Удачливый малый"
            elif igrovoiAvtomat[1] == '2': text += "\n🥈Нереальный везунчик"
            elif igrovoiAvtomat[1] == '3': text += "\n🥇Миллионер"
            lombarder = achs.lombarder.split("|")
            if lombarder[1] == '1': text += "\n🍀Ученик продаж"
            elif lombarder[1] == '2': text += "\n🥉Продавец со стажем"
            elif lombarder[1] == '3': text += "\n🥈Мастер продаж"
            elif lombarder[1] == '4': text += "\n🥇Легенда ломбарда"
            ubica = achs.ubica.split("|")
            if ubica[1] == '1': text += "\n🟢Убийца нечисти"
            elif ubica[1] == '2': text += "\n🍀Уничтожитель нечисти"
            elif ubica[1] == '3': text += "\n🥉Потрошитель нечисти"
            elif ubica[1] == '4': text += "\n🥈Главный страх нечисти"
            elif ubica[1] == '5': text += "\n🥇Решатель проблем с нечистью"
            prohozhdenie = achs.prohozhdenie.split("|")
            if prohozhdenie[1] == '1': text += "\n🥈Лесник"
            elif prohozhdenie[1] == '2': text += "\n🥇Искатель приключений"
            pvpsher = achs.pvpsher.split("|")
            if pvpsher[1] == '1': text += "\n🍀Новичкам везёт"
            elif pvpsher[1] == '2': text += "\n🥉Подающий надежды"
            elif pvpsher[1] == '3': text += "\n🥈Стоящая внимания угроза"
            elif pvpsher[1] == '4': text += "\n🥇Вышибала"
            donater = achs.donater.split("|")
            if donater[1] == '1': text += "\n🍀Донатер"
            elif donater[1] == '2': text += "\n🍀Между первым и вторым..."
            elif donater[1] == '3': text += "\n🥉ToH supporter"
            elif donater[1] == '4': text += "\n🥈Рыцарь Kakushigoto"
            elif donater[1] == '5': text += "\n🥇Кормилец Kakushigoto"
            prodavan = achs.prodavan.split("|")
            if prodavan[1] == '1': text += "\n🍀Начинающий продавец"
            elif prodavan[1] == '2': text += "\n🥉Опытный продавец"
            elif prodavan[1] == '3': text += "\n🥈Любимчик Раскуловой"
            elif prodavan[1] == '4': text += "\n🥇Тот-у-кого-можно-купить-всё"
            halloween2020 = achs.halloween2020.split("|")
            if halloween2020[1] == '1': text += "\n🎃Хеллоуинская тыква 2020"
            kawaikluch = achs.kawaikluch.split("|")
            if kawaikluch[1] == '1': text += "\n🥈Общий вклад"
            elif kawaikluch[1] == '2': text += "\n🥇Дайте снег!"
            expds = achs.expds.split("|")
            if expds[1] == '1': text += "\n🍀Начинающий экспедитор"
            elif expds[1] == '2': text += "\n🥉Экспедитор со стажем"
            elif expds[1] == '3': text += "\n🥈Фанат экспедиций"
            elif expds[1] == '4': text += "\n🥇Экспедиции это моя жизнь"
            cases = achs.cases.split("|")
            if cases[1] == '1': text += "\n🍀Разбиратель щепок"
            elif cases[1] == '2': text += "\n🥉Костевой магнат"
            elif cases[1] == '3': text += "\n🥈Охотник за сундуками"
            elif cases[1] == '4': text += "\n🥇Все сундуки - мои"
            chessJune = achs.chessJune.split("|")
            if chessJune[1] == '1': text += "\n🍀Участник ToH Chess Season 1"
            elif chessJune[1] == '2': text += "\n🥉Полуфиналист ToH Chess Season 1"
            elif chessJune[1] == '3': text += "\n🥈Призёр ToH Chess Season 1"
            elif chessJune[1] == '4': text += "\n🥇Победитель ToH Chess Season 1"
            craft = achs.craft.split("|")
            if craft[1] == '1': text += "\n🍀Да здравствует стол волшебства!"
            elif craft[1] == '2': text += "\n🥉Улучшатель 3000"
            elif craft[1] == '3': text += "\n🥈Сычер"
            elif craft[1] == '4': text += "\n🥇ПАЛКА-КОПАЛКА"
            gacha = achs.gacha.split("|")
            if gacha[1] == '1': text += "\n🍀Молитвы? Что?"
            elif gacha[1] == '2': text += "\n🥉Призывалец"
            elif gacha[1] == '3': text += "\n🥈ВСЕ АРТЕФАКТЫ МОИ"
            elif gacha[1] == '4': text += "\n🥇Повелитель призывов"
            radar = achs.radar.split("|")
            if radar[1] == '1': text += "\n🍀Добро пожаловать в Радар!"
            elif radar[1] == '2': text += "\n🥉Сталкерские замашки"
            elif radar[1] == '3': text += "\n🥈Прописка в Радаре"
            elif radar[1] == '4': text += "\n🥇Герой Радара"
            kitchen = achs.kitchen.split("|")
            if kitchen[1] == '1': text += "\n🍀Добро пожаловать в КУХНЮ!"
            elif kitchen[1] == '2': text += "\n🥉Борщ готовить буш"
            elif kitchen[1] == '3': text += "\n🥈Силой Пота и кухни..."
            elif kitchen[1] == '4': text += "\n🥇Шеф-повар"
            fishing = achs.fishing.split("|")
            if fishing[1] == '1': text += "\n🍀Рыболов? Ламер"
            elif fishing[1] == '2': text += "\n🥉Junior-рыболов"
            elif fishing[1] == '3': text += "\n🥈Middle-рыболов"
            elif fishing[1] == '4': text += "\n🥇Сеньйор рыбак"
            await bot.send_message(m.chat.id, text)
        else:
            add = await db.Ach(user_id=m.from_user.id)
            await add.save()
            await bot.send_message(m.chat.id, "Попробуйте еще раз.")
