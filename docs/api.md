# Проект API (Урок 6)

| Метод | Путь | Кто | Что делает | Story | Таблица |
|---|---|---|---|---|---|
| GET | /api/subjects | student, teacher | Получить список предметов | US-1 | subjects |
| POST | /api/quizzes | teacher | Создать новый тест (quiz) | US-1 | quizzes |
| GET | /api/quizzes | student, teacher | Список доступных тестов (quizzes) | US-1 | quizzes |
| GET | /api/quizzes/{id} | student, teacher | Просмотр деталей теста | US-1 | quizzes |
| PATCH | /api/quizzes/{id} | teacher | Редактировать тест / изменить статус публикации | US-1 | quizzes |
| DELETE | /api/quizzes/{id} | teacher | Удалить тест | US-1 | quizzes |
| POST | /api/quizzes/{id}/questions | teacher | Добавить вопрос с вариантами ответов | US-2 | questions, question_options |
| POST | /api/quizzes/{id}/questions/generate | teacher | Сгенерировать вопросы и варианты с помощью AI (Ollama) | US-2 | questions, question_options |
| GET | /api/quizzes/{id}/questions | teacher | Просмотр вопросов теста преподавателем | US-2 | questions, question_options |
| POST | /api/quizzes/{id}/attempts | student | Пройти тест / отправить ответы на вопросы | US-3 | attempts, attempt_answers |
| GET | /api/attempts/{id} | student (автор), teacher | Просмотр результатов попытки и оценки | US-3 | attempts, attempt_answers |
| GET | /api/attempts?my=true | student | История своих попыток сдачи тестов | US-3 | attempts |

> **Чек-лист согласованности:**
> - [x] Для каждой Must story есть все необходимые эндпоинты (US-1, US-2, US-3).
> - [x] Интеграция с архитектурой: добавлен эндпоинт обращения к AI (`/generate` через Ollama).
> - [x] Все пути начинаются с `/api/` и согласованы по REST (ресурс во множественном числе).
> - [x] Все таблицы соответствуют `er-diagram.md` (`subjects`, `quizzes`, `questions`, `question_options`, `attempts`, `attempt_answers`).
> - [x] Права доступа строго разграничены: вопросы до сдачи видит только `teacher`, студент видит только свои результаты (`автор`).

---

## Коды ответов

| Код | Название | Значение | Когда возвращается |
|---|---|---|---|
| **200** | OK | Успешно | Данные успешно получены по GET-запросу или обновлены через PATCH |
| **201** | Created | Создано | Успешно создан новый ресурс (тест, вопрос, сгенерированные AI вопросы, попытка) через POST |
| **204** | No Content | Нет содержимого | Ресурс успешно удалён через DELETE |
| **400** | Bad Request | Неверный запрос | Несоответствие количества ответов или неверный формат данных |
| **401** | Unauthorized | Не авторизован | Пользователь не вошёл в систему (токен Keycloak отсутствует или недействителен) |
| **403** | Forbidden | Доступ запрещён | Студент пытается создать/удалить тест или просмотреть чужой результат |
| **404** | Not Found | Не найдено | Тест, вопрос или результат с указанным ID не найден |
| **422** | Unprocessable Entity | Ошибка валидации | Данные не прошли валидацию Pydantic (слишком короткий заголовок, отрицательный балл и т.д.) |
| **500** | Internal Server Error | Ошибка сервера | Непредвиденная внутренняя ошибка базы данных, сервера или сбой сервиса Ollama |
