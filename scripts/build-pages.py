"""Compose the Services and Work pages using the portfolio's shared sections."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / 'dist'
home = (root / 'index.html').read_text()
home = home.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="styles.css"', 'href="/styles.css"').replace('src="script.js"', 'src="/script.js"')
home = home.replace('<body>', '<body id="top">')
home = home.replace('<a href="#services">Services</a><a href="#work">Work</a><a href="#about">About me</a>', '<a href="/services/">Services</a><a href="/work/">Work</a><a href="/#about">About me</a>')
home = home.replace('class="identity" href="#home"', 'class="identity" href="/"').replace('class="footer-wordmark" href="#home"', 'class="footer-wordmark" href="/"').replace('class="back-top" href="#home"', 'class="back-top" href="#top"')
home = home.replace('href="#work">Explore my work', 'href="/work/">Explore my work')
home = home.replace('href="https://talha-ali.com/" target="_blank" rel="noopener noreferrer">Visit my portfolio', 'href="/work/">Explore all work')

services = [
    ('website-design', 'Website design', 'design', 'A clear direction. A website that feels like you.', 'From the first wireframe to the final detail, I translate your brand into a website that is clear, usable, and consistent across every screen.', ['Page structure & wireframes', 'Figma to responsive layouts', 'Thoughtful interactions', 'Accessible interface details'], ['UI/UX', 'Figma', 'Responsive design']),
    ('wordpress-development', 'WordPress development', 'code', 'Custom-built. Easy to make your own.', 'Flexible WordPress websites built around the way you publish. Custom themes and reusable sections give your team control without making everyday changes complicated.', ['Custom theme development', 'ACF flexible content', 'Gutenberg blocks', 'Custom post types & templates'], ['WordPress', 'ACF', 'PHP']),
    ('e-commerce', 'E-commerce', 'shop', 'Make every step of shopping feel effortless.', 'Product pages, variations, shipping rules, and checkout all need to work together. I build WooCommerce and Shopify experiences around your products and customers.', ['WooCommerce & Shopify builds', 'Product and variation templates', 'Custom shipping logic', 'Store integrations'], ['WooCommerce', 'Shopify', 'Liquid']),
    ('performance-seo', 'Speed & technical SEO', 'speed', 'A better experience starts with the foundations.', 'I find what is slowing your site down and improve the technical details behind it, from image delivery and page structure to crawlability and mobile usability.', ['Performance review & fixes', 'Image and asset optimization', 'Technical SEO setup', 'Responsive usability checks'], ['Performance', 'Technical SEO', 'Core Web Vitals']),
    ('website-care', 'Website care', 'care', 'A dependable partner beyond launch.', 'Websites need attention as your business grows. I help with routine updates, troubleshooting, content changes, and the improvements that keep your site useful.', ['Theme & plugin updates', 'Bug fixes and troubleshooting', 'Content and layout updates', 'Ongoing development support'], ['Maintenance', 'Support', 'Site improvements']),
    ('integrations', 'Integrations & automation', 'flow', 'Connect your website to the way you work.', 'Make forms, customer information, and business tools work together. I build practical connections that reduce repetitive steps and support your existing workflow.', ['Form and webhook integrations', 'Custom REST API connections', 'CRM and email tool connections', 'Workflow automation'], ['REST APIs', 'Webhooks', 'Automation']),
]
for slug, name, *_ in services:
    home = home.replace(f'href="#contact" data-service="{name}"', f'href="/services/#{slug}" data-service="{name}"')
if 'class="footer-pages"' not in home:
    home = home.replace('<div class="footer-bottom">', '<nav class="footer-pages" aria-label="Footer navigation" style="display:flex;gap:24px;padding-bottom:24px;font-size:14px"><a href="/">Home</a><a href="/services/">Services</a><a href="/work/">Work</a><a href="/#contact">Contact</a></nav><div class="footer-bottom">')
(root / 'index.html').write_text(home)

head = home.split('<main id="main">')[0]
footer = '<footer' + home.split('<footer', 1)[1]
contact = re.search(r'    <section class="contact section-wrap".*?</section>', home, re.S).group()
icon = lambda name: f'<svg aria-hidden="true"><use href="#{name}"/></svg>'
button = lambda text, href, white=False: f'<a class="button button-{"white" if white else "lime"}" href="{href}">{text}<span class="button-icon">{icon("diagonal" if white else "arrow")}</span></a>'

def video(compact=False):
    return f'''<figure class="showreel {'compact-reel' if compact else ''}">
      <div class="video-shell"><video controls playsinline preload="none" poster="/assets/showreel-poster.jpg" aria-label="Talha Ali portfolio showcase, 18 seconds, no audio"><source src="/assets/portfolio-showreel.mp4" type="video/mp4"><p>Your browser cannot play this video. <a href="/assets/portfolio-showreel.mp4">Open the portfolio showreel</a>.</p></video></div>
      <figcaption><span>DESIGN IN MOTION</span><span>18-second portfolio showcase · No audio</span><a href="/assets/portfolio-showreel.mp4" download>Download reel ↓</a></figcaption>
    </figure>'''

def save_page(name, title, description, main):
    page_head = re.sub(r'<title>.*?</title>', f'<title>{title} — Talha Ali</title>', head)
    page_head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', page_head)
    page_head = page_head.replace('<body id="top">', f'<body id="top" class="subpage {name}-page">').replace('</head>', '<link rel="stylesheet" href="/pages.css">\n</head>')
    page_head = page_head.replace(f'<a href="/{name}/">', f'<a href="/{name}/" aria-current="page">', 1)
    folder = root / name
    folder.mkdir(exist_ok=True)
    (folder / 'index.html').write_text(page_head + '<main id="main">' + main + contact + '</main>' + footer)

service_cards = ''
for n, (slug, name, symbol, subtitle, description, items, tags) in enumerate(services, 1):
    service_cards += f'''<article class="solution-card" id="{slug}"><div class="solution-top"><span>0{n}</span>{icon(symbol)}</div><h3>{name}</h3><p class="solution-lead">{subtitle}</p><p>{description}</p><ul>{''.join('<li>'+item+'</li>' for item in items)}</ul><div class="tech-tags">{''.join('<span>'+tag+'</span>' for tag in tags)}</div><a class="solution-cta" href="#contact" data-service="{name}">Let’s talk about your project {icon('diagonal')}</a></article>'''
process = [
    ('Discover & plan', 'We start with your business, your audience, and what the website needs to do. Then we agree on the pages, features, scope, and priorities before work begins.'),
    ('Design & refine', 'I map the content and shape the key layouts. We review the direction together and refine the details before moving into development.'),
    ('Build & connect', 'The approved design becomes a responsive website. I set up editable content, build the features you need, and connect the tools your business uses.'),
    ('Review, launch & hand over', 'We review the pages, forms, and important user journeys. After launch, I walk you through updating your content and agree on any ongoing support.'),
]
faqs = [
    ('Can you work from my existing Figma design?', 'Yes. I can turn an approved Figma design into a custom WordPress theme, a Shopify theme, or a responsive website. We will review the layouts and functionality before setting the scope.'),
    ('Can you improve my existing website?', 'Yes. A project can be a complete redesign or a focused improvement, such as a new landing page, better product templates, performance work, or a feature your current site is missing.'),
    ('How long will my project take?', 'The timeline depends on the number of pages, features, integrations, and how much content is ready. I will share a project-specific estimate after reviewing your brief.'),
    ('How do you price projects?', 'I quote based on the agreed scope and requirements. Share your design, project goals, and preferred deadline so I can prepare a clear estimate.'),
    ('Will I be able to update the website myself?', 'Yes. Editable content and reusable sections are part of the plan. I will walk you through the areas your team needs to manage after launch.'),
    ('Do you work with agencies and remote teams?', 'Yes. I can help with project-based development or ongoing delivery, working with your design files, communication tools, and development process.'),
]
services_main = f'''
  <section class="page-hero section-wrap">
    <div class="breadcrumb"><a href="/">Home</a><span>/</span>Services</div>
    <div class="section-kicker"><span class="small-star">✳</span> DESIGN, DEVELOPMENT & EVERYTHING BETWEEN</div>
    <h1>Websites made<br>to <span class="accent">make a difference.</span></h1>
    <div class="hero-lower"><p>Thoughtful design, custom development, and the right connections. I help businesses and agencies turn a good idea into a website that works.</p><div class="page-actions">{button('Let’s discuss your project','#contact')}{button('Explore the work','/work/',True)}</div></div>
    <nav class="service-jumps" aria-label="Explore services">{''.join(f'<a href="#{s[0]}">{s[1]} ↗</a>' for s in services)}</nav>
  </section>
  <section class="reel-section section-wrap" aria-label="Portfolio video">{video()}</section>
  <section class="solutions section-wrap" id="solutions"><div class="section-heading"><div><div class="section-kicker"><span class="small-star">✳</span> WHAT I DO</div><h2>One partner.<br><span class="accent">The whole website.</span></h2></div><p>From the first layout to the last integration, choose the support your project needs.</p></div><div class="solutions-grid">{service_cards}</div></section>
  <section class="working-together section-wrap"><div class="section-heading"><div><div class="section-kicker"><span class="small-star">✳</span> HOW I WORK</div><h2>Good work starts with<br><span class="accent">a good partnership.</span></h2></div><p>Clear communication and considered decisions, from the first conversation to the final handover.</p></div><div class="benefit-grid"><article><span>01</span><h3>Direct collaboration</h3><p>You work directly with the person building your website. Questions, ideas, and feedback reach me without layers in between.</p></article><article><span>02</span><h3>Made for your team</h3><p>Reusable sections and editable content help your team keep the website useful long after launch.</p></article><article><span>03</span><h3>Details that matter</h3><p>Responsive layouts, usable forms, performance, and accessibility inform the build from the start.</p></article></div></section>
  <section class="process-section section-wrap"><div><div class="section-kicker"><span class="small-star">✳</span> FROM FIRST IDEA TO LIVE WEBSITE</div><h2>A clear path<br>to <span class="accent">launch.</span></h2><p>Four steps. A shared direction.<br>No guesswork about what comes next.</p>{button('Start a conversation','#contact')}</div><div class="process-list">{''.join(f'<details {"open" if i==0 else ""}><summary><span class="step-number">0{i+1}</span><h3>{name}</h3><span class="details-plus" aria-hidden="true">+</span></summary><p>{text}</p></details>' for i,(name,text) in enumerate(process))}</div></section>
  <section class="services-work section-wrap"><div class="section-heading"><div><div class="section-kicker"><span class="small-star">✳</span> FROM THE PORTFOLIO</div><h2>See it <span class="accent">in the work.</span></h2></div><a class="text-link" href="/work/">Explore all work {icon('diagonal')}</a></div><a class="wide-project" href="/work/#didi-hirsch"><img src="/assets/didi.jpg" alt="Didi Hirsch website displayed across desktop layouts" width="1920" height="1280" loading="lazy"><div><span class="section-kicker">WEB DESIGN / DEVELOPMENT</span><h3>Didi Hirsch</h3><span class="text-link">Take a closer look {icon('diagonal')}</span></div></a></section>
  <section class="faq-section section-wrap"><div><div class="section-kicker"><span class="small-star">✳</span> A FEW HELPFUL ANSWERS</div><h2>Before we<br><span class="accent">get started.</span></h2><p>Have a different question?</p><a class="text-link" href="mailto:hello@talha-ali.com">Ask me directly {icon('diagonal')}</a></div><div class="faq-list">{''.join(f'<details><summary>{question}<span class="details-plus" aria-hidden="true">+</span></summary><p>{answer}</p></details>' for question,answer in faqs)}</div></section>
'''
save_page('services', 'Website Design & Development Services', 'Custom WordPress, website design, e-commerce, technical SEO, website care, and integrations by Talha Ali.', services_main)

work_main = f'''
  <section class="work-page-hero section-wrap"><div class="breadcrumb"><a href="/">Home</a><span>/</span>Work</div><div class="section-kicker"><span class="small-star">✳</span> THE PORTFOLIO</div><h1>Creative work.<br><span class="outlined">Built for people.</span></h1><div class="work-intro"><p>A closer look at the design, development, and details behind a few selected web experiences.</p><a class="text-link" href="#projects">Explore the projects <span aria-hidden="true">↓</span></a></div></section>
  <section class="work-reel section-wrap"><div class="reel-side"><span class="section-kicker">A QUICK LOOK</span><h2>Work in<br><span class="accent">motion.</span></h2><p>Press play for a short look at the portfolio, from a desktop experience to a website made for smaller screens.</p></div>{video(True)}</section>
  <section class="portfolio-list section-wrap" id="projects"><div class="portfolio-section-top"><span>SELECTED PROJECTS</span><span>02 / WEB EXPERIENCES</span></div><div class="portfolio-grid">
    <article class="portfolio-item" id="didi-hirsch"><a class="portfolio-visual" href="https://talha-ali.com/case-studies/didi-hirsch/" target="_blank" rel="noopener noreferrer"><img src="/assets/didi.jpg" alt="Didi Hirsch website design with desktop and page layouts" width="1920" height="1280" loading="lazy"><span class="project-open">{icon('diagonal')}</span></a><div class="project-meta"><span>WEB DESIGN / DEVELOPMENT</span><span>01</span></div><h2>Didi Hirsch</h2><p>A closer look at the layouts and visual direction of the Didi Hirsch website, as featured in my portfolio.</p><div class="tech-tags"><span>Website design</span><span>Desktop experience</span><span>Responsive layouts</span></div><a class="text-link" href="https://talha-ali.com/case-studies/didi-hirsch/" target="_blank" rel="noopener noreferrer">View the project {icon('diagonal')}</a></article>
    <article class="portfolio-item" id="mobile-experience"><a class="portfolio-visual" href="https://talha-ali.com/" target="_blank" rel="noopener noreferrer"><img src="/assets/fortress.jpg" alt="Cedar Springs website displayed on a mobile phone" width="1920" height="1280" loading="lazy"><span class="project-open">{icon('diagonal')}</span></a><div class="project-meta"><span>RESPONSIVE WEB EXPERIENCE</span><span>02</span></div><h2>Made for every screen.</h2><p>A mobile website showcase from my portfolio, with a focus on visual presentation and the experience on a smaller screen.</p><div class="tech-tags"><span>Mobile design</span><span>Responsive development</span></div><a class="text-link" href="https://talha-ali.com/" target="_blank" rel="noopener noreferrer">Visit the original portfolio {icon('diagonal')}</a></article>
  </div></section>
  <section class="work-statement section-wrap"><span class="small-star" aria-hidden="true">✳</span><h2>Different businesses.<br>Different challenges.<br><span class="accent">The same care in every detail.</span></h2><div class="statement-bottom"><p>Have a design ready to build, a store to improve, or an idea that needs a starting point?</p>{button('Find the right service','/services/',True)}</div></section>
'''
save_page('work', 'Selected Website Design & Development Work', 'Explore selected website projects and a short portfolio showreel by Talha Ali.', work_main)
print('Updated home navigation; created /services/ and /work/.')
