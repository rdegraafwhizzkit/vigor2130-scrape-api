create database home;
grant all on home.* to 'home'@'%' identified by 'Home123!';
flush privileges;
use home;
drop table if exists velop;
create table velop(computer_name varchar(128), velop varchar(32), timestamp integer, id varchar(56) primary key);
truncate table velop;