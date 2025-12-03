import requests
import json
import time
import sys
from datetime import datetime

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC"

# LISTA MAESTRA DE REGIONES (Idiomas corregidos)
REGIONS = [
    # --- ESPECIALES (Solicitud de Usuario) ---
    {"c":"FK", "l":"es-419"}, # Malvinas -> Español Latino
    {"c":"GI", "l":"es-ES"},  # Gibraltar -> Español España

    # --- AMÉRICA ---
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"US", "l":"en-US"}, {"c":"CA", "l":"en-CA"}, {"c":"UY", "l":"es-419"},
    {"c":"VE", "l":"es-419"}, {"c":"EC", "l":"es-419"}, {"c":"GT", "l":"es-419"},
    {"c":"BO", "l":"es-419"}, {"c":"CR", "l":"es-419"}, {"c":"DO", "l":"es-419"},
    {"c":"SV", "l":"es-419"}, {"c":"HN", "l":"es-419"}, {"c":"NI", "l":"es-419"},
    {"c":"PA", "l":"es-419"}, {"c":"PY", "l":"es-419"}, {"c":"PR", "l":"es-419"},
    {"c":"JM", "l":"en-US"}, {"c":"BS", "l":"en-US"}, {"c":"BB", "l":"en-US"},
    {"c":"TT", "l":"en-US"}, {"c":"AG", "l":"en-US"}, {"c":"DM", "l":"en-US"},
    {"c":"GD", "l":"en-US"}, {"c":"KN", "l":"en-US"}, {"c":"LC", "l":"en-US"},
    {"c":"VC", "l":"en-US"}, {"c":"BZ", "l":"en-US"}, {"c":"HT", "l":"fr-FR"},
    {"c":"AW", "l":"en-US"}, {"c":"CW", "l":"en-US"}, {"c":"SX", "l":"en-US"},
    {"c":"GP", "l":"fr-FR"}, {"c":"MQ", "l":"fr-FR"}, {"c":"BL", "l":"fr-FR"},
    {"c":"MF", "l":"fr-FR"}, {"c":"KY", "l":"en-US"}, {"c":"BM", "l":"en-US"},
    {"c":"VI", "l":"en-US"}, {"c":"VG", "l":"en-US"}, {"c":"TC", "l":"en-US"},
    {"c":"AI", "l":"en-US"}, {"c":"MS", "l":"en-US"}, {"c":"GY", "l":"en-US"},
    {"c":"SR", "l":"en-US"}, {"c":"GF", "l":"fr-FR"}, {"c":"PM", "l":"fr-FR"},

    # --- EUROPA ---
    {"c":"ES", "l":"es-ES"}, {"c":"FR", "l":"fr-FR"}, {"c":"DE", "l":"de-DE"},
    {"c":"IT", "l":"it-IT"}, {"c":"GB", "l":"en-GB"}, {"c":"PT", "l":"pt-PT"},
    {"c":"NL", "l":"nl-NL"}, {"c":"BE", "l":"fr-BE"}, {"c":"CH", "l":"de-CH"},
    {"c":"AT", "l":"de-AT"}, {"c":"IE", "l":"en-GB"}, {"c":"SE", "l":"sv-SE"},
    {"c":"NO", "l":"no-NO"}, {"c":"DK", "l":"da-DK"}, {"c":"FI", "l":"fi-FL"},
    {"c":"IS", "l":"en-GB"}, {"c":"LU", "l":"fr-FR"}, {"c":"MC", "l":"fr-FR"},
    {"c":"LI", "l":"de-DE"}, {"c":"MT", "l":"en-GB"}, {"c":"AD", "l":"es-ES"},
    {"c":"SM", "l":"it-IT"}, {"c":"VA", "l":"it-IT"}, 
    {"c":"IM", "l":"en-GB"}, {"c":"GG", "l":"en-GB"}, {"c":"JE", "l":"en-GB"},
    {"c":"FO", "l":"da-DK"}, {"c":"GL", "l":"da-DK"}, {"c":"AX", "l":"sv-SE"},
    {"c":"SJ", "l":"no-NO"}, {"c":"PL", "l":"pl-PL"}, {"c":"CZ", "l":"cs-CZ"},
    {"c":"SK", "l":"sk-SK"}, {"c":"HU", "l":"hu-HU"}, {"c":"RO", "l":"ro-RO"},
    {"c":"BG", "l":"bg-BG"}, {"c":"HR", "l":"hr-HR"}, {"c":"GR", "l":"el-GR"},
    {"c":"SI", "l":"sl-SI"}, {"c":"EE", "l":"et-EE"}, {"c":"LV", "l":"lv-LV"},
    {"c":"LT", "l":"lt-LT"}, {"c":"CY", "l":"el-GR"}, {"c":"AL", "l":"sq-AL"},
    {"c":"MK", "l":"mk-MK"}, {"c":"BA", "l":"hr-BA"}, {"c":"RS", "l":"sr-RS"},
    {"c":"ME", "l":"sr-ME"}, {"c":"TR", "l":"tr-TR"},

    # --- ASIA / PACÍFICO ---
    {"c":"JP", "l":"ja-JP"}, 
    {"c":"KR", "l":"ko-KR"}, 
    {"c":"TW", "l":"zh-Hant-TW"}, # Intentar forzar Chino Tradicional
    {"c":"HK", "l":"zh-Hant-HK"}, # Intentar forzar Chino Tradicional
    {"c":"SG", "l":"en-SG"}, 
    {"c":"AU", "l":"en-AU"},
    {"c":"NZ", "l":"en-NZ"}, 
    {"c":"NC", "l":"fr-FR"}, 
    {"c":"PF", "l":"fr-FR"}, 
    {"c":"WF", "l":"fr-FR"}, 
    {"c":"GU", "l":"en-US"}, 
    {"c":"MP", "l":"en-US"}, 
    {"c":"AS", "l":"en-US"},

    # --- OTROS ---
    {"c":"RE", "l":"fr-FR"}, {"c":"YT", "l":"fr-FR"}, {"c":"MU", "l":"en-GB"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

def log(msg):
    print(msg)
    sys.stdout.flush()

def get_data():
    database = {
        "meta": { "updated": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC") },
        "regions": {}
    }

    log(f"🌍 INICIANDO MEGA-ESCANEO ({len(REGIONS)} REGIONES)...")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        
        if idx % 10 == 0: log(f"Procesando bloque {idx+1}...")

        try:
            # Bundle
            url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
            try:
                r = requests.get(url_bundle, headers=HEADERS, timeout=4)
            except:
                continue 

            if r.status_code == 200:
                data = r.json()
                seasons = data.get('data', {}).get('DmcSeriesBundle', {}).get('seasons', {}).get('seasons', [])
                
                if seasons:
                    region_data = {"seasons": [], "news": []}
                    
                    for s in seasons:
                        s_id = s['seasonId']
                        s_num = s.get('seasonSequenceNumber', 0)
                        
                        # Episodios
                        url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/60/page/1"
                        try:
                            r_eps = requests.get(url_eps, headers=HEADERS, timeout=4)
                            if r_eps.status_code == 200:
                                eps_raw = r_eps.json().get('data', {}).get('DmcEpisodes', {}).get('videos', [])
                                clean_eps = []
                                
                                for ep in eps_raw:
                                    date_str = ep.get('availabilityDate', '')
                                    is_new = False
                                    if date_str:
                                        try:
                                            dt = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
                                            if 0 <= (datetime.utcnow() - dt).days <= 90: is_new = True
                                        except: pass

                                    title = ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título')
                                    desc = ep.get('text', {}).get('description', {}).get('medium', {}).get('program', {}).get('default', {}).get('content', '')
                                    if not desc: desc = ep.get('text', {}).get('description', {}).get('brief', {}).get('program', {}).get('default', {}).get('content', '')

                                    ep_obj = {
                                        "n": ep.get('sequenceNumber', 0),
                                        "t": title,
                                        "ds": desc,
                                        "dt": date_str.split('T')[0] if date_str else "",
                                        "a": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('audioTracks', [])],
                                        "s": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('captionTracks', [])]
                                    }
                                    clean_eps.append(ep_obj)
                                    if is_new: region_data["news"].append({"e":f"T{s_num} E{ep_obj['n']}", "t":title, "d":ep_obj['dt']})

                                region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                        except: pass

                    database["regions"][code] = region_data
                    log(f"   ✅ {code}: OK")
            
        except Exception as e:
            pass

        time.sleep(0.1)

    # ---------------------------------------------------------
    # ZONA DE PRUEBAS: SIMULACIÓN DE LANZAMIENTO
    # ---------------------------------------------------------
    # Elegimos un país para la prueba, por ejemplo: Argentina (AR)
    PAIS_TEST = "AR"
    
    if PAIS_TEST in database["regions"]:
        print(f"!!! INYECTANDO EPISODIO DE PRUEBA EN {PAIS_TEST} !!!")
        
        # Creamos un episodio falso con fecha de HOY
        fake_news = {
            "e": "T6 E01 (TEST)", 
            "t": "🧪 EL GRAN LANZAMIENTO (Simulado)", 
            "d": datetime.utcnow().strftime("%Y-%m-%d") # Fecha actual automática
        }
        
        # Lo insertamos al principio de la lista de novedades
        database["regions"][PAIS_TEST]["news"].insert(0, fake_news)
        
        # También lo agregamos a una temporada ficticia para el catálogo
        fake_season = {
            "id": 6,
            "eps": [{
                "n": 1,
                "t": "🧪 EL GRAN LANZAMIENTO (Simulado)",
                "ds": "Esta es una prueba técnica para verificar que el sistema de alertas de la web funciona correctamente al detectar un estreno mundial.",
                "dt": datetime.utcnow().strftime("%Y-%m-%d"),
                "a": ["Spanish (Latin American)", "French", "English"],
                "s": ["Spanish", "English"]
            }]
        }
        # Agregamos la temporada 6 falsa al principio
        database["regions"][PAIS_TEST]["seasons"].insert(0, fake_season)
    # ---------------------------------------------------------
    
    return database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS ACTUALIZADA.")
    except Exception as e:
        log(f"💀 ERROR: {e}")
