p_year = ['2020-01-01 00:00:00', '2020-12-31 23:59:59']
tasks = [
    {
        "text": "Кількість кандидатів, які хоча би 1 раз змінили роботу у 2020-му році ",
        "sql_str": """SELECT COUNT(*) FROM (
	                SELECT candidate_id
		            FROM test_task t 
		            WHERE t.hire_reported BETWEEN %s AND %s
		            GROUP BY t.candidate_id) tt ;""",
        "par": p_year
    },
    {
        "text": "Кількість кандидатів, які 2 раза змінили роботу у 2020-му році ",
        "sql_str": """SELECT COUNT(*) FROM (
                	    SELECT candidate_id
		                FROM test_task t 
		                WHERE t.hire_reported BETWEEN %s AND %s
		                GROUP BY t.candidate_id
                        HAVING COUNT(t.candidate_id) = 2 ) tt ;""",
        "par": p_year
    },
    {
        "text": "Кількість кандидатів, які більше 2 раз змінили роботу у 2020-му році ",
        "sql_str": """SELECT COUNT(*) FROM (
	                    SELECT candidate_id
		                FROM test_task t 
		                WHERE t.hire_reported BETWEEN %s AND %s
                		GROUP BY t.candidate_id
                        HAVING COUNT(t.candidate_id) > 2 ) tt ;""",
        "par": p_year
    },
    {
        "text": "Кількість наймів кандидатів з досвідом до 1 р включно ",
        "sql_str": """SELECT COUNT(*) FROM (
                        SELECT DISTINCT t.candidate_id 
		                    FROM test_task t
	                        WHERE t.experience_years <= 1 AND 
                            t.hire_reported BETWEEN %s AND %s) tt;""",
        "par": p_year
    },
    {
        "text": "Квтегорія с найбільшою кількістю наймів кандидатів з досвідом до 1 р включно",
        "sql_str": """	SELECT DISTINCT COUNT(t.candidate_id), t.primary_keyword_candidate
                		FROM test_task t
	                    WHERE t.experience_years <= 1 AND 
                        t.hire_reported BETWEEN %s AND %s AND
                        t.primary_keyword_candidate <> ''
                        GROUP BY t.primary_keyword_candidate
                        ORDER BY COUNT(t.candidate_id) ;""",
        "par": p_year
    },
    {
        "text": "Найбільше збільшення компенсації ",
        "sql_str": """	SELECT t.candidate_id,  tmax.hire_salary, tmin.hire_salary,
                            (tmax.hire_salary - tmin.hire_salary) AS salary_diff
                            FROM GetCandidateDates t
                            LEFT JOIN test_task tmin
                            ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
                            LEFT JOIN test_task tmax
                            ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported
                            WHERE tmax.hire_salary <> 0 AND tmin.hire_salary <> 0
                            GROUP BY t.candidate_id
                            ORDER BY tmax.hire_salary - tmin.hire_salary""",
        "par": []
    },
    {
        "text": "Кількість кандидатів які збілішили  компенсвцію більше, ніж на 200 $ ",
        "sql_str": """	SELECT COUNT(*) FROM (
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
                            ORDER BY tmax.hire_salary - tmin.hire_salary) tt;""",
        "par": []
    },
    {
        "text": "Кількість кандидатів які збільшили  компенсвцію більше, ніж на 20% ",
        "sql_str": """	SELECT COUNT(*) FROM (
                            SELECT t.candidate_id,  tmax.hire_salary AS sl_max, tmin.hire_salary AS sl_min,
                            (tmax.hire_salary - tmin.hire_salary) AS salary_diff
                            FROM GetCandidateDates t
                            LEFT JOIN test_task tmin
                            ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
                            LEFT JOIN test_task tmax
                            ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported
                            WHERE tmax.hire_salary <> 0 AND tmin.hire_salary <> 0
                            GROUP BY t.candidate_id
                            HAVING (tmax.hire_salary - tmin.hire_salary) / tmin.hire_salary > 0.2
                            ORDER BY tmax.hire_salary - tmin.hire_salary) tt;""",
        "par": []
    },
    {
        "text": "Відсоток кандидатів, які змінювали роботу 2 чи більше рази у 2020-му році ",
        "sql_str": """SET @cnt_ch = (SELECT COUNT(*) FROM GetCandidateDates);
                    SET @cnt_tot = (SELECT COUNT(*) FROM (
                    SELECT DISTINCT t.candidate_id FROM test_task t 
                    WHERE t.hire_reported BETWEEN %s AND %s) tt);
                    SELECT @cnt_ch / @cnt_tot * 100 AS percent;""",
        "par": p_year
    },
    {
        "text": "На скільки $$ в середньому зросли зарплати у таких кандидатів після зміни роботи",
        "sql_str": """SELECT AVG(tmax.hire_salary - tmin.hire_salary) AS salary_diff_avg
                        FROM GetCandidateDates t
                        LEFT JOIN test_task tmin
                        ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
                        LEFT JOIN test_task tmax
                        ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported;""",
        "par": []
    },
    {
        "text": "Серед кандидатів, що змінювали роботу 2 чи більше рази - для якого відсотка кандидатів між двома наймами пройшло менше ніж 6 місяців",
        "sql_str": """SET @cng_6m = (SELECT count(*)
				            FROM GetCandidateDates t
				            WHERE  date_add(date(t.dts), INTERVAL 6 MONTH) < date(t.dte));
                        SET @cnt_tot = (SELECT COUNT(*) FROM (
				            SELECT DISTINCT t.candidate_id FROM test_task t 
				            WHERE t.hire_reported BETWEEN %s AND %s) tt);
                        SELECT @cng_6m / @cnt_tot * 100 AS percent;""",
        "par": p_year

    }
]
grafs = {
    "text": "Кількість наймів кандидатів з досвідом до 1 р  включно ",
    "sql_str": """SELECT DISTINCT COUNT(t.candidate_id) AS cnt, t.primary_keyword_candidate, t.en_level_candidate
		                FROM test_task t
	                    WHERE t.experience_years <= 1  AND 
	                    t.hire_reported BETWEEN %(dstart)s AND %(dend)s AND
                        t.primary_keyword_candidate <> ''
                        GROUP BY t.primary_keyword_candidate, en_level_candidate
                        ORDER BY COUNT(t.candidate_id);""",
    "par": {'dstart': '2020-01-01 00:00:00',
            'dend': '2020-12-31 23:59:59'}
}
sal = {
    "text": "Зміна компнсації за 2020р ",
    "sql_str": """SELECT t.candidate_id,  tmax.hire_salary AS sl_max, tmin.hire_salary AS sl_min,
                    (tmax.hire_salary - tmin.hire_salary) AS salary_diff
                    FROM GetCandidateDates t
                    LEFT JOIN test_task tmin
                    ON t.candidate_id = tmin.candidate_id AND t.dts = tmin.hire_reported
                    LEFT JOIN test_task tmax
                    ON t.candidate_id = tmax.candidate_id AND t.dte = tmax.hire_reported
                    WHERE tmax.hire_salary <> 0 AND tmin.hire_salary <> 0
                    GROUP BY t.candidate_id
                    ORDER BY tmax.hire_salary - tmin.hire_salary;""",
    "par": {'dstart': '2020-01-01 00:00:00',
            'dend': '2020-12-31 23:59:59'}

}
