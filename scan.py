import requests
import json
import time
import sys
import os
from datetime import datetime, timedelta

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC"
DB_FILE = "database.json"

# --- CONFIGURACIÓN DE HORARIOS ---
UTC_OFFSETS = {
    "US": -5, "CA": -5, "MX": -6, "AR": -3, "BR": -3, "CL": -3, "CO": -5, "PE": -5,
    "UY": -3, "VE": -4, "EC": -5, "GT": -6, "BO": -4, "CR": -6, "DO": -4, "SV": -6,
    "HN": -6, "NI": -6, "PA": -5, "PY": -3, "FK": -3, "GS": -2, "PR": -4, "JM": -5,
    "BS": -5, "BB": -4, "TT": -4, "AG": -4, "DM": -4, "GD": -4, "KN": -4, "LC": -4,
    "VC": -4, "BZ": -6, "HT": -5, "AW": -4, "CW": -4, "SX": -4, "BQ": -4, "GP": -4,
    "MQ": -4, "BL": -4, "MF": -4, "KY": -5, "BM": -4, "VI": -4, "VG": -4, "TC": -5,
    "AI": -4, "MS": -4, "GY": -4, "SR": -3, "GF": -3, "PM": -3, "UM": -11,
    "ES": 1, "FR": 1, "DE": 1, "IT": 1, "GB": 0, "PT": 0, "NL": 1, "BE": 1, "CH": 1,
    "AT": 1, "IE": 0, "SE": 1, "NO": 1, "DK": 1, "FI": 2, "IS": 0, "LU": 1, "MC": 1,
    "LI": 1, "MT": 1, "AD": 1, "SM": 1, "VA": 1, "GI": 1, "IM": 0, "GG": 0, "JE": 0,
    "AX": 2, "FO": 0, "GL": -3, "SJ": 1, "BV": 1, "PL": 1, "CZ": 1, "SK": 1, "HU": 1,
    "RO": 2, "BG": 2, "HR": 1, "GR": 2, "SI": 1, "EE": 2, "LV": 2, "LT": 2, "CY": 2,
    "AL": 1, "MK": 1, "BA": 1, "RS": 1, "ME": 1, "TR": 3, "XK": 1,
    "JP": 9, "KR": 9, "TW": 8, "HK": 8, "SG": 8, "AU": 11, "NZ": 13, 
    "NC": 11, "PF": -10, "WF": 12, "GU": 10, "MP": 10, "AS": -11, "RE": 4, "YT": 3,
    "MU": 4, "CK": -10, "NU": -11, "TK": 13, "PN": -8, "SH": 0, "IO": 6, "TF": 5,
    "CC": 6.5, "CX": 7, "NF": 11, "HM": 5
}

