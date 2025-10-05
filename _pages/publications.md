---
layout: page
permalink: /publications/
title: Publications
description: "automatically generated publication list from NASA's ADS service, powered by jekyll-scholar. You can directly check the list of publications on NASA's ADS service <a href='https://ui.adsabs.harvard.edu/search/filter_author_facet_hier_fq_author=AND&filter_author_facet_hier_fq_author=author_facet_hier%3A%220%2FGuerrini%2C%20S%22&fq=%7B!type%3Daqp%20v%3D%24fq_database%7D&fq=%7B!type%3Daqp%20v%3D%24fq_author%7D&fq_author=(author_facet_hier%3A%220%2FGuerrini%2C%20S%22)&fq_database=(database%3Aastronomy%20OR%20database%3Aphysics)&q=%20author%3A%22Sacha%20Guerrini%22&sort=date%20desc%2C%20bibcode%20desc&p_=0'>here</a>."
years: [2025, 2024]
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
