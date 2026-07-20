# -*- coding: utf-8 -*-
"""
Sühendan Mengüç - site üreteci.

Tüm içerik ve tasarım bu dosyada tutulur; `python build.py` çalıştırıldığında
şu dosyalar üretilir:

    index.html      (Türkçe)
    en/index.html   (İngilizce)
    de/index.html   (Almanca)
    sitemap.xml
    robots.txt
    404.html

Metinleri değiştirmek için aşağıdaki CONTENT sözlüğünü düzenleyip betiği
yeniden çalıştırmak yeterli. HTML dosyalarını elle düzenleme - üzerine yazılır.
"""

import os
import io

SITE = "https://suhendanmenguc.com"
LASTMOD = "2026-07-20"

# Dil kodu -> (html lang, URL yolu, klasör)
LANGS = {
    "tr": ("tr", "/", ""),
    "en": ("en", "/en/", "en"),
    "de": ("de", "/de/", "de"),
}

META = {
    "tr": {
        "title": "Sühendan Mengüç — Ressam, Yazar ve Gezgin",
        "desc": "Ressam, yazar ve gezgin Sühendan Mengüç'ün kişisel sitesi. "
                "Yağlı boya ve suluboya resimleri, kısa hikayeleri, gezi notları "
                "ve hayata dair düşünceleri.",
        "locale": "tr_TR",
    },
    "en": {
        "title": "Sühendan Mengüç — Painter, Writer and Traveler",
        "desc": "The personal site of Sühendan Mengüç, painter, writer and traveler. "
                "Oil and watercolour paintings, short stories, travel notes and "
                "reflections on life.",
        "locale": "en_GB",
    },
    "de": {
        "title": "Sühendan Mengüç — Malerin, Autorin und Reisende",
        "desc": "Die persönliche Seite von Sühendan Mengüç, Malerin, Autorin und "
                "Reisende. Ölbilder und Aquarelle, Kurzgeschichten, Reisenotizen "
                "und Gedanken über das Leben.",
        "locale": "de_DE",
    },
}

NAV = {
    "tr": ["Hakkımda", "Resimlerim", "Hikayelerim", "Gezilerim", "Düşüncelerim"],
    "en": ["About", "Paintings", "Stories", "Travels", "Thoughts"],
    "de": ["Über mich", "Bilder", "Geschichten", "Reisen", "Gedanken"],
}

HERO = {
    "tr": ("Ressam · Yazar · Gezgin",
           "Renklerle, kelimelerle ve yollarla dokunmuş bir hayat. Resimlerimi, "
           "hikayelerimi, gezilerimi ve hayata dair düşüncelerimi burada paylaşıyorum.",
           "Eserleri Keşfet"),
    "en": ("Painter · Writer · Traveler",
           "A life woven from colours, words and roads. Here I share my paintings, "
           "my stories, my travels and my thoughts on life.",
           "Explore the Works"),
    "de": ("Malerin · Autorin · Reisende",
           "Ein Leben, gewebt aus Farben, Worten und Wegen. Hier teile ich meine "
           "Bilder, meine Geschichten, meine Reisen und meine Gedanken über das Leben.",
           "Werke entdecken"),
}

ABOUT = {
    "tr": ("Hakkımda", "Portre fotoğrafı",
           "Merhaba, ben Sühendan. Ömrümü resim yaparak, hikayeler yazarak ve dünyayı "
           "gezerek geçiriyorum. Bir tuvalin önünde ya da tanımadığım bir şehrin "
           "sokaklarında kendimi en canlı hissediyorum.",
           "Bana göre sanat, yaşamı daha dikkatli görmenin bir yolu. Bu sayfa da o "
           "dikkatin küçük bir günlüğü: gördüklerim, hissettiklerim ve merak ettiğim "
           "sorular."),
    "en": ("About Me", "Portrait photo",
           "Hello, I'm Sühendan. I spend my life painting, writing stories and "
           "travelling the world. I feel most alive in front of a canvas or in the "
           "streets of a city I don't yet know.",
           "To me, art is a way of seeing life more attentively. This page is a small "
           "diary of that attention: what I see, what I feel and the questions I keep "
           "wondering about."),
    "de": ("Über mich", "Porträtfoto",
           "Hallo, ich bin Sühendan. Ich verbringe mein Leben mit Malen, dem Schreiben "
           "von Geschichten und dem Reisen durch die Welt. Am lebendigsten fühle ich "
           "mich vor einer Leinwand oder in den Straßen einer Stadt, die ich noch "
           "nicht kenne.",
           "Für mich ist Kunst eine Art, das Leben aufmerksamer zu sehen. Diese Seite "
           "ist ein kleines Tagebuch dieser Aufmerksamkeit: was ich sehe, was ich "
           "fühle und die Fragen, über die ich immer wieder nachdenke."),
}

