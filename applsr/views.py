from django.http import HttpResponse
import random
from datetime import datetime, timedelta, time
import types

from django.http import HttpResponse
from django.template import loader

from applsr.models import Character
from applsr.models import Masterword
from applsr.models import DiceRoll
from applsr.models import Viking
from django.db.models import Q



def mj_viking(request):
    template = loader.get_template('applsr/mj_viking.html')
    context = {

    }
    return HttpResponse((template.render(context, request)))

# Create your views here.
def viking(request, nom):
    template = loader.get_template('applsr/viking.html')

    char = Viking.objects.filter(name=nom)
    context = {
        'car': char[0],
    }
    return HttpResponse(template.render(context, request))


def lancer_viking_duel(request, nom):
    dices = []
    success = 0
    dices_string = ""+nom.capitalize()
    dices_string += " fait un <i>Jet de Duel</i>"
    dices_string += ":<br/>"

    nb = 1
    for i in range(0, nb):
        roll = random.randint(1, 6)
        if roll < 5:
            dices_string += " [ " + str(roll) + " ] "
        else:
            dices_string += " [ <b>" + str(roll) + "</b> ] "
        dices.append(roll)
        if roll == 5:
            success += 1
        elif roll == 6:
            success += 2
    result = {
        'dices': dices,
        'success': success,
    }

    if success == 0:
        dices_string += "<br/>mais n'obtient <b>aucune réussite</b>..."
    elif success == 1:
        dices_string += "<br/>et obtient <b>une réussite.</b>"
    else:
        dices_string += "<br/>et obtient <b>" + str(success) + " réussites grâce à son critique !</b>"

    now = datetime.now()
    dices_string = ""+str(now.hour+2)+":"+str(now.minute)+":"+str(now.second)+" - "+dices_string
    dice = DiceRoll(dices=dices_string, secret=False, lancer=nom)
    dice.save()
    return result


def lancer_viking(request, nom, action, malus, bonus):
    char = Viking.objects.filter(name=nom)
    more_dices = 0
    more_dices -= malus
    more_dices += bonus

    dice = ""
    if 'jet' == action:
        dice = dice_roll_viking(nom.capitalize(), 'J', malus, 0, 0, 0)
    if 'duel' == action:
        lancer_viking_duel(request, nom)
    if 'JCH' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JCH', char[0].charisme, more_dices, malus, bonus)
    if 'JCB' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JCB', char[0].combat, more_dices, malus, bonus)
    if 'JNV' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JNV', char[0].navigation, more_dices, malus, bonus)
    if 'JNT' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JNT', char[0].nature, more_dices, malus, bonus)
    if 'JMG' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JMG', char[0].magie, more_dices, malus, bonus)
    if 'JSV' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JSV', char[0].savoir, more_dices, malus, bonus)
    if 'JAG' == action:
        dice = dice_roll_viking(char[0].name.capitalize(), 'JAG', char[0].agriculture, more_dices, malus, bonus)
    return HttpResponse(dice)


