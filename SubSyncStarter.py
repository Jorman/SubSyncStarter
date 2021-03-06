import os
import sys
import logging
import subprocess
import configparser


reference_file = sys.argv[1]
sub_file = sys.argv[2]
sub_code2 = sys.argv[3]
sub_code3 = sys.argv[4]
bad_file = os.path.splitext(reference_file)[0] + '.bad'
subsyncstarter_path = os.path.dirname(sys.argv[0])

config = configparser.ConfigParser()
config.read(os.path.join(subsyncstarter_path,'config.ini'))
loglevel_starter = config['General']['LoggingLevel']
logfile_starter = config['General']['Logfile']
location_subsync = config['SubSync']['Location']
loglevel_subsync = config['SubSync']['LoggingLevel']
logfile_subsync = config['SubSync']['Logfile']
effort = config['SubSync']['Effort']
window_size = config['SubSync']['WindowSize']
max_point_dist = config['SubSync']['MaxPointDistance']

command = "/snap/bin/subsync --cli --verbose " + loglevel_subsync + " --logfile '" + logfile_subsync + "' --window-size " + window_size + " --max-point-dist " + max_point_dist + " sync --sub '" + sub_file + "' --ref '" + reference_file + "' --out '" + sub_file + "' --effort " + effort +" --overwrite"

logging.root.handlers = []
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, handlers=[logging.FileHandler(logfile_starter, encoding="utf-8"),logging.StreamHandler()])
log = logging.getLogger()

log.debug('Reference file: %s' % reference_file)
log.debug('Subtitles file: %s' % sub_file)
log.debug('Subtitles code (2): %s' % sub_code2)
log.debug('Subtitles code (3): %s' % sub_code3)

log.info('Starting synchronization of subtitles file: %s' % sub_file)
log.debug('Running command: %s' % command)

try:
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    output = output.decode('utf-8')
    output_list = output.splitlines()
    for outputs in output_list:
        log.debug('Output: %s' % outputs)
    log.debug('Error: %s' % err)
    log.debug('Exit code: %s' % p_status)
    if "[+] done" in output_list[-1]:
        if os.path.isfile(bad_file):
            os.remove(bad_file)
        log.info('Sync succesful')
        print('Sync succesful')
    else:
        os.remove(sub_file)
        log.warning('Sync failed - wrong subs')
        print('Sync failed - wrong subs')
except:
    os.remove(sub_file)
    log.exception('Sync failed - exception')
    print('Sync failed - exception')