ART_STYLE = [
    "linear-gradient(135deg,#ff8a5b,#ff5a5f)",
    "linear-gradient(135deg,#29c7d6,#0a7fa3)",
    "linear-gradient(135deg,#ffc13d,#ff8a3d)",
    "linear-gradient(135deg,#b15bd6,#6a2fb0)",
    "linear-gradient(135deg,#7fd94a,#0e9e8e)",
    "linear-gradient(135deg,#ff5aa5,#c02f7a)",
]

ART_HEAD = {
    "tr": ("Resimlerim", "Tuvale bıraktığım renkler ve anlar."),
    "en": ("Paintings", "The colours and moments I leave on the canvas."),
    "de": ("Bilder", "Die Farben und Augenblicke, die ich auf der Leinwand hinterlasse."),
}

ART = {
    "tr": [("Sabahın İlk Işığı", "Tuval üzerine yağlı boya"),
           ("Deniz Kıyısında", "Suluboya"),
           ("Sonbahar Bahçesi", "Akrilik"),
           ("Gece ve Sessizlik", "Karışık teknik"),
           ("Zeytin Ağaçları", "Tuval üzerine yağlı boya"),
           ("Bir Portre Denemesi", "Kömür kalem")],
    "en": [("First Light of Morning", "Oil on canvas"),
           ("By the Sea", "Watercolour"),
           ("Autumn Garden", "Acrylic"),
           ("Night and Silence", "Mixed media"),
           ("Olive Trees", "Oil on canvas"),
           ("A Portrait Study", "Charcoal")],
    "de": [("Erstes Morgenlicht", "Öl auf Leinwand"),
           ("Am Meer", "Aquarell"),
           ("Herbstgarten", "Acryl"),
           ("Nacht und Stille", "Mischtechnik"),
           ("Olivenbäume", "Öl auf Leinwand"),
           ("Eine Porträtstudie", "Kohlezeichnung")],
}

STORY_HEAD = {
    "tr": ("Hikayelerim", "Kelimelerle kurduğum küçük dünyalar.", "Devamını oku →"),
    "en": ("Stories", "Small worlds I build with words.", "Read more →"),
    "de": ("Geschichten", "Kleine Welten, die ich mit Worten erschaffe.", "Weiterlesen →"),
}

