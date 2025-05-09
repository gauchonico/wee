from django.db import migrations, models
import django.db.models.deletion

def create_users_for_agents(apps, schema_editor):
    Agent = apps.get_model('agents', 'Agent')
    User = apps.get_model('auth', 'User')
    for agent in Agent.objects.filter(user__isnull=True):
        # Create a username from the agent's name
        username = f"agent_{agent.id}"
        # Create a temporary email
        email = f"{username}@example.com"
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password='agent12345',  # Default password
            first_name=agent.first_name,
            last_name=agent.last_name
        )
        # Link the user to the agent
        agent.user = user
        agent.save()

class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0007_alter_incentive_options_remove_incentive_agent'),
    ]

    operations = [
        migrations.RunPython(create_users_for_agents),
        migrations.AddField(
            model_name='agent',
            name='is_credit_manager',
            field=models.BooleanField(default=False, help_text='Indicates if this agent can also act as a credit manager'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ] 