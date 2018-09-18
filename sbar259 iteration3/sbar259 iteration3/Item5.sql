create table Drone(
	id int not null,
    name varchar(100),
    class_type tinyint,
    rescue boolean,
    operatorID int unique,
    mapID int,
    
    primary key(id),
    foreign key(operatorID) references Operator(id),
    foreign key(mapID) references Map(id)
); 

create table Operator(
	id int not null,
    first_name varchar(100) not null,
    last_name varchar(100),
    date_of_birth date not null,
    drone_license tinyint,
    rescue_endorsement boolean not null,
    number_of_operations int,
    
    primary key(id)
);

create table Map(
    id int not null,
    name varchar(100) not null,
    filepath varchar(255) not null,
    
    primary key(id)
);