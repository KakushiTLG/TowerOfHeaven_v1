async def dvp(call, user):
    text = """Tower of Heaven Chess Season 2 не за горами! Оставляй заявку на турнир, одолей противников и забери в карман главный приз!
Оставить заявку на участие можно в /report. Обязательно необходимо указать ссылку на свой профиль chess.com и не забыть добавить хэштег #chess

Главные призы:
1 место - 1.5 млн.💰
2 место - 750 тыс. 💰
3 место - 250 тыс. 💰
Ждём ваших заявок!"""
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



async def ref_ivent(m, user):
    allRefs = await db.Referals.filter(refer=user.user_id)
    text = "Конкурс рефералов:\n"
    if allRefs:
        for ref in allRefs:
            usr = await db.Users.filter(id=ref.idplayer).only('username')
            pts = int(ref.uppedLvls * 2) + int(ref.uppedStats * 0.2) + int(ref.killedMobs * 0.15)
            text += f"\nИгрок {usr[0].username} - {pts} очков"
    else:
        text += "\nУ вас нет рефералов, участвующих в ивенте."
    await m.answer(text)