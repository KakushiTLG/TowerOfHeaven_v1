import sys
__ver__ = "2.0"
gameActive = 1
invsType = 1
_buzyUsers = {}
__buzyUsers = {} # antiflood
captchaUsers = {}

@dp.errors_handler(exception=Exception)
async def error_cant_parse(update: types.Update, error):
    if error.__class__.__name__ == 'RetryAfter':
        if "callback_query" in update:
            try:
                await bot.answer_callback_query(callback_query_id=update.callback_query.id, show_alert=True, text="Бум-бах-трах!\n{}".format(error))
                return
            except:
                return
    elif error.__class__.__name__ == 'BadRequest':
        if "callback_query" in update:
            try:
                await bot.answer_callback_query(callback_query_id=update.callback_query.id, show_alert=True, text="Сообщение устарело")
            except:
                pass
        return
    elif error.__class__.__name__ == 'MessageToDeleteNotFound' or error.__class__.__name__ == 'MessageNotModified' or error.__class__.__name__ == 'MessageToEditNotFound' or error.__class__.__name__ == 'InvalidQueryID':
        pass
    else:
        tb1 = sys.exc_info()[1]
        tb = sys.exc_info()[2]
        tbinfo = str(traceback.format_exc())
        await bot.send_message(702528084, f'traceback [{tbinfo}]\n\n\nerror [{error}]\n\nerror class [{error.__class__}]\n\n[{error.__class__.__name__}]\n\nupdate [{update}]')

        return True

async def checker(m):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if user:
        await db.Users.filter(user_id=m.from_user.id).update(sleepPlayer=int(time.time() + 86400))
        success = True
    else:
        await start(m)
        success = False
        user = None
    return success, user


