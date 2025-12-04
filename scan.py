import requests
import json
import time
import sys
import os
from datetime import datetime, timedelta

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC"

# --- LISTA DE REGIONES CORREGIDA ---
REGIONS = [
    # --- LATINOAMÉRICA Y TERRITORIOS AUSTRALES (Idioma: es-419) ---
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"UY", "l":"es-419"}, {"c":"VE", "l":"es-419"}, {"c":"EC", "l":"es-419"},
    {"c":"GT", "l":"es-419"}, {"c":"BO", "l":"es-419"}, {"c":"CR", "l":"es-419"},
    {"c":"DO", "l":"es-419"}, {"c":"SV", "l":"es-419"}, {"c":"HN", "l":"es-419"},
    {"c":"NI", "l":"es-419"}, {"c":"PA", "l":"es-419"}, {"c":"PY", "l":"es-419"},
    {"c":"FK", "l":"es-419"}, # Islas Malvinas
    {"c":"GS", "l":"es-419"}, # Islas Georgias del Sur (Forzado a Latino)

    # --- NORTEAMÉRICA Y CARIBE ---
    {"c":"US", "l":"en-US"}, {"c":"CA", "l":"en-CA"}, {"c":"PR", "l":"es-419"}, 
    {"c":"PM", "l":"fr-FR"}, 
    {"c":"JM", "l":"en-US"}, {"c":"BS", "l":"en-US"}, {"c":"BB", "l":"en-US"}, 
    {"c":"TT", "l":"en-US"}, {"c":"AG", "l":"en-US"}, {"c":"DM", "l":"en-US"}, 
    {"c":"GD", "l":"en-US"}, {"c":"KN", "l":"en-US"}, {"c":"LC", "l":"en-US"}, 
    {"c":"VC", "l":"en-US"}, {"c":"BZ", "l":"en-US"}, {"c":"HT", "l":"fr-FR"},
    
    # Caribe Neerlandés y Territorios
    {"c":"AW", "l":"nl-NL"}, {"c":"CW", "l":"nl-NL"}, {"c":"SX", "l":"nl-NL"},
    {"c":"BQ", "l":"nl-NL"}, 
    {"c":"GP", "l":"fr-FR"}, {"c":"MQ", "l":"fr-FR"}, {"c":"BL", "l":"fr-FR"},
    {"c":"MF", "l":"fr-FR"}, {"c":"KY", "l":"en-US"}, {"c":"BM", "l":"en-US"},
    {"c":"VI", "l":"en-US"}, {"c":"VG", "l":"en-US"}, {"c":"TC", "l":"en-US"},
    {"c":"AI", "l":"en-US"}, {"c":"MS", "l":"en-US"}, {"c":"GY", "l":"en-US"},
    {"c":"SR", "l":"en-US"}, {"c":"GF", "l":"fr-FR"},
    {"c":"UM", "l":"en-US"}, 

    # --- EUROPA ---
    # España y territorios asociados (Forzados a Castellano puro)
    {"c":"ES", "l":"es-ES"}, 
    {"c":"AD", "l":"es-ES"}, # Andorra
    {"c":"GI", "l":"es-ES"}, # Gibraltar

    # Resto de Europa
    {"c":"FR", "l":"fr-FR"}, {"c":"DE", "l":"de-DE"}, {"c":"IT", "l":"it-IT"}, 
    {"c":"GB", "l":"en-GB"}, {"c":"PT", "l":"pt-PT"}, {"c":"NL", "l":"nl-NL"}, 
    {"c":"BE", "l":"fr-BE"}, {"c":"CH", "l":"de-CH"}, {"c":"AT", "l":"de-AT"}, 
    {"c":"IE", "l":"en-GB"}, {"c":"SE", "l":"sv-SE"}, {"c":"NO", "l":"no-NO"}, 
    {"c":"DK", "l":"da-DK"}, {"c":"FI", "l":"fi-FI"}, {"c":"IS", "l":"en-GB"}, 
    {"c":"LU", "l":"fr-FR"}, {"c":"MC", "l":"fr-FR"}, {"c":"LI", "l":"de-DE"}, 
    {"c":"MT", "l":"en-GB"}, {"c":"SM", "l":"it-IT"}, {"c":"VA", "l":"it-IT"}, 
    {"c":"IM", "l":"en-GB"}, {"c":"GG", "l":"en-GB"}, {"c":"JE", "l":"en-GB"},
    
    # Regiones Nórdicas y Especiales
    {"c":"AX", "l":"sv-SE"}, # Åland (Agregado con idioma Sueco)
    {"c":"FO", "l":"da-DK"}, {"c":"GL", "l":"da-DK"}, {"c":"SJ", "l":"no-NO"}, 
    {"c":"BV", "l":"no-NO"}, 

    # Europa del Este y Balcanes
    {"c":"PL", "l":"pl-PL"}, {"c":"CZ", "l":"cs-CZ"}, {"c":"SK", "l":"sk-SK"}, 
    {"c":"HU", "l":"hu-HU"}, {"c":"RO", "l":"ro-RO"}, {"c":"BG", "l":"bg-BG"}, 
    {"c":"HR", "l":"hr-HR"}, {"c":"GR", "l":"el-GR"}, {"c":"SI", "l":"sl-SI"}, 
    {"c":"EE", "l":"et-EE"}, {"c":"LV", "l":"lv-LV"}, {"c":"LT", "l":"lt-LT"}, 
    {"c":"CY", "l":"el-GR"}, {"c":"AL", "l":"sq-AL"}, {"c":"MK", "l":"mk-MK"}, 
    {"c":"BA", "l":"hr-BA"}, {"c":"RS", "l":"sr-RS"}, {"c":"ME", "l":"sr-ME"}, 
    {"c":"TR", "l":"tr-TR"}, {"c":"XK", "l":"sq-AL"}, 

    # --- ASIA / PACÍFICO / OCEANÍA ---
    {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"}, 
    {"c":"TW", "l":"zh-TW"}, {"c":"HK", "l":"zh-HK"}, 
    {"c":"SG", "l":"en-SG"}, {"c":"AU", "l":"en-AU"},
    {"c":"NZ", "l":"en-NZ"}, 
    
    # Territorios del Pacífico y Océano Índico
    {"c":"NC", "l":"fr-FR"}, {"c":"PF", "l":"fr-FR"}, {"c":"WF", "l":"fr-FR"}, 
    {"c":"GU", "l":"en-US"}, {"c":"MP", "l":"en-US"}, {"c":"AS", "l":"en-US"}, 
    {"c":"RE", "l":"fr-FR"}, {"c":"YT", "l":"fr-FR"}, {"c":"MU", "l":"en-GB"},
    {"c":"CK", "l":"en-NZ"}, {"c":"NU", "l":"en-NZ"}, {"c":"TK", "l":"en-NZ"},
    {"c":"PN", "l":"en-GB"}, {"c":"SH", "l":"en-GB"}, {"c":"IO", "l":"en-GB"}, 
    {"c":"TF", "l":"fr-FR"}, 
    {"c":"CC", "l":"en-AU"}, {"c":"CX", "l":"en-AU"}, 
    {"c":"NF", "l":"en-AU"}, {"c":"HM", "l":"en-AU"}
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}

