# -*- coding: utf-8 -*-
"""
Sühendan Mengüç - site üreteci.

Sabit metinler (kahraman, hakkımda, kitap, bölüm başlıkları) bu dosyada
tutulur. Gerçek galeri/gezi/hikaye/düşünce içeriği `site_content.json`'dan
okunur (bkz. `integrate_selection.py`).

Site üç "sayfa grubu" halinde üretilir:
  - ana sayfa   (/, /en/, /de/)              Hero, Hakkımda, Kitabım,
                                              Resimlerim, Hikayelerim,
                                              Gezilerim/Anlar önizleme,
                                              Düşüncelerim
  - gezilerim   (/gezilerim/, /en/travels/, /de/reisen/)   30 albüm, tam
  - anlar       (/anlar/, /en/moments/, /de/momente/)      83 kare, tam

`python build.py` çalıştırıldığında 9 HTML dosyası + sitemap.xml + robots.txt
+ 404.html üretilir. Metinleri değiştirmek için CONTENT sözlüklerini (sabit)
veya site_content.json'u (gerçek galeri) düzenleyip betiği yeniden çalıştırmak
yeterli. HTML dosyalarını elle düzenleme - üzerine yazılır.
"""

import io
import json
import os

SITE = "https://suhendanmenguc.com"
LASTMOD = "2026-07-22"
LANG_CODES = ["tr", "en", "de"]
HTML_LANG = {"tr": "tr", "en": "en", "de": "de"}

# Her sayfa grubu için dil -> URL yolu
PAGE_GROUPS = {
    "home": {"tr": "/", "en": "/en/", "de": "/de/"},
    "travels": {"tr": "/gezilerim/", "en": "/en/travels/", "de": "/de/reisen/"},
    "moments": {"tr": "/anlar/", "en": "/en/moments/", "de": "/de/momente/"},
}
# Dil -> disk üzerindeki klasör (path'in başındaki/sonundaki '/' olmadan)
PAGE_FOLDERS = {
    "home": {"tr": "", "en": "en", "de": "de"},
    "travels": {"tr": "gezilerim", "en": "en/travels", "de": "de/reisen"},
    "moments": {"tr": "anlar", "en": "en/moments", "de": "de/momente"},
}

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_content.json"),
             encoding="utf-8") as _f:
    SITE_CONTENT = json.load(_f)

META = {
    "tr": {
        "title": "Sühendan Mengüç — Ressam, Yazar ve Gezgin",
        "desc": "Ressam, yazar ve gezgin Sühendan Mengüç'ün kişisel sitesi. "
                "Suluboya resimleri, 'Bozburun' adlı kitabı, gerçek hikayeleri "
                "ve hayata dair düşünceleri.",
        "locale": "tr_TR",
    },
    "en": {
        "title": "Sühendan Mengüç — Painter, Writer and Traveler",
        "desc": "The personal site of Sühendan Mengüç, painter, writer and traveler. "
                "Watercolour paintings, her book 'Bozburun', true stories and "
                "reflections on life.",
        "locale": "en_GB",
    },
    "de": {
        "title": "Sühendan Mengüç — Malerin, Autorin und Reisende",
        "desc": "Die persönliche Seite von Sühendan Mengüç, Malerin, Autorin und "
                "Reisende. Aquarelle, ihr Buch 'Bozburun', wahre Geschichten "
                "und Gedanken über das Leben.",
        "locale": "de_DE",
    },
}

META_TRAVELS = {
    "tr": {"title": "Gezilerim — Sühendan Mengüç",
           "desc": "Sühendan Mengüç'ün gezi fotoğrafları: 30 albüm, 554 kare — "
                   "Hawaii'den Prag'a, Bozburun'dan İstanbul'a."},
    "en": {"title": "Travels — Sühendan Mengüç",
           "desc": "Travel photographs by Sühendan Mengüç: 30 albums, 554 photos — "
                   "from Hawaii to Prague, Bozburun to Istanbul."},
    "de": {"title": "Reisen — Sühendan Mengüç",
           "desc": "Reisefotos von Sühendan Mengüç: 30 Alben, 554 Fotos — "
                   "von Hawaii bis Prag, Bozburun bis Istanbul."},
}

