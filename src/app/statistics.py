from typing import Annotated

from infra.data.crud import DataBackend


async def get_stat(user_id: int, data_backend: DataBackend):
    lessons = await data_backend.get_lessons()
    created = []
    for lesson in lessons:
        if lesson.authorId == user_id:
            created.append(lesson)

    results = await data_backend.get_results_by_user_id(user_id)