LANG_CODES = {
    "es-419": "Spanish (LatAm)", 
    "es-ES": "Spanish", # Cambiado para que ES/AD/GI muestren solo "Spanish"
    "es": "Spanish",
    "en": "English", "pt-BR": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)",
    "fr-FR": "French", "fr-CA": "French (Canadian)", "de": "German", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "zh-Hant": "Chinese (Traditional)", "zh-Hans": "Chinese (Simplified)",
    "zh-HK": "Cantonese", "zh-TW": "Taiwanese Mandarin", "ru": "Russian", "pl": "Polish", "tr": "Turkish",
    "nl": "Dutch", "da": "Danish", "sv": "Swedish", "no": "Norwegian", "fi": "Finnish",
    "el": "Greek", "he": "Hebrew", "ar": "Arabic", "th": "Thai", "id": "Indonesian",
    "vi": "Vietnamese", "ms": "Malay", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian",
    "sq": "Albanian", "mk": "Macedonian", "sr": "Serbian", "hr": "Croatian", "sl": "Slovenian",
    "bg": "Bulgarian", "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian"
}

# --- CONFIGURACIÓN DE FILTRADO ---
FIX_TARGET_DATE = "2025-12-03" 
FIX_OLD_DATE = "2000-01-01"    

FIX_DACH_REGIONS = ["DE", "CH", "LI", "AT"] 
FIX_TITLES = [
    "mister agreste", "sleeping syren", "the dark castle", "wreckless driver", "yaksi gozen",
    "senor agreste", "señor agreste", "sirena durmiente", "el castillo oscuro", "conductor temerario"
]

FIX_EXPIRY_DATE = datetime(2025, 12, 7, 23, 59, 59)

def log(msg):
    print(msg)
    sys.stdout.flush()

