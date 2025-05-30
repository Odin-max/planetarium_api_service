from django.db import models
from user.models import User
from django.core.exceptions import ValidationError


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    show_themes = models.ManyToManyField(
        ShowTheme,
        blank=True,
        related_name="astronomy_shows"
    )

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveSmallIntegerField()
    seats_in_row = models.PositiveSmallIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show} in {self.planetarium_dome} at {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"Reservation #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    def __str__(self):
        return (
            f"{str(self.show_session)} (row: {self.row}, seat: {self.seat})"
        )

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for value, name, limit in [
            (row, "row", planetarium_dome.rows),
            (seat, "seat", planetarium_dome.seats_in_row),
        ]:
            if not (1 <= value <= limit):
                raise error_to_raise({
                    name: f"{name.capitalize()} must be between 1 and {limit}"
                })

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]
