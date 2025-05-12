from dataclasses import dataclass, field
from collections.abc import Callable, Awaitable, Sequence


from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from .conversation_storage import ConversationStorage
from .promts import SYSTEM_PROMPT
from .models import Context


@dataclass
class Assistant:
    storage: ConversationStorage
    context: Context
    model: Model
    system_prompt_runners: Sequence[
        Callable[[RunContext[Context]], Awaitable[str]] | Callable[[], Awaitable[str]]
    ] = field(default_factory=list)

    @property
    def agent(self):
        agent = Agent(
            self.model,
            deps_type=Context,
            system_prompt=SYSTEM_PROMPT,
            output_type=str,
        )

        for runner in self.system_prompt_runners:
            agent.system_prompt(runner)

        return agent

    async def chat(self, user_prompt: str):
        session_id = self.context.session_id
        resp = await self.agent.run(
            user_prompt,
            message_history=await self.storage.get_messages(session_id),
            deps=self.context,
        )

        await self.storage.add_message(session_id, resp.new_messages())
        return resp.output

    async def chat_stream(self, user_prompt: str):
        session_id = self.context.session_id
        async with self.agent.run_stream(
            user_prompt,
            message_history=await self.storage.get_messages(session_id),
            deps=self.context,
        ) as stream:
            async for token in stream.stream_text(delta=True):
                yield token

            await self.storage.add_message(session_id, stream.new_messages())
