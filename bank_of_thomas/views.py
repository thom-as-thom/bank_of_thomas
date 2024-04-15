from django.shortcuts import render
from django.templatetags.static import static


def home(request):
    banner1_context = {
        "super_title": "What are you waiting for to start referring and enjoy the benefits of T-Bank?",
        "title": "With referrals you can also travel!",
        "sub_title": "Choose T-Bank Points or credit balance on your credit card",
        "cta": "Learn more",
        "cta_href": "#",
        "image_url": static("images/image-36.jpg"),
    }
    banner2_context = {
        "sub_title": "Get to know our insurance",
        "title": "T-Bank car insurance",
        "sub_title": "You have up to 50 percent discount on the first installments. Hire it or quote it fully online. Choose the plan that best suits your needs, and that's it!",
        "cta": "Learn more",
        "cta_href": "#",
        "image_url": static("images/image-37.jpg"),
    }
    carrousel_content = [
        {
            "title": "Invest",
            "image_url": static("images/image-38.jpg"),
        },
        {
            "title": "Banking services for your company",
            "image_url": static("images/image-39.jpg"),
        },
        {
            "title": "Purchase life insurance",
            "image_url": static("images/image-40.jpg"),
        },
        {
            "title": "Request your mortgage loan",
            "image_url": static("images/image-42.jpg"),
        },
        {
            "title": "Open a savings account",
            "image_url": static("images/image-43.jpg"),
        },
        {
            "title": "Request a credit card",
            "image_url": static("images/image-44.jpg"),
        },
    ]
    return render(
        request,
        "home.html",
        {
            "banner1": banner1_context,
            "banner2": banner2_context,
            "carrousel": carrousel_content,
        },
    )
