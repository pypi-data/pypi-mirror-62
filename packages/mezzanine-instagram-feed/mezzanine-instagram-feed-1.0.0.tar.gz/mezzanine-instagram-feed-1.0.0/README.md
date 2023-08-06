
# Mezzanine Instagram Feed

Connect Mezzanine sites to Instagram feeds

## Installation

1. Install via pip: `pip install mezzanine-instagram-feed`.
2. Add `instagramfeed` to your `INSTALLED_APPS`.

## Usage

Load the templatetag library and pass the username you want to query to the `instagramfeed_photos` template tag.

```django
{% load instagramfeed_tags %}

{% instagram_posts "USERNAME HERE" as posts %}
{% for posts in post %}
  <a href="https://instagram.com/p/{{ post.shortcode }}">
    <img src="{{ post.thumbnail_src }}" alt="{{ post.edge_media_to_caption.edges.0.node.text }}">
  </a>
{% endfor %}
```

## Contributing

Review contribution guidelines at [CONTRIBUTING.md].

[CONTRIBUTING.md]: CONTRIBUTING.md
