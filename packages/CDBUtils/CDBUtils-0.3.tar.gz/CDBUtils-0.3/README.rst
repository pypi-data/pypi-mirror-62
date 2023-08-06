========
CDBUtils
========
**CDBUtils is since DBUtils 1.3**
The CDBUtils home page can be found here:https://gitee.com/ctec/CDBUtils/

*Extension parameter descriptions:*

- test_on_borrow: check availability of the connection fetched from the pool (True = check,False = default = never check)
- test_idle: Check connection availability on idle(True = default = check,False = never check)
- validation_sql: the sql for validate the connection (default is "SELECT 1 FROM DUAL")
- idle_check_time: the seconds for Check and remove the idle connection interval.
- validate_timeout: the max seconds to execute the validation Sql,default is 1.
- max_wait_time: the max wait time for fetch one connection from the pool, default is 5s
