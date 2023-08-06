# BOTLIB - Framework to program bots.
#
#

import lo
import logging

def __dir__():
    return ("User", "Users")

class User(lo.Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(lo.Db):

    cache = lo.Object()
    userhosts = lo.Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = self.userhosts.get(origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        logging.error("denied %s" % origin)
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return self.all("mods.usr.User", s)

    def get_user(self, origin):
        if origin in Users.cache:
            return Users.cache[origin]
        u =  list(self.get_users(origin))
        if u:
            Users.cache[origin] = u[-1]
            return u[-1]
 
    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        user.save()
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        Users.cache[origin] = user
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user
