import requests
import json
import time
from datetime import datetime

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC" # Miraculous

# --- LISTA MASIVA DE REGIONES ---
# Formato: Código ISO del país + Idioma preferido para la API
REGIONS = [
    # AMÉRICA DEL NORTE & CARIBE
    {"c":"US", "l":"en-US"}, {"c":"CA", "l":"en-CA"}, {"c":"PR", "l":"es-419"}, 
    {"c":"VI", "l":"en-US"}, {"c":"BM", "l":"en-US"}, {"c":"KY", "l":"en-US"},
    {"c":"BS", "l":"en-US"}, {"c":"JM", "l":"en-US"}, {"c":"TC", "l":"en-US"},
    {"c":"AW", "l":"en-US"}, {"c":"CW", "l":"en-US"}, {"c":"SX", "l":"en-US"},
    {"c":"GP", "l":"fr-FR"}, {"c":"MQ", "l":"fr-FR"}, {"c":"BL", "l":"fr-FR"},
    {"c":"MF", "l":"fr-FR"}, {"c":"PM", "l":"fr-FR"}, {"c":"AG", "l":"en-US"},
    {"c":"BB", "l":"en-US"}, {"c":"DM", "l":"en-US"}, {"c":"GD", "l":"en-US"},
    {"c":"KN", "l":"en-US"}, {"c":"LC", "l":"en-US"}, {"c":"VC", "l":"en-US"},
    {"c":"TT", "l":"en-US"}, {"c":"BZ", "l":"en-US"}, {"c":"HT", "l":"fr-FR"},

    # LATINOAMÉRICA (Soberanos y Dependencias)
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"UY", "l":"es-419"}, {"c":"VE", "l":"es-419"}, {"c":"EC", "l":"es-419"},
    {"c":"GT", "l":"es-419"}, {"c":"BO", "l":"es-419"}, {"c":"CR", "l":"es-419"},
    {"c":"DO", "l":"es-419"}, {"c":"SV", "l":"es-419"}, {"c":"HN", "l":"es-419"},
    {"c":"NI", "l":"es-419"}, {"c":"PA", "l":"es-419"}, {"c":"PY", "l":"es-419"},
    {"c":"GY", "l":"en-US"},  {"c":"SR", "l":"en-US"},  {"c":"GF", "l":"fr-FR"},
    {"c":"FK", "l":"es-419"}, # Islas Malvinas

    # EUROPA OESTE & DEPENDENCIAS
    {"c":"ES", "l":"es-ES"}, {"c":"FR", "l":"fr-FR"}, {"c":"DE", "l":"de-DE"},
    {"c":"IT", "l":"it-IT"}, {"c":"GB", "l":"en-GB"}, {"c":"IE", "l":"en-GB"},
    {"c":"PT", "l":"pt-PT"}, {"c":"NL", "l":"nl-NL"}, {"c":"BE", "l":"fr-FR"},
    {"c":"CH", "l":"de-DE"}, {"c":"AT", "l":"de-DE"}, {"c":"LU", "l":"fr-FR"},
    {"c":"SE", "l":"sv-SE"}, {"c":"NO", "l":"no-NO"}, {"c":"DK", "l":"da-DK"},
    {"c":"FI", "l":"fi-FL"}, {"c":"IS", "l":"en-GB"}, {"c":"MC", "l":"fr-FR"},
    {"c":"GI", "l":"en-GB"}, {"c":"GG", "l":"en-GB"}, {"c":"JE", "l":"en-GB"},
    {"c":"IM", "l":"en-GB"}, {"c":"MT", "l":"en-GB"}, {"c":"FO", "l":"da-DK"},
    {"c":"GL", "l":"da-DK"}, {"c":"AX", "l":"sv-SE"}, {"c":"SJ", "l":"no-NO"},

    # EUROPA ESTE / BALCANES
    {"c":"PL", "l":"pl-PL"}, {"c":"CZ", "l":"cs-CZ"}, {"c":"SK", "l":"sk-SK"},
    {"c":"HU", "l":"hu-HU"}, {"c":"RO", "l":"ro-RO"}, {"c":"BG", "l":"bg-BG"},
    {"c":"HR", "l":"hr-HR"}, {"c":"GR", "l":"el-GR"}, {"c":"SI", "l":"sl-SI"},
    {"c":"EE", "l":"et-EE"}, {"c":"LV", "l":"lv-LV"}, {"c":"LT", "l":"lt-LT"},
    {"c":"CY", "l":"el-GR"}, {"c":"TR", "l":"tr-TR"}, {"c":"RS", "l":"sr-RS"},
    {"c":"BA", "l":"hr-HR"}, {"c":"MK", "l":"mk-MK"}, {"c":"ME", "l":"sr-RS"},
    {"c":"AL", "l":"sq-AL"},

    # ASIA PACÍFICO & OCEANÍA
    {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"}, {"c":"TW", "l":"zh-Hant-TW"},
    {"c":"HK", "l":"zh-Hant-HK"}, {"c":"SG", "l":"en-SG"}, {"c":"AU", "l":"en-AU"},
    {"c":"NZ", "l":"en-NZ"}, {"c":"NC", "l":"fr-FR"}, {"c":"PF", "l":"fr-FR"},
    {"c":"WF", "l":"fr-FR"}, {"c":"GU", "l":"en-US"}, {"c":"MP", "l":"en-US"},
    {"c":"AS", "l":"en-US"},

    # ÁFRICA / ÍNDICO (Territorios Disney+ Standard)
    {"c":"RE", "l":"fr-FR"}, {"c":"YT", "l":"fr-FR"}, {"c":"ZA", "l":"en-ZA"} 
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Origin': 'https://www.disneyplus.com',
    'Referer': 'https://www.disneyplus.com/'
}

