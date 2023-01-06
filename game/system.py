async def weaponSkillUsed(user, success=None):
    if user.item == 'Копьё' and success:
        if success:
            await db.System.filter(name='spearSuccess').update(value=F('value') + 1)
        await db.System.filter(name='spearAll').update(value=F('value') + 1)
    elif user.item == 'Пистолет с ножом' and success:
        if success:
            await db.System.filter(name='pistolSuccess').update(value=F('value') + 1)
        await db.System.filter(name='pistolAll').update(value=F('value') + 1)
    elif user.item == 'Меч' and success:
        if success:
            await db.System.filter(name='swordSuccess').update(value=F('value') + 1)
        await db.System.filter(name='swordAll').update(value=F('value') + 1)
    elif user.item == 'Катана' and success:
        if success:
            await db.System.filter(name='katanaSuccess').update(value=F('value') + 1)
        await db.System.filter(name='katanaAll').update(value=F('value') + 1)

async def energyAverage(user, success=None):
    allEnergy = await db.System.get(name='allEnergy')
    allEnergy.value += user.energy
    counter = await db.System.get(name='energyCounter')
    counter.value += 1
    averageEnergy = await db.System.get(name='avgEnergy')
    averageEnergy.value = allEnergy.value / counter.value
    await allEnergy.save()
    await counter.save()
    await averageEnergy.save()


async def radarMobCreet(success):
    if success:
        await db.System.filter(name='radarMobCreets').update(value=F('value') + 1)
    await db.System.filter(name='radarMobAllAtks').update(value=F('value') + 1)


async def gachaStat(status):
    if status == 'lega':
        await db.System.filter(name='gachaLega').update(value=F('value') + 1)
    elif status == 'garant':
        await db.System.filter(name='gachaGarant').update(value=F('value') + 1)
    await db.System.filter(name='gachaAll').update(value=F('value') + 1)

async def radarAll():
    await db.System.filter(name='radarAll').update(value=F('value') + 1)
