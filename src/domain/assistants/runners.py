from pydantic_ai import RunContext

from .models import Context


async def bind_user_name(ctx: RunContext[Context]) -> str:
    return f"The user name is {ctx}."


async def bind_native_language(ctx: RunContext[Context]) -> str:
    return f"The native language is {ctx}."
