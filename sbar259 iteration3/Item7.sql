insert into Operator(id, first_name, last_name, date_of_birth, rescue_endorsement, number_of_operations)
values (1, "John", "Doe", '2003-01-01', False, 0); 
insert into Operator(id, first_name, last_name, date_of_birth, drone_license, rescue_endorsement, number_of_operations)
values (2, "Josh", "Doe", '2003-01-01', 1, False, 0); 
insert into Operator(id, first_name, last_name, date_of_birth, drone_license, rescue_endorsement, number_of_operations)
values (3, "Jake", "Doe", '1990-01-01', 2, False, 0); 
insert into Operator(id, first_name, last_name, date_of_birth, drone_license, rescue_endorsement, number_of_operations)
values (4, "Jane", "Doe", '1990-01-01', 2, True, 10); 

insert into Map (id, name, filepath)
values (1, "Abel Tasman", "map_abel_tasman_3.jpg");
insert into Map (id, name, filepath)
values (2, "Ruatiti", "ruatiti.jpg");

insert into Drone (id,  name, class_type)
values (1, "Drone1", 1);
insert into Drone (id,  name, class_type)
values (2, "Drone2", 2);
insert into Drone (id,  name, class_type, rescue)
values (3, "Drone3", 2, True);

insert into Drone (id,  name, class_type, rescue, operatorID, mapID)
values (4, "Drone4", 1, False, 2, 1);
insert into Drone (id,  name, class_type, rescue, operatorID, mapID)
values (5, "Drone5", 3, True, 3, 2);