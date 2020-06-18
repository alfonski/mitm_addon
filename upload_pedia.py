from mitmproxy import ctx
import mitmproxy
import json
import time, sys


class UploadPedia:

    def __init__(self):
        self.enable = False

    def request(self, flow):
        if not self.enable:
            return
        url = flow.request.pretty_url
        matcher = "upedia.tokopedia.net"
        if matcher in url:
            flow.request.host = "13.228.97.64"
            print("HOST: " + flow.request.host)
            # print("Throttling request")
            # animation = "|/-\\"
            # for i in range(65):
            #     time.sleep(1)
            #     sys.stdout.write("\r" + animation[i % len(animation)] + " " + str(i))
            #     sys.stdout.flush()
            # print("")
            # print("Continue rerquest...")

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if not self.enable:
            return


addons = [
    UploadPedia()
]

