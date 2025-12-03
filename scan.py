import requests
import json
import time
import sys
from datetime import datetime

# --- CONFIGURACIÓN ---
SERIES_ID = "1CjTiHEJbLRC"

# Lista de regiones
REGIONS = [
    # Principales
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"US", "l":"en-US"}, {"c":"ES", "l":"es-ES"}, {"c":"FR", "l":"fr-FR"},
    # Resto
    {"c":"CL", "l":"es-419"}, {"c":"CO", "l":"es-419"}, {"c":"PE", "l":"es-419"},
    {"c":"GB", "l":"en-GB"}, {"c":"DE", "l":"de-DE"}, {"c":"IT", "l":"it-IT"},
    {"c":"PT", "l":"pt-PT"}, {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"},
    {"c":"TR", "l":"tr-TR"}, {"c":"SG", "l":"en-SG"}, {"c":"AU", "l":"en-AU"},
    {"c":"CA", "l":"en-CA"}, {"c":"NL", "l":"nl-NL"}, {"c":"SE", "l":"sv-SE"},
    {"c":"NO", "l":"no-NO"}, {"c":"DK", "l":"da-DK"}, {"c":"PL", "l":"pl-PL"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

# Función para imprimir inmediatamente en la consola de GitHub
def log(msg):
    print(msg)
    sys.stdout.flush() # <--- ESTO FUERZA A QUE SE VEA EL TEXTO AL INSTANTE

def get_data():
    database = {
        "meta": { "updated": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC") },
        "regions": {}
    }

    log(f"🚀 INICIANDO ESCANEO DE {len(REGIONS)} PAISES...")

    for idx, reg in enumerate(REGIONS):
        code = reg['c']
        lang = reg['l']
        
        # Imprimimos ANTES de conectar para saber si se cuelga aquí
        log(f"[{idx+1}/{len(REGIONS)}] Conectando a {code}...")

        try:
            # Timeout muy corto (3.05 segundos) para no atascarse
            url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
            r = requests.get(url_bundle, headers=HEADERS, timeout=3.05)

            if r.status_code == 200:
                data = r.json()
                seasons = data.get('data', {}).get('DmcSeriesBundle', {}).get('seasons', {}).get('seasons', [])
                
                region_data = {"seasons": [], "news": []}
                log(f"   ✅ {code}: Encontradas {len(seasons)} temporadas.")

                for s in seasons:
                    s_id = s['seasonId']
                    s_num = s.get('seasonSequenceNumber', 0)
                    
                    url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/60/page/1"
                    try:
                        r_eps = requests.get(url_eps, headers=HEADERS, timeout=3.05)
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
                                if not desc: desc = "..."

                                ep_obj = {
                                    "n": ep.get('sequenceNumber', 0),
                                    "t": title,
                                    "ds": desc[:200], 
                                    "dt": date_str.split('T')[0] if date_str else "",
                                    "a": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('audioTracks', [])][:4],
                                    "s": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('captionTracks', [])][:4]
                                }
                                clean_eps.append(ep_obj)
                                if is_new: 
                                    region_data["news"].append({"e":f"T{s_num} E{ep_obj['n']}", "t":title, "d":ep_obj['dt']})

                            region_data["seasons"].append({"id": s_num, "eps": clean_eps})
                    except:
                        pass # Si falla un episodio, seguimos

                if region_data["seasons"]:
                    database["regions"][code] = region_data
            else:
                log(f"   ⚠️ {code}: Bloqueado o sin datos ({r.status_code})")

        except Exception as e:
            log(f"   ❌ {code}: Error o Timeout. Saltando...")

    return database

if __name__ == "__main__":
    try:
        data = get_data()
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        log("🎉 BASE DE DATOS GUARDADA.")
    except Exception as e:
        log(f"💀 ERROR FATAL: {e}")
