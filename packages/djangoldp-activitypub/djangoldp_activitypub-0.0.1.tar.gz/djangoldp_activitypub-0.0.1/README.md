# DjangoLDP ActivityPub

Enable activitypub on all djangoldp modules

## Setup
1 - Add the routing middleware on settings.py to route requests accepting `application/activity+json` to the module views

```python
MIDDLEWARE = [...]
MIDDLEWARE += [
    'djangoldp_activitypub.routing.middleware.HTTPHeaderRoutingMiddleware',
]
```

2 - Configure the routing middleware
```python
HTTP_HEADER_ROUTING_MIDDLEWARE_URLCONF_MAP = {
    'application/activity+json': 'djangoldp_activitypub.routing.urls',
}
```

## Send Activity

You can listen Activity changes with `@receiver` and interact like this :

```python
try:
    from djangoldp_activitypub.models import Follower
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from djangoldp_activitypub.activities import AP
    from djangoldp_joboffer.models import JobOffer


    @receiver(post_save, sender=Follower)
    def on_follower(sender, instance, **kwargs):                 # Auto accept follow requests
        if not instance.confirmed:
            AP.accept(instance)

    @receiver(post_save, sender=JobOffer)
    def on_job_offer(sender, instance, **kwargs):
        AP.create_activity(AP.note(JobOffer, instance))


except ModuleNotFoundError:
    pass
```