def dice_roll_viking(car, test, nb, more_dices, mal, ben):
    dices = []
    success = 0
    dices_string = ""
    if mal > 0 or ben > 0:
        dices_string += "Avec "

    if mal == 1:
        dices_string += "une <i>malédiction</i>"
    elif mal > 1:
        dices_string += "" + str(mal) + " <i>malédictions</i>"

    if mal > 0 and ben > 0:
        dices_string += " et "

    if ben == 1:
        dices_string += "une <i>bénédiction</i>"
    elif ben > 1:
        dices_string += "" + str(ben) + " <i>bénédictions</i>"

    if mal > 0 or ben > 0:
        dices_string += ", "

    dices_string += "<b>" + car + "</b> "
    dices_string += "fait un <i>Jet "
    if test == 'JCH':
        dices_string += "de Charisme</i> "
    elif test == 'JAG':
        dices_string += "d\'Agriculture</i> "
    elif test == 'JCB':
        dices_string += "de Combat</i> "
    elif test == 'JMG':
        dices_string += "de Magie</i> "
    elif test == 'JSV':
        dices_string += "de Savoir</i> "
    elif test == 'JNV':
        dices_string += "de Navigation</i> "
    elif test == 'JNT':
        dices_string += "de Nature</i> "

    dices_string += ":<br/>"

    nb = nb + more_dices
    for i in range(0, nb):
        roll = random.randint(1, 6)
        if roll <5:
            dices_string += " [ " + str(roll) + " ] "
        else:
            dices_string += " [ <b>" + str(roll) + "</b> ] "
        dices.append(roll)
        if roll == 5:
            success += 1
        elif roll == 6:
            success += 1
    result = {
        'requete': test,
        'dices': dices,
        'success': success,
    }

    if success == 0:
        dices_string += "<br/>mais n'obtient <b>aucune réussite</b>..."
    elif success == 1:
        dices_string += "<br/>et obtient <b>une réussite</b>"
    else:
        dices_string += "<br/>et obtient <b>" + str(success) + " réussites</b>"

    dices_string += "."
    now = datetime.now()
    dices_string = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" - "+dices_string
    dice = DiceRoll(dices=dices_string, secret=False, lancer=car)
    dice.save()

    return result


def newviking(request, joueur, nom, role, agriculture, charisme, combat, magie, savoir, navigation, nature, point_de_vie_max):
    viking = Viking(joueur=joueur, name=nom, role=role, agriculture=agriculture, charisme=charisme, combat=combat, magie=magie, savoir=savoir, navigation=navigation, nature=nature, point_de_vie=point_de_vie_max, point_de_vie_max=point_de_vie_max, point_de_pouvoir=0)
    viking.save()
    return HttpResponse("")


def updateviking(request, nom, agriculture, charisme, combat, magie, savoir, navigation, nature, point_de_vie_max):
    char = Viking.objects.filter(name=nom)
    char.update(agriculture=agriculture)
    char.update(charisme=charisme)
    char.update(combat=combat)
    char.update(magie=magie)
    char.update(savoir=savoir)
    char.update(navigation=navigation)
    char.update(nature=nature)
    char.update(point_de_vie_max=point_de_vie_max)

    return HttpResponse("")


def modifs_valeurs_viking2(request, nom, stat, valeur, add):
    char = Viking.objects.filter(joueur=nom)
    modifs_valeurs_viking(request, char[0].name, stat, valeur, add)


def modifs_valeurs_viking(request, nom, stat, valeur, add):
    if add != "true":
        valeur = valeur * -1

    char = Viking.objects.filter(name=nom)
    car = Viking.objects.all().filter(name=nom)[0]
    if stat == "pv":
        char.update(point_de_vie=car.point_de_vie + valeur)
    if stat == "pv_max":
        char.update(point_de_vie_max=car.point_de_vie_max + valeur)
    if stat == "magie":
        char.update(point_de_pouvoir=car.point_de_pouvoir + valeur)
    return HttpResponse("")


def getvik2(request, joueur):
    car = Viking.objects.all().filter(joueur=joueur)[0]
    return getvik(request, car.name)

def getvik(request, nom):
    car = Viking.objects.all().filter(name=nom)[0]
    json = '{"name":"' + car.name + '","agriculture":' + str(car.agriculture) + ',"charisme":' + str(
        car.charisme) + ',"combat":' + str(car.combat) + ',"magie":' + str(
        car.magie) + ',"savoir":' + str(car.savoir) \
           + ',"navigation":' + str(car.navigation) + ',"nature":' + str(
        car.nature) + ',"point_de_vie":' + str(car.point_de_vie) + ',"point_de_vie_max":' + str(
        car.point_de_vie_max) + ',"point_de_pouvoir":' + str(car.point_de_pouvoir) + '}'
    return HttpResponse(json)




def mj(request):
    template = loader.get_template('applsr/mj.html')
    context = {

    }
    return HttpResponse((template.render(context, request)))


def masterwords(request, role):
    template = loader.get_template('applsr/masterwords.html')
    context = {
        'role': role
    }
    return HttpResponse((template.render(context, request)))


