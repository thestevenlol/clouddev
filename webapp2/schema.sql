create table swimmers (
    id int not null primary key auto_increment,
    name varchar(50) not null,
    age int not null
);

create table events (
    id int not null primary key auto_increment,
    distance int not null,
    stroke varchar(10) not null
);

create table times (
    swimmer_id int not null,
    event_id int not null,
    time varchar(10) not null,
    ts timestamp not null default current_timestamp,
    foreign key (swimmer_id) references swimmers(id),
    foreign key (event_id) references events(id),
    unique (swimmer_id, event_id, time)
);

ALTER TABLE swimmers ADD UNIQUE (name, age);
ALTER TABLE events ADD UNIQUE (distance, stroke);