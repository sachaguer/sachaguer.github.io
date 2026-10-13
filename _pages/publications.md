---
layout: page
permalink: /publications/
title: Publications
description: "automatically generated publication list from SciX's ADS service, powered by jekyll-scholar. You can directly check the list of publications on SciX's ADS service <a href='https://scixplorer.org/search?d=general&p=1&q=author%3A%22Sacha+Guerrini%22++collection%3A%22astronomy%22&sort=score+desc&sort=date+desc'>here</a>."
years: [2026, 2025, 2024]
nav: true
nav_order: 1
---

<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}

  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
