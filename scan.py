import requests
import json
import time
import sys
from datetime import datetime, timedelta

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC"

# LISTA DE TÍTULOS QUE SIEMPRE SON NOVEDAD (Sin importar la fecha)
# Escribe aquí partes clave de los títulos en minúsculas
FORCED_NEW_TITLES = [
    "mister agreste", 
    "sleeping syren", 
    "dark castle", 
    "wrexkels driver", 
    "wreckels driver", # Variación por si acaso
    "yaksi gozen"
]

# LISTA DE REGIONES DACH+LI PARA FORZAR TEMPORADA 6
DACH_LI_CODES = ["DE", "AT", "CH", "LI"]

# MAPA DE LIMPIEZA DE SUBTÍTULOS
LANG_CODES = {
    "es-419": "Spanish (Latin American)", "es-ES": "Spanish (Castilian)", "es": "Spanish",
    "en": "English", "pt-BR": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)",
    "fr-FR": "French", "fr-CA": "French (Canadian)", "de": "German", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "zh-Hant": "Chinese (Traditional)", "zh-Hans": "Chinese (Simplified)",
    "zh-HK": "Cantonese", "ru": "Russian", "pl": "Polish", "tr": "Turkish",
    "nl": "Dutch", "da": "Danish", "sv": "Swedish", "no": "Norwegian", "fi": "Finnish",
    "el": "Greek", "he": "Hebrew", "ar": "Arabic", "th": "Thai", "id": "Indonesian",
    "vi": "Vietnamese", "ms": "Malay", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian"
}

# LISTA DE REGIONES
REGIONS = [
    # LATAM
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"UY", "l":"es-419"}, {"c":"VE", "l":"es-419"}, {"c":"EC", "l":"es-419"},
    {"c":"GT", "l":"es-419"}, {"c":"BO", "l":"es-419"}, {"c":"CR", "l":"es-419"},
    {"c":"DO", "l":"es-419"}, {"c":"SV", "l":"es-419"}, {"c":"HN", "l":"es-419"},
    {"c":"NI", "l":"es-419"}, {"c":"PA", "l":"es-419"}, {"c":"PY", "l":"es-419"},
    {"c":"FK", "l":"es-419"}, # Malvinas
    
    # NORTE AMERICA
    {"c":"US", "l":"en-US"}, {"c":"CA", "l":"en-CA"}, {"c":"PR", "l":"es-419"}, {"c":"PM", "l":"fr-FR"},

    # EUROPA
    {"c":"ES", "l":"es-ES"}, {"c":"FR", "l":"fr-FR"}, {"c":"DE", "l":"de-DE"},
    {"c":"IT", "l":"it-IT"}, {"c":"GB", "l":"en-GB"}, {"c":"PT", "l":"pt-PT"},
    {"c":"NL", "l":"nl-NL"}, {"c":"BE", "l":"fr-BE"}, {"c":"CH", "l":"de-CH"},
    {"c":"AT", "l":"de-AT"}, {"c":"IE", "l":"en-GB"}, {"c":"SE", "l":"sv-SE"},
    {"c":"NO", "l":"no-NO"}, {"c":"DK", "l":"da-DK"}, {"c":"FI", "l":"fi-FL"},
    {"c":"IS", "l":"en-GB"}, {"c":"LU", "l":"fr-FR"}, {"c":"MC", "l":"fr-FR"},
    {"c":"LI", "l":"de-DE"}, {"c":"MT", "l":"en-GB"}, {"c":"AD", "l":"es-ES"},
    {"c":"SM", "l":"it-IT"}, {"c":"VA", "l":"it-IT"}, {"c":"GI", "l":"es-ES"},
    {"c":"IM", "l":"en-GB"}, {"c":"GG", "l":"en-GB"}, {"c":"JE", "l":"en-GB"},
    {"c":"FO", "l":"da-DK"}, {"c":"GL", "l":"da-DK"}, {"c":"AX", "l":"sv-SE"},
    {"c":"SJ", "l":"no-NO"}, {"c":"PL", "l":"pl-PL"}, {"c":"CZ", "l":"cs-CZ"},
    {"c":"SK", "l":"sk-SK"}, {"c":"HU", "l":"hu-HU"}, {"c":"RO", "l":"ro-RO"},
    {"c":"BG", "l":"bg-BG"}, {"c":"HR", "l":"hr-HR"}, {"c":"GR", "l":"el-GR"},
    {"c":"SI", "l":"sl-SI"}, {"c":"EE", "l":"et-EE"}, {"c":"LV", "l":"lv-LV"},
    {"c":"LT", "l":"lt-LT"}, {"c":"CY", "l":"el-GR"}, {"c":"AL", "l":"sq-AL"},
    {"c":"MK", "l":"mk-MK"}, {"c":"BA", "l":"hr-BA"}, {"c":"RS", "l":"sr-RS"},
    {"c":"ME", "l":"sr-ME"}, {"c":"TR", "l":"tr-TR"},

    # ASIA / PACIFICO
    {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"}, {"c":"TW", "l":"zh-Hant-TW"},
    {"c":"HK", "l":"zh-Hant-HK"}, {"c":"SG", "l":"en-SG"}, {"c":"AU", "l":"en-AU"},
    {"c":"NZ", "l":"en-NZ"}, {"c":"NC", "l":"fr-FR"}, {"c":"PF", "l":"fr-FR"},
    {"c":"WF", "l":"fr-FR"}, {"c":"GU", "l":"en-US"}, {"c":"MP", "l":"en-US"},
    {"c":"AS", "l":"en-US"},

    # CARIBE
    {"c":"JM", "l":"en-US"}, {"c":"BS", "l":"en-US"}, {"c":"BB", "l":"en-US"},
    {"c":"TT", "l":"en-US"}, {"c":"AG", "l":"en-US"}, {"c":"DM", "l":"en-US"},
    {"c":"GD", "l":"en-US"}, {"c":"KN", "l":"en-US"}, {"c":"LC", "l":"en-US"},
    {"c":"VC", "l":"en-US"}, {"c":"BZ", "l":"en-US"}, {"c":"HT", "l":"fr-FR"},
    {"c":"AW", "l":"en-US"}, {"c":"CW", "l":"en-US"}, {"c":"SX", "l":"en-US"},
    {"c":"GP", "l":"fr-FR"}, {"c":"MQ", "l":"fr-FR"}, {"c":"BL", "l":"fr-FR"},
    {"c":"MF", "l":"fr-FR"}, {"c":"KY", "l":"en-US"}, {"c":"BM", "l":"en-US"},
    {"c":"VI", "l":"en-US"}, {"c":"VG", "l":"en-US"}, {"c":"TC", "l":"en-US"},
    {"c":"AI", "l":"en-US"}, {"c":"MS", "l":"en-US"}, {"c":"GY", "l":"en-US"},
    {"c":"SR", "l":"en-US"}, {"c":"GF", "l":"fr-FR"}, 

    # OTROS
    {"c":"RE", "l":"fr-FR"}, {"c":"YT", "l":"fr-FR"}, {"c":"MU", "l":"en-GB"}
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}

def log(msg):
    print(msg)
    sys.stdout.flush()

def clean_sub_name(code, raw_name):
    # Traducir códigos técnicos a nombres legibles
    if not raw_name or "--" in raw_name or raw_name == code:
        # Intentar extraer el código de idioma base (ej: es-419 -> es-419)
        base_code = raw_name.split('--')[0] if raw_name else code
        return LANG_CODES.get(base_code, base_code)
    return raw_name

