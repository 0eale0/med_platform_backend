from rest_framework import serializers

from apps.menus.models import Menu, Ingredient, Dish, Day, DayDish, DishIngredient


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class DishSerializerForPatient(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'default_weight', 'proteins',
                  'fats', 'carbohydrates', 'calories', 'recipe', 'day']

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):
    menu = MenuSerializer()

    class Meta:
        model = Day
        fields = "__all__"


class DayDishSerializer(serializers.ModelSerializer):
    day = DaySerializer()
    dish = DishSerializer()

    class Meta:
        model = DayDish
        fields = "__all__"


class DishIngredientSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = "__all__"


class DishListSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    additional = serializers.SerializerMethodField()

    def get_additional(self, obj):
        return DayDishSerializer(DayDish.objects.filter(additional_to=obj).all(), many=True).data

    class Meta:
        model = DayDish
        fields = "__all__"


class IngredientAndAmountSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    default_weight = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_ingredient_name

    def get_id(self, obj):
        return obj.get_ingredient_id

    def get_amount(self, obj):
        return obj.ingredient_amount

    def get_default_weight(self, obj):
        return obj.get_ingredient_default_weight

    class Meta:
        model = DishIngredient
        fields = ['amount', 'name', 'id', 'default_weight']


class DishDetailSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        return IngredientAndAmountSerializer(DishIngredient.objects.filter(dish=obj).all(), many=True).data

    class Meta:
        model = Dish
        fields = "__all__"


class AdditionalAndDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        exclude = ['day', 'id']


class DishAndTimeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='dish.id')
    name = serializers.CharField(source='dish.name')
    amount = serializers.CharField(source='dish.default_weight')
    proteins = serializers.CharField(source='dish.proteins')
    fats = serializers.CharField(source='dish.fats')
    carbohydrates = serializers.CharField(source='dish.carbohydrates')
    calories = serializers.CharField(source='dish.calories')
    recipe = serializers.CharField(source='dish.recipe')
    additional_to = serializers.SerializerMethodField()

    def get_additional_to(self, obj):
        dishes = [day.dish for day in DayDish.objects.filter(additional_to=obj.dish_id).all()]
        return AdditionalAndDaySerializer(dishes, many=True).data

    class Meta:
        model = DayDish
        exclude = ['dish', 'day', 'dish_amount']


class DayDishDetailSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()

    def get_dishes(self, obj):
        return DishAndTimeSerializer(DayDish.objects.filter(day_id=obj.id).all(), many=True).data

    class Meta:
        model = Day
        exclude = ['menu']
