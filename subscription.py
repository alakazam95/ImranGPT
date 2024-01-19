import datetime
from datetime import datetime, timedelta
import data.creator as db

db_creator = db.dbCreator()


def activate_subscription(user_id, type='free'):
    """Активирует бесплатную подписку для пользователя."""
    if type == 'paid':
        new_limit_update_date = datetime.now() + timedelta(days=30)  # Дата обновления через месяц
        db_creator.set_user_limit(user_id, -1)
    else:
        new_limit_update_date = datetime.now() + timedelta(days=7)  # Дата обновления через неделю
        db_creator.set_user_limit(user_id, 50000)
    db_creator.set_subscription_type(user_id, type)
    db_creator.set_limit_update_date(user_id, (new_limit_update_date.strftime('%Y-%m-%d %H:%M:%S')))