antiflood = {}
boyaraUsers = {}
testers = ['702528084', '347910148']
#testers = ['702528084', '330432380', '339227462', '352318352', '699798209', '428376783', '754334151']
async def on_db():
    db = pymysql.connect(host='localhost',
                         user='kakushigoto',
                         password='passwd',                             
                         db='dbname',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    return db
firstLauch = 1
bannedUsers = {}
@dp.message_handler(content_types=["text"])
async def texthand(m):
    global firstLauch
    if m.from_user.id in bannedUsers and bannedUsers[m.from_user.id] == 1: return
    if firstLauch == 1 and gameActive == 1:
        await bot.send_message(devChat, "Reboot")
        firstLauch = 0
        issues = await db.Problems.filter(status=1)
        if issues:
            text = "Были исправлены следующие проблемы:\n"
            for z in issues:
                text += "\n🔘 {};".format(z.comment)
            text += "\n\nОстальные известные проблемы находятся в процессе решения, отследить которые можно на странице https://toh.fdu.su/issues\n\n\nПриятной игры!"
            msg = await bot.send_message(-1001229520706, text)
        issues = await db.Problems.filter(status=1).delete()
        users = await db.Users.filter(ban=1).only('user_id')
        for i in users: bannedUsers[i.user_id] = 0
    try:
        await dp.throttle(str(m.from_user.id), rate=1)
    except exceptions.Throttled:
        return


    try:
        if boyaraUsers and boyaraUsers[m.from_user.id] and boyaraUsers[m.from_user.id] == 1 and m.chat.id == m.from_user.id:
            await bot.send_message(m.from_user.id, "Вы не в состоянии...")
            return
    except:
        pass

    if gameActive == 0 and str(m.from_user.id) not in testers and m.chat.id == m.from_user.id:
        await bot.send_message(m.chat.id, "🚧Технические работы. В скором времени всё, вероятно, заработает...")
        return

    if m.chat.id == m.from_user.id:
        success, user = await checker(m)
        if success == True:
            
            if not user:
                user = await db.Users.get(user_id=m.from_user.id)
            if user.godEye == 1:
                await logBot.send_message(godEyeChat, "{} ({})\nCurrent time {}\nText: {}".format(user.username, user.id, m.date, m.text))
                randCaptcha = 15
                rand = random.randint(0, 1000)
                if randCaptcha <= rand:
                    if user.id in captchaUsers and captchaUsers[user.id] >= int(time.time()):
                        user.ban = 5
                        await db.Users.filter(id=user.id).update(ban=5)
                        captchaUsers[user.id] = int(time.time()) + 43200
                    elif user.id not in captchaUsers:
                        user.ban = 5
                        await db.Users.filter(id=user.id).update(ban=5)
                        captchaUsers[user.id] = int(time.time()) + 43200
            else:
                hour = datetime.datetime.fromtimestamp(time.time()).strftime("%H")
                if hour <=5:
                    randCaptcha = 10
                elif hour <=20:
                    randCaptcha = 3
                else:
                    randCaptcha = 10
                rand = random.randint(0, 1000)
                if randCaptcha <= rand:
                    if user.id in captchaUsers and captchaUsers[user.id] >= int(time.time()):
                        user.ban = 5
                        await db.Users.filter(id=user.id).update(ban=5)
                        captchaUsers[user.id] = int(time.time()) + 43200
                    elif user.id not in captchaUsers:
                        user.ban = 5
                        await db.Users.filter(id=user.id).update(ban=5)
                        captchaUsers[user.id] = int(time.time()) + 43200
            if user.ban == 5:
                a = requests.post("https://captcha.otorh.in/api/create", data={"api_key": "O3j928ivRnA9e7G16Zy9", "code": user.id}).json()
                url = "https://captcha.otorh.in/?code=" + a['code']
                await bot.send_message(m.chat.id, "Пройдите капчу по ссылке {}".format(url))
                return
            elif user.ban != 1: pass
            else:
                bannedUsers[user.user_id] = 1
                await profile(m, user)
                return
            if m.text.lower() in ['профиль']:
                await profile(m, user)
            elif m.text.lower() in ['инвентарь']:
                await inventory(m, user)
            elif m.text.lower() in ['навигация']:
                await navigation(m, user)
            elif m.text.lower() in ['рефералы']:
                await refs(m)
            elif m.text.lower() in ['снаряжение']:
                await inventory(m, user)
            elif m.text.startswith("/arena_"):
                await arena_(m)
            elif m.text.lower() in ['/blacklist']:
                await itemsBlackList(m, user)
            elif m.text.startswith('/nf_'):
                await nf_(m, user)
            elif m.text.lower() in ['/notif_settings']:
                await notif_settings(m, user)
            elif m.text.lower() in ['/api_settings']:
                await usrSetApi(m, user)
            elif m.text.startswith('/s_api_'):
                await s_api(m, user)
            elif m.text.startswith('/raskulova_sell'):
                await raskulova_sell(m)
            elif m.text.startswith('/raskulova_buy'):
                await raskulova_buy(m)
            elif m.text.startswith('/raskulova_select_'):
                await raskulova_select(m)
            elif m.text.startswith('/bot'):
                await botProfile(m, user)
            elif m.text.startswith('/profile'):
                await profileFull(m, user)
            elif m.text.startswith('/look_around'):
                await look_around(m, user)
            elif m.text.startswith("/interact_"):
                await interact_(m, user)
            elif m.text.startswith("/bp"):
                await bp(m, user)
            elif m.text.startswith('/match_'):
                await match_(m, user)
            elif m.text.startswith('/bet_'):
                await bet(m, user)
            elif m.text.lower() == '/lobby':
                await lobby(m, user)
            elif m.text.startswith('/lobby_invite'):
                await lobbyInvite(m, user)
            elif m.text.startswith('/lobby_exit'):
                await lobbyExit(m, user)
            elif m.text.startswith('/about_craft'):
                await about_craft(m)
            elif m.text.startswith('/about_gacha'):
                await about_gacha(m)
            elif m.text.startswith('/parlament'):
                await parlament(m, user)
            elif m.text.startswith('/changeCom_'):
                await changeCom_(m, user)
            elif m.text.startswith('/badges'):
                await badges(m, user)
            elif m.text.startswith('/set_badge_'):
                await set_badge(m, user)
            elif m.text.startswith('/stats'):
                await stats(m)
            elif m.text.startswith('/token'):
                await getToken(m, user)
            elif m.text.startswith('/skills'):
                await skills(m, user)
            elif m.text.startswith('/myrefs'):
                await refs(m, user)
            elif m.text.startswith('/donate'):
                await donatestar(m, user)
            elif m.text.startswith('/mypartn'):
                await mypartn(m, user)
            elif m.text.startswith('/settings'):
                await settings(m, user)
            elif m.text.startswith('/quests'):
                await quests(m, user)
            elif m.text.startswith('/startBonus'):
                await startBonus(m, user)
            elif m.text.startswith('/weapon'):
                await weapon(m, user)
            elif m.text.startswith('/mentorship'):
                await mentorship(m, user)
            elif m.text.startswith('/home') or m.text.startswith("myHouse"):
                await myHouse(m, user)
            elif m.text in ['/ach', '/achievement', '/achievements', '/achs']:
                await achList(m, user)
            elif m.text.lower() == '/newinv':
                await newInv(m, user)
            elif m.text.startswith('/fastAccessDelete_'):
                await fastAccessDelete_(m, user)
            elif m.text.startswith('/fastAccessAdd '):
                await fastAccessAdd(m, user)
            elif m.text.startswith('/inv_fa'):
                await inv_fa(m, user)
            elif m.text.startswith('/pizza_shop'):
                await pizza_shop(m, user)
            elif m.text.startswith('/raskulova_kriBuy_'):
                await raskulova_kriBuy_(m, user)
            

            elif m.text.startswith('/ref_ivent'):
                await ref_ivent(m, user)

        await logger.write(m, user)


async def waiterTest(call):
    if __buzyUsers and call.from_user.id in __buzyUsers:
        if __buzyUsers[call.from_user.id] == 'stopped':
            passing = False
            return passing
        if __buzyUsers and call.from_user.id in __buzyUsers and __buzyUsers[call.from_user.id] > 0:
            print("Stopped {}".format(call.from_user.username))
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ожидаем окончания предыдущего действия...")                
            count = 0
            while __buzyUsers[call.from_user.id] != 0:
                count += 1
                if count >= 20:
                    __buzyUsers[call.from_user.id] = 0
                await asyncio.sleep(0.2)
            print("Passed {}".format(call.from_user.username))
            passing = True
        elif __buzyUsers[call.from_user.id] > 10:
            print("Full stopped {}".format(call.from_user.username))
            passing = False
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Действие отменено - флуд-контроль. Попробуйте через минуту.")                
            try:
                await dp.throttle(str(call.from_user.id), rate=60)
            except exceptions.Throttled:
                return
        else:
            passing = True
    else:
        print("Already passed {}".format(call.from_user.username))
        passing = True
        __buzyUsers[int(call.from_user.id)] = 0
    return passing

@dp.callback_query_handler(lambda call: call.from_user.id not in bannedUsers)
async def callhand(call):
    try:
        await dp.throttle(str(call.from_user.id), rate=1)
        await call.answer()
    except exceptions.Throttled: return
    if gameActive == 0 and str(call.from_user.id) not in testers and call.message.chat.id == call.from_user.id: return
    passing = await waiterTest(call)
    if not passing or passing != True: return
    user = await db.Users.get(user_id=call.from_user.id).first()
    if user.godEye == 1:
        currentTime = datetime.datetime.fromtimestamp(time.time())
        await logBot.send_message(godEyeChat, "{} ({}): CALLBACK_INFO - {}\nNow time: {}\nMsg time: {} from:\n\n{}".format(user.username, user.id, call.data, currentTime, call.message.date, call.message.text))
        randCaptcha = 15
        rand = random.randint(0, 1000)
        if randCaptcha <= rand:
            if user.id in captchaUsers and captchaUsers[user.id] >= int(time.time()):
                user.ban = 5
                await db.Users.filter(id=user.id).update(ban=5)
                captchaUsers[user.id] = int(time.time()) + 43200
            elif user.id not in captchaUsers:
                user.ban = 5
                await db.Users.filter(id=user.id).update(ban=5)
                captchaUsers[user.id] = int(time.time()) + 43200
    else:
        hour = datetime.datetime.fromtimestamp(time.time()).strftime("%H")
        if hour <=5:
            randCaptcha = 10
        elif hour <=20:
            randCaptcha = 3
        else:
            randCaptcha = 10
        rand = random.randint(0, 1000)
        if randCaptcha <= rand:
            if user.id in captchaUsers and captchaUsers[user.id] >= int(time.time()):
                user.ban = 5
                await db.Users.filter(id=user.id).update(ban=5)
                captchaUsers[user.id] = int(time.time()) + 43200
            elif user.id not in captchaUsers:
                user.ban = 5
                await db.Users.filter(id=user.id).update(ban=5)
                captchaUsers[user.id] = int(time.time()) + 43200
    if user.ban == 5:
        a = requests.post("https://captcha.otorh.in/api/create", data={"api_key": "O3j928ivRnA9e7G16Zy9", "code": user.id}).json()
        url = "https://captcha.otorh.in/?code=" + a['code']
        await bot.send_message(call.message.chat.id, "Пройдите капчу по ссылке {}".format(url))
        return
    elif user.ban in [0, 2]:
        await db.Users.filter(id=user.id).update(sleepPlayer=int(time.time() + 86400))
        d = call.data
        __buzyUsers[call.from_user.id] += 1
        if d.startswith('ownpanel_'): await ownpanelcheck(call)
        elif d.startswith('admin_'): await ownpanelcheck1(call)
        elif d.startswith('report_'): await reportedFix(call)
        elif d.startswith('getuser_'): await getuser(call)
        elif d.startswith('battle_'): await battlestart(call, user)
        elif d.startswith('extraCase_'): await extraCase(call, user)
        elif d.startswith('donateKartochki_'): await donateKartochki(call, user)
        elif d.startswith('fraka_'): await fraka(call, user)
        elif d.startswith('vsnosFrak_'): await frac_deposit(call, user)
        elif d.startswith('zamSet_'): await zamSet_(call, user)
        elif d.startswith('groupBonusKach_'): await groupBonusKach_(call, user)
        elif d.startswith('nav_location_'): await nav_location(call, user)
        elif d.startswith('nav_city_'): await nav_city(call, user)
        elif d.startswith('nav_base_'): await nav_base(call, user)
        elif d.startswith('kach_'): await kach(call, user)
        elif d.startswith('hotel_'): await hotel(call, user)
        elif d.startswith('bighotel_'): await bighotel(call, user)
        elif d.startswith('trade_'): await trade(call, user)
        elif d.startswith('tradewith_'): await tradewith(call, user)
        elif d.startswith('trades_'): await trading(call, user)
        elif d.startswith('tradecon_'): await tradecon(call, user)
        elif d.startswith('tradestar_'): await tradestar(call, user)
        elif d.startswith('shrineUse'): await shrineUse(call, user)
        elif d.startswith('nav_bigcity_'): await nav_bigcity(call, user)
        elif d.startswith('poslanie_'): await poslanie(call, user)
        elif d.startswith('bar_'): await bar(call, user)
        elif d.startswith('coin_start'): await coinStart(call, user)
        elif d.startswith('dunjgo_'): await dunjgo(call, user)
        elif d.startswith('navgo'): await navgo(call, user)
        elif d.startswith('navback'): await navback(call, user)
        elif d.startswith('navstop'): await navstop(call, user)
        elif d.startswith('ko4at_'): await ko4at_(call, user)
        elif d.startswith('nav_oceanus_'): await nav_oceanus(call, user)
        elif d.startswith('nav_wintercity_'): await nav_wintercity(call, user)
        elif d.startswith('nav_radar_'): await nav_radar(call, user)
        elif d.startswith('winterkach_'): await winterkach_(call, user)
        elif d.startswith('invUse_'): await invUse(call, user)
        elif d.startswith('invDrop_'): await invDrop(call)
        elif d.startswith('bomb_'): await bomb_(call, user)
        elif d.startswith('invUsing_'): await invUsing(call, user)
        elif d.startswith('inveClose'): await invClose(call, user)
        elif d.startswith('inventory_'): await inventory_(call, user)
        elif d.startswith('invRefresh'): await invRefresh(call, user)
        elif d.startswith('inv'): await inv(call, user)
        elif d.startswith('armorpers'): await armorpers(call, user)
        elif d.startswith('varenie_'): await varenie(call, user)
        elif d.startswith('quest_'): await quests_(call, user)
        elif d.startswith('shop_'): await _shop(call, user)
        elif d.startswith('buy_'): await buy(call, user)
        elif d.startswith('donateshop'): await donateshop(call, user)
        elif d.startswith('donate_start'): await donatestart(call, user)
        elif d.startswith('dshopbuy_'): await dshopbuy(call, user)
        elif d.startswith('buyBooster_'): await buyBooster(call, user)
        elif d.startswith('donateSelectItem_'): await donateSelectItem(call, user)
        elif d.startswith('donateSelectFrak_'): await donateSelectFrak(call, user)
        elif d.startswith('shopsell'): await shopsell(call, user)
        elif d.startswith('backtoshop'): await backtoshop(call, user)
        elif d.startswith('bomjsell'): await bomjsell(call, user)
        elif d.startswith('bomj_sell_'): await bomj_sell(call, user)
        elif d.startswith('wintershop'): await winterShop(call, user)
        elif d.startswith('wintershBuy_'): await wintershopBuy(call, user)
        elif d.startswith('defShop'): await defShop(call, user)
        elif d.startswith('defshBuy_'): await defshBuy(call, user)
        elif d.startswith('oceanshop'): await oceanshop(call, user)
        elif d.startswith('ocshBuy_'): await ocshopbuy(call, user)
        elif d.startswith('raskul_'): await raskulova(call, user)
        elif d.startswith('raskulselecttype_'): await raskulselecttype_(call, user)
        elif d.startswith('lot_'): await lotEdit(call, user)
        elif d.startswith('lotValute_'): await lotValute_(call, user)
        elif d.startswith('lotDone_'): await lotDone(call, user)
        elif d.startswith('gotoKitchen'): await gotoKitchen(call, user)
        elif d.startswith('cooking_'): await cooking(call, user)
        elif d.startswith('expedition_'): await expedition_(call, user)
        elif d.startswith('coinBet_'): await coinBetSelectValute(call, user)
        elif d.startswith('skillsUp'): await skillsUp(call)
        elif d.startswith('upSkill'): await upSkill(call)
        elif d.startswith('attack_'): await attack_(call, user)
        elif d.startswith('catch_robber'): await catch_robber(call)
        elif d.startswith('krazha_'): await krazha_(call, user)
        elif d.startswith('parl_commisions'): await parl_commisions(call, user)
        elif d.startswith('newattack_'): await newattack_(call, user)
        elif d.startswith('counterattack'): await counter_attack(call)
        elif d.startswith('queue_attack'): await queue_attack(call)
        elif d.startswith('bets_'): await bets_(call, user)
        elif d.startswith('activeBets'): await activeBets(call, user)
        elif d.startswith('bet_'): await bet_(call, user)
        elif d.startswith('betDone_'): await betDone_(call, user)
        elif d.startswith('editMatch_'): await editMatch_(call, user)
        elif d.startswith('JiAlley'): await JiAlley(call, user)
        elif d.startswith('kriMarket_'): await krimarket(call, user)
        elif d.startswith('houseBuy'): await houseBuy(call, user)
        elif d.startswith('houseSell'): await houseSell(call, user)
        elif d.startswith('HOUSESELLCONFIRM'): await HOUSESELLCONFIRM(call, user)
        elif d.startswith('iveSklad_'): await invSklad(call, user)
        elif d.startswith('house_'): await house(call, user)
        elif d.startswith('home_'): await home(call, user)
        elif d.startswith('doshopBoxes'): await doshopBoxes(call, user)
        elif d.startswith('doshopItems'): await doshopItems(call, user)
        elif d.startswith('doshopOther'): await doshopOther(call, user)
        elif d.startswith('scenarioFirst'): await scenarioFirst(call, user)
        elif d.startswith('sich'): await sich(call, user)
        elif d.startswith('alchemy'): await alchemy(call, user)
        elif d.startswith('gacha'): await gacha(call, user)
        elif d.startswith('shopGacha'): await shopGacha(call, user)
        elif d.startswith('buyGacha'): await buyGacha(call, user)
        elif d.startswith('coinJackpot'): await coinJackpot(call, user)
        elif d.startswith('radarBuy'): await radarBuy(call, user)
        elif d.startswith('startRadar'): await startRadar(call, user)
        elif d.startswith('craftInv'): await craftInv(call, user)
        elif d.startswith('frakKrazha'): await frakKrazha(call, user)
        elif d.startswith('frakSecurity_'): await frakSecurity_(call, user)
        elif d.startswith('camp_npc_'): await camp_npc(call, user)
        elif d.startswith('sunday'): await sunday(call, user)
        elif d.startswith('weaponUp'): await weaponUp(call, user)
        elif d.startswith('Kitchen'): await Kitchen(call, user)
        elif d.startswith('kitchen_start'): await kitchen_start(call, user)
        elif d.startswith('addKitchen_'): await addKitchen_(call, user)
        elif d.startswith('tpWeaponFarm'): await tpWeaponFarm(call, user)
        elif d.startswith('printer_'): await printer_(call, user)
        elif d.startswith('upgradeArt_'): await upgradeArt_(call, user)
        elif d.startswith('printerCreate_'): await printerCreate_(call, user)
        elif d.startswith('createItem_'): await createItem_(call, user)
        elif d.startswith('createClan'): await createClan(call, user)
        elif d.startswith('clanCreate'): await clanCreate(call, user)
        elif d.startswith('joinClan_'): await joinClan_(call, user)
        elif d.startswith('acceptClanJoin_'): await acceptClanJoin_(call, user)
        elif d.startswith('declineClanJoin_'): await declineClanJoin_(call, user)
        elif d.startswith('nav_metro'): await nav_metro(call, user)
        elif d.startswith('mtshBuy_'): await mtshBuy_(call, user)
        elif d.startswith('fishilka'): await fishilka(call, user)
        elif d.startswith('endFishing'): await endFishing(call, user)
        elif d.startswith('catchFish'): await catchFish(call, user)
        elif d.startswith('leadSet_'): await leadSet_(call, user)
        elif d.startswith('botProfile'): await botProfileCallback(call, user)
        elif d.startswith('botLogs'): await botLogs(call, user)
        elif d.startswith('botCMD'): await botCMD(call, user)
        elif d.startswith('botDestroy'): await botDestroy(call, user)
        elif d.startswith('doshopCurrency'): await doshopCurrency(call, user)
        elif d.startswith('newYearIventBuy'): await newYearIventBuy(call, user)
        elif d.startswith("battleUseEnergy"): await battleUseEnergy(call,user)
        elif d.startswith("battleUseFire"): await battleUseFire(call,user)
        elif d.startswith("joinHNS_"): await joinHNS_(call,user)
        elif d.startswith("partyHS"): await partyHS(call,user)
        elif d.startswith("toshen_"): await toshen_(call,user)
        elif d.startswith("dvp"): await dvp(call,user)
        elif d.startswith("houseUpgrade_"): await houseUpgrade_(call,user)
        elif d.startswith("koltGrav_"): await koltGrav_(call,user)
        elif d.startswith("pizzashop"): await pizzashop(call,user)
        elif d.startswith("otrh_pasd"): await otrh_pasd(call,user)
        await asyncio.sleep(0.2)
        __buzyUsers[call.from_user.id] -= 1
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Действие отменено. Ошибка доступа.")                
    try:
        await call.answer()
    except:
        pass
    await logger.write(call, user)

@dp.message_handler(content_types=['new_chat_members'])
async def checkfrak(m):
    user = await db.Users.exists(user_id=m.from_user.id)
    if not user:
        await bot.kick_chat_member(m.chat.id, m.from_user.id)
        await bot.delete_message(m.chat.id, m.message_id)
    if user:
        user = await db.Users.get(user_id=m.from_user.id)
        if m.chat.id == -1001345068459:
            user = await db.Users.exists(user_id=m.from_user.id)
            if user:
                user = await db.Users.get(user_id=m.from_user.id)
                if user.ban == 0:
                    user.money += 1000
                    user.ban = 2
                    await user.save()
                    await bot.send_message(user.user_id, "Вам было зачислено 1000💰 за вступление в группу!")
