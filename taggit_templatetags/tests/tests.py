from django.test import TestCase
from django.template import Context, Template

from taggit_templatetags.tests.models import AlphaModel, BetaModel
from taggit.tests.tests import BaseTaggingTest

class TemplateTagListTestCase(BaseTaggingTest):
    a_model = AlphaModel
    b_model = BetaModel
    
    def setUp(self):
        a1 = self.a_model.objects.create(name="apple")
        a2 = self.a_model.objects.create(name="pear")
        b1 = self.b_model.objects.create(name="dog")
        b2 = self.b_model.objects.create(name="kitty")
        
        a1.tags.add("green")
        a1.tags.add("sweet")
        a1.tags.add("fresh")
        
        a2.tags.add("yellow")
        a2.tags.add("sour")
        
        b1.tags.add("sweet")
        b1.tags.add("yellow")
        
        b2.tags.add("sweet")
        b2.tags.add("green")
    
    def get_template(self, argument):
        return """      {%% load taggit_extras %%}
                        {%% get_taglist %s %%}
                """ % argument
                
    def test_project(self):
        t = Template(self.get_template("as taglist"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["sweet", "green", "yellow", "fresh", "sour"], False)
        
    def test_app(self):
        t = Template(self.get_template("as taglist for 'tests'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["sweet", "green", "yellow", "fresh", "sour"], False)
        
    def test_model(self):
        t = Template(self.get_template("as taglist for 'tests.pet'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["sweet", "green", "yellow"], False)

class TemplateTagCloudTestCase(BaseTaggingTest):
    a_model = AlphaModel
    b_model = BetaModel
    
    def setUp(self):
        a1 = self.a_model.objects.create(name="apple")
        a2 = self.a_model.objects.create(name="pear")
        b1 = self.b_model.objects.create(name="dog")
        b2 = self.b_model.objects.create(name="kitty")
        
        a1.tags.add("green")
        a1.tags.add("sweet")
        a1.tags.add("fresh")
        
        a2.tags.add("yellow")
        a2.tags.add("sour")
        
        b1.tags.add("sweet")
        b1.tags.add("yellow")
        
        b2.tags.add("sweet")
        b2.tags.add("green")
    
    def get_template(self, argument):
        return """      {%% load taggit_extras %%}
                        {%% get_tagcloud %s %%}
                """ % argument
                
    def test_project(self):
        t = Template(self.get_template("as taglist"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["fresh", "green", "sour", "sweet", "yellow"], False)
        self.assert_equal(c.get("taglist")[3].name, "sweet")
        self.assert_equal(c.get("taglist")[3].weight, 6.0)
        self.assert_equal(c.get("taglist")[1].name, "green")
        self.assert_equal(c.get("taglist")[1].weight, 5.0)
        self.assert_equal(c.get("taglist")[2].name, "sour")
        self.assert_equal(c.get("taglist")[2].weight, 1.0)
                
    def test_app(self):
        t = Template(self.get_template("as taglist for 'tests'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["fresh", "green", "sour", "sweet", "yellow"], False)
        self.assert_equal(c.get("taglist")[3].name, "sweet")
        self.assert_equal(c.get("taglist")[3].weight, 6.0)
        self.assert_equal(c.get("taglist")[1].name, "green")
        self.assert_equal(c.get("taglist")[1].weight, 5.0)
        self.assert_equal(c.get("taglist")[2].name, "sour")
        self.assert_equal(c.get("taglist")[2].weight, 1.0)  
        
    def test_model(self):
        t = Template(self.get_template("as taglist for 'tests.pet'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["green", "sweet", "yellow"], False)
        self.assert_equal(c.get("taglist")[0].name, "green")
        self.assert_equal(c.get("taglist")[0].weight, 6.0)
        self.assert_equal(c.get("taglist")[1].name, "sweet")
        self.assert_equal(c.get("taglist")[1].weight, 2.5)
        self.assert_equal(c.get("taglist")[2].name, "yellow")
        self.assert_equal(c.get("taglist")[2].weight, 1.0)