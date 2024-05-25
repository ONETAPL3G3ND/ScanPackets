from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
import asyncio
import logging
from mitmproxy.addonmanager import Loader


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RequestLogger:
    def load(self, loader: Loader):
        loader.add_option(
            name="listen_host", typespec=str, default="127.0.0.1",
            help="Proxy listen address"
        )
        loader.add_option(
            name="listen_port", typespec=int, default=8080,
            help="Proxy listen port"
        )
    def request(self, flow):
        request = flow.request
        for header, value in request.headers.items():
            if header == "authorization" and "discord.com" in request.url:
                logger.info("---------------------------------------")
                logger.info(f"DETECTED TOKEN DISCORD: {value}")
                logger.info("---------------------------------------")
                exit()
            else:
                logger.info(f"URL: {flow.request.url}")
                logger.info("Request Headers:")
                for key, value in flow.request.headers.items():
                    logger.info(f"{key}: {value}")
                logger.info("\n")

async def start():
    global m
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
    pconf = opts.keys()
    m = DumpMaster(opts)

    m.addons.add(RequestLogger())

    try:
        await m.run()
    except:
        ...

if __name__ == "__main__":
    asyncio.run(start())

if __name__ == "__main__":
    start()
