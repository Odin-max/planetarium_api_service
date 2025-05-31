import tempfile
from datetime import datetime, timedelta

from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Ticket,
    Reservation
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    TicketSerializer,
    ReservationSerializer,
)

User = get_user_model()


def create_user(email="test@example.com", password="testpass123"):
    return User.objects.create_user(email=email, password=password)


class SerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.theme = ShowTheme.objects.create(name="Stars")
        self.show = AstronomyShow.objects.create(title="Galaxy", description="Space")
        self.show.show_themes.add(self.theme)

        self.dome = PlanetariumDome.objects.create(
            name="Main Dome", rows=10, seats_in_row=10
        )

        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=datetime.now() + timedelta(days=1)
        )

        self.reservation = Reservation.objects.create(user=self.user)

        self.ticket = Ticket.objects.create(
            row=1,
            seat=2,
            show_session=self.session,
            reservation=self.reservation
        )

    def test_show_theme_serializer(self):
        serializer = ShowThemeSerializer(self.theme)
        self.assertEqual(serializer.data["name"], "Stars")

    def test_astronomy_show_serializer(self):
        serializer = AstronomyShowSerializer(self.show)
        self.assertEqual(serializer.data["title"], "Galaxy")
        self.assertIn(self.theme.id, serializer.data["show_themes"])

    def test_planetarium_dome_serializer(self):
        serializer = PlanetariumDomeSerializer(self.dome)
        self.assertEqual(serializer.data["capacity"], 100)

    def test_show_session_serializer(self):
        serializer = ShowSessionSerializer(self.session)
        self.assertEqual(serializer.data["astronomy_show"], self.show.id)

    def test_ticket_serializer_validation(self):
        data = {
            "row": 2,
            "seat": 2,
            "show_session": self.session.id,
            "reservation": self.reservation.id
        }
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_reservation_create_with_tickets(self):
        data = {
            "user": self.user.id,
            "tickets": [
                {
                    "row": 3,
                    "seat": 3,
                    "show_session": self.session.id
                }
            ]
        }
        serializer = ReservationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
