from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.utils import simplejson
from django.core.urlresolvers import reverse

from grade.views import gerar_rooms, gerar_areas, gerar_zones, gerar_authors
from grade.views import gerar_talks, clean_data

from grade.models import Room, Area, Zone, Author, Talk

from django.contrib.auth.models import User
from twitterauth.models import Profile


class TestViews(TestCase):
    def setUp(self):
        data_json = open("public/json/data.json", "r").read()
        self.json = simplejson.loads(data_json)

        self.factory = RequestFactory()

        # we need an user
        user = User.objects.create_user('gradefisl',
                                'gradefisl@twitter.com',
                                'QZAx8IwvwpLOHGNDOTrIhSO3E5KyeOtb9UIrqJ9nyM')

        profile = Profile()
        profile.user = user
        profile.oauth_token = '324585531-Q1syPHxVC8X0ausLadVHDnDhzXRxx0z26lRjuHBm'
        profile.oauth_secret = 'QZAx8IwvwpLOHGNDOTrIhSO3E5KyeOtb9UIrqJ9nyM'
        profile.save()

    def test_roomset_is_empty(self):
        clean_data()

        self.assertEquals(Room.objects.count(), 0)

    def test_areaset_is_empty(self):
        clean_data()

        self.assertEquals(Area.objects.count(), 0)

    def test_zoneset_is_empty(self):
        clean_data()

        self.assertEquals(Zone.objects.count(), 0)

    def test_authorset_is_empty(self):
        clean_data()

        self.assertEquals(Author.objects.count(), 0)

    def test_talkset_is_empty(self):
        clean_data()

        self.assertEquals(Talk.objects.count(), 0)

    def test_generate_room_from_json(self):
        gerar_rooms(self.json)
        self.assertEquals(Room.objects.count(), 12)

    def test_generate_areas_from_json(self):
        gerar_areas(self.json)
        self.assertEquals(Area.objects.count(), 22)

    def test_genereta_zone_from_json(self):
        gerar_zones(self.json)
        self.assertEquals(Zone.objects.count(), 7)

    def test_generate_author_from_json(self):
        gerar_authors(self.json)
        self.assertEquals(Author.objects.count(), 511)

    def test_generate_talk_from_json(self):
        gerar_talks(self.json)
        self.assertEquals(Talk.objects.count(), 362)

    def test_choice_talk(self):
        talk_id = 10
        talk = Talk.objects.get(id=talk_id)
        user = User.objects.get(id=1)

        client = Client()
        client.login(username='gradefisl',
                     password='QZAx8IwvwpLOHGNDOTrIhSO3E5KyeOtb9UIrqJ9nyM')

        # lets choice the talk
        client.get(reverse('grade:choice_talk', args=[10]))

        self.assertEquals(talk.listeners.filter(id=user.id).count(), 1)

    def test_access_view_and_generate_talks(self):
        client = Client()
        response = client.get('/gerar_grade/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "Grade gerada com sucesso!")

    def test_access_home_and_see_all_talks(self):
        # TODO: Use splinter to test browser access

        client = Client()
        response = client.get('/')

        self.assertEquals(response.status_code, 200)