def enregistrer(request, _name, _info):
    Masterword.objects.filter(name=_name).update(info=_info)
    return HttpResponse("ok")


def initmw(request):
    Masterword.objects.all().delete()
    for x in range(1, 8):
        for y in range(1, 4):
            name = "l" + str(x) + "c" + str(y)
            m = Masterword(name=name, info='')
            m.save()
    name = "l8c1"
    m = Masterword(name=name, info='')
    m.save()
    name = "indice"
    m = Masterword(name=name, info='')
    m.save()
    for y in range(1, 4):
        name = "prop"+str(y)
        m = Masterword(name=name, info='')
        m.save()
    name = "theme"
    m = Masterword(name=name, info='')
    m.save()
    for y in range(1, 9):
        name = "valide"+str(y)
        m = Masterword(name=name, info='')
        m.save()
    for y in range(1, 8):
        name = "reponse"+str(y)
        m = Masterword(name=name, info='')
        m.save()
    return HttpResponse("ok")


def afficher_mw(request):
    info = "{"
    for x in range(1, 8):
        for y in range(1, 4):
            name = "l"+str(x)+"c"+str(y)
            char = Masterword.objects.filter(name=name)
            info += "\""+char[0].name+"\":\""+char[0].info+"\","
    name = "l8c1"
    char = Masterword.objects.filter(name=name)
    info += "\"" + char[0].name + "\":\"" + char[0].info + "\","
    name = "indice"
    char = Masterword.objects.filter(name=name)
    info += "\"" + char[0].name + "\":\"" + char[0].info + "\","
    for y in range(1, 9):
        name = "valide"+str(y)
        char = Masterword.objects.filter(name=name)
        info += "\"" + char[0].name + "\":\"" + char[0].info + "\","
    for y in range(1, 8):
        name = "reponse"+str(y)
        char = Masterword.objects.filter(name=name)
        info += "\"" + char[0].name + "\":\"" + char[0].info + "\","
    for y in range(1, 4):
        name = "prop"+str(y)
        char = Masterword.objects.filter(name=name)
        info += "\"" + char[0].name + "\":\"" + char[0].info + "\","
    name = "theme"
    char = Masterword.objects.filter(name=name)
    info += "\"" + char[0].name + "\":\"" + char[0].info + "\"}"

    return HttpResponse(info)


