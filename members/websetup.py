"""Setup the members.afpy.org application"""
import logging

from members.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup members here"""
    load_environment(conf.global_conf, conf.local_conf)
