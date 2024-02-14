# subscription_manager.py
import data.creator as db

db_manager = db.DBManager()


def update_gpt_limits(user_id, gpt_model, tokens_used=0):
    """
    Обновляет лимиты GPT для пользователя в зависимости от используемой модели.

    :param user_id: ID пользователя
    :param gpt_model: Модель GPT, которая использовалась (например, 'gpt-3.5-turbo' или 'gpt-4')
    :param tokens_used: Количество использованных токенов
    """
    user = db_manager.get_user(user_id)
    if user['gpt_subscription_type'] is None:
        # Если у пользователя нет подписки, обновляем общее количество токенов GPT
        new_tokens = user['gpt3_tokens'] - tokens_used
        db_manager.update_user(user_id, gpt3_tokens=new_tokens)
    elif gpt_model == 'gpt-3.5-turbo':
        new_limit = user['gpt35_limit'] - 1
        db_manager.update_user(user_id, gpt35_limit=new_limit)
    elif gpt_model == 'gpt-4':
        new_limit = user['gpt4_limit'] - 1
        db_manager.update_user(user_id, gpt4_limit=new_limit)
    elif gpt_model == 'midjourney5.2':
        new_limit = user['mj52_limit'] - 1
        db_manager.update_user(user_id, mj52_limit=new_limit)
    print(f"Лимиты для пользователя {user_id} и модели {gpt_model} обновлены.")
