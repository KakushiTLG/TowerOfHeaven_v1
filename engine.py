import asyncio

from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Q
from tortoise.expressions import F
import random
import time

#database = peewee.MySQLDatabase('megu', user='kakushigoto', password='d87ospdn1j', host='localhost', port=3306)

def ABC(length):
    output = ""
    for x in range(length):
        output += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')
    return output



"""class Base(Model):

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return super(Base, cls).get(*args, **kwargs)
        except Exception as e:
            return False

    class Meta:
        database = database"""



class SiteViews(Model):
    id = fields.IntField(pk=True)
    idPost = fields.IntField()
    idplayer = fields.IntField()
    class Meta:
        table = 'siteViews'
class SiteComments(Model):
    id = fields.IntField(pk=True)
    idPost = fields.IntField()
    idplayer = fields.IntField()
    text = fields.CharField(max_length=1024)
    class Meta:
        table = 'siteComments'
class SiteBanned(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    class Meta:
        table = 'siteBanned'


class Referals(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    refer = fields.IntField()
    uppedLvls = fields.IntField(default=0)
    uppedStats = fields.IntField(default=0)
    killedMobs = fields.IntField(default=0)
    class Meta:
        table = 'referals'









class HideNseek(Model):
    id = fields.IntField(pk=True)
    players = fields.JSONField()
    seeker = fields.IntField(null=True)
    status = fields.IntField(default=1)
    lefttime = fields.IntField(default=50)
    map = fields.JSONField(null=True)
    class Meta:
        table = 'hide_and_seek'
class Matches(Model):
    id = fields.IntField(pk=True)
    tournament = fields.CharField(max_length=128)
    p1 = fields.CharField(max_length=128)
    p2 = fields.CharField(max_length=128)
    w1sum = fields.IntField(default=0)
    w2sum = fields.IntField(default=0)
    status = fields.IntField(default=1)
    winner = fields.CharField(max_length=128, null=True)
    commision = fields.IntField(default=10)
    class Meta:
        table = 'matches'

class Bets(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    idmatch = fields.IntField()
    summ = fields.IntField(default=0)
    winner = fields.CharField(max_length=128)
    status = fields.IntField(default=0)
    class Meta:
        table = 'bets'


class Battle(Model):
    id = fields.IntField(pk=True)
    idbattle = fields.CharField(max_length=128)
    player = fields.CharField(max_length=128)
    mob = fields.CharField(max_length=128)
    message_id = fields.CharField(max_length=128)
    class Meta:
        table = 'battle'

class Collab(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(null=False)
    status = fields.IntField()
    code = fields.CharField(max_length=128)

    class Meta:
        table = 'collab'

class Logivent(Model):
    id = fields.IntField(pk=True)
    message = fields.CharField(max_length=128)

    class Meta:
        table = 'logivent'

class Problems(Model):
    id = fields.IntField(pk=True)
    comment = fields.CharField(max_length=128)
    status = fields.IntField(default=0)
    date = fields.IntField(default=int(time.time()))
    subs = fields.CharField(max_length=1024)

    class Meta:
        table = 'problems'





class Lobby(Model):
    id = fields.IntField(pk=True)
    player1 = fields.IntField()
    player2 = fields.IntField(default=None)
    damage1 = fields.IntField(default=0)
    damage2 = fields.IntField(default=0)
    battleLog = fields.CharField(max_length=4000, default="")
    battleStatus = fields.IntField(default=0)
    lvl = fields.IntField(default=0)
    position = fields.IntField(default=0)
    mobHp = fields.IntField(default=0)
    mobAtk = fields.IntField(default=0)
    mobName = fields.CharField(max_length=60, default="")
    class Meta:
        table = 'lobby'

class InventoryFastAccess(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    name = fields.CharField(max_length=128)
    class Meta:
        table = 'inventory_fast_access'

class Inventory(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.CharField(max_length=128)
    name = fields.CharField(max_length=128)
    descr = fields.CharField(max_length=256, null=True)
    type = fields.CharField(max_length=128)
    bonus = fields.IntField(default=0)
    active = fields.IntField(default=1)
    lvl = fields.IntField(default=1)
    size = fields.IntField(default=0)
    count = fields.IntField(default=0)
    atk_block = fields.IntField(default=0)
    expires = fields.IntField(default=0)
    class Meta:
        table = 'inventory'


class Locations(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    prev = fields.CharField(max_length=128)
    next = fields.CharField(max_length=128)
    size = fields.IntField()
    maxgold = fields.IntField()
    maxexp = fields.IntField()
    shrines = fields.CharField(max_length=128)

    class Meta:
        table = 'locations'

class Monsters(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    atk = fields.IntField()
    hp = fields.IntField()
    nowhp = fields.IntField()
    battleStatus = fields.IntField(default=0)
    battleWith = fields.IntField(null=True)
    location = fields.CharField(max_length=128)
    pos = fields.IntField()
    maxexp = fields.IntField()
    maxgold = fields.IntField()

    class Meta:
        table = 'monsters'

class Shop(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    type = fields.CharField(max_length=128)
    count = fields.IntField()
    price = fields.IntField()

    class Meta:
        table = 'shop'

class Raskul(Model):
    id = fields.IntField(pk=True)
    item = fields.IntField()
    price = fields.IntField()
    valute = fields.CharField(default='💰', max_length=128)
    status = fields.IntField(default=1)
    name = fields.CharField(max_length=128, null=True)
    owner = fields.IntField()
    type = fields.CharField(max_length=128)

    class Meta:
        table = 'raskul'

class RaskulAutoBuy(Model):
    id = fields.IntField(pk=True)
    price = fields.IntField()
    valute = fields.CharField(default='💰', max_length=128)
    status = fields.IntField(default=1)
    name = fields.CharField(max_length=128, null=True)
    owner = fields.IntField()

    class Meta:
        table = 'raskulAutoBuy'




class KriMarket(Model):
    id = fields.IntField(pk=True)
    allCount = fields.IntField(null=True)
    count = fields.IntField(null=True)
    seller = fields.IntField(null=True)
    priceForOne = fields.IntField(null=True)
    status = fields.IntField(default=1)

    class Meta:
        table = 'kriMarket'

class System(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    value = fields.IntField()
    class Meta:
        table = 'system'
class Ivent(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    pts = fields.IntField(default=0)
    class Meta:
        table = 'ivent'


class IventArena(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    count = fields.IntField(default=1)
    class Meta:
        table = 'ivent_arena'
class Temp(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=128)
    count = fields.IntField()
    class Meta:
        table = 'temp'
class TempPP(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=128)
    count = fields.FloatField()
    class Meta:
        table = 'tempPP'
class Coin(Model):
    id = fields.IntField(pk=True)
    player1 = fields.IntField()
    player2 = fields.IntField()
    status = fields.IntField()
    bet = fields.IntField()
    valute = fields.CharField(default='💰', max_length=128)
    endTime = int(time.time()) + 604800
    timeEnd = fields.IntField(default=endTime)
    class Meta:
        table = 'coin'


class CoinJackpot(Model):
    id = fields.IntField(pk=True)
    player1 = fields.IntField()
    player2 = fields.IntField()
    player3 = fields.IntField()
    bet = fields.IntField()
    fond = fields.IntField()
    winner = fields.IntField()
    class Meta:
        table = 'coin_jackpot'


class Expeditions(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField()
    timeEnd = fields.IntField()
    expType = fields.IntField()
    class Meta:
        table = 'expds'

class Fraks(Model):
    name = fields.CharField(null=False, max_length=128)
    lvl = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    atk = fields.IntField(default=20)
    anti = fields.IntField(default=0)
    players = fields.IntField(default=1)
    leader = fields.IntField(null=False)
    zam = fields.IntField(null=True)
    fond = fields.IntField(default=0)
    fondKri = fields.IntField(default=0)
    ametist = fields.IntField(default=0)
    rubin = fields.IntField(default=0)
    sapphire = fields.IntField(default=0)
    izumrud = fields.IntField(default=0)
    adText = fields.CharField(null=True, max_length=300)
    limitFond = fields.IntField(null=True)
    pvpBonus = fields.IntField(default=0)
    debuff = fields.IntField(default=0)
    onsenLvl = fields.IntField(default=0)
    hotelLvl = fields.IntField(default=0)
    cooldown = fields.IntField(default=0)
    underAtk = fields.IntField(default=0)
    class Meta:
        table = 'fraks'

class Trades(Model):
    id = fields.IntField(pk=True)
    fromP = fields.IntField()
    toP = fields.IntField()
    item = fields.IntField()
    star = fields.IntField(default=0)
    star2 = fields.IntField(default=0)
    itemreturn = fields.IntField(null=True)
    status = fields.IntField(default=0)
    class Meta:
        table = 'trades'

class DuelPool(Model):
    id = fields.IntField(pk=True)
    agressor = fields.BigIntField(default=0)
    defender = fields.BigIntField(default=0)
    current_turn = fields.CharField(null=False, max_length=128)
    react_until = fields.IntField(default=0)
    battle_log = fields.CharField(null=True, max_length=8192)
    is_reacted = fields.IntField(default=0)
    duel_location = fields.CharField(null=True, max_length=128)

    class Meta:
        table = 'DuelPool'


class Crafts(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    active = fields.IntField(null=False)
    firstItem = fields.IntField(default=None)
    secondItem = fields.IntField(default=None)
    thirdItem = fields.IntField(default=None)
    fourthItem = fields.IntField(default=None)
    fifthItem = fields.IntField(default=None)
    type=fields.CharField(max_length=128)

    class Meta:
        table = 'craft'

class Houses(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    owner = fields.IntField(null=False)
    arentLeft = fields.IntField(default=0)
    woods = fields.IntField(default=0)
    stones = fields.IntField(default=0)
    lvl = fields.IntField(default=0)
    exp = fields.IntField(default=0)
    inventory = fields.IntField(default=1)
    regenerate = fields.IntField(default=1)
    plusGold = fields.IntField(default=1)
    buyfor = fields.CharField(max_length=128)
    class Meta:
        table = 'houses'

class Recipes(Model):
    id = fields.IntField(pk=True)
    owner = fields.IntField()
    name = fields.CharField(max_length=128)
    source = fields.CharField(max_length=128)

    class Meta:
        table = 'recipes'

class Buffs(Model):
    id = fields.IntField(pk=True)
    owner = fields.IntField()
    type = fields.CharField(max_length=128)
    num = fields.IntField()
    status = fields.IntField(default=1)
    timeEnd = fields.IntField()

    class Meta:
        table = 'buffs'



class Ach(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(null=False)
    novichek = fields.CharField(default='0|0', max_length=128)
    trader = fields.CharField(default='0|0', max_length=128)
    kachalka = fields.CharField(default='0|0', max_length=128)
    shopbuy = fields.CharField(default='0|0', max_length=128)
    premiumhotel = fields.CharField(default='0|0', max_length=128)
    skupshik = fields.CharField(default='0|0', max_length=128)
    alcohol = fields.CharField(default='0|0', max_length=128)
    quest = fields.CharField(default='0|0', max_length=128)
    stavochnik = fields.CharField(default='0|0', max_length=128)
    igrovoiAvtomat = fields.CharField(default='0|0', max_length=128)
    donater = fields.CharField(default='0|0', max_length=128)
    lombarder = fields.CharField(default='0|0', max_length=128)
    halloween2020 = fields.CharField(default='0|0', max_length=128)
    kawaikluch = fields.CharField(default='0|0', max_length=128)
    ubica = fields.CharField(default='0|0', max_length=128)
    prohozhdenie = fields.CharField(default='0|0', max_length=128)
    pvpsher = fields.CharField(default='0|0', max_length=128)
    teamplayer = fields.CharField(default='0|0', max_length=128)
    prodavan = fields.CharField(default='0|0', max_length=128)
    expds = fields.CharField(default='0|0', max_length=128)
    cases = fields.CharField(default='0|0', max_length=128)
    chessJune = fields.CharField(default='0|0', max_length=128)
    gacha = fields.CharField(default='0|0', max_length=128)
    craft = fields.CharField(default='0|0', max_length=128)
    radar = fields.CharField(default='0|0', max_length=128)
    kitchen = fields.CharField(default='0|0', max_length=128)
    fishing = fields.CharField(default='0|0', max_length=128)
    class Meta:
        table = 'achievements'

class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=128, null=True)
    user_id = fields.BigIntField(null=False)
    lvl = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    energy = fields.IntField(default=100)
    psy = fields.IntField(default=100)
    eat = fields.IntField(default=100)
    money = fields.IntField(default=500)
    almaz = fields.IntField(default=0)
    gems = fields.IntField(default=0)
    shmekli = fields.IntField(default=0)
    donatesum = fields.IntField(default=0)
    ref = fields.CharField(null=True, max_length=128)
    frak = fields.CharField(null=True, max_length=128)
    location = fields.CharField(default="Город", max_length=128)
    progLoc = fields.CharField(default="Город|0", max_length=128)
    progStatus = fields.IntField(default=0)
    position = fields.CharField(default="Площадь", max_length=128)
    inventorySizeMax = fields.IntField(default=10)
    item = fields.CharField(null=True, max_length=128)
    visualitem = fields.CharField(null=True, max_length=128)
    uppts = fields.IntField(default=5)
    atk = fields.IntField(default=20)
    hp = fields.IntField(default=20)
    nowhp = fields.IntField(default=20)
    cooker = fields.IntField(default=0)
    fisher = fields.IntField(default=0)
    luckerAvtomat = fields.IntField(default=0)
    masterWeapon = fields.IntField(default=0)
    skillInv = fields.IntField(default=0)
    krazha = fields.IntField(default=0)
    antikrazha = fields.IntField(default=0)
    reactionPvP = fields.IntField(default=0)
    zamoroz = fields.IntField(default=0)
    humidity = fields.IntField(default=0)
    armor = fields.IntField(default=0)
    battleStatus = fields.IntField(default=0)
    battleWith = fields.IntField(null=True)
    sleepPlayer = fields.IntField(default=0)
    tradecount = fields.IntField(default=0)
    tradenum = fields.IntField(default=3)
    scenario = fields.IntField(default=0, max_length=128)
    scenarioStatus = fields.IntField(default=0, max_length=128)
    quest = fields.CharField(null=True, max_length=128)
    questId = fields.IntField(default=0)
    questStatus = fields.IntField(default=0)
    heavenCurrency = fields.IntField(default=0)
    kawaiCurrency = fields.IntField(default=0)
    oceanCurrency = fields.IntField(default=0)
    radarCurrency = fields.IntField(default=0)
    metroCurrency = fields.IntField(default=0)
    oduvanchik = fields.IntField(default=0)
    rca = fields.IntField(default=0)
    roza = fields.IntField(default=0)
    sakura = fields.IntField(default=0)
    kotelokLimit = fields.IntField(default=500)
    partner = fields.IntField(default=0)
    donatesumPartn = fields.IntField(default=0)
    ban = fields.IntField(default=0)
    banEnds = fields.IntField(default=0)
    banreason = fields.CharField(null=True, max_length=128)
    regDate = fields.IntField(null=True)
    slava = fields.IntField(default=0)
    coupon = fields.IntField(default=0)
    ppTop = fields.IntField(default=0)
    iventCount = fields.IntField(default=0)
    booster = fields.IntField(default=0)
    supporter = fields.IntField(default=0)
    bpLvl = fields.IntField(default=0)
    bpStatus = fields.IntField(default=0)
    badge = fields.CharField(null=True, max_length=64)
    token = fields.CharField(null=True, max_length=64)
    godEye = fields.IntField(null=True, max_length=64)
    gachaGarant = fields.IntField(default=0)
    radarKD = fields.IntField(default=0)
    dailyBP = fields.IntField(default=0)
    class Meta:
        table = 'users'

class Giveaway(Model):
    id = fields.IntField(pk=True)
    user = fields.IntField(null=False)
    class Meta:
        table = 'giveaway'
class BlacklistItems(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    name = fields.CharField(default=0, max_length=256)
    class Meta:
        table = 'blacklistItems'

class Api(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=True)
    bot = fields.CharField(default=0, max_length=128)
    botStatus = fields.IntField(default=0)
    class Meta:
        table = 'api'

class Notifications(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=True)
    hotel = fields.IntField(default=1)
    onsen = fields.IntField(default=1)
    eat = fields.IntField(default=1)
    energy = fields.IntField(default=1)
    loc_effects = fields.IntField(default=1)
    regs = fields.IntField(default=1)
    buffs = fields.IntField(default=1)
    class Meta:
        table = 'notifications'

class MoneyDropLoc(Model):
    id = fields.IntField(pk=True)
    progLoc = fields.CharField(max_length=128)
    amount = fields.IntField(default=0)
    username = fields.CharField(max_length=128)
    class Meta:
        table = 'moneyDropLoc'

class tempQuest(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(null=False)
    quest = fields.CharField(null=False, max_length=128)
    progress = fields.IntField(null=False)
    status = fields.IntField(null=False)
    timeEnd = fields.IntField(null=False)
    class Meta:
        table = 'tempQuest'


class Quests(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    name = fields.CharField(null=False, max_length=128)
    descr = fields.CharField(null=False, max_length=512)
    status = fields.IntField(null=False)
    progress = fields.IntField(null=False)
    class Meta:
        table = 'quests'

class Bot(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    model = fields.CharField(default='A', max_length=16)
    atk = fields.IntField(default=5)
    hp = fields.IntField(default=5)
    nowhp = fields.IntField(default=5)
    lvl = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    status = fields.IntField(default=1)
    details = fields.IntField(default=0)
    password = fields.CharField(default=ABC(8), max_length=32)
    class Meta:
        table = 'bots'



class BotInventory(Model):
    id = fields.IntField(pk=True)
    idbot = fields.IntField(null=False)
    name = fields.CharField(max_length=128)
    descr = fields.CharField(max_length=128, null=True)
    type = fields.CharField(max_length=128)
    bonus = fields.IntField(default=0)
    active = fields.IntField(default=1)
    lvl = fields.IntField(default=1)
    size = fields.IntField(default=0)
    lastAtk = fields.IntField(default=0)
    class Meta:
        table = 'botInventory'

class BotLogs(Model):
    id = fields.IntField(pk=True)
    idbot = fields.IntField(null=False)
    text = fields.CharField(max_length=512)
    class Meta:
        table = 'botLogs'


class NewYearIvent(Model):
    id = fields.IntField(pk=True)
    idplayer = fields.IntField(null=False)
    surprises = fields.IntField(default=0)
    hlopushki = fields.IntField(default=0)

    class Meta:
        table = 'NewYearIvent'




async def get_db():
    await Tortoise.init(db_url="mysql://usr:psswd@localhost:3306/megu", modules={"models": ["engine"]})
    await Tortoise.generate_schemas()
loop = asyncio.get_event_loop()
tort_db = loop.run_until_complete(get_db())




async def getpp(user):
    if True:
        itemBonus = 0
        item = await Inventory.get_or_none(type='Оружие', idplayer=user.id, active=2).only('bonus').first()
        if item:
            itemBonus = item.bonus / 9
        achs = await Ach.get_or_none(user_id=user.user_id).only('pvpsher', 'ubica').first()
        if achs:
            checkMobKills = achs.ubica.split("|")
            killedMobs = int(checkMobKills[0])
            checkPvpWins = achs.pvpsher.split("|")
            pvpWins = int(checkPvpWins[0])
            if user.atk > 2000: kfAtk = (500 * 0.14) + (500 * 0.16) + (500 * 0.21) + (500 * 0.25) + ((user.atk - 2000) * 0.3)
            elif user.atk > 1500: kfAtk = (500 * 0.14) + (500 * 0.16) + (500 * 0.21) + ((user.atk - 1500) * 0.25)
            elif user.atk > 1000: kfAtk = (500 * 0.14) + (500 * 0.16) + ((user.atk - 1000) * 0.21)
            elif user.atk > 500: kfAtk = (500 * 0.14) + ((user.atk - 500) * 0.16)
            else: kfAtk = user.atk * 0.13
            if user.hp > 2000: kfHp = (500 * 0.15) + (500 * 0.17) + (500 * 0.22) + (500 * 0.26) + ((user.hp - 2000) * 0.32)
            elif user.hp > 1500: kfHp = (500 * 0.15) + (500 * 0.17) + (500 * 0.22) + ((user.hp - 1500) * 0.26)
            elif user.hp > 1000: kfHp = (500 * 0.15) + (500 * 0.17) + ((user.hp - 1000) * 0.22)
            elif user.hp > 500: kfHp = (500 * 0.15) + ((user.hp - 500) * 0.17)
            else: kfHp = user.hp * 0.15
            if user.slava > 750: kfSlava = (250 * 1) + (500 * 1.25) + ((user.slava - 750) * 1.5)
            elif user.slava > 250: kfSlava = (250 * 1) + ((user.slava - 250) * 1.25)
            else: kfSlava = user.slava * 1
            if killedMobs > 30000: kfMobs = (1000 * 0.11) + (14000 * 0.06) + (15000 * 0.04) + ((killedMobs - 30000) * 0.01)
            elif killedMobs > 15000: kfMobs = (1000 * 0.11) + (14000 * 0.06) + ((killedMobs - 15000) * 0.04)
            elif killedMobs > 1000: kfMobs = (1000 * 0.11) + ((killedMobs - 1000) * 0.06)
            else: kfMobs = killedMobs * 0.11
            _pp = ((kfAtk + (user.lvl * itemBonus)) + (kfHp)) + (kfSlava) + (kfMobs) + (pvpWins * 0.5)
            pp = round(_pp, 2)
        else:
            pp = 0
    return pp


inventorySizes = {}
battleUserArmors = {}

import inventories
inventorys = inventories.invs

async def commitInventory(user, item):
    global inventorys
    if item == 'getInv':
        inventorys[user.id] = {}
        inv = await Inventory.filter(~Q(active=0), idplayer=user.id)
        for itm in inv:
            inventorys[user.id][itm.id] = {'name': itm.name, 'active': itm.active, 'size': itm.size,
                        'atk_block': itm.atk_block, 'lvl': itm.lvl, 'expires': itm.expires, 'type': itm.type,
                        'bonus': itm.bonus}
        return
    if user.id in inventorys and item.id in inventorys[user.id]:
        if item.active == 0 or item.idplayer != user.id:
            del inventorys[user.id][item.id]
        else:
            inventorys[user.id][item.id]['active'] = item.active
    else:
        inventorys[user.id] = {}
        inv = await Inventory.filter(~Q(active=0), idplayer=user.id)
        for itm in inv:
            inventorys[user.id][itm.id] = {'name': itm.name, 'active': itm.active, 'size': itm.size,
                        'atk_block': itm.atk_block, 'lvl': itm.lvl, 'expires': itm.expires, 'type': itm.type,
                        'bonus': itm.bonus}

def updateInventoriesModule():
    global inventorys
    with open('./inventories.py', 'w', encoding='utf-8') as file:
        file.write('invs = {}'.format(inventorys))
        file.close()


async def cachedInventory(user, result):
    if result.active == 2:
        if user.id not in battleUserArmors or battleUserArmors[user.id] == None:
            battleUserArmors[user.id] = []
            _checkarmor = await Inventory.filter(active=2, idplayer=user.id).only('name')
            for itm in _checkarmor:
                battleUserArmors[user.id].append(itm.name)
        else:
            if result.name not in battleUserArmors[user.id]:
                battleUserArmors[user.id].append(result.name)
            else:
                battleUserArmors[user.id] = []
                _checkarmor = await Inventory.filter(active=2, idplayer=user.id).only('name')
                for itm in _checkarmor:
                    battleUserArmors[user.id].append(itm.name)
    else:
        if user.id not in battleUserArmors or battleUserArmors[user.id] == None:
            battleUserArmors[int(user.id)] = []
            _checkarmor = await Inventory.filter(active=2, idplayer=user.id).only('name')
            for itm in _checkarmor:
                battleUserArmors[int(user.id)].append(itm.name)
        else:
            if result.name in battleUserArmors[user.id]:
                battleUserArmors[user.id].remove(result.name)
            else:
                battleUserArmors[int(user.id)] = []
                _checkarmor = await Inventory.filter(active=2, idplayer=user.id).only('name')
                for itm in _checkarmor:
                    battleUserArmors[int(user.id)].append(itm.name)
    await commitInventory(user, result)


async def getInventorySize(user, inventory=None):
    inventorySize = 0
    if inventory:
        for dict in inventory:
            size = await items(dict.name, check='size')
            inventorySize += int(size)
        timed = int(time.time()) + 60
        inventorySizes[user.id] = {'time': timed, 'inventorySize': inventorySize}
    else: # Убрать из условия True чтобы включить кэширование
        if user.id not in inventorySizes or True or user.id in inventorySizes and inventorySizes[user.id]['time'] > int(time.time()):
            inventory = await Inventory.filter(idplayer=user.id, active=1).only('name')
            sizes = {}
            for dict in inventory:
                if dict.name not in sizes:
                    size = await items(dict.name, check='size')
                    sizes[dict.name] = int(size)
                inventorySize += int(sizes[dict.name])
            timed = int(time.time()) + 60
            inventorySizes[user.id] = {'time': timed, 'inventorySize': inventorySize}
        else: inventorySize = inventorySizes[user.id]['inventorySize']
    return inventorySize
async def getHouseInventorySize(user, inventory=None):
    inventorySize = 0
    if inventory:
        for dict in inventory:
            size = await items(dict.name, check='size')
            inventorySize += int(size)
    else:
        inventory = await Inventory.filter(idplayer=user.id, active=10).only('name')
        for dict in inventory:
            size = await items(dict.name, check='size')
            inventorySize += int(size)
    return inventorySize
async def getCraftInventorySize(user, inventory=None):
    inventorySize = 0
    if inventory:
        for dict in inventory:
            inventorySize += 1
    else:
        inventory = await Inventory.filter(idplayer=user.id, active=5).only('name')
        for dict in inventory:
            inventorySize += 1
    return inventorySize



async def addItemBot(name, droid):
    droid = await Bot.get_or_none(id=droid.id).first()
    if not droid: return False
    _ = BotItems[name]
    name, Type, descr, size, bonus = _.name, _.type, _.descr, _.size, _.bonus
    await BotInventory.create(name=name, type=Type, descr=descr, size=size, bonus=bonus, lvl=1, idbot=droid.id, active=1)
    return True





async def addItem(name, user, arg=None, invsType=None):
    newItem = None
    checkItemInBlacklist = await BlacklistItems.exists(idplayer=user.id, name=name)
    if not checkItemInBlacklist:
        if invsType != None:
            checkItem = await Inventory.exists(name=name, idplayer=user.id)
        else:
            if arg != None:
                Type, size, bonus, atk_block, expires = await items(name, check=False)
                if not atk_block: atk_block = 0
                if expires and expires > 0:
                    expTime = int(time.time()) + (expires * 60 * 60)
                    newItem = await Inventory.create(name=name, type=Type, size=size, bonus=bonus, active=1, idplayer=user.id, atk_block=atk_block, expires=expTime)
                else:
                    newItem = await Inventory.create(name=name, type=Type, size=size, bonus=bonus, active=1, idplayer=user.id, atk_block=atk_block)
                success = True
                return success
            else:
                check = False
                Type, size, bonus, atk_block, expires = await items(name, check=False)
                if not atk_block: atk_block = 0
                inventorySize = await getInventorySize(user)
                if inventorySize + size > user.inventorySizeMax:
                    success = False
                else:
                    if expires:
                        expTime = int(time.time()) + (expires * 60 * 60)
                        newItem = await Inventory.create(name=name, type=Type, size=size, bonus=bonus, active=1, idplayer=user.id, atk_block=atk_block, expires=expTime)
                    else:
                        newItem = await Inventory.create(name=name, type=Type, size=size, bonus=bonus, active=1, idplayer=user.id, atk_block=atk_block)
                    success = True
        if success and newItem:
            await cachedInventory(user, newItem)
    else:
        success = True
    return success



async def addArt(name, user, arg=None, invsType=None):
    if invsType != None:
        checkItem = await Inventory.exists(name=name, idplayer=user.id)
    else:
        check = False
        Type, size, bonus, atk_block, expires = await items(name, check=False)
        if not atk_block: atk_block = 0
        if name in ['Сувенир с моря', 'Квинтэссенция камня','Палка ярости','Камень-металлолом']: active=1
        else:active=5
        newItem = await Inventory(name=name, type=Type, size=size, bonus=bonus, active=active, idplayer=user.id, atk_block=atk_block, expires=0, lvl=arg)
        await newItem.save()
        success = True
    return success

async def addBoost(user, lvl):
    await Inventory.create(name='Бустер', type='Прочее', size=0, bonus=0, active=1, idplayer=user.id, atk_block=0, lvl=lvl)




async def useEat(user, result):
    if result.active == 1:
        if result.expires >= int(time.time()):
            name, size, bonus, atk_block, expires = await items(result.name, check=True)
            if user.eat + bonus > 100: user.eat = 100
            else: user.eat += bonus
            result.active = 0
            text = "Ты сьел {}. Приятного аппетита!".format(name)
            if result.name == "Печенье с предсказанием":
                pechene = ['Записка из печенья гласит: _Ваша улыбка обладает невероятной силой.\nОтпугивать окружающих._', 'Записка из печенья гласит: _Трижды хлопни, прошепчи "Натурал", потряси правой рукой, а теперь проверь свой инвентарь._', 'Записка из печенья гласит: _Сегодня вам может повезти. А может и не повезти_\n¯(ツ)¯',
                'Записка из печенья гласит: _ОНИ ДЕРЖАТ МЕНЯ В ЗАЛОЖНИКАХ И ЗАСТАВЛЯЮТ ПОСТОЯННО ПРИДУМЫВАТЬ ТЕКСТЫ ДЛЯ ЭТОГО ПЕЧЕНЬЯ, ПОМОГИТЕ!_', 'Записка из печенья гласит: _Не гневи разработчика, он может засунуть тебе хер огра в такие места, о которых ты и не догадывался._', 'Записка из печенья гласит: _На тебя сегодня упадёт пианино, будь осторожен._',
                'Записка из печенья гласит: _ЗДОХНЕШ!_', 'Записка из печенья гласит: _Звёзды говорят... Козерога в этом месяце ждёт успех и процветание._', 'Записка из печенья гласит: _Бип. Бросьте монетку, чтобы получить предсказание. Буп._', 'Записка из печенья гласит: _Герой, судьба твоя трудна. На твоём пути к счастью препятствия будут появляться одно за другим... Но, в конце концов, ты обретёшь то, чего всегда желал, герой._',
                'Записка из печенья гласит: _И всё поглотит пламя._', 'Записка из печенья гласит: _\nКартофель 1 кг \nМасло сливочное \nКетчуп \nМакароны \nЯйца_', 'Записка из печенья гласит: _Игры кончились, у тебя 24 часа чтобы погасить долг. У нас твои близкие и лучше тебе поторопиться, пока с ними не случилось чего-то._',
                'Записка из печенья гласит: _Проснитесь и пойте, проснитесь и пойте._', 'Записка из печенья гласит: _Отдай девчонку и долг будет прощен._', 'Записка из печенья гласит: _Свалка таит в себе куда более ценные скоровища, чем кажется на первый взгляд._',
                'Записка из печенья гласит: _В этом печенье был очень сильный яд, который через три дня заставит твои внутренности плавиться, кожу облазить, а кости ломаться под малейшей нагрузкой. Положи 900 золота возле камня слева от тебя и мы отдадим тебе антидот. Ты конечно можешь и не верить, но кто знает, чем все это обернётся._',
                'Записка из печенья гласит: _Порой нужно отдавать, не ожидая получить что-то взамен._', 
                'Записка из печенья гласит: _Если появится возможность - воспользуйся ею._', 'Записка из печенья гласит: _В любой непонятной ситуации закупайся свитками телепортации._', 'Записка из печенья гласит: _Мы узнали твоё настоящее имя! Тебе не уйти_']
                name = user.username
                pr = random.choice(pechene)
                text += str(pr)
            elif result.name == 'Бульон курильщика':
                if user.nowhp <= user.hp:
                    await Users.filter(id=result.idplayer).update(nowhp=F('nowhp') + 150)
            elif result.name == 'Сашими':
                if user.nowhp <= user.hp:
                    await Users.filter(id=result.idplayer).update(nowhp=F('nowhp') + 200)
            elif result.name == 'Борщ':
                if user.nowhp <= user.hp:
                    await Users.filter(id=result.idplayer).update(nowhp=F('nowhp') + 250)
            elif result.name == 'Сила узбека':
                if user.nowhp <= user.hp:
                    await Users.filter(id=result.idplayer).update(nowhp=F('nowhp') + 300)
            elif result.name == 'Пряная рыба с луком':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальная пряная рыба с луком':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=10, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Манты с сюрпризом':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальные манты с сюрпризом':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=10, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Макарошки с кулером':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=2, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальные макарошки с кулером':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            

            elif result.name == 'Солевая сигарилла':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=2, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальная солевая сигарилла':
                tme = 60 * 30
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Аль денте салат':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=15, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальный аль денте салат':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=30, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Богатырский суп':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=15, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальный богатырский суп':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=30, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Онигири':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальные онигири':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=10, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            
            elif result.name == 'Собственно в соку':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=5, status=1, timeEnd=timeEnd)
                await newBuff.save()            
            elif result.name == 'Идеальный собственно в соку':
                tme = 60 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=10, status=1, timeEnd=timeEnd)
                await newBuff.save()            

            elif result.name == 'Подозрительная жидкость':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=40, status=1, timeEnd=timeEnd)
                await newBuff.save()
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))        
            elif result.name == 'Идеальная подозрительная жидкость':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='atk', num=50, status=1, timeEnd=timeEnd)
                await newBuff.save()            
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))

            elif result.name == 'Зубная паста':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=40, status=1, timeEnd=timeEnd)
                await newBuff.save()
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))        
            elif result.name == 'Идеальная зубная паста':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='armor', num=50, status=1, timeEnd=timeEnd)
                await newBuff.save()            
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))

            elif result.name == 'Слёзы Сани':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=15, status=1, timeEnd=timeEnd)
                await newBuff.save()
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))        
            elif result.name == 'Идеальные слёзы Сани':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='uv', num=20, status=1, timeEnd=timeEnd)
                await newBuff.save()            
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))

            elif result.name == 'Жареный раком':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=15, status=1, timeEnd=timeEnd)
                await newBuff.save()
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))        
            elif result.name == 'Идеальный жареный раком':
                tme = 120 * 60
                timeEnd = int(time.time()) + tme
                newBuff = await Buffs(owner=user.id, type='creet', num=20, status=1, timeEnd=timeEnd)
                await newBuff.save()            
                await Users.filter(id=result.idplayer).update(nowhp=F('hp'))

            await Users.filter(id=user.id).update(eat=user.eat)
        else:
            name, size, bonus, atk_block, expires = await items(result.name, check=True)
            result.active = 0
            antiBonus = int(user.nowhp * 0.35)
            text = "Откусив кусочек от {}, ты почувствовал этот максимально тошнотворный вкус. К сожалению, это было последнее что ты успел почувствовать перед тем как тебя стошнило... Что же, иногда следует смотреть на срок годности.\n-{}❤️".format(name, antiBonus)
            if result.name == "🥠 Печенье с предсказанием":
                pechene = ['Записка из печенья гласит: _Ваша улыбка обладает невероятной силой.\nОтпугивать окружающих._', 'Записка из печенья гласит: _Трижды хлопни, прошепчи "Натурал", потряси правой рукой, а теперь проверь свой инвентарь._', 'Записка из печенья гласит: _Сегодня вам может повезти. А может и не повезти_\n¯(ツ)¯',
                'Записка из печенья гласит: _ОНИ ДЕРЖАТ МЕНЯ В ЗАЛОЖНИКАХ И ЗАСТАВЛЯЮТ ПОСТОЯННО ПРИДУМЫВАТЬ ТЕКСТЫ ДЛЯ ЭТОГО ПЕЧЕНЬЯ, ПОМОГИТЕ!_', 'Записка из печенья гласит: _Не гневи разработчика, он может засунуть тебе хер огра в такие места, о которых ты и не догадывался._', 'Записка из печенья гласит: _На тебя сегодня упадёт пианино, будь осторожен._',
                'Записка из печенья гласит: _ЗДОХНЕШ!_', 'Записка из печенья гласит: _Звёзды говорят... Козерога в этом месяце ждёт успех и процветание._', 'Записка из печенья гласит: _Бип. Бросьте монетку, чтобы получить предсказание. Буп._', 'Записка из печенья гласит: _Герой, судьба твоя трудна. На твоём пути к счастью препятствия будут появляться одно за другим... Но, в конце концов, ты обретёшь то, чего всегда желал, герой._',
                'Записка из печенья гласит: _И всё поглотит пламя._', 'Записка из печенья гласит: _\nКартофель 1 кг \nМасло сливочное \nКетчуп \nМакароны \nЯйца_', 'Записка из печенья гласит: _Игры кончились, у тебя 24 часа чтобы погасить долг. У нас твои близкие и лучше тебе поторопиться, пока с ними не случилось чего-то._',
                'Записка из печенья гласит: _Проснитесь и пойте, проснитесь и пойте._', 'Записка из печенья гласит: _Отдай девчонку и долг будет прощен._', 'Записка из печенья гласит: _Свалка таит в себе куда более ценные скоровища, чем кажется на первый взгляд._',
                'Записка из печенья гласит: _В этом печенье был очень сильный яд, который через три дня заставит твои внутренности плавиться, кожу облазить, а кости ломаться под малейшей нагрузкой. Положи 900 золота возле камня слева от тебя и мы отдадим тебе антидот. Ты конечно можешь и не верить, но кто знает, чем все это обернётся._',
                'Записка из печенья гласит: _Порой нужно отдавать, не ожидая получить что-то взамен._', 
                'Записка из печенья гласит: _Если появится возможность - воспользуйся ею._', 'Записка из печенья гласит: _В любой непонятной ситуации закупайся свитками телепортации._', 'Записка из печенья гласит: _Мы узнали твоё настоящее имя! Тебе не уйти_']
                name = user.username
                pr = random.choice(pechene)
                text += str(pr)
            await Users.filter(id=user.id).update(eat=0, nowhp = F('nowhp') - antiBonus)
        await Inventory.filter(id=result.id).update(active=0)
    else: text = "Предмета на существует!"
    if result.name == "Валентинка" and result.descr:
        text += "\nВнутри шоколадки оказалась записка:\n\n{}".format(result.descr)
    elif result.name == "Валентинка":
        text += "\nВнутри шоколадки оказалась записка:\n\nИнновационные технологии помогают человечество летать в космос и ломать умы над вопросами колонизации планет. Компания ТОшеН предлагает вам заняться подготовкой планет к этому процессу прямо сейчас!\n[Это @Operation2222_bot](tg://user?id=5045146213)"
    return text


 # Айди, имя, тип, размер, бонус, атк_блок, истекает