def dice_roll(car, test, focus, pouvoir, nb, more_dices, use_ra, mal, ben, is_secret, des_caches, elem, opposition=0):
    print(is_secret)
    print("-----------------------------------------")
    dices = []
    success = 0
    dices_string = ""
    if is_secret:
        dices_string += "(secret)"
    if mal > 0 or ben > 0:
        dices_string += "Avec "

    if mal == 1:
        dices_string += "une <i>malédiction</i>"
    elif mal > 1:
        dices_string += "" + str(mal) + " <i>malédictions</i>"

    if mal > 0 and ben > 0:
        dices_string += " et "

    if ben == 1:
        dices_string += "une <i>bénédiction</i>"
    elif ben > 1:
        dices_string += "" + str(ben) + " <i>bénédictions</i>"

    if mal > 0 or ben > 0:
        dices_string += ", "

    dices_string += "<b>" + car + "</b> "
    if focus:
        dices_string += "se <i>concentre</i> et "

    if test == 'Jsoin':
        dices_string += "<i>Soigne</i>"+elem+" "
    elif test == 'JM':
        dices_string += "lance un <i>Sort</i> "
    elif test == 'JAF':
        dices_string += "utilise une <i>Arcane Fixe</i>."
        now = datetime.now()
        dices_string = "" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " - " + dices_string
        dice = DiceRoll(dices=dices_string, secret=is_secret, lancer=car)
        dice.save()
        result = {
            'requete': test,
            'dices': dices,
            'success': success,
            'degats': 0,
        }
        return result
    elif test == 'JAE':
        dices_string += "utilise une <i>Arcane d'Esprit</i> "
    elif test == 'JAS':
        dices_string += "utilise une <i>Arcane d'Essence</i> "
    else:
        dices_string += "fait un <i>Jet "
        if test == 'JC':
            dices_string += "de Chair</i> "
        elif test == 'JS':
            dices_string += "d\'Esprit</i> "
        elif test == 'JE':
            dices_string += "d\'Essence</i> "
        elif test == 'JCH':
            dices_string += "de Charisme</i> "
        elif test == 'JAG':
            dices_string += "d\'Agriculture</i> "
        elif test == 'JCB':
            dices_string += "de Combat</i> "
        elif test == 'JMG':
            dices_string += "de Magie</i> "
        elif test == 'JSV':
            dices_string += "de Savoir</i> "
        elif test == 'JNV':
            dices_string += "de Navigation</i> "
        elif test == 'JNT':
            dices_string += "de Nature</i> "

    if pouvoir:
        success += 1
        dices_string += "en y mettant toute sa <i>puissance</i>  "

    if not des_caches:
        dices_string += ":<br/>"
    nb = nb + more_dices
    for i in range(0, nb):
        roll = random.randint(1, 6)
        if not des_caches:
            dices_string += " [ " + str(roll) + " ] "
        dices.append(roll)
        if roll == 5:
            success += 1
        elif roll == 6:
            success += 2


    if use_ra:
        success += 1

    if test == 'Jsoin':
        success += 1

    if success == 0:
        dices_string += "<br/>mais n'obtient <b>aucune réussite</b>..."
    elif success == 1:
        dices_string += "<br/>et obtient <b>une réussite</b>"
    else:
        dices_string += "<br/>et obtient <b>" + str(success) + " réussites</b>"

    if use_ra:
        dices_string += ", grâce à son <i>héritage latent</i>"

    dices_string += "."

    degats=0
    if opposition > 0 :
        degats = int((opposition - success + 1)/2)
        if degats < 0 :
            degats = 0
        dices_string += " Cela lui inflige " + str(degats) + "  dégats."
    

    now = datetime.now()
    dices_string = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" - "+dices_string
    dice = DiceRoll(dices=dices_string, secret=is_secret, lancer=car)
    dice.save()
    result = {
        degats
#        'requete': test,
 #       'dices': dices,
  #      'success': success,
   #     'degats': degats
    }
    return result


def dice_roll_fake(car, test, focus, pouvoir, nb, more_dices, use_ra, mal, ben, is_secret, des_caches):
    print(is_secret)
    print("-----------------------------------------")
    dices = []
    success = 0
    dices_string = ""
    if is_secret:
        dices_string += "(secret)"
    if mal > 0 or ben > 0:
        dices_string += "Avec "

    if mal == 1:
        dices_string += "une <i>malédiction</i>"
    elif mal > 1:
        dices_string += "" + str(mal) + " <i>malédictions</i>"

    if mal > 0 and ben > 0:
        dices_string += " et "

    if ben == 1:
        dices_string += "une <i>bénédiction</i>"
    elif ben > 1:
        dices_string += "" + str(ben) + " <i>bénédictions</i>"

    if mal > 0 or ben > 0:
        dices_string += ", "

    dices_string += "<b>" + car + "</b> "
    if focus:
        dices_string += "se <i>concentre</i> et "

    if test == 'JM':
        dices_string += "lance un <i>Sort</i> "
    if test == 'JAF' or test == 'JAE' or test == 'JAS':
        dices_string += "utilise une <i>Arcane</i> "
    else:
        dices_string += "fait un <i>Jet "
        if test == 'JC':
            dices_string += "de Chair</i> "
        elif test == 'JS':
            dices_string += "d\'Esprit</i> "
        elif test == 'JE':
            dices_string += "d\'Essence</i> "
        elif test == 'JCH':
            dices_string += "de Charisme</i> "
        elif test == 'JAG':
            dices_string += "d\'Agriculture</i> "
        elif test == 'JCB':
            dices_string += "de Combat</i> "
        elif test == 'JMG':
            dices_string += "de Magie</i> "
        elif test == 'JSV':
            dices_string += "de Savoir</i> "
        elif test == 'JNV':
            dices_string += "de Navigation</i> "
        elif test == 'JNT':
            dices_string += "de Nature</i> "
    if pouvoir:
        success += 1
        dices_string += "en y mettant toute sa <i>puissance</i>  "

    if not des_caches:
        dices_string += ":<br/>"
    nb = nb + more_dices
    success = des_caches
    result = {
        'requete': test,
        'dices': dices,
        'success': success,
    }

    if use_ra:
        success += 1

    if success == 0:
        dices_string += "<br/>mais n'obtient <b>aucune réussite</b>..."
    elif success == 1:
        dices_string += "<br/>et obtient <b>une réussite</b>"
    else:
        dices_string += "<br/>et obtient <b>" + str(success) + " réussites</b>"

    if use_ra:
        dices_string += ", grâce à son <i>héritage latent</i>"

    dices_string += "."
    now = datetime.now()
    dices_string = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" - "+dices_string
    dice = DiceRoll(dices=dices_string, secret=is_secret, lancer=car)
    dice.save()

    return result


