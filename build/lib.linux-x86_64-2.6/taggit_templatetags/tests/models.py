from django.db import models

from taggit.managers import TaggableManager

class BaseModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.name
    
    class Meta(object):
        abstract = True 

class AlphaModel(BaseModel):
    pass

class BetaModel(BaseModel):
    pass
