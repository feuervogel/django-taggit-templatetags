from django.conf import settings

# define the minimal weight of a tag in the tagcloud
TAGCLOUD_MIN = getattr(settings, 'TAGGIT_TAGCLOUD_MIN', 1.0)

# define the maximum weight of a tag in the tagcloud 
TAGCLOUD_MAX = getattr(settings, 'TAGGIT_TAGCLOUD_MAX', 6.0) 