STORIES = {
    "tr": [
        ("Rüzgârın Getirdiği Mektup",
         "Bir sonbahar sabahı, kapımın önünde adı olmayan bir mektup buldum…",
         "Zarfın içinden çıkan tek bir cümle vardı: &quot;Beklediğin şey aslında seni "
         "bekliyor.&quot; O gün, yıllardır ertelediğim yolculuğa çıkmaya karar verdim. "
         "Bazen bir cümle, bütün bir hayatı yerinden oynatmaya yeter."),
        ("Şehrin En Sessiz Saati",
         "Herkes uyurken uyanık kalanların bildiği bir sır vardır…",
         "Gece yarısını geçen o saatlerde şehir, gündüz taşıdığı bütün maskeleri "
         "çıkarır. Sokak lambaları altında yürürken, kendimi ilk kez gerçekten yalnız "
         "değil, sadece sakin hissettim."),
        ("İki Fincan Kahve",
         "Yıllar sonra aynı masada, aynı iki fincan…",
         "Konuşmadık. Konuşmaya gerek yoktu. Bazı dostluklar, aradan geçen zamanı hiç "
         "yaşanmamış gibi siler ve sizi tam bıraktığınız yerden alır. Kahveler soğudu "
         "ama biz ısındık."),
    ],
    "en": [
        ("A Letter Brought by the Wind",
         "One autumn morning, I found a nameless letter at my door…",
         "Inside the envelope there was a single sentence: &quot;What you are waiting "
         "for is actually waiting for you.&quot; That day, I decided to set out on the "
         "journey I had postponed for years. Sometimes one sentence is enough to move "
         "an entire life."),
        ("The Quietest Hour of the City",
         "There is a secret known to those who stay awake while everyone sleeps…",
         "In those hours past midnight, the city takes off all the masks it wears by "
         "day. Walking under the streetlights, for the first time I felt not truly "
         "alone, but simply calm."),
        ("Two Cups of Coffee",
         "Years later, at the same table, the same two cups…",
         "We didn't speak. There was no need to. Some friendships erase the time in "
         "between as if it never happened, and pick you up right where you left off. "
         "The coffees went cold, but we grew warm."),
    ],
    "de": [
        ("Ein vom Wind gebrachter Brief",
         "An einem Herbstmorgen fand ich vor meiner Tür einen Brief ohne Namen…",
         "Im Umschlag stand nur ein einziger Satz: &quot;Worauf du wartest, wartet in "
         "Wahrheit auf dich.&quot; An jenem Tag beschloss ich, die Reise anzutreten, "
         "die ich jahrelang aufgeschoben hatte. Manchmal genügt ein einziger Satz, um "
         "ein ganzes Leben in Bewegung zu setzen."),
        ("Die stillste Stunde der Stadt",
         "Es gibt ein Geheimnis, das nur jene kennen, die wach bleiben, während alle "
         "schlafen…",
         "In jenen Stunden nach Mitternacht legt die Stadt alle Masken ab, die sie "
         "tagsüber trägt. Als ich unter den Straßenlaternen ging, fühlte ich mich zum "
         "ersten Mal nicht wirklich allein, sondern einfach ruhig."),
        ("Zwei Tassen Kaffee",
         "Jahre später, am selben Tisch, dieselben zwei Tassen…",
         "Wir sprachen nicht. Es war nicht nötig. Manche Freundschaften löschen die "
         "dazwischenliegende Zeit, als hätte es sie nie gegeben, und holen dich genau "
         "dort ab, wo du aufgehört hast. Der Kaffee wurde kalt, doch uns wurde warm."),
    ],
}

TRAVEL_STYLE = [
    ("linear-gradient(135deg,#12b3a6,#0a6f8a)", "✈"),
    ("linear-gradient(135deg,#ffb03d,#ff6a3d)", "☀"),
    ("linear-gradient(135deg,#29c7d6,#0e9e8e)", "⛰"),
]

TRAVEL_HEAD = {
    "tr": ("Gezilerim", "Adımlarımın ve merakımın izinden."),
    "en": ("Travels", "Following my steps and my curiosity."),
    "de": ("Reisen", "Den Spuren meiner Schritte und meiner Neugier folgend."),
}

TRAVELS = {
    "tr": [
        ("Kapadokya, Türkiye", "Peri Bacaları ve Balonlar",
         "Şafak sökerken gökyüzünü dolduran onlarca balonu izlemek, hayatımda gördüğüm "
         "en dingin manzaralardan biriydi. Taşların binlerce yıllık sabrı insana ölçek "
         "kazandırıyor."),
        ("Toskana, İtalya", "Tepelerdeki Sarı Işık",
         "Zeytinlikler arasında kaybolduğum o öğleden sonra, neden bu kadar çok "
         "ressamın buraya geldiğini anladım. Işık burada boya gibi akıyor."),
        ("Lizbon, Portekiz", "Yokuşlar ve Tramvaylar",
         "Sarı tramvayların çıngırağı, çinili duvarlar ve okyanusa bakan meydanlar… "
         "Lizbon, hüznü bile güzel yaşamayı bilen bir şehir."),
    ],
    "en": [
        ("Cappadocia, Türkiye", "Fairy Chimneys and Balloons",
         "Watching dozens of balloons fill the sky at dawn was one of the most serene "
         "sights I have ever seen. The thousand-year patience of the stones gives a "
         "person a sense of scale."),
        ("Tuscany, Italy", "The Yellow Light on the Hills",
         "The afternoon I lost myself among the olive groves, I understood why so many "
         "painters came here. The light flows like paint."),
        ("Lisbon, Portugal", "Slopes and Trams",
         "The bell of the yellow trams, tiled walls and squares facing the ocean… "
         "Lisbon is a city that knows how to live even its melancholy beautifully."),
    ],
    "de": [
        ("Kappadokien, Türkei", "Feenkamine und Ballons",
         "Bei Sonnenaufgang Dutzende Ballons den Himmel füllen zu sehen, war einer der "
         "friedlichsten Anblicke meines Lebens. Die tausendjährige Geduld der Felsen "
         "verleiht dem Menschen ein Gefühl für Maßstab."),
        ("Toskana, Italien", "Das gelbe Licht auf den Hügeln",
         "An dem Nachmittag, als ich mich zwischen den Olivenhainen verlor, verstand "
         "ich, warum so viele Maler hierherkamen. Das Licht fließt hier wie Farbe."),
        ("Lissabon, Portugal", "Steigungen und Straßenbahnen",
         "Das Klingeln der gelben Straßenbahnen, gekachelte Wände und Plätze mit Blick "
         "aufs Meer… Lissabon ist eine Stadt, die selbst ihre Melancholie schön zu "
         "leben weiß."),
    ],
}

