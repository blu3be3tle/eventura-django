from events.models import Event
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Eventura Account'
        message = (
            f"Hi {instance.username},\n\n"
            f"Please activate your account by clicking the link below:\n"
            f"{activation_url}\n\n"
            "Thank You!"
        )

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, [instance.email])
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        participant_group, created = Group.objects.get_or_create(
            name='Participant')

        instance.group.add(participant_group)


@receiver(m2m_changed, sender=Event.users.through)
def rsvp_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_pk in pk_set:
            user = User.objects.get(pk=user_pk)
            event = instance

            subject = f'RSVP Confirmation for: {event.name}'
            message = (
                f"Hi {user.username},\n\n"
                f"This is a confirmation that you have successfully RSVP'd for the event:\n\n"
                f"Event: {event.name}\n"
                f"Date: {event.date}\n"
                f"Time: {event.time}\n"
                f"Location: {event.location}\n\n"
                "We look forward to seeing you there!\n\n"
                "Thanks,\nThe Eventura Team"
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
