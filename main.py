from datetime import datetime
import httpx

import openai

openai.audio

text = """Locust is an open source performance/load testing tool for HTTP and other protocols. Its developer-friendly approach lets you define your tests in regular Python code.

Locust tests can be run from command line or using its web-based UI. Throughput, response times and errors can be viewed in real time and/or exported for later analysis.

You can import regular Python libraries into your tests, and with Locust’s pluggable architecture it is infinitely expandable. Unlike when using most other tools, your test design will never be limited by a GUI or domain-specific language.

To start using Locust, go to Installation"""
with httpx.Client(timeout=60) as client:

    data = {"text": text, "type": "reading", "level": 4}
    response = client.post("http://localhost:8000/lesson/v1/generate", json=data)
    if response.status_code == 200:
        resp_data = response.json()
    else:
        resp_data = {"info": response.text}
    resp = {"status": response.status_code, "json": resp_data}
    print(resp)
    with open("test.json", "w") as f:
        import json

        json.dump(resp, f, indent=4)
from src.api.models.lesson import UploadLesson, ReadingContent, LessonType, Level

# generated_lesson = {
#     "status": 200,
#     "json": {
#         "type": "reading",
#         "level": 4,
#         "content": {
#             "text": "Locust is an open source performance/load testing tool for HTTP and other protocols. Its developer-friendly approach lets you define your tests in regular Python code.\n\nLocust tests can be run from command line or using its web-based UI. Throughput, response times and errors can be viewed in real time and/or exported for later analysis.\n\nYou can import regular Python libraries into your tests, and with Locust\u2019s pluggable architecture it is infinitely expandable. Unlike when using most other tools, your test design will never be limited by a GUI or domain-specific language.\n\nTo start using Locust, go to Installation",
#             "questions": [
#                 {
#                     "index": 0,
#                     "text": "What is Locust?",
#                     "answers": [
#                         "a tool for drawing",
#                         "a tool for creating websites",
#                         "a tool for performance testing",
#                         "a tool for editing photos",
#                     ],
#                     "correct_answer": 2,
#                 },
#                 {
#                     "index": 1,
#                     "text": "In what language can you define tests in Locust?",
#                     "answers": ["Java", "C++", "Python", "Ruby"],
#                     "correct_answer": 2,
#                 },
#                 {
#                     "index": 2,
#                     "text": "Where can Locust tests be run from?",
#                     "answers": [
#                         "Only from the command line",
#                         "Only using a web-based UI",
#                         "From the command line or using a web-based UI",
#                         "Only using a specific IDE",
#                     ],
#                     "correct_answer": 2,
#                 },
#                 {
#                     "index": 3,
#                     "text": "When can throughput, response times, and errors be viewed?",
#                     "answers": [
#                         "In real time",
#                         "After the test is finished",
#                         "Both in real time and after the test",
#                         "None of the above",
#                     ],
#                     "correct_answer": 2,
#                 },
#                 {
#                     "index": 4,
#                     "text": "What is a key feature of Locust\u2019s architecture?",
#                     "answers": [
#                         "It is limited by a GUI",
#                         "It is infinitely expandable",
#                         "It is limited by a domain-specific language",
#                         "It cannot be expanded",
#                     ],
#                     "correct_answer": 1,
#                 },
#                 {
#                     "index": 5,
#                     "text": "What should you do to start using Locust?",
#                     "answers": [
#                         "Go to Configuration",
#                         "Go to Installation",
#                         "Go to Documentation",
#                         "Go to Examples",
#                     ],
#                     "correct_answer": 1,
#                 },
#             ],
#         },
#     },
# }

# with httpx.Client(timeout=60) as client:
#     text = """Locust is an open source performance/load testing tool for HTTP and other protocols. Its developer-friendly approach lets you define your tests in regular Python code.

# Locust tests can be run from command line or using its web-based UI. Throughput, response times and errors can be viewed in real time and/or exported for later analysis.

# You can import regular Python libraries into your tests, and with Locust’s pluggable architecture it is infinitely expandable. Unlike when using most other tools, your test design will never be limited by a GUI or domain-specific language.

# To start using Locust, go to Installation"""
#     data = UploadLesson(
#         authorId=1,
#         name="test",
#         type=LessonType.reading,
#         level=Level.B2,
#         description="description",
#         content=ReadingContent.model_validate(generated_lesson["json"]["content"]),
#     )
#     response = client.post(
#         "http://localhost:8000/lesson/v1/upload", json=data.model_dump()
#     )
#     if response.status_code == 200:
#         resp_data = response.json()
#     else:
#         resp_data = {"info": response.text}
#     resp = {"status": response.status_code, "json": resp_data}
#     print(resp)
#     with open("test.json", "w") as f:
#         import json

#         json.dump(resp, f, indent=4)

# from src.api.models.exercise import GradeExercise, Question


# questions = [
#     {
#         "index": 0,
#         "question": "What is Locust?",
#         "answers": [
#             "a tool for drawing",
#             "a tool for creating websites",
#             "a tool for performance testing",
#             "a tool for editing photos",
#         ],
#         "correct_answer": 2,
#         "student_answer": 2,
#     },
#     {
#         "index": 1,
#         "question": "In what language can you define tests in Locust?",
#         "answers": ["Java", "C++", "Python", "Ruby"],
#         "correct_answer": 2,
#         "student_answer": 3,
#     },
#     {
#         "index": 2,
#         "question": "Where can Locust tests be run from?",
#         "answers": [
#             "Only from the command line",
#             "Only using a web-based UI",
#             "From the command line or using a web-based UI",
#             "Only using a specific IDE",
#         ],
#         "correct_answer": 2,
#         "student_answer": 1,
#     },
#     {
#         "index": 3,
#         "question": "When can throughput, response times, and errors be viewed?",
#         "answers": [
#             "In real time",
#             "After the test is finished",
#             "Both in real time and after the test",
#             "None of the above",
#         ],
#         "correct_answer": 2,
#         "student_answer": 1,
#     },
#     {
#         "index": 4,
#         "question": "What is a key feature of Locust\u2019s architecture?",
#         "answers": [
#             "It is limited by a GUI",
#             "It is infinitely expandable",
#             "It is limited by a domain-specific language",
#             "It cannot be expanded",
#         ],
#         "correct_answer": 1,
#         "student_answer": 1,
#     },
#     {
#         "index": 5,
#         "question": "What should you do to start using Locust?",
#         "answers": [
#             "Go to Configuration",
#             "Go to Installation",
#             "Go to Documentation",
#             "Go to Examples",
#         ],
#         "correct_answer": 1,
#         "student_answer": 2,
#     },
# ]

# with httpx.Client(timeout=60) as client:
#     data = GradeExercise(
#         lesson_id=1,
#         user_id=1,
#         transcript=text,
#         level=Level.B2,
#         lesson_type=LessonType.reading,
#         questions=[Question.model_validate(q) for q in questions],
#     )
#     response = client.post(
#         "http://localhost:8000/exercise/v1/grade", json=data.model_dump()
#     )
#     if response.status_code == 200:
#         resp_data = response.json()
#     else:
#         resp_data = {"info": response.text}
#     resp = {"status": response.status_code, "json": resp_data}
#     print(resp)
#     with open("test.json", "w") as f:
#         import json

#         json.dump(resp, f, indent=4)
