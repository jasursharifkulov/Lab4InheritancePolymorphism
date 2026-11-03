# 2.1: sned does not override send; the inherited pass silently returns None.
# 2.2: ABC prevents instantiating a subclass that has not implemented send.
# 2.3: send is abstract; notify is concrete and shared by all channels.
# 2.4: self.max_length selects the actual channel's limit.
from abc import ABC, abstractmethod
import pytest


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient, text): ...

    def notify(self, recipient, text):
        self.send(recipient, text[:self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096
    def send(self, recipient, text):
        print(f'telegram -> {recipient}: {text}')


class SmsNotifier(Notifier):
    max_length = 160
    def send(self, recipient, text):
        print(f'sms -> {recipient}: {text}')


def test_abstract_and_typo():
    class BrokenTelegram(Notifier):
        def sned(self, recipient, text):
            pass
    with pytest.raises(TypeError):
        Notifier()
    with pytest.raises(TypeError):
        BrokenTelegram()


@pytest.mark.parametrize('channel,prefix,limit', [
    (TelegramNotifier(), 'telegram', 4096), (SmsNotifier(), 'sms', 160),
])
def test_channel_limits(channel, prefix, limit, capsys):
    channel.notify('@ali', 'x' * 5000)
    assert capsys.readouterr().out == f'{prefix} -> @ali: ' + 'x' * limit + '\n'
