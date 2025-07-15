# # BookListSerializer, BookDetailSerializer, BookCreateSerializer
# from rest_framework import serializers
# from .models import Book, Publisher
# from django.utils import timezone
#
# class BookCreateSerializer(serializers.ModelSerializer):
#     title = serializers.SerializerMethodField(validators=[validate_title_length])
#     amount_pages = serializers.IntegerField()
#     publisher = serializers.SerializerMethodField(
#         slug_field='slug',
#         queryset=Publisher.objects.all(),
#     )
#
#     class Meta:
#         model = Book
#         fields = ('title',
#                   'author',
#                   'publication_date',
#                   'description',
#                   'Genre',
#                   'amount_pages',
#                   'publisher',
#                   'created_at',
#                   'category',)
#         read_only_fields = ('created_at', 'id')
#
#     def create(self, validated_data):
#         validated_data['created_at'] = timezone.now()
#         return super().create(validated_data)
#
#     def validate(self, data):
#         if 'title' in validated_date:
#
#         if data['discounted_price'] > data['price']:
#             raise serializers.ValidationError("Discounted price cant be higher than regular price")
#
#         return data
#
#
# class BookListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#
# class BookDetailSerializer(serializers.ModelSerializer):
#     publisher = serializers.PrimaryKeyRelatedField(
#         # slug_field='name',
#         queryset=Publisher.objects.all()
#     )
#
#     class Meta:
#         model = Book
#         fields = '__all__'