def afficher(request, nom, secret):
    is_secret= secret == "true"
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    if is_secret:
        queryset = DiceRoll.objects.order_by('-date').filter(date__gte=today_start).filter(date__lt=today_end)
    else:
        queryset = DiceRoll.objects.order_by('-date').filter(date__gte=today_start).filter(date__lt=today_end).filter(Q(secret=False) | Q(lancer=nom.capitalize()))
    if queryset.count() > 10:
        queryset = queryset[:10]

    aff = "<table class=\"table table-hover\">"
    for q in queryset:
        aff += "<tr><td>" + q.dices + "</td></tr>"
    aff += "</table>"
    print(aff)
    return HttpResponse(aff)


def lancer_empirique(request, nom, valeur, secret):
    is_secret = secret == "true"
    dices_string = ""
    if is_secret:
        dices_string += "(secret)"
    dices_string += nom.capitalize()+" fait un <b>Jet Empirique</b> ("+valeur+"):<br/>"
    v = valeur.split("d")
    for i in range(0, int(v[0])):
        roll = random.randint(1, int(v[1]))
        dices_string += " [ " + str(roll) + " ] "
    now = datetime.now()
    dices_string = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" - "+dices_string
    dice = DiceRoll(dices=dices_string, secret=is_secret, lancer=nom.capitalize())
    dice.save()
    return HttpResponse(dices_string)


