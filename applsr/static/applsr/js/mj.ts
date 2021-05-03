type Stat = "pv" | "arcanes" | "dettes" | "pf" | "pp" | "ben" | "mal";

let nbPJ = 0;
let listPJ: string[] = [];
let table = "";

nompj = "mj";
display_secret = true; // override value from lsr.js

function getCurrentCharacter(): string | HTMLElement | null {
    //return document.querySelector<HTMLInputElement>("#pj-select")!.value;
    return document.querySelector<HTMLElement>('input[name="resist"]:checked')?.parentElement ?? null;
}

document.addEventListener("DOMContentLoaded", () => {
    setInterval(() => {
        afficherPJ();
    }, 2000);

    afficherPJ();
});

function modif(nom: string, stat: Stat, valeur: number, add: boolean) {
    fetch('/mj_interdit_aux_joueurs/modifs_valeurs/' + nom + '/' + stat + '/' + valeur + '/' + add).catch(function(e) {
        console.error("error", e);
    }).then(() => afficher(nompj));
}

function ajouter_pj(name: string) {
    let liste_pj = document.querySelector<HTMLElement>('#liste_pj')!;
    table = table +
        '<td align="center">' + '<span id="pj_name"><b>' + name + '</b></span>'
        + '<div class="line"><i><span id="pj_fl_' + name + '"></span></i></div>'
        + '<div class="line"><i><span id="pj_fu_' + name + '"></span></i></div>'
        + '<div class="line"><i><span id="pj_fs_' + name + '"></span></i></div>'
        + '<div class="btn-group line">'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pv\',1, false);" >-</button>'
            + '<span class="btn btn-info">PV = <span id="pj_pv_' + name + '">3</span>/<span id="pj_pv_max_' + name + '">6</span></span>'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pv\',1, true);" >+</button>'
        + '</div>'
        + '<div class="btn-group line">'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pf\',1, false);" >-</button>'
            + '<span class="btn btn-info">PF = <span id="pj_pf_' + name + '">3</span>/<span id="pj_pf_max_' + name + '">6</span></span>'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pf\',1, true);" >+</button>'
        + '</div>'
        + '<div class="btn-group line">'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pp\',1, false);" >-</button>'
            + '<span class="btn btn-info">PP = <span id="pj_pp_' + name + '">3</span>/<span id="pj_pp_max_' + name + '">6</span></span>'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'pp\',1, true);" >+</button>'
        + '</div>'
        + '<div class="btn-group line">'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'dettes\',1, false);" >-</button>'
            + '<span class="btn btn-info">DT = <span id="pj_dettes_' + name + '">9</span></span>'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'dettes\',1, true);" >+</button>'
        + '</div>'
        + '<div class="btn-group line">'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'arcanes\',1, false);" >-</button>'
            + '<span class="btn btn-info">AK = <span id="pj_arcanes_' + name + '">3</span>/<span id="pj_arcanes_max_' + name + '">6</span></span>'
            + '<button class="btn" onclick="modif(\'' + name + '\',\'arcanes\',1, true);" >+</button>'
        + '</div>'
        + '</td>';
    liste_pj.innerHTML = '<table class="pj-for-mj"><tr>' + table + '</tr></table>';
    nbPJ++;
    listPJ.push(name);
}

function afficherPJ() {
    listPJ.forEach(function(name, index, array) {
        fetch('/lsr/getcar/' + name)
            .then((response) => response.text())
            .then(json => {
                const obj = JSON.parse(json);
                document.querySelector('#pj_pv_' + name)!.innerHTML = obj.point_de_vie;
                document.querySelector('#pj_pv_max_' + name)!.innerHTML = obj.point_de_vie_max;
                document.querySelector('#pj_pf_' + name)!.innerHTML = obj.point_de_focus;
                document.querySelector('#pj_pf_max_' + name)!.innerHTML = obj.point_de_focus_max;
                document.querySelector('#pj_pp_' + name)!.innerHTML = obj.point_de_pouvoir;
                document.querySelector('#pj_pp_max_' + name)!.innerHTML = obj.point_de_pouvoir_max;
                document.querySelector('#pj_dettes_' + name)!.innerHTML = obj.dettes;
                document.querySelector('#pj_arcanes_' + name)!.innerHTML = obj.arcanes;
                document.querySelector('#pj_arcanes_max_' + name)!.innerHTML = obj.arcanes_max;
                document.querySelector('#pj_fl_' + name)!.innerHTML = obj.fl;
                document.querySelector('#pj_fu_' + name)!.innerHTML = obj.fu;
                document.querySelector('#pj_fs_' + name)!.innerHTML = obj.fs;
            }).catch(function(e) {
                console.error("error", e);
            });
    });
}

