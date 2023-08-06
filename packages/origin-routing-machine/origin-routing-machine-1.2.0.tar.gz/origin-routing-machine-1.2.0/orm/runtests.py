import sys
import time
import re
from urllib.parse import urlparse
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def python_regex(orm_regex):
    return "^{}$".format(orm_regex)


def run_tests(tests, target, verify_certs=True):
    # pylint:disable=too-many-locals,too-many-branches,too-many-statements
    prev_file = ""
    for test in tests:
        if prev_file != test["_orm_source_file"]:
            print("# Run tests from: {}".format(test["_orm_source_file"]))
        prev_file = test["_orm_source_file"]
        name = test.get("name")
        url = test["request"]["url"]
        expect_status = test["expect"].get("status")
        expect_body = test["expect"].get("body", [])
        expect_headers = test["expect"].get("headers", [])
        expect_time_min = test["expect"].get("time_min")
        expect_time_max = test["expect"].get("time_max")
        print("  Test: {}".format(name))

        url_parsed = urlparse(url)
        do_target = "{scheme}://{netloc}{path}".format(
            scheme=url_parsed.scheme, netloc=target, path=url_parsed.path
        )

        if url_parsed.query:
            do_target = "{}?{}".format(do_target, url_parsed.query)
        if url_parsed.fragment:
            do_target = "{}#{}".format(do_target, url_parsed.fragment)

        headers = {"Host": url_parsed.netloc}
        print("    request.get: {}".format(do_target), end="")
        reqtime = time.time()
        r = requests.get(
            do_target, headers=headers, verify=verify_certs, allow_redirects=False
        )
        reqtime = time.time() - reqtime
        print(" [{:.3f}s]".format(reqtime))
        if expect_status:
            if r.status_code != expect_status:
                print(
                    "Got status code {}, expect {}".format(r.status_code, expect_status)
                )
                sys.exit(1)

        for b in expect_body:
            regex = python_regex(b["regex"])
            if not re.search(regex, r.text, flags=re.MULTILINE):
                print("Body did not match {}".format(regex))
                print("Body:\n{}".format(r.text))
                sys.exit(1)

        for h in expect_headers:
            # Make sure that all expected headers are there
            if h["field"] not in r.headers:
                print("Header {} not found".format(h["field"]))
                sys.exit(1)

            # Check that the expected header contains the correct data
            for header in expect_headers:
                hf = header["field"]
                hr = python_regex(header["regex"])
                if not re.search(hr, r.headers.get(hf)):
                    print(
                        "Header {} contains {}, expected {}".format(
                            hf, r.headers.get(hf), hr
                        )
                    )
                    sys.exit(1)
        if expect_time_min:
            if reqtime < expect_time_min:
                print(
                    "Request time (t) was {}s, expected >= {}s.".format(
                        reqtime, expect_time_min
                    )
                )
                sys.exit(1)
        if expect_time_max:
            if reqtime > expect_time_max:
                print(
                    "Request time (t) was {}s, expected <= {}s.".format(
                        reqtime, expect_time_max
                    )
                )
                sys.exit(1)
        print()
