from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from subscription import GPTSubscription, MJSubscription


class SubscriptionManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.scheduler = BackgroundScheduler()

    def start(self):
        # Задача проверки подписок будет запускаться каждый день в полночь
        self.scheduler.add_job(self.check_all_subscriptions, 'cron', hour=0, minute=0)
        self.scheduler.start()

    def check_all_subscriptions(self):
        users = self.db_manager.get_all_users()
        for user in users:
            self.check_and_update_subscription(user['user_id'])

    def check_and_update_subscription(self, user_id):
        user = self.db_manager.get_user(user_id)
        if not user:
            return

        current_date = datetime.now()
        self.update_gpt_daily_limits(user, current_date)
        self.update_mj_daily_limits(user, current_date)
        self.update_gpt_subscription(user, current_date)
        self.update_mj_subscription(user, current_date)

    def update_gpt_daily_limits(self, user, current_date):
        # Проверка и обновление дневных лимитов для GPT
        if user['gpt_subscription_type']:
            gpt_sub_end_date = datetime.strptime(user['gpt_sub_end_date'], "%Y-%m-%d %H:%M:%S")
            if gpt_sub_end_date > current_date:
                last_update_date = datetime.strptime(user['gpt_daily_update_date'], "%Y-%m-%d %H:%M:%S").date()
                if last_update_date < current_date.date():
                    limits = GPTSubscription.SUBSCRIPTION_TYPES[user['gpt_subscription_type']]
                    self.db_manager.update_user(user['user_id'], gpt3_tokens=0, gpt4_limit=limits['limit_gpt4'], gpt35_limit=limits['limit_gpt35'], gpt_daily_update_date=current_date.strftime("%Y-%m-%d %H:%M:%S"))

    def update_mj_daily_limits(self, user, current_date):
        # Проверка и обновление дневных лимитов для Midjourney
        if user['mj_subscription_type']:
            mj_sub_end_date = datetime.strptime(user['mj_sub_end_date'], "%Y-%m-%d %H:%M:%S")
            if mj_sub_end_date > current_date:
                last_update_date = datetime.strptime(user['mj_daily_update_date'], "%Y-%m-%d %H:%M:%S").date()
                if last_update_date < current_date.date():
                    limit = MJSubscription.SUBSCRIPTION_TYPES[user['mj_subscription_type']]['limit']
                    self.db_manager.update_user(user['user_id'], mj52_limit=limit, mj6_limit=limit, mj_daily_update_date=current_date.strftime("%Y-%m-%d %H:%M:%S"))

    def update_gpt_subscription(self, user, current_date):
        # Проверка и обновление подписки GPT
        gpt_sub_end_date = datetime.strptime(user['gpt_sub_end_date'], "%Y-%m-%d %H:%M:%S") if user[
            'gpt_sub_end_date'] else None
        if gpt_sub_end_date and gpt_sub_end_date <= current_date:
            # Если подписка GPT истекла, обновляем информацию о подписке на None
            self.db_manager.update_user(user['user_id'], gpt_subscription_type=None, gpt_sub_end_date=None,
                                        gpt4_limit=0, gpt35_limit=0)

    def update_mj_subscription(self, user, current_date):
        # Проверка и обновление подписки Midjourney
        mj_sub_end_date = datetime.strptime(user['mj_sub_end_date'], "%Y-%m-%d %H:%M:%S") if user[
            'mj_sub_end_date'] else None
        if mj_sub_end_date and mj_sub_end_date <= current_date:
            # Если подписка Midjourney истекла, обновляем информацию о подписке на None
            self.db_manager.update_user(user['user_id'], mj_subscription_type=None, mj_sub_end_date=None, mj52_limit=0,
                                        mj6_limit=0)

    def stop(self):
        self.scheduler.shutdown()