function effacer_pnj(new_pnj_name: string) {
    const pnj = document.querySelector('#pnj_' + new_pnj_name)!;
    pnj.innerHTML = "";
    pnj.parentElement?.removeChild(pnj);
}

function modifPNJ(pnj_name: string, stat: Stat, valeur: number) {
    const mod = document.querySelector('#pnj_' + stat + '_' + pnj_name)!;
    console.log('#pnj_' + stat + '_' + pnj_name)
    console.log(valeur)
    mod.innerHTML = (parseInt(mod.innerHTML) + valeur).toString();
}

function jetPNJ(name: string, action: RollType, stat: number, pf: boolean, pp: boolean, ra: boolean, sec: boolean, dc: boolean /** dés cachés */, parentRollId: string | null = null) {
    const mal = parseInt(document.querySelector('#pnj_mal_' + name)!.innerHTML);
    const ben = parseInt(document.querySelector('#pnj_ben_' + name)!.innerHTML);
    const opposition = parseInt(document.querySelector<HTMLInputElement>('#opposition')!.value);

    if(document.querySelector<HTMLInputElement>('#opposition_checked')!.checked) {
        fetch('/mj/lancer_pnj/' + name + '/' + action + '/' + stat + '/' + pf + '/' + pp + '/' + ra + '/' + mal + '/' + ben + '/' + sec + '/' + dc + '/' + opposition + '?parent_roll_id=' + parentRollId).then(function(response) {
            response.text().then(function(text) {
                const degats = parseInt(text);
                modifPNJ(name, "pv", degats * -1);
                afficher("mj");
            });
        });
    } else {
        fetch('/mj/lancer_pnj/' + name + '/' + action + '/' + stat + '/' + pf + '/' + pp + '/' + ra + '/' + mal + '/' + ben + '/' + sec + '/' + dc + '/0' + '?parent_roll_id=' + parentRollId).then(() => afficher("mj"));
    }
    if(action == 'JM')
        modifPNJ(name, 'dettes', 1);
    if(pf)
        modifPNJ(name, 'pf', -1);
    if(pp) {
        modifPNJ(name, 'pp', -1);
        modifPNJ(name, 'dettes', 1);
    }
}

function createJetPnjTemplate(new_pnj_name: string, new_pnj_stat_value: string, new_pnj_stat_name: string, action: RollType) {
    return '<button class="btn" onclick="jetPNJ(\'' + new_pnj_name + '\',\'' + action + '\',' + new_pnj_stat_value + ',document.getElementById(\'use_pf_' + new_pnj_name + '\').checked,document.getElementById(\'use_pp_' + new_pnj_name + '\').checked,document.getElementById(\'use_ra_' + new_pnj_name + '\').checked, document.getElementById(\'use_sc_' + new_pnj_name + '\').checked, document.getElementById(\'use_dc_' + new_pnj_name + '\').checked);">' + new_pnj_stat_name + '</button>'
}

