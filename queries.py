ADD_STUDENT = "INSERT INTO students (name, group_name) VALUES (%s, %s) RETURNING id;"
GET_ALL_STUDENTS = "SELECT id, name, group_name, is_active, created_at FROM students ORDER BY name;"
GET_STUDENT_BY_ID = "SELECT * FROM students WHERE id = %s;"
UPDATE_STUDENT = "UPDATE students SET name = %s, group_name = %s, is_active = %s WHERE id = %s;"
DELETE_STUDENT = "DELETE FROM students WHERE id = %s;"

# Задания
ADD_TASK = "INSERT INTO tasks (title, max_score) VALUES (%s, %s) RETURNING id;"
GET_ALL_TASKS = "SELECT id, title, max_score, is_archived, created_at FROM tasks ORDER BY title;"
GET_TASK_BY_ID = "SELECT * FROM tasks WHERE id = %s;"
UPDATE_TASK = "UPDATE tasks SET title = %s, max_score = %s, is_archived = %s WHERE id = %s;"
DELETE_TASK = "DELETE FROM tasks WHERE id = %s;"

# Сдачи
ADD_OR_UPDATE_SUBMISSION = """
    INSERT INTO submissions (student_id, task_id, score, comment)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (student_id, task_id) DO UPDATE SET
        score = EXCLUDED.score,
        comment = EXCLUDED.comment,
        submitted_at = CURRENT_TIMESTAMP;
"""
GET_ALL_SUBMISSIONS = """
    SELECT
        s.id AS submission_id,
        st.name AS student_name,
        st.group_name,
        t.title AS task_title,
        s.score,
        s.submitted_at,
        s.comment
    FROM submissions s
    JOIN students st ON s.student_id = st.id
    JOIN tasks t ON s.task_id = t.id
    ORDER BY s.submitted_at DESC;
"""

# Отчеты 
REPORT_AVG_SCORE = """
    SELECT
        st.id,
        st.name,
        st.group_name,
        COALESCE(AVG(s.score), 0) AS avg_score,
        COUNT(s.id) AS submission_count
    FROM students st
    LEFT JOIN submissions s ON st.id = s.student_id
    GROUP BY st.id, st.name, st.group_name
    ORDER BY avg_score DESC;
"""

REPORT_TOP_STUDENTS = """
    SELECT
        st.id,
        st.name,
        st.group_name,
        COALESCE(SUM(s.score), 0) AS total_score,
        COUNT(s.id) AS submission_count
    FROM students st
    LEFT JOIN submissions s ON st.id = s.student_id
    GROUP BY st.id, st.name, st.group_name
    ORDER BY total_score DESC
    LIMIT 5;
"""

REPORT_NO_SUBMISSIONS = """
    SELECT id, name, group_name
    FROM students st
    WHERE NOT EXISTS (
        SELECT 1 FROM submissions s WHERE s.student_id = st.id
    );
"""