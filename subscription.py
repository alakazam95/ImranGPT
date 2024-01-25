import datetime
from datetime import datetime, timedelta
import data.creator as db

db_creator = db.dbCreator()


def check_subscription_status(user_id):
    return db_creator.get_subscription_type(user_id)


def activate_subscription(user_id):
    sub_type = db_creator.get_subscription_type(user_id)
    """Активирует бесплатную подписку для пользователя."""
    if sub_type == 'paid':
        new_limit_update_date = datetime.now() + timedelta(days=30)  # Дата обновления через месяц
        db_creator.set_user_limit(user_id, -1)
        db_creator.renew_daily_limits(user_id)
        db_creator.set_daily_limit_update_date(user_id, (datetime.now() + timedelta(days=1)))
    else:
        new_limit_update_date = datetime.now() + timedelta(days=7)  # Дата обновления через неделю
        db_creator.set_user_limit(user_id, 50000)

    db_creator.set_subscription_type(user_id, sub_type)
    db_creator.set_limit_update_date(user_id, (new_limit_update_date.strftime('%Y-%m-%d %H:%M:%S')))
