BATON = {
    'SITE_HEADER': 'Kalpafit',
    'SITE_TITLE': 'Kalpafit',
    'INDEX_TITLE': 'Site administration',
    'SUPPORT_HREF': '',
    'COPYRIGHT': 'All rights reserved by DigitalPrizm',  # noqa
    'POWERED_BY': 'DigitalPrizm',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'COLLAPSABLE_USER_AREA': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': False,
    'GRAVATAR_DEFAULT_IMG': 'retro',
    'GRAVATAR_ENABLED': True,
    'LOGIN_SPLASH': '',
    'FORCE_THEME': True,
    'SEARCH_FIELD': {
        'label': 'Search contents...',
        'url': '/search/',
    },

    'MENU': (
        # User Management http://127.0.0.1:8000/admin/accounts/user/?is_author__exact=1
        # { 'type': 'title', 'label': 'Users', 'apps': ('accounts',) },
        {'type': 'free', 'label': 'User Management', 'children': [
            {'type': 'model', 'label': 'Users List', 'name': 'user', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'Authors List', 'name': 'authormodel', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'User Profile', 'name': 'userprofile', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            # {'type': 'model', 'label': 'User Devices', 'name': 'userdevice', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'User OTP', 'name': 'userotp', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'Group Permissions', 'name': 'group', 'app': 'auth', 'icon': 'fa fa-gavel'},
        ]},

        # Product Management
        {'type': 'free', 'label': 'Product Management', 'children': [

            {'type': 'free', 'label': 'Product', 'children': [
                {'type': 'model', 'label': 'Product Categories', 'name': 'category', 'app': 'catalogue', 'icon': 'fa fa-gavel',
                 'class': 'custom-yellow'},
                # category
                {'type': 'model', 'label': 'Option Groups', 'name': 'attributeoptiongroup', 'app': 'catalogue', 'icon': 'fa fa-gavel'},
                # attributeoptiongroup
                {'type': 'model', 'label': 'Options', 'name': 'option', 'app': 'catalogue', 'icon': 'fa fa-gavel'},  # option
                # { 'type': 'model', 'label': 'Product attribute value', 'name': 'productattributevalue', 'app': 'catalogue', 'icon': 'fa fa-gavel' }, #productattributevalue
                # { 'type': 'model', 'label': 'Product attribute', 'name': 'productattribute', 'app': 'catalogue', 'icon': 'fa fa-gavel' }, #productattribute
                # { 'type': 'model', 'label': 'Product Category', 'name': 'productcategory', 'app': 'catalogue', 'icon': 'fa fa-gavel' }, #productcategory
                {'type': 'model', 'label': 'Product Type', 'name': 'productclass', 'app': 'catalogue', 'icon': 'fa fa-gavel'},
                # productclass
                {'type': 'model', 'label': 'Tag Type', 'name': 'tagtype', 'app': 'catalogue', 'icon': 'fa fa-gavel'},  # tagtype
                {'type': 'model', 'label': 'Tag', 'name': 'tag', 'app': 'catalogue', 'icon': 'fa fa-gavel'},  # tag
                {'type': 'model', 'label': 'Product', 'name': 'product', 'app': 'catalogue', 'icon': 'fa fa-gavel'},  # products
                {'type': 'model', 'label': 'Product Image', 'name': 'productimage', 'app': 'catalogue', 'icon': 'fa fa-gavel'},
            ]},  # --> product

            # productimage

            {'type': 'free', 'label': 'Product Reviews', 'children': [
                {'type': 'model', 'label': 'Product Review', 'name': 'productreview', 'app': 'reviews', 'icon': 'fa fa-gavel'},
                # productreview
                {'type': 'model', 'label': 'Vote', 'name': 'vote', 'app': 'reviews', 'icon': 'fa fa-gavel'},  # vote

                {'type': 'free', 'label': 'Partner & Stock', 'children': [
                    {'type': 'model', 'label': 'Fulfillment Partner', 'name': 'partner', 'app': 'partner', 'icon': 'fa fa-gavel'},
                    # fulfillment partner
                    {'type': 'model', 'label': 'Stock Record', 'name': 'stockrecord', 'app': 'partner', 'icon': 'fa fa-gavel'},
                ]},  # --> Product Reviews
            ]},  # --> Product Reviews
            # stockrecord
        ]},

        # Blogs & Courses
        # { 'type': 'title', 'label': 'Blogs', 'apps': ('blogs',) },
        {'type': 'free', 'label': 'Blogs & Courses', 'children': [
            {'type': 'model', 'label': 'Categories', 'name': 'category', 'app': 'categories', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'Tags', 'name': 'tag', 'app': 'tags', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'Blogs', 'name': 'blog', 'app': 'blogs', 'icon': 'fa fa-gavel'},

            # Classes and courses
            {'type': 'free', 'label': 'Classes & Courses', 'children': [
                {'type': 'model', 'label': 'Training Categories', 'name': 'trainingcategory', 'app': 'categories', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Classes', 'name': 'classes', 'app': 'courses', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Video Played Details', 'name': 'videoplayeddetail', 'app': 'courses', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Courses', 'name': 'courses', 'app': 'courses', 'icon': 'fa fa-gavel'},
            ]},  # --> Classes and courses

        ]},

        # Ecommerce
        # { 'type': 'title', 'label': 'Ecommerce', 'apps': ('ecommerce',) },
        {'type': 'free', 'label': 'Ecommerce', 'children': [

            # cart management
            {'type': 'free', 'label': 'Cart Management', 'children': [
                {'type': 'model', 'label': 'Cart Lines', 'name': 'line', 'app': 'basket', 'icon': 'fa fa-gavel'},  # cart lines
                {'type': 'model', 'label': 'Line Attributes', 'name': 'lineattribute', 'app': 'basket', 'icon': 'fa fa-gavel'},  # cart lines
                {'type': 'model', 'label': 'Cart', 'name': 'basket', 'app': 'basket', 'icon': 'fa fa-gavel'},
            ]},  # --> cart
            # coupon management
            {'type': 'free', 'label': 'Coupons Management', 'children': [
                {'type': 'model', 'label': 'Coupons', 'name': 'voucher', 'app': 'voucher', 'icon': 'fa fa-gavel'},  # coupons
                {'type': 'model', 'label': 'Coupon Applications', 'name': 'voucherapplication', 'app': 'voucher', 'icon': 'fa fa-gavel'},
            ]},  # --> coupon
            # offer management
            {'type': 'free', 'label': 'Offer Management', 'children': [
                {'type': 'model', 'label': 'Benefits', 'name': 'benefit', 'app': 'offer', 'icon': 'fa fa-gavel'},  # benefit
                {'type': 'model', 'label': 'Conditional Offer', 'name': 'conditionaloffer', 'app': 'offer', 'icon': 'fa fa-gavel'},
                # conditional offer
                {'type': 'model', 'label': 'Condition', 'name': 'condition', 'app': 'offer', 'icon': 'fa fa-gavel'},  # condition
                {'type': 'model', 'label': 'Range', 'name': 'range', 'app': 'offer', 'icon': 'fa fa-gavel'},
            ]},  # --> offer
            # range

            # order management
            {'type': 'free', 'label': 'Order Management', 'children': [
                {'type': 'model', 'label': 'Billing Address', 'name': 'billingaddress', 'app': 'order', 'icon': 'fa fa-gavel'},  # billingaddress
                {'type': 'model', 'label': 'Line Attribute', 'name': 'lineattribute', 'app': 'order', 'icon': 'fa fa-gavel'},  # line attribute
                {'type': 'model', 'label': 'Line Price', 'name': 'lineprice', 'app': 'order', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Order', 'name': 'order', 'app': 'order', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Order Discount', 'name': 'orderdiscount', 'app': 'order', 'icon': 'fa fa-gavel'},  # orderdiscount
                {'type': 'model', 'label': 'Order Line', 'name': 'line', 'app': 'order', 'icon': 'fa fa-gavel'},  # order line
                {'type': 'model', 'label': 'Order Note', 'name': 'ordernote', 'app': 'order', 'icon': 'fa fa-gavel'},  # order note
                {'type': 'model', 'label': 'Order Status Change', 'name': 'orderstatuschange', 'app': 'order', 'icon': 'fa fa-gavel'},
            ]},  # --> order
            {'type': 'free', 'label': 'Payment Event', 'children': [
                {'type': 'model', 'label': 'Payment Event Type', 'name': 'paymenteventtype', 'app': 'order', 'icon': 'fa fa-gavel'},
                # paymenteventtype
                {'type': 'model', 'label': 'Payment Event', 'name': 'paymentevent', 'app': 'order', 'icon': 'fa fa-gavel'},  # paymentevent
                {'type': 'model', 'label': 'Shipping Event Type', 'name': 'shippingeventtype', 'app': 'order', 'icon': 'fa fa-gavel'},
            ]},

            {'type': 'free', 'label': 'Shipping Management', 'children': [
                {'type': 'model', 'label': 'Shipping Event', 'name': 'shippingevent', 'app': 'order', 'icon': 'fa fa-gavel'},  # shippingevent
                {'type': 'model', 'label': 'Shipping Address', 'name': 'shippingaddress', 'app': 'order', 'icon': 'fa fa-gavel'},  # shippingaddress
                {'type': 'model', 'label': 'Surcharge', 'name': 'surcharge', 'app': 'order', 'icon': 'fa fa-gavel'},  # surcharge
                {'type': 'model', 'label': 'Order Event', 'name': 'communicationevent', 'app': 'order', 'icon': 'fa fa-gavel'},
            ]},

            {'type': 'free', 'label': 'Payment Management', 'children': [
                {'type': 'model', 'label': 'Bankcard', 'name': 'bankcard', 'app': 'payment', 'icon': 'fa fa-gavel'},  # bankcard
                {'type': 'model', 'label': 'Source Type', 'name': 'sourcetype', 'app': 'payment', 'icon': 'fa fa-gavel'},  # sourcetype
                {'type': 'model', 'label': 'Source', 'name': 'source', 'app': 'payment', 'icon': 'fa fa-gavel'},  # source
                {'type': 'model', 'label': 'Transaction', 'name': 'transaction', 'app': 'payment', 'icon': 'fa fa-gavel'},
            ]},  # --> payment
            # transaction

            {'type': 'free', 'label': 'Shipping Management', 'children': [
                {'type': 'model', 'label': 'Order And Item Charges', 'name': 'orderanditemcharges', 'app': 'shipping', 'icon': 'fa fa-gavel'},
                # weightbased
                {'type': 'model', 'label': 'Weight Based Shipping Method', 'name': 'weightbased', 'app': 'shipping', 'icon': 'fa fa-gavel'},
            ]},  # --> shipping
            # orderanditemcharges

            # wishlistsharedemail
            {'type': 'free', 'label': 'Wish List Management', 'children': [
                {'type': 'model', 'label': 'Wish Lists', 'name': 'wishlist', 'app': 'wishlists', 'icon': 'fa fa-gavel'},  # wishlist
                {'type': 'model', 'label': 'Wish List Lines', 'name': 'line', 'app': 'wishlists', 'icon': 'fa fa-gavel'},  # line
                {'type': 'model', 'label': 'Wish List Shared emails', 'name': 'wishlistsharedemail', 'app': 'wishlists', 'icon': 'fa fa-gavel'},
            ]},  # --> wishlist
            # communication event type
            {'type': 'free', 'label': 'Communication ', 'children': [
                {'type': 'model', 'label': 'Communication Event Type', 'name': 'communicationeventtype', 'app': 'communication',
                 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Email', 'name': 'email', 'app': 'communication', 'icon': 'fa fa-gavel'},
            ]},  # --> communication  # email

        ]},

        {'type': 'free', 'label': 'Setting', 'children': [

            {'type': 'free', 'label': 'Application Setting', 'children': [
                {'type': 'model', 'label': 'Dropdown', 'name': 'dropdownclass', 'app': 'statictext', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Static Text', 'name': 'statictext', 'app': 'statictext', 'icon': 'fa fa-gavel'},

                {'type': 'model', 'label': 'Countries', 'name': 'country', 'app': 'address', 'icon': 'fa fa-gavel'},  # countries
                {'type': 'model', 'label': 'Django Dramatiq', 'name': 'task', 'app': 'django_dramatiq', 'icon': 'fa fa-gavel'},
            ]},  # --> application setting
            # django dramatiq

            {'type': 'free', 'label': 'Slide Show ', 'children': [
                {'type': 'model', 'label': 'Slideshows', 'name': 'slideshow', 'app': 'slideshow', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Display Region', 'name': 'displayregion', 'app': 'slideshow', 'icon': 'fa fa-gavel'},
            ]},
            {'type': 'free', 'label': 'Company Setting', 'children': [
                {'type': 'free', 'label': 'Company Details', 'url': '/admin/statictext/companydetails/2/change/', 'app': 'statictext',
                 'icon': 'fa fa-gavel'},
                {'type': 'free', 'label': 'Terms and conditions', 'url': '/admin/statictext/regulations/1/change/', 'app': 'statictext',
                 'icon': 'fa fa-gavel'},
                {'type': 'free', 'label': 'About Us', 'url': '/admin/statictext/regulations/3/change/', 'app': 'statictext', 'icon': 'fa fa-gavel'},
                {'type': 'free', 'label': 'Privacy Policy', 'url': '/admin/statictext/regulations/2/change/', 'app': 'statictext',
                 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'Social Media Url', 'name': 'socialmediaurl', 'app': 'statictext', 'icon': 'fa fa-gavel'},
            ]},  # --> company setting

            {'type': 'free', 'label': 'FAQ ', 'children': [
                {'type': 'model', 'label': 'FAQ', 'name': 'faq', 'app': 'statictext', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'FAQ Categories', 'name': 'faqcategory', 'app': 'statictext', 'icon': 'fa fa-gavel'},
            ]},

            {'type': 'free', 'label': 'Oscar Analytics', 'children': [
                {'type': 'model', 'label': 'Product Record', 'name': 'productrecord', 'app': 'analytics', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'User Product View', 'name': 'userproductview', 'app': 'analytics', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'User Record', 'name': 'userrecord', 'app': 'analytics', 'icon': 'fa fa-gavel'},
                {'type': 'model', 'label': 'User Search Queries', 'name': 'usersearch', 'app': 'analytics', 'icon': 'fa fa-gavel'},
            ]},  # --> oscar analytics

        ]},

        {'type': 'free', 'label': 'Communication', 'children': [
            {'type': 'model', 'label': 'Contact Log', 'name': 'contactinformation', 'app': 'accounts', 'icon': 'fa fa-gavel'},
            {'type': 'model', 'label': 'Support Request', 'name': 'supportrequest', 'app': 'accounts', 'icon': 'fa fa-gavel'},
        ]},

        {'type': 'free', 'label': 'Technical Support', 'children': [

            {'type': 'model', 'label': 'FlatPage', 'name': 'flatpage', 'app': 'flatpages', 'icon': 'fa fa-gavel'},  # flat
            {'type': 'model', 'label': 'Sites', 'name': 'site', 'app': 'sites', 'icon': 'fa fa-gavel'},  # sites

            {'type': 'free', 'label': 'User Authentication & Authorization ', 'children': [
                {'type': 'model', 'label': 'Knox', 'name': 'authtoken', 'app': 'knox', 'icon': 'fa fa-gavel'},
            ]},  # -->authentication & authorization  # Knox

            # UserSocialAuth
            {'type': 'free', 'label': 'Social Auth', 'children': [
                {'type': 'model', 'label': 'Association', 'name': 'association', 'app': 'social_django', 'icon': 'fa fa-gavel'},  # Association
                {'type': 'model', 'label': 'Nonce', 'name': 'nonce', 'app': 'social_django', 'icon': 'fa fa-gavel'},  # Nonce
                {'type': 'model', 'label': 'User Social Auth', 'name': 'usersocialauth', 'app': 'social_django', 'icon': 'fa fa-gavel'},
            ]},  # --> Social auth

        ]},

    ),

}