def get_data():
    database = {
        "meta": {
            "updated": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"),
            "total_regions": len(REGIONS)
        },
        "regions": {}
    }

    print(f"--- INICIANDO ESCANEO GLOBAL ({len(REGIONS)} REGIONES) ---")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        
        # Estructura base para la región
        region_data = {"seasons": [], "news": []}
        
        try:
            # 1. Obtener Seasons del Bundle
            url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
            r = requests.get(url_bundle, headers=HEADERS, timeout=5)
            
            if r.status_code == 200:
                data = r.json()
                seasons = data.get('data', {}).get('DmcSeriesBundle', {}).get('seasons', {}).get('seasons', [])
                
                print(f"[{idx+1}/{len(REGIONS)}] {code}: OK ({len(seasons)} temporadas)")

                for s in seasons:
                    s_id = s['seasonId']
                    s_num = s.get('seasonSequenceNumber', 0)
                    
                    # 2. Obtener Episodios
                    url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/60/page/1"
                    r_eps = requests.get(url_eps, headers=HEADERS, timeout=5)
                    
                    if r_eps.status_code == 200:
                        eps_raw = r_eps.json().get('data', {}).get('DmcEpisodes', {}).get('videos', [])
                        
                        clean_eps = []
                        for ep in eps_raw:
                            # Parsear Fecha
                            date_str = ep.get('availabilityDate', '')
                            is_new = False
                            
                            if date_str:
                                try:
                                    dt = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
                                    # Lógica Novedades (Últimos 90 días)
                                    delta = (datetime.utcnow() - dt).days
                                    if 0 <= delta <= 90:
                                        is_new = True
                                except:
                                    pass

                            # Extraer datos mínimos (Optimización de tamaño JSON)
                            ep_obj = {
                                "n": ep.get('sequenceNumber', 0),
                                "t": ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título'),
                                "d": date_str.split('T')[0] if date_str else "",
                                "a": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('audioTracks', [])][:4], # Max 4
                                "s": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('captionTracks', [])][:4] # Max 4
                            }
                            
                            clean_eps.append(ep_obj)
                            
                            if is_new:
                                region_data["news"].append({
                                    "e": f"T{s_num} E{ep_obj['n']}",
                                    "t": ep_obj['t'],
                                    "d": ep_obj['d']
                                })
                        
                        region_data["seasons"].append({
                            "id": s_num,
                            "eps": clean_eps
                        })

                # Solo guardar si encontró algo
                if region_data["seasons"]:
                    database["regions"][code] = region_data
            else:
                print(f"[{idx+1}/{len(REGIONS)}] {code}: Sin datos o bloqueo ({r.status_code})")

        except Exception as e:
            print(f"[{idx+1}/{len(REGIONS)}] {code}: ERROR - {str(e)}")
        
        # Pequeña pausa para ser amigable con el servidor
        time.sleep(0.2)

    return database

if __name__ == "__main__":
    data = get_data()
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Base de datos generada exitosamente.")
