'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import re
from enum import Enum, auto

class ConfigPropertyType(Enum):
	ARO = auto()
	ACO = auto()
	URO = auto()
	UCO = auto()

class CliArgsConfig:
    ARJ_PATTERN = re.compile("(?i)(aro|aco)\\s*:\\s*(\\S+)\\s*")
    USER_PATTERN = re.compile("(?i)(uro|uco)\\s*:\\s*(\\S+)\\s*")

    def __init__(self, options):
        self.__arj_options_map = {
            ConfigPropertyType.ARO : dict(),
            ConfigPropertyType.ACO : dict()
        }
        self.__user_options_map = {
            ConfigPropertyType.URO : dict(),
            ConfigPropertyType.UCO : dict()
        }

        for option in options:
            m = CliArgsConfig.ARJ_PATTERN.match(option.name)
            if m is not None:
                c_type = ConfigPropertyType[m.group(1).upper()]
                try:
                    arj_prop = m.group(2)
                except:
                    raise Exception("Empty Arjuna Option Key provided in CLI: {}".format(option.name))
                else:
                    try:
                        arj_option = Arjuna.normalise_arjuna_option(arj_prop)
                    except:
                        raise Exception("You have provided an invalid Arjuna Option in CLI: {}".format(option.name))
                    else:
                        self.__arj_options_map[c_type][arj_option] = option.value
                        continue

            m = CliArgsConfig.USER_PATTERN.match(option.name)
            if m is not None:
                c_type = ConfigPropertyType[m.group(1).upper()]
                try:
                    user_option = Arjuna.normalise_user_option(m.group(2))
                except:
                    raise Exception("Empty User Option key provided in CLI: {}".format(option.name))
                else:
                    self.__arj_options_map[c_type][user_option] = option.value
                    continue

    def as_map(self):
        map = dict()
        map["arjuna_reference_options"] = self.__get_arjuna_reference_options()
        map["arjuna_custom_options"] = self.__get_arjuna_custom_options()
        map["user_reference_options"] = self.__get_user_reference_options()
        map["user_reference_options"] = self.__get_user_custom_options()

    def __get_arjuna_reference_options(self):
        return self.__arj_options_map[ConfigPropertyType.ARO]

    def __get_arjuna_custom_options(self):
        return self.__arj_options_map[ConfigPropertyType.ACO]

    def __get_user_reference_options(self):
        return self.__arj_options_map[ConfigPropertyType.URO]

    def __get_user_custom_options(self):
        return self.__arj_options_map[ConfigPropertyType.UCO]


#### From old Setu code
from arjuna.core.enums import *
from arjuna.core.value import Value


class ROWrapper:

    def __init__(self, config):
        self.__config = config

    def value(self, option):
        return self.__config.value(option)


class Configuration:

    def __init__(self, test_session, name, config):
        super().__init__()
        self.__session = test_session
        self.__name = name
        self.__wrapped_config = config
        self.__arjuna_options = ROWrapper(self.__wrapped_config.arjuna_config)
        self.__user_options = ROWrapper(self.__wrapped_config.user_config)

    @property
    def _wrapped_config(self):
        return self.__wrapped_config

    @property
    def test_session(self):
        return self.__session

    @property
    def arjuna_options(self):
        return self.__arjuna_options

    @property
    def user_options(self):
        return self.__user_options

    def get_arjuna_options_as_map(self):
        return self.__wrapped_config.arjuna_config.as_json_dict()

    def is_arjuna_option_not_set(self, option):
        return self.__wrapped_config.arjuna_config.is_not_set(option)

    @property
    def name(self):
        return self.__name

    @property
    def guiauto_context(self):
        return self.arjuna_options.value(ArjunaOption.GUIAUTO_CONTEXT) # .as_enum(GuiAutomationContext)

    @property
    def locale(self):
        return self.arjuna_options.value(ArjunaOption.LOCALE) # .as_enum(GuiAutomationContext)

    @property
    def browser_name(self):
        return self.arjuna_options.value(ArjunaOption.BROWSER_NAME) #.as_enum(BrowserName)

    @property
    def browser_version(self):
        return self.arjuna_options.value(ArjunaOption.BROWSER_VERSION)

    @property
    def browser_binary_path(self):
        return self.arjuna_options.value(ArjunaOption.BROWSER_BIN_PATH)

    @property
    def test_run_env_name(self):
        return self.arjuna_options.value(ArjunaOption.TESTRUN_ENVIRONMENT)

    @property
    def screenshots_dir(self):
        return self.arjuna_options.value(ArjunaOption.PROJECT_RUN_SCREENSHOTS_DIR)

    @property
    def log_dir(self):
        return self.arjuna_options.value(ArjunaOption.LOG_DIR)

    @property
    def guiauto_max_wait(self):
        return self.arjuna_options.value(ArjunaOption.GUIAUTO_MAX_WAIT)

    def as_map(self):
        return self.__wrapped_config.as_json_dict()

class CliArgsConfig:

    def __init__(self, arg_dict):
        self.__aco = {}
        self.__ato = {}
        self.__uco = {}
        self.__uto = {}

        kinds = {
            "aco": self.__aco,
            "ato": self.__ato,
            "uco": self.__uco,
            "uto": self.__uto
        }

        lower_actual_key_map = {i.lower():i for i in arg_dict}
        for kind in kinds:
            if kind in lower_actual_key_map:
                actual_key = lower_actual_key_map[kind]
                d_item = arg_dict[actual_key]
                if d_item:
                    for entry in d_item:
                        k,v = entry
                        kinds[kind][k.lower()] = v
                del arg_dict[actual_key]

        for akey, avalue in arg_dict.items():
            self.__aco[akey.lower()] = avalue

    def as_map(self):
        return {
            "arjunaCentralOptions": self.__aco,
            "arjunaTestOptions": self.__ato,
            "userCentralOptions": self.__uco,
            "userTestOptions": self.__uto
        }