META_MOMENTS = {
    "tr": {"title": "Anlar — Sühendan Mengüç",
           "desc": "Sühendan Mengüç'ün Instagram'ından kısa kareler ve anlık notlar."},
    "en": {"title": "Moments — Sühendan Mengüç",
           "desc": "Short shots and quick notes from Sühendan Mengüç's Instagram."},
    "de": {"title": "Momente — Sühendan Mengüç",
           "desc": "Kurze Aufnahmen und spontane Notizen aus Sühendan Mengüçs Instagram."},
}

# 7 öğe: Hakkımda, Kitabım, Resimlerim, Hikayelerim, Gezilerim, Anlar, Düşüncelerim
NAV = {
    "tr": ["Hakkımda", "Kitabım", "Resimlerim", "Hikayelerim", "Gezilerim", "Anlar", "Düşüncelerim"],
    "en": ["About", "My Book", "Paintings", "Stories", "Travels", "Moments", "Thoughts"],
    "de": ["Über mich", "Mein Buch", "Bilder", "Geschichten", "Reisen", "Momente", "Gedanken"],
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

# ----------------------------------------------------------------------
# Kitabım — gerçek veriler Amazon ürün sayfasından doğrulandı (2026-07-22):
# başlık/alt başlık kapaktan, yazar/yayınevi/tarih/sayfa "Ürün Bilgileri"nden.
# Tanıtım metni kendi cümlelerimizle özetlendi (yayıncı metninin birebir
# kopyası değil).
# ----------------------------------------------------------------------
BOOK = {
    "tr": {
        "head": "Kitabım", "title": "Bozburun", "subtitle": "Bozburun'u bili miyosun?",
        "author": "Sühendan Taşkın Mengüç",
        "meta": "112 sayfa · Meşe Kitaplığı · Ağustos 2022",
        "blurb": "1980'lerde tanışıp tutkuyla bağlandığım Bozburun köyünü ve "
                 "insanlarını yalın bir dille anlattığım bir anı kitabı. Yıllar "
                 "öncesinin sakin köyünü, çalışkan insanlarını bugüne taşıyor.",
        "amazon": "Amazon'dan Satın Al", "kitapyurdu": "Kitapyurdu'ndan Satın Al",
    },
    "en": {
        "head": "My Book", "title": "Bozburun", "subtitle": "Do you know Bozburun?",
        "author": "Sühendan Taşkın Mengüç",
        "meta": "112 pages · Meşe Kitaplığı · August 2022",
        "blurb": "My memoir about the village of Bozburun and its people — a place I "
                 "fell in love with in the 1980s — told in plain, heartfelt prose. It "
                 "carries the quiet village and hardworking people of years past into "
                 "the present.",
        "amazon": "Buy on Amazon", "kitapyurdu": "Buy on Kitapyurdu",
    },
    "de": {
        "head": "Mein Buch", "title": "Bozburun", "subtitle": "Kennst du Bozburun?",
        "author": "Sühendan Taşkın Mengüç",
        "meta": "112 Seiten · Meşe Kitaplığı · August 2022",
        "blurb": "Mein Erinnerungsbuch über das Dorf Bozburun und seine Menschen — "
                 "einen Ort, in den ich mich in den 1980er Jahren verliebte —, erzählt "
                 "in schlichter, herzlicher Sprache. Es trägt das stille Dorf und die "
                 "fleißigen Menschen früherer Jahre in die Gegenwart.",
        "amazon": "Bei Amazon kaufen", "kitapyurdu": "Bei Kitapyurdu kaufen",
    },
}
BOOK_LINKS = {
    "amazon": "https://www.amazon.com.tr/Bozburun-S%C3%BChenda-Ta%C5%9Fk%C4%B1n-Meng%C3%BC%C3%A7/dp/6057326903",
    "kitapyurdu": "https://www.kitapyurdu.com/kitap/bozburun/623382.html?manufacturer_id=251021",
}
BOOK_COVER = "assets/book/cover.webp"

ART_HEAD = {
    "tr": ("Resimlerim", "Tuvale bıraktığım renkler ve anlar."),
    "en": ("Paintings", "The colours and moments I leave on the canvas."),
    "de": ("Bilder", "Die Farben und Augenblicke, die ich auf der Leinwand hinterlasse."),
}
ART_CAPTION = {"tr": "Suluboya Çalışması", "en": "Watercolour Study", "de": "Aquarellstudie"}

STORY_HEAD = {
    "tr": ("Hikayelerim", "Yaşadığım küçük anlar ve anılar.", "Devamını oku →"),
    "en": ("Stories", "Small moments and memories from my life.", "Read more →"),
    "de": ("Geschichten", "Kleine Momente und Erinnerungen aus meinem Leben.", "Weiterlesen →"),
}

TRAVEL_HEAD = {
    "tr": ("Gezilerim", "Adımlarımın ve merakımın izinden. 30 albüm, 554 kare."),
    "en": ("Travels", "Following my steps and my curiosity. 30 albums, 554 photos."),
    "de": ("Reisen", "Den Spuren meiner Schritte und meiner Neugier folgend. 30 Alben, 554 Fotos."),
}
TRAVEL_TEASER = {
    "tr": ("Gezilerim", "30 albüm, 554 kare — Hawaii'den Prag'a, Bozburun'dan İstanbul'a.", "Tüm Gezilerimi Gör →"),
    "en": ("Travels", "30 albums, 554 photos — from Hawaii to Prague, Bozburun to Istanbul.", "See All My Travels →"),
    "de": ("Reisen", "30 Alben, 554 Fotos — von Hawaii bis Prag, Bozburun bis Istanbul.", "Alle Reisen ansehen →"),
}

MOMENT_HEAD = {
    "tr": ("Anlar", "Instagram'dan kısa kareler ve anlık notlar."),
    "en": ("Moments", "Short shots and quick notes from my Instagram."),
    "de": ("Momente", "Kurze Aufnahmen und spontane Notizen aus meinem Instagram."),
}
MOMENT_TEASER = {
    "tr": ("Anlar", "Instagram'dan kısa kareler ve anlık notlar.", "Tüm Anları Gör →"),
    "en": ("Moments", "Short shots and quick notes from my Instagram.", "See All Moments →"),
    "de": ("Momente", "Kurze Aufnahmen und spontane Notizen aus meinem Instagram.", "Alle Momente ansehen →"),
}

THOUGHT_HEAD = {
    "tr": ("Düşüncelerim", "Hayata dair, üzerine düşündüğüm sorular."),
    "en": ("Thoughts", "Questions about life that I keep pondering."),
    "de": ("Gedanken", "Fragen über das Leben, über die ich immer wieder nachdenke."),
}

FOOTER = {
    "tr": ("Ressam · Yazar · Gezgin", "İletişim", "Instagram", "E-posta",
           "© 2026 Sühendan Mengüç · Tüm hakları saklıdır."),
    "en": ("Painter · Writer · Traveler", "Contact", "Instagram", "Email",
           "© 2026 Sühendan Mengüç · All rights reserved."),
    "de": ("Malerin · Autorin · Reisende", "Kontakt", "Instagram", "E-Mail",
           "© 2026 Sühendan Mengüç · Alle Rechte vorbehalten."),
}

BACK_LABEL = {"tr": "← Ana sayfaya dön", "en": "← Back to home", "de": "← Zurück zur Startseite"}
PHOTO_WORD = {"tr": "fotoğraf", "en": "photos", "de": "Fotos"}

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
    nav { display: flex; align-items: center; flex-wrap: wrap; gap: 0.3rem 1.1rem; }
    nav a { color: var(--muted); text-decoration: none; font-size: 0.88rem; transition: color 0.2s; }
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
    .hero-cta.alt { background: transparent; border: 2px solid var(--terracotta); color: var(--terracotta); padding: calc(0.85rem - 2px) calc(2rem - 2px); }
    #about { display: grid; grid-template-columns: 260px 1fr; gap: 3rem; align-items: center; }
    .portrait {
      aspect-ratio: 3 / 4; border-radius: 12px; overflow: hidden;
      background: linear-gradient(135deg, #6fe0cb, #0e9e8e);
      display: flex; align-items: center; justify-content: center; color: #fff;
      font-style: italic; text-align: center; padding: 1rem;
      box-shadow: 0 14px 30px rgba(12, 59, 52, 0.18);
    }
    .portrait img { width: 100%; height: 100%; object-fit: cover; }
    .about-text h2 { margin-bottom: 1rem; }
    .about-text p + p { margin-top: 1rem; }
    .alt { background: var(--cream-2); max-width: none; }
    .alt > .inner { max-width: 1080px; margin: 0 auto; }
    #book { display: grid; grid-template-columns: 240px 1fr; gap: 2.5rem; align-items: start; }
    #book .book-cover { width: 100%; border-radius: 8px; box-shadow: 0 14px 30px rgba(12, 59, 52, 0.18); display: block; }
    #book .book-text h2 { margin-bottom: 0.3rem; }
    #book .book-text h3 { font-size: 1.8rem; color: var(--ink); margin: 0.4rem 0 0.1rem; }
    #book .book-subtitle { font-style: italic; color: var(--terracotta); margin-bottom: 0.5rem; }
    #book .book-meta { font-size: 0.85rem; color: var(--muted); margin-bottom: 1.1rem; }
    #book .book-buttons { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem; }
    .gallery-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.2rem;
    }
    .art {
      background: var(--cream); border-radius: 10px; overflow: hidden;
      box-shadow: 0 8px 20px rgba(12, 59, 52, 0.08); cursor: pointer;
      transition: transform 0.25s, box-shadow 0.25s;
    }
    .art:hover { transform: translateY(-5px); box-shadow: 0 16px 32px rgba(12, 59, 52, 0.16); }
    .art img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; display: block; }
    .art .caption { padding: 0.7rem 0.9rem 0.9rem; }
    .art .caption h3 { font-size: 1rem; margin-bottom: 0.1rem; }
    .art .caption span { font-size: 0.8rem; color: var(--muted); }
    .stories { display: flex; flex-direction: column; gap: 1.2rem; }
    .story {
      background: var(--cream); border: 1px solid var(--cream-2);
      border-left: 4px solid var(--terracotta); border-radius: 8px;
      padding: 1.4rem 1.6rem; cursor: pointer; transition: box-shadow 0.2s;
    }
    .story:hover { box-shadow: 0 10px 24px rgba(12, 59, 52, 0.1); }
    .story .meta {
      font-size: 0.78rem; letter-spacing: 0.5px; text-transform: uppercase;
      color: var(--terracotta); margin-bottom: 0.2rem;
    }
    .story h3 { font-size: 1.25rem; margin-bottom: 0.3rem; }
    .story .excerpt { color: var(--muted); }
    .story .full { max-height: 0; overflow: hidden; transition: max-height 0.5s ease; }
    .story.open .full { max-height: 2000px; }
    .story .full p { margin-top: 1rem; white-space: pre-line; }
    .story .more {
      display: inline-block; margin-top: 0.8rem; color: var(--terracotta);
      font-size: 0.85rem; font-weight: 600;
    }
    .page-hero {
      max-width: 1080px; margin: 0 auto; padding: 8rem 2rem 1rem;
    }
    .page-hero h1 { font-size: clamp(2.2rem, 5vw, 3rem); color: var(--brown); margin-bottom: 0.5rem; }
    .back-link {
      display: inline-block; margin-top: 1rem; color: var(--terracotta);
      text-decoration: none; font-size: 0.9rem; font-weight: 600;
    }
    .teaser-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.8rem; margin-bottom: 1.6rem;
    }
    .teaser-grid a { display: block; border-radius: 8px; overflow: hidden; text-decoration: none; position: relative; }
    .teaser-grid img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; transition: transform 0.25s; }
    .teaser-grid a:hover img { transform: scale(1.06); }
    .travels { display: flex; flex-direction: column; gap: 1.2rem; }
    .travel-block {
      background: var(--cream); border-radius: 12px; padding: 0;
      box-shadow: 0 8px 20px rgba(12, 59, 52, 0.07); overflow: hidden;
    }
    .travel-block summary {
      cursor: pointer; font-family: var(--serif); font-size: 1.3rem; color: var(--ink);
      padding: 1.2rem 1.5rem; list-style: none; display: flex; align-items: baseline; gap: 0.6rem;
    }
    .travel-block summary::-webkit-details-marker { display: none; }
    .travel-block summary::before { content: "▸"; color: var(--terracotta); font-size: 1rem; }
    .travel-block[open] summary::before { content: "▾"; }
    .travel-block summary .count { font-family: var(--sans); font-size: 0.82rem; color: var(--muted); font-weight: 400; }
    .travel-block .body { padding: 0 1.5rem 1.6rem; }
    .travel-block .blurb { color: var(--muted); font-style: italic; margin-bottom: 1rem; font-size: 0.92rem; }
    .photo-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 0.6rem;
    }
    .photo-grid img {
      width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 6px;
      cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; display: block;
    }
    .photo-grid img:hover { transform: scale(1.04); box-shadow: 0 6px 16px rgba(12, 59, 52, 0.2); }
    .moment { background: var(--cream); border-radius: 10px; overflow: hidden;
      box-shadow: 0 6px 16px rgba(12, 59, 52, 0.07); cursor: pointer; transition: transform 0.2s; }
    .moment:hover { transform: translateY(-3px); }
    .moment img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; }
    .moment .cap { padding: 0.5rem 0.7rem 0.7rem; font-size: 0.78rem; color: var(--muted); }
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
      background: rgba(12, 59, 52, 0.92); align-items: center; justify-content: center; padding: 2rem;
    }
    .lightbox.show { display: flex; }
    .lightbox .box { max-width: 720px; width: 100%; background: var(--cream); border-radius: 12px; overflow: hidden; }
    .lightbox .lb-img { width: 100%; max-height: 72vh; object-fit: contain; display: block; background: #05201b; }
    .lightbox .lb-cap { padding: 1rem 1.4rem 1.4rem; }
    .lightbox .lb-cap h3 { font-size: 1.2rem; margin-bottom: 0.2rem; }
    .lightbox .lb-cap span { color: var(--muted); font-size: 0.9rem; }
    .lightbox .close {
      position: absolute; top: 1.5rem; right: 2rem; color: #fff; font-size: 2.2rem;
      cursor: pointer; line-height: 1; background: none; border: none;
    }
    @media (max-width: 760px) {
      section, .page-hero { padding: 3.5rem 1.4rem; }
      .page-hero { padding-top: 7rem; }
      #about, #book { grid-template-columns: 1fr; }
      .portrait { max-width: 260px; margin: 0 auto; }
      #book .book-cover { max-width: 220px; margin: 0 auto; }
      header { padding: 0.8rem 1.2rem; }
      nav { gap: 0.2rem 0.8rem; }
    }
"""

JS = """
    function toggleStory(el) { el.classList.toggle("open"); }
    function openLightbox(imgEl) {
      var lbImg = document.getElementById("lbImg");
      lbImg.src = imgEl.currentSrc || imgEl.src;
      document.getElementById("lbTitle").textContent = imgEl.dataset.title || "";
      document.getElementById("lbMedium").textContent = imgEl.dataset.sub || "";
      document.getElementById("lightbox").classList.add("show");
    }
    function closeLightbox(e) {
      if (e.target.id === "lightbox" || e.target.classList.contains("close")) {
        document.getElementById("lightbox").classList.remove("show");
      }
    }
"""


def hreflang_tags(group):
    out = []
    for code in LANG_CODES:
        out.append('  <link rel="alternate" hreflang="%s" href="%s%s">'
                    % (code, SITE, PAGE_GROUPS[group][code]))
    out.append('  <link rel="alternate" hreflang="x-default" href="%s%s">'
                % (SITE, PAGE_GROUPS[group]["tr"]))
    return "\n".join(out)


def lang_links(group, current):
    out = []
    for code in LANG_CODES:
        cur = ' aria-current="true"' if code == current else ''
        out.append('<a class="lang-btn" href="%s" hreflang="%s"%s>%s</a>'
                    % (PAGE_GROUPS[group][code], code, cur, code.upper()))
    return "\n        ".join(out)


def nav_html(lang):
    home = PAGE_GROUPS["home"][lang]
    travels = PAGE_GROUPS["travels"][lang]
    moments = PAGE_GROUPS["moments"][lang]
    n = NAV[lang]
    items = [
        (home + "#about", n[0]),
        (home + "#book", n[1]),
        (home + "#paintings", n[2]),
        (home + "#stories", n[3]),
        (travels, n[4]),
        (moments, n[5]),
        (home + "#thoughts", n[6]),
    ]
    return "\n      ".join('<a href="%s">%s</a>' % (href, label) for href, label in items)


def person_schema(lang):
    m = META[lang]
    path = PAGE_GROUPS["home"][lang]
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


def head_html(lang, group, title, desc, extra_schema=""):
    path = PAGE_GROUPS[group][lang]
    locale = META[lang]["locale"]
    return """<head>
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
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-5T1Y2555HS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-5T1Y2555HS');
  </script>
</head>""" % (title, desc, SITE, path, hreflang_tags(group),
              title, desc, SITE, path, locale,
              title, desc, extra_schema, CSS)


def header_html(lang, group):
    home = PAGE_GROUPS["home"][lang]
    return """  <header>
    <a class="brand" href="%s">Sühendan Mengüç</a>
    <nav>
      %s
      <span class="langs">
        %s
      </span>
    </nav>
  </header>""" % (home, nav_html(lang), lang_links(group, lang))


def footer_html(lang):
    f_tag, f_contact, f_insta, f_mail, f_rights = FOOTER[lang]
    return """  <footer>
    <div class="fname">Sühendan Mengüç</div>
    <div>%s</div>
    <div class="links">
      <a href="#">%s</a>
      <a href="#">%s</a>
      <a href="#">%s</a>
    </div>
    <small>%s</small>
  </footer>""" % (f_tag, f_contact, f_insta, f_mail, f_rights)


LIGHTBOX_HTML = """  <div class="lightbox" id="lightbox" onclick="closeLightbox(event)">
    <button class="close" onclick="closeLightbox(event)">&times;</button>
    <div class="box">
      <img class="lb-img" id="lbImg" src="" alt="">
      <div class="lb-cap">
        <h3 id="lbTitle"></h3>
        <span id="lbMedium"></span>
      </div>
    </div>
  </div>"""


def excerpt_of(text, limit=130):
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def page_shell(lang, group, title, desc, body_sections, extra_schema=""):
    return """<!DOCTYPE html>
<html lang="%s">
%s
<body>
%s

%s

%s
  <script>%s  </script>
</body>
</html>
""" % (HTML_LANG[lang], head_html(lang, group, title, desc, extra_schema),
       header_html(lang, group), body_sections, LIGHTBOX_HTML, JS)


def build_home_page(lang):
    m = META[lang]
    roles, hero_desc, hero_cta = HERO[lang]
    about_t, portrait_ph, about1, about2 = ABOUT[lang]
    book = BOOK[lang]
    art_t, art_lead = ART_HEAD[lang]
    story_t, story_lead, read_more = STORY_HEAD[lang]
    tt_title, tt_desc, tt_cta = TRAVEL_TEASER[lang]
    mt_title, mt_desc, mt_cta = MOMENT_TEASER[lang]
    thought_t, thought_lead = THOUGHT_HEAD[lang]
    art_caption = ART_CAPTION[lang]
    home = PAGE_GROUPS["home"][lang]
    travels_path = PAGE_GROUPS["travels"][lang]
    moments_path = PAGE_GROUPS["moments"][lang]

    if SITE_CONTENT.get("portrait"):
        portrait_html = '<img src="/%s" alt="%s">' % (SITE_CONTENT["portrait"], about_t)
    else:
        portrait_html = portrait_ph

    arts = []
    for i, item in enumerate(SITE_CONTENT["art"], 1):
        title = "%s %d" % (art_caption, i)
        arts.append(
            '        <figure class="art">\n'
            '          <img src="/%s" loading="lazy" decoding="async" alt="%s"\n'
            '               onclick="openLightbox(this)" data-title="%s">\n'
            '          <figcaption class="caption"><h3>%s</h3></figcaption>\n'
            '        </figure>' % (item["file"], title, title, title)
        )

    stories = []
    for s in SITE_CONTENT["stories"]:
        title = s["title"][lang]
        meta = s["meta"][lang]
        text = s["text"][lang]
        excerpt = excerpt_of(text)
        meta_html = '<div class="meta">%s</div>' % meta if meta else ""
        stories.append(
            '      <article class="story" onclick="toggleStory(this)">\n'
            '        %s<h3>%s</h3>\n'
            '        <p class="excerpt">%s</p>\n'
            '        <div class="full"><p>%s</p></div>\n'
            '        <span class="more">%s</span>\n'
            '      </article>' % (meta_html, title, excerpt, text, read_more)
        )

    thoughts = []
    for th in SITE_CONTENT["thoughts"]:
        thoughts.append('      <div class="thought"><p>%s</p></div>' % th["text"][lang])

    # Gezilerim önizleme: ilk 8 albümün kapak fotoğrafı
    travel_teaser = []
    for t in SITE_CONTENT["travels"][:8]:
        if not t["photos"]:
            continue
        travel_teaser.append(
            '<a href="%s"><img src="/%s" loading="lazy" alt="%s"></a>'
            % (travels_path, t["photos"][0], t["title"][lang])
        )

    # Anlar önizleme: ilk 10 kare
    moment_teaser = []
    for mo in SITE_CONTENT["ig_moments"][:10]:
        moment_teaser.append(
            '<a href="%s"><img src="/%s" loading="lazy" alt=""></a>' % (moments_path, mo["file"])
        )

    body = """  <section class="hero">
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

  <section id="book">
    <img class="book-cover" src="/%s" alt="%s — %s">
    <div class="book-text">
      <h2 class="section-title">%s</h2>
      <h3>%s</h3>
      <p class="book-subtitle">%s</p>
      <p class="book-meta">%s</p>
      <p>%s</p>
      <div class="book-buttons">
        <a class="hero-cta" href="%s" target="_blank" rel="noopener">%s</a>
        <a class="hero-cta alt" href="%s" target="_blank" rel="noopener">%s</a>
      </div>
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

  <section id="travels-teaser" class="alt">
    <div class="inner">
      <h2 class="section-title">%s</h2>
      <p class="section-lead">%s</p>
      <div class="teaser-grid">
        %s
      </div>
      <a href="%s" class="hero-cta">%s</a>
    </div>
  </section>

  <section id="moments-teaser">
    <h2 class="section-title">%s</h2>
    <p class="section-lead">%s</p>
    <div class="teaser-grid">
      %s
    </div>
    <a href="%s" class="hero-cta">%s</a>
  </section>

  <section id="thoughts" class="alt">
    <div class="inner">
      <h2 class="section-title">%s</h2>
      <p class="section-lead">%s</p>
      <div class="thoughts">
%s
      </div>
    </div>
  </section>

%s""" % (roles, hero_desc, home, hero_cta,
         portrait_html, about_t, about1, about2,
         BOOK_COVER, book["title"], book["author"],
         book["head"], book["title"], book["subtitle"], book["meta"], book["blurb"],
         BOOK_LINKS["amazon"], book["amazon"], BOOK_LINKS["kitapyurdu"], book["kitapyurdu"],
         art_t, art_lead, "\n".join(arts),
         story_t, story_lead, "\n".join(stories),
         tt_title, tt_desc, "\n        ".join(travel_teaser), travels_path, tt_cta,
         mt_title, mt_desc, "\n      ".join(moment_teaser), moments_path, mt_cta,
         thought_t, thought_lead, "\n".join(thoughts),
         footer_html(lang))

    return page_shell(lang, "home", m["title"], m["desc"], body, person_schema(lang))


def build_travels_page(lang):
    m = META_TRAVELS[lang]
    travel_t, travel_lead = TRAVEL_HEAD[lang]
    home = PAGE_GROUPS["home"][lang]

    blocks = []
    for t in SITE_CONTENT["travels"]:
        title = t["title"][lang]
        blurb = t["blurb"][lang]
        photos = []
        for p in t["photos"]:
            photos.append(
                '<img src="/%s" loading="lazy" decoding="async" alt="%s"\n'
                '             onclick="openLightbox(this)" data-title="%s">' % (p, title, title)
            )
        blocks.append(
            '        <details class="travel-block">\n'
            '          <summary>%s <span class="count">(%d %s)</span></summary>\n'
            '          <div class="body">\n'
            '            <p class="blurb">%s</p>\n'
            '            <div class="photo-grid">\n              %s\n            </div>\n'
            '          </div>\n'
            '        </details>' % (title, len(photos), PHOTO_WORD[lang], blurb, "\n              ".join(photos))
        )

    body = """  <section class="page-hero">
    <h1>%s</h1>
    <p class="section-lead">%s</p>
    <a href="%s#about" class="back-link">%s</a>
  </section>
  <section>
    <div class="travels">
%s
    </div>
  </section>

%s""" % (travel_t, travel_lead, home, BACK_LABEL[lang], "\n".join(blocks), footer_html(lang))

    return page_shell(lang, "travels", m["title"], m["desc"], body)


def build_moments_page(lang):
    m = META_MOMENTS[lang]
    moment_t, moment_lead = MOMENT_HEAD[lang]
    home = PAGE_GROUPS["home"][lang]

    moments = []
    for mo in SITE_CONTENT["ig_moments"]:
        cap = mo["caption"].get(lang) or mo["caption"].get("tr") or ""
        cap_html = '<div class="cap">%s</div>' % cap if cap else ""
        moments.append(
            '        <figure class="moment" onclick="openLightbox(this.querySelector(\'img\'))">\n'
            '          <img src="/%s" loading="lazy" decoding="async" alt="" data-title="">\n'
            '          %s\n'
            '        </figure>' % (mo["file"], cap_html)
        )

    body = """  <section class="page-hero">
    <h1>%s</h1>
    <p class="section-lead">%s</p>
    <a href="%s#about" class="back-link">%s</a>
  </section>
  <section>
    <div class="gallery-grid">
%s
    </div>
  </section>

%s""" % (moment_t, moment_lead, home, BACK_LABEL[lang], "\n".join(moments), footer_html(lang))

    return page_shell(lang, "moments", m["title"], m["desc"], body)


def build_sitemap():
    urls = []
    for group in ("home", "travels", "moments"):
        for code in LANG_CODES:
            path = PAGE_GROUPS[group][code]
            alts = []
            for c2 in LANG_CODES:
                alts.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>'
                            % (c2, SITE, PAGE_GROUPS[group][c2]))
            alts.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>'
                        % (SITE, PAGE_GROUPS[group]["tr"]))
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
    for lang in LANG_CODES:
        folder = PAGE_FOLDERS["home"][lang]
        target = os.path.join(folder, "index.html") if folder else "index.html"
        write(target, build_home_page(lang))
    for lang in LANG_CODES:
        write(os.path.join(PAGE_FOLDERS["travels"][lang], "index.html"), build_travels_page(lang))
    for lang in LANG_CODES:
        write(os.path.join(PAGE_FOLDERS["moments"][lang], "index.html"), build_moments_page(lang))
    write("sitemap.xml", build_sitemap())
    write("robots.txt", ROBOTS)
    write("404.html", NOT_FOUND)
    print("Tamam.")


if __name__ == "__main__":
    main()
