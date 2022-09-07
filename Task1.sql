SET @cnt_ch = (SELECT COUNT(*) FROM GetCandidateDates);
SET @cnt_tot = (SELECT COUNT(*) FROM (
				SELECT DISTINCT t.candidate_id FROM test_task t 
				WHERE t.hire_reported BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:59') tt);
SELECT @cnt_ch / @cnt_tot * 100 AS percent;