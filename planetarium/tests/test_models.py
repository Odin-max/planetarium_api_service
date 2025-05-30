import pytest
from django.core.exceptions import ValidationError
from planetarium.models import Ticket, PlanetariumDome, ShowSession, Reservation, AstronomyShow
from django.contrib.auth import get_user_model
from django.utils.timezone import now


@pytest.mark.django_db
class TestTicketValidation:

    @pytest.fixture
    def dome(self):
        return PlanetariumDome.objects.create(name="Dome A", rows=10, seats_in_row=15)

    @pytest.fixture
    def show_session(self, dome):
        show = AstronomyShow.objects.create(title="Black Holes", description="Deep space science")
        return ShowSession.objects.create(
            astronomy_show=show,
            planetarium_dome=dome,
            show_time=now()
        )

    @pytest.fixture
    def reservation(self):
        user = get_user_model().objects.create_user(email="test@example.com", password="12345")
        return Reservation.objects.create(user=user)

    def test_valid_ticket_passes_validation(self, show_session):
        try:
            Ticket.validate_ticket(5, 10, show_session.planetarium_dome, ValidationError)
        except ValidationError:
            pytest.fail("ValidationError was raised on valid input")

    def test_invalid_row_raises_error(self, show_session):
        with pytest.raises(ValidationError) as exc:
            Ticket.validate_ticket(0, 10, show_session.planetarium_dome, ValidationError)

        assert "row" in exc.value.message_dict
        assert "between 1 and" in str(exc.value)

    def test_invalid_seat_raises_error(self, show_session):
        with pytest.raises(ValidationError) as exc:
            Ticket.validate_ticket(3, 20, show_session.planetarium_dome, ValidationError)

        assert "seat" in exc.value.message_dict
        assert "between 1 and" in str(exc.value)

    def test_clean_method_raises_on_invalid_data(self, show_session, reservation):
        ticket = Ticket(
            row=11,
            seat=5,
            show_session=show_session,
            reservation=reservation
        )

        with pytest.raises(ValidationError) as exc:
            ticket.clean()

        assert "row" in exc.value.message_dict

    def test_clean_method_valid_ticket(self, show_session, reservation):
        ticket = Ticket(
            row=4,
            seat=12,
            show_session=show_session,
            reservation=reservation
        )

        ticket.clean()