def clean_sub_name(code, raw_name):
    if not raw_name or "--" in raw_name or raw_name == code:
        base = raw_name.split('--')[0] if raw_name else code
        return LANG_CODES.get(base, base)
    return raw_name

def load_previous_db():
    if os.path.exists("database.json"):
        try:
            with open("database.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"regions": {}}

def get_data():
    OLD_DB = load_previous_db()
    new_database = { "meta": { "updated": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC") }, "regions": {} }
    
    # FECHA BASE: HORA DEL PACÍFICO (UTC-8)
    # Se usa para calcular el día actual de referencia.
    pacific_time_now = datetime.utcnow() - timedelta(hours=8)
    today_str = pacific_time_now.strftime("%Y-%m-%d")
    IS_FIX_WINDOW = (pacific_time_now <= FIX_EXPIRY_DATE)
    
    log(f"🌍 INICIANDO ESCANEO (Ref. Time: Pacific {today_str})...")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        if idx % 10 == 0: log(f"Procesando bloque {idx+1}...")

        new_eps_count = 0 
        memory_map = {}
        if code in OLD_DB.get("regions", {}):
            for s in OLD_DB["regions"][code].get("seasons", []):
                for ep in s.get("eps", []):
                    memory_map[f"{s['id']}-{ep['n']}"] = ep.get('dt', '')

        try:
            url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
            r = requests.get(url_bundle, headers=HEADERS, timeout=4)
            if r.status_code == 200:
                data = r.json()
                seasons = data.get('data', {}).get('DmcSeriesBundle', {}).get('seasons', {}).get('seasons', [])
                if seasons:
                    region_data = {"seasons": [], "news": []}
                    for s in seasons:
                        s_id = s['seasonId']
                        s_num = s.get('seasonSequenceNumber', 0)
                        # AUMENTADO pageSize a 150 para evitar saltar episodios en regiones como HK
                        url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/150/page/1"
                        try:
                            r_eps = requests.get(url_eps, headers=HEADERS, timeout=4)
                            if r_eps.status_code == 200:
                                eps_raw = r_eps.json().get('data', {}).get('DmcEpisodes', {}).get('videos', [])
                                clean_eps = []
                                for i, ep in enumerate(eps_raw):
                                    ep_num = ep.get('episodeSequenceNumber') or ep.get('sequenceNumber') or (i + 1)
                                    title = ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título')
                                    
                                    if IS_FIX_WINDOW:
                                        is_target = False
                                        if code in FIX_DACH_REGIONS and s_num == 6 and ep_num <= 7: is_target = True
                                        t_clean = title.lower() if title else ""
                                        if any(ft in t_clean for ft in FIX_TITLES): is_target = True
                                        final_date = FIX_TARGET_DATE if is_target else FIX_OLD_DATE
                                    else:
                                        stored_date = memory_map.get(f"{s_num}-{ep_num}")
                                        final_date = stored_date if stored_date else today_str

                                    desc = ep.get('text', {}).get('description', {}).get('medium', {}).get('program', {}).get('default', {}).get('content', '')
                                    if not desc: desc = ep.get('text', {}).get('description', {}).get('brief', {}).get('program', {}).get('default', {}).get('content', '')

                                    meta = ep.get('mediaMetadata', {})
                                    subs_list = []
                                    for sub in meta.get('captionTracks', []):
                                        subs_list.append({"l": clean_sub_name(sub.get('language'), sub.get('renditionName')), "t": sub.get('trackType', 'NORMAL')})
                                    audios_list = []
                                    for aud in meta.get('audioTracks', []):
                                        audios_list.append(clean_sub_name(aud.get('language'), aud.get('renditionName')))

                                    clean_eps.append({"n": ep_num, "t": title, "ds": desc, "dt": final_date, "a": audios_list, "s": subs_list})
                                    if final_date:
                                        try:
                                            dt_obj = datetime.strptime(final_date, "%Y-%m-%d")
                                            # Se calcula la novedad basándose en la hora del Pacífico
                                            if 0 <= (pacific_time_now - dt_obj).days <= 90: 
                                                region_data["news"].append({"e":f"T{s_num} E{ep_num}", "t":title, "d":final_date})
                                                new_eps_count += 1
                                        except: pass
                                region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                        except: pass
                    new_database["regions"][code] = region_data
                    
                    msg_extra = f"({new_eps_count} Nuevos)" if new_eps_count > 0 else "(0 Nuevos)"
                    log(f"   ✅ {code}: OK {msg_extra}")
        except: pass
        time.sleep(0.1)
    return new_database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS ACTUALIZADA.")
    except Exception as e: log(f"💀 ERROR: {e}")
