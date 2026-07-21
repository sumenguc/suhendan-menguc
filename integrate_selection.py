# -*- coding: utf-8 -*-
"""
_secim/secim_sonuc.json içindeki seçimi okuyup:
  1. Dahil edilen medya dosyalarını (webp/heic->webp zaten önbellekte) `assets/`
     altına gerçek site varlıkları olarak kopyalar (videolar HARİÇ - ayrı konu).
  2. `site_content.json` üretir: build.py'ın okuyup sayfaya basacağı,
     TR/EN/DE çevirileriyle birlikte yapılandırılmış içerik.

Kullanım:  python integrate_selection.py
"""

import io
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SEL_PATH = os.path.join(ROOT, "_secim", "secim_sonuc.json")
ASSETS = os.path.join(ROOT, "assets")

from select_gallery import FB_ALBUMS, FB_TEXTS  # noqa: E402

# ----------------------------------------------------------------------
# Gezi albümü başlıkları — TR / EN / DE (gerçek yer/olay adları)
# ----------------------------------------------------------------------
TRAVEL_META = {
    "Hawaii2014": ("Hawaii, 2014", "Hawaii, 2014", "Hawaii, 2014"),
    "Mallorca2008": ("Mallorca, 2008", "Mallorca, 2008", "Mallorca, 2008"),
    "Prag2009": ("Prag, 2009", "Prague, 2009", "Prag, 2009"),
    "KronolojikGnde": ("Anılarımdan", "From My Memories", "Aus meinen Erinnerungen"),
    "Fotoraflar": ("Fotoğraflar", "Photographs", "Fotografien"),
    "BodenseeEyll20": ("Bodensee, Eylül 2010", "Lake Constance, September 2010", "Bodensee, September 2010"),
    "RotterdamMays2": ("Rotterdam, Mayıs 2011", "Rotterdam, May 2011", "Rotterdam, Mai 2011"),
    "IJsselmeerAust": ("IJsselmeer, Ağustos 2011", "IJsselmeer, August 2011", "IJsselmeer, August 2011"),
    "KellerwegfestA": ("Kellerwegfest, Ağustos 2011", "Kellerwegfest, August 2011", "Kellerwegfest, August 2011"),
    "NewYork2014": ("New York, 2014", "New York, 2014", "New York, 2014"),
    "AkkrumYelkenHa": ("Akkrum Yelken Haftasonu, 2008", "Akkrum Sailing Weekend, 2008", "Akkrum Segelwochenende, 2008"),
    "EveElaubat2011": ("Eve & Ela, Şubat 2011", "Eve & Ela, February 2011", "Eve & Ela, Februar 2011"),
    "SanFrancisco20": ("San Francisco, 2014", "San Francisco, 2014", "San Francisco, 2014"),
    "ShendanMeng": ("Kendi Anılarım", "My Own Memories", "Meine eigenen Erinnerungen"),
    "EliseEyll": ("Elise & Eylül", "Elise & Eylül", "Elise & Eylül"),
    "TribergSchwarz": ("Triberg, Schwarzwald, 2011", "Triberg, Black Forest, 2011", "Triberg, Schwarzwald, 2011"),
    "stanbulAralk20": ("İstanbul, Aralık 2010", "Istanbul, December 2010", "Istanbul, Dezember 2010"),
    "ZrihPaskalyaGe": ("Zürih Paskalya Gezisi, 2009", "Zurich Easter Trip, 2009", "Zürich Osterreise, 2009"),
    "Chicago2014": ("Chicago, 2014", "Chicago, 2014", "Chicago, 2014"),
    "WillingenAralk": ("Willingen, Aralık 2008", "Willingen, December 2008", "Willingen, Dezember 2008"),
    "TrkiyeMart2012": ("Türkiye, Mart 2012", "Türkiye, March 2012", "Türkei, März 2012"),
    "arapTadm": ("Şarap Tadımı", "Wine Tasting", "Weinprobe"),
    "Bozburun": ("Bozburun", "Bozburun", "Bozburun"),
    "YeniEvimizzmir": ("Yeni Evimiz, İzmir", "Our New Home, İzmir", "Unser neues Zuhause, İzmir"),
    "Hawaii20142": ("Hawaii, 2014 (devamı)", "Hawaii, 2014 (continued)", "Hawaii, 2014 (Fortsetzung)"),
    "Noelay": ("Noel Çayı", "Christmas Tea", "Weihnachtstee"),
    "FuldaNisan2012": ("Fulda, Nisan 2012", "Fulda, April 2012", "Fulda, April 2012"),
    "EftymiannDoumG": ("Eftymia'nın Doğum Günü", "Eftymia's Birthday", "Eftymias Geburtstag"),
    "InstagramFotor": ("Instagram Yedeğim", "My Instagram Backup", "Mein Instagram-Archiv"),
    "FrankfurtNisan": ("Frankfurt, Nisan", "Frankfurt, April", "Frankfurt, April"),
}