function ajouter_pnj(new_pnj_name: string, new_pnj_chair: string, new_pnj_esprit: string, new_pnj_essence: string, new_pnj_pv_max: number | "PVmax", new_pnj_pf_max: number | "PFmax", new_pnj_pp_max: number | "PPmax") {
    const new_pnj_dettes = Math.floor(Math.random() * Math.floor(5));
    const liste_pnj = document.querySelector('#liste_pnj')!;
    if(new_pnj_pv_max == "PVmax") {
        new_pnj_pv_max = parseInt(new_pnj_chair) * 2;
    }
    if(new_pnj_pf_max == "PFmax") {
        new_pnj_pf_max = parseInt(new_pnj_esprit);
    }
    if(new_pnj_pp_max == "PPmax") {
        new_pnj_pp_max = parseInt(new_pnj_essence);
    }
    liste_pnj.innerHTML = liste_pnj.innerHTML
        + '<div class="pnj" id="pnj_' + new_pnj_name + '" data-jc="' + new_pnj_chair + '" data-js="' + new_pnj_esprit + '" data-je="' + new_pnj_essence + '">'

        + '<input type="radio" name="resist" />'
        + '<button class="btn btn-danger" onclick="effacer_pnj(\'' + new_pnj_name + '\');"> X </button>'
        + '<span><b class="name">' + new_pnj_name + '</b> : </span>'
        
        + '<span class="btn-group">'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pv\',-1);" >-</button>'
            + '<span class="btn btn-info">'
                + 'PV = <span id="pnj_pv_' + new_pnj_name + '">' + new_pnj_pv_max
                + '</span>/<span id="pj_pv_max_' + new_pnj_name + '">' + new_pnj_pv_max + '</span>'
            + '</span>'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pv\',1);" >+</button>'
        + '</span>'
        
        + '<span class="btn-group">'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pf\',-1);" >-</button>'
            + '<span class="btn btn-info">'
                + '<input id="use_pf_' + new_pnj_name + '" type="checkbox" autocomplete="off">'
                + 'PF: <span id="pnj_pf_' + new_pnj_name + '">' + new_pnj_pf_max + '</span>/' + new_pnj_pf_max
            + '</span>'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pf\',1);" >+</button>'
        + '</span>'

        + '<span class="btn-group">'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pp\',-1);" >-</button>'
            + '<span class="btn btn-info">'
                + '<input id="use_pp_' + new_pnj_name + '" type="checkbox" autocomplete="off">'
                + 'PP: <span id="pnj_pp_' + new_pnj_name + '">' + new_pnj_pp_max + '</span>/' + new_pnj_pp_max
            + '</span>'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'pp\',1);" >+</button>'
        + '</span>'

        + '<label class="btn">'
            + '<input id="use_ra_' + new_pnj_name + '" type="checkbox" autocomplete="off"> RA'
        + '</label>'

        + '<label class="btn">'
            + '<input id="use_sc_' + new_pnj_name + '" type="checkbox" autocomplete="off"> Secret'
        + '</label>'

        + '<label class="btn">'
            + '<input id="use_dc_' + new_pnj_name + '" type="checkbox" checked="true" autocomplete="off"> Cachés'
        + '</label>'

        + createJetPnjTemplate(new_pnj_name, new_pnj_chair, "Chair", "JC")
        + createJetPnjTemplate(new_pnj_name, new_pnj_esprit, "Esprit", "JS")
        + createJetPnjTemplate(new_pnj_name, new_pnj_essence, "Essence", "JE")
        + createJetPnjTemplate(new_pnj_name, new_pnj_essence, "Magie", "JM")
        
        + '<span class="btn-group">'
            + '<button class="btn btn-danger" onclick="modifPNJ(\'' + new_pnj_name + '\',\'mal\',-1);" >-</button>'
            + '<span class="btn btn-outline-danger">Mal: <span id="pnj_mal_' + new_pnj_name + '">0</span></span>'
            + '<button class="btn btn-danger" onclick="modifPNJ(\'' + new_pnj_name + '\',\'mal\',1);" >+</button> '
        + '</span>'
        
        + '<span class="btn-group">'
            + '<button class="btn btn-success" onclick="modifPNJ(\'' + new_pnj_name + '\',\'ben\',-1);" >-</button>'
            + '<span class="btn btn-outline-success">Ben: <span id="pnj_ben_' + new_pnj_name + '">0</span></span>'
            + '<button class="btn btn-success" onclick="modifPNJ(\'' + new_pnj_name + '\',\'ben\',1);" >+</button> '
        + '</span>'
        
        + '<span class="btn-group">'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'dettes\',-1);" >-</button>'
            + '<span class="btn btn-info">Dettes: <span id="pnj_dettes_' + new_pnj_name + '">' + new_pnj_dettes + '</span></span>'
            + '<button class="btn" onclick="modifPNJ(\'' + new_pnj_name + '\',\'dettes\',1);" >+</button>'
        + '</span>'

        + '</div>'
}

function effacerLancersDes() {
    fetch('/mj_interdit_aux_joueurs/effacerLancersDes');
}