# --- LISTA DE REGIONES ---
REGIONS = [
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"UY", "l":"es-419"}, {"c":"VE", "l":"es-419"}, {"c":"EC", "l":"es-419"},
    {"c":"GT", "l":"es-419"}, {"c":"BO", "l":"es-419"}, {"c":"CR", "l":"es-419"},
    {"c":"DO", "l":"es-419"}, {"c":"SV", "l":"es-419"}, {"c":"HN", "l":"es-419"},
    {"c":"NI", "l":"es-419"}, {"c":"PA", "l":"es-419"}, {"c":"PY", "l":"es-419"},
    {"c":"FK", "l":"es-419"}, {"c":"GS", "l":"es-419"}, 
    {"c":"US", "l":"en-US"}, {"c":"CA", "l":"en-CA"}, {"c":"PR", "l":"es-419"}, 
    {"c":"PM", "l":"fr-FR"}, {"c":"JM", "l":"en-US"}, {"c":"BS", "l":"en-US"}, 
    {"c":"BB", "l":"en-US"}, {"c":"TT", "l":"en-US"}, {"c":"AG", "l":"en-US"}, 
    {"c":"DM", "l":"en-US"}, {"c":"GD", "l":"en-US"}, {"c":"KN", "l":"en-US"}, 
    {"c":"LC", "l":"en-US"}, {"c":"VC", "l":"en-US"}, {"c":"BZ", "l":"en-US"}, 
    {"c":"HT", "l":"fr-FR"}, {"c":"AW", "l":"nl-NL"}, {"c":"CW", "l":"nl-NL"}, 
    {"c":"SX", "l":"nl-NL"}, {"c":"BQ", "l":"nl-NL"}, {"c":"GP", "l":"fr-FR"}, 
    {"c":"MQ", "l":"fr-FR"}, {"c":"BL", "l":"fr-FR"}, {"c":"MF", "l":"fr-FR"}, 
    {"c":"KY", "l":"en-US"}, {"c":"BM", "l":"en-US"}, {"c":"VI", "l":"en-US"}, 
    {"c":"VG", "l":"en-US"}, {"c":"TC", "l":"en-US"}, {"c":"AI", "l":"en-US"}, 
    {"c":"MS", "l":"en-US"}, {"c":"GY", "l":"en-US"}, {"c":"SR", "l":"en-US"}, 
    {"c":"GF", "l":"fr-FR"}, {"c":"UM", "l":"en-US"}, 
    {"c":"ES", "l":"es-ES"}, {"c":"AD", "l":"es-ES"}, {"c":"GI", "l":"es-ES"},
    {"c":"FR", "l":"fr-FR"}, {"c":"DE", "l":"de-DE"}, {"c":"IT", "l":"it-IT"}, 
    {"c":"GB", "l":"en-GB"}, {"c":"PT", "l":"pt-PT"}, {"c":"NL", "l":"nl-NL"}, 
    {"c":"BE", "l":"fr-BE"}, {"c":"CH", "l":"de-CH"}, {"c":"AT", "l":"de-AT"}, 
    {"c":"IE", "l":"en-GB"}, {"c":"SE", "l":"sv-SE"}, {"c":"NO", "l":"no-NO"}, 
    {"c":"DK", "l":"da-DK"}, {"c":"FI", "l":"fi-FI"}, {"c":"IS", "l":"en-GB"}, 
    {"c":"LU", "l":"fr-FR"}, {"c":"MC", "l":"fr-FR"}, {"c":"LI", "l":"de-DE"}, 
    {"c":"MT", "l":"en-GB"}, {"c":"SM", "l":"it-IT"}, {"c":"VA", "l":"it-IT"}, 
    {"c":"IM", "l":"en-GB"}, {"c":"GG", "l":"en-GB"}, {"c":"JE", "l":"en-GB"},
    {"c":"AX", "l":"sv-SE"}, {"c":"FO", "l":"da-DK"}, {"c":"GL", "l":"da-DK"}, 
    {"c":"SJ", "l":"no-NO"}, {"c":"BV", "l":"no-NO"}, 
    {"c":"PL", "l":"pl-PL"}, {"c":"CZ", "l":"cs-CZ"}, {"c":"SK", "l":"sk-SK"}, 
    {"c":"HU", "l":"hu-HU"}, {"c":"RO", "l":"ro-RO"}, {"c":"BG", "l":"bg-BG"}, 
    {"c":"HR", "l":"hr-HR"}, {"c":"GR", "l":"el-GR"}, {"c":"SI", "l":"sl-SI"}, 
    {"c":"EE", "l":"et-EE"}, {"c":"LV", "l":"lv-LV"}, {"c":"LT", "l":"lt-LT"}, 
    {"c":"CY", "l":"el-GR"}, {"c":"AL", "l":"sq-AL"}, {"c":"MK", "l":"mk-MK"}, 
    {"c":"BA", "l":"hr-BA"}, {"c":"RS", "l":"sr-RS"}, {"c":"ME", "l":"sr-ME"}, 
    {"c":"TR", "l":"tr-TR"}, {"c":"XK", "l":"sq-AL"}, 
    {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"}, 
    {"c":"TW", "l":"zh-TW"}, 
    {"c":"HK", "l":"zh-HK"}, 
    {"c":"SG", "l":"en-SG"}, {"c":"AU", "l":"en-AU"},
    {"c":"NZ", "l":"en-NZ"}, 
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
    "es-419": "Spanish (LatAm)", "es-ES": "Spanish", "es": "Spanish",
    "en": "English", "pt-BR": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)",
    "fr-FR": "French", "fr-CA": "French (Canadian)", "de": "German", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "zh-Hant": "Chinese (Traditional)", "zh-Hans": "Chinese (Simplified)",
    "zh-HK": "Cantonese", "zh-TW": "Mandarin (Taiwan)", "cmn-TW": "Mandarin (Taiwan)",
    "ru": "Russian", "pl": "Polish", "tr": "Turkish", "nl": "Dutch", "da": "Danish", 
    "sv": "Swedish", "no": "Norwegian", "fi": "Finnish", "el": "Greek", "he": "Hebrew", 
    "ar": "Arabic", "th": "Thai", "id": "Indonesian", "vi": "Vietnamese", "ms": "Malay", 
    "cs": "Czech", "hu": "Hungarian", "ro": "Romanian", "sq": "Albanian", "mk": "Macedonian", 
    "sr": "Serbian", "hr": "Croatian", "sl": "Slovenian", "bg": "Bulgarian", 
    "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian"
}

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
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"regions": {}}

