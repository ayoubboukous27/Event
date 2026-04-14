import xml.etree.ElementTree as ET
import requests

# رابط XMLTVFR الكامل
xmltv_url = "https://xmltvfr.fr/xmltv/xmltv.xml"

# تحميل الملف
r = requests.get(xmltv_url)
r.raise_for_status()
root_src = ET.fromstring(r.content)

# القنوات والشعارات
logos = {
"TF1.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/TF1.png",
"TF14k.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/TF1-4K.png",
"France2.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-2-fr.png",
"France24k.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/F2-UHD.png",
"France3.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-3-fr.png",
"France4.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-4-fr.png",
"France5.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-5-fr.png",
}

# إنشاء ملف XMLTV جديد
tv = ET.Element("tv")

# نسخ القنوات
for ch in root_src.findall("channel"):
    ch_id = ch.attrib["id"]
    if ch_id in logos:
        # القناة الأصلية
        new_ch = ET.SubElement(tv, "channel", id=ch_id)
        name_elem = ch.find("display-name")
        if name_elem is not None:
            ET.SubElement(new_ch, "display-name").text = name_elem.text
        ET.SubElement(new_ch, "icon", src=logos[ch_id])
        # نسخة 4K لـ France2
        if ch_id == "France2.fr":
            new_ch_4k = ET.SubElement(tv, "channel", id="France24k.fr")
            ET.SubElement(new_ch_4k, "display-name").text = "France 2 4K"
            ET.SubElement(new_ch_4k, "icon", src=logos["France24k.fr"])

# نسخ البرامج
for prog in root_src.findall("programme"):
    ch_id = prog.attrib.get("channel")
    if ch_id in logos:
        # البرنامج الأصلي
        new_prog = ET.SubElement(tv, "programme", prog.attrib)
        for tag in ["title", "desc", "category", "sub-title", "date"]:
            elem = prog.find(tag)
            if elem is not None:
                ET.SubElement(new_prog, tag).text = elem.text

        # إذا كانت France2.fr ننسخ البرنامج أيضا لـ 4K
        if ch_id == "France2.fr":
            new_attrib = prog.attrib.copy()
            new_attrib["channel"] = "France24k.fr"
            new_prog_4k = ET.SubElement(tv, "programme", new_attrib)
            for tag in ["title", "desc", "category", "sub-title", "date"]:
                elem = prog.find(tag)
                if elem is not None:
                    ET.SubElement(new_prog_4k, tag).text = elem.text

# حفظ الملف النهائي
tree = ET.ElementTree(tv)
tree.write("canal_epg_fr_selected.xml", encoding="utf-8", xml_declaration=True)
