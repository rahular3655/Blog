from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from .models import StaticText
from .serializers import StaticTextSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework import serializers


class StaticTextSerializerTest(TestCase):
    def setUp(self):
        # Create a sample StaticText object for testing
        self.static_text_data = {
            "page_name": "SIGNUP_PAGE",
            "static_text": {
                    "PLEASE_ENTER_YOUR_NAME": [{"en": "Please enter your name"}, {"tn": "கடவு சொல்லை திருப்பி உள்ளிடு"}], 
                    "PLEASE_ENTER_YOUR_PASSWORD": [{"en": "Please enter your password"}, {"tn": "கடவு சொல்லை திருப்பி உள்ளிடு"}]
                },
            "image": "wallpapers/Screenshot_from_2023-07-24_12-14-01.png",
        }
        self.static_text = StaticText.objects.create(**self.static_text_data)

        # Create a request factory for simulating requests
        self.factory = RequestFactory()

    def test_valid_translation(self):
        # Mock the request with the required headers
        request = self.factory.get(
            "/some-url/",
            HTTP_ACCEPT_LANGUAGE="en",
            HTTP_PAGE_NAME="SIGNUP_PAGE",
        )

        serializer = StaticTextSerializer()
        translated_text = serializer.get_filtered_queryset(request)

        expected_result = [
            {
                "PLEASE_ENTER_YOUR_NAME": "Please enter your name"
            },
            {
                "PLEASE_ENTER_YOUR_PASSWORD": "Please enter your password"
            },
            {
                "image": "wallpapers/Screenshot_from_2023-07-24_12-14-01.png"
            }
        ]
        self.assertEqual(translated_text, expected_result)

    def test_invalid_page_name(self):
        # Mock the request with missing page_name header
        request = self.factory.get(
            "/some-url/",
            HTTP_ACCEPT_LANGUAGE="en",
        )

        serializer = StaticTextSerializer()

        with self.assertRaises(serializers.ValidationError) as context:
            serializer.get_filtered_queryset(request)

        self.assertEqual(
            context.exception.detail, ["page name is required."]
        )
        
    def test_no_image(self):
        # Mock the request without image
        self.static_text.image = None
        self.static_text.save()

        request = self.factory.get(
            "/some-url/",
            HTTP_ACCEPT_LANGUAGE="en",
            HTTP_PAGE_NAME="SIGNUP_PAGE",
        )

        serializer = StaticTextSerializer()
        translated_text = serializer.get_filtered_queryset(request)

        expected_result = [
            {
                "PLEASE_ENTER_YOUR_NAME": "Please enter your name"
            },
            {
                "PLEASE_ENTER_YOUR_PASSWORD": "Please enter your password"
            },
            {
                "image": ""
            }
        ]
        self.assertEqual(translated_text, expected_result)
        
    # def test_empty_language(self):
    #     # Mock the request with missing page_name header
    #     request = self.factory.get(
    #         "/some-url/",
    #         HTTP_ACCEPT_LANGUAGE="",
    #     )

    #     serializer = StaticTextSerializer()

    #     serializer = StaticTextSerializer()
    #     translated_text = serializer.get_filtered_queryset(request)
        
    #     expected_result = [
    #         {
    #             "PLEASE_ENTER_YOUR_NAME": "Please enter your name"
    #         },
    #         {
    #             "PLEASE_ENTER_YOUR_PASSWORD": "Please enter your password"
    #         },
    #         {
    #             "image": "wallpapers/Screenshot_from_2023-07-24_12-14-01.png"
    #         }
    #     ]

    #     self.assertEqual(translated_text, expected_result)
