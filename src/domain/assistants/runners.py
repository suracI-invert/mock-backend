from pydantic_ai import RunContext

from .models import Context


async def bind_context(ctx: RunContext[Context]) -> str:
    return f"""The user name is {ctx.deps.user_name}.
    The native language is {ctx.deps.lang}."""
