from helpers.modules.TcpServerModule import TcpServerModule

class TelnetServerModule(TcpServerModule):
    __commands = {}

    def command_help(self, send_handler, args, kwargs, client_key):
        """Command help handler"""
        send_handler('Command available:')

        for command in self.__commands.values():
            line = '    - %s' % command['full_command']

            if command['description']:
                line += ': %s' % command['description']

            send_handler(line)

    def command_not_found(self, command, args, kwargs, client_key):
        """Command not found handler"""
        self.send('command "%s" not found' % command, client_key)

    def command_quit(self, send_handler, args, kwargs, client_key):
        """Command quit handler"""
        self.close_client(client_key)

    def init(self):
        super().init()
        self.register_command('?', self.command_help, 'print the help messages')
        self.register_command('help', self.command_help, 'print the help message')
        self.register_command('exit', self.command_quit, 'disconnect to the server')
        self.register_command('quit', self.command_quit, 'disconnect to the server')

    def receive(self, data, client_key):
        try:
            words = data.decode('utf-8').strip().split()
        except UnicodeDecodeError:
            return

        if not words:
            return

        command = words[0]
        args = words[1:]
        kwargs = {}

        if command not in self.__commands:
            return self.command_not_found(command, args, kwargs, client_key)

        def send_handler(msg):
            self.send(msg, client_key)

        self.__commands[command]['handler'](send_handler, args, kwargs, client_key)

    def register_command(self, command, handler, description='', full_command='', help_handler=None):
        """register handler for a command"""
        self.__commands[command] = {
            'handler': handler,
            'full_command': full_command if full_command else command,
            'description': description,
            'help_handler': help_handler,
        }

    def send(self, message, client_key):
        """Send message to client"""
        super().send('%s\n' % message, client_key)
