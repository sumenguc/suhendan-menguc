# -*- coding: utf-8 -*-
"""
Facebook/Instagram arşivinden site içeriği SEÇME galerisi üretir.

Bu betik kişisel veri klasörlerini TARAR ama orijinal dosyaları hiçbir
şekilde değiştirmez/taşımaz/silmez. Ürettiği tek şey:
  - `_secim/index.html`   (tıklanabilir seçim sayfası)
  - `_secim/webp_cache/`  (HEIC/JPG/PNG dosyalarının küçültülmüş WEBP kopyaları)
Bunların hepsi .gitignore ile GitHub'dan hariç tutulur.

Kullanım:  python select_gallery.py
Sonra:     python select_server.py     (POST /save-selection destekleyen sunucu)
           tarayıcıda http://127.0.0.1:8765/_secim/ aç, kutucuklarla seç,
           "Seçimleri Kaydet" butonuna bas -> _secim/secim_sonuc.json yazılır.
"""

import io
import os
import re

try:
    from PIL import Image
    import pillow_heif
    pillow_heif.register_heif_opener()
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

ROOT = os.path.dirname(os.path.abspath(__file__))
FB = "facebook-suhendanmenguc-20.07.2026-yV321TFs"
IG = "instagram-suhendanmenguc-2026-07-20-9wFx6XM5"
WEBP_CACHE = os.path.join(ROOT, "_secim", "webp_cache")

RASTER_EXT = (".jpg", ".jpeg", ".png", ".heic", ".heif")  # webp'ye çevrilecekler
ALREADY_WEBP_EXT = (".webp",)
VID_EXT = (".mp4",)

# ----------------------------------------------------------------------
# Facebook albüm listesi: (klasör adı, görünen ad, kategori)
# kategori: "art" | "travel" | "profile" | "video"
# Mobilyuklemeler (taşınma), stickers_used ve Chicago Ziyareti 2008
# kullanıcı isteğiyle bilinçli olarak DIŞARIDA.
# ----------------------------------------------------------------------
FB_ALBUMS = [
    ("SuluboyalarimMyAquarells_10152223566833518", "Suluboyalarım", "art"),
    ("Hawaii2014_10152472992053518", "Hawaii, 2014", "travel"),
    ("Mallorca2008_33359273517", "Mallorca, 2008", "travel"),
    ("BodenseeSeptember2010_442693288517", "Bodensee, Eylül 2010", "travel"),
    ("Prag2009_224225853517", "Prag, 2009", "travel"),
    ("your_posts", "Kronolojik Gönderiler", "travel"),
    ("Fotograflar_10151298370383518", "Fotoğraflar", "travel"),
    ("201105Rotterdam_10150192383353518", "Rotterdam, Mayıs 2011", "travel"),
    ("IjsselmeerAug2011_10150293031338518", "IJsselmeer, Ağustos 2011", "travel"),
    ("Aug2011Kellerwegfest_10150319031428518", "Kellerwegfest, Ağustos 2011", "travel"),
    ("NewYork2014_10152473073068518", "New York, 2014", "travel"),
    ("2008JuneAkkrumSailingWeekend_17273678517", "Akkrum Yelken Haftasonu, Haziran 2008", "travel"),
    ("EveElaFeb2011_10150116653243518", "Eve & Ela, Şubat 2011", "travel"),
    ("SanFrancisco2014_10152472902973518", "San Francisco, 2014", "travel"),
    ("SuhendanMenguc_5911018517", "Sühendan Mengüç", "travel"),
    ("EliseEylulisthere_10151230067053518", "Elise & Eylül", "travel"),
    ("Dec2011TribergSchwarzwald_10150473090423518", "Triberg, Schwarzwald, Aralık 2011", "travel"),
    ("201012Istanbul_494362948517", "İstanbul, Aralık 2010", "travel"),
    ("09EasterTriptoZurih_73174948517", "Zürih Paskalya Gezisi, 2009", "travel"),
    ("Chicago2014_10152472872813518", "Chicago, 2014", "travel"),
    ("WillingenDec08_42335478517", "Willingen, Aralık 2008", "travel"),
    ("Turkiye2012Mart_10150678525268518", "Türkiye, Mart 2012", "travel"),
    ("Winetasting_451252428517", "Şarap Tadımı", "travel"),
    ("Bozburun_5914468517", "Bozburun", "travel"),
    ("OurnewhomeIzmir_10151202419788518", "Yeni Evimiz, İzmir", "travel"),
    ("Hawaii2014_10152473043198518", "Hawaii, 2014 (2)", "travel"),
    ("FransXmasTea_10150473203288518", "Noel Çayı", "travel"),
    ("Apr12Fulda_10150721026528518", "Fulda, Nisan 2012", "travel"),
    ("EftymiasBirthday_10150473197243518", "Eftymia'nın Doğum Günü", "travel"),
    ("InstagramPhotos_10155676723078518", "Instagram Fotoğrafları (FB yedeği)", "travel"),
    ("FrankfurtApr1_10150703229058518", "Frankfurt, Nisan", "travel"),
    ("ProfilResimleri_434315638517", "Profil Resimleri", "profile"),
    ("KapakFotograflari_10151350912088518", "Kapak Fotoğrafları", "profile"),
    ("videos", "Videolar", "video"),
]

