class Drone(object):
    """ Stores details on a drone. """

    def __init__(self, name, class_type=1, rescue=False):
        self.id = 0
        self.name = name
        self.class_type = class_type
        self.rescue = rescue
        self.operator = None


class DroneAction(object):
    """ A pending action on the DroneStore. """

    def __init__(self, drone, operator, commit_action):
        self.drone = drone
        self.operator = operator
        self.messages = []
        self._commit_action = commit_action
        self._committed = False

    def add_message(self, message):
        """ Adds a message to the action. """
        self.messages.append(message)

    def is_valid(self):
        """ Returns True if the action is valid, False otherwise. """
        return len(self.messages) == 0

    def commit(self):
        """ Commits (performs) this action. """
        if self._committed:
            raise Exception("Action has already been committed")

        self._commit_action(self.drone, self.operator)
        self._committed = True


class DroneStore(object):
    """ DroneStore stores all the drones for DALSys. """

    def __init__(self, conn=None):
        self._drones = {}
        self._last_id = 0
        self._conn = conn

    def add(self, args):
        """ Adds a new drone to the store. """
        drone_class = None
        name = None
        rescue = "False"
        for item in args:
            if item.startswith("-class="):
                drone_class = int(item[-1])
            elif item == "-rescue":
                rescue = "True"
            else:
                item = item.replace("'", "")
                name = "'"+item+"'"

        #if name or class was not entered
        if name is None and drone_class is None:
            raise Exception("Name and Class is required")
        if name is None:
            raise Exception("Name is required")
        if drone_class is None:
            raise Exception("Class is required")
        print drone_class

        #set ID to the next increment
        cursor = self._conn.cursor()
        cursor.execute("select max(id) from Drone")
        for max_id in cursor:
            id = max_id[0] + 1
        
        #insert the drone
        query = 'insert into Drone (id, name, class_type, rescue) \
        values (%d, %s, %d, %s)'%(id, name, drone_class, rescue)

        #display message
        print "Added drone with ID %04d"%id
        cursor.execute(query)
        cursor.close()
    
    def update(self, args):
        """Updates characteristics of a drone"""
        #making sure a valid id was entered
        try:
            id = args[0]
            int(id)
        except:
            raise Exception("ID is required")

        cursor = self._conn.cursor()
        
        #making sure drone exists
        query = 'SELECT COUNT(*) FROM Drone WHERE id = '+id+';'

        id_exists = False
        cursor.execute(query)
        for (count) in cursor:
            id_exists = int(count[0])

        if not id_exists:
            raise Exception("Unknown drone")

        #getting current values from the drone
        query = 'SELECT * FROM Drone WHERE id = '+id+';'
        cursor.execute(query)
        for (current_id, current_name, current_class_type, current_rescue, operatorID, mapID) in cursor:
            current_id = str(current_id)
            current_class_type = str(current_class_type)
            current_rescue = str(current_rescue)

        
        #declaring variables
        new_class_type = current_class_type
        new_name = current_name
        new_rescue = "0"

        #getting variables from input
        for item in args[1:]:
            if item.startswith("-class="):
                new_class_type = item[-1]
            elif item.startswith("-name="):
                new_name = item[6:]+", "
                new_name = name.replace("'", "")
                
            elif item == "-rescue":
                new_rescue = "1"
            else:
                raise Exception("Uknown Parameter")

        #raise exception if no changes
        something_changed = False
        changed_items = [None, None, None]
        if  new_name != current_name:
            changed_items[0] = "-Changed name to "+new_name
            something_changed = True
        if new_class_type != current_class_type:
            changed_items[1] = "-Changed class to "+new_class_type
            something_changed = True
        if new_rescue != current_rescue:
            changed_items[2] = "-Changed Rescue Endorsement to "+new_rescue
            something_changed = True

        if not something_changed:
            raise Exception("No changes detected")


        #preparing SQL statement
        things_to_update = "name = '"+new_name+"', class_type = "+new_class_type+", rescue = "+new_rescue
        
        #executing SQL statement
        query = "UPDATE Drone SET "+things_to_update+" WHERE id = "+ id
        cursor.execute(query)
        cursor.close()

        #print messages
        print "Updated drone with ID %04d"%int(id)
        for item in changed_items:
            if item != None:
                print item



    def remove(self, args):
        """ Removes a drone from the store. """

        #making sure a valid id was entered
        try:
            id = args[0]
            int(id)
        except:
            raise Exception("ID is required")

        cursor = self._conn.cursor()
        
        #making sure drone exists
        query = 'SELECT COUNT(*) FROM Drone WHERE id = '+id+';'

        id_exists = False
        cursor.execute(query)
        for (count) in cursor:
            id_exists = int(count[0])

        if not id_exists:
            raise Exception("Unknown drone")
        
        #disable safe update mode
        query = 'SET SQL_SAFE_UPDATES = 0;'
        cursor.execute(query)

        #delete the drone
        query = 'DELETE FROM Drone WHERE id='+id
        cursor.execute(query)
        print "Drone removed"


    def get(self, id):
        """ Retrieves a drone from the store by its ID. """
        if not id in self._drones:
            return None
        else:
            return self._drones[id]

    def list_all(self, args):
        """ Lists all the drones in the system. """
        if args == []:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            ORDER BY Drone.Name'
        elif "-rescue" in args and "-class=1" in args:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            WHERE Drone.class_type = 1 AND Drone.rescue = 1 \
            ORDER BY Drone.Name'
        elif "-rescue" in args and "-class=2" in args:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            WHERE Drone.class_type = 2 AND Drone.rescue = 1 \
            ORDER BY Drone.Name'
        elif "-class=1" in args:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            WHERE Drone.class_type = 1\
            ORDER BY Drone.Name'
        elif "-class=2" in args:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            WHERE Drone.class_type = 2\
            ORDER BY Drone.Name'
        elif "-rescue" in args:
            query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
            Operator.first_name, Operator.last_name FROM Drone \
            LEFT JOIN Operator ON Drone.operatorID = Operator.id \
            WHERE Drone.rescue = 1\
            ORDER BY Drone.Name'
        else:
            raise Exception ("Invalid Parameters")
        cursor= self._conn.cursor()


        #raise error if no drones for that criteria
        cursor.execute(query)
        has_drones = False
        for(id,name, class_type, rescue, first_name, last_name) in cursor:
            has_drones = True
        if not has_drones:
            raise Exception("There are no drones for this criteria")

        #make make table from results
        cursor.execute(query)
        print "ID\t\t\t\tName\t\tClass\tRescue\tOperator"
        for(id,name, class_type, rescue, first_name, last_name) in cursor:
            if first_name is not None:
                print "%04d"%id +"\t"+"%30s"%name+"%10s"%str(class_type)+"%10s"%str(rescue)+"%10s"%str(first_name)+" "+str(last_name) 
            else:
                print "%04d"%id +"\t"+"%30s"%name+"%10s"%str(class_type)+"%10s"%str(rescue)+"%10s"%str(first_name)+"<None>"
        cursor.close()

    def allocate(self, args):
        """ Starts the allocation of a drone to an operator. """
        #making sure a valid id was entered
        print args
        try:
            drone_id = args[0]
            int(drone_id)
        except:
            raise Exception("ID is required")
        
        try:
            first_name = args[1]
            first_name = first_name.replace("'","")
            first_name = "'"+first_name+"'"

            last_name = args[2]
            last_name = last_name.replace("'","")
            last_name = "'"+last_name+"'"
        except:
            raise Exception("Operator is required")

        cursor = self._conn.cursor()

        #making sure drone exists
        query = 'SELECT COUNT(*) FROM Drone WHERE id = '+drone_id+';'

        id_exists = False
        cursor.execute(query)
        for (count) in cursor:
            id_exists = int(count[0])
        if not id_exists:
            raise Exception("Unknown drone")
        
        #making sure operator exists
        query = 'SELECT COUNT(*) FROM Operator WHERE first_name = '+first_name+' AND last_name = '+last_name

        op_exists = False
        cursor.execute(query)
        for (count) in cursor:
            op_exists = int(count[0])
        if not op_exists:
            add_op = str(raw_input("Operator does not exist, do oyu want to add operator [Y/n]?"))
            if add_op.lower() == 'y':
                #set ID to the next increment
                cursor = self._conn.cursor()
                cursor.execute("select max(id) from Operator")
                for max_id in cursor:
                    id = max_id[0] + 1
            
                #insert the drone
                query = 'insert into Operator (id, first_name, last_name, drone_license, rescue_endorsement) \
                values (%d, %s, %s, 2, 1)'%(id, first_name, last_name)
                cursor.execute(query)
                print("Operator added")
            
        #getting data from the operator
        query = 'SELECT id, drone_license, rescue_endorsement  FROM Operator WHERE first_name = '+first_name+' AND last_name = '+last_name
        cursor.execute(query)
        for (id, drone_license, rescue_endorsement) in cursor:
            op_id = str(id)
            op_drone_license = str(drone_license)
            op_rescue_endorsement = str(rescue_endorsement)
            
        #Getting Data from drone
        query = 'SELECT class_type, rescue, operatorID FROM Drone WHERE id = '+drone_id
        cursor.execute(query)
        for (class_type, rescue, operatorID) in cursor:
            drone_class_type = class_type
            drone_rescue = rescue
            drone_operatorID = operatorID

        if drone_class_type > op_drone_license or drone_rescue > op_rescue_endorsement:
            print drone_class_type
            print op_drone_license
            print drone_rescue
            print op_rescue_endorsement
            raise Exception

        #checking if drone is already allocated
        if drone_operatorID != None:
            #get operator
            print (drone_operatorID)
            query = 'SELECT first_name, last_name from Operator WHERE id = '+str(drone_operatorID)
            cursor.execute(query)
            for (first, last) in cursor:
                current_first_name = first
                current_last_name = last
            print("Validation errors:")
            print "Drone already allocated to "+first+" "+last
            _continue = str(raw_input("Do you want to continue? [Y/n]?"))
            if _continue.lower() == 'n':
                raise Exception("Allocation cancelled")
        


        query = "UPDATE Drone SET operatorID = "+op_id+" WHERE id = "+ drone_id
        cursor.execute(query)
        print "Drone allocated to "+first_name[1:-1]+" "+last_name[1:-1]
        cursor.close()

    def save(self, drone):
        """ Saves the drone to the database. """
        pass    # TODO: we don't have a database yet