class BottoItem(object):
    __slots__ = ['i_id', 'name', 'type', 'descr', 'size', 'bonus']
    def __init__(self, i_id, name, _type, _descr, size, bonus):
        self.i_id = i_id
        self.name = name
        self.type = _type
        self.descr = _descr
        self.size = size
        self.bonus = bonus

    def toJSON(self):
        data = dict()
        for var in self.__slots__:
            data[var] = getattr(self, var)
        return json.dumps(data)



BotItems = {}

BotItems['Чип ОС'] = BottoItem(1, 'Чип ОС', 'Чип', 'Извлечение означает смерть', 5, 0)
BotItems['Чип ОЗ'] = BottoItem(2, 'Чип ОЗ', 'Чип', 'Показывает текущее здоровье Бота', 5, 0)
BotItems['Чип ОП'] = BottoItem(3, 'Чип ОП', 'Чип', 'Показывает шкалу опыта', 5, 0)
BotItems['Урон+'] = BottoItem(4, 'Урон+', 'Урон', 'Повышает урон Бота на 3%', 5, 0)
BotItems['Урон++'] = BottoItem(5, 'Урон++', 'Урон', 'Повышает урон Бота на 6%', 9, 0)
BotItems['Урон+++'] = BottoItem(6, 'Урон+++', 'Урон', 'Повышает урон Бота на 9%', 12, 0)
BotItems['Крит+'] = BottoItem(7, 'Крит+', 'Чип', 'Повышает шанс крита Бота на 3%', 5, 0)
BotItems['Крит++'] = BottoItem(8, 'Крит++', 'Чип', 'Повышает шанс крита Бота на 6%', 9, 0)
BotItems['Крит+++'] = BottoItem(9, 'Крит+++', 'Чип', 'Повышает шанс крита Бота на 9%', 12, 0)
BotItems['Здоровье+'] = BottoItem(10, 'Здоровье+', 'Здоровье', 'Повышает общий показатель здоровья Бота на 3%', 5, 0)
BotItems['Здоровье++'] = BottoItem(11, 'Здоровье++', 'Здоровье', 'Повышает общий показатель здоровья Бота на 6%', 9, 0)
BotItems['Здоровье+++'] = BottoItem(12, 'Здоровье+++', 'Здоровье', 'Повышает общий показатель здоровья Бота на 9%', 12, 0)
BotItems['Уклонение+'] = BottoItem(13, 'Уклонение+', 'Чип', 'Повышает шанс уклонения Бота на 3%', 5, 0)
BotItems['Уклонение++'] = BottoItem(14, 'Уклонение++', 'Чип', 'Повышает шанс уклонения Бота на 6%', 9, 0)
BotItems['Уклонение+++'] = BottoItem(15, 'Уклонение+++', 'Чип', 'Повышает шанс уклонения Бота на 9%', 12, 0)
BotItems['Защита+'] = BottoItem(16, 'Защита+', 'Чип', 'Повышает гарантированное поглощения урона по Боту на 3%', 5, 0)
BotItems['Защита++'] = BottoItem(17, 'Защита++', 'Чип', 'Повышает гарантированное поглощения урона по Боту на 6%', 9, 0)
BotItems['Защита+++'] = BottoItem(18, 'Защита+++', 'Чип', 'Повышает гарантированное поглощения урона по Боту на 9%', 12, 0)
BotItems['Утилизация+'] = BottoItem(19, 'Утилизация+', 'Чип', 'Восстанавливает боту 3% здоровья при убийстве монстра', 5, 0)
BotItems['Утилизация++'] = BottoItem(20, 'Утилизация++', 'Чип', 'Восстанавливает боту 6% здоровья при убийстве монстра', 9, 0)
BotItems['Утилизация+++'] = BottoItem(21, 'Утилизация+++', 'Чип', 'Восстанавливает боту 9% здоровья при убийстве монстра', 12, 0)
BotItems['Уклонение+'] = BottoItem(22, 'Уклонение+', 'Чип', 'Повышает шанс уклонения от атаки монстра на 3%', 5, 0)
BotItems['Уклонение++'] = BottoItem(23, 'Уклонение++', 'Чип', 'Повышает шанс уклонения от атаки монстра на 6%', 9, 0)
BotItems['Уклонение+++'] = BottoItem(24, 'Уклонение+++', 'Чип', 'Повышает шанс уклонения от атаки монстра на 9%', 12, 0)
BotItems['Удача+'] = BottoItem(25, 'Удача+', 'Чип', 'Повышает шанс выпадения Деталей на 3%', 5, 0)
BotItems['Удача++'] = BottoItem(26, 'Удача++', 'Чип', 'Повышает шанс выпадения Деталей на 6%', 9, 0)
BotItems['Удача+++'] = BottoItem(27, 'Удача+++', 'Чип', 'Повышает шанс выпадения Деталей на 9%', 12, 0)
BotItems['Лазерный выстрел'] = BottoItem(28, 'Лазерный выстрел', 'Оружие', 'Наносит 500% урона, КД - 10К', 15, 0)
BotItems['Чип поиска конфет'] = BottoItem(29, 'Чип поиска конфет', 'Чип', 'Повышает шанс на нахождение конфеты на 5%', 5, 0)








 # Айди, имя, тип, размер, бонус, атк_блок, истекает
