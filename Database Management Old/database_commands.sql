INSERT INTO results (RUNNER_ID) VALUES (
    (SELECT USER_ID FROM login WHERE USERNAME = '{username}')
);
INSERT INTO wolf_results (RUN_ID, POPULATION, AVG_ATK, AVG_HP, AVG_SPD) VALUES (
    (SELECT RUN_ID FROM results WHERE RUN_ID = {run_id}),
    {population},
    {atk},
    {hp},
    {spd}
);
INSERT INTO jaguar_results (RUN_ID, POPULATION, AVG_ATK, AVG_HP, AVG_SPD) VALUES (
    (SELECT RUN_ID FROM results WHERE RUN_ID = {run_id}),
    {population},
    {atk},
    {hp},
    {spd}
);
INSERT INTO rabbit_results (RUN_ID, POPULATION, AVG_ATK, AVG_HP, AVG_SPD) VALUES (
    (SELECT RUN_ID FROM results WHERE RUN_ID = {run_id}),
    {population},
    {atk},
    {hp},
    {spd}
);
INSERT INTO deer_results (RUN_ID, POPULATION, AVG_ATK, AVG_HP, AVG_SPD) VALUES (
    (SELECT RUN_ID FROM results WHERE RUN_ID = {run_id}),
    {population},
    {atk},
    {hp},
    {spd}
);