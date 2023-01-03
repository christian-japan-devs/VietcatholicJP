from django.utils.translation import gettext_lazy as _
# Booking status
status_choice = (
    ('W', 'Waiting'),
    ('A', 'Approved'),
    ('D', 'Denied'),
    ('P', 'Presented'),
    ('AB', 'Absented'),
    ('C', 'Cancel')
)

cf_status_choice = (
    ('CF', 'CONFIRMED'),
    ('NF', 'NOTCONFIRM')
)
# language

language_choice = (
    ('ja', _('日本語')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('vi', _('Tiếng Việt'))
)


week_day_choice = (
    ('0', _('Thứ hai')),
    ('1', _('Thứ ba')),
    ('2', _('Thứ tư')),
    ('3', _('Thứ năm')),
    ('4', _('Thứ sáu')),
    ('5', _('Thứ bảy')),
    ('6', _('Chúa Nhật')),
)

jp_region_choices = (
    ('hokkaido', 'Hokkaido'),
    ('tohoku', 'Tohoku'),
    ('kanto', 'Kanto'),
    ('chubu', 'Chubu'),
    ('kansai', 'Kansai'),
    ('chugoku', 'Chugoku'),
    ('shikoku', 'Shikoku'),
    ('kyushu', 'Kyushu')
)

jp_province_choices = (
    ('hokkaido', 'Hokkaido'),
    ('akita', 'Akita'),
    ('aomori', 'Aomori'),
    ('fukushima', 'Iwate'),
    ('miyagi', 'Miyagi'),
    ('yamagata', 'yamagata'),
    ('chiba', 'Chiba'),
    ('gunma', 'Gunma'),
    ('ibaraki', 'Ibaraki'),
    ('kanagawa', 'Kanagawa'),
    ('saitama', 'Saitama'),
    ('tochigi', 'Tochigi'),
    ('tokyo', 'Tokyo'),
    ('aichi', 'Aichi'),
    ('fukui', 'Fukui'),
    ('gifu', 'Gifu'),
    ('ishikawa', 'Ishikawa'),
    ('nagano', 'Nagano'),
    ('niigata', 'Niigata'),
    ('shizuoka', 'Shizuoka'),
    ('toyama', 'Toyama'),
    ('yamanashi', 'Yamanashi'),
    ('hyogo', 'Hyogo'),
    ('kyoto', 'Kyoto'),
    ('mie', 'Mie'),
    ('nara', 'Nara'),
    ('osaka', 'Osaka'),
    ('shiga', 'Shiga'),
    ('wakayama', 'Wakayama'),
    ('hiroshima', 'Hiroshima'),
    ('okayama', 'Okayama'),
    ('shimane', 'Shimane'),
    ('tottori', 'Tottori'),
    ('yamaguchi', 'Yamaguchi'),
    ('ehime', 'Ehime'),
    ('kagawa', 'Kagawa'),
    ('kochi', 'Kochi'),
    ('tokushima', 'Tokushima'),
    ('fukuoka', 'Fukuoka'),
    ('kagoshima', 'Kagoshima'),
    ('kumamoto', 'Kumamoto'),
    ('miyazaki', 'Miyazaki'),
    ('nagasaki', 'Nagasaki'),
    ('oita', 'Oita'),
    ('okinawa', 'Okinawa'),
    ('saga', 'Saga')
)