# ----------------------------------------------------------------------
# Facebook metin adayları (Explore taramasından, tam metin)
# ----------------------------------------------------------------------
FB_TEXTS = [
    ("Liman notu", "19 Ağu 2025 · Frankfurt/Rhein",
     "Dün hava sertti. Fırtınadan kaçanlarla doldu liman. Sabah erken GÜNDOĞUSU "
     "esiyordu. Simdi YILDIZa döndü. Bu mevsimde nadir eser boyle. Denizin rengi de "
     "rüzgara göre değişiyor. Şimdi çivit mavisi oldu. 🥰"),
    ("Müze izlenimi", "Ağu 2025 · Städel Museum",
     "Bugün Städel Museum da, Monet sergisinde gördüklerim beni Monet'den daha çok "
     "etkiledi. Yerde resim çizen çocuk mankenmiş meğer. Herkesin gerçeği anlamasi "
     "biraz zaman aliyordu."),
    ("Coğrafya kaderdir", "",
     "Kalbim orada kaldi. Orada da doğmuş olabilirdim. Coğrafya kaderdir."),
    ("Sanat üzerine", "",
     "Kendimi kotu hissettigimde sanat beni ayaga kaldirir. Sanat olmazsa nasil "
     "yasarim!"),
    ("Kitap çıkışı", "",
     "Nihayet bugün çıktı. Covit günlerinde iki yıllık emekle hayalim gerçekleşti."),
    ("Şiirsel an", "",
     "Güneş gitti. Işık değişti. Hava soğudu. Dondum. Yerim dar. Gerisi yarına."),
    ("Komşu hikayesi", "Almanya günlük hayatı",
     "Karsimizdaki evin eski dış merdivenlerini yenilemek istiyormus sahibi. Iki gun "
     "önce üç işçi, aletleri tasiyan kamyonet ve bir de çıkan molozu koyacakları "
     "konteynerle gelip işe başladılar. Önce kaplama taslarini çıkardılar. Sonra "
     "balyozlarla basladilar alttaki betonu kirmaya. Hepsi BEŞ basamak olan "
     "merdivenlerin vur Allah vur sadece bir basamagini kirabildiler. Arada oturdugum "
     "yerden bir titresim duyuyorum. Deprem mi? diyorum. Sonra burada deprem "
     "olmadigini hatirlayip rahatliyorum. Kocam söylenmeye basladi: 'Ulan bonbardimana "
     "karşı bunker mi yapiyorsunuz? Ne bu be? Hepi topu 5 basamakli ev giris "
     "merdiveni. Ordu ustune cikip da ziplayacak mi? Alman abartisi iste' diye. "
     "Biraz sonra adamlar kiramayinca işi birakti. Ertesi gün paletli küçük bir "
     "kırıcı getirdiler. TAKA TAKA TAKA bütün gün calisti. Kalan dört basamağı "
     "kırdı. 3. gün sabah kapinin onunde kalan platformu kırdı. Arkadan bir küçük "
     "kepçe ve seyyar tuvalet geldi. Merdivenden cikan buyuk beton parcalarini "
     "konteynere doldurdu. Evin etrafini seperatorle kapattilar. Etrafa bir tek toz "
     "toprak sacilmadi. Simdi evin etrafini kazmaya basladilar. Galiba izolasyon "
     "yapilacak."),
    ("Yazı dersi anısı", "",
     "Dün aksam SANAL YAZI EVİNDE YEŞİM CİMCOZ'UN bu senenin son dersi ders ötesiydi. "
     "Herşey kendiliginden, biraz spritüel, nazik, samimi, öğretici.. Yeşimcim❤️"),
    ("Koro konseri anısı", "",
     "Dün akşam bir yildir calismalarina katildigim koronun konseri vardi. Herkes cok "
     "mutluydu. Basarili oldu. Uzun uzun alkiş aldik. Benim için güzel bir anı oldu."),
]

