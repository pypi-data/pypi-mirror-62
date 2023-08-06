#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import shutil
import glob

try:
    from tools import *
    from log import logger
except:
    from yoctools.tools import *
    from yoctools.log import logger


class HardwareInfo:
    def __init__(self, dic):
        self.cpu_id = ''
        self.vendor_name = ''
        self.cpu_name = ''
        self.arch_name = ''
        self.chip_name = ''
        self.board_name = ''
        self.ld_script = ''

        self.cpu_list = {}

        for k, v in dic.items():
            if k in ['cpu_id', 'cpu_name', 'arch_name', 'chip_name', 'vendor_name', 'board_name', 'ld_script'] and v:
                self.__dict__[k] = v
            else:
                if type(v) == dict:
                    self.cpu_list[k] = v

    def __str__(self):
        text = ''
        for k, v in self.__dict__.items():
            if text:
                text += ', '
            text += k + ': ' + str(v)
        return text


class build_config:
    def __init__(self, dic):
        self.include = []
        self.internal_include = []
        self.libs = []
        self.libpath = []
        self.cflag = ''
        self.cxxflag = ''
        self.asmflag = ''
        self.ldflag = ''
        self.define = ''

        for k, v in dic.items():
            if v:
                self.__dict__[k] = v

class Package(object):
    def __init__(self, filename):
        self.name = ''
        self.description = ''
        self.type = ''
        self.keywords = {}
        self.author = ''
        self.license = ''
        self.homepage = ''
        self.yoc_version = ''
        self.depends = {}
        self.build_config = build_config({})
        self.defconfig = {}
        self.source_file = []
        self.install = []
        self.hw_info = HardwareInfo({})

        self.load(filename)

    def load(self, filename):
        conf = yaml_load(filename)

        for k, v in conf.items():
            if v:
                if k == 'build_config':
                    v = build_config(v)
                if k in ['board', 'chip', 'solution', 'hw_info']:
                    self.__dict__['hw_info'] = HardwareInfo(v)
                else:
                    self.__dict__[k] = v
                if k == 'lib':
                    self.__dict__['libs'] = v

        if self.type in ['board', 'chip', 'solution']:
            if self.type not in conf and 'hw_info' not in conf:
                logger.error('%s component must set `%s` field' % (filename, self.type))
                exit(-1)

        if not self.name:
            logger.error('%s `name` cannot be empty!' % filename)
            exit(-1)

        if self.type not in ['solution', 'common', 'board', 'chip']:
            logger.error('%s `type` must be "solution" or "common" or "board" or "chip".' % filename)
            exit(-1)

    def show(self):
        for k, v in self.__dict__.items():
            if not v:
                continue
            if k in ['build_config']:
                print(k)
                for kk, vv, in v.__dict__.items():
                    print("  ", kk, ":", vv)
            elif k in ['defconfig']:
                print(k)
                for k1, v1 in v.items():
                    print("  ", k1, ":", v1)
            else:
                print(k, str(v))


def package_test():
    p = Package('../solutions/helloworld/package.yaml')
    # p = Package('../solutions/chip_test_hobbit4_e902/package.yaml')
    # p = Package('../components/chip-hobbit4_e902/package.yaml')
    p = Package('../components/aos/package.yaml')
    # p = Package('../components/chip_pangu/package.yaml')
    # p = Package('package.yaml')
    p.show()


if __name__ == "__main__":
    package_test()
