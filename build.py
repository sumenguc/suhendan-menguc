# -*- coding: utf-8 -*-
"""
Sühendan Mengüç - site üreteci.

Sabit metinler (kahraman, hakkımda, bölüm başlıkları) bu dosyada tutulur.
Gerçek galeri/gezi/hikaye/düşünce içeriği `site_content.json`'dan okunur
(bkz. `integrate_selection.py` - seçim galerisinden bu dosyayı üretir).

`python build.py` çalıştırıldığında şu dosyalar üretilir:

    index.html      (Türkçe)
    en/index.html   (İngilizce)
    de/index.html   (Almanca)
    sitemap.xml
    robots.txt
    404.html

Metinleri değiştirmek için CONTENT sözlüklerini (sabit) veya site_content.json'u
(gerçek galeri) düzenleyip betiği yeniden çalıştırmak yeterli. HTML dosyalarını
elle düzenleme - üzerine yazılır.
"""

import io
import json
import os

SITE = "https://suhendanmenguc.com"
LASTMOD = "2026-07-21"

# Dil kodu -> (html lang, URL yolu, klasör)
LANGS = {
    "tr": ("tr", "/", ""),
    "en": ("en", "/en/", "en"),
    "de": ("de", "/de/", "de"),
}

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_content.json"),
             encoding="utf-8") as _f:
    SITE_CONTENT = json.load(_f)

META = {
    "tr": {
        "title": "Sühendan Mengüç — Ressam, Yazar ve Gezgin",
        "desc": "Ressam, yazar ve gezgin Sühendan Mengüç'ün kişisel sitesi. "
                "Suluboya resimleri, gezi fotoğrafları, gerçek hikayeleri "
                "ve hayata dair düşünceleri.",
        "locale": "tr_TR",
    },
    "en": {
        "title": "Sühendan Mengüç — Painter, Writer and Traveler",
        "desc": "The personal site of Sühendan Mengüç, painter, writer and traveler. "
                "Watercolour paintings, travel photographs, true stories and "
                "reflections on life.",
        "locale": "en_GB",
    },
    "de": {
        "title": "Sühendan Mengüç — Malerin, Autorin und Reisende",
        "desc": "Die persönliche Seite von Sühendan Mengüç, Malerin, Autorin und "
                "Reisende. Aquarelle, Reisefotos, wahre Geschichten "
                "und Gedanken über das Leben.",
        "locale": "de_DE",
    },
}

NAV = {
    "tr": ["Hakkımda", "Resimlerim", "Hikayelerim", "Gezilerim", "Anlar", "Düşüncelerim"],
    "en": ["About", "Paintings", "Stories", "Travels", "Moments", "Thoughts"],
    "de": ["Über mich", "Bilder", "Geschichten", "Reisen", "Momente", "Gedanken"],
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
    "tr": ("Gezilerim", "Adımlarımın ve merakımın izinden."),
    "en": ("Travels", "Following my steps and my curiosity."),
    "de": ("Reisen", "Den Spuren meiner Schritte und meiner Neugier folgend."),
}

MOMENT_HEAD = {
    "tr": ("Anlar", "Instagram'dan kısa kareler."),
    "en": ("Moments", "Short shots from my Instagram."),
    "de": ("Momente", "Kurze Aufnahmen aus meinem Instagram."),
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
    .travels { display: flex; flex-direction: column; gap: 2rem; }
    .travel-block {
      background: var(--cream); border-radius: 12px; padding: 1.6rem 1.6rem 1.8rem;
      box-shadow: 0 8px 20px rgba(12, 59, 52, 0.07);
    }
    .travel-block h3 { font-size: 1.4rem; margin-bottom: 0.25rem; }
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
      section { padding: 3.5rem 1.4rem; }
      #about { grid-template-columns: 1fr; }
      .portrait { max-width: 260px; margin: 0 auto; }
      header { padding: 0.8rem 1.2rem; }
      nav { gap: 0.2rem 0.9rem; }
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


def excerpt_of(text, limit=130):
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def build_page(lang):
    html_lang, path, folder = LANGS[lang]
    m = META[lang]
    nav = NAV[lang]
    roles, hero_desc, hero_cta = HERO[lang]
    about_t, portrait_ph, about1, about2 = ABOUT[lang]
    art_t, art_lead = ART_HEAD[lang]
    story_t, story_lead, read_more = STORY_HEAD[lang]
    travel_t, travel_lead = TRAVEL_HEAD[lang]
    moment_t, moment_lead = MOMENT_HEAD[lang]
    thought_t, thought_lead = THOUGHT_HEAD[lang]
    f_tag, f_contact, f_insta, f_mail, f_rights = FOOTER[lang]
    art_caption = ART_CAPTION[lang]

    # ---- Sanat (gerçek suluboyalar) ----
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

    # ---- Hikayelerim (gerçek metinler) ----
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

    # ---- Gezilerim (gerçek albümler) ----
    travels = []
    for t in SITE_CONTENT["travels"]:
        title = t["title"][lang]
        blurb = t["blurb"][lang]
        photos = []
        for p in t["photos"]:
            photos.append(
                '<img src="/%s" loading="lazy" decoding="async" alt="%s"\n'
                '             onclick="openLightbox(this)" data-title="%s">' % (p, title, title)
            )
        travels.append(
            '        <div class="travel-block">\n'
            '          <h3>%s</h3>\n'
            '          <p class="blurb">%s</p>\n'
            '          <div class="photo-grid">\n            %s\n          </div>\n'
            '        </div>' % (title, blurb, "\n            ".join(photos))
        )

    # ---- Anlar (Instagram kareleri) ----
    moments = []
    for mo in SITE_CONTENT["ig_moments"]:
        cap = mo["caption"].get(lang) or mo["caption"].get("tr") or ""
        cap_html = '<div class="cap">%s</div>' % cap if cap else ""
        moments.append(
            '        <figure class="moment" onclick="openLightbox(this.querySelector(\'img\'))">\n'
            '          <img src="/%s" loading="lazy" decoding="async" alt=""\n'
            '               data-title="">\n'
            '          %s\n'
            '        </figure>' % (mo["file"], cap_html)
        )

    # ---- Düşüncelerim (gerçek metinler) ----
    thoughts = []
    for th in SITE_CONTENT["thoughts"]:
        thoughts.append('      <div class="thought"><p>%s</p></div>' % th["text"][lang])

    home = path

    # ---- Portre ----
    if SITE_CONTENT.get("portrait"):
        portrait_html = '<img src="/%s" alt="%s">' % (SITE_CONTENT["portrait"], about_t)
    else:
        portrait_html = portrait_ph

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
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-5T1Y2555HS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-5T1Y2555HS');
  </script>
</head>
<body>
  <header>
    <a class="brand" href="%s">Sühendan Mengüç</a>
    <nav>
      <a href="%s#about">%s</a>
      <a href="%s#paintings">%s</a>
      <a href="%s#stories">%s</a>
      <a href="%s#travels">%s</a>
      <a href="%s#moments">%s</a>
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

  <section id="moments">
    <h2 class="section-title">%s</h2>
    <p class="section-lead">%s</p>
    <div class="gallery-grid">
%s
    </div>
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
      <img class="lb-img" id="lbImg" src="" alt="">
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
       home, nav[0], home, nav[1], home, nav[2], home, nav[3], home, nav[4], home, nav[5],
       lang_links(lang),
       roles, hero_desc, home, hero_cta,
       portrait_html, about_t, about1, about2,
       art_t, art_lead, "\n".join(arts),
       story_t, story_lead, "\n".join(stories),
       travel_t, travel_lead, "\n".join(travels),
       moment_t, moment_lead, "\n".join(moments),
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