THOUGHT_HEAD = {
    "tr": ("Düşüncelerim", "Hayata dair, üzerine düşündüğüm sorular."),
    "en": ("Thoughts", "Questions about life that I keep pondering."),
    "de": ("Gedanken", "Fragen über das Leben, über die ich immer wieder nachdenke."),
}

THOUGHTS = {
    "tr": ["Belki de mutluluk bir varış noktası değil, dikkatimizi verdiğimiz her anın "
           "içinde saklı küçük bir alışkanlıktır.",
           "Bir resmi bitiren ressam değil, ona bakan gözdür. Aynı şey hayat için de "
           "geçerli: anlamı biz veririz.",
           "Yolculuk, gittiğimiz yeri değil, geri döndüğümüzde farklılaşan bakışımızı "
           "değiştirir.",
           "Sessizlik boşluk değildir; çoğu zaman en gürültülü düşüncelerimizi "
           "duyabildiğimiz tek yerdir."],
    "en": ["Perhaps happiness is not a destination, but a small habit hidden inside "
           "every moment we truly pay attention to.",
           "It is not the painter who finishes a painting, but the eye that beholds "
           "it. The same is true of life: we are the ones who give it meaning.",
           "Travel does not change the place we go to; it changes the way we look once "
           "we return.",
           "Silence is not emptiness; it is often the only place where we can hear our "
           "loudest thoughts."],
    "de": ["Vielleicht ist Glück kein Ziel, sondern eine kleine Gewohnheit, verborgen "
           "in jedem Augenblick, dem wir wirklich Aufmerksamkeit schenken.",
           "Nicht die Malerin vollendet ein Bild, sondern das Auge, das es betrachtet. "
           "Dasselbe gilt für das Leben: Wir sind es, die ihm Sinn geben.",
           "Das Reisen verändert nicht den Ort, an den wir gehen, sondern den Blick, "
           "mit dem wir zurückkehren.",
           "Stille ist keine Leere; oft ist sie der einzige Ort, an dem wir unsere "
           "lautesten Gedanken hören können."],
}

FOOTER = {
    "tr": ("Ressam · Yazar · Gezgin", "İletişim", "Instagram", "E-posta",
           "© 2026 Sühendan Mengüç · Tüm hakları saklıdır."),
    "en": ("Painter · Writer · Traveler", "Contact", "Instagram", "Email",
           "© 2026 Sühendan Mengüç · All rights reserved."),
    "de": ("Malerin · Autorin · Reisende", "Kontakt", "Instagram", "E-Mail",
           "© 2026 Sühendan Mengüç · Alle Rechte vorbehalten."),
}