CSS = """
:root {
  --cream: #f2fbf7; --cream-2: #d3f3ea; --terracotta: #ff5a5f;
  --brown: #0e9e8e; --ink: #0c3b34; --muted: #4a726a;
  --serif: Georgia, "Times New Roman", serif;
  --sans: -apple-system, "Segoe UI", Roboto, Helvetica, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: var(--sans); background: var(--cream); color: var(--ink); line-height: 1.6; }
header { position: sticky; top: 0; z-index: 20; background: rgba(242,251,247,.97); backdrop-filter: blur(6px);
  border-bottom: 1px solid var(--cream-2); padding: 1rem 1.5rem; }
header h1 { font-family: var(--serif); font-weight: 400; font-size: 1.4rem; margin: 0 0 .3rem; }
header p { margin: 0; color: var(--muted); font-size: .9rem; }
main { max-width: 1200px; margin: 0 auto; padding: 1.5rem; padding-bottom: 6rem; }
h2.section { font-family: var(--serif); font-weight: 400; color: var(--brown); font-size: 1.6rem;
  margin: 2.5rem 0 .3rem; border-bottom: 2px solid var(--cream-2); padding-bottom: .4rem; }
p.section-note { color: var(--muted); font-size: .88rem; margin: 0 0 1rem; }
details.album { background: #fff; border: 1px solid var(--cream-2); border-radius: 10px;
  margin: 1rem 0; padding: .8rem 1rem; }
details.album > summary { cursor: pointer; font-weight: 600; font-size: 1.05rem; color: var(--ink);
  display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; }
details.album > summary .count { color: var(--muted); font-weight: 400; font-size: .85rem; }
.album-toggle { font-size: .72rem; font-weight: 600; color: var(--terracotta); background: none;
  border: 1px solid var(--terracotta); border-radius: 6px; padding: .15rem .5rem; cursor: pointer; margin-left: auto; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: .7rem; margin-top: .8rem; }
figure.item { position: relative; margin: 0; background: var(--cream); border-radius: 8px; overflow: hidden;
  border: 1px solid var(--cream-2); transition: opacity .15s, filter .15s; }
figure.item.excluded { opacity: .35; filter: grayscale(1); }
figure.item.excluded figcaption .id::after { content: " ✕ hariç"; color: var(--terracotta); font-weight: 700; }
figure.item img, figure.item video { width: 100%; height: 130px; object-fit: cover; display: block; background: #eee; }
figure.item figcaption { padding: .35rem .5rem; font-size: .72rem; color: var(--muted); }
figure.item figcaption .id { display: block; font-weight: 700; color: var(--terracotta); font-family: monospace; font-size: .78rem; }
figure.item figcaption .cap { display: block; margin-top: .15rem; color: var(--ink); font-size: .74rem; }
.pick-wrap { position: absolute; top: 6px; left: 6px; z-index: 2; background: rgba(255,255,255,.85);
  border-radius: 6px; padding: 2px 4px; line-height: 0; }
.pick-wrap input { width: 18px; height: 18px; cursor: pointer; }
.ph { width: 100%; height: 130px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg,#d3f3ea,#f2fbf7); color: var(--brown); font-size: .7rem; text-align: center; padding: .4rem; }
.text-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem; }
.text-card { position: relative; background: #fff; border: 1px solid var(--cream-2); border-radius: 10px; padding: 1rem 1.1rem 1rem 2.6rem;
  transition: opacity .15s, filter .15s; }
.text-card.excluded { opacity: .35; filter: grayscale(1); }
.text-card.excluded .id::after { content: " ✕ hariç"; color: var(--terracotta); font-weight: 700; }
.text-card .pick-wrap { top: .8rem; left: .7rem; background: none; }
.text-card .id { font-family: monospace; font-weight: 700; color: var(--terracotta); font-size: .8rem; }
.text-card h3 { font-family: var(--serif); font-weight: 400; margin: .3rem 0 .1rem; font-size: 1.1rem; }
.text-card .meta { color: var(--muted); font-size: .78rem; margin-bottom: .5rem; }
.text-card p { margin: 0; font-size: .92rem; }
.stats { display: flex; gap: 1.2rem; flex-wrap: wrap; color: var(--muted); font-size: .85rem; margin-top: .3rem; }
.savebar { position: fixed; bottom: 0; left: 0; right: 0; z-index: 30; background: var(--ink); color: #fff;
  padding: .8rem 1.5rem; display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; box-shadow: 0 -4px 16px rgba(0,0,0,.15); }
.savebar strong { color: #fff; }
.savebar button { font-family: var(--sans); font-weight: 700; border: none; border-radius: 8px;
  padding: .6rem 1.3rem; cursor: pointer; font-size: .92rem; }
#saveBtn { background: var(--terracotta); color: #fff; }
#clearBtn { background: transparent; color: #d9ecE6; border: 1px solid #4a726a; }
#saveStatus { font-size: .85rem; color: #9fd8c9; }
.savebar .included { color: #9fd8c9; }
"""

JS = """
(function () {
  // Varsayilan olarak HER OGE SITEYE DAHILDIR. Kutucuk isaretlemek o ogeyi
  // HARIC TUTAR. Boylece cogunlugu istenen yuzlerce fotografta tek tek
  // "istiyorum" isaretlemek yerine, sadece azinlikta olan istenmeyenler
  // isaretlenir.
  var STORAGE_KEY = "suhendan_secim_v2";
  function loadExcluded() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); } catch (e) { return {}; }
  }
  function saveExcluded(obj) { localStorage.setItem(STORAGE_KEY, JSON.stringify(obj)); }
  var excluded = loadExcluded();
  var allBoxes = null;

  function updateCounter() {
    var total = allBoxes.length;
    var exCount = Object.keys(excluded).length;
    document.getElementById("pickCount").textContent = exCount;
    document.getElementById("includedCount").textContent = total - exCount;
  }

  function applyState() {
    allBoxes.forEach(function (cb) {
      var id = cb.dataset.id;
      cb.checked = !!excluded[id];
      toggleCard(cb, cb.checked);
    });
    updateCounter();
  }

  function toggleCard(cb, on) {
    var card = cb.closest(".item") || cb.closest(".text-card");
    if (card) card.classList.toggle("excluded", on);
  }

  document.addEventListener("change", function (e) {
    if (!e.target.classList.contains("pick")) return;
    var id = e.target.dataset.id;
    if (e.target.checked) excluded[id] = true; else delete excluded[id];
    toggleCard(e.target, e.target.checked);
    saveExcluded(excluded);
    updateCounter();
  });

  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("album-toggle")) {
      var grid = e.target.closest("details").querySelector(".grid");
      var boxes = grid.querySelectorAll("input.pick");
      var exAll = e.target.dataset.mode === "exclude";
      boxes.forEach(function (cb) {
        cb.checked = exAll;
        var id = cb.dataset.id;
        if (exAll) excluded[id] = true; else delete excluded[id];
        toggleCard(cb, exAll);
      });
      e.target.dataset.mode = exAll ? "include" : "exclude";
      e.target.textContent = exAll ? "Tümünü Dahil Et" : "Tümünü Hariç Tut";
      saveExcluded(excluded);
      updateCounter();
    }
  });

  document.getElementById("clearBtn").addEventListener("click", function () {
    excluded = {};
    saveExcluded(excluded);
    applyState();
    document.getElementById("saveStatus").textContent = "";
  });

  function collect() {
    var items = [];
    allBoxes.forEach(function (cb) {
      var id = cb.dataset.id;
      var isExcluded = !!excluded[id];
      var fig = cb.closest(".item");
      var card = cb.closest(".text-card");
      if (fig) {
        var media = fig.querySelector("img,video");
        var cap = fig.querySelector(".cap");
        items.push({
          id: id, type: "media", excluded: isExcluded,
          path: media ? media.getAttribute("src") : null,
          caption: cap ? cap.textContent : null
        });
      } else if (card) {
        var h3 = card.querySelector("h3");
        var p = card.querySelector("p");
        items.push({
          id: id, type: "text", excluded: isExcluded,
          title: h3 ? h3.textContent : null,
          text: p ? p.textContent : null
        });
      }
    });
    return items;
  }

  document.getElementById("saveBtn").addEventListener("click", function () {
    var status = document.getElementById("saveStatus");
    var items = collect();
    var includedCount = items.filter(function (i) { return !i.excluded; }).length;
    status.textContent = "Kaydediliyor...";
    fetch("/save-selection", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: items, totalCount: items.length,
        includedCount: includedCount, excludedCount: items.length - includedCount,
        savedAt: new Date().toISOString()
      })
    }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function () {
      status.textContent = "Kaydedildi (" + includedCount + " dahil, " + (items.length - includedCount) + " hariç) — Claude'a haber verebilirsin.";
    }).catch(function (err) {
      status.textContent = "Kaydetme başarısız: " + err.message + " (select_server.py çalışıyor mu?)";
    });
  });

  allBoxes = Array.prototype.slice.call(document.querySelectorAll("input.pick"));
  applyState();
})();
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def rel_url(abs_path):
    """Proje kökünden itibaren MUTLAK yol ('/' ile başlar).

    _secim/index.html bir alt klasörde servis edildiği için göreli yollar
    tarayıcıda yanlış çözümlenir. Sunucu proje kökünden çalıştığı için
    baştan '/' koymak sunucu-köküne göre doğru mutlak bir yol üretir.
    """
    rel = os.path.relpath(abs_path, ROOT)
    return "/" + rel.replace("\\", "/")


def list_files(dir_path):
    """Doğrudan içindeki dosyalar (alt klasörlere inmez)."""
    if not os.path.isdir(dir_path):
        return []
    out = []
    for name in sorted(os.listdir(dir_path)):
        p = os.path.join(dir_path, name)
        if os.path.isfile(p):
            out.append(p)
    return out


def list_files_recursive(dir_path):
    """Alt klasörler dahil tüm dosyalar (tarih klasörlü Instagram medyası için)."""
    if not os.path.isdir(dir_path):
        return []
    out = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        dirnames.sort()
        for fn in sorted(filenames):
            out.append(os.path.join(dirpath, fn))
    return out


_webp_stats = {"converted": 0, "cached": 0, "failed": 0}


def to_webp(abs_src):
    """HEIC/JPG/PNG dosyasını _secim/webp_cache altında WEBP'ye çevirir.

    Zaten güncel bir WEBP varsa yeniden çevirmez (idempotent). Başarısız
    olursa None döner (çağıran yer orijinali kullanır).
    """
    if not HAVE_PIL:
        return None
    rel = os.path.relpath(abs_src, ROOT).replace("\\", "/")
    out_rel = os.path.splitext(rel)[0] + ".webp"
    out_abs = os.path.join(WEBP_CACHE, out_rel.replace("/", os.sep))
    try:
        if os.path.isfile(out_abs) and os.path.getmtime(out_abs) >= os.path.getmtime(abs_src):
            _webp_stats["cached"] += 1
            return out_abs
        out_dir = os.path.dirname(out_abs)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        img = Image.open(abs_src)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA") if "A" in img.mode else img.convert("RGB")
        img.save(out_abs, "WEBP", quality=82, method=4)
        _webp_stats["converted"] += 1
        return out_abs
    except Exception:
        _webp_stats["failed"] += 1
        return None


def media_figure(item_id, abs_path, caption=""):
    ext = os.path.splitext(abs_path)[1].lower()
    name = esc(os.path.basename(abs_path))
    cap_html = ('<span class="cap">%s</span>' % esc(caption)) if caption else ""
    checkbox = '<span class="pick-wrap"><input type="checkbox" class="pick" data-id="%s" title="İstemiyorum, hariç tut"></span>' % esc(item_id)

    if ext in RASTER_EXT:
        webp_path = to_webp(abs_path)
        src = webp_path if webp_path else abs_path
        url = esc(rel_url(src))
        body = '<img src="%s" loading="lazy" decoding="async" alt="%s">' % (url, name)
    elif ext in ALREADY_WEBP_EXT:
        url = esc(rel_url(abs_path))
        body = '<img src="%s" loading="lazy" decoding="async" alt="%s">' % (url, name)
    elif ext in VID_EXT:
        url = esc(rel_url(abs_path))
        # preload="none": çok sayıda video öğesi olabiliyor, "metadata" hepsi
        # için eşzamanlı istek başlatıp sayfayı kilitliyor.
        body = '<video src="%s" controls preload="none"></video>' % url
    else:
        body = '<div class="ph">%s</div>' % name

    return (
        '<figure class="item">%s%s'
        '<figcaption><span class="id">%s</span>%s</figcaption>'
        '</figure>' % (checkbox, body, esc(item_id), cap_html)
    )


def build_ig_caption_map():
    """Instagram posts.html / posts_1.html içinden foto -> caption eşlemesi çıkar."""
    caps = {}
    base = os.path.join(ROOT, IG, "your_instagram_activity", "media")
    pat = re.compile(r'<img src="(media/posts/[^"]+)"[^/]*/></a><div>(.*?)</div>', re.S)
    for fn in ("posts.html", "posts_1.html"):
        path = os.path.join(base, fn)
        if not os.path.isfile(path):
            continue
        with io.open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        for href, cap in pat.findall(content):
            cap = cap.strip().replace("&#039;", "'").replace("&amp;", "&")
            key = href[len("media/posts/"):]
            if cap and (key not in caps or not caps[key]):
                caps[key] = cap
    return caps


def build():
    sections = []
    stats = {}

    # --- Facebook albümleri ---
    art_html, travel_html, profile_html, video_html = [], [], [], []
    art_count = travel_count = profile_count = video_count = 0

    for folder, label, cat in FB_ALBUMS:
        dir_path = os.path.join(ROOT, FB, "your_facebook_activity", "posts", "media", folder)
        files = list_files(dir_path)
        if not files:
            continue
        prefix = {"art": "W", "travel": "T-%s" % re.sub(r"[^A-Za-z0-9]", "", label)[:14],
                  "profile": "P-%s" % re.sub(r"[^A-Za-z0-9]", "", label)[:10],
                  "video": "V"}[cat]
        figs = []
        for i, f in enumerate(files, 1):
            item_id = "%s-%02d" % (prefix, i)
            figs.append(media_figure(item_id, f))
        block = (
            '<details class="album" open><summary>%s <span class="count">(%d dosya)</span>'
            '<button type="button" class="album-toggle" data-mode="exclude">Tümünü Hariç Tut</button></summary>'
            '<div class="grid">%s</div></details>'
            % (esc(label), len(files), "".join(figs))
        )
        if cat == "art":
            art_html.append(block); art_count += len(files)
        elif cat == "profile":
            profile_html.append(block); profile_count += len(files)
        elif cat == "video":
            video_html.append(block); video_count += len(files)
        else:
            travel_html.append(block); travel_count += len(files)

    sections.append(('<h2 class="section">🎨 Sanat Eserlerim (Suluboyalar)</h2>'
                      '<p class="section-note">Facebook arşivindeki tablo fotoğrafları — site için en doğrudan aday.</p>'
                      + "".join(art_html)))
    sections.append(('<h2 class="section">✈️ Seyahat ve Hayat Albümleri (Facebook)</h2>'
                      '<p class="section-note">%d albüm, tam liste — hiçbir fotoğraf atlanmadı. Başlığa tıklayıp kapatabilirsin.</p>'
                      % len(travel_html)
                      + "".join(travel_html)))
    sections.append(('<h2 class="section">🖼️ Profil / Kapak Fotoğrafı Adayları</h2>'
                      + "".join(profile_html)))
    sections.append(('<h2 class="section">🎬 Videolar (Facebook)</h2>'
                      '<p class="section-note">Oynatmak için videoya tıkla.</p>'
                      + "".join(video_html)))
    stats["fb_art"] = art_count
    stats["fb_travel"] = travel_count
    stats["fb_profile"] = profile_count
    stats["fb_video"] = video_count

    # --- Facebook metin adayları ---
    cards = []
    for i, (title, meta, text) in enumerate(FB_TEXTS, 1):
        item_id = "TX-%d" % i
        checkbox = '<span class="pick-wrap"><input type="checkbox" class="pick" data-id="%s" title="İstemiyorum, hariç tut"></span>' % item_id
        cards.append(
            '<div class="text-card">%s<span class="id">%s</span><h3>%s</h3>'
            '<div class="meta">%s</div><p>%s</p></div>'
            % (checkbox, item_id, esc(title), esc(meta), esc(text))
        )
    sections.append('<h2 class="section">✍️ Metin Adayları (Facebook)</h2>'
                     '<p class="section-note">Gezi notları, sanat izlenimleri, kısa düşünceler — hikaye/gezi/düşünce bölümlerine aday.</p>'
                     '<div class="text-grid">%s</div>' % "".join(cards))
    stats["fb_text"] = len(FB_TEXTS)

    # --- Instagram gönderileri (caption'larla birlikte) ---
    ig_caps = build_ig_caption_map()
    ig_posts_dir = os.path.join(ROOT, IG, "media", "posts")
    ig_files = list_files_recursive(ig_posts_dir)
    ig_figs = []
    for i, f in enumerate(ig_files, 1):
        rel_key = os.path.relpath(f, ig_posts_dir).replace("\\", "/")
        cap = ig_caps.get(rel_key, "")
        ig_figs.append(media_figure("IG-%02d" % i, f, cap))
    sections.append('<h2 class="section">📸 Instagram Gönderileri</h2>'
                     '<p class="section-note">%d dosya. Alt yazısı olanların metni kutunun altında görünüyor.</p>'
                     '<div class="grid">%s</div>' % (len(ig_files), "".join(ig_figs)))
    stats["ig_posts"] = len(ig_files)
    stats["ig_captioned"] = sum(1 for f in ig_files
                                 if ig_caps.get(os.path.relpath(f, ig_posts_dir).replace("\\", "/")))

    # --- Instagram reels ---
    ig_reels_dir = os.path.join(ROOT, IG, "media", "reels")
    reel_files = [f for f in list_files_recursive(ig_reels_dir) if f.lower().endswith(VID_EXT)]
    reel_figs = [media_figure("IGR-%02d" % i, f) for i, f in enumerate(reel_files, 1)]
    sections.append('<h2 class="section">🎬 Instagram Reels</h2>'
                     '<div class="grid">%s</div>' % "".join(reel_figs))
    stats["ig_reels"] = len(reel_files)

    # NOT: Instagram Stories bölümü kullanıcı isteğiyle kaldırıldı (caption'sız, düşük değer).

    stats_line = " · ".join(
        "%s: %d" % (k, v) for k, v in [
            ("Suluboya", stats["fb_art"]), ("Seyahat", stats["fb_travel"]),
            ("Profil/Kapak", stats["fb_profile"]), ("FB Video", stats["fb_video"]),
            ("Metin", stats["fb_text"]), ("IG Gönderi", stats["ig_posts"]),
            ("IG Caption'lı", stats["ig_captioned"]), ("IG Reels", stats["ig_reels"]),
        ]
    )

    html = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>İçerik Seçim Galerisi</title>
<style>%s</style>
</head>
<body>
<header>
  <h1>Sühendan Mengüç — Site İçin İçerik Seçim Galerisi</h1>
  <p><strong>Her öğe varsayılan olarak sitede kullanılacak.</strong> İstemediklerini sol üstündeki
  kutucuğa tıklayıp hariç tut (soluklaşıp üstü çizili görünür). Bir albümün tamamını istemiyorsan
  başlığındaki "Tümünü Hariç Tut" düğmesini kullan. Bitince alttaki "Seçimleri Kaydet"e bas.</p>
  <div class="stats">%s</div>
</header>
<main>
%s
</main>
<div class="savebar">
  <span>Hariç tutulan: <strong id="pickCount">0</strong></span>
  <span class="included">Dahil edilecek: <strong id="includedCount">0</strong></span>
  <button id="saveBtn" type="button">Seçimleri Kaydet</button>
  <button id="clearBtn" type="button">Hariç Tutmaları Temizle</button>
  <span id="saveStatus"></span>
</div>
<script>%s</script>
</body>
</html>""" % (CSS, stats_line, "\n".join(sections), JS)

    out_dir = os.path.join(ROOT, "_secim")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_path = os.path.join(out_dir, "index.html")
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("Yazildi: %s (%d bayt)" % (out_path, len(html.encode("utf-8"))))
    print("Istatistikler:", stats_line)
    print("WEBP donusum:", _webp_stats)


if __name__ == "__main__":
    build()
