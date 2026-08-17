from logging import Logger

from tplinkrouterc6v.client.xdr import TPLinkXDRClient
from tplinkrouterc6v.common.exception import ClientException
from tplinkrouterc6v.client.c6u import TplinkRouter, TplinkRouterV1_11
from tplinkrouterc6v.client.sg import TplinkRouterSG
from tplinkrouterc6v.client.deco import TPLinkDecoClient
from tplinkrouterc6v.client_abstract import AbstractRouter
from tplinkrouterc6v.client.mr import TPLinkMRClient, TPLinkMRClientGCM, TPLinkMR600Client
from tplinkrouterc6v.client.c50 import TPLinkC50Client
from tplinkrouterc6v.client.wr841 import TPLinkWR841NClient
from tplinkrouterc6v.client.mr200 import TPLinkMR200Client
from tplinkrouterc6v.client.mr6400v7 import TPLinkMR6400v7Client
from tplinkrouterc6v.client.ex import TPLinkEXClient, TPLinkEXClientGCM
from tplinkrouterc6v.client.c5400x import TplinkC5400XRouter
from tplinkrouterc6v.client.c3200 import TplinkC3200Router
from tplinkrouterc6v.client.c1200 import TplinkC1200Router
from tplinkrouterc6v.client.c80 import TplinkC80Router
from tplinkrouterc6v.client.vr import TPLinkVRClient
from tplinkrouterc6v.client.vr400v2 import TPLinkVR400v2Client
from tplinkrouterc6v.client.r import TPLinkRClient
from tplinkrouterc6v.client.wdr import TplinkWDRRouter
from tplinkrouterc6v.client.re330 import TplinkRE330Router
from tplinkrouterc6v.client.eap115 import TPLinkEAP115Client
from tplinkrouterc6v.client.cpe210 import TPLinkCPE210Client
from tplinkrouterc6v.client.sg108e import TPLinkSG108EClient
from tplinkrouterc6v.client.vr1200v import TplinkVR1200vRouter


class TplinkRouterProvider:
    @staticmethod
    def get_client(host: str, password: str, username: str = 'admin', logger: Logger = None,
                   verify_ssl: bool = True, vpn_support: bool = True, timeout: int = 30) -> AbstractRouter:
        logger.debug('vpn support is %s', vpn_support)
        for client_name, client in TplinkRouterProvider.get_clients().items():
            if isinstance(client, TplinkC1200Router):
                continue
            router = client(host, password, username, logger, verify_ssl, timeout)
            if router.supports():
                logger.info('TplinkRouterProvider: supports() succeeded for %s, client chosen: %s', host, client.__name__)
                return router
            elif logger is not None:
                logger.debug('TplinkRouterProvider: supports() failed for %s (%s)', host, client.__name__)

        message = ('Login failed! Please check if your router local password is correct,'
                   'check if the default router username is correct or '
                   'try to use web encrypted password instead. Check the documentation!')
        router = TplinkC1200Router(host, password, username, logger, verify_ssl, timeout)
        try:
            router.authorize()
            return router
        except Exception:
            pass

        for client in [TPLinkVRClient, TPLinkXDRClient]:
            router = client(host, password, username, None, verify_ssl, timeout)
            try:
                router.authorize()
                message = ('Your router might be supported by {}. Please open the issue here '
                           'https://github.com/AlexandrErohin/TP-Link-Archer-C6U').format(router.__class__)
                break
            except Exception:
                pass

        raise ClientException(message)

    @staticmethod
    def get_clients() -> dict[str, type[AbstractRouter]]:
        return {
            TplinkC5400XRouter.__name__: TplinkC5400XRouter,
            TPLinkVRClient.__name__: TPLinkVRClient,
            TPLinkEXClientGCM.__name__: TPLinkEXClientGCM,
            TPLinkEXClient.__name__: TPLinkEXClient,
            TplinkVR1200vRouter.__name__: TplinkVR1200vRouter,
            TPLinkC50Client.__name__: TPLinkC50Client,
            TPLinkWR841NClient.__name__: TPLinkWR841NClient,
            TPLinkMRClientGCM.__name__: TPLinkMRClientGCM,
            TPLinkMRClient.__name__: TPLinkMRClient,
            TPLinkMR200Client.__name__: TPLinkMR200Client,
            TPLinkMR6400v7Client.__name__: TPLinkMR6400v7Client,
            TPLinkVR400v2Client.__name__: TPLinkVR400v2Client,
            TPLinkMR600Client.__name__: TPLinkMR600Client,
            TPLinkDecoClient.__name__: TPLinkDecoClient,
            TPLinkXDRClient.__name__: TPLinkXDRClient,
            TPLinkRClient.__name__: TPLinkRClient,
            TplinkRouterSG.__name__: TplinkRouterSG,
            TplinkRouterV1_11.__name__: TplinkRouterV1_11,
            TplinkRouter.__name__: TplinkRouter,
            TplinkC80Router.__name__: TplinkC80Router,
            TplinkWDRRouter.__name__: TplinkWDRRouter,
            TplinkRE330Router.__name__: TplinkRE330Router,
            TplinkC3200Router.__name__: TplinkC3200Router,
            TPLinkEAP115Client.__name__: TPLinkEAP115Client,
            TPLinkCPE210Client.__name__: TPLinkCPE210Client,
            TPLinkSG108EClient.__name__: TPLinkSG108EClient,
            TplinkC1200Router.__name__: TplinkC1200Router,
        }
