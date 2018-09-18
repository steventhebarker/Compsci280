#ggg import mysql.connector
import Tkinter as tk
import ttk

from drones import Drone, DroneStore
from operators import Operator, OperatorStore


class Application(object):
    """ Main application view - displays the menu. """

    def __init__(self, conn):
        # Initialise the stores
        self.drones = DroneStore(conn)
        self.operators = OperatorStore(conn)
        self._conn = conn

        # Initialise the GUI window
        self.root = tk.Tk()
        self.root.title('Drone Allocation and Localisation')
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Add in the buttons
        drone_button = tk.Button(
            frame, text="View Drones", command=self.view_drones, width=40, padx=5, pady=5)
        drone_button.pack(side=tk.TOP)
        operator_button = tk.Button(
            frame, text="View Operators", command=self.view_operators, width=40, padx=5, pady=5)
        operator_button.pack(side=tk.TOP)
        exit_button = tk.Button(frame, text="Exit System",
                                command=quit, width=40, padx=5, pady=5)
        exit_button.pack(side=tk.TOP)

    def main_loop(self):
        """ Main execution loop - start Tkinter. """
        self.root.mainloop()

    def view_operators(self):
        """ Display the operators. """
        # Instantiate the operators window
        # Display the window and wait
        print 'TODO operators'

    def view_drones(self):
        """ Display the drones. """
        wnd = DroneListWindow(self, self._conn)
        self.root.wait_window(wnd.root)

class ListWindow(object):
    """ Base list window. """

    def __init__(self, parent, title, conn):
        # Add a variable to hold the stores
        self.drones = parent.drones
        self.operators = parent.operators
        self._conn = conn

        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

    def add_list(self, columns, edit_action):
        # Add the list
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.title())
        ysb = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                            command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL,
                            command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        self.tree.bind("<Double-1>", edit_action)

        # Add tree and scrollbars to frame
        self.tree.grid(in_=self.frame, row=0, column=0, sticky=tk.NSEW)
        ysb.grid(in_=self.frame, row=0, column=1, sticky=tk.NS)
        xsb.grid(in_=self.frame, row=1, column=0, sticky=tk.EW)

        # Set frame resize priorities
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def close(self):
        """ Closes the list window. """
        self.root.destroy()


class DroneListWindow(ListWindow):
    """ Window to display a list of drones. """

    def __init__(self, parent, _conn):
        super(DroneListWindow, self).__init__(parent, 'Drones', _conn)

        # Add the list and fill it with data
        columns = ('id', 'name', 'class', 'rescue', 'operator')
        self.add_list(columns, self.edit_drone)
        self.populate_data() 

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Add Drone",
                               command=self.add_drone, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=2, column=0, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=3, column=0, sticky=tk.E)

    def populate_data(self):
        """ Populates the data in the view. """
        print 'TODO: Load data'
        #ggg cursor = self._conn.cursor()
        # query='SELECT Drone.ID, Drone.Name, Drone.class_type, Drone.rescue,\
        #     Operator.first_name, Operator.last_name FROM Drone \
        #     LEFT JOIN Operator ON Drone.operatorID = Operator.id \
        #     ORDER BY Drone.Name'
        # cursor.execute(query)
        # for(id,name, class_type, rescue, first_name, last_name) in cursor:
        #     if last_name is not None:
        #         self.tree.insert('', 'end', values=(id, name, class_type, rescue, first_name+' '+last_name))
        #     elif first_name is not None:
        #         self.tree.insert('', 'end', values=(id, name, class_type, rescue, first_name))
        #     else:
        #         self.tree.insert('', 'end', values=(id, name, class_type, rescue, '<None>'))
        # cursor.close()

        # The following is a dummy record - need to remove and replace with data from the store

    def add_drone(self):
        """ Starts a new drone and displays it in the list. """
        # Start a new drone instance
        print 'TODO: Start a new drone'
        drone = None

        # Display the drone
        self.view_drone(drone, self._save_new_drone)

    def _save_new_drone(self, drone):
        """ Saves the drone in the store and updates the list. """
        self.drones.add(drone)
        self.populate_data()

    def edit_drone(self, event):
        """ Retrieves the drone and shows it in the editor. """
        # Retrieve the identifer of the drone
        item = self.tree.item(self.tree.focus())
        item_id = item['values'][0]

        # Load the drone from the store
        print 'TODO: Load drone with ID %04d' % (item_id)
        drone = None

        # Display the drone
        self.view_drone(drone, self._update_drone)

    def _update_drone(self, drone):
        """ Saves the new details of the drone. """
        self.drones.save(drone)
        self.populate_data()

    def view_drone(self, drone, save_action):
        """ Displays the drone editor. """
        wnd = DroneEditorWindow(self, drone, save_action)
        self.root.wait_window(wnd.root)

class EditorWindow(object):
    """ Base editor window. """

    def __init__(self, parent, title, save_action):
        # Initialise the new top-level window (modal dialog)
        self._parent = parent.root
        self.root = tk.Toplevel(parent.root)
        self.root.title(title)
        self.root.transient(parent.root)
        self.root.grab_set()

        # Initialise the top level frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH,
                        expand=tk.Y, padx=10, pady=10)

        # Add the editor widgets
        last_row = self.add_editor_widgets()

        # Add the command buttons
        add_button = tk.Button(self.frame, text="Save",
                               command=save_action, width=20, padx=5, pady=5)
        add_button.grid(in_=self.frame, row=last_row + 1, column=1, sticky=tk.E)
        exit_button = tk.Button(self.frame, text="Close",
                                command=self.close, width=20, padx=5, pady=5)
        exit_button.grid(in_=self.frame, row=last_row + 2, column=1, sticky=tk.E)

    def add_editor_widgets(self):
        """ Adds the editor widgets to the frame - this needs to be overriden in inherited classes. 
        This function should return the row number of the last row added - EditorWindow uses this
        to correctly display the buttons. """
        return -1

    def close(self):
        """ Closes the editor window. """
        self.root.destroy()

class DroneEditorWindow(EditorWindow):
    """ Editor window for drones. """

    def __init__(self, parent, drone, save_action):
        # TODO: Add either the drone name or <new> in the window title, depending on whether this is a new
        # drone or not
        super(DroneEditorWindow, self).__init__(parent, 'Drone: ', self.save_drone)
        self._drone = drone
        self._save_action = save_action

        # TODO: Load drone details

    def add_editor_widgets(self):
        """ Adds the widgets dor editing a drone. """
        print 'TODO: Create widgets and populate them with data'
        return -1

    def save_drone(self):
        """ Updates the drone details and calls the save action. """
        print 'TODO: Update the drone from the widgets'
        self._save_action(self._drone)



if __name__ == '__main__':
    #ggg conn = mysql.connector.connect(user='sbar259',
    #                                password='Labradoodle111',
    #                                host='studdb-mysql.fos.auckland.ac.nz',
    #                                database='stu_sbar259_COMPSCI_280_C_S2_2018',
    #                                charset = 'utf8')
    conn = '' #ggg
    app = Application(conn)
    app.main_loop()
    conn.close()