def get_local_release_date(pacific_date_str, region_code):
    """
    Calcula la fecha local basada en las 12:00 AM (00:00) Hora del Pacífico.
    """
    if not pacific_date_str or region_code not in UTC_OFFSETS:
        return pacific_date_str
    try:
        base_date = datetime.strptime(pacific_date_str, "%Y-%m-%d")
        utc_release_time = base_date.replace(hour=8) # 00:00 PST = 08:00 UTC
        offset = UTC_OFFSETS.get(region_code, 0)
        local_release_time = utc_release_time + timedelta(hours=offset)
        local_date_str = local_release_time.strftime("%Y-%m-%d")
        return local_date_str
    except Exception:
        return pacific_date_str

def get_data():
    OLD_DB = load_previous_db()
    
    pacific_time_now = datetime.utcnow() - timedelta(hours=8)
    today_str = pacific_time_now.strftime("%Y-%m-%d")
    
    new_database = { 
        "meta": { "updated": pacific_time_now.strftime("%d/%m/%Y %H:%M PT") }, 
        "regions": {} 
    }
    
    IS_FIX_WINDOW = (pacific_time_now <= FIX_EXPIRY_DATE)
    
    log(f"🌍 INICIANDO ESCANEO (Ref. Time: Pacific {today_str})...")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        
        if idx % 10 == 0: 
            log(f"--> Procesando bloque {idx+1}...")

        new_eps_count = 0 
        total_eps_count = 0 
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
                        
                        url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/60/page/1"
                        
                        try:
                            r_eps = requests.get(url_eps, headers=HEADERS, timeout=4)
                            if r_eps.status_code == 200:
                                eps_raw = r_eps.json().get('data', {}).get('DmcEpisodes', {}).get('videos', [])
                                total_eps_count += len(eps_raw)
                                clean_eps = []
                                
                                for i, ep in enumerate(eps_raw):
                                    ep_num = ep.get('episodeSequenceNumber') or ep.get('sequenceNumber') or (i + 1)
                                    title = ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título')
                                    
                                    episode_key = f"{s_num}-{ep_num}"
                                    stored_date = memory_map.get(episode_key)

                                    # --- LOGICA DE FECHAS AJUSTADA ---
                                    
                                    # 1. Determinar si es Target (Evento especial)
                                    is_target = False
                                    if IS_FIX_WINDOW:
                                        if code in FIX_DACH_REGIONS and s_num == 6 and ep_num <= 7: is_target = True
                                        t_clean = title.lower() if title else ""
                                        if any(ft in t_clean for ft in FIX_TITLES): is_target = True

                                    # 2. Asignar fecha RAW
                                    if stored_date:
                                        # Si ya estaba en la DB, respetar su fecha
                                        raw_date = stored_date
                                    elif is_target:
                                        # Si es el evento especial, forzar 3 Dic
                                        raw_date = FIX_TARGET_DATE
                                    elif IS_FIX_WINDOW:
                                        # Estamos en ventana de fix, pero NO es target y NO estaba en DB.
                                        # Esto pasa cuando borraste la DB.
                                        # Para no marcar temporadas viejas como "Nuevas hoy":
                                        api_date = ep.get('releases', [{}])[0].get('releaseDate', None)
                                        
                                        # Si la API tiene fecha y es de 2024/2025, la usamos (es nuevo).
                                        # Si no, usamos fecha vieja.
                                        if api_date and ("2024" in api_date or "2025" in api_date):
                                            raw_date = api_date
                                        else:
                                            raw_date = FIX_OLD_DATE
                                    else:
                                        # MODO NORMAL (Después del 7 Dic):
                                        # Si no estaba en la DB, es NUEVO para nosotros -> Fecha Hoy.
                                        raw_date = today_str

                                    # 3. Ajustar Zona Horaria
                                    final_date = get_local_release_date(raw_date, code)

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
                                    
                                    # 4. Detección de Novedades (Ventana 90 días)
                                    if final_date and final_date != FIX_OLD_DATE:
                                        try:
                                            dt_obj_local = datetime.strptime(final_date, "%Y-%m-%d")
                                            offset = UTC_OFFSETS.get(code, 0)
                                            local_now = datetime.utcnow() + timedelta(hours=offset)
                                            
                                            if 0 <= (local_now - dt_obj_local).days <= 90: 
                                                region_data["news"].append({"e":f"T{s_num} E{ep_num}", "t":title, "d":final_date})
                                                new_eps_count += 1
                                        except: pass
                                
                                region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                        except: pass
                    
                    new_database["regions"][code] = region_data
                    
                    if new_eps_count > 0:
                        log(f"   ✨ {code}: OK ({total_eps_count} Total | {new_eps_count} Nuevos)")
                    else:
                        log(f"   🔹 {code}: OK ({total_eps_count} Total | 0 Nuevos)")
            else:
                log(f"   ⚠️ {code}: Error API {r.status_code}")
                
        except Exception as e: 
            log(f"   ❌ {code}: Error ({e})")
        
        time.sleep(0.1)
        
    return new_database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS ACTUALIZADA.")
    except Exception as e: log(f"💀 ERROR: {e}")
