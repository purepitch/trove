#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ######################################################################
# 
# Program:   password.py
#
# Objective: Secure handling of passwords via bcrypt encrypted file
#            that can be stored in a central repository.
#            A master passphrase is needed to get access to the
#            passwords.
#
# Author(s): A. D. Gerdes (gerdes@rrzn.uni-hannover.de)
# 
# 
# ######################################################################

import sys
import re
import os
import getpass
from optparse import OptionParser
from subprocess import Popen, PIPE
import hashlib
import datetime


class ListEntry:
    def __init__(self):
        self.eid = ""
        self.name = ""
        self.user = ""
        self.passwd = ""
        self.helptext = ""
        self.description = ""


def print_entry(entry, printid,  printuser, printpasswd, printhelp,
                printdescr):
    print 80 * "-"
    if printid == True:
        fillnum = 80 - (len(entry.name) + 2 + 15)
        print "[" + entry.name + "]" + fillnum * " " + entry.eid[0:15]
    else:
        print "[" + entry.name + "]"
    if printuser == True:
        print 'User:   ', entry.user
    if printpasswd == True:
        print 'Passwd: ', entry.passwd
    if printhelp == True:
        print 'Help:   ', entry.helptext
    if printdescr == True:
        print 'Desc:   ', entry.description


def calculate_hash(entry):
    return hashlib.sha1(entry.name + entry.user + entry.passwd +
                        entry.helptext).hexdigest()

def encrypt_file(filename, passwd):
    f = open(os.devnull, 'w')
    encrypt = Popen(['bcrypt',filename], stdin=PIPE, stdout=f, stderr=f)
    encrypt.stdin.write(passwd + "\n" + passwd + "\n")
    encrypt.wait()
    f.close()


def decrypt_file(filename,passwd):
    f = open(os.devnull, 'w')
    decrypt = Popen(['bcrypt',filename], stdin=PIPE, stdout=f, stderr=f)
    decrypt.stdin.write(passwd + "\n")
    decrypt.wait()
    f.close()


def extract_entries(filecontent):
    mylist = []
    myentry = ListEntry()
    for linenumber in range(len(filecontent)):
        line = filecontent[linenumber].strip()
        if (re.search('^\[', line) and re.search('\]$', line)):
            if myentry.name == "":
                pass
            else:
                myentry.eid = calculate_hash(myentry)
                mylist.append(myentry)
                del myentry
                myentry = ListEntry()
            myentry.name = line.rstrip(']').lstrip('[')
        elif line.split(':')[0] == 'user':
            myentry.user = line.split(':',1)[1].strip()
        elif line.split(':')[0] == 'passwd':
            myentry.passwd = line.split(':',1)[1].strip()
        elif line.split(':')[0] == 'help':
            myentry.helptext = line.split(':',1)[1].strip()
        elif line.split(':')[0] == 'description':
            myentry.description = line.split(':',1)[1].strip()
        if (linenumber == (len(filecontent) - 1)):
            myentry.eid = calculate_hash(myentry)
            mylist.append(myentry)
        else:
            continue
    return mylist


def add_entry(passwdlist):
    newentry = ListEntry()
    newentry.name =  raw_input("Name of computer or website: ")
    newentry.user =  raw_input("Username: ")
    newentry.passwd =  raw_input("Password: ")
    newentry.helptext =  raw_input("Help text (mnemonic): ")
    newentry.description =  raw_input("Additional description: ")
    newentry.eid = calculate_hash(newentry)
    passwdlist.append(newentry)
    print_entry(newentry,True, True, True, True,True)
    return passwdlist


def del_entry(passwdlist, entryid):
    newpasswdlist = []
    entrydeleted = False
    for entry in passwdlist:
        if re.search(entryid, entry.eid):
            print "[csspw] Entry '" + entryid + "' will be deleted."
            decision = raw_input("Are you sure? (y/N) ")
            if decision == "y":
                entrydeleted = True
            else:
                newpasswdlist.append(entry)
                print "[csspw] No entry deleted."
        else:
            newpasswdlist.append(entry)
    if (entrydeleted == False):
        print "[csspw] Warning: EID not found in file. No entry deleted."
    return newpasswdlist


def edit_entry(passwdlist, entryid):
    editpasswdlist = []
    entryedit = False
    for entry in passwdlist:
        if re.search(entryid, entry.eid):
            name = raw_input("Name ["+ entry.name + "]: ")
            if name == "":
                pass
            else:
                entry.name = name
            user =  raw_input("User [" + entry.user + "]: ")
            if user == "":
                pass
            else:
                entry.user = user
            password =  raw_input("Password [" + entry.passwd + "]: ")
            if password == "":
                pass
            else:
                entry.passwd = password
            helptext =  raw_input("Help [" + entry.helptext + "]: ")
            if helptext == "":
                pass
            else:
                entry.helptext = helptext
            description =  raw_input("Descr [" + entry.description + "]: ")
            if description == "":
                pass
            else:
                entry.description = description
            entry.eid = calculate_hash(entry)
            print_entry(entry,True, True, True, True,True)
            entryedit = True
        editpasswdlist.append(entry)
    if (entryedit == False):
        print "[csspw] Warning: EID not found in file. No entry to edit."
    return editpasswdlist

def search_entries(passwdlist, key, passwordsearch):
    match = False
    resultlist = []
    if (passwordsearch == True):
        for entry in passwdlist:
            if re.search(key, entry.passwd):
                match = True
                resultlist.append(entry)
    else:
        for entry in passwdlist:
            if re.search(key.lower(), (entry.name).lower()):
                match = True
                resultlist.append(entry)
    return resultlist, match


if __name__ == "__main__":
    # Parse command line arguments:
    parser = OptionParser()
    parser.usage = "%prog [options] [search string]"
    parser.add_option("-a", "--add", dest="add",
                      default=False, action="store_true",
                      help="add entry to list")
    parser.add_option("-d", "--del", dest="delete",
                      default=False, action="store_true",
                      help="delete entry from list")
    parser.add_option("--desc", dest="printdescription",
                      default=False, action="store_true",
                      help="print server description if available")
    parser.add_option("-e", "--edit", dest="edit",
                      default=False, action="store_true",
                      help="edit entry")
    parser.add_option("-f", "--file", dest="filename",
                      default= sys.path[0] + "/rrzn.pwd.bfe", metavar="FILE",
                      help="encrypted password file to use [rrzn.pwd.bfe]")
    parser.add_option("--hint", dest="printhelp", default=True,
                      help="print help text to remember password",
                      action="store_true")
    parser.add_option("--list-all", dest="listall",
                      default=False, action="store_true",
                      help="list all server names")
    parser.add_option("--no-id", dest="printid",
                      default=True, action="store_false",
                      help="do not print entry ID")
    parser.add_option("-p", "--password", dest="passwordsearch",
                      default=False, action="store_true",
                      help="list all entries with search string in passwd field")
    (options, args) = parser.parse_args()

    # Say hello:
    print "This is csspw - A password management program"

    # Check if positional argument is there
    if (len(args) == 0 and \
            not (options.add or options.delete or options.edit \
                 or options.listall)):
        print "\nYou must either specify a search string"
        print "or give one of the options: '-a', '-d' or '-e'\n\n"
        parser.print_help()
        sys.exit(1)

    if len(args) > 1:
        print "\nYou have specified more than one positional argument."
        print "Only the first word will be used for the search.\n\n"

    passwdfile = options.filename.rstrip('.bfe')
    # print "DEBUG: ", passwdfile
    # Ask for passphrase
    masterpwd = getpass.getpass('[csspw] Please enter master passphrase: ')

    # Decrypt password file using subprocess:
    decrypt_file(options.filename, masterpwd)
    if os.path.isfile(passwdfile):
        size_of_passwdfile = os.path.getsize(passwdfile)
    else:
		size_of_passwdfile = 0

    # Read password text file
    if os.path.isfile(passwdfile) and size_of_passwdfile > 0:
        pwdfile = open(passwdfile, 'r')
        pwdfilelines = pwdfile.readlines()
        pwdfile.close()
    else:
        print "[csspw] The file " + passwdfile
        print "[csspw] could not be found or it is empty." 
        print "[csspw] That means the passphrase was probably wrong"
        print "[csspw] and the password file was not decrypted."
        print "[csspw] Terminating."
        os.system("rm -f " + passwdfile)
        sys.exit(2)

    # Encrypt password file again:
    encrypt_file(passwdfile, masterpwd)

    # Dive through file content and fill entry list
    # This will be a list of ListEntry objects (see class above)
    entrylist = extract_entries(pwdfilelines)
    entrylist = sorted(entrylist, key=lambda entry: entry.name.lower())
    print "[csspw] Found total number of " + str(len(entrylist)) + " entries."

    if options.add == True:
        mypasswdlist = add_entry(entrylist)
        nf = open(passwdfile, 'w')
        nf.write("# Auto generated passwd list by password.py\n")
        nf.write("# Date: " + str(datetime.datetime.now()) + "\n\n")
        for entry in mypasswdlist:
            nf.write("[" + entry.name + "]\n")
            nf.write("user: " + entry.user + "\n")
            nf.write("passwd: " + entry.passwd + "\n")
            nf.write("help: " + entry.helptext + "\n")
            nf.write("description: " + entry.description + "\n\n")
        nf.close()
        os.system("rm -f " + options.filename)
        encrypt_file(passwdfile, masterpwd)

    elif options.edit == True:
        eid = raw_input("Entry ID: ")
        mypasswdlist = edit_entry(entrylist, eid)
        ef = open(passwdfile, 'w')
        ef.write("# Auto generated passwd list by password.py\n")
        ef.write("# Date: " + str(datetime.datetime.now()) + "\n\n")
        for entry in mypasswdlist:
            ef.write("[" + entry.name + "]\n")
            ef.write("user: " + entry.user + "\n")
            ef.write("passwd: " + entry.passwd + "\n")
            ef.write("help: " + entry.helptext + "\n")
            ef.write("description: " + entry.description + "\n\n")
        ef.close()
        os.system("rm -f " + options.filename)
        encrypt_file(passwdfile, masterpwd)

    elif options.delete == True:
        if ( len(sys.argv) == 3 ):
            eid = sys.argv[2]
        else:
            eid = raw_input("Entry ID: ")
        mypasswdlist = del_entry(entrylist, eid)
        nf = open(passwdfile, 'w')
        nf.write("# Auto generated passwd list by password.py\n")
        nf.write("# Date: " + str(datetime.datetime.now()) + "\n\n")
        for entry in mypasswdlist:
            nf.write("[" + entry.name + "]\n")
            nf.write("user: " + entry.user + "\n")
            nf.write("passwd: " + entry.passwd + "\n")
            nf.write("help: " + entry.helptext + "\n")
            nf.write("description: " + entry.description + "\n\n")
        nf.close()
        os.system("rm -f " + options.filename)
        encrypt_file(passwdfile, masterpwd)

    elif options.listall == True:
        for entry in entrylist:
            print_entry(entry,True, False, False, False,False)
        print 80 * "-"

    else:
    # Search server / entry  names for search string:
    # (compare lower case representations)
        searchstring = args[0]
        resultlist, success = search_entries(entrylist, searchstring,
                                             options.passwordsearch)
        if (success == True):
            print "[csspw] Found " + str(len(resultlist)) + " result(s) for " \
                  + searchstring + "."
            for entry in resultlist:
                print_entry(entry,options.printid, True, True,
                            options.printhelp, options.printdescription)
            print 80 * "-"
        else:
            print "[csspw] No lowercase match in entry names."

    print "[csspw] Terminating."

# vim: expandtab tabstop=4 shiftwidth=4:
