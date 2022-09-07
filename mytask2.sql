-- "Кількість кандидатів, які 2 раза змінили роботу у 2020-му році "
SELECT COUNT(*) FROM (
	SELECT candidate_id
		FROM test_task t 
		WHERE t.hire_reported BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:59'
		GROUP BY t.candidate_id
        HAVING COUNT(t.candidate_id) = 2 ) tt ;