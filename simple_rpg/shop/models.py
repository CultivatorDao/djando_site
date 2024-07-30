from django.db import models

# Create your models here.


class Rarity(models.Model):
    name = models.CharField(max_length=20)
    multiplier = models.FloatField(default=1.0)
    color = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    def get_next(self):
        pk = self.pk + 1 if Rarity.objects.last().pk >= self.pk + 1 else self.pk
        return Rarity.objects.get(pk=pk)


class Item(models.Model):
    name = models.CharField(max_length=30)
    rarity = models.ForeignKey(Rarity, related_name="items", on_delete=models.SET_DEFAULT, default=None)
    # refinement = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.apply_rarity_bonus()

    def __str__(self):
        return f"{self.rarity} {self.name}"

    def apply_rarity_bonus(self):
        raise NotImplementedError()

    def increase_rarity(self, rarity=None):
        if rarity:
            self.rarity = rarity
        else:
            rarity = self.rarity.get_next()

        self.rarity = rarity
        self.apply_rarity_bonus()

    # def apply_refinement_bonus(self):
    #     raise NotImplementedError()

    # def increase_refinement(self):
    #     self.refinement += 1
    #     self.apply_refinement_bonus()


class Consumable(Item):
    effect_type = models.CharField(max_length=50)
    effect_power = models.IntegerField(default=0)

    def apply_rarity_bonus(self):
        self.effect_power *= self.rarity.multiplier

    def consume(self, consumer):
        pass


class Ingredient(Item):
    ingredient_type = models.CharField(max_length=50)
    hardness = models.IntegerField(default=0)

    def apply_rarity_bonus(self):
        self.hardness *= self.rarity.multiplier


class Equipment(Item):
    pass