def lancer(request, nom, action, pf, pp, ra, mal, ben, secret, des_caches):
    use_pf = pf == "true"
    use_pp = pp == "true"
    use_ra = ra == "true"
    is_secret = secret == "true"
    is_des_caches = des_caches == "true"
    char = Character.objects.filter(name=nom)
    more_dices = 0
    focus = False
    pouvoir = False
    if use_pf and char[0].point_de_focus > 0:
        more_dices += 1
        focus = True
        Character.objects.filter(id=char[0].id).update(point_de_focus=char[0].point_de_focus - 1)
    if use_pp and char[0].point_de_pouvoir > 0:
        pouvoir = True
        Character.objects.filter(id=char[0].id).update(dettes=char[0].dettes + 1)
        Character.objects.filter(id=char[0].id).update(point_de_pouvoir=char[0].point_de_pouvoir - 1)
    more_dices -= mal
    more_dices += ben

    dice = ""
    if 'JC' == action:
        #malus_chair = (char[0].point_de_vie_max - char[0].point_de_vie) // 6
        ##elem = "<<" + str(malus_chair) + ">>"
        #more_dices -= malus_chair
        dice = dice_roll(char[0].name.capitalize(), 'JC', focus, pouvoir, char[0].chair, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JS' == action:
        dice = dice_roll(char[0].name.capitalize(), 'JS', focus, pouvoir, char[0].esprit, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JE' == action:
        dice = dice_roll(char[0].name.capitalize(), 'JE', focus, pouvoir, char[0].essence, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JM' == action:
        Character.objects.filter(id=char[0].id).update(dettes=char[0].dettes + 1)
        dice = dice_roll(char[0].name.capitalize(), 'JM', focus, pouvoir, char[0].essence, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JAF' == action and char[0].arcanes > 0:
        Character.objects.filter(id=char[0].id).update(arcanes=char[0].arcanes - 1)
        dice = dice_roll(char[0].name.capitalize(), 'JAF', focus, pouvoir, char[0].essence, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JAE' == action and char[0].arcanes > 0:
        Character.objects.filter(id=char[0].id).update(arcanes=char[0].arcanes - 1)
        dice = dice_roll(char[0].name.capitalize(), 'JAE', focus, pouvoir, char[0].esprit, more_dices, use_ra, mal, ben, is_secret, is_des_caches, "")
    if 'JAS' == action and char[0].arcanes > 0:
        Character.objects.filter(id=char[0].id).update(arcanes=char[0].arcanes - 1)
        dice = dice_roll(char[0].name.capitalize(), 'JAS', focus, pouvoir, char[0].essence, more_dices, use_ra, mal,
                         ben, is_secret, is_des_caches, "")
    if 'Jsoin' == action :
        Character.objects.filter(id=char[0].id).update(dettes=char[0].dettes + 1)
        Character.objects.filter(id=char[0].id).update(point_de_pouvoir=char[0].point_de_pouvoir - 1)
        elem=""
        if char[0].element == "glace" :
            elem =" par la glace"
        if char[0].element == "eau":
            elem = " par l\'eau"
        if char[0].element == "feu" :
            elem =" par le feu"
        if char[0].element == "ombre" :
            elem =" par l\'ombre"
        if char[0].element == "vent" :
            elem =" par le vent"
        if char[0].element == "terre" :
            elem =" par la terre"
        if char[0].element == "foudre" :
            elem =" par la foudre"
        if char[0].element == "lumiere" :
            elem =" par la lumière"
            Character.objects.filter(id=char[0].id).update(point_de_pouvoir=char[0].point_de_pouvoir +1)
        if char[0].element == "arbre" :
            elem =" par la nature"
        if char[0].element == "gorgonne" :
            elem =" par la corruption"
        if char[0].element == "lion" :
            elem =" par la bête"
        if char[0].element == "illithid" :
            elem =" par l'esprit'"
        if char[0].element == "deva" :
            elem =" par la deva"
        dice = dice_roll(char[0].name.capitalize(), 'Jsoin', focus, pouvoir, char[0].essence, more_dices, use_ra, mal,
                         ben, is_secret, is_des_caches, elem)

    return HttpResponse(dice)

def lancer_pnj(request, nom, action, stat, pf, pp, ra, mal, ben, secret, des_caches, opposition):
    use_pf = pf == "true"
    use_pp = pp == "true"
    use_ra = ra == "true"
    is_secret = secret == "true"
    more_dices = 0
    focus = False
    pouvoir = False
    if use_pf:  # and char[0].point_de_focus > 0:
        more_dices += 1
        focus = True
    if use_pp:  # and char[0].point_de_focus > 0:
        pouvoir = True
    more_dices -= mal
    more_dices += ben

    dice = ""
    is_des_caches = des_caches == "true"
    dice = dice_roll(nom.capitalize(), action, focus, pouvoir, stat, more_dices, use_ra, mal, ben, is_secret,is_des_caches, "", opposition)

    return HttpResponse(dice)


def lancer_pnj2(request, nom, action, stat, pf, pp, ra, mal, ben, secret, des_caches):
    use_pf = pf == "true"
    use_pp = pp == "true"
    use_ra = ra == "true"
    is_secret = secret == "true"
    more_dices = 0
    focus = False
    pouvoir = False
    if use_pf:  # and char[0].point_de_focus > 0:
        more_dices += 1
        focus = True
    if use_pp:  # and char[0].point_de_focus > 0:
        pouvoir = True
    more_dices -= mal
    more_dices += ben

    dice = ""
    dice = dice_roll_fake(nom.capitalize(), action, focus, pouvoir, stat, more_dices, use_ra, mal, ben, is_secret,des_caches)

    return HttpResponse(dice)


def lsr(request, nom):
    template = loader.get_template('applsr/index.html')

    char = Character.objects.filter(name=nom)
    if char.count() == 1:
        if request.method == 'POST':
            # form = L7RForm(request.POST)
            action = "erreur"
            if 'JC-M' in request.POST:
                action = 'JC-M'
            if 'JC' in request.POST:
                action = 'JC'
            if 'JC-B' in request.POST:
                action = 'JC-B'
            if 'JS-M' in request.POST:
                action = 'JS-M'
            if 'JS' in request.POST:
                action = 'JS'
            if 'JS-B' in request.POST:
                action = 'JS-B'
            if 'JE-M' in request.POST:
                action = 'JE-M'
            if 'JE' in request.POST:
                action = 'JE'
            if 'JE-B' in request.POST:
                action = 'JE-B'
            print(action)

            # if form.is_valid():
            #    dice = lsr_js(form.cleaned_data['use_pf'], form.cleaned_data['use_pp'], nom, action)
    context = {
        'car': char[0],
    }
    return HttpResponse(template.render(context, request))


def effacer_lancers_des(request):
    DiceRoll.objects.all().delete()
    return HttpResponse("")


def modifs_valeurs(request, nom, stat, valeur, add):
    if add != "true":
        valeur = valeur * -1

    char = Character.objects.filter(name=nom)
    car = Character.objects.all().filter(name=nom)[0]
    if stat == "pv":
        char.update(point_de_vie=car.point_de_vie + valeur)
    if stat == "pv_max":
        char.update(point_de_vie_max=car.point_de_vie_max + valeur)
    if stat == "pf":
        char.update(point_de_focus=car.point_de_focus + valeur)
    if stat == "pf_max":
        char.update(point_de_focus_max=car.point_de_focus_max + valeur)
    if stat == "pp":
        char.update(point_de_pouvoir=car.point_de_pouvoir + valeur)
    if stat == "pp_max":
        char.update(point_de_pouvoir_max=car.point_de_pouvoir_max + valeur)
    if stat == "chair":
        char.update(chair=car.chair + valeur)
    if stat == "esprit":
        char.update(esprit=car.esprit + valeur)
    if stat == "essence":
        char.update(essence=car.essence + valeur)
    if stat == "dettes":
        char.update(dettes=car.dettes + valeur)
    if stat == "arcanes":
        char.update(arcanes=car.arcanes + valeur)
    if stat == "arcanes_max":
        char.update(arcanes_max=car.arcanes_max + valeur)
    return HttpResponse("")


def getcar(request, nom):
    car = Character.objects.all().filter(name=nom)[0]
    json = '{"name":"' + car.name + '","chair":' + str(car.chair) + ',"esprit":' + str(
        car.esprit) + ',"essence":' + str(car.essence) + ',"point_de_vie":' + str(
        car.point_de_vie) + ',"point_de_vie_max":' + str(car.point_de_vie_max) \
           + ',"point_de_focus":' + str(car.point_de_focus) + ',"point_de_focus_max":' + str(
        car.point_de_focus_max) + ',"point_de_pouvoir":' + str(car.point_de_pouvoir) + ',"point_de_pouvoir_max":' + str(
        car.point_de_pouvoir_max) + ',"dettes":' + str(car.dettes) + ',"arcanes":' + str(car.arcanes) + ',"arcanes_max":' + str(
        car.arcanes_max) + ',"fl":"' + car.fl + '","fu":"' + car.fu + '","fs":"' + car.fs + '"}'
    return HttpResponse(json)


def updatepj(request, nom, chair, esprit, essence, point_de_vie_max,point_de_focus_max,point_de_pouvoir_max,niveau):
    char = Character.objects.filter(name=nom)
    char.update(chair=chair)
    char.update(esprit=esprit)
    char.update(essence=essence)
    char.update(point_de_vie_max=point_de_vie_max)
    char.update(point_de_focus_max=point_de_focus_max)
    char.update(point_de_pouvoir_max=point_de_pouvoir_max)
    char.update(niveau=niveau)

    return HttpResponse("")