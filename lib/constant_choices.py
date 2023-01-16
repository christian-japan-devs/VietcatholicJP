from django.utils.translation import gettext_lazy as _
from lib.constants import (REGISTRED,NOT_PAIED,NOT_CONFIRM,ABSENT,PRESENTED,
    MEMBER,LEADER,VICE_LEADER,PLUS,MINUS,INCOME,OUTCOME,NOT_YET
    ,DOING,FINISHED,DELAY,CANCEL)

# Booking status
status_choice = (
    ('W', 'Waiting'),
    ('A', 'Approved'),
    ('D', 'Denied'),
    ('P', 'Presented'),
    ('AB', 'Absented'),
    ('C', 'Cancel')
)

group_type_choice = (
    ('commu','Cộng đoàn'),
    ('group','Nhóm giới trẻ'),
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

aboutus_types = (
    ('vcj','Giao-doan'),
    ('vcj','Cha tuyen uy')
)
year_choice = (
    ('A', _('Năm A')),
    ('B', _('Năm B')),
    ('C', _('Năm C')),
)

priority_choice = (
    ('3', 'Cao'),
    ('2', 'Trung bình'),
    ('1', 'Thấp')
)

task_statuses = (
    (NOT_YET, 'Chưa làm'),
    (DOING, 'Đang làm'),
    (FINISHED, 'Hoàn thành'),
    (DELAY, 'Dời lịch'),
    (CANCEL, 'Huỷ')
)

event_status_choice = (
    (REGISTRED,'Đã đăng ký'),
    (NOT_PAIED,'Chưa thanh toán'),
    (NOT_CONFIRM,'Chưa xác nhận'),
    (ABSENT,'Vắng mặt'),
    (PRESENTED,'Đã tham dự'),
)


membership_type = (
    (LEADER,'Nhóm trưởng'),
    (VICE_LEADER,'Nhóm phó'),
    (MEMBER,'Thành viên'),
)

score_type = (
    (PLUS,'Cộng'),
    (MINUS,'Trừ')
)

trasaction_type = (
    (INCOME,'Thu'),
    (OUTCOME,'Chi')
)

sequence_choise = (
    ('0', '1'),
    ('1', '2'),
    ('2', '3'),
    ('3', '4'),
    ('4', '5'),
    ('5', '6'),
    ('6', '7'),
    ('7', '8'),
    ('8', '9'),
    ('9', '10'),
    ('10', '11'),
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