CSS = """
    :root {
      --cream: #f2fbf7;
      --cream-2: #d3f3ea;
      --terracotta: #ff5a5f;
      --brown: #0e9e8e;
      --ink: #0c3b34;
      --muted: #4a726a;
      --serif: Georgia, "Times New Roman", serif;
      --sans: -apple-system, "Segoe UI", Roboto, Helvetica, sans-serif;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 80px; }
    body {
      font-family: var(--sans); background: var(--cream);
      color: var(--ink); line-height: 1.7;
    }
    h1, h2, h3 { font-family: var(--serif); font-weight: 400; line-height: 1.25; }
    header {
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 0.5rem 1rem; padding: 0.9rem 2rem;
      background: rgba(242, 251, 247, 0.92); backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--cream-2);
    }
    .brand {
      font-family: var(--serif); font-size: 1.25rem; letter-spacing: 0.5px;
      color: var(--ink); white-space: nowrap; text-decoration: none;
    }
    nav { display: flex; align-items: center; flex-wrap: wrap; gap: 0.3rem 1.2rem; }
    nav a { color: var(--muted); text-decoration: none; font-size: 0.9rem; transition: color 0.2s; }
    nav a:hover { color: var(--terracotta); }
    .langs { display: flex; gap: 0.35rem; margin-left: 0.5rem; }
    .lang-btn {
      display: inline-block; text-decoration: none; background: transparent;
      color: var(--muted); border: 1px solid #a9d9cd; padding: 0.25rem 0.6rem;
      border-radius: 6px; font-size: 0.72rem; font-weight: 700;
      letter-spacing: 0.5px; transition: all 0.2s;
    }
    .lang-btn:hover { border-color: var(--terracotta); color: var(--terracotta); }
    .lang-btn[aria-current="true"] {
      background: var(--terracotta); border-color: var(--terracotta); color: #fff;
    }
    section { max-width: 1080px; margin: 0 auto; padding: 5rem 2rem; }
    .section-title { font-size: 2rem; color: var(--brown); margin-bottom: 0.4rem; }
    .section-lead {
      color: var(--muted); font-style: italic; margin-bottom: 2.5rem; max-width: 640px;
    }
    .hero {
      max-width: none; min-height: 92vh; display: flex; flex-direction: column;
      justify-content: center; align-items: center; text-align: center;
      padding-top: 6rem;
      background:
        radial-gradient(circle at 25% 18%, rgba(255, 90, 95, 0.16), transparent 55%),
        radial-gradient(circle at 78% 30%, rgba(255, 193, 61, 0.20), transparent 50%),
        radial-gradient(circle at 70% 80%, rgba(14, 158, 142, 0.20), transparent 55%),
        var(--cream);
    }
    .hero h1 {
      font-size: clamp(2.6rem, 6vw, 4.6rem); color: var(--ink); margin-bottom: 0.8rem;
    }
    .hero .roles {
      font-family: var(--serif); font-style: italic;
      font-size: clamp(1.1rem, 2.2vw, 1.5rem); color: #7d2ecc;
      letter-spacing: 1px; margin-bottom: 1.5rem;
    }
    .hero p { max-width: 560px; color: var(--muted); margin-bottom: 2.2rem; }
    .hero-cta {
      display: inline-block; background: var(--terracotta); color: #fff;
      text-decoration: none; padding: 0.85rem 2rem; border-radius: 50px;
      font-weight: 600; transition: transform 0.2s, box-shadow 0.2s;
    }
    .hero-cta:hover { transform: translateY(-3px); box-shadow: 0 12px 26px rgba(255, 90, 95, 0.3); }
    #about { display: grid; grid-template-columns: 260px 1fr; gap: 3rem; align-items: center; }
    .portrait {
      aspect-ratio: 3 / 4; border-radius: 12px;
      background: linear-gradient(135deg, #6fe0cb, #0e9e8e);
      display: flex; align-items: center; justify-content: center; color: #fff;
      font-style: italic; text-align: center; padding: 1rem;
      box-shadow: 0 14px 30px rgba(12, 59, 52, 0.18);
    }
    .about-text h2 { margin-bottom: 1rem; }
    .about-text p + p { margin-top: 1rem; }
    .alt { background: var(--cream-2); max-width: none; }
    .alt > .inner { max-width: 1080px; margin: 0 auto; }
    .gallery-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 1.5rem;
    }
    .art {
      background: var(--cream); border-radius: 10px; overflow: hidden;
      box-shadow: 0 8px 20px rgba(12, 59, 52, 0.08); cursor: pointer;
      transition: transform 0.25s, box-shadow 0.25s;
    }
    .art:hover { transform: translateY(-5px); box-shadow: 0 16px 32px rgba(12, 59, 52, 0.16); }
    .art .thumb {
      aspect-ratio: 4 / 3; background-size: cover; background-position: center;
      display: flex; align-items: center; justify-content: center; color: #fff;
      font-family: var(--serif); font-size: 1.4rem;
    }
    .art .caption { padding: 0.9rem 1rem 1.1rem; }
    .art .caption h3 { font-size: 1.1rem; margin-bottom: 0.2rem; }
    .art .caption span { font-size: 0.82rem; color: var(--muted); }
    .stories { display: flex; flex-direction: column; gap: 1.2rem; }
    .story {
      background: var(--cream); border: 1px solid var(--cream-2);
      border-left: 4px solid var(--terracotta); border-radius: 8px;
      padding: 1.4rem 1.6rem; cursor: pointer; transition: box-shadow 0.2s;
    }
    .story:hover { box-shadow: 0 10px 24px rgba(12, 59, 52, 0.1); }
    .story h3 { font-size: 1.25rem; margin-bottom: 0.3rem; }
    .story .excerpt { color: var(--muted); }
    .story .full { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
    .story.open .full { max-height: 600px; }
    .story .full p { margin-top: 1rem; }
    .story .more {
      display: inline-block; margin-top: 0.8rem; color: var(--terracotta);
      font-size: 0.85rem; font-weight: 600;
    }
    .travels { display: flex; flex-direction: column; gap: 2.5rem; }
    .travel { display: grid; grid-template-columns: 300px 1fr; gap: 2rem; align-items: center; }
    .travel:nth-child(even) .photo { order: 2; }
    .travel .photo {
      aspect-ratio: 4 / 3; border-radius: 10px; background-size: cover;
      background-position: center; display: flex; align-items: center;
      justify-content: center; color: #fff; font-family: var(--serif);
      box-shadow: 0 12px 26px rgba(12, 59, 52, 0.14);
    }
    .travel .place {
      font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; color: var(--terracotta);
    }
    .travel h3 { font-size: 1.5rem; margin: 0.2rem 0 0.6rem; }
    .travel p { color: var(--muted); }
    .thoughts {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem;
    }
    .thought {
      background: var(--cream); border-radius: 10px; padding: 2rem 1.8rem;
      box-shadow: 0 8px 20px rgba(12, 59, 52, 0.07); position: relative;
    }
    .thought::before {
      content: "\\201C"; font-family: var(--serif); font-size: 4rem;
      color: rgba(255, 90, 95, 0.28); position: absolute; top: 0.2rem; left: 1rem; line-height: 1;
    }
    .thought p {
      font-family: var(--serif); font-size: 1.08rem; font-style: italic;
      color: var(--ink); margin-top: 1rem;
    }
    footer { background: var(--ink); color: #b9d6ce; text-align: center; padding: 2.5rem 2rem; }
    footer .fname { font-family: var(--serif); font-size: 1.3rem; color: var(--cream); margin-bottom: 0.5rem; }
    footer .links { margin: 0.8rem 0 1rem; display: flex; gap: 1.2rem; justify-content: center; flex-wrap: wrap; }
    footer .links a { color: #b9d6ce; text-decoration: none; font-size: 0.9rem; border-bottom: 1px dotted #4a726a; }
    footer .links a:hover { color: #fff; }
    footer small { color: #7fa79d; font-size: 0.8rem; }
    .lightbox {
      display: none; position: fixed; inset: 0; z-index: 200;
      background: rgba(12, 59, 52, 0.9); align-items: center; justify-content: center; padding: 2rem;
    }
    .lightbox.show { display: flex; }
    .lightbox .box { max-width: 640px; width: 100%; background: var(--cream); border-radius: 12px; overflow: hidden; }
    .lightbox .lb-img {
      aspect-ratio: 4 / 3; background-size: cover; background-position: center;
      display: flex; align-items: center; justify-content: center; color: #fff;
      font-family: var(--serif); font-size: 2rem;
    }
    .lightbox .lb-cap { padding: 1.2rem 1.5rem 1.6rem; }
    .lightbox .lb-cap h3 { font-size: 1.4rem; margin-bottom: 0.3rem; }
    .lightbox .lb-cap span { color: var(--muted); }
    .lightbox .close {
      position: absolute; top: 1.5rem; right: 2rem; color: #fff; font-size: 2.2rem;
      cursor: pointer; line-height: 1; background: none; border: none;
    }
    @media (max-width: 760px) {
      section { padding: 3.5rem 1.4rem; }
      #about { grid-template-columns: 1fr; }
      .portrait { max-width: 260px; margin: 0 auto; }
      .travel, .travel:nth-child(even) .photo { grid-template-columns: 1fr; order: 0; }
      header { padding: 0.8rem 1.2rem; }
      nav { gap: 0.2rem 0.9rem; }
    }
"""

