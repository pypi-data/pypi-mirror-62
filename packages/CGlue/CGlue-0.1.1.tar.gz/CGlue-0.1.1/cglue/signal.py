class SignalConnection:
    def __init__(self, context, name, signal, provider_name, attributes):
        self.name = name
        self.signal = signal
        self.provider = provider_name
        self.attributes = attributes
        self.consumers = []
        self.context = context

        signal.create(context, self)

    def add_consumer(self, consumer_name, consumer_attributes):
        self.consumers.append((consumer_name, consumer_attributes))

    def generate(self):
        # collect implementations in a list
        function_mods_list = []
        function_mods = self.signal.generate_provider(self.context, self, self.provider)
        if function_mods:
            function_mods_list.append(function_mods)

        for consumer, attributes in self.consumers:
            function_mods = self.signal.generate_consumer(self.context, self, consumer, attributes)
            if function_mods:
                function_mods_list.append(function_mods)

        self.context['runtime'].raise_event('signal_generated', self, function_mods_list)

        # apply modifications
        for function_mods in function_mods_list:
            for port_name, mods in function_mods.items():
                functions = self.context['functions'][port_name]
                for func_type, mods in mods.items():
                    if func_type in functions:
                        if 'body' in mods:
                            functions[func_type].add_body(mods['body'])

                        if 'return_statement' in mods:
                            functions[func_type].set_return_statement(mods['return_statement'])

                        if 'used_arguments' in mods:
                            for argument in mods['used_arguments']:
                                functions[func_type].mark_argument_used(argument)


class SignalType:
    def __init__(self, consumers='multiple', required_attributes=None):
        if required_attributes is None:
            required_attributes = []

        self._consumers = consumers
        self.required_attributes = frozenset(required_attributes)

    @property
    def consumers(self):
        return self._consumers

    def create(self, context, connection: SignalConnection):
        pass

    def generate_provider(self, context, connection: SignalConnection, provider_name):
        pass

    def generate_consumer(self, context, connection: SignalConnection, consumer_name, attributes):
        pass

    def create_connection(self, context, name, provider, attributes):
        missing_attributes = self.required_attributes.difference(attributes.keys())
        if missing_attributes:
            missing_list = ", ".join(missing_attributes)
            raise Exception(f'{missing_list} attributes are missing from connection provided by {provider}')
        return SignalConnection(context, name, self, provider, attributes)