class DataItem(object):
    __slots__ = ['i_id', 'name', 'type', 'size', 'bonus', 'atk_block', 'expires']
    def __init__(self, i_id, name, _type, size, bonus, atk_block, expires):
        self.i_id = i_id
        self.name = name
        self.type = _type
        self.size = size
        self.bonus = bonus
        self.atk_block = atk_block
        self.expires = expires

    def toJSON(self):
        data = dict()
        for var in self.__slots__:
            data[var] = getattr(self, var)
        return json.dumps(data)



Items = {}

Items['Туннельный свиток'] = DataItem(1, '📜Туннельный свиток', 'Свиток', 0, 0, 0, 0)
Items['Бумажный бургер'] = DataItem(2, '🍔Бумажный бургер', 'Еда', 1, 13, 0, 48)
Items['Он называет это "яблоко"'] = DataItem(3, '🔴"яблоко"', 'Еда', 1, 30, 0, 100)
Items['Хер огра'] = DataItem(4, '🥒Хер огра', 'Еда', 1, 34, 0, 24)
Items['Бывший сосед'] = DataItem(5, '🥩Бывший сосед', 'Еда', 1, 38, 0, 5)
Items['Консервы из палеозоя'] = DataItem(6, '🥫Консервы из палеозоя', 'Еда', 1, 24, 0, 72)
Items['Печенье с предсказанием'] = DataItem(7, '🥠Печенье с предсказанием', 'Еда', 1, 18, 0, 48)
Items['Лучше не спрашивай'] = DataItem(8, '👁‍🗨Лучше не спрашивай', 'Еда', 1, 99, 0, 48)
Items['Бывший сосед(поджаренный)'] = DataItem(9, '🥓Бывший сосед(поджаренный)', 'Еда', 1, 55, 0, 24)
Items['Бывший сосед(замороженный)'] = DataItem(10, '🥩Бывший сосед(замороженный)', 'Еда', 1, 62, 0, 48)
Items['Большой хер огра'] = DataItem(11, '🥒Большой хер огра', 'Еда', 1, 65, 0, 12)
Items['Кошелёк падшего героя'] = DataItem(12, 'Кошелёк падшего героя', 'Прочее', 0, 0, 0, 0)
Items['Кожаный шлем'] = DataItem(13, '🧢Кожаный шлем', 'Броня', 1, 9, 0, 0)
Items['Кожаный нагрудник'] = DataItem(14, '👕Кожаный нагрудник', 'Броня', 2, 15, 0, 0)
Items['Кожаные штаны'] = DataItem(15, '👖Кожаные штаны', 'Броня', 1, 12, 0, 0)
Items['Кожаные ботинки'] = DataItem(16, '👟Кожаные ботинки', 'Броня', 1, 12, 0, 0)
Items['Хоккейная маска'] = DataItem(17, '🧢Хоккейная маска', 'Броня', 1, 21, 0, 0)
Items['Бронежилет'] = DataItem(18, '👕Бронежилет', 'Броня', 2, 39, 0, 0)
Items['Спортивки адидас'] = DataItem(19, '👖Спортивки адидас', 'Броня', 1, 32, 0, 0)
Items['Берцы'] = DataItem(20, '👟Берцы', 'Броня', 1, 21, 0, 0)
Items['Шлем из фольги'] = DataItem(21, '🧢Шлем из фольги', 'Броня', 1, 3, 0, 0)
Items['Майка из пакета'] = DataItem(22, '👕Майка из пакета', 'Броня', 1, 6, 0, 0)
Items['НЕкроссовки'] = DataItem(23, '👟НЕкроссовки', 'Броня', 1, 3, 0, 0)
Items['Шляпа фокусника'] = DataItem(24, '🎩Шляпа фокусника', 'Броня', 1, 20, 0, 0)
Items['Кросы адидас'] = DataItem(25, '👟Кросы адидас', 'Броня', 1, 22, 0, 0)
Items['Комбинезон сталкера'] = DataItem(26, '👕Комбинезон сталкера', 'Броня', 2, 40, 0, 0)
Items['Нижнее бельё Раскуловой'] = DataItem(27, '👙Нижнее бельё Раскуловой', 'Броня', 1, 25, 0, 0)
Items['Тушка питона'] = DataItem(28, '🐍Тушка питона', 'Хлам', 1, 0, 0, 0)
Items['Перо ястреба'] = DataItem(29, '🦅Перо ястреба', 'Хлам', 0, 0, 0, 0)
Items['Свиток телепортации'] = DataItem(30, '📜Свиток телепортации', 'Свиток', 1, 0, 0, 0)
Items['Среднее зелье здоровья'] = DataItem(31, '🧪Среднее зелье здоровья', 'Зелье', 1, 35, 0, 0)
Items['Малое зелье здоровья'] = DataItem(32, '🧪Малое зелье здоровья', 'Зелье', 1, 15, 0, 0)
Items['Большое зелье здоровья'] = DataItem(33, '🧪Большое зелье здоровья', 'Зелье', 1, 55, 0, 0)
Items['Малое зелье восстановления'] = DataItem(34, '🧪Малое зелье восстановления', 'Зелье', 1, 0, 0, 0)
Items['Среднее зелье восстановления'] = DataItem(35, '🧪Среднее зелье восстановления', 'Зелье', 1, 0, 0, 0)
Items['Зелье восстановления'] = DataItem(36, '🧪Зелье восстановления', 'Зелье', 2, 0, 0, 0)
Items['Кофе'] = DataItem(37, '☕️Кофе', 'Экипировка', 1, 70, 0, 0)
Items['Улучшенный рюкзак'] = DataItem(38, '🎒Улучшенный рюкзак', 'Экипировка', 0, 0, 0, 0)
Items['Кусок паззла'] = DataItem(39, '🧩Кусок паззла', 'Артефакт', 0, 0, 0, 0)
Items['Волшебные кости'] = DataItem(40, '🎲Волшебные кости', 'Артефакт', 0, 0, 0, 0)
Items['Амулет здоровья'] = DataItem(41, '🔶Амулет здоровья', 'Артефакт', 1, 0, 0, 0)
Items['Маленький сундучок'] = DataItem(42, '🧳Маленький сундучок', 'Сундук', 1, 0, 0, 0)
Items['Шкатулка Кефира'] = DataItem(43, '🧳Шкатулка Кефира', 'Сундук', 1, 0, 0, 0)
Items['Вибратор Ани'] = DataItem(44, '🎤Вибратор Ани', 'Хлам', 0, 0, 0, 0)
Items['Звезда смерти'] = DataItem(45, '🌐Звезда смерти', 'Хлам', 0, 0, 0, 0)
Items['Ручной Ктулху (для утех)'] = DataItem(46, '🦑Ручной Ктулху (для утех)', 'Хлам', 0, 0, 0, 0)
Items['Огромный сундук'] = DataItem(47, '🧳Огромный сундук', 'Сундук', 2, 0, 0, 0)
Items['Бесплатная путёвка на свалку'] = DataItem(48, '🎟Бесплатная путёвка на свалку', 'Свиток', 1, 0, 0, 0)
Items['Ashot case'] = DataItem(49, '🧳Ashot case', 'Сундук', 1, 0, 0, 0)
Items['Сун-дук'] = DataItem(50, '🧳Сун-дук', 'Сундук', 1, 0, 0, 0)
Items['Осколок энергии'] = DataItem(51, '🔷Осколок энергии', 'Артефакт', 1, 0, 0, 0)
Items['Кольцо живости'] = DataItem(52, '💍Кольцо живости', 'Артефакт', 1, 0, 0, 0)
Items['Кепка адидас'] = DataItem(53, '🧢Кепка адидас', 'Броня', 1, 28, 0, 0)
Items['Ночнушка Раскуловой'] = DataItem(54, '👚Ночнушка Раскуловой', 'Броня', 2, 43, 0, 0)
Items['Штаны Ашодас'] = DataItem(55, '👖Штаны Ашодас', 'Броня', 1, 36, 0, 0)
Items['Туфельки Раскуловой'] = DataItem(56, '👠Туфельки Раскуловой', 'Броня', 1, 24, 0, 0)
Items['Положительный тест на беременность'] = DataItem(57, '🌡Положительный тест на беременность', 'Хлам', 1, 0, 0, 0)
Items['Отрицательный тест на беременность'] = DataItem(58, '🌡Отрицательный тест на беременность', 'Хлам', 1, 0, 0, 0)
Items['Детектор аномалий'] = DataItem(59, '📟Детектор аномалий', 'Хлам', 1, 0, 0, 0)
Items['Аптечка'] = DataItem(60, '🧳Аптечка', 'Сундук', 1, 0, 0, 0)
Items['Успокаивающее'] = DataItem(61, '💉Успокаивающее', 'Зелье', 0, 35, 0, 0)
Items['Колпак главврача'] = DataItem(62, '🧢Колпак главврача', 'Броня', 1, 15, 0, 0)
Items['Халат главрача'] = DataItem(63, '👕Халат главрача', 'Броня', 1, 24, 0, 0)
Items['Штаны главврача'] = DataItem(64, '👖Штаны главврача', 'Броня', 1, 21, 0, 0)
Items['Тапочки главврача'] = DataItem(65, '👟Тапочки главврача', 'Броня', 1, 18, 0, 0)
Items['Амфора экстренной помощи'] = DataItem(66, '🏺Амфора экстренной помощи', 'Сундук', 0, 0, 0, 0)
Items['Ашондук'] = DataItem(67, '🧳Ашондук', 'Сундук', 1, 0, 0, 0)
Items['Сундук щитоносцев'] = DataItem(68, '🧳Сундук щитоносцев', 'Сундук', 2, 0, 0, 0)
Items['Крышка от мусорника'] = DataItem(69, '🛡Крышка от мусорника', 'Броня', 3, 5, 0, 0)
Items['Покрышка со свалки'] = DataItem(70, '🛡Покрышка со свалки', 'Броня', 3, 10, 0, 0)
Items['Деревянный щит'] = DataItem(71, '🛡Деревянный щит', 'Броня', 3, 15, 0, 0)
Items['Щит охранника'] = DataItem(72, '🛡Щит охранника', 'Броня', 3, 20, 0, 0)
Items['Щит покорителя Шаи-Хулуда'] = DataItem(73, '🛡Щит покорителя Шаи-Хулуда', 'Броня', 3, 25, 0, 0)
Items['Железный щит'] = DataItem(74, '🛡Железный щит', 'Броня', 3, 0, 0, 0)
Items['Щит бомжа'] = DataItem(75, '🛡Щит бомжа', 'Броня', 3, 0, 0, 0)
Items['Золотая покрышка'] = DataItem(76, '🛡Золотая покрышка', 'Броня', 3, 0, 0, 0)
Items['Щит верности Раскуловой'] = DataItem(77, '🛡Щит верности Раскуловой', 'Броня', 3, 0, 0, 0)
Items['Первый сектор'] = DataItem(78, 'Телепорт в первый сектор', 'Олимп', 0, 0, 0, 0)
Items['Второй сектор'] = DataItem(79, 'Телепорт во второй сектор', 'Олимп', 0, 0, 0, 0)
Items['Третий сектор'] = DataItem(80, 'Телепорт в третий сектор', 'Олимп', 0, 0, 0, 0)
Items['Четвёртый сектор'] = DataItem(81, 'Телепорт в четвёртый сектор', 'Олимп', 0, 0, 0, 0)
Items['Пятый сектор'] = DataItem(82, 'Телепорт в пятый сектор', 'Донат', 0, 0, 0, 0)
Items['Плащ-невидимка'] = DataItem(83, '👘Плащ-невидимка', 'Артефакт', 1, 0, 0, 0)
Items['Багровая чешуя'] = DataItem(84, '🔻Багровая чешуя', 'Ивент-валюта', 0, 0, 0, 0)
Items['Первый заход в бар'] = DataItem(85, 'Первый заход в бар', 'Прочее', 0, 0, 0, 0)
Items['Первый заход в элитный бар'] = DataItem(86, 'Первый заход в элитный бар', 'Прочее', 0, 0, 0, 0)
Items['Осколок огня'] = DataItem(87, '🔥Осколок огня', 'Артефакт', 1, 0, 0, 0)
Items['Анализатор БМ'] = DataItem(88, '🚥Анализатор БМ', 'Артефакт', 1, 0, 0, 0)
Items['Анти-анализатор БМ'] = DataItem(89, '🚥Анти-анализатор БМ', 'Артефакт', 1, 0, 0, 0)
Items['Колючая маска'] = DataItem(90, '🧢Колючая маска ', 'Броня', 1, 41, 2, 0)
Items['Багровые поножи'] = DataItem(91, '👖Багровые поножи', 'Броня', 1, 50, 2, 0)
Items['Багровый жилет'] = DataItem(92, '🦺Багровый жилет', 'Броня', 2, 57, 2, 0)
Items['Ботинки с шипами'] = DataItem(93, '🥾Ботинки с шипами', 'Броня', 1, 37, 2, 0)
Items['Щит-крыло'] = DataItem(94, '🛡Щит-крыло', 'Броня', 3, 36, 0, 0)
Items['Яйца Ренанва'] = DataItem(95, '🏀Яйца Ренанва', 'Броня', 3, 36, 0, 0)
Items['Чешуйчатое снадобье'] = DataItem(96, '🧫Чешуйчатое снадобье', 'Зелье', 1, 0, 0, 0)
Items['Травяной чай'] = DataItem(97, '🍵Травяной чай', 'Зелье', 1, 0, 0, 0)
Items['Багровая бомба'] = DataItem(98, '🧨Багровая бомба', 'Экипировка', 1, 0, 0, 0)
Items['Билет на тот свет'] = DataItem(99, '🎟Билет на тот свет', 'Экипировка', 1, 0, 0, 0)
Items['Шаурма'] = DataItem(100, '🌯Шаурма', 'Еда', 1, 43, 0, 2)
Items['Двойная шаурма'] = DataItem(101, '🌯Двойная шаурма', 'Еда', 1, 85, 0, 1)
Items['Осколок секса'] = DataItem(102, '🔞Осколок секса', 'Хлам', 1, 0, 0, 0)
Items['Амулет оргазма'] = DataItem(103, '🧿Амулет оргазма', 'Хлам', 1, 0, 0, 0)
Items['Ивент инвентарь'] = DataItem(104, 'Ивент инвентарь', 'Ивент', 0, 0, 0, 0)
Items['Котелок'] = DataItem(105, '🥘Котелок', 'Экипировка', 2, 0, 0, 0)
Items['Бамбук для курения'] = DataItem(106, '🚬Бамбук для курения', 'Экипировка', 1, 0, 0, 0)
Items['Нижнее бельё Какушиготы'] = DataItem(107, '👙Нижнее бельё Какушиготы', 'Хлам', 0, 0, 0, 0)
Items['Treat'] = DataItem(108, '🍬Treat', 'Хеллоуин', 0, 0, 0, 0)
Items['Рецепт бамбук'] = DataItem(109, 'Рецепт бамбук', 'Рецепт', 0, 0, 0, 0)
Items['Рецепт бакин'] = DataItem(110, 'Рецепт бакин', 'Рецепт', 0, 0, 0, 0)
Items['Бакин'] = DataItem(111, '💊Бакин', 'Другое', 0, 0, 0, 0)
Items['Останки героев'] = DataItem(112, '🦴Останки героев', 'Растение', 0, 0, 0, 0)
Items['Рецепт героИн'] = DataItem(113, 'Рецепт героИн', 'Рецепт', 0, 0, 0, 0)
Items['ГероИн'] = DataItem(114, '🗞ГероИн', 'Другое', 1, 0, 0, 0)
Items['Снунец'] = DataItem(115, '🧊Снунец', 'Ивент-валюта', 0, 0, 0, 0)
Items['Дрова'] = DataItem(116, '🌳Дрова', 'Другое', 1, 0, 0, 0)
Items['Шапка-ушанка'] = DataItem(117, '🧢Шапка-ушанка', 'Броня', 1, 45, 3, 0)
Items['АШуба'] = DataItem(118, '🧥АШуба', 'Броня', 2, 60, 3, 0)
Items['Летние шорты'] = DataItem(119, '🩳Летние шорты', 'Броня', 1, 52, 3, 0)
Items['Зимние калоши'] = DataItem(120, '🥾Зимние калоши', 'Броня', 1, 45, 3, 0)
Items['Самонагревающаяся покрышка'] = DataItem(121, '🛡Самонагревающаяся покрышка', 'Броня', 3, 40, 0, 0)
Items['Погодный шар'] = DataItem(122, '🔮Погодный шар', 'Экипировка', 1, 0, 0, 0)
Items['Погодный шар 2.0'] = DataItem(123, '🔮Погодный шар 2.0', 'Экипировка', 1, 0, 0, 0)
Items['Настойка боярышника'] = DataItem(124, '🍶Настойка боярышника 90°', 'Зелье', 1, 0, 0, 0)
Items['Рецепт боярышник'] = DataItem(125, 'Рецепт боярышника', 'Рецепт', 0, 0, 0, 0)
Items['Рецепт ВиАгро'] = DataItem(126, 'Рецепт ВиАгро', 'Рецепт', 0, 0, 0, 0)
Items['ВиАгро'] = DataItem(127, '💊ВиАгро', 'Экипировка', 1, 0, 0, 0)
Items['Валентинка'] = DataItem(128, '💌Валентинка', 'Еда', 1, 100, 0, 0)
Items['Обломок синего камня'] = DataItem(129, '🔹Обломок синего камня', 'Прочее', 1, 0, 0, 0)
Items['Горная шапка'] = DataItem(130, '🧢Горная шапка', 'Броня', 1, 40, 0, 0)
Items['Жилет скалолаза'] = DataItem(131, '🦺Жилет скалолаза', 'Броня', 2, 55, 0, 0)
Items['Короткие шорты'] = DataItem(132, '🩳Короткие шорты', 'Броня', 1, 55, 0, 0)
Items['Горные кроссовки'] = DataItem(133, '👟Горные кроссовки', 'Броня', 1, 45, 0, 0)
Items['Чулки'] = DataItem(134, '🧦Чулки', 'Броня', 1, 75, 0, 0)
Items['Опустошенный сундук'] = DataItem(135, '🧳Опустошенный сундук', 'Сундук', 1, 0, 0, 0)
Items['Коробка с карточками'] = DataItem(136, '🧳Коробка с карточками', 'Донат', 0, 0, 0, 0)
Items['Камень энергии'] = DataItem(137, '🔷Камень энергии', 'Артефакт', 1, 0, 0, 0)
Items['Горшок лепрекона'] = DataItem(138, '🍯Горшок лепрекона', 'Артефакт', 1, 0, 0, 0)
Items['Карманная дриада'] = DataItem(139, '🌿Карманная дриада', 'Артефакт', 1, 0, 0, 0)
Items['Ситень'] = DataItem(140, '💧Сumень', 'Ивент-валюта', 0, 0, 0, 0)
Items['Дырявая лодка'] = DataItem(141, '🛶Дырявая лодка', 'Броня', 1, 65, 8, 0)
Items['Плавки'] = DataItem(142, '🩲Плавки', 'Броня', 1, 75, 8, 0)
Items['Купальник Раскуловой'] = DataItem(143, '🩱Купальник Раскуловой', 'Броня', 2, 90, 8, 0)
Items['Очки'] = DataItem(144, '🥽Очки', 'Броня', 1, 80, 8, 0)
Items['Полотенце'] = DataItem(145, '🧻Полотенце', 'Прочее', 1, 0, 0, 0)
Items['Кольцо всеотражения'] = DataItem(146, '💍Кольцо всеотражения', 'Артефакт', 1, 0, 0, 0)
Items['Рецепт паучий афродизиак'] = DataItem(147, 'Рецепт паучий афродизиак', 'Рецепт', 1, 0, 0, 0)
Items['Рецепт приготовления малого зелья восстановления'] = DataItem(148, 'Рецепт приготовления малого зелья восстановления', 'Рецепт', 1, 0, 0, 0)
Items['Рецепт приготовления среднего зелья восстановления'] = DataItem(149, 'Рецепт приготовления среднего зелья восстановления', 'Рецепт', 1, 0, 0, 0)
Items['Паучий афродизиак'] = DataItem(150, '🕸Паучий афродизиак', 'Прочее', 1, 0, 0, 0)
Items['Свиток башни'] = DataItem(151, '📜Свиток башни', 'Прочее', 0, 0, 0, 0)
Items['Документ DSFB-4'] = DataItem(152, '📜Документ DSFB-4', 'Сюжетка', 0, 0, 0, 0)
Items['Карта заброшенного архива'] = DataItem(153, '📜Карта заброшенного архива', 'Сюжетка', 0, 0, 0, 0)
Items['Палка-копалка'] = DataItem(154, '🎋Палка-копалка', 'Крафт', 1, 0, 0, 0)
Items['Камень обыкновенный'] = DataItem(155, '▫️Камень обыкновенный', 'Крафт', 1, 0, 0, 0)
Items['Кусок металлолома'] = DataItem(156, '🔩Кусок металлолома', 'Крафт', 1, 0, 0, 0)
Items['Айрис'] = DataItem(157, '🥀Айрис', 'Крафт', 1, 0, 0, 0)
Items['Каменный цветок'] = DataItem(158, '🌱Каменный цветок', 'Крафт', 1, 0, 0, 0)
Items['Ситенка'] = DataItem(159, '🧿Ситенка', 'Крафт', 1, 0, 0, 0)
Items['Камень Андриколь'] = DataItem(160, '▪️Камень Андриколь', 'Крафт', 1, 0, 0, 0)
Items['Рюмб'] = DataItem(161, '♦️Рюмб', 'Ивент-валюта', 0, 0, 0, 0)
Items['Письмо для Табернам'] = DataItem(162, '✉️Письмо для Табернам', 'Прочее', 0, 0, 0, 0)
Items['Письмо для Табервама'] = DataItem(163, '✉️Письмо для Табервама', 'Прочее', 0, 0, 0, 0)
Items['Шлем усиленный'] = DataItem(164, '⛑Шлем усиленный', 'Броня', 1, 65, 6, 0)
Items['Плащ-уящ'] = DataItem(165, '🧥Плащ-уящ', 'Броня', 2, 70, 6, 0)
Items['Шортики'] = DataItem(166, '🩳Шортики', 'Броня', 1, 60, 6, 0)
Items['Сталкерские ботинки'] = DataItem(167, '🥾Сталкерские ботинки', 'Броня', 1, 50, 6, 0)
Items['Схрон сталкера'] = DataItem(168, '🧳Схрон сталкера', 'Сундук', 1, 0, 0, 2)
Items['Хабарик'] = DataItem(169, 'Хабарик', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Телесные жидкости'] = DataItem(170, 'Телесные жидкости', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Филе рыбы'] = DataItem(171, 'Филе рыбы', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Лёд'] = DataItem(172, 'Лёд', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Борщевик'] = DataItem(173, 'Борщевик', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Прах'] = DataItem(174, 'Прах', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Драугрские приправы'] = DataItem(175, 'Драугрские приправы', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Перемерзший рис'] = DataItem(176, 'Перемерзший рис', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Пряность'] = DataItem(177, 'Пряность', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Соль'] = DataItem(178, 'Соль', 'Ингредиент готовки', 1, 0, 0, 24)
Items['Лук'] = DataItem(179, 'Лук', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Съедобный CUMень'] = DataItem(180, 'Съедобный CUMень', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Макароны'] = DataItem(181, 'Макароны', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Перо феникса'] = DataItem(182, 'Перо феникса', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Шуба селедки'] = DataItem(183, 'Шуба селедки', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Кровь (не твоя)'] = DataItem(184, 'Кровь (не твоя)', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Чернила'] = DataItem(185, 'Чернила', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Машинное масло'] = DataItem(186, 'Машинное масло', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Кошачья Пыльца'] = DataItem(187, 'Кошачья Пыльца', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Пот'] = DataItem(188, 'Пот', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Акула без шубы'] = DataItem(189, 'Акула без шубы', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Пинус'] = DataItem(190, 'Пинус', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Фиолетовость'] = DataItem(191, 'Фиолетовость', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Драконья чешуя'] = DataItem(192, 'Драконья чешуя', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Саня'] = DataItem(193, 'Саня', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Рак'] = DataItem(194, 'Рак', 'Особый ингредиент готовки', 1, 0, 0, 64)
Items['Пистолет с ножом'] = DataItem(195, '🗡Пистолет с ножом', 'Оружие', 5, 4, 0, 0)
Items['Копьё'] = DataItem(196, '🗡Копьё', 'Оружие', 5, 3, 0, 0)
Items['Меч'] = DataItem(197, '🗡Меч', 'Оружие', 5, 5, 0, 0)
Items['Катана'] = DataItem(198, '🗡Катана', 'Оружие', 5, 4, 0, 0)
Items['Кинжал вампира'] = DataItem(199, '🗡Кинжал вампира', 'Оружие', 5, 4, 0, 0)
Items['Странная заготовка'] = DataItem(200, '🔦Странная заготовка', 'Прочее', 0, 0, 0, 0)
Items['Нечто'] = DataItem(201, 'Нечто', 'Еда', 0, 35, 0, 86)
Items['Бульон курильщика'] = DataItem(202, '🍵Бульон курильщика', 'Еда', 0, 50, 0, 24)
Items['Идеальный бульон курильщика'] = DataItem(203, '🍵Идеальный бульон курильщика', 'Еда', 0, 100, 0, 48)
Items['Сашими'] = DataItem(204, '🐟Сашими', 'Еда', 0, 50, 0, 24)
Items['Идеальное сашими'] = DataItem(205, '🐟Идеальное сашими', 'Еда', 0, 100, 0, 48)
Items['Борщ'] = DataItem(206, '🧫Борщ', 'Еда', 0, 50, 0, 24)
Items['Идеальный борщ'] = DataItem(207, '🧫Идеальный борщ', 'Еда', 0, 100, 0, 48)
Items['Сила узбека'] = DataItem(208, '🍜Сила узбека', 'Еда', 0, 50, 0, 24)
Items['Идеальная сила узбека'] = DataItem(209, '🍜Идеальная сила узбека', 'Еда', 0, 100, 0, 48)
Items['Пряная рыба с луком'] = DataItem(210, '🐠Борщ', 'Еда', 0, 50, 0, 24)
Items['Идеальная пряная рыба с луком'] = DataItem(211, '🐠Идеальная пряная рыба с луком', 'Еда', 0, 100, 0, 48)
Items['Манты с сюрпризом'] = DataItem(212, '🥟Манты с сюрпризом', 'Еда', 0, 50, 0, 24)
Items['Идеальные манты с сюрпризом'] = DataItem(213, '🥟Идеальные манты с сюрпризом', 'Еда', 0, 100, 0, 48)
Items['Макарошки с кулером'] = DataItem(214, '🍝Макарошки с кулером', 'Еда', 0, 50, 0, 24)
Items['Идеальные макарошки с кулером'] = DataItem(215, '🍝Идеальные макарошки с кулером', 'Еда', 0, 100, 0, 48)
Items['Солевая сигарилла'] = DataItem(216, '🚬Солевая сигарилла', 'Еда', 0, 50, 0, 24)
Items['Идеальная солевая сигарилла'] = DataItem(217, '🚬Идеальная солевая сигарилла', 'Еда', 0, 100, 0, 48)
Items['Аль денте салат'] = DataItem(218, '🥗Аль денте салат', 'Еда', 0, 50, 0, 24)
Items['Идеальный аль денте салат'] = DataItem(219, '🥗Идеальный аль денте салат', 'Еда', 0, 100, 0, 48)
Items['Богатырский суп'] = DataItem(220, '🍜Богатырский суп', 'Еда', 0, 50, 0, 24)
Items['Идеальный богатырский суп'] = DataItem(221, '🍜Идеальный богатырский суп', 'Еда', 0, 100, 0, 48)
Items['Онигири'] = DataItem(222, '🍘Онигири', 'Еда', 0, 50, 0, 24)
Items['Идеальные онигири'] = DataItem(223, '🍘Идеальные онигири', 'Еда', 0, 100, 0, 48)
Items['Собственно в соку'] = DataItem(224, '🍛Собственно в соку', 'Еда', 0, 50, 0, 24)
Items['Идеальный собственно в соку'] = DataItem(225, '🍛Идеальный собственно в соку', 'Еда', 0, 100, 0, 48)
Items['Бумага'] = DataItem(226, '🗞Бумага', 'Прочее', 0, 0, 0, 0)
Items['Сиф'] = DataItem(227, '🥠Сиф', 'Легендарный ингредиент готовки', 1, 0, 0, 128)
Items['Водяной пистолет'] = DataItem(228, '🔫Водяной пистолет', 'Легендарный ингредиент готовки', 1, 0, 0, 128)
Items['Немного магии'] = DataItem(229, '✨Немного магии', 'Легендарный ингредиент готовки', 1, 0, 0, 128)
Items['Ты'] = DataItem(230, '🔹Ты', 'Легендарный ингредиент готовки', 1, 0, 0, 128)
Items['Подозрительная жидкость'] = DataItem(231, '🥛Подозрительная жидкость', 'Еда', 1, 50, 0, 24)
Items['Идеальная подозрительная жидкость'] = DataItem(232, '🥛Идеальная подозрительная жидкость', 'Еда', 1, 100, 0, 48)
Items['Зубная паста'] = DataItem(233, '🥫Зубная паста', 'Еда', 1, 50, 0, 24)
Items['Идеальная зубная паста'] = DataItem(234, '🥫Идеальная зубная паста', 'Еда', 1, 100, 0, 48)
Items['Слёзы Сани'] = DataItem(235, '💦Слёзы Сани', 'Еда', 1, 50, 0, 24)
Items['Идеальные слёзы Сани'] = DataItem(236, '💦Идеальные слёзы Сани', 'Еда', 1, 100, 0, 48)
Items['Жареный раком'] = DataItem(237, '🍌Жареный раком', 'Еда', 1, 50, 0, 24)
Items['Идеальный жареный раком'] = DataItem(238, '🍌Идеальный жареный раком', 'Еда', 1, 100, 0, 48)
Items['Ёмкость для жидкости'] = DataItem(239, '🍼Ёмкость для жидкости', 'Прочее', 0, 0, 0, 0)
Items['Зелье сопротивления холоду'] = DataItem(240, '🧪Зелье сопротивления холоду', 'Зелье', 1, 0, 0, 0)
Items['Зелье сопротивления влажности'] = DataItem(241, '🧪Зелье сопротивления влажности', 'Зелье', 1, 0, 0, 0)
Items['Зелье цепной молнии'] = DataItem(242, '🧪Зелье цепной молнии', 'Зелье', 1, 0, 0, 0)
Items['Сувенир с моря'] = DataItem(243, '🐚Cувенир с моря', 'Артефакт', 1, 0, 0, 0)
Items['Квинтэссенция камня'] = DataItem(244, '🗿Квинтэссенция камня', 'Артефакт', 1, 0, 0, 0)
Items['Палка ярости'] = DataItem(245, '🥢Палка ярости', 'Артефакт', 1, 0, 0, 0)
Items['Камень-металлолом'] = DataItem(246, '🥌Камень-металлолом', 'Артефакт', 1, 0, 0, 0)
Items['Простая удочка'] = DataItem(247, '🎣Простая удочка', 'Рыбалка', 1, 0, 0, 0)
Items['Непростая удочка'] = DataItem(248, '🎣Непростая удочка', 'Рыбалка', 1, 0, 0, 0)
Items['Очень непростая удочка'] = DataItem(249, '🎣Очень непростая удочка', 'Рыбалка', 1, 0, 0, 0)
Items['Весьма непростая удочка'] = DataItem(250, '🎣Весьма непростая удочка', 'Рыбалка', 1, 0, 0, 0)
Items['Частичка Вавилона'] = DataItem(251, '🍁Частичка Вавилона', 'Хлам', 0, 0, 0, 0)
Items['Шлем'] = DataItem(252, '🥽Шлем', 'Броня', 1, 95, 10, 0)
Items['Костюм химзащиты'] = DataItem(253, '👕Костюм химзащиты', 'Броня', 2, 110, 10, 0)
Items['Шортики 2.0'] = DataItem(254, '🩳Шортики 2.0', 'Броня', 1, 90, 10, 0)
Items['Противорадиационные ботинки'] = DataItem(255, '🥾Противорадиационные ботинки', 'Броня', 1, 85, 10, 0)
Items['Противогаз'] = DataItem(256, '🤿Противогаз', 'Экипировка', 1, 100, 0, 0)
Items['Фильтры'] = DataItem(257, '🕳Фильтры', 'Противогаз', 0, 5, 0, 0)
Items['Бустер'] = DataItem(258, '⚡️Бустер', 'Прочее', 0, 0, 0, 0)
Items['Карась'] = DataItem(259, '🐡Карась', 'Рыба', 1, 0, 0, 0)
Items['Бычок'] = DataItem(260, '🐡Бычок', 'Рыба', 1, 0, 0, 0)
Items['Окунь'] = DataItem(261, '🐡Окунь', 'Рыба', 1, 0, 0, 0)
Items['Тарань'] = DataItem(262, '🐡Тарань', 'Рыба', 1, 0, 0, 0)
Items['Сом'] = DataItem(263, '🐡Сом', 'Рыба', 1, 0, 0, 0)
Items['Судак'] = DataItem(264, '🐠Судак', 'Рыба', 1, 0, 0, 0)
Items['Язь'] = DataItem(265, '🐠Язь', 'Рыба', 1, 0, 0, 0)
Items['Щука'] = DataItem(266, '🐠Щука', 'Рыба', 1, 0, 0, 0)
Items['Пиранья'] = DataItem(267, '🐠Пиранья', 'Рыба', 1, 0, 0, 0)
Items['Сопа'] = DataItem(268, '🐠Сопа', 'Рыба', 1, 0, 0, 0)
Items['Красноперка'] = DataItem(269, '🐟Красноперка', 'Рыба', 1, 0, 0, 0)
Items['Осетр'] = DataItem(270, '🐟Осетр', 'Рыба', 1, 0, 0, 0)
Items['Форель'] = DataItem(271, '🐟Форель', 'Рыба', 1, 0, 0, 0)
Items['Лосось'] = DataItem(272, '🐟Лосось', 'Рыба', 1, 0, 0, 0)
Items['Конфетка'] = DataItem(273, '🍬Конфетка', 'Прочее', 0, 0, 0, 0)
Items['Гирлянда'] = DataItem(274, '🟣Гирлянда', 'Прочее', 0, 0, 0, 0)
Items['Хлопушка'] = DataItem(275, '🎉Хлопушка', 'Прочее', 1, 0, 0, 0)
Items['Осколок льда'] = DataItem(276, '🟦Осколок льда', 'Артефакт', 1, 0, 0, 0)
Items['Осколок эфира'] = DataItem(277, '🟧Осколок эфира', 'Артефакт', 1, 0, 0, 0)
Items['Кольт'] = DataItem(278, '🗡Кольт', 'Оружие', 5, 5, 0, 0)
Items['Золотой кольт'] = DataItem(278, '🗡Золотой кольт', 'Оружие', 5, 5, 0, 0)



 # Айди, имя, тип, размер, бонус, атк_блок, истекает



async def items(name, check, botItem=None):
    if botItem:
        if name in BotItems:
            _ = BotItems[name]
            name, Type, descr, size, bonus = _.name, _.type, _.descr, _.size, _.bonus
            return name, Type, descr, size, bonus
    if check=='check':
        print(name)
        try:
            _ = Items[name]
            name, Type, size, bonus, atk_block, expires = _.name, _.type, _.size, _.bonus, _.atk_block, _.expires
            return True 
        except:
            return False
    if name in Items:
        _ = Items[name]
        name, Type, size, bonus, atk_block, expires = _.name, _.type, _.size, _.bonus, _.atk_block, _.expires
        if not expires:
            expires = 0
        if not atk_block:
            atk_block = 0
        if Type != "Еда":
            if check == True: return name, size, bonus, atk_block, expires
            elif check == 'size': return size
            else: return Type, size, bonus, atk_block, expires
        else:
            if check == True: return name, size, bonus, atk_block, expires
            elif check == 'size': return size
            else: return Type, size, bonus, atk_block, expires

    else:
        print("Error. {}".format(name))
        name = False
        Type = False
        size = False
        bonus = False
        atk_block = False
        expires = False
        if check == True: return name, size, bonus, atk_block, expires
        elif check == 'size': return size
        else: return Type, size, bonus, atk_block, expires





async def specialItems(name, user):
    if name == '🎒Улучшенный рюкзак':
        user.inventorySizeMax = user.inventorySizeMax + 5
        await user.save()
        item = await Inventory.get(name='Улучшенный рюкзак', idplayer=user.id)
        item.active = 0
        await item.save()
    return


async def awardsForHome(user):
    randomStones = None
    randomWoods = None
    checkHome = await Houses.get_or_none(owner=user.id)
    if checkHome and checkHome.owner == user.id:
        randomGiving = random.randint(1, 100)
        if randomGiving > 80:
            if user.location == "Случайный лес":
                randomWoods = random.randint(1, 3)
                randomGiveStones = random.randint(1, 100)
                if randomGiveStones > 60:
                    randomStones = random.randint(1, 3)
            elif user.location == "Лесная гробница":
                randomWoods = random.randint(1, 4)
                randomStones = random.randint(1, 3)
            elif user.location == "Песчаная пирамида":
                randomStones = random.randint(1, 2)
            elif user.location == "Заснеженный лес":
                randomWoods = random.randint(1, 2)
                randomGiveStones = random.randint(1, 100)
                if randomGiveStones > 50:
                    randomStones = random.randint(1, 3)
            elif user.location == "Окус Локус":
                randomWoods = random.randint(1, 2)
                randomGiveStones = random.randint(1, 100)
                if randomGiveStones > 45:
                    randomStones = random.randint(1, 2)
            elif user.location in ["Свалка HD", "Свалка HR", "Свалка FL", "Свалка SR", "Свалка SR2"]:
                randomWoods = random.randint(1, 2)
                randomStones = random.randint(1, 3)
            text = ""
            if randomWoods:
                text += "\n\n+ {}🌳".format(randomWoods)
                checkHome.woods += randomWoods
            if randomStones:
                if randomWoods:
                    text += " {}🪨".format(randomStones)
                else:
                    text += "\n\n{}🪨".format(randomStones)
                checkHome.stones += randomStones
            await Houses.filter(id=checkHome.id).update(stones=checkHome.stones, woods=checkHome.woods)
        else:
            text = "None"
    else:
        text = "None"
    return text


async def dropArt(user, mob):
    return
    rand = random.randint(1, 100)
    if rand <= 50: lvl = 1
    elif rand <= 85: lvl = 2
    else: lvl = 3
    itemsdict = ['Палка-копалка', 'Камень обыкновенный', 'Кусок металлолома', 'Айрис', 'Каменный цветок', 'Ситенка', 'Камень Андриколь']
    randomItem = random.choice(itemsdict)
    newItem = await Inventory(name=randomItem, Type='Крафт', size=1, bonus=0, lvl=lvl, count=0, atk_block=0, active=5)
    await newItem.save()
    name, size, bonus, atk_block, expires = await items(randomItem, check=True)
    text = name
    return text




async def winnerIngForKitchen(mob, user):
    checkHome = await Houses.get_or_none(owner=user.id)
    itemToDrop = None
    text = ""
    if True:
        rand = random.randint(0, 100) # Обычные ингридиенты
        if user.location == 'Случайный лес' and rand <= 25:
            itemsForDrop = ['Хабарик', 'Борщевик']
            itemToDrop = random.choice(itemsForDrop)
            success = await addItem(itemToDrop, user)
        elif user.location == 'Окус Локус' and rand <= 25:
            itemsForDrop = ['Филе рыбы', 'Соль']
            itemToDrop = random.choice(itemsForDrop)
            success = await addItem(itemToDrop, user)
        elif user.location == 'Песчаная пирамида' and rand <= 25:
            itemsForDrop = ['Телесные жидкости', 'Прах']
            itemToDrop = random.choice(itemsForDrop)
            success = await addItem(itemToDrop, user)
        elif user.location == 'Заснеженный лес' and rand <= 25:
            itemsForDrop = ['Лёд', 'Перемерзший рис', 'Пряность']
            itemToDrop = random.choice(itemsForDrop)
            success = await addItem(itemToDrop, user)
        elif user.location == 'Лесная гробница' and rand <= 25:
            itemToDrop = 'Драугрские приправы'
            success = await addItem(itemToDrop, user)

        if itemToDrop and success == True:
            text += "\n{}".format(itemToDrop)
        elif itemToDrop and success == False:
            text += "\nВы нашли {}, но ваш инвентарь полон".format(itemToDrop)


    #                                                Особые ингридиенты


    unusualItemToDrop = None
    rand = random.randint(0, 100)
    if mob.name == '🏹Драугр с луком' and rand <= 10:
        unusualItemToDrop = 'Лук'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🌑Живая cumенная рыба' and rand <= 10:
        unusualItemToDrop = 'Съедобный CUMень'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🍝Макаронный монстр' and rand <= 10:
        unusualItemToDrop = 'Макароны'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🍝Макаронный монстр' and rand <= 10:
        unusualItemToDrop = 'Макароны'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🦆Феникс' and rand <= 10:
        unusualItemToDrop = 'Перо феникса'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🦟Москит улетающий' and rand <= 10:
        unusualItemToDrop = 'Кровь (не твоя)'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🚜Оптимус Прайм' and rand <= 10:
        unusualItemToDrop = 'Машинное масло'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🦈Акула в шубе' and rand <= 10:
        unusualItemToDrop = 'Акула без шубы'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🐙Эптаног' and rand <= 10 or user.location in ["Свалка HD", "Свалка HR", "Свалка FL"] and rand <= 30:
        unusualItemToDrop = 'Чернила'
        success = await addItem(unusualItemToDrop, user)
    #                                           РЕДКИЕ ИНГРИДИЕНТЫ
    elif mob.name == '🐟Селедка в шубе' and rand <= 5:
        unusualItemToDrop = 'Шуба селедки'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🐈КотоФея' and rand <= 5:
        unusualItemToDrop = 'Кошачья Пыльца'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '👨‍🔬Гарри Поттер' and rand <= 5:
        unusualItemToDrop = 'Пот'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🐡Рыбус-минус' and rand <= 5:
        unusualItemToDrop = 'Пинус'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '👿Фиолетовый драугр' and rand <= 5:
        unusualItemToDrop = 'Фиолетовость'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🐲Дракон' and rand <= 5:
        unusualItemToDrop = 'Драконья чешуя'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🛷Крампус' and rand <= 5:
        unusualItemToDrop = 'Саня'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🧙🏿‍♂️Рактомант' and rand <= 5:
        unusualItemToDrop = 'Рак'
        success = await addItem(unusualItemToDrop, user)
    
    elif mob.name == '🔹Ты🔹' and rand <= 10:
        unusualItemToDrop = 'Ты'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == ' 🎅Священный покоритель проституток' and rand <= 10:
        unusualItemToDrop = 'Сиф'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🔫Сатанаэль🔫' and rand <= 10:
        unusualItemToDrop = 'Водяной пистолет'
        success = await addItem(unusualItemToDrop, user)
    elif mob.name == '🔱ТритАнус🔱' and rand <= 10:
        unusualItemToDrop = 'Немного магии'
        success = await addItem(unusualItemToDrop, user)

    if unusualItemToDrop and success == True:
        text += "\n{}".format(unusualItemToDrop)
    elif unusualItemToDrop and success == False:
        text += "\nВы нашли {}, но ваш инвентарь полон".format(unusualItemToDrop)
    return text


async def winnerHeal(location):
    chance = random.randint(1, 100)
    if location == 'Пустыня':
        if chance <= 70:
            item = 'Малое зелье здоровья'
        elif chance > 70 and chance <= 95:
            item = 'Среднее зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Случайный лес':
        if chance <= 50:
            item = 'Малое зелье здоровья'
        elif chance < 50 and chance >= 75:
            item = 'Среднее зелье здоровья'
        elif chance < 75 and chance >= 85:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Свалка SR':
        if chance <= 35:
            item = "Свиток телепортации"
        elif chance < 35 and chance >= 50:
            item = 'Малое зелье здоровья'
        elif chance < 50 and chance >= 75:
            item = 'Среднее зелье здоровья'
        elif chance < 75 and chance >= 85:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    elif location == 'Большая свалка':
        if chance <= 30:
            item = 'Малое зелье здоровья'
        elif chance < 30 and chance >= 55:
            item = 'Среднее зелье здоровья'
        elif chance < 55 and chance >= 80:
            item = 'Большое зелье здоровья'
        else:
            item = 'Зелье восстановления'
    else:
        pass
    return item



async def questItems(idp, mob):
    if idp.questId == 1 and idp.questStatus == 1 and mob.name == '🐍Змея':
        rand = random.randint(1, 100)
        success = await addItem('Тушка питона', idp)
        if success == True:
            text = "\nНайдена тушка питона\n"
        else:
            text = "\nНайдена тушка питона, но вам некуда её взять. Вы прошли мимо\n"
        count = await Inventory.filter(name='Тушка питона', idplayer=idp.id, active=1).only('id').count()
        if count >= 3:
            text += "Ты собрал необходимое количество. Можно возвращаться.\n"
    elif idp.questId == 2 and idp.questStatus == 1 and mob.name == '🦅Ястреб':
        rand = random.randint(1, 100)
        if rand <= 70:
            success = await addItem('Перо ястреба', idp)
            if success == True:
                text = "\nВыдрано перо ястреба\n"
            else:
                text = "\nВы могли бы выдрать перо ястреба, но вам некуда его взять. Вы прошли мимо\n"
        elif rand > 70 and rand < 100:
            success = await addItem('Перо ястреба', idp)
            success = await addItem('Перо ястреба', idp)
            success = await addItem('Перо ястреба', idp)
            if success == True:
                text = "\nВыдрано 3 пера ястреба\n"
            else:
                text = "\nВы могли бы выдрать перо ястреба, но вам некуда его взять. Вы прошли мимо\n"
        else:
            text = ''
        count = await Inventory.filter(name='Перо ястреба', idplayer=idp.id, active=1).only('id').count()
        if count >= 5:
            text += "Ты собрал необходимое количество. Можно возвращаться.\n"

    else:
        text = ''
    return text


import telebot

closeLog = -1001305857653
async def winner(idp, location):
    token = ''
    tbot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)         
    sometext = ""
    player = await Users.get(id=idp.id)
    mob = await Monsters.get(id=idp.battleWith).first()
    text = await questItems(player, mob)
    sometext += text
    achm = await Ach.exists(user_id=idp.user_id)
    if achm:
        achm = await Ach.get(user_id=idp.user_id).first()
    else:
        achm = await Ach(user_id=user.user_id)
        await achm.save()
    z = achm.ubica.split("|")
    newProgress = int(z[0]) + 1
    achm.ubica = "{}|{}".format(newProgress, z[1])
    texttt = None
    if newProgress >= 500 and int(z[1]) == 0:
        ubica = "{}|1".format(newProgress)
        await Users.filter(id=player.id).update(money=F('money') + 500)
        texttt = '⚠️Получено достижение - "Убийца нечисти"\n+500💰'
    elif newProgress >= 2000 and int(z[1]) == 1:
        ubica = "{}|2".format(newProgress)
        await Users.filter(id=player.id).update(money=F('money') + 1000)
        texttt = '⚠️Получено достижение - "Уничтожитель нечисти"\n+1000💰'
    elif newProgress >= 5000 and int(z[1]) == 2:
        ubica = "{}|3".format(newProgress)
        await Users.filter(id=player.id).update(money=F('money') + 2000)
        texttt = '⚠️Получено достижение - "Потрошитель нечисти"\n+2000💰'
    elif newProgress >= 10000 and int(z[1]) == 3:
        ubica = "{}|4".format(newProgress)
        await Users.filter(id=player.id).update(money=F('money') + 10000)
        texttt = '⚠️Получено достижение - "Главный страх нечисти"\n+10000💰'
    elif newProgress >= 20000 and int(z[1]) == 4:
        ubica = "{}|5".format(newProgress)
        await Users.filter(id=player.id).update(money=F('money') + 20000)
        texttt = '⚠️Получено достижение - "Решатель проблем с нечистью"\n+20000💰'
    else:
        ubica = "{}|5".format(newProgress)
    await Ach.filter(user_id=player.user_id).update(ubica=ubica)
    if texttt:
        tbot.send_message(player.user_id, texttt)
    # await achm.save()
    # await player.save()
    await player.refresh_from_db(fields=['money'])
    checkHome = await Houses.get_or_none(owner=player.id)
    if player.booster > int(time.time()):
        mob.maxgold *= 1.15
        mob.maxexp *= 1.15
    if checkHome:
        mob.maxgold = (checkHome.plusGold / 100 + 1) * mob.maxgold
    if player.location == 'Свалка HD':
        mob.maxexp *= 1.2
        mob.maxgold *= 1.2
    elif player.location == 'Свалка HR':
        mob.maxexp *= 1.15
        mob.maxgold *= 1.15
    elif player.location == 'Свалка FL':
        mob.maxexp *= 1.1
        mob.maxgold *= 1.1
    elif player.location in ["Свалка SR", "Свалка SR2"]:
        mob.maxgold *= 0.8
        mob.maxexp *= 0.9
        if player.location == "Свалка SR":
            item = await winnerHeal(location)
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
    minexp = int(mob.maxexp * 0.7)
    mingold = int(mob.maxgold * 0.7)
    exp = random.randint(minexp, int(mob.maxexp))
    maxgold = mob.maxgold
    checkArtGold = await Inventory.get_or_none(name='Горшок лепрекона', active=2, idplayer=player.id)
    if checkArtGold:
        bonusGold = (checkArtGold.lvl * 3 - 3) / 100
        a = maxgold * 0.60 + bonusGold
        mingold = maxgold * 0.55 + bonusGold
        _gold = int(a)
        if player.psy == -10:
            gold = _gold * 2
        else:
            gold = _gold
    else:
        if player.psy == -10:
            _gold = random.randint(mingold, int(maxgold))
            gold = _gold * 2
        else:
            gold = random.randint(mingold, int(maxgold))
    await Users.filter(id=player.id).update(exp = F('exp') + exp)
    await player.refresh_from_db(fields=['exp'])
    if player.lvl < 100:
        _needExp = int(player.lvl / 2) * 25
        needExp = int(player.lvl * 150) + _needExp
    elif player.lvl < 200:
        needExp = int(player.lvl * 150) * (player.lvl / 50)
    else:
        needExp = int(player.lvl * 150) * (player.lvl / 15)
    randomItem = random.randint(1, 100)
    if location == 'Пустыня':
        if randomItem <= 8:
            _items = ['Бумажный бургер', 'Он называет это "яблоко"', 'Хер огра', 'Бывший сосед', 
                'Консервы из палеозоя', 'Бывший сосед(поджаренный)']
            item = random.choice(_items)
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 33 and randomItem <= 55:
            item = await winnerHeal(location)
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 10 and randomItem <= 17:
            item = 'Свиток телепортации'
            success = await addItem('Свиток телепортации', player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 17 and randomItem <= 32:
            item = 'Маленький сундучок'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        checkQuest = await Inventory.exists(name='Кошелёк падшего героя', idplayer=player.id)
        if not checkQuest and mob.name == '🍃Оживший оазис' and player.questId == 6 and player.questStatus == 1:
            await addItem('Кошелёк падшего героя', player, arg='1')
            sometext += "\nВозле трупа вы нашли кошелёк. Это оказался кошелёк человека о котором говорил охранник. Следует вернуться и отдать его."
    elif player.location == 'Случайный лес' or player.location == 'Лесная гробница':
        if randomItem <= 15:
            _items = ['Бумажный бургер', 'Он называет это "яблоко"', 'Бывший сосед', 'Консервы из палеозоя']
            item = random.choice(_items)
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 63 and randomItem <= 70:
            if player.lvl >= 15:
                _items = ['Бумага', 'Ёмкость для жидкости']
                item = random.choice(_items)
            else:
                item = 'Свиток телепортации'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 15 and randomItem <= 37:
            item = 'Огромный сундук'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 37 and randomItem <= 43:
            item = 'Кофе'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 51 and randomItem <= 56:
            item = 'Сундук щитоносцев'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 57 and randomItem <= 62:
            item = 'Ashot case'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон".format(name)
            else:
                sometext += "\n{}".format(name)
        if mob.name == '💅Депрессивная школьница':
            rand = random.randint(1, 100)
            if rand <= 25:
                success = await addItem('Положительный тест на беременность', player)
                name, size, bonus, atk_block, expires = await items('Положительный тест на беременность', check=True)
                if success == True:
                    sometext += "\n{}".format(name)
        rand = random.randint(0, 100)
        if rand < 20:
            player.heavenCurrency += 1
            sometext += "\n🔻Багровая чешуя"
        if player.location == 'Лесная гробница':
            rand = random.randint(1, 100)
            if rand >= 55:
                success = await addItem('Останки героев', player)
                if success == True:
                    sometext += "\n🦴Кости"
    elif player.location == 'Заснеженный лес':
        rand = random.randint(1, 100)
        randq = random.randint(2, 10)
        player.kawaiCurrency += randq
        sometext += "\nx{} 🧊Снунец".format(randq)
        item = None
        if rand <= 20: item = 'Кофе'
        elif rand <= 25: item = 'Бывший сосед(замороженный)'
        elif rand <= 40: item = 'Дрова'
        elif rand <= 45: item = 'Шкатулка Кефира'
        elif rand <= 60:
            _items = ['Бумага', 'Ёмкость для жидкости']
            item = random.choice(_items)
        if item:
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == True:
                sometext += "\n{}".format(name)
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон".format(name)
    elif player.location == "Туннели метро":
        if randomItem > 63 and randomItem <= 70:
            if player.lvl >= 15:
                _items = ['Бумага', 'Ёмкость для жидкости']
                item = random.choice(_items)
            else:
                item = 'Свиток телепортации'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 15 and randomItem <= 37:
            item = 'Фильтры'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 37 and randomItem <= 43:
            item = 'Кофе'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
            else:
                sometext += "\n{}".format(name)
        elif randomItem > 51 and randomItem <= 56:
            item = 'Сундук щитоносцев'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == False:
                sometext += "\nВы нашли {}, но ваш инвентарь полон".format(name)
            else:
                sometext += "\n{}".format(name)




    if mob.name == ' 🎅Священный покоритель проституток':
        await Inventory.create(name='Портал в Океанус', idplayer=player.id, size=0, bonus=0, active=0, type='Прочее')
        await Inventory.create(name='Портал в Радар1', idplayer=player.id, size=0, bonus=0, active=0, type='Прочее')
    elif mob.name == '🔹Ты🔹':
        await Inventory.create(name='Портал в Радар3', idplayer=player.id, size=0, bonus=0, active=0, type='Прочее')
    elif mob.name == '⚡️Индра (перерождённый)⚡️':
        await Inventory.create(name='Портал в Метро1', idplayer=player.id, size=0, bonus=0, active=0, type='Прочее')
    elif player.location == 'Логово сектантов':
        if mob.name == '🚑Главврач':
            success = await addItem('Аптечка', player)
            name, size, bonus, atk_block, expires = await items('Аптечка', check=True)
            if success == True:
                sometext += "\n" + name
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
    elif player.location == 'Песчаная пирамида' or player.location == 'Окус Локус':
        rand = random.randint(1, 100)
        if rand < 3:
            if player.lvl >= 15:
                _items = ['Бумага', 'Ёмкость для жидкости']
                item = random.choice(_items)
            else:
                item = 'Свиток телепортации'
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == True:
                sometext += "\n" + name
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
        elif rand < 25:
            success = await addItem('Хер огра', player)
            name, size, bonus, atk_block, expires = await items('Хер огра', check=True)
            if success == True:
                sometext += "\n" + name
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
        elif rand < 30:
            success = await addItem('Огромный сундук', player)
            name, size, bonus, atk_block, expires = await items('Огромный сундук', check=True)
            if success == True:
                sometext += "\n" + name
            else:
                sometext += "\nВы нашли {}, но ваш инвентарь полон.".format(name)
        if mob.name == '🦆Феникс':
            await Inventory.create(name='Первый сектор', idplayer=player.id, active=0, type='Олимп', size=0, bonus=0)
        if mob.name == '🦾Камеол (Целестиал)👁':
            await Inventory.create(name='Второй сектор', idplayer=player.id, active=0, type='Олимп', size=0, bonus=0)
        if mob.name == '🧖🏼Микаэль (целестиал)✝️':
            await Inventory.create(name='Третий сектор', idplayer=player.id, active=0, type='Олимп', size=0, bonus=0)
        if mob.name == '🔫Сатанаэль🔫' and player.scenario == 2 and player.scenarioStatus == 3:
            await Users.filter(id=player.id).update(scenarioStatus=4)
        rand = random.randint(1, 100)
        if rand < 15 and player.location != 'Окус Локус':
            player.heavenCurrency += 1
            sometext += "\n🔻Багровая чешуя"
    rand = random.randint(1, 100)
    if player.location != 'Песчаная пирамида':
        checkKotelok = await Inventory.exists(name='Котелок', idplayer=player.id, active=1)
        if checkKotelok:
            randomRasteniya = ['Одуванчик', 'Роза', 'RCA', 'Цветок сакуры']
            item = random.choice(randomRasteniya)
            checkArt = await Inventory.get_or_none(name='Карманная дриада', idplayer=player.id, active=2)
            if checkArt:
                rand = random.randint(0, 100)
                chance = checkArt.lvl * 5 - 5
                
                if rand <= chance:
                    if item == 'Одуванчик' and player.oduvanchik < player.kotelokLimit:
                        await Users.filter(id=player.id).update(oduvanchik = F('oduvanchik') + 3)
                        sometext += "\n3х 🌼Одуванчик"
                    elif item == 'Роза' and player.roza < player.kotelokLimit:
                        await Users.filter(id=player.id).update(roza = F('roza') + 3)
                        sometext += "\n3х 🌹Роза"
                    elif item == 'Цветок сакуры' and player.sakura < player.kotelokLimit:
                        await Users.filter(id=player.id).update(sakura = F('sakura') + 3)
                        sometext += "\n3х 🌸Цветок сакуры"
                    elif item == 'RCA' and player.rca < player.kotelokLimit:
                        await Users.filter(id=player.id).update(rca = F('rca') + 3)
                        sometext += "\n3х 🌷RCA"
                
                else:
                    if item == 'Одуванчик' and player.oduvanchik < player.kotelokLimit:
                        await Users.filter(id=player.id).update(oduvanchik = F('oduvanchik') + 2)
                        sometext += "\n2х 🌼Одуванчик"
                    elif item == 'Роза' and player.roza < player.kotelokLimit:
                        await Users.filter(id=player.id).update(roza = F('roza') + 2)
                        sometext += "\n2х 🌹Роза"
                    elif item == 'Цветок сакуры' and player.sakura < player.kotelokLimit:
                        await Users.filter(id=player.id).update(sakura = F('sakura') + 2)
                        sometext += "\n2х 🌸Цветок сакуры"
                    elif item == 'RCA' and player.rca < player.kotelokLimit:
                        await Users.filter(id=player.id).update(rca = F('rca') + 2)
                        sometext += "\n2х 🌷RCA"
            else:
                if item == 'Одуванчик' and player.oduvanchik < player.kotelokLimit:
                    await Users.filter(id=player.id).update(oduvanchik = F('oduvanchik') + 1)
                    sometext += "\n🌼Одуванчик"
                elif item == 'Роза' and player.roza < player.kotelokLimit:
                    await Users.filter(id=player.id).update(roza = F('roza') + 1)
                    sometext += "\n🌹Роза"
                elif item == 'Цветок сакуры' and player.sakura < player.kotelokLimit:
                    await Users.filter(id=player.id).update(sakura = F('sakura') + 1)
                    sometext += "\n🌸Цветок сакуры"
                elif item == 'RCA' and player.rca < player.kotelokLimit:
                    await Users.filter(id=player.id).update(rca = F('rca') + 1)
                    sometext += "\n🌷RCA"
        if rand < 20:
            randomEat = ['Малое зелье здоровья', 'Среднее зелье здоровья', 'Большое зелье здоровья', 'Малое зелье восстановления', 'Большой хер огра']
            item = random.choice(randomEat)
            success = await addItem(item, player)
            name, size, bonus, atk_block, expires = await items(item, check=True)
            if success == True: sometext += "\n" + name
            else: sometext += "\nВы нашли {}, но ваш инвентарь полон".format(name)
    if player.location == 'Окус Локус':
        rand = random.randint(0, 100)
        if rand <= 15:
            player.oceanCurrency += 1
            sometext += "\n💧Cumень"
    elif player.location == 'Туннели метро':
        rand = random.randint(0, 100)
        if rand <= 15:
            player.metroCurrency += 1
            sometext += "\n🗝Ключ"
    #plusText = await dropArt(player, mob)
    #sometext += plusText
    toText = await awardsForHome(player)
    if toText != "None": sometext += toText
    if player.quest == 'Убийца' and player.questStatus == 1:
        quest_to_update = await tempQuest.filter(user_id=player.user_id, quest=player.quest, status=0).first()
        await tempQuest.filter(id=quest_to_update.id).update(progress = F('progress') + 1)

    etherium = await Inventory.get_or_none(name='Осколок эфира', idplayer=player.id, active=2)
    if etherium:
        etherium.bonus += 1
        await etherium.save()
        ethBonus = int(etherium.bonus * (1.0 + (etherium.lvl * 0.5)))

        if ethBonus > int(player.hp / 2):
            ethBonus = int(player.hp / 2)

        player.nowhp += ethBonus
        if player.nowhp > player.hp:
            player.nowhp = player.hp
        else:
            sometext += f"\nОсколок эфира восстановил {ethBonus}❤️\n"


    bonusText = None
    if player.exp >= needExp:
        player.lvl += 1
        # player.exp = 0
        # player.nowhp = player.hp
        # player.eat = 100
        # player.energy = 100
        plusMoney = int(player.lvl * 50)
        # player.money += plusMoney

        await Users.filter(id=player.id).update(lvl = F('lvl') + 1,
                                                    exp = F('exp') - needExp,
                                                    energy=100,
                                                    nowhp = F('hp'),
                                                    eat=100,
                                                    money = F('money') + plusMoney,
                                                    uppts = F('uppts') + 1)
        await player.refresh_from_db()
        tbot.send_message(-1001317123616, "Игрок {} теперь {} уровня".format(player.username, player.lvl))
        sometext += "\n✨Вы получили новый уровень. Здоровье, энергия и сытость восстановлены.✨\n{}💰\n1🔘".format(plusMoney)
        if player.ref:
            refPlusMoney = player.lvl * 50
            await Users.filter(user_id=player.ref).update(money = F('money') + refPlusMoney)
            # refer.money += 500
            # await refer.save()
            try:
                tbot.send_message(refer.user_id, "Вы получили {}💰 за новый уровень вашего реферала {}!".format(refPlusMoney, player.username))
            except:
                pass
        if player.lvl == 2: bonusText = "\n⚠️Ого, ты получил свой первый 🔘Скиллпоинт. Использовать их можно и нужно в /skills"
        elif player.lvl == 5: bonusText = "\n⚠️Открыты трейды. Теперь ты можешь обмениваться с другими игроками!\nОткрыты ежедневные награды за посещение сайта toh.su !"
        elif player.lvl == 15: bonusText = "\n⚠️Открыт новый город: Кавайня!"
        elif player.lvl == 50: bonusText = "\n⚠️Открыт новый город: Океанус!"
        elif player.lvl == 100: bonusText = "\n⚠️Открыт новый город: Метро!"
        elif player.lvl == 25: bonusText = "\n⚠️Открыт доступ к экспедициям!"
        elif player.lvl == 35: bonusText = "\n⚠️Открыт новый город: Радар!"
        elif player.lvl == 7: bonusText = "\n⚠️Открыт доступ к охраннику в баре!"
        elif player.lvl == 75: bonusText = "\n⚠️Открыт доступ к созданию собственного клана!"
        elif player.lvl == 200: bonusText = "\n⚠️Открыт доступ к бесплатному созданию собственного клана!"
        if await Referals.exists(idplayer=player.id):
            await Referals.filter(idplayer=player.id).update(uppedLvls=F('uppedLvls') + 1)
        if player.quest == 'Уровнеподъёмщик' and player.questStatus == 1:
            quest = await db.tempQuest.get(user_id=player.user_id, quest=player.quest, status=0).first()
            quest.progress += 1
            await quest.save()


    # player.money = player.money + gold
    # player.battleStatus = 0
    plusText = await winnerIngForKitchen(mob, player)
    sometext += plusText
    if bonusText:
        sometext += bonusText
    await Users.filter(id=player.id).update(money = F('money') + gold, battleStatus=0, nowhp=player.nowhp, heavenCurrency=player.heavenCurrency, kawaiCurrency=player.kawaiCurrency, oceanCurrency=player.oceanCurrency, radarCurrency=player.radarCurrency, metroCurrency=player.metroCurrency)
    await player.refresh_from_db()
    await Inventory.filter(name='Странная заготовка', idplayer=player.id, active=1).update(bonus=F('bonus') + 1)
    checkSunday = await System.get(name='sunday')
    if checkSunday.value == 1 and player.frak not in ['', ' ', None]:
        rand = random.randint(0, 100)
        if rand <= 25 and player.location not in ["Свалка SR", "Свалка SR2"]:
            success = await addItem('Обломок синего камня', player)
            if success == True:
                sometext += "\n🔹Обломок синего камня"
            else:
                sometext += "\nВы нашли 🔹Обломок синего камня, но ваш инвентарь полон"
    droid = await Bot.get_or_none(idplayer=player.id, status__in=[1, 2]).first()
    if not droid:
        droid = await Bot.get_or_none(idplayer=player.id, status=0).first()
    if droid:

        rand = random.randint(1, 100)
        num = 20
        if player.location in ['Свалка HD', 'Свалка FL', 'Свалка HR']: num += 5
        chips = await BotInventory.filter(name__in=['Удача+', 'Удача++', 'Удача+++'], idbot=droid.id, active=2).only('name')
        for chip in chips:
            if chip.name == 'Удача+': num += 3
            elif chip.name == "Удача++": num += 6
            elif chip.name == "Удача+++": num += 9
        if rand <= num:
            expForBot = random.randint(1, 15)
            needExpForBot = droid.lvl * 1000
            if droid.exp + expForBot >= needExpForBot:
                await Bot.filter(id=droid.id).update(lvl=F('lvl') + 1, exp=F('exp') - needExpForBot)
                sometext += f"\nБот-00{droid.id}-{droid.model} получил новый уровень. Слоты памяти увеличены на 5📦"
            else:
                await Bot.filter(id=droid.id).update(exp=F('exp') + expForBot)
            await Bot.filter(id=droid.id).update(details=F('details') + 1)
            detailsList = ['Ржавая глыба', 'Погнутая пластина', 'Титановый сплав', 'Особый сплав', 'Сломанный ключ', 'Вытянутая катушка',
            'Сломанная схема', 'Сорванный винт', 'Новенький винт', 'Маленькая шестерня', 'Большая шестерня', 'Ржавый болт', 'Новенький болт',
            'Сломанная гайка', 'Новенькая гайка', 'Смятое гнездо', 'Прочное гнездо','Обрезок кабеля', 'Новенький кабель', 'Сломанная батарея',
            'Большая батарея', 'Простой механизм', 'Обычный механизм', 'Деталь усиления', 'Машинное масло', 'Присадочный металл', 'Ядро машины']
            detail = random.choice(detailsList)
            sometext += "\n🔧" + detail


    if await Referals.exists(idplayer=player.id):
        await Referals.filter(idplayer=player.id).update(killedMobs=F('killedMobs') + 1)

    return gold, exp, sometext
