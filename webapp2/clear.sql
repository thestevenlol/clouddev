delete from swimmers where id > 0;
alter table swimmers AUTO_INCREMENT = 1;

delete from events where id > 0;
alter table events AUTO_INCREMENT = 1;

delete from times;