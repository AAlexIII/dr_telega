#!/usr/bin/python
# coding: utf-8
import pymongo
from bot import *
import pprint
from copy import copy
from PIL import Image, ImageDraw, ImageFont

good = {'1': {'klav': {'Отклонить вызов': '42', 'Принять вызов': '2'},
              'photo': '1.png',
              'text': 'Слыша где-то вдалеке раздражающую мелодию звонка, вы сонно '
                      'открываете глаза, протягивая руку к телефону рядом.\n- Ох, что '
                      'вчера было… или даже не вчера… Башка раскалывается… Да кто '
                      'это, черт побери, трезвонит в такую рань… Ещё и номер '
                      'незнакомый…'},
        '2': {'klav': {'Эм... что? Вы кто?': '3'},
              'photo': '2.jpg',
              'text': 'Привет. Сегодня в 11 в банке, все готово?'},
        '3': {'klav': {'Идти собираться ': '4'},
              'photo': '4.jpg',
              'text': '- «Звонок завершен»… Странно… Ладно… ё-моё… 10 утра… Какое '
                      'сегодня число? Что?! 4 декабря?! Сегодня же в универ… Ладно, '
                      'еще к третьей успеваю. А мне ведь тоже в банк надо, айсик '
                      'перестал работать, нужно будет заскочить, разобраться, если '
                      'успею, – думаете вы.'},
        '4': {'klav': {'А кто это там?': '5'}, 'photo': '5.jpg', 'text': 'Эх, свежо.'},
        '5': {'klav': {'Поздороваться': '6', 'Пойти дальше': '27'},
              'photo': '6.png',
              'text': 'А там, похоже, Катя. Может, подойти и поздороваться? Время '
                      'еще есть…'},
        '6': {'klav': {'Погнали, там недалеко кафе есть': '7',
                       'Сори, как-нибудь в следующий раз': '27'},
              'photo': '7.jpg',
              'text': ' - Катя! Хэй, привет, давно не виделись!\n - Ого, какие люди! Да, '
                      'давно не виделись, как ты? Учишься где-то?\n - А, да, в СПбГЭУ. '
                      '\n - Как? Ты же в ИТМО хотел?!\n - Да там долгая история... \n - Так '
                      'давай посидим где-нибудь, расскажешь?'},
        '7': {'klav': {'Всё так': '8', 'Нет, вы меня слушали?': '8'},
              'photo': '8.png',
              'text': 'Итак ваш заказ: картошка и морковка. Верно?'},
        '8': {'klav': {'ЧТО': '9'},
              'photo': '9.png',
              'text': 'Вам принесли заказ. Оживленно беседуя с другом о жизни, вы '
                      'внезапно замечаете, что его лицо краснеет и распухает.'},
        '9': {'klav': {'Вызвать скорую': '10'},
              'photo': '',
              'text': 'Откуда тут оррреххх???'},

        '10': {'klav': {'Удобно с мигалками': '11'},
               'photo': '10.jpg',
               'text': 'Секунда и вы мчитесь на скорой.'},
        '11': {'klav': {'Какие новости?': '12'},
               'photo': '11.jpg',
               'text': 'Уже почти полчаса сидите и ждёте новостей, думая о том, как бы не опоздать '
                       'в универ, но вроде это уважительная причи.. Тут неожиданно '
                       'выскакивает врач'},
        '12': {'klav': {'Что вы делаете?': '13'},
               'photo': '12.png',
               'text': 'Вы замечаете, что халат врача весь в крови. Не отвечая на '
                       'ваши вопросы, обсыпает вас какой-то пыльцой или блестками.'},
        '13': {'klav': {'Присесть': '14'},
               'photo': '',
               'text': 'Вы чувствуете что-то необычное на голове.'},
        '14': {'klav': {'Бежать': '15', 'Ждать': '22'},
               'photo': '14.png',
               'text': 'Кровавый доктор достал из кармана огромный нож и подходит '
                       'ближе'},
        '15': {'klav': {'Зачёт по физ-ре заслужил': '16'},
               'photo': '15.png',
               'text': 'Алый врач выстреливает клыкастой змеей, но промахивается. Вам '
                       'удается убежать.'},
        '16': {'klav': {'Нужно поменьше играть на ночь': '17'},
               'photo': '16.png',
               'text': 'Уже в метро, спускаясь на эскалаторе, вы задумались о '
                       'произошедшем.'},
        '17': {'klav': {'Обернутся': '18'},
               'photo': '20.png',
               'text': 'Выйдя из метро, вы чувствуете на себе чей-то внимательный '
                       'взгляд..'},
        '18': {'klav': {'Ой, милые киси 🧡': '19'},
               'photo': '',
               'text': 'Немного посмотрев по сторонам, вы заметили двух кошек, '
                       'разглядывающих вас'},
        '19': {'klav': {'Поспешить': '20'},
               'photo': '',
               'text': 'Но что-то не так. Но боясь опоздать, вы отправляетесь в '
                       'университет…'},

        '20': {'klav': {'Опять бежать': '21'},
               'photo': '',
               'text': 'По пути вы видите на пути милое существо. Опять кошка? '
                       'Обернувшись, вы замечаете еще несколько «преследователей» '
                       'позади. Вы ускоряете шаг, но животные не отстают.'},
        '21': {'klav': {'Конец?': '100'},
               'photo': '',
               'text': 'Остаток пути до университета преодолеваете бегом, так как '
                       'семейство кошачьих в количестве около 10-20 особей бежало за '
                       'вами и пыталась наброситься на спину.'},
        '22': {'klav': {'Спокойно следить': '23'},
               'photo': '13.png',
               'text': 'Алый врач подошел, срезал у вас с головы гриб, положил его во '
                       'взявшийся из ниоткуда котелок с варевом на стойке медсестер, '
                       'помешал половником и отлил немного варева в миску'},
        '23': {'klav': {'Выглядит не очень': '24'},
               'photo': '22.png',
               'text': '- На, попробуй – доктор протянул вам миску с супом'},
        '24': {'klav': {'Выпить': '25'},
               'photo': '23.png',
               'text': '- А, тебя вид моего халата пугает, - доктор улыбнулся, будто '
                       'это что-то действительно забавное, - у нас тут ремонт, краска '
                       'упала. А лекарство от нового вируса выпить нужно.'},
        '25': {'klav': {'Выйти': '26'},
               'photo': '',
               'text': 'Обдумывая произошедшее, вы не заметили, как сели в троллейбус '
                       'и доехали до университета'},
        '26': {'klav': {'По набережной Грибоедова': '62.1', 'Через Думскую': '62'},
               'photo': '51.jpg',
               'text': 'От троллейбусной остановки до ворот университета можно дойти '
                       '2 способами, какой выбрать?'},
        '26.1': {'klav': {'По набережной Грибоедова': '62.2', 'Через Думскую': '62'},
                 'photo': '25.jpg',
                 'text': 'От метро до ворот университета можно дойти '
                         '2 способами, какой выбрать?'},
        '27': {'klav': {'Идти в банк': '28'}, 'photo': '', 'text': 'Ещё увидимся.'},
        '28': {'klav': {'Что за чудеса?': '29'},
               'photo': '',
               'text': 'Зайдя в банк, вы сразу подходите к окну с сидящей там '
                       'сотрудницей'},
        '29': {'klav': {'А я думал так просто всё': '30'},
               'photo': '27.png',
               'text': 'Все происходит так быстро. Несколько  полноватых мужчин в '
                       'масках и черной одежде неожиданно скидывают капюшоны, достают '
                       'пистолеты, вырубают охранника и начинают кричать:\n- Все! Ни '
                       'с места! Это ограбление!\n- Эй, ты! Ты пойдешь с нами! '
                       'Доставай ключи!'},

        '30': {
            'klav': {'Подождать, пока грабители подойдут ближе и набросится на того, что с пистолетом': '31',
                     'Тихо ждать дальнейшего развития событий': '33'},
            'photo': '28.jpg',
            'text': 'Трое грабителей подходят к сотруднице из окна (один из них '
                    'направляет на нее пистолет)'},
        '31': {'klav': {'Говорили, геройствовать не надо!': '32'},
               'photo': '29.jpg',
               'text': 'Вы храбро🧡 бросились на преступников, но один из них выстрелил '
                       'несколько раз вам в грудь, и вы скоротечно стали трупом'},
        '32': {'klav': {'Конец?': '100'},
               'photo': '30.png',
               'text': 'Вы добрались до университета, правда теперь вас никто не '
                       'замечает, конечно, кто сможет заметить бестелесного духа '
                       'несчастного студента'},
        '33': {'klav': {'Почему именно сейчас?': '33.1'},
               'photo': '32.jpg',
               'text': 'Внезапно у вас зазвонил телефон'},
'33.1': {'klav': {'Прощаться': '34'},
               'photo': '33.jpg',
               'text': 'Грабитель направляет на вас пистолет'},
        '34': {'klav': {'Диско?': '35'},
               'photo': '34.jpg',
               'text': ' музыка, суровые грабители срывают с себя '
                       'одежду (теперь они в трико) и начинают танцевать'},
        '35': {'klav': {'Теперь всё в норме': '36'},
               'photo': '36.png',
               'text': 'Также внезапно врываются полицейские, грабители застыли'},
        '36': {'klav': {'Ааааааааааа': '37'},
               'photo': '35.png',
               'text': 'Полицейские тоже начинают танцевать, мигалки сверкают в '
                       'такт музыке, сирены только зазывают в танец'},
        '37': {'klav': {'Пуститься в пляс': '38'},
               'photo': '',
               'text': 'Теперь атмосфера🧡 стала максимально танцевальной'},
        '38': {'klav': {'А я откуда знаю?': '39'},
               'photo': '38.jpg',
               'text': 'Спустя некоторое время вы уже сидите в качестве свидетеля в '
                       'кабинете следователя, полицейские не могут найти только '
                       'информатора грабителей'},
        '39': {'klav': {'Молчать': '1', 'Рассказать об этом следователю': '40'},
               'photo': '',
               'text': 'Вы вспоминаете про утренний звонок и думаете, что следователя '
                       'это может заинтересовать'},

        '40': {'klav': {'Конец?': '100'},
               'photo': '39.jpg',
               'text': 'Вы рассказываете о звонке детективу, показываете ему номер, с '
                       'которого вам утром позвонили, после чего следователь путем '
                       'умозаключений догадывается, что один из сотрудников банка, '
                       'который сейчас ждет опроса как свидетель, и есть информатор, '
                       'в знак благодарности за помощь в поимке преступника детектив '
                       'соглашается подвезти до университета '},
        '41': {'klav': {'Конец?': '100'},
               'photo': '',
               'text': 'Вы промолчали о звонке утром, через несколько минут вас '
                       'отпустили из участка, вы сели на трамвай и поехали в '
                       'университет с угрызениями совести'},
        '42': {'klav': {'Бежать собираться': '43'},
               'photo': '4.jpg',
               'text': 'Ё моё… 10 утра… Какое сегодня число? Что?! 4 декабря?! '
                       'Сегодня же в универ… Ладно, еще к третьей успеваю'},
        '43': {'klav': {'Идти к остановке маршрутки': '55',
                        'Идти к станции метро': '44'},
               'photo': '',
               'text': 'Эх, свежо'},
        '44': {'klav': {'Да как это возможно?': '45'},
               'photo': '',
               'text': 'Вы решаете снять денег. Девушка перед вами роняет карту на пол'},
        '45': {'klav': {'Что это?': '46'},
               'photo': '42.png',
               'text': 'Девушка поднимает карту, а вы замечаете у нее хвостик'},
        '46': {'klav': {'В каком смысле хвост?': '47'},
               'photo': '43.jpg',
               'text': 'Хвост, что же еще?'},
        '47': {'klav': {'Я действительно долго спал...': '48'},
               'photo': '',
               'text': 'Вы что! Такие вопросы задаете, будто вчера только '
                       'проснулись...'},
        '48': {'klav': {'Серьезно?': '49'},
               'photo': '',
               'text': 'Это вирус этот, эволюционировал и теперь зараженные в енотов '
                       'превращаются'},
        '49': {'klav': {'Уйти подальше': '50'},
               'photo': '',
               'text': 'Молодой человек!'},

        '50': {'klav': {'Какое странное утро': '51'},
               'photo': '17.png',
               'text': 'Садясь в вагон метро, вы задумались о произошедшем.'},
        '51': {'klav': {'Наверное новый подкаст': '52'},
               'photo': '',
               'text': 'Вы едете вагоне, думая о своём. Внезапно у всех пассажиров на '
                       'экранах телефонов появляется видеоролик, от чего они '
                       'перестают двигаться'},
        '52': {'klav': {'Бежать': '54', 'Кривляться': '53'},
               'photo': '44.png',
               'text': 'Вагон метро постепенно останавливается, в поезд заходит банда '
                       'енотов, они проходят между людьми, срывают их маски и '
                       'прыскают чем-то в лицо каждому, после брызг все быстро '
                       'превращаются в енотов'},
        '53': {'klav': {'Выйти из метро': '26.1'},
               'photo': '19.jpg',
               'text': 'Банда енотов не заметила вас и через 2 минуты ушла, '
                       'поезд метро продолжил движение'},
        '54': {'klav': {'Я енот?': '71'},
               'photo': '',
               'text': 'Банда енотов заметила вас, куда от них убежишь. Вас схватили '
                       'и превратили в енота🧡'},
        '55': {'klav': {'Обычная поездка': '56'},
               'photo': '',
               'text': 'Дождавшись маршрутку. Вы спокойно едете. Смотрите на людей, '
                       'многие с лишним весом, другие курят и чихают, кто-то ест '
                       'чипсы'},
        '56': {'klav': {'Вот это сервис': '57'},
               'photo': '',
               'text': 'Если бы. Машину потряхивает, и она взлетает. Не успев понять, '
                       'что происходит. Машина падает на крышу соседнего с '
                       'университетом здания'},
        '57': {'klav': {'Выбраться через окно': '58'},
               'photo': '',
               'text': 'Тут в дверь пробивается огромный клюв, все паникуют'},
        '58': {'klav': {'Это гигантское гнездо': '59'},
               'photo': '',
               'text': 'Вы на свободе, смотрите вокруг. Похоже… похоже..'},
        '59': {'klav': {'Ребят, а вы разве не вымерли...?': '60'},
               'photo': '',
               'text': 'Аккуратно, не задев яиц, герой выбирается из гнезда, но его '
                       'тут же встречает силуэт птеродактиля'},
        '60': {'klav': {'Пора бежать': '61'},
               'photo': '',
               'text': 'Ты прав, но ваш род со всеми этими привычками, такими как '
                       'злоупотребление алкоголем, энергетиками и вредной едой, '
                       'курение и отсутствие необходимых физических нагрузок, как '
                       'никогда близки к вымиранию. Так что мы пришли к вам на '
                       'замену'},
        '61': {'klav': {'С таким-то дневником самоконтроля': '68'},
               'photo': '',
               'text': 'Птеродактиль пытается схватить и съесть вас, но вы успеваете '
                       'убежать'},
        '62.1': {'klav': {'Заступиться': '63', 'Пройти мимо': '67'},
                 'photo': '47.jpg',
                 'text': 'Хороший выбор. Несколько «темная» улица, похоже вы ошиблись стороной.'
                         ' Идя по ней, вы замечаете, хулиганы '
                         'пристают к парню из-за его внешнего вида.'},
        '62.2': {'klav': {'Заступиться': '63', 'Пройти мимо': '67'},
                 'photo': '47.jpg',
                 'text': 'Хороший выбор, но выбрали не тот выход метро. Несколько «темная» улица.'
                         ' Идя по ней, вы замечаете, хулиганы '
                         'пристают к парню из-за его внешнего вида.'},
        '62': {'klav': {'Заступиться': '63', 'Пройти мимо': '67'},
               'photo': '47.jpg',
               'text': 'Несколько «темная» улица. Идя по ней, вы замечаете, хулиганы '
                       'пристают к парню из-за его внешнего вида.'},
        '63': {'klav': {'Не то чтобы …': '64'},
               'photo': '48.jpg',
               'text': 'Хулиганов несколько и теперь смотрят они смотрят на вас\n- '
                       'Ты че, самый умный, да? Нарываешься?'},
        '64': {'klav': {'Вот сила слов!': '65'},
               'photo': '49.1.png',
               'text': 'Неожиданно для вас все хулиганы начали дрожать от страха и '
                       'постепенно отступать'},
        '65': {'klav': {'Ты кто?': '66'},
               'photo': '50.jpg',
               'text': 'Вы оборачиваетесь посмотреть за направлением взглядов '
                       'хулиганов, и видите огромного крылатого льва'},
        '66': {'klav': {'Конец?': '100'},
               'photo': '',
               'text': 'Лев рассказывает, что почуял храбрость🧡 и прилетел с '
                       'Банковского моста, чтобы помочь вам, также, в награду за '
                       'героизм он довозит вас до ворот университета, а после '
                       'возвращается на свой постамент.'},
        '67': {'klav': {'Конец?': '100'},
               'photo': '',
               'text': 'Вы проходите мимо хулиганов, но тут же велосипедист проезжает '
                       'рядом с вами. Вы еле успели отскочить, но не совсем удачно, '
                       'поскользнулись и упали в лужу. Салфеток не оказалось, поэтому '
                       'в университет пришлось идти грязным.'},
        '68': {'klav': {'Послушать': '70', 'Рассеять': '69'},
               'photo': '',
               'text': 'Вас начинают тревожить странные мысли'},
        '69': {'klav': {'Конец?': '100'},
               'photo': '',
               'text': 'Взбредёт же в голову! Вы удачно спускаетесь с крыши и '
                       'подходите к зданию университета'},
        '70': {'klav': {'Начать сначала': '1'},
               'photo': '',
               'text': 'Вы слушаете голос в голове. Возвращаетесь к странной птице и '
                       'заявляете, что у ваших рас есть возможность существовать '
                       'вместе, что только благодаря вашему союзу вы сможете долго '
                       'процветать. После чего забираетесь на крылатое существо и '
                       'летите прямо к медикам, помогаете им вылечить всех больных. '
                       'Вы начинаете активную политическую карьеру, пропагандируете '
                       'бережное отношение к себе и окружающим, вы популярны и '
                       'получаете всё, о чём можно мечтать. Но до университета вы не '
                       'добрались. Вы проиграли'},
        '71': {'klav': {'(пытаешься что-то сказать, но ты енот)': '72'},
               'photo': '',
               'text': 'Да-да, ты енот. Привыкай.\n\nХотя не понятно, почему у тебя '
                       'сохранилось сознание? Именно его засекли учёные, которые '
                       'только что ворвались в вагон. Пока один из них отвлекал всех '
                       'едой. Человек в синей маске и халате подошёл к вам'},
        '72': {'klav': {'Офигевать от происходящего': '1'},
               'photo': '',
               'text': 'Времени нет, только ты сумел сохранить рассудок, значит '
                       'сможешь выдержать перегрузку. Мы отправим тебя в начало дня. '
                       'Чтобы спасти всех тебе просто нужно открыть дверь '
                       'университета. Мы верим в тебя'},

        '100': {'klav': {'Вспомнить': '101'},
                'photo': '',
                'text': 'Вы открываете дверь университета и ваши глаза\nВот это сон! '
                        ''},
        '101': {'klav': {},
                'photo': '',
                'text': 'УРА! Спасибо, что сыграли в нашу игру!\n\n'
                        'Если вы захотите поздравить нас с ДР, отправьте '
                        'граффити подарка в сообщения группы https://vk.com/ssfipm\n'
                        'Также нам будет приятно, если вы напишите впечатления по игре туда же\n\n'
                        'Вы можете попробовать найти все 5 оранжевых сердец в различных ветках истории '
                        'быстрее остальных\n'
                        'Для этого очистите историю и нажмите старт\n'
                        'Или введите введите /start'}, }


@bot.callback_query_handler(func=lambda call: True)
def reaction(call):
    c = call.data
    who = call.message.chat.id
    mes = call.message
    q = call.from_user.username
    bot.delete_message(who,mes)
    print(f"От: @{q} запрос {c}")
    if c == '54':
        send_m(662587491, f'@{q}\n{who}\nПервое сердце')
    elif c == '32':
        send_m(662587491, f'@{q}\n{who}\nВторое сердце')
    elif c == '37':
        send_m(662587491, f'@{q}\n{who}\nТретье сердце')
    elif c == '66':
        send_m(662587491, f'@{q}\n{who}\nЧетвертое сердце')
    elif c == '18':
        send_m(662587491, f'@{q}\n{who}\nПятое сердце')
    if good[c]['photo']:
        send_ph(who,'foto/'+good[c]['photo'])
    sm(who, good[c]['text'], good[c]['klav'])
    bot.answer_callback_query(call.id)


@bot.message_handler(commands=['start'])
def start(message):
    who = message.chat.id
    send_m(662587491, '@' + str(message.chat.username))
    sm(who, """Привет
Это небольшое и,мы надеемся, забавное приключение ко Дню Рождения ФИПМ

Мы спрятали 5 сердец. Первые, кто найдёт их все, получат призы
По этому вопросу обращайтесь к @gasadaser""", {'Начать': '1'})


@bot.message_handler(content_types=['text'])
def send_mes(message):
    who = message.chat.id
    send_m(who, 'Привет, нажми /start для начала приключения, по вопросам пиши @gasadaser')


while 1:
    print('go')
    bot.polling(none_stop=True)
    """db.user.find_one({'id': who})
    db.user.delete_many({'id': who})
    db.user.insert_one({'id': who, 'email': 'нет', 'send': None})"""
