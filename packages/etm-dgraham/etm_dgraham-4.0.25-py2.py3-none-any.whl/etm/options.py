import os
import sys
from ruamel.yaml import YAML
import logging
import logging.config
logger = logging.getLogger()
import string
import random
from copy import deepcopy

yaml = YAML()  

def randomString(stringLength=10):
    """Generate a random string with the combination of lowercase and uppercase letters and digits """

    letters = string.ascii_letters + 2*'0123456789' 
    return ''.join(random.choice(letters) for i in range(stringLength))


class Settings():

    inp = """\
################# IMPORTANT #############################
#
# Changes to this file only take effect when etm is next
# restarted.
#
#########################################################

# ampm: true or false. Use AM/PM format for datetimes if true 
# else use 24 hour format. 
ampm: true

# locale: A two character locale abbreviation. E.g., "fr" for 
# French.
locale: en

# style: dark or light. Designed for, respectively, dark or 
# light terminal backgounds. Some output may not be visible
# unless this is set correctly for your display.
style: dark
""" + f"""\

# secret: A string to use as the secret_key for @m masked 
# entries. In etm versions after 4.0.21, the default string 
# is randomly generated when this file is first created and 
# should be unique for each etm installation. WARNING: if 
# you change this key, any @m entries that you made before 
# the change will be unreadable after the change. 
secret: {randomString(10)}
""" + """\

# omit_extent: A list of calendars. Events with @c entries
# belonging to this list will only have their starting times
# displayed in agenda view and will neither appear nor cause
# conflicts in busy view.
omit_extent:
    - omit

# keep_current: true or false. If true, the agenda for the  
# current and following two weeks will be written to "current.txt" 
# in your etm home directory and updated when necessary. You 
# could, for example, create a link to this file in a pCloud or 
# DropBox folder and have access to your current schedule on 
# your mobile device.
keep_current: false

# archive_after: A non-negative integer. If zero, do not 
# archive items. If positive, finished tasks and events with 
# last datetimes falling more than this number of years 
# before the current date will automatically be archived on a 
# daily basis.  Archived items are moved from the "items" 
# folder in the database to the "archive" folder and no 
# longer appear in normal views. Note that unfinished tasks 
# and records are not archived.
archive_after: 0

# num_finished: A non-negative integer. If positive, when 
# saving retain only the most recent 'num_finished' 
# completions of an infinitely repeating task, i.e., repeating 
# without an "&c" count or an "&u" until attribute. If zero or 
# not infinitely repeating, save all completions.
num_finished: 0

# usedtime_minutes: Round used times up to the nearest 
# usedtime_minutes in used time views. Possible choices are 1, 
# 6, 12, 30 and 60. With 1, no rounding is done and times are 
# reported as hours and minutes. Otherwise, the prescribed 
# rounding is done and times are reported as floating point 
# hours. Note that each "@u" timeperiod is rounded before 
# aggregation.
usedtime_minutes: 1

# alerts: A dictionary with single-character, "alert" keys and 
# corresponding "system command" values. Note that characters 
# "t" (text message) and "e" (email) are already used.  The 
# "system command" string should be a comand with any 
# applicable arguments that could be run in a terminal.
# Properties of the item triggering the alert can be included 
# in the command arguments using the syntax '{property}', e.g., 
# {summary} in the command string would be replaced by the 
# summary of the item. Similarly {start} by the starting time, 
# {when} by the time remaining until the starting time, 
# {location} by the @l entry and {description} by the @d entry. 
# E.g., If the event "* sales meeting @s 2019-02-12 3p" 
# triggered an alert 30 minutes before the starting time the 
# string "{summary} {when}" would expand to "sales meeting in 
# 30 minutes". E.g. on my macbook
# 
#    alerts:
#        v:   /usr/bin/say -v "Alex" "{summary}, {when}"
#        ...
#
# would make the alert 'v' use the builtin text to speech sytem 
# to speak the item's summary followed by a slight pause 
# (the comma) and then the time remaining until the starting 
# time, e.g., "sales meeting, in 20 minutes" would be triggered
# by including "@a 20m: v" in the reminder.
alerts:

# expansions: A dictionary with 'expansion name' keys and 
# corresponding 'replacement string' values. E.g. with
#
#    expansions:
#        tennis: "@e 1h30m @a 30m: d @i personal:exercise" 
#        ...
#
# then when "@x tennis" is entered the popup completions for 
# "@x tennis" would offer replacement by the corresponding 
# "@e 1h30m @a 30m: d @i personal:exercise".
expansions:

# sms: Settings to send "t" (sms text message) alerts to the 
# list of phone numbers from the item's @n attendee 
# entries using the item's summary and the body as specified 
# in the template below as the message. E.g., suppose you 
# have a gmail account with email address "who457@gmail.com" 
# and want to text alerts to Verizon moble phone (123) 
# 456-7890. Then your sms entries should be
#     from:   who457@gmail.com
#     pw:     your gmail password
#     server: smtp.gmail.com:587
# and your item should include the following attendee entry
#     @n 1234567890@vzwpix.com
# In the illustrative phone number, @vzwpix.com is the mms 
# gateway for Verizon. Other common mms gateways are
#     AT&T:     @mms.att.net
#     Sprint:   @pm.sprint.com
#     T-Mobile: @tmomail.net
# Note. Google "mms gateway listing" for other alternatives.
sms:
    body:   "{location} {when}"
    from: 
    pw: 
    server: 

# smtp: Settings to send "e" (email message) alerts to the 
# list of email addresses from the item's @n attendee
# entries using the item's summary as the subject and body as 
# the message. E.g., if you have a gmail account with email 
# address "whatever457@gmail.com", then your entries should 
# be
#     from: whatever457@gmail.com
#     id: whatever457
#     pw: your gmail password
#     server: smtp.gmail.com
smtp:
    body: "{location} {when}\\n{description}"
    from: 
    id: 
    pw: 
    server: 
"""

    def __init__(self, etmdir):
        if os.path.isdir(etmdir):
            self.settings = yaml.load(Settings.inp)
            self.cfgfile = os.path.normpath(
                    os.path.join(etmdir, 'cfg.yaml'))
            if os.path.exists(self.cfgfile):
                with open(self.cfgfile, 'r') as fn:
                    self.user = yaml.load(fn)
                if self.user and isinstance(self.user, dict):
                    self.changes = self.check_options()
                else:
                    self.changes = [f'invalid settings from {self.cfgfile} - using defaults']
            else:
                self.changes = [f'missing {self.cfgfile} - using defaults']

            if self.changes:
                with open(self.cfgfile, 'w') as fn:
                    yaml.dump(self.settings, fn)
                logger.info(f"updated {self.cfgfile}: {', '.join(self.changes)}")
            else:
                logger.info(f"using settings from {self.cfgfile}")
        else:
            raise ValueError(f"{etmdir} is not a valid directory")


    def check_options(self):
        changed = []
        new = deepcopy(self.user)
        # add missing default keys
        for key, value in self.settings.items():
            if isinstance(self.settings[key], dict):
                if key not in new or not isinstance(new[key], dict):
                    new[key] = self.settings[key]
                    changed.append(f"added {key}: self.settings[key]")
                else:
                    for k, v in self.settings[key].items():
                        if k not in new[key]:
                            new[key][k] = self.settings[key][k] 
                            changed.append(f"added {key}.{k}: {self.settings[key][k]}")
            elif key not in new:
                new[key] = self.settings[key]
                changed.append(f"added {key}: {self.settings[key]}")
        # remove invalid user keys
        for key, value in self.user.items():
            if key not in self.settings:
                # not a valid option
                del new[key]
                changed.append(f"removed {key}: {self.user[key]}")
            elif key in ['sms', 'smtp']:
                # only allow the specified subfields for these keys
                for k, v in self.user[key].items():
                    if k not in self.settings[key]:
                        changed.append(f"removed {key}.{k}: {new[key][k]}")
                        del new[key][k]

        for key, value in new.items():
            self.settings[key] = new[key]

        if self.settings['usedtime_minutes'] not in [1, 6, 12, 30, 60]:
            changed.append(f"{self.settings['usedtime_minutes']} is invalid for usedtime_minute. Using default value: 1.")
            self.settings['usedtime_minutes'] = 1 

        return changed


