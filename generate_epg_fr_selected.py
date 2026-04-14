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
"TF1.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/TF1.png",
"TF14k.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/TF1-4K.png",
"France2.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-2-fr.png",
"France24k.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/F2-UHD.png",
"France3.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-3-fr.png",
"France4.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-4-fr.png",
"France5.fr": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/france/france-5-fr.png",
"EvenementsSports4KUHD.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/%C3%A9v%C3%A9nement-4k.png",
"CanalPlusFoot.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/Canal+FootProto2023.png",
"CanalPlus.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/Picsart_26-03-21_20-33-02-272.png",
"CanalPlusUHD.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/Picsart_26-03-21_20-20-08-937.png",
"M6.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/M6.png",
"CanalPlusPremierLeague.fr": "https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/%2Bpremier_league.png",
"CanalPlusKIDS.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/Canal+KidsProto2023.png",
"CanalPlusSport.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/Canal+SportProto2023.png",
"CanalPlusSport360.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/Canal+Sport360Proto2023.png",
"beINSPORTS1.fr": "https://github.com/tv-logo/tv-logos/raw/refs/heads/main/countries/world-middle-east/bein-sports/bein-sports-1-french-mea.png",
"beINSPORTS2.fr": "https://github.com/tv-logo/tv-logos/raw/refs/heads/main/countries/world-middle-east/bein-sports/bein-sports-2-french-mea.png",
"beINSPORTS3.fr": "https://github.com/tv-logo/tv-logos/raw/refs/heads/main/countries/world-middle-east/bein-sports/bein-sports-3-french-mea.png",
"FranceTVDocs.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/France_TV_Docs_Short.png",
"FranceTVSeries.fr": "https://github.com/ayoubboukous27/Event/raw/refs/heads/main/Logos/France_TV_S%C3%A9ries_Short.png",
}

# إضافة Canal+ Live 1 → 10
for i in range(1, 11):
    channel_id = f"CanalPlusLive{i}.fr"
    logos[channel_id] = f"https://raw.githubusercontent.com/ayoubboukous27/Event/refs/heads/main/Logos/live{i}.png"

# إنشاء ملف XMLTV جديد
tv = ET.Element("tv")

# إضافة القنوات المختارة
for ch in root_src.findall("channel"):
    ch_id = ch.attrib["id"]
    if ch_id in logos:
        new_ch = ET.SubElement(tv, "channel", id=ch_id)
        name_elem = ch.find("display-name")
        if name_elem is not None:
            ET.SubElement(new_ch, "display-name").text = name_elem.text
        ET.SubElement(new_ch, "icon", src=logos[ch_id])
        if ch_id == "France2.fr":
            new_ch_4k = ET.SubElement(tv, "channel", id="France24k.fr")
            ET.SubElement(new_ch_4k, "display-name").text = "France 2 4K"
            ET.SubElement(new_ch_4k, "icon", src=logos["France24k.fr"])

# نسخ البرامج للقنوات المختارة
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
        if ch_id == "France2.fr":
            new_attrib = prog.attrib.copy()
            new_attrib["channel"] = "France24k.fr"
            new_prog_4k = ET.SubElement(tv, "programme", new_attrib)
            if title is not None:
                ET.SubElement(new_prog_4k, "title").text = title.text
            if desc is not None:
                ET.SubElement(new_prog_4k, "desc").text = desc.text

# حفظ الملف النهائي
tree = ET.ElementTree(tv)
tree.write("canal_epg_fr_selected.xml", encoding="utf-8", xml_declaration=True)
