# AI Study Assistant — Карта слоёв бэкенда

## Описание проекта

AI Study Assistant помогает студентам изучать дисциплины,
проходить тесты (квизы) и отслеживать свой прогресс в обучении.

## Роли пользователей

- Преподаватель (Teacher) — создаёт тесты.
- Студент (Student) — проходит тесты и просматривает результаты.

## Карта слоёв (Layer map)

| Слой (Layer) | Преподаватель создаёт тест | Студент проходит тест |
|---|---|---|
| Router | POST /api/quizzes · Teacher | POST /api/quizzes/{id}/attempts · Student |
| Schema | QuizCreate → QuizRead | AttemptCreate → AttemptRead |
| Service | Проверка названия и прав преподавателя | Проверка публикации, валидация ответов, подсчёт баллов |
| Repository | QuizRepository.create | AttemptRepository.create |
| Model | quizzes, questions | attempts, questions |
| Error → HTTP | Короткое название → 422; Студент создаёт тест → 403 | Тест не найден → 404; Неверное количество ответов → 400 |

## Архитектурные правила

- Router не должен содержать SQL-запросов.
- Schema валидирует входные и выходные данные.
- Service содержит всю бизнес-логику.
- Repository отвечает за операции с базой данных.
- Model описывает таблицы базы данных.
- Секретные ключи хранятся только в .env.
