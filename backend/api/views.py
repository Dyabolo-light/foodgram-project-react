from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginators import BasePaginator
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             RecipeReadSerializer,
                             RecipesByFollowingSerializer,
                             RecipeWriteSerializer, TagSerializer,
                             UserSerializer, SubscribeSerializer)
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Cart, Favourite, Follow, Ingredient,
                            IngredientsInRecipe, Recipe, Tag)
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser


class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = BasePaginator
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        serializer_class=SubscribeSerializer
    )
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(CustomUser, id=self.kwargs.get('id'))
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        if request.method == 'POST':
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(Follow, author=author, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        serializer_class=FollowSerializer,
    )
    def subscriptions(self, request):
        follows = CustomUser.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        serializer = self.get_serializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = BasePaginator
    filterset_class = RecipeFilter
    serializer_class = RecipeWriteSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated, ],
        serializer_class=RecipesByFollowingSerializer
    )
    def favorite(self, request, pk):
        recipe = self.get_object()
        if request.method == 'POST':
            # if Favourite.objects.filter(
            #         recipe=recipe, user=self.request.user
            # ).exists():
            #     return Response(
            #         {'Error message': 'Рецепт уже есть в избранном'},
            #         status=status.HTTP_400_BAD_REQUEST)
            Favourite.objects.create(recipe=recipe, user=self.request.user)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favourite.objects.filter(recipe=recipe,
                                 user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated, ],
        serializer_class=RecipesByFollowingSerializer
    )
    def shopping_cart(self, request, pk):
        recipe = self.get_object()
        if request.method == 'POST':
            # if Cart.objects.filter(
            #         recipe=recipe, user=self.request.user
            # ).exists():
            #     return Response(
            #         {'Error message': 'Рецепт уже есть в списке покупок'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            Cart.objects.create(recipe=recipe, user=self.request.user)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Cart.objects.filter(recipe=recipe, user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount')).order_by('ingredient__name')

        shopping_list = 'Список покупок:\n'
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient.get("ingredient__name")}'
                f' {ingredient.get("total_amount")}'
                f' {ingredient.get("ingredient__measurement_unit")}\n'
            )
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename=shopping_cart.txt'
        )
        return response


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    pagination_class = None
    search_fields = ('^name',)
