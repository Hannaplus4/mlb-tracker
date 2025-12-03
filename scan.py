import requests
import json
import os
from datetime import datetime

# CONFIGURACIÓN
SERIES_ID = "1CjTiHEJbLRC" # Miraculous
REGIONS = [
    {"c":"AR", "l":"es-419"}, {"c":"MX", "l":"es-419"}, {"c":"BR", "l":"pt-BR"},
    {"c":"US", "l":"en-US"}, {"c":"ES", "l":"es-ES"}, {"c":"FR", "l":"fr-FR"},
    {"c":"DE", "l":"de-DE"}, {"c":"IT", "l":"it-IT"}, {"c":"GB", "l":"en-GB"},
    {"c":"JP", "l":"ja-JP"}, {"c":"KR", "l":"ko-KR"}, {"c":"TR", "l":"tr-TR"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_data():
    database = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "regions": {}
    }

    print(f"Iniciando escaneo de {len(REGIONS)} regiones...")

    for reg in REGIONS:
        code = reg['c']
        lang = reg['l']
        print(f"Escaneando {code}...")
        
        region_data = {"seasons": [], "news": []}
        
        # 1. Obtener Seasons
        url_bundle = f"https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/encodedSeriesId/{SERIES_ID}"
        
        try:
            r = requests.get(url_bundle, headers=HEADERS)
            if r.status_code != 200:
                print(f" - {code}: No disponible o error bundle")
                continue
                
            data = r.json()
            seasons = data.get('data', {}).get('DmcSeriesBundle', {}).get('seasons', {}).get('seasons', [])
            
            for s in seasons:
                s_id = s['seasonId']
                s_num = s.get('seasonSequenceNumber', 0)
                
                # 2. Obtener Episodios
                url_eps = f"https://disney.content.edge.bamgrid.com/svc/content/DmcEpisodes/version/5.1/region/{code}/audience/k-false,l-true/maturity/1899/language/{lang}/seasonId/{s_id}/pageSize/60/page/1"
                r_eps = requests.get(url_eps, headers=HEADERS)
                eps_data = r_eps.json().get('data', {}).get('DmcEpisodes', {}).get('videos', [])
                
                clean_eps = []
                for ep in eps_data:
                    # Extraer datos mínimos para ahorrar espacio
                    ep_obj = {
                        "n": ep.get('sequenceNumber', 0),
                        "t": ep.get('text', {}).get('title', {}).get('full', {}).get('program', {}).get('default', {}).get('content', 'Sin Título'),
                        "d": ep.get('availabilityDate', ''),
                        # Extraer audio simple
                        "a": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('audioTracks', [])][:3], # Solo primeros 3
                        "s": [x.get('renditionName', x.get('language')) for x in ep.get('mediaMetadata', {}).get('captionTracks', [])][:3]
                    }
                    clean_eps.append(ep_obj)
                    
                    # Chequear Novedad (90 días)
                    if ep_obj['d']:
                        dt = datetime.strptime(ep_obj['d'].split('T')[0], "%Y-%m-%d")
                        delta = (datetime.utcnow() - dt).days
                        if 0 <= delta <= 90:
                            region_data["news"].append(ep_obj)

                region_data["seasons"].append({
                    "num": s_num,
                    "eps": clean_eps
                })
            
            database["regions"][code] = region_data

        except Exception as e:
            print(f"Error en {code}: {str(e)}")

    return database

if __name__ == "__main__":
    data = get_data()
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Escaneo finalizado. database.json guardado.")
