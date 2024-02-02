from datetime import datetime, timedelta


class Subscription:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def activate(self, user_id):
        raise NotImplementedError("This method should be implemented by subclasses.")


class GPTSubscription(Subscription):
    SUBSCRIPTION_TYPES = {
        'Старт': {'limit_gpt4': 20, 'limit_gpt35': 50, 'price': 490},
        'Стандарт': {'limit_gpt4': 50, 'limit_gpt35': 100, 'price': 990},
        'Премиум': {'limit_gpt4': 150, 'limit_gpt35': 150, 'price': 2990}
    }

    def __init__(self, db_manager, subscription_type):
        super().__init__(db_manager)
        self.subscription_type = subscription_type
        self.limits = self.SUBSCRIPTION_TYPES[subscription_type]

    def activate(self, user_id):
        new_sub_date = datetime.now()
        new_sub_end_date = new_sub_date + timedelta(days=30)  # Подписка длится 30 дней

        # Активируем новую подписку
        self.db_manager.update_user(user_id,
                                    gpt_subscription_type=self.subscription_type,
                                    gpt_sub_update_date=new_sub_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    gpt_sub_end_date=new_sub_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    gpt4_limit=self.limits['limit_gpt4'],
                                    gpt35_limit=self.limits['limit_gpt35'],
                                    gpt3_tokens=0)  # Сброс токенов при активации новой подписки


class MJSubscription(Subscription):
    SUBSCRIPTION_TYPES = {
        'Старт': {'limit': 10, 'price': 290},
        'Стандарт': {'limit': 25, 'price': 590},
        'Премиум': {'limit': 50, 'price': 990}
    }

    def __init__(self, db_manager, subscription_type):
        super().__init__(db_manager)
        self.subscription_type = subscription_type
        self.limits = self.SUBSCRIPTION_TYPES[subscription_type]

    def activate(self, user_id):
        new_sub_date = datetime.now()
        new_sub_end_date = new_sub_date + timedelta(days=30)  # Подписка длится 30 дней

        # Активируем новую подписку
        self.db_manager.update_user(user_id,
                                    mj_subscription_type=self.subscription_type,
                                    mj_sub_update_date=new_sub_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    mj_sub_end_date=new_sub_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    mj52_limit=self.limits['limit'],
                                    mj6_limit=self.limits['limit'])  # Если лимиты одинаковы для обеих версий MJ
