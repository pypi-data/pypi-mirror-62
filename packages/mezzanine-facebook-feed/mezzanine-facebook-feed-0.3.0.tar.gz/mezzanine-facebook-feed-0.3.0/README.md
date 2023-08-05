
# Mezzanine Facebook Feed

Connect Mezzanine sites to Facebook feeds

## Installation

1. Install via pip: `pip install mezzanine-facebook-feed`.
2. Add `fbfeed` to your `INSTALLED_APPS`.
3. Run migrations.

## Usage

### Add Facebook App credentials

Add your Facebook App ID and Secret to Mezzanine's setting page. Configure your App with a redirect URI of `<your domain>/admin/fbfeed/access/redirect/`.

### Create an Access instance

To access Facebook you need to create access tokens so Mezzanine can run queries on your behalf. To create access tokens visit your admin site and click `FB Feed > Access`.

1. Create an Access instance and give it a name (this is arbitrary and for your use only).
1. Set Facebook ID to the numeric ID of the user or page you want to query. If you want to query your own data, enter "me".
1. Save the Access instance and open it again in the admin.
1. Click the "Get Access Token" button in the upper-right corner.
1. You will be redirected to Facebook. Complete the login process.
1. If everything goes well, you'll see the access token in the Access admin page.
1. Otherwise an error message will be shown on the top of the admin site.

### Display your data in templates

```django
{% load fbfeed_tags %}
{% fbfeed_photos as photos %}
{% for photo in photos %}
  <a href="{{ photo.link }}">
    <img src="{{ photo.images.0.source }}" alt="{{ photo.alt_text }}">
  </a>
{% endfor %}
```

## Contributing

Review contribution guidelines at [CONTRIBUTING.md].

[CONTRIBUTING.md]: CONTRIBUTING.md
