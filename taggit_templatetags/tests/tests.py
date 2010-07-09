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
        

class TaggableManagerTestCase(BaseTaggingTest):
    food_model = Food
    pet_model = Pet
    housepet_model = HousePet
    
    def test_add_tag(self):
        apple = self.food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(self.food_model.tags.all()),  [])

        apple.tags.add('green')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add('green')
        self.assert_tags_equal(pear.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        apple.tags.add('red')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])

        self.assert_tags_equal(
            self.food_model.tags.most_common(),
            ['green', 'red'],
            sort=False
        )

        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])
        tag = Tag.objects.create(name="delicious")
        apple.tags.add(tag)
        self.assert_tags_equal(apple.tags.all(), ["red", "delicious"])
        
        apple.delete()
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])
        
        f = self.food_model()
        with self.assert_raises(ValueError):
            f.tags.all()
    
    def test_unique_slug(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("Red", "red")

    def test_delete_obj(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red")
        self.assert_tags_equal(apple.tags.all(), ["red"])
        strawberry = self.food_model.objects.create(name="strawberry")
        strawberry.tags.add("red")
        apple.delete()
        self.assert_tags_equal(strawberry.tags.all(), ["red"])

    def test_lookup_by_tag(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green")
        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green")

        self.assertEqual(
            list(self.food_model.objects.filter(tags__in=["red"])),
            [apple]
        )
        self.assertEqual(
            list(self.food_model.objects.filter(tags__in=["green"])),
            [apple, pear]
        )

        kitty = self.pet_model.objects.create(name="kitty")
        kitty.tags.add("fuzzy", "red")
        dog = self.pet_model.objects.create(name="dog")
        dog.tags.add("woof", "red")
        self.assertEqual(
            list(self.food_model.objects.filter(tags__in=["red"]).distinct()),
            [apple]
        )

        tag = Tag.objects.get(name="woof")
        self.assertEqual(list(self.pet_model.objects.filter(tags__in=[tag])), [dog])

        cat = self.housepet_model.objects.create(name="cat", trained=True)
        cat.tags.add("fuzzy")

        self.assertEqual(
            map(lambda o: o.pk, self.pet_model.objects.filter(tags__in=["fuzzy"])),
            [kitty.pk, cat.pk]
        )

    def test_similarity_by_tag(self):
        """Test that pears are more similar to apples than watermelons"""
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green", "juicy", "small", "sour")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "juicy", "small", "sweet")

        watermelon = self.food_model.objects.create(name="watermelon")
        watermelon.tags.add("green", "juicy", "large", "sweet")

        similar_objs = apple.tags.similar_objects()
        self.assertEqual(similar_objs, [pear, watermelon])
        self.assertEqual(map(lambda x: x.similar_tags, similar_objs), [3, 2])

    def test_tag_reuse(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy", "juicy")
        self.assert_tags_equal(apple.tags.all(), ['juicy'])


class TaggableManagerDirectTestCase(TaggableManagerTestCase):
    food_model = DirectFood
    pet_model = DirectPet
    housepet_model = DirectHousePet


class TaggableFormTestCase(BaseTaggingTest):
    form_class = FoodForm
    food_model = Food
    
    def test_form(self):
        self.assertEqual(self.form_class.base_fields.keys(), ['name', 'tags'])

        f = self.form_class({'name': 'apple', 'tags': 'green, red, yummy'})
        self.assertEqual(str(f), """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>\n<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy" id="id_tags" /></td></tr>""")
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])

        f = self.form_class({'name': 'apple', 'tags': 'green, red, yummy, delicious'}, instance=apple)
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy', 'delicious'])
        self.assertEqual(self.food_model.objects.count(), 1)
        
        f = self.form_class({"name": "raspberry"})
        raspberry = f.save()
        self.assert_tags_equal(raspberry.tags.all(), [])
        
        f = self.form_class(instance=apple)
        self.assertEqual(str(f), """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" value="apple" maxlength="50" /></td></tr>\n<tr><th><label for="id_tags">Tags:</label></th><td><input type="text" name="tags" value="green, red, yummy, delicious" id="id_tags" /></td></tr>""")

class TaggableFormDirectTestCase(TaggableFormTestCase):
    form_class = DirectFoodForm
    food_model = DirectFood
