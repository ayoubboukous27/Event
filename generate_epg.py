from datetime import datetime, timedelta

channel_id = "canal_plus_evenements_4k"
program_title = "Canal + Événements 4K"
program_desc = "Canal + Événements 4K diffuse les plus grands événements sportifs et culturels en Ultra Haute Définition."
# استبدال رابط الشعار بالرابط الجديد
icon_url = "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Picsart_26-03-21_17-12-28-760.png"

# Commence à l'heure actuelle (UTC) arrondie à l'heure
start_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

# Début du XML
xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
xml += f'  <channel id="{channel_id}">\n'
xml += f'    <display-name>{program_title}</display-name>\n'
xml += f'    <icon src="{icon_url}" />\n'
xml += f'  </channel>\n\n'

# Générer 7 jours * 24 heures
for day in range(7):
    for hour in range(24):
        start = start_time + timedelta(days=day, hours=hour)
        stop = start + timedelta(hours=1)
        xml += f'  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="{channel_id}">\n'
        xml += f'    <title>{program_title}</title>\n'
        xml += f'    <desc>{program_desc}</desc>\n'
        xml += f'  </programme>\n'

xml += "</tv>"

# Écriture dans le fichier
with open("canal_epg.xml", "w", encoding="utf-8") as f:
    f.write(xml)
