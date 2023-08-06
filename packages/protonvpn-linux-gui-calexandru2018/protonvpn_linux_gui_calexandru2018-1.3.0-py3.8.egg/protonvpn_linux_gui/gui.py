# Default package import
import os
import re
import sys
import pathlib
from threading import Thread
import time
import concurrent.futures

# ProtonVPN base CLI package import
from custom_pvpn_cli_ng.protonvpn_cli.constants import (USER, CONFIG_FILE)
from custom_pvpn_cli_ng.protonvpn_cli import cli

# ProtonVPN helper funcitons
from custom_pvpn_cli_ng.protonvpn_cli.utils import check_root

# Custom helper functions
from .utils import (
    populate_server_list,
    prepare_initilizer,
    load_on_start,
    load_configurations,
)

# Import functions that are called with threads
from .thread_functions import(
    quick_connect,
    disconnect,
    refresh_server_list,
    random_connect,
    last_connect,
    connect_to_selected_server,
    on_login,
    check_for_updates
)

from .constants import VERSION

# PyGObject import
import gi

# Gtk3 import
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, Gdk

class Handler:
    """Handler that has all callback functions.
    """
    def __init__(self, interface):
        self.interface = interface

    # Login BUTTON HANDLER
    def on_login_button_clicked(self, button):
        """Button/Event handler to intialize user account. Calls populate_server_list(server_list_object) to populate server list.
        """     
        login_window = self.interface.get_object("LoginWindow")
        user_window = self.interface.get_object("Dashboard")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(on_login, self.interface)
            return_value = future.result()
            
            if not return_value and not return_value is None:
                return

            user_window.show()
            login_window.destroy()    

    # Dashboard BUTTON HANDLERS
    def server_filter_input_key_release(self, object, event):
        """Event handler, to filter servers after each key release
        """
        user_filter_by = object.get_text()
        server_list_object = self.interface.get_object("ServerListStore")
        tree_view_object = self.interface.get_object("ServerList")

        # Creates a new filter from a ListStore
        n_filter = server_list_object.filter_new()

        # set_visible_func:
        # @first_param: filter function
        # @ seconde_param: input to filter by
        n_filter.set_visible_func(self.column_filter, data=user_filter_by)
        
        # Apply the filter model to a TreeView
        tree_view_object.set_model(n_filter)

        # Updates the ListStore model
        n_filter.refilter()

    def column_filter(self, model, iter, data=None):
        """Filter by columns and returns the corresponding rows
        """
        treeview = self.interface.get_object("ServerList")
        
        for col in range(0, treeview.get_n_columns()):
            value = model.get_value(iter, col).lower();
            if data.lower() in value.lower():
                return True
            else:
                continue

    def connect_to_selected_server_button_clicked(self, button):
        """Button/Event handler to connect to selected server
        """     
        thread = Thread(target=connect_to_selected_server, args=[self.interface])
        thread.daemon = True
        thread.start()

    def quick_connect_button_clicked(self, button):
        """Button/Event handler to connect to the fastest server
        """
        thread = Thread(target=quick_connect, args=[self.interface])
        thread.daemon = True
        thread.start()

    def last_connect_button_clicked(self, button):
        """Button/Event handler to reconnect to previously connected server
        """        
        thread = Thread(target=last_connect, args=[self.interface])
        thread.daemon = True
        thread.start()

    def random_connect_button_clicked(self, button):
        """Button/Event handler to connect to a random server
        """
        thread = Thread(target=random_connect, args=[self.interface])
        thread.daemon = True
        thread.start()

    def disconnect_button_clicked(self, button):
        """Button/Event handler to disconnect any existing connections
        """
        thread = Thread(target=disconnect, args=[self.interface])
        thread.daemon = True
        thread.start()
        
    def refresh_server_list_button_clicked(self, button):
        """Button/Event handler to refresh/repopulate server list
        - At the moment, will also refresh the Dashboard information, this will be fixed in the future.
        """
        thread = Thread(target=refresh_server_list, args=[self.interface])
        thread.daemon = True
        thread.start()

    def about_menu_button_clicked(self, button):
        """Button /Event handlerto open About dialog
        """
        about_dialog = self.interface.get_object("AboutDialog")
        about_dialog.set_version(VERSION)
        about_dialog.show()
    
    def check_for_updates_button_clicked(self, button):
        thread = Thread(target=check_for_updates)
        thread.daemon = True
        thread.start()

    def help_button_clicked(self, button):
        # To-do
        print("To-do show help.")

    def configuration_menu_button_clicked(self, button):
        """Button/Event handler to open Configurations window
        """
        load_configurations(self.interface)
        
    # To avoid getting the Preferences window destroyed and not being re-rendered again
    def ConfigurationsWindow_delete_event(self, object, event):
        """On Delete handler is used to hide the window so it renders next time the dialog is called
        
        -Returns:Boolean
        - It needs to return True, otherwise the content will not re-render after closing the dialog
        """
        if object.get_property("visible") == True:
            object.hide()
            return True

    # To avoid getting the About window destroyed and not being re-rendered again
    def AboutDialog_delete_event(self, object, event):
        """On Delete handler is used to hide the dialog and that it successfully  renders next time it is called
        
        -Returns:Boolean
        - It needs to return True, otherwise the content will not re-render after closing the window
        """
        if object.get_property("visible") == True:
            object.hide()
            return True

    # Preferences/Configuration menu HANDLERS
    def update_user_pass_button_clicked(self, button):
        """Button/Event handler to update Username & Password
        """
        username_field = self.interface.get_object("update_username_input")
        password_field = self.interface.get_object("update_password_input")

        username_text = username_field.get_text().strip()
        password_text = password_field.get_text().strip()

        if len(username_text) == 0 or len(password_text) == 0:
            print("Both field need to be filled")
            return

        cli.set_username_password(write=True, gui_enabled=True, user_data=(username_text, password_text))
        password_field.set_text("")

    def dns_preferens_combobox_changed(self, combobox):
        """Button/Event handler that is triggered whenever combo box value is changed.
        """
        # DNS ComboBox
        # 0 - Leak Protection Enabled
        # 1 - Custom DNS
        # 2 - None

        dns_custom_input = self.interface.get_object("dns_custom_input")

        if combobox.get_active() == 0 or combobox.get_active() == 2:
            dns_custom_input.set_property('sensitive', False)
        else:
            dns_custom_input.set_property('sensitive', True)

    def update_dns_button_clicked(self, button):
        """Button/Event handler to update DNS protection 
        """
        dns_combobox = self.interface.get_object("dns_preferens_combobox")

        dns_leak_protection = 1
        custom_dns = None
        if (not dns_combobox.get_active() == 0) and (not dns_combobox.get_active() == 2):
            dns_leak_protection = 0
            custom_dns = self.interface.get_object("dns_custom_input").get_text()
        elif dns_combobox.get_active() == 2:
            dns_leak_protection = 0
        
        cli.set_dns_protection(gui_enabled=True, dns_settings=(dns_leak_protection, custom_dns))

    def update_pvpn_plan_button_clicked(self, button):
        """Button/Event handler to update ProtonVPN Plan  
        """
        protonvpn_plan = 0
        protonvpn_plans = {
            1: self.interface.get_object("member_free_update_checkbox").get_active(),
            2: self.interface.get_object("member_basic_update_checkbox").get_active(),
            3: self.interface.get_object("member_plus_update_checkbox").get_active(),
            4: self.interface.get_object("member_visionary_update_checkbox").get_active()
        }

        for k,v in protonvpn_plans.items():
            if v == True:
                protonvpn_plan = int(k)
                break
            
        cli.set_protonvpn_tier(write=True, gui_enabled=True, tier=protonvpn_plan)
        print("[!]Refreshing server list")
        load_on_start(self.interface)        
        print("[!]Done")

    def update_def_protocol_button_clicked(self, button):
        """Button/Event handler to update OpenVP Protocol  
        """
        openvpn_protocol = 'tcp' if self.interface.get_object('protocol_tcp_update_checkbox').get_active() == True else 'udp'
        
        cli.set_default_protocol(write=True, gui_enabled=True, protoc=openvpn_protocol)

    # Kill Switch
    def killswitch_combobox_changed(self, combobox):
        """Event handler that reactes when the combobox value changes
        - If killswitch is enabled, then it disables the split tunneling input and button
        """
        if combobox.get_active() == 0:
            self.interface.get_object("split_tunneling_textview").set_property('sensitive', True)
            self.interface.get_object("update_split_tunneling_button").set_property('sensitive', True)
        else:
            self.interface.get_object("split_tunneling_textview").set_property('sensitive', False)
            self.interface.get_object("update_split_tunneling_button").set_property('sensitive', False)

    def update_killswtich_button_clicked(self, button):
        """Button/Event handler to update Killswitch  
        """
        ks_combobox = self.interface.get_object("killswitch_combobox")

        cli.set_killswitch(gui_enabled=True, user_choice=ks_combobox.get_active())

    # To-do Start on boot

    def update_split_tunneling_button_clicked(self, button):
        """Button/Event handler to update Split Tunneling 
        """
        split_tunneling_buffer = self.interface.get_object("split_tunneling_textview").get_buffer()

        # Get text takes a start_iter, end_iter and the buffer itself as last param
        split_tunneling_content = split_tunneling_buffer.get_text(split_tunneling_buffer.get_start_iter(), split_tunneling_buffer.get_end_iter(), split_tunneling_buffer)
        
        # Split IP/CIDR by either ";" and/or "\n"
        split_tunneling_content = re.split('[;\n]', split_tunneling_content)

        # Remove empty spaces
        split_tunneling_content = [content.strip() for content in split_tunneling_content]

        # Remove empty list elements
        split_tunneling_content = list(filter(None, split_tunneling_content))

        cli.set_split_tunnel(gui_enabled=True, user_data=split_tunneling_content)


    def purge_configurations_button_clicked(self, button):
            """Button/Event handler to purge configurations
            """
            # To-do: Confirm prior to allowing user to do this
            cli.purge_configuration(gui_enabled=True)

def initialize_gui():
    """Initializes the GUI 
    ---
    If user has not initialized a profile, the GUI will ask for the following data:
    - Username
    - Password
    - Plan
    - Protocol

    sudo protonvpn-gui
    - Will start the GUI without invoking cli()
    """
    check_root()

    interface = Gtk.Builder()

    posixPath = pathlib.PurePath(pathlib.Path(__file__).parent.absolute().joinpath("resources/main.glade"))
    glade_path = ''
    
    for path in posixPath.parts:
        if path == '/':
            glade_path = glade_path + path
        else:
            glade_path = glade_path + path + "/"

            
    interface.add_from_file(glade_path[:-1])

    interface.connect_signals(Handler(interface))

    if not os.path.isfile(CONFIG_FILE):
        window = interface.get_object("LoginWindow")
        dashboard = interface.get_object("Dashboard")
        dashboard.connect("destroy", Gtk.main_quit)
    else:
        window = interface.get_object("Dashboard")
        window.connect("destroy", Gtk.main_quit)
        load_on_start(interface)
    
    window.show()
    
    # Gdk.threads_init()
    # Gdk.threads_enter()
    GObject.threads_init()
    Gtk.main()
    # Gdk.threads_leave()
    
