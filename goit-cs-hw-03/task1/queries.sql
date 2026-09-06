-- 1. Завдання користувача з id = 1
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Завдання зі статусом new
SELECT * FROM tasks
WHERE status_id = (
    SELECT id FROM status WHERE name = 'new'
);

-- 3. Змінити статус завдання з id = 1
UPDATE tasks
SET status_id = (
    SELECT id FROM status WHERE name = 'in progress'
)
WHERE id = 1;

-- 4. Користувачі без завдань
SELECT * FROM users
WHERE id NOT IN (
    SELECT user_id FROM tasks
);

-- 5. Додати завдання користувачу з id = 9
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Перевірити базу даних',
    'Виконати та перевірити SQL-запити',
    (SELECT id FROM status WHERE name = 'new'),
    9
);

-- 6. Усі незавершені завдання
SELECT * FROM tasks
WHERE status_id != (
    SELECT id FROM status WHERE name = 'completed'
);

-- 7. Видалити завдання з id = 2
DELETE FROM tasks WHERE id = 2;

-- 8. Користувачі з поштою example.com
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача з id = 1
UPDATE users SET fullname = 'Михайло Ковальов' WHERE id = 1;

-- 10. Кількість завдань за кожним статусом
SELECT s.name, COUNT(t.id) AS tasks_count
FROM status AS s
LEFT JOIN tasks AS t ON t.status_id = s.id
GROUP BY s.id, s.name
ORDER BY s.id;

-- 11. Завдання користувачів із поштою example.com
SELECT t.*, u.fullname, u.email
FROM tasks AS t
JOIN users AS u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT * FROM tasks WHERE description IS NULL;

-- 13. Користувачі та їхні завдання у статусі in progress
SELECT u.fullname, u.email, t.title, t.description
FROM users AS u
INNER JOIN tasks AS t ON t.user_id = u.id
INNER JOIN status AS s ON s.id = t.status_id
WHERE s.name = 'in progress';

-- 14. Користувачі та кількість їхніх завдань
SELECT u.id, u.fullname, COUNT(t.id) AS tasks_count
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.id
GROUP BY u.id, u.fullname
ORDER BY u.id;