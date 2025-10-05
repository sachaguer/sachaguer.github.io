---
layout: page
permalink: /publications/
title: Publications
description: automatically generated publication list from NASA's ADS service, powered by jekyll-scholar.
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