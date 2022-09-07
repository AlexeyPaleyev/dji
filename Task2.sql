SELECT -- t.candidate_id,  
AVG(tmax.hire_salary - tmin.hire_salary) AS salary_diff_avg
FROM GetCandidateDates t
LEFT JOIN test_task tmin
ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
LEFT JOIN test_task tmax
ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported
-- GROUP BY t.candidate_id
-- ORDER BY tmax.hire_salary - tmin.hire_salary
;

