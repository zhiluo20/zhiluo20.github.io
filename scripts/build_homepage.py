#!/usr/bin/env python3
"""Build Mecury's eleven static, indexable homepage localizations."""
import html,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.mecury.co.uk'
ORDER=['en','fr','de','th','ja','ko','zh-Hans','zh-Hant','es','ar','it']
CONTENT=json.loads((ROOT/'content/home.json').read_text())
def path(locale): return '/' if locale=='en' else '/'+locale.lower()+'/'
def esc(value): return html.escape(str(value),quote=True)
def txt(value,locale):
    value=esc(value)
    if locale=='ar':
        value=re.sub(r'(?<![A-Za-z])(?:Imperial College London|Server Sentinel|Vibeit(?: Studio)?|Mecury|Python|iPad|Mac|Apple|Zhi Luo|Zhi|M)(?![A-Za-z])',lambda m:'<bdi dir="ltr">'+m.group(0)+'</bdi>',value)
    return value

def build(locale):
    t=CONTENT[locale]; text=lambda s:txt(s,locale)
    def lines(values): return '<br>'.join(text(x) for x in values)
    def paragraphs(values): return ''.join('<p>'+text(x)+'</p>' for x in values)
    here=path(locale);url=BASE+here;direction='rtl' if locale=='ar' else 'ltr'
    options=''.join(f'<a href="{path(code)}" lang="{code}" hreflang="{code}" aria-label="{esc(CONTENT[code]["name"])}" {"aria-current=page" if locale==code else ""}><span>{esc(CONTENT[code]["name"])}</span><small dir="ltr">{esc(CONTENT[code]["short"])}</small></a>' for code in ORDER)
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE+path(code)}">' for code in ORDER)+f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    graph={'@context':'https://schema.org','@graph':[
      {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Mecury','publisher':{'@id':BASE+'/#organization'},'inLanguage':ORDER},
      {'@type':'WebPage','@id':url+'#webpage','url':url,'name':t['pageTitle'],'description':t['description'],'inLanguage':locale,'isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#zhiluo'}},
      {'@type':'Organization','@id':BASE+'/#organization','name':'Mecury International Ltd','url':BASE+'/','founder':{'@id':BASE+'/#zhiluo'}},
      {'@type':'Person','@id':BASE+'/#zhiluo','name':'Zhi Luo','jobTitle':t['role'],'alumniOf':{'@type':'CollegeOrUniversity','name':'Imperial College London'},'sameAs':['https://github.com/zhiluo20']}
    ]}
    steps=''.join(f'<article class="story-step"><span class="number"><bdi dir="ltr">0{i+1}</bdi> — {text(step[0])}</span><h3>{text(step[1])}</h3><p>{text(step[2])}</p></article>' for i,step in enumerate(t['steps']))
    careers=''.join(f'<span class="{"current" if i==5 else ""}">{text(item)}{" ↗" if i==5 else ""}</span>' for i,item in enumerate(t['careers']))
    specs=''.join('<span>'+text(item)+'</span>' for item in t['specs'])
    nav=''.join(f'<a href="{anchor}">{text(label)}</a>' for anchor,label in zip(['#vibeit','#story','#projects'],t['nav']))
    def project(slug,name,icon,copy):
        return f'<a class="project-row" href="{BASE}/{slug}/"><img src="/assets/home/{icon}" alt="" width="48" height="48" loading="lazy"><div><h3><bdi dir="ltr">{name}</bdi></h3><p>{lines(copy)}</p></div><span class="arrow" aria-hidden="true">↗</span></a>'
    json_ld=json.dumps(graph,ensure_ascii=False).replace('<', chr(92)+'u003c')
    return f'''<!doctype html>
<html lang="{locale}" dir="{direction}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(t['pageTitle'])}</title><meta name="description" content="{esc(t['description'])}"><meta name="theme-color" content="#111517"><link rel="canonical" href="{url}">{alternates}<meta property="og:type" content="website"><meta property="og:site_name" content="Mecury"><meta property="og:title" content="{esc(t['pageTitle'])}"><meta property="og:description" content="{esc(t['description'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/home/portrait-creative.png"><meta property="og:image:alt" content="{esc(t['portraitAlt'])}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/home/favicon.svg"><link rel="stylesheet" href="/home.css"><script type="application/ld+json">{json_ld}</script><script src="/home.js" defer></script></head>
<body class="b"><a class="skip" href="#main">{text(t['skip'])}</a>
<header class="wrap nav"><a class="wordmark" href="{here}" aria-label="Mecury"><bdi dir="ltr">Mecury.</bdi></a><nav class="nav-links" aria-label="Mecury">{nav}</nav><details class="lang-menu"><summary aria-label="{esc(t['language'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><span dir="ltr">{esc(t['short'])}</span><span aria-hidden="true">⌄</span></summary><div class="lang-options">{options}</div></details></header>
<main>
<section class="wrap hero" id="main"><figure class="hero-photo"><img src="/assets/home/portrait-creative.png" alt="{esc(t['portraitAlt'])}" width="1536" height="1024" fetchpriority="high"></figure><div class="hero-copy"><p class="eyebrow">{text(t['heroKicker'])}</p><h1>{text(t['headline'][0])}<br><em>{text(t['headline'][1])}</em></h1><p class="hero-intro">{text(t['intro'])}</p><div class="cta-row"><a class="primary" href="{BASE}/vibeit/">{text(t['explore'])}<span aria-hidden="true">↗</span></a><a class="text-link" href="#story">{text(t['read'])}<span aria-hidden="true">↓</span></a></div><div class="identity"><strong><bdi dir="ltr">Zhi Luo</bdi></strong>{text(t['role'])}<br>{text(t['education'])}</div><a class="hero-product" href="#vibeit"><img src="/assets/home/vibeit-device.png" alt="{esc(t['productAlt'])}" width="1477" height="1065"><div><p class="eyebrow">{text(t['firstChapter'])}</p><h2><bdi dir="ltr">Vibeit Studio</bdi></h2><p>{text(t['teaser'])}</p></div><span class="arrow" aria-hidden="true">↗</span></a></div><div class="hero-bottom"><span>{text(t['heroFooter'])}</span><span class="hairline" aria-hidden="true"></span><a href="#vibeit">{text(t['scroll'])} ↓</a></div></section>
<section class="wrap vibeit-section" id="vibeit"><div class="vibeit-head"><div><div class="product-label"><img src="/assets/home/vibeit-icon.png" alt="" width="38" height="38" loading="lazy"><span dir="ltr">Vibeit Studio</span></div><h2>{lines(t['productTitle'])}</h2></div><div class="product-intro">{paragraphs(t['productIntro'])}</div></div><figure class="product-stage"><img class="device" src="/assets/home/vibeit-device.png" alt="{esc(t['productAlt'])}" width="1477" height="1065" loading="lazy"></figure><div class="product-foot"><div class="specs">{specs}</div><a class="text-link" href="{BASE}/vibeit/">{text(t['productLink'])}<span aria-hidden="true">↗</span></a></div></section>
<section class="wrap story" id="story"><p class="eyebrow muted">{text(t['storyKicker'])}</p><h2>{lines(t['storyTitle'])}</h2><div class="story-steps">{steps}</div></section>
<section class="possibilities" id="zhiluo"><div class="wrap possibility-grid"><div><p class="eyebrow">{text(t['aboutKicker'])}</p><h2>{lines(t['aboutTitle'])}</h2><div class="about-copy">{paragraphs(t['aboutBody'])}</div><div class="career-list">{careers}</div></div><figure><img class="formal-photo" src="/assets/home/portrait-formal.jpg" alt="{esc(t['formalAlt'])}" width="1086" height="1448" loading="lazy"><figcaption class="photo-caption"><span dir="ltr">Zhi Luo</span><span>{text(t['portraitCaption'])}</span></figcaption></figure></div></section>
<section class="wrap other-projects" id="projects"><div class="section-heading"><h2>{text(t['otherTitle'])}</h2><span class="eyebrow">{text(t['otherKicker'])}</span></div><div class="other-grid">{project('timenu','Timenu','timenu-icon.png',t['timenu'])}{project('server-sentinel','Server Sentinel','server-sentinel-icon.png',t['sentinel'])}</div></section>
<section class="wrap closing"><div><h2>{lines(t['closingTitle'])}</h2><p>{text(t['closingBody'])}</p></div><a class="primary" href="{BASE}/vibeit/">{text(t['closingCta'])}<span aria-hidden="true">↗</span></a></section>
</main><footer class="wrap"><div class="footer"><a class="wordmark" href="{here}" dir="ltr">Mecury.</a><div><a href="{BASE}/vibeit/support.html">{text(t['contact'])}</a><a href="https://github.com/zhiluo20"><bdi dir="ltr">GitHub ↗</bdi></a><a href="{BASE}/privacy.html">{text(t['privacy'])}</a></div></div><div class="footer-bottom"><span dir="ltr">© 2026 Mecury International Ltd</span><span>{text(t['footerNote'])}</span></div></footer>
</body></html>'''

keys=set(CONTENT['en'])
for locale in ORDER:
    assert set(CONTENT[locale])==keys,locale
    target=ROOT/path(locale).lstrip('/')/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(build(locale)+'\n')
urls=''.join(f'<url><loc>{BASE+path(locale)}</loc></url>' for locale in ORDER)
urls+=''.join(f'<url><loc>{BASE}/{suffix}</loc></url>' for suffix in ['privacy.html','vibeit/','timenu/','server-sentinel/'])
(ROOT/'home-sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>\n')
print('Built',len(ORDER),'localized pages and the homepage sitemap.')
