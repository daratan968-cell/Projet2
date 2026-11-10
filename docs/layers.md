
# AI Study Assistant — Backend Layer Map

## Project description

AI Study Assistant helps students study subjects,
take quizzes and track their learning progress.

## User roles

- Teacher — creates quizzes.
- Student — takes quizzes and views results.

## Layer map

| Layer | Teacher creates quiz | Student takes quiz |
|---|---|---|
| Router | POST /api/quizzes · Teacher | POST /api/quizzes/{id}/attempts · Student |
| Schema | QuizCreate → QuizRead | AttemptCreate → AttemptRead |
| Service | Check title and teacher permissions | Check publication, validate answers, calculate score |
| Repository | QuizRepository.create | AttemptRepository.create |
| Model | quizzes, questions | attempts, questions |
| Error → HTTP | Short title → 422; Student creates quiz → 403 | Quiz not found → 404; Wrong answer count → 400 |

## Architecture rules

- Router must not contain SQL.
- Schema validates input and output.
- Service contains business logic.
- Repository handles database operations.
- Model describes database tables.
- Secrets are stored only in .env.