JS = """
    function toggleStory(el) { el.classList.toggle("open"); }
    function openLightbox(fig) {
      var thumb = fig.querySelector(".thumb");
      var lbImg = document.getElementById("lbImg");
      lbImg.style.background = thumb.style.background;
      lbImg.textContent = thumb.textContent;
      document.getElementById("lbTitle").textContent = fig.dataset.title;
      document.getElementById("lbMedium").textContent = fig.dataset.medium;
      document.getElementById("lightbox").classList.add("show");
    }
    function closeLightbox(e) {
      if (e.target.id === "lightbox" || e.target.classList.contains("close")) {
        document.getElementById("lightbox").classList.remove("show");
      }
    }
"""


def hreflang_tags(current):
    out = []
    for code, (_, path, _) in LANGS.items():
        out.append('  <link rel="alternate" hreflang="%s" href="%s%s">' % (code, SITE, path))
    out.append('  <link rel="alternate" hreflang="x-default" href="%s/">' % SITE)
    return "\n".join(out)


def lang_links(current):
    out = []
    for code, (_, path, _) in LANGS.items():
        cur = ' aria-current="true"' if code == current else ''
        out.append('<a class="lang-btn" href="%s" hreflang="%s"%s>%s</a>'
                   % (path, code, cur, code.upper()))
    return "\n        ".join(out)


def person_schema(lang):
    m = META[lang]
    _, path, _ = LANGS[lang]
    job = {"tr": "Ressam", "en": "Painter", "de": "Malerin"}[lang]
    return """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "S\\u00fchendan Meng\\u00fc\\u00e7",
    "url": "%s%s",
    "jobTitle": "%s",
    "description": "%s",
    "knowsLanguage": ["tr", "en", "de"]
  }
  </script>""" % (SITE, path, job, m["desc"])


def build_page(lang):
    html_lang, path, folder = LANGS[lang]
    m = META[lang]
    nav = NAV[lang]
    roles, hero_desc, hero_cta = HERO[lang]
    about_t, portrait_ph, about1, about2 = ABOUT[lang]
    art_t, art_lead = ART_HEAD[lang]
    story_t, story_lead, read_more = STORY_HEAD[lang]
    travel_t, travel_lead = TRAVEL_HEAD[lang]
    thought_t, thought_lead = THOUGHT_HEAD[lang]
    f_tag, f_contact, f_insta, f_mail, f_rights = FOOTER[lang]

    arts = []
    for i, (title, medium) in enumerate(ART[lang]):
        arts.append(
            '        <figure class="art" onclick="openLightbox(this)" '
            'data-title="%s" data-medium="%s">\n'
            '          <div class="thumb" style="background:%s">%d</div>\n'
            '          <figcaption class="caption">\n'
            '            <h3>%s</h3>\n'
            '            <span>%s</span>\n'
            '          </figcaption>\n'
            '        </figure>' % (title, medium, ART_STYLE[i], i + 1, title, medium))

    stories = []
    for title, excerpt, full in STORIES[lang]:
        stories.append(
            '      <article class="story" onclick="toggleStory(this)">\n'
            '        <h3>%s</h3>\n'
            '        <p class="excerpt">%s</p>\n'
            '        <div class="full"><p>%s</p></div>\n'
            '        <span class="more">%s</span>\n'
            '      </article>' % (title, excerpt, full, read_more))

    travels = []
    for i, (place, title, desc) in enumerate(TRAVELS[lang]):
        grad, icon = TRAVEL_STYLE[i]
        travels.append(
            '        <div class="travel">\n'
            '          <div class="photo" style="background:%s">%s</div>\n'
            '          <div>\n'
            '            <div class="place">%s</div>\n'
            '            <h3>%s</h3>\n'
            '            <p>%s</p>\n'
            '          </div>\n'
            '        </div>' % (grad, icon, place, title, desc))

    thoughts = []
    for t in THOUGHTS[lang]:
        thoughts.append('      <div class="thought"><p>%s</p></div>' % t)

    home = path

    return """<!DOCTYPE html>
<html lang="%s">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s</title>
  <meta name="description" content="%s">
  <link rel="canonical" href="%s%s">
%s
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Sühendan Mengüç">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:url" content="%s%s">
  <meta property="og:locale" content="%s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%s">
  <meta name="twitter:description" content="%s">
%s
  <style>%s  </style>
</head>
<body>
  <header>
    <a class="brand" href="%s">Sühendan Mengüç</a>
    <nav>
      <a href="%s#about">%s</a>
      <a href="%s#paintings">%s</a>
      <a href="%s#stories">%s</a>
      <a href="%s#travels">%s</a>
      <a href="%s#thoughts">%s</a>
      <span class="langs">
        %s
      </span>
    </nav>
  </header>

  <section class="hero">
    <h1>Sühendan Mengüç</h1>
    <p class="roles">%s</p>
    <p>%s</p>
    <a href="%s#paintings" class="hero-cta">%s</a>
  </section>

  <section id="about">
    <div class="portrait">%s</div>
    <div class="about-text">
      <h2 class="section-title">%s</h2>
      <p>%s</p>
      <p>%s</p>
    </div>
  </section>

  <section id="paintings" class="alt">
    <div class="inner">
      <h2 class="section-title">%s</h2>
      <p class="section-lead">%s</p>
      <div class="gallery-grid">
%s
      </div>
    </div>
  </section>

  <section id="stories">
    <h2 class="section-title">%s</h2>
    <p class="section-lead">%s</p>
    <div class="stories">
%s
    </div>
  </section>

  <section id="travels" class="alt">
    <div class="inner">
      <h2 class="section-title">%s</h2>
      <p class="section-lead">%s</p>
      <div class="travels">
%s
      </div>
    </div>
  </section>

  <section id="thoughts">
    <h2 class="section-title">%s</h2>
    <p class="section-lead">%s</p>
    <div class="thoughts">
%s
    </div>
  </section>

  <footer>
    <div class="fname">Sühendan Mengüç</div>
    <div>%s</div>
    <div class="links">
      <a href="#">%s</a>
      <a href="#">%s</a>
      <a href="#">%s</a>
    </div>
    <small>%s</small>
  </footer>

  <div class="lightbox" id="lightbox" onclick="closeLightbox(event)">
    <button class="close" onclick="closeLightbox(event)">&times;</button>
    <div class="box">
      <div class="lb-img" id="lbImg"></div>
      <div class="lb-cap">
        <h3 id="lbTitle"></h3>
        <span id="lbMedium"></span>
      </div>
    </div>
  </div>

  <script>%s  </script>
</body>
</html>
""" % (html_lang, m["title"], m["desc"], SITE, path, hreflang_tags(lang),
       m["title"], m["desc"], SITE, path, m["locale"],
       m["title"], m["desc"], person_schema(lang), CSS,
       home,
       home, nav[0], home, nav[1], home, nav[2], home, nav[3], home, nav[4],
       lang_links(lang),
       roles, hero_desc, home, hero_cta,
       portrait_ph, about_t, about1, about2,
       art_t, art_lead, "\n".join(arts),
       story_t, story_lead, "\n".join(stories),
       travel_t, travel_lead, "\n".join(travels),
       thought_t, thought_lead, "\n".join(thoughts),
       f_tag, f_contact, f_insta, f_mail, f_rights, JS)