def get_data():
    database = {"meta": {"updated": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")}, "regions": {}}
    log(f"🌍 INICIANDO ESCANEO... ({len(REGIONS)} regiones)")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        
        if idx % 10 == 0: log(f"Procesando bloque {idx+1}...")

        try:
            url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
            try: r = requests.get(url_bundle, headers=HEADERS, timeout=4)
            except: continue 

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
                                clean_eps = []
                                
                                for i, ep in enumerate(eps_raw):
                                    ep_num = ep.get('episodeSequenceNumber') or ep.get('sequenceNumber') or (i + 1)

                                    date_str = ep.get('availabilityDate', '')
                                    is_new = False
                                    ep_date_clean = ""

                                    # LÓGICA DE FECHA
                                    if date_str:
                                        try:
                                            ep_date_clean = date_str.split('T')[0]
                                            dt = datetime.strptime(ep_date_clean, "%Y-%m-%d")
                                            # Rango amplio: -60 días a +120 días
                                            delta = (datetime.utcnow() - dt).days
                                            if -60 <= delta <= 120:
                                                is_new = True
                                        except: pass

                                    # OBTENER TÍTULO
                                    title = ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título')
                                    
                                    # --- REGLA FORZADA 1: TÍTULOS ESPECÍFICOS ---
                                    title_lower = title.lower()
                                    if any(forced in title_lower for forced in FORCED_NEW_TITLES):
                                        is_new = True

                                    # --- REGLA FORZADA 2: TEMPORADA 6 EN DACH+LI ---
                                    if code in DACH_LI_CODES and s_num == 6:
                                        is_new = True

                                    # SUBTITULOS
                                    meta = ep.get('mediaMetadata', {})
                                    subs_list = []
                                    for sub in meta.get('captionTracks', []):
                                        l_code = sub.get('language')
                                        raw_n = sub.get('renditionName')
                                        clean_n = clean_sub_name(l_code, raw_n)
                                        subs_list.append({
                                            "l": clean_n,
                                            "t": sub.get('trackType', 'NORMAL')
                                        })

                                    # AUDIOS
                                    audios_list = []
                                    for aud in meta.get('audioTracks', []):
                                        l_code = aud.get('language')
                                        raw_n = aud.get('renditionName')
                                        audios_list.append(clean_sub_name(l_code, raw_n))

                                    desc = ep.get('text', {}).get('description', {}).get('medium', {}).get('program', {}).get('default', {}).get('content', '')
                                    if not desc: desc = ep.get('text', {}).get('description', {}).get('brief', {}).get('program', {}).get('default', {}).get('content', '')

                                    ep_obj = {
                                        "n": ep_num,
                                        "t": title,
                                        "ds": desc,
                                        "dt": ep_date_clean,
                                        "a": audios_list,
                                        "s": subs_list
                                    }
                                    clean_eps.append(ep_obj)
                                    if is_new: region_data["news"].append({"e":f"T{s_num} E{ep_num}", "t":title, "d":ep_date_clean})

                                region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                        except: pass

                    database["regions"][code] = region_data
                    if len(region_data["news"]) > 0:
                        log(f"   ✅ {code}: OK ({len(region_data['news'])} novedades)")
                    else:
                        log(f"   ✅ {code}: OK")
        except: pass
        time.sleep(0.1)

    return database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS GUARDADA.")
    except Exception as e:
        log(f"💀 ERROR: {e}")                                    desc = ep.get('text', {}).get('description', {}).get('medium', {}).get('program', {}).get('default', {}).get('content', '')
                                    if not desc: desc = ep.get('text', {}).get('description', {}).get('brief', {}).get('program', {}).get('default', {}).get('content', '')

                                    # 4. ARREGLO SUBTITULOS Y AUDIO
                                    meta = ep.get('mediaMetadata', {})
                                    
                                    # Subs: Guardamos objeto {l: idioma, t: tipo}
                                    subs_list = []
                                    for sub in meta.get('captionTracks', []):
                                        subs_list.append({
                                            "l": sub.get('renditionName', sub.get('language', 'unk')),
                                            "t": sub.get('trackType', 'NORMAL')
                                        })

                                    # Audio: Lista simple de strings
                                    audios_list = [x.get('renditionName', x.get('language')) for x in meta.get('audioTracks', [])]

                                    ep_obj = {
                                        "n": ep_num,
                                        "t": title,
                                        "ds": desc,
                                        "dt": date_str.split('T')[0] if date_str else "",
                                        "a": audios_list,
                                        "s": subs_list
                                    }
                                    clean_eps.append(ep_obj)
                                    if is_new: region_data["news"].append({"e":f"T{s_num} E{ep_num}", "t":title, "d":ep_obj['dt']})

                                region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                        except: pass

                    database["regions"][code] = region_data
                    log(f"   ✅ {code}: OK")
            
        except Exception as e:
            pass

        time.sleep(0.1)

    return database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS GUARDADA.")
    except Exception as e:
        log(f"💀 ERROR: {e}")