BLURB_TPL = {
    "tr": "{place}. {n} kareden bir seçki.",
    "en": "{place}. A selection of {n} photos.",
    "de": "{place}. Eine Auswahl von {n} Fotos.",
}

# ----------------------------------------------------------------------
# Gerçek metinler — TX index -> (TR zaten select_gallery.FB_TEXTS içinde)
# Buradaki EN/DE çevirileri elle yazıldı.
# ----------------------------------------------------------------------
TX_TRANSLATIONS = {
    1: {  # Liman notu
        "en": ("Harbour Note", "19 Aug 2025 · Frankfurt/Rhein",
               "The weather was rough yesterday. The harbour filled with boats fleeing the storm. "
               "Early in the morning the wind was from the EAST. Now it has turned NORTH. Rare for "
               "this season. The colour of the sea changes with the wind too. Now it has turned indigo. 🥰"),
        "de": ("Hafennotiz", "19. Aug. 2025 · Frankfurt/Rhein",
               "Gestern war das Wetter rau. Der Hafen füllte sich mit Booten, die vor dem Sturm "
               "flüchteten. Früh am Morgen wehte der Wind aus OST. Jetzt hat er auf NORD gedreht. "
               "Selten für diese Jahreszeit. Auch die Farbe des Meeres ändert sich mit dem Wind. "
               "Jetzt ist sie indigoblau geworden. 🥰"),
    },
    2: {  # Müze izlenimi
        "en": ("A Museum Impression", "Aug 2025 · Städel Museum",
               "What I saw today at the Monet exhibition at the Städel Museum moved me more than "
               "Monet himself. It turned out the child drawing on the floor was a live model. It "
               "took everyone a moment to realise what was real."),
        "de": ("Ein Museumseindruck", "Aug. 2025 · Städel Museum",
               "Was ich heute in der Monet-Ausstellung im Städel Museum sah, berührte mich mehr als "
               "Monet selbst. Das Kind, das auf dem Boden zeichnete, entpuppte sich als lebendes "
               "Modell. Alle brauchten einen Moment, um zu begreifen, was echt war."),
    },
    3: {  # Coğrafya kaderdir
        "en": ("Geography is Destiny", "",
               "My heart stayed there. I could have been born there too. Geography is destiny."),
        "de": ("Geografie ist Schicksal", "",
               "Mein Herz ist dort geblieben. Ich hätte auch dort geboren werden können. "
               "Geografie ist Schicksal."),
    },
    4: {  # Sanat üzerine
        "en": ("On Art", "",
               "When I feel low, art lifts me back up. I don't know how I'd live without it!"),
        "de": ("Über die Kunst", "",
               "Wenn ich mich schlecht fühle, richtet mich die Kunst wieder auf. Ich weiß nicht, "
               "wie ich ohne sie leben könnte!"),
    },
    5: {  # Kitap çıkışı
        "en": ("The Book is Out", "",
               "It finally came out today. A dream two years in the making, through the Covid years, "
               "has come true."),
        "de": ("Das Buch ist da", "",
               "Es ist heute endlich erschienen. Ein Traum, an dem ich zwei Jahre lang, mitten in den "
               "Covid-Jahren, gearbeitet habe, ist wahr geworden."),
    },
    6: {  # Şiirsel an
        "en": ("A Poetic Moment", "",
               "The sun is gone. The light has changed. The air turned cold. I froze. My place is "
               "narrow. The rest is for tomorrow."),
        "de": ("Ein poetischer Moment", "",
               "Die Sonne ist weg. Das Licht hat sich verändert. Die Luft wurde kalt. Ich fror. "
               "Mein Platz ist eng. Der Rest ist für morgen."),
    },
    7: {  # Komşu hikayesi
        "en": ("The Neighbour's Renovation", "Everyday life in Germany",
               "The owner of the house across from us wanted to renew the old front steps. Two days "
               "later three workers showed up with a van full of tools and a container for the "
               "rubble. First they pulled up the cladding stones. Then they started breaking the "
               "concrete underneath with sledgehammers. Of the five steps, after all that hammering "
               "they had only managed to break one. Every now and then I'd feel a tremor from where "
               "I was sitting. \"Is that an earthquake?\" I'd wonder, then remember there's no such "
               "thing here and relax. My husband started grumbling: \"Are you building a bunker "
               "against an air raid or something? What is this? It's a five-step entrance staircase. "
               "Are they planning to jump off the top? Such German thoroughness.\" A little later the "
               "workers gave up trying to break it by hand. The next day they brought a small tracked "
               "breaker. It hammered away all day — TAK TAK TAK — and finished off the remaining four "
               "steps. On the third day, in the morning, it broke up the platform left by the door. "
               "Then a small excavator and a portable toilet arrived. The excavator loaded the big "
               "chunks of concrete from the steps into the container. They fenced off the area around "
               "the house. Not a speck of dust escaped. Now they've started digging around the house. "
               "I think they're about to do the waterproofing."),
        "de": ("Die Renovierung des Nachbarn", "Alltag in Deutschland",
               "Der Besitzer des Hauses gegenüber wollte die alte Außentreppe erneuern. Zwei Tage "
               "später kamen drei Arbeiter mit einem Transporter voller Werkzeug und einem Container "
               "für den Schutt. Zuerst entfernten sie die Verkleidungssteine. Dann begannen sie, den "
               "darunterliegenden Beton mit Vorschlaghämmern zu zerschlagen. Von den fünf Stufen "
               "hatten sie nach all dem Hämmern nur eine geschafft. Ab und zu spürte ich von meinem "
               "Platz aus ein Beben. \"Ist das ein Erdbeben?\", dachte ich, erinnerte mich dann, dass "
               "es hier so etwas nicht gibt, und beruhigte mich. Mein Mann fing an zu schimpfen: "
               "\"Baut ihr einen Bunker gegen Bombenangriffe oder was? Was soll das? Das ist eine "
               "Fünf-Stufen-Eingangstreppe. Wollen die oben drauf springen? So eine deutsche "
               "Gründlichkeit.\" Kurz darauf gaben die Arbeiter den Versuch auf, von Hand weiter zu "
               "zerschlagen. Am nächsten Tag brachten sie einen kleinen Raupenbrecher. Er hämmerte "
               "den ganzen Tag — TAK TAK TAK — und erledigte die restlichen vier Stufen. Am dritten "
               "Tag zerschlug er morgens die verbliebene Plattform vor der Tür. Dann kamen ein kleiner "
               "Bagger und eine mobile Toilette. Der Bagger lud die großen Betonbrocken der Treppe in "
               "den Container. Sie zäunten den Bereich um das Haus ab. Kein Staubkorn entkam. Jetzt "
               "haben sie angefangen, rund um das Haus zu graben. Ich glaube, jetzt kommt die "
               "Abdichtung."),
    },
    8: {  # Yazı dersi anısı
        "en": ("A Writing Class Memory", "",
               "Last night's session at the ONLINE WRITING HOUSE with YEŞİM CİMCOZ, the last class "
               "of the year, went beyond a class. Everything flowed naturally, a little spiritual, "
               "gentle, warm, instructive.. My dear Yeşim ❤️"),
        "de": ("Erinnerung an eine Schreibklasse", "",
               "Die gestrige Sitzung im ONLINE-SCHREIBHAUS bei YEŞİM CİMCOZ, die letzte Klasse des "
               "Jahres, ging über eine gewöhnliche Unterrichtsstunde hinaus. Alles floss wie von "
               "selbst, ein wenig spirituell, sanft, herzlich, lehrreich.. Meine liebe Yeşim ❤️"),
    },
    9: {  # Koro konseri anısı
        "en": ("A Choir Concert Memory", "",
               "Last night was the concert of the choir I've been rehearsing with for a year. "
               "Everyone was so happy. It went well. We got long, warm applause. It was a beautiful "
               "memory for me."),
        "de": ("Erinnerung an ein Chorkonzert", "",
               "Gestern Abend war das Konzert des Chors, mit dem ich seit einem Jahr probe. Alle "
               "waren so glücklich. Es lief gut. Wir bekamen langen, herzlichen Applaus. Für mich "
               "war es eine schöne Erinnerung."),
    },
}

