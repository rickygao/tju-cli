from io import BytesIO
from enum import Enum, auto, unique

import requests
from bs4 import BeautifulSoup


@unique
class Time(Enum):
    EightToNine = '00001'
    NineToTen = '00002'
    TenToEleven = '00003'
    ElevenToTwelve = '00004'
    TwelveToThirteen = '00005'
    ThirteenToFourteen = '00006'
    FourteenToFifteen = '000007'
    FifteenToSixteen = '00008'
    SixteenToSeventeen = '00009'
    SeventeenToEighteen = '00010'
    EighteenToNinteen = '00011'
    NinteenToTwenty = '00012'
    TwentyToTwentyOne = '00013'


@unique
class Category(Enum):
    Badminton = '01'
    Ppball = '02'
    Billiard = '03'
    Open = '04'
    Football = '05'
    Baseketball = '06'
    Tennis = '07'
    Classroom = '08'
    Auditorium = '09'
    Volleyball = '10'


@unique
class Campus(Enum):
    WeiJinLu = '01'
    PeiYangYuan = '02'


@unique
class Place(Enum):
    PeiYangYuanBadminton1 = '2201'
    PeiYangYuanBadminton2 = '2202'
    PeiYangYuanBadminton3 = '2203'
    PeiYangYuanBadminton4 = '2204'
    PeiYangYuanBadminton5 = '2205'
    PeiYangYuanBadminton6 = '2206'
    PeiYangYuanBadminton7 = '2207'
    PeiYangYuanBadminton8 = '2208'
    PeiYangYuanBadminton9 = '2209'
    PeiYangYuanBadminton10 = '2210'
    PeiYangYuanBadminton11 = '2211'
    PeiYangYuanBadminton12 = '2212'


@unique
class BookResult(Enum):
    Success = auto()
    Invalid = auto()
    Failure = auto()

    @property
    def ok(self):
        return self is BookResult.Success


class BookClient:
    def __init__(self):
        self._session = requests.Session()

    def authenticate(self, username, password):
        with self._session.post(
            url='http://cgzx.tju.edu.cn:8080/index.php/Book/Login/authCheck.html',
            data={'name': username, 'pwd': password},
        ) as response:
            status = response.text
        return status == 'SUCCESS'

    def book(self, date, time: Time, category: Category, campus: Campus, place: Place):
        with self._session.get(
            url='http://cgzx.tju.edu.cn:8080/index.php/Book/Book/index4.html',
            params={
                'day': date.isoformat(),
                'time': time.value,
                'cg': category.value,
                'cp': campus.value,
                'cdinfoid': place.value,
            }
        ) as response:
            bs = BeautifulSoup(response.text, 'html.parser')
            form = bs.select_one('form[name="myForm"]')

            if form is None:
                return BookResult.Invalid

            inputs = form.select('input')
            data = {
                element['name']: element['value']
                for element in inputs
                if element.has_attr('name')
            }

        with self._session.post(
            url='http://cgzx.tju.edu.cn:8080/index.php/Book/Book/order.html',
            data=data
        ) as response:
            bs = BeautifulSoup(response.text, 'html.parser')
            msg = bs.select_one('.f18')
            if msg is None or msg.text != '成功':
                return BookResult.Failure

        return BookResult.Success

    @property
    def authenticated(self):
        with self._session.get(
            url='http://cgzx.tju.edu.cn:8080/index.php/Book/Book/index.html',
            allow_redirects=False,
        ) as response:
            is_redirect = response.is_redirect
        return not is_redirect

    @property
    def session(self):
        return self._session
