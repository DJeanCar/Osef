from .models import Notification

def notifications(request):
  if request.user.is_authenticated():
    notifications = Notification.objects.filter(sender = request.user, viewed = False).order_by('-created_at')[:15]
    notificationsViewed = Notification.objects.filter(sender = request.user, viewed = True).order_by('-created_at')[:15]
    dic = {
      "notifications": notifications, 
      "notificationsViewed": notificationsViewed,
      "has_notifications": notifications.exists(),
      "number_of_notifications": notifications.count()
    }
    return dic
  else:
    return {"notifications": [], "has_notifications": 0}