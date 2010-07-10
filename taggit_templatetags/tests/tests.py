from django.test import TestCase
from django.template import Context, Template

from taggit_templatetags.tests.models import AlphaModel, BetaModel
from taggit.tests.tests import BaseTaggingTest

from taggit_templatetags.templatetags.taggit_extras import get_weight_fun

class TestWeightFun(TestCase):
    def test_one(self):
        t_min = 1
        t_max = 6
        f_min = 10
        f_max = 20
        weight_fun = get_weight_fun(t_min, t_max, f_min, f_max)
        self.assertEqual(weight_fun(20), 6)
        self.assertEqual(weight_fun(10), 1)
        self.assertEqual(weight_fun(15), 3.5)
    
    def test_two(self):
        t_min = 10
        t_max = 100
        f_min = 5
        f_max = 7
        weight_fun = get_weight_fun(t_min, t_max, f_min, f_max)
        self.assertEqual(weight_fun(5), 10)
        self.assertEqual(weight_fun(7), 100)
        self.assertEqual(weight_fun(6), 55)


class TemplateTagListTestCase(TestCase, BaseTaggingTest):
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
        t = Template(self.get_template("as taglist for 'tests.BetaModel'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["sweet", "green", "yellow"], False)

class TemplateTagCloudTestCase(TestCase, BaseTaggingTest):
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
                
    def atest_project(self):
        t = Template(self.get_template("as taglist"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["fresh", "green", "sour", "sweet", "yellow"], False)
        self.assertEqual(c.get("taglist")[3].name, "sweet")
        self.assertEqual(c.get("taglist")[3].weight, 6.0)
        self.assertEqual(c.get("taglist")[1].name, "green")
        self.assertEqual(c.get("taglist")[1].weight, 5.0)
        self.assertEqual(c.get("taglist")[2].name, "sour")
        self.assertEqual(c.get("taglist")[2].weight, 1.0)
                
    def atest_app(self):
        t = Template(self.get_template("as taglist for 'tests'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["fresh", "green", "sour", "sweet", "yellow"], False)
        self.assertEqual(c.get("taglist")[3].name, "sweet")
        self.assertEqual(c.get("taglist")[3].weight, 6.0)
        self.assertEqual(c.get("taglist")[1].name, "green")
        self.assertEqual(c.get("taglist")[1].weight, 5.0)
        self.assertEqual(c.get("taglist")[2].name, "sour")
        self.assertEqual(c.get("taglist")[2].weight, 1.0)  
        
    def test_model(self):
        t = Template(self.get_template("as taglist for 'tests.BetaModel'"))
        c = Context({})
        t.render(c)
        self.assert_tags_equal(c.get("taglist"), ["green", "sweet", "yellow"], False)
        self.assertEqual(c.get("taglist")[0].name, "green")
        self.assertEqual(c.get("taglist")[0].weight, 1.0)
        self.assertEqual(c.get("taglist")[1].name, "sweet")
        self.assertEqual(c.get("taglist")[1].weight, 6.0)
        self.assertEqual(c.get("taglist")[2].name, "yellow")
        self.assertEqual(c.get("taglist")[2].weight, 1.0)