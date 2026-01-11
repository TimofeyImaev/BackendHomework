# Пример использования contextvars
import contextvars
import asyncio

user_id = contextvars.ContextVar('user_id')

async def handle_request():
    user_id.set(42)  # Устанавливаем контекст
    # Теперь все колбэки в этом контексте будут видеть user_id=42

asyncio.run(handle_request())