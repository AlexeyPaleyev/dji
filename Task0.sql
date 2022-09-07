USE `db`;
CREATE OR REPLACE VIEW GetCandidateDates AS
SELECT t.candidate_id, MIN(t.hire_reported) AS dts, MAX(t.hire_reported) AS dte  
	FROM db.test_task t	
	WHERE t.hire_reported BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:59'
	GROUP BY t.candidate_id
	HAVING COUNT(t.candidate_id) > 1;



