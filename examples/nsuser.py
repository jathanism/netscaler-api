#!/usr/bin/env python

import netscaler
import os

class IllegalName(netscaler.InteractionError): pass

class UserAdmin(netscaler.API):
    def is_safe(self, username):
        """Returns False for names containing 'root' or starting with 'ns'."""
        if 'root' in username or username.startswith('ns'):
            return False
        return True

    def add_user(self, username, password):
        """Custom user adder that won't allow unsafe names"""
        if not self.is_safe(username):
            raise IllegalName(username)

        try:
            resp = self.run("addsystemuser", username=username, password=password})
            return True
        except netscaler.InteractionError, err:
            return False

    def del_user(self, username):
        """Custom user remover that protects usernames"""
        if not self.is_safe(username):
            raise IllegalName(username)

        try:
            resp = self.run("rmsystemuser", username=username)
            return True
        except netscaler.InteractionError, err:
            return False

    def user_exists(self, username):
        """Returns True if user exists."""
        try:
            resp = self.run("getsystemuser", username=username)
            return True
        except netscaler.InteractionError, err:
            return False


if __name__ == '__main__':

    netscaler.DEBUG = True

    cwd = os.getcwd()

    wsdl_url = 'file://%s/NSUserAdmin.wsdl' % cwd
    username = password = 'nsroot'
    host = 'netscaler'

    api = UserAdmin(host, username=username, password=password, wsdl_url=wsdl_url, cache=None)

    api.login()
    print 'logged in:', api.logged_in
    print 'autosave? ', api.autosave
    print

    users = ('jathan', 'dynasty', 'john')

    for user in users:
        print 'checking', user
        if api.user_exists(user):
            print user, 'exists.'
            print 'deleting', user
            api.del_user(user)
            print

        else:
            # add a user with matching password
            print user, 'no exists.'
            if api.add_user(user, user):
                print user, 'added!'
                print
            

