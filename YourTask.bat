::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJG6L5kkjOBpXSTimNmq0AbogzOzo0/mTo1kUV942dY7c36eyOe8G+HrwdIUm6SsUkcgDbA==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJG6L5kkjOBpXSTimNmq0AbogzOzo09OIt18pVfE0NorD39Q=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
cd %~dp0
call %~dp0Scripts\activate.bat

rem ejecutar el proxy de fondo
start /B cloud-sql-proxy --address 127.0.0.1 --port 3306 yourtaskmanager-402219:us-central1:your-task-manager

rem pausar consola por unos segundos para esperar que la conexión del proxy se realize 
timeout /t 5 /nobreak > nul

rem cuando termina empezar el servicio de la app
start chrome http://127.0.0.1:8000/
py manage.py runserver

pause