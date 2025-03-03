from rest_framework import serializers

from .models import StaticText, Regulations, CompanyDetails, FAQ, SocialMediaUrl, DropDownClass, DropDown, FaqCategory, FAQAnswer


class ListStaticTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticText
        fields = ('title', 'slug',)


class RegulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulations
        fields = ('name', 'value', 'is_public', 'description',)


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = ('name', 'slug',)


class FAQAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQAnswer
        fields = ('answer',)


class FAQSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ('question', 'answers')

    def get_answers(self, obj):
        faq_answers = FAQAnswer.objects.filter(question=obj)
        return FAQAnswerSerializer(faq_answers, many=True).data


class SocialMediaUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUrl
        fields = ('name', 'url', 'image',)


class CompanySerializer(serializers.ModelSerializer):
    urls = SocialMediaUrlSerializer(many=True)

    class Meta:
        model = CompanyDetails
        fields = ('name', 'email', 'address', 'phone', 'logo', 'logo_white', 'urls')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        active_urls = instance.urls.filter(is_active=True)
        data['urls'] = SocialMediaUrlSerializer(active_urls, many=True).data
        return data


class DropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDown
        fields = ('id', 'value',)


class DropDownListSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()

    class Meta:
        model = DropDownClass
        fields = ('name', 'slug', 'values')

    def get_values(self, obj):
        dropdowns = obj.dropdowns.all()
        return DropDownSerializer(dropdowns, many=True).data
