from parser import Parser
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                                    WebSocketClientFactory


class MHomeClientProtocol(WebSocketClientProtocol):
    """
    Senz client which handles switching. Client connnect to Senz server and
    listen for incoming switching queris. Switchig query would be looks like
        1. 'PUT #switch kitchen @eranga' - switch on
        2. ':PUT #switch kitchen @eranga' - switch off

    When received PUT query client needs to send a message to appropriate GPIO
    port to switching(switch ON/OFF)

    After switching operation, client needs to send status back to server via
    DATA query
        'DATA #msg success @eranga'
    """
    def onConnect(self, response):
        """
        Calls when successfuly connected with the server
        """
        print '-----------------------'
        print '------CONNECTED--------'
        print '-----------------------\n'

    def onOpen(self):
        """
        Calls when open websocket connection with Senz server
        Need to send Login query form here
        """
        print '-----------------------'
        print '---------OPEN----------'
        print '-----------------------\n'
        self.sendMessage("LOGIN #username home #password tess")

    def onMessage(self, payload, isBinary):
        """
        call when message recives to listening port. Message need to be parse
        according to the QueryParser. Then need to be delegate task to
        appropriate, handler according to the parsed query paramets

        in here most of the time we do get follwoing queries
            1. PUT #switch kitchen @eranga - switch on
            2. :PUT #switch kitchen @eranga - switch off
        """
        print '-----------------------'
        print(payload)
        print '-----------------------\n'
        parser = Parser()
        query = parser.parse(message=payload)

        if query.command == "PUT":
            print("Switching on...")
            print(query.parameters)
            print(query.user)
            # TODO call GPIO client to switch on
        elif query.command == ":PUT":
            print("Switching off...")
            print(query.parameters)
            print(query.user)
            # TODO call GPIO client to switch off

    def onClose(self, wasClean, code, reason):
        """
        Calls when connection closed with Senz server.
        Reset all connections, params from here
        """
        print '-----------------------'
        print '-------CLOSED----------'
        print '-----------------------\n'


if __name__ == '__main__':
    # start web socket client
    # listen for 9000 port
    factory = WebSocketClientFactory("ws://10.2.2.132:9000", debug=False)
    factory.protocol = MHomeClientProtocol

    reactor.connectTCP("10.2.2.132", 9000, factory)
    reactor.run()
