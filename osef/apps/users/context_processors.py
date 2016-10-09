from .models import Notification

def notifications(request):
  if request.user.is_authenticated():
    notifications = Notification.objects.filter(sender = request.user, viewed = False)
    dic = {
      "notifications": notifications, 
      "has_notifications": notifications.exists(),
      "number_of_notifications": notifications.count()
    }
    return dic
  else:
    return {"notifications": [], "has_notifications": 0}