def setup_logging(level, etmdir, file=None):
    """
    Setup logging configuration. Override root:level in
    logging.yaml with default_level.
    """

    if not os.path.isdir(etmdir):
        return

    log_levels = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARN,
        4: logging.ERROR,
        5: logging.CRITICAL
    }

    level = int(level)
    if level in log_levels:
        loglevel = log_levels[level]
    else:
        loglevel = log_levels[3]

    # if we get here, we have an existing etmdir
    logfile = os.path.normpath(os.path.abspath(os.path.join(etmdir, "etm.log")))

    config = {'disable_existing_loggers': False,
              'formatters': {'simple': {
                  'format': '--- %(asctime)s - %(levelname)s - %(module)s.%(funcName)s\n    %(message)s'}},
              'handlers': {
                    'file': {
                        'backupCount': 5,
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'encoding': 'utf8',
                        'filename': logfile,
                        'formatter': 'simple',
                        'level': loglevel,
                        'when': 'midnight',
                        'interval': 1}
              },
              'loggers': {
                  'etmmv': {
                    'handlers': ['file'],
                    'level': loglevel,
                    'propagate': False}
              },
              'root': {
                  'handlers': ['file'],
                  'level': loglevel},
              'version': 1}
    logging.config.dictConfig(config)
    logger.critical("\n######## Initializing logging #########")
    if file:
        logger.critical(f'logging for file: {file}\n    logging at level: {loglevel}\n    logging to file: {logfile}')
    else:
        logger.critical(f'logging at level: {loglevel}\n    logging to file: {logfile}')

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        etmdir = sys.argv.pop(1)
    else:
        sys.exit("The etm path must be provided.")

    settings = Settings(etmdir)
    print(settings.settings, "\n")
    print(settings.changes, "\n")
    yaml.dump(settings.settings, sys.stdout)

