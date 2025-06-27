from django.core.cache import cache

def save_confirmation_code(email, code, timeout=300):
    """Сохраняет код подтверждения в Redis на 5 минут"""
    cache_key = f"confirm_code:{email}"
    cache.set(cache_key, code, timeout=timeout)

def get_confirmation_code(email):
    """Получает код из Redis"""
    return cache.get(f"confirm_code:{email}")

def delete_confirmation_code(email):
    """Удаляет код из Redis"""
    cache.delete(f"confirm_code:{email}")