import argparse

import libs.log as log
from http_ops import Initialize
from utils.test_desc import AddTestInfo
from utils.utils import get_calamari_config


class Test(Initialize):
    def __init__(self, **config):
        super(Test, self).__init__(**config)

        assert self.http_request.getfsid(), "failed to get fsid"

        self.url = (
            self.http_request.base_url
            + "cluster"
            + "/"
            + str(self.http_request.fsid)
            + "/"
            + "server"
        )

        self.url2 = self.http_request.base_url + "server"


def exec_test1(config_data):
    add_test_info = AddTestInfo(
        15.1,
        "\napi/v2/cluster/<fsid>/server\n" "\napi/v2/cluster/<fsid>/server/<fqdn>\n",
    )

    add_test_info.started_info()

    try:
        test = Test(**config_data)

        cleaned_response = test.get(test.url)

        ids = [k["fqdn"] for k in cleaned_response]

        get_server_by_ids = lambda x: test.get(test.url + "/" + x)

        map(get_server_by_ids, ids)

        add_test_info.success("test ok")

    except AssertionError, e:
        log.error(e)
        add_test_info.failed("test error")

    return add_test_info.completed_info(config_data["log_copy_location"])


def exec_test2(config_data):
    add_test_info = AddTestInfo(
        15.2, "\napi/v2/server" "api/v2/server/<fqdn>\n" "api/v2/server/<fqdn>/grains"
    )

    add_test_info.started_info()

    try:
        test = Test(**config_data)

        cleaned_response = test.get(test.url2)

        fqdns = [k["fqdn"] for k in cleaned_response]

        get_server_by_ids = lambda x: test.get(test.url + "/" + x)

        map(get_server_by_ids, fqdns)

        get_server_by_grains = lambda x: test.get(test.url + "/" + x + "/" + "grains")

        map(get_server_by_grains, fqdns)

        add_test_info.success("test ok")

    except AssertionError, e:
        log.error(e)
        add_test_info.failed("test error")

    return add_test_info.completed_info(config_data["log_copy_location"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calamari API Automation")

    parser.add_argument(
        "-c",
        dest="config",
        default="config.yaml",
        help="calamari config file: yaml file",
    )

    args = parser.parse_args()

    calamari_config = get_calamari_config(args.config)

    exec_test1(calamari_config)
    exec_test2(calamari_config)
