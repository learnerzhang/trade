import configparser


class ConfigUtils:
    config = configparser.ConfigParser()
    config.read('confs/test_tv.cfg')

    @classmethod
    def get_section(cls, section, key):
        if section in cls.config.sections():
            if key in cls.config[section]:
                return cls.config[section][key]
        return 

    @classmethod
    def get_stock(cls, key):
        return cls.get_section("STOCK", key)

    @classmethod
    def get_redis(cls, key):
        return cls.get_section("REDIS", key)

    @classmethod
    def get_mysql(cls, key):
        return cls.get_section("MYSQL", key)

    @classmethod
    def get_flask(cls, key):
        return cls.get_section("FLASK", key)

    @classmethod
    def get_model(cls, key):
        return cls.get_section("MODEL", key)


if __name__ == '__main__':
    print(ConfigUtils.get_stock("END_DATE"))

