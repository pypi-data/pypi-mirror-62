"""Test the mindspace library."""

from pytest import raises
from mindspace_protocol import MindspaceParser, CommandNotFound


class Works(Exception):
    pass


class CustomMindspaceParser(MindspaceParser):
    def huh(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        raise Works()


parser = MindspaceParser()


class NoArgumentsWorks(Exception):
    pass


class WithArgumentsWorks(Exception):
    pass


class WithKwargsWorks(Exception):
    pass


class WithBothWorks(Exception):
    pass


@parser.command
def no_arguments():
    raise NoArgumentsWorks()


@parser.command
def with_arguments(first, second):
    assert first == 'hello'
    assert second == 'world'
    raise WithArgumentsWorks()


@parser.command
def with_kwargs(hello=None, this=None):
    assert hello == 'world'
    assert this == 'works'
    raise WithKwargsWorks()


@parser.command
def with_both(first, second, this=None, name=None):
    assert first == 'hello'
    assert second == 'world'
    assert this == 'works'
    assert name == __name__
    raise WithBothWorks()


def test_no_arguments():
    with raises(NoArgumentsWorks):
        parser.handle_command('no_arguments')


def test_with_arguments():
    with raises(WithArgumentsWorks):
        parser.handle_command('with_arguments', 'hello', 'world')


def test_with_kwargs():
    with raises(WithKwargsWorks):
        parser.handle_command('with_kwargs', hello='world', this='works')


def test_with_both():
    with raises(WithBothWorks):
        parser.handle_command(
            'with_both', 'hello', 'world', this='works', name=__name__
        )


def test_command_not_found():
    name = 'no command called this, hahahaha!'
    with raises(CommandNotFound) as exc:
        parser.handle_command(name)
    p, command = exc.value.args
    assert command == name
    assert p is parser


def test_custom_huh():
    p = CustomMindspaceParser()
    name = 'test'
    args = (1, 2, 3)
    kwargs = {'hello': 'world'}
    with raises(Works):
        p.handle_command(name, *args, **kwargs)
    assert p.name == name
    assert p.args == args
    assert p.kwargs == kwargs


def test_custom_name():
    p = MindspaceParser()
    p.command(name='test')(print)
    assert print.__name__ not in p.commands
    assert p.commands['test'] is print
