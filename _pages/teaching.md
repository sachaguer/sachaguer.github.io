---
layout: page
permalink: /teaching/
title: Teaching
description: "A collection of notebooks and pages related to my teaching activity at <em>Université Paris Cité</em>."
nav: true
nav_order: 6
horizontal: false
display_categories: [statistical-physics]
---

<!-- pages/teaching.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized teaching materials -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
      {% assign _heading_raw = category | replace: '-', ' ' %}
      {% capture _heading_pretty %}{% for w in _heading_raw | split: ' ' %}{% if forloop.first == false %} {% endif %}{{ w | capitalize }}{% endfor %}{% endcapture %}
      <h2 class="category">{{ _heading_pretty }}</h2>
    </a>
  {% assign categorized_teaching = "" | split: "" %}{% for teaching in site.teaching %}{% if teaching.category == category %}{% assign categorized_teaching = categorized_teaching | push: teaching %}{% endif %}{% endfor %}{% assign sorted_teaching = categorized_teaching | sort: "importance" %}
  <!-- Generate cards for each teaching item -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_teaching %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_teaching %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display teaching materials without categories -->

{% assign sorted_teaching = site.teaching | sort: "importance" %}

  <!-- Generate cards for each teaching item -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_teaching %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_teaching %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