def build_sitemap():
    urls = []
    for code, (_, path, _) in LANGS.items():
        alts = []
        for c2, (_, p2, _) in LANGS.items():
            alts.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (c2, SITE, p2))
        alts.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>' % SITE)
        urls.append(
            '  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n'
            '%s\n  </url>' % (SITE, path, LASTMOD, "\n".join(alts)))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            '%s\n</urlset>\n' % "\n".join(urls))


ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE

NOT_FOUND = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sayfa bulunamadı — Sühendan Mengüç</title>
  <meta name="robots" content="noindex">
  <style>
    body {
      margin: 0; min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; justify-content: center; text-align: center;
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      background: #f2fbf7; color: #0c3b34; padding: 2rem;
    }
    h1 { font-family: Georgia, serif; font-weight: 400; font-size: 3rem; margin: 0 0 0.5rem; }
    p { color: #4a726a; margin: 0 0 2rem; }
    a {
      display: inline-block; background: #ff5a5f; color: #fff; text-decoration: none;
      padding: 0.8rem 1.8rem; border-radius: 50px; font-weight: 600;
    }
  </style>
</head>
<body>
  <h1>404</h1>
  <p>Aradığın sayfa burada değil.</p>
  <a href="/">Ana sayfaya dön</a>
</body>
</html>
"""


def write(path, content):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  yazildi: %s (%d bayt)" % (path, len(content.encode("utf-8"))))


def main():
    print("Site uretiliyor...")
    for lang, (_, _, folder) in LANGS.items():
        target = os.path.join(folder, "index.html") if folder else "index.html"
        write(target, build_page(lang))
    write("sitemap.xml", build_sitemap())
    write("robots.txt", ROBOTS)
    write("404.html", NOT_FOUND)
    print("Tamam.")


if __name__ == "__main__":
    main()