# ----------------------------------------------------------------------
# Instagram caption çevirileri (sadece caption'ı olanlar) — orijinal id -> (en, de)
# ----------------------------------------------------------------------
IG_CAPTION_TR_TO_EN_DE = {
    "Dün hava sertti. Fırtınadan kaçanlarla doldu liman. Sabah erken GÜNDOĞUSU esiyordu. Simdi YILDIZa döndü. Bu mevsimde nadir eser boyle. Denizin rengi de rüzgara göre değişiyor. Şimdi çivit mavisi oldu. 🥰":
        ("The weather was rough yesterday. The harbour filled with boats fleeing the storm. It's rare for this season. 🥰",
         "Gestern war das Wetter rau. Der Hafen füllte sich mit Booten auf der Flucht vor dem Sturm. Selten für diese Jahreszeit. 🥰"),
    "Dün akşam bir yildir calismalarina katildigim koronun konseri vardi. Herkes cok mutluydu. Basarili oldu. Uzun uzun alkiş aldik.  Benim için güzel bir anı oldu.":
        ("Last night was the concert of the choir I've rehearsed with for a year. It went well, long applause — a lovely memory.",
         "Gestern Abend war das Konzert des Chors, mit dem ich seit einem Jahr probe. Es lief gut, langer Applaus — eine schöne Erinnerung."),
    "Karsimizdaki evin eski dış merdivenlerini yenilemek istiyormus sahibi. Iki gun önce üç işçi ,aletleri tasiyan kamyonet ve bir de çıkan molozu koyacakları konteynerle gelip işe başladılar. Önce kaplama taslarini çıkardılar. Sonra balyozlarla basladilar alttaki betonu kirmaya. Hepsi BEŞ basamak olan merdivenlerin vur Allah vur sadece bir basamagini kirabildiler. Arada oturdugum yerden bir titresim duyuyorum. Deprem mi? diyorum. Sonra burada deprem olmadigini hatirlayip rahatliyorum. Kocam söylenmeye basladi. ''Ulan bonbardimana karşı bunker mi yapiyorsunuz? Ne bu be? Hepi topu 5 basamakli ev giris merdiveni. Ordu ustune cikip da ziplayacak mi? Alman abartisi iste'' diye. Biraz sonra adamlar kiramayinca işi":
        ("The neighbour's front steps renovation turned into a days-long, very German ordeal of sledgehammers and machinery.",
         "Die Treppenrenovierung des Nachbarn wurde zu einem tagelangen, sehr deutschen Vorhaben mit Vorschlaghämmern und Maschinen."),
    "Bugün nihayet yillardir istediğimiz  Kastabos Antik Kentine tırmandı. 14 bin adim. Yarısı tırmanma. Şükürler olsun.":
        ("Today we finally climbed up to Kastabos, the ancient city we'd wanted to see for years. 14,000 steps, half of it a climb. So grateful.",
         "Heute sind wir endlich zur antiken Stadt Kastabos hochgestiegen, die wir seit Jahren sehen wollten. 14.000 Schritte, die Hälfte davon Klettern. Sehr dankbar."),
    "HERKESE SAĞLIK, NEŞE, BOLLUK; ÜLKEMIZE ÖZGÜRLÜK, REFAH, ADALET, DÜNYAYA BARIŞ, AKLI BAŞINDA POLITIKACILAR  GELMESINI DILIYORUM.":
        ("Wishing everyone health, joy and abundance; freedom, prosperity and justice for our country; peace for the world, and sensible politicians.",
         "Ich wünsche allen Gesundheit, Freude und Fülle; unserem Land Freiheit, Wohlstand und Gerechtigkeit; der Welt Frieden und vernünftige Politiker."),
    "BU COCUKLAR PIRLANTA!":
        ("These kids are diamonds!", "Diese Kinder sind Diamanten!"),
    "Arkadaşım Mufide Gönenç'in kızı Müge ve torunu Pera  melek oldular. Cenazeler 23 Ocak Perşembe  gunu Urla yeni camiden kaldırılıp birlikte defnedilecekler.":
        ("My friend Mufide Gönenç's daughter Müge and grandchild Pera have passed away. In loving memory.",
         "Die Tochter Müge und das Enkelkind Pera meiner Freundin Mufide Gönenç sind verstorben. In liebevoller Erinnerung."),
    "Akşam, yine akşam, yine akşam. Göllerde bu dem bir kamış olsam. A.HAŞİM":
        ("\"Evening, evening again, evening again. If only I were a reed on the lake now.\" — A. Haşim",
         "\"Abend, wieder Abend, wieder Abend. Wäre ich jetzt doch ein Schilfrohr am See.\" — A. Haşim"),
    "Bugün Rhein kalabalık.":
        ("The Rhein is busy today.", "Der Rhein ist heute voll."),
    "Dün aksam SANAL YAZI EVİNDE  YEŞİM CİMCOZ'UN  bu senenin son dersi ders ötesiydi.Herşey kendiliginden , biraz spritüel, nazik, samimi, öğretici.. Yeşimcim❤️❤️❤️❤️❤️":
        ("Last night's session at the online writing house with Yeşim Cimcoz, the year's last class, went beyond a class. ❤️",
         "Die gestrige Sitzung im Online-Schreibhaus bei Yeşim Cimcoz, die letzte Klasse des Jahres, ging über den Unterricht hinaus. ❤️"),
    "Balkondan günü batırmak.":
        ("Watching the day set from the balcony.", "Vom Balkon aus den Tag untergehen sehen."),
}


