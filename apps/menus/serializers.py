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

    class Meta:
        model = DayDish
        fields = "__all__"


class IngredientAndAmountSerializer(serializers.ModelSerializer):
    # эту штуку можно было сделать и красивее, но я не придумал как
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
    # можно и нужно логику перенести сюда,
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        return IngredientAndAmountSerializer(DishIngredient.objects.filter(dish=obj).all(), many=True).data

    class Meta:
        model = Dish
        fields = "__all__"
