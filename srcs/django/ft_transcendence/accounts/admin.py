from django.contrib import admin
from .models import Profile, FriendList, FriendRequest
from stats.models import UserStats

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'isstudent', 'creation_date', 'active']
    search_fields = ['user__username']
    readonly_fields = ['display_user_stats']

    def display_user_stats(self, obj):
        user_stats = UserStats.objects.filter(user=obj.user).first()
        if user_stats:
            return f"""
                Total Games: {user_stats.total_games}
                Wins: {user_stats.wins}
                Losses: {user_stats.losses}
                Goals Scored: {user_stats.goals_scored}
                Goals Conceded: {user_stats.goals_conceded}
                Time Played: {user_stats.time_played}
                Number of Defense: {user_stats.nb_defense}
            """
        return "No user stats available."

    display_user_stats.short_description = 'User Stats'
    display_user_stats.allow_tags = True

admin.site.register(Profile, ProfileAdmin)

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender', 'receiver']
    search_fields = ['sender__username', 'sender_email', 'receiver_email', 'receiver_username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)