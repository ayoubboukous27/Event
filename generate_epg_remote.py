import xml.etree.ElementTree as ET
import requests

# رابط XMLTVFR للقناة الأصلية
url = "https://xmltvfr.fr/xmltv/xmltv.xml"

# جلب الملف
r = requests.get(url)
r.raise_for_status()

root_src = ET.fromstring(r.content)

# إنشاء TV جديد
tv = ET.Element("tv")

# إضافة القناة مع شعارك الجديد
channel = ET.SubElement(tv, "channel", id="canal_plus_evenements_4k")
ET.SubElement(channel, "display-name").text = "Canal + Événements 4K"
ET.SubElement(channel, "icon", src="https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Picsart_26-03-21_17-12-28-760.png")

# نسخ جميع برامج القناة الأصلية مع تغيير الاسم
for prog in root_src.findall('programme[@channel="EvenementsSports4KUHD.fr"]'):
    new_prog = ET.SubElement(tv, "programme", {
        "start": prog.attrib["start"],
        "stop": prog.attrib["stop"],
        "channel": "canal_plus_evenements_4k"
    })
    title = prog.find("title")
    desc = prog.find("desc")
    if title is not None:
        ET.SubElement(new_prog, "title").text = title.text
    if desc is not None:
        ET.SubElement(new_prog, "desc").text = desc.text

# حفظ الملف الجديد
tree = ET.ElementTree(tv)
tree.write("canal_epg_remote.xml", encoding="utf-8", xml_declaration=True)
