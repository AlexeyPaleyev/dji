-- Кількість кандидатів які збыльшили  компенсвцію більше, ніж на 200 $
SELECT COUNT(*) FROM (
SELECT t.candidate_id,  tmax.hire_salary AS sl_max, tmin.hire_salary AS sl_min,
(tmax.hire_salary - tmin.hire_salary) AS salary_diff
FROM GetCandidateDates t
LEFT JOIN test_task tmin
ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
LEFT JOIN test_task tmax
ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported
WHERE tmax.hire_salary <> 0 AND tmin.hire_salary <> 0
GROUP BY t.candidate_id
HAVING tmax.hire_salary - tmin.hire_salary > 200
ORDER BY tmax.hire_salary - tmin.hire_salary) tt


;

