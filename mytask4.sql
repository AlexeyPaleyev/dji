-- кількість наймів кандидатів з досвідом до 0.5 р по категоріях

	SELECT DISTINCT COUNT(t.candidate_id), t.primary_keyword_candidate
		FROM test_task t
	WHERE t.experience_years < 0.5 AND 
    t.hire_reported BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:59' AND
    t.primary_keyword_candidate <> ''
    GROUP BY t.primary_keyword_candidate
    ORDER BY COUNT(t.candidate_id) ;