import xml.etree.ElementTree as ET
import requests

# رابط XMLTVFR الكامل
xmltv_url = "https://xmltvfr.fr/xmltv/xmltv.xml"

# تحميل الملف
r = requests.get(xmltv_url)
r.raise_for_status()
root_src = ET.fromstring(r.content)

# القنوات المطلوبة والشعارات
logos = {
    "TF1.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/TF1_logo_1990.svg.png",
    "TF14k.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Tf14k-logo.png",
    "France2.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-2-fr.png",
    "France3.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-3-fr.png",
    "France4.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-4-fr.png",
    "France5.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-5-fr.png",
    "EvenementsSports4KUHD.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Picsart_26-03-21_17-41-51-504.png",
    "CanalPlusFoot.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/SAVE_20260321_185456.jpg",
    "CanalPlus.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/Picsart_26-03-21_19-10-24-004.png",
    "CanalPlusUHD.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/Picsart_26-03-21_19-11-24-727.png",
}

# إنشاء ملف XMLTV جديد
tv = ET.Element("tv")

# إضافة القنوات الموجودة ضمن القائمة المختارة
for ch in root_src.findall("channel"):
    ch_id = ch.attrib["id"]
    if ch_id in logos:
        new_ch = ET.SubElement(tv, "channel", id=ch_id)
        name_elem = ch.find("display-name")
        if name_elem is not None:
            ET.SubElement(new_ch, "display-name").text = name_elem.text
        ET.SubElement(new_ch, "icon", src=logos[ch_id])

# نسخ البرامج الخاصة بالقنوات المختارة
for prog in root_src.findall("programme"):
    ch_id = prog.attrib.get("channel")
    if ch_id in logos:
        new_prog = ET.SubElement(tv, "programme", prog.attrib)
        title = prog.find("title")
        desc = prog.find("desc")
        if title is not None:
            ET.SubElement(new_prog, "title").text = title.text
        if desc is not None:
            ET.SubElement(new_prog, "desc").text = desc.text

# حفظ الملف النهائي
tree = ET.ElementTree(tv)
tree.write("canal_epg_fr_selected.xml", encoding="utf-8", xml_declaration=True)