def slug_for(label, maxlen):
    return re.sub(r"[^A-Za-z0-9]", "", label)[:maxlen]


def load_selection():
    with io.open(SEL_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [i for i in data["items"] if not i.get("excluded")]


def copy_asset(src_url, dest_rel):
    """src_url: secim_sonuc.json içindeki '/...' yol. dest_rel: assets/altında hedef."""
    src = os.path.join(ROOT, src_url.lstrip("/"))
    dest = os.path.join(ASSETS, dest_rel)
    dest_dir = os.path.dirname(dest)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    shutil.copyfile(src, dest)
    return "assets/" + dest_rel.replace(os.sep, "/")


def main():
    items = load_selection()
    by_id = {i["id"]: i for i in items}

    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)

    # ---- Sanat (Suluboyalar) ----
    art = []
    w_ids = sorted([i for i in by_id if i.startswith("W-")], key=lambda x: int(x.split("-")[1]))
    for n, idv in enumerate(w_ids, 1):
        it = by_id[idv]
        rel = copy_asset(it["path"], "art/%02d.webp" % n)
        art.append({"file": rel})
    print("Sanat:", len(art), "eser kopyalandi")

    # ---- Profil ----
    p_ids = sorted([i for i in by_id if i.startswith("P-")])
    portrait = None
    if p_ids:
        it = by_id[p_ids[0]]
        portrait = copy_asset(it["path"], "profile/portrait.webp")
    print("Portre:", portrait)

    # ---- Gezi albümleri ----
    travel_groups = {}
    for idv, it in by_id.items():
        if not idv.startswith("T-"):
            continue
        parts = idv.split("-")
        slug = parts[1]
        travel_groups.setdefault(slug, []).append((int(parts[2]), it))

    travels = []
    slug_order = [re.sub(r"[^A-Za-z0-9]", "", label)[:14]
                  for folder, label, cat in FB_ALBUMS if cat == "travel"]
    for slug in slug_order:
        if slug not in travel_groups:
            continue
        entries = sorted(travel_groups[slug], key=lambda x: x[0])
        photos = []
        for n, (_, it) in enumerate(entries, 1):
            rel = copy_asset(it["path"], "travels/%s/%02d.webp" % (slug, n))
            photos.append(rel)
        title_tr, title_en, title_de = TRAVEL_META.get(slug, (slug, slug, slug))
        travels.append({
            "slug": slug,
            "title": {"tr": title_tr, "en": title_en, "de": title_de},
            "blurb": {
                "tr": BLURB_TPL["tr"].format(place=title_tr, n=len(photos)),
                "en": BLURB_TPL["en"].format(place=title_en, n=len(photos)),
                "de": BLURB_TPL["de"].format(place=title_de, n=len(photos)),
            },
            "photos": photos,
        })
    print("Gezi albumu:", len(travels), "toplam foto:", sum(len(t["photos"]) for t in travels))

    # ---- Instagram kareleri ----
    ig_ids = sorted([i for i in by_id if i.startswith("IG-")], key=lambda x: int(x.split("-")[1]))
    ig_moments = []
    for n, idv in enumerate(ig_ids, 1):
        it = by_id[idv]
        rel = copy_asset(it["path"], "instagram/%02d.webp" % n)
        cap_tr = it.get("caption") or ""
        cap_en, cap_de = "", ""
        if cap_tr in IG_CAPTION_TR_TO_EN_DE:
            cap_en, cap_de = IG_CAPTION_TR_TO_EN_DE[cap_tr]
        ig_moments.append({
            "file": rel,
            "caption": {"tr": cap_tr, "en": cap_en, "de": cap_de},
        })
    print("Instagram karesi:", len(ig_moments))

    # ---- Gerçek metinler (TX) ----
    stories_idx = [7, 8, 9, 5]   # anlatı niteliğinde olanlar
    thoughts_idx = [1, 2, 3, 4, 6]  # kısa/felsefi olanlar

    stories = []
    for i in stories_idx:
        if "TX-%d" % i not in by_id:
            continue
        title_tr, meta_tr, text_tr = FB_TEXTS[i - 1]
        tr_data = TX_TRANSLATIONS[i]
        stories.append({
            "title": {"tr": title_tr, "en": tr_data["en"][0], "de": tr_data["de"][0]},
            "meta": {"tr": meta_tr, "en": tr_data["en"][1], "de": tr_data["de"][1]},
            "text": {"tr": text_tr, "en": tr_data["en"][2], "de": tr_data["de"][2]},
        })

    thoughts = []
    for i in thoughts_idx:
        if "TX-%d" % i not in by_id:
            continue
        title_tr, meta_tr, text_tr = FB_TEXTS[i - 1]
        tr_data = TX_TRANSLATIONS[i]
        thoughts.append({
            "text": {"tr": text_tr, "en": tr_data["en"][2], "de": tr_data["de"][2]},
        })
    print("Hikaye:", len(stories), "Dusunce:", len(thoughts))

    content = {
        "art": art,
        "portrait": portrait,
        "travels": travels,
        "ig_moments": ig_moments,
        "stories": stories,
        "thoughts": thoughts,
    }
    out_path = os.path.join(ROOT, "site_content.json")
    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print("Yazildi:", out_path)


if __name__ == "__main__":
    main()
