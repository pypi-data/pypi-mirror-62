import pytest

from blockkit import elements
from blockkit.blocks import Input
from blockkit.composition import ConfirmationDialog, Option, PlainText
from blockkit.fixed_blocks import *


@pytest.fixture
def mock_fixed_input():
    class MockFixedInput(FixedInputMixin, Input):
        element_class = elements.PlainTextInput
        block_id = "block_id"
        action_id = "action_id"
        label = "label"
        optional = True
        hint = "hint"

    return MockFixedInput


class TestFixedInputMixin:
    @pytest.fixture
    def parse_args(self, make_parse_block_args):
        return make_parse_block_args({"value": "value"})

    def test_fixed(self, snapshot, mock_fixed_input):
        snapshot.assert_match(mock_fixed_input())

    def test_override(self, snapshot, mock_fixed_input):
        snapshot.assert_match(mock_fixed_input(block_id="override"))

    def test_parse(self, parse_args, mock_fixed_input):
        mock_fixed_input.parse(**parse_args)

    def test_parse_missing_block_id(self, parse_args, mock_fixed_input):
        mock_fixed_input.block_id = None
        del parse_args["block_id"]
        with pytest.raises(TypeError):
            mock_fixed_input.parse(**parse_args)

    def test_parse__missing_action_id(self, parse_args, mock_fixed_input):
        mock_fixed_input.action_id = None
        del parse_args["action_id"]
        with pytest.raises(TypeError):
            mock_fixed_input.parse(**parse_args)


class MockFixedDatePickerInput(FixedDatePickerInput):
    block_id = "test_block"
    action_id = "test_action"
    label = "label"
    optional = True
    hint = "hint"
    placeholder = "placeholder"
    initial_date = "2020-01-01"
    confirm = ConfirmationDialog(
        text_object=PlainText("text"), title="title", confirm="confirm", deny="deny",
    )


class TestFixedDatePickerInput:
    def test_fixed(self, snapshot):
        snapshot.assert_match(MockFixedDatePickerInput())

    @pytest.mark.parametrize(
        "field, value",
        [
            ("placeholder", "override"),
            ("initial_date", "2019-01-01"),
            (
                "confirm",
                ConfirmationDialog(
                    text_object=PlainText("override"),
                    title="override",
                    confirm="confirm",
                    deny="deny",
                ),
            ),
        ],
    )
    def test_override(self, snapshot, field, value):
        snapshot.assert_match(MockFixedDatePickerInput(**{field: value}))


class MockFixedStaticSelectInput(FixedStaticSelectInput):
    block_id = "test_block"
    action_id = "test_action"
    label = "label"
    optional = True
    hint = "hint"
    options = [Option("text", "value")]
    initial_option = Option("text", "value")
    placeholder = "placeholder"
    confirm = ConfirmationDialog(
        text_object=PlainText("text"), title="title", confirm="confirm", deny="deny",
    )


class TestFixedStaticSelectInput:
    def test_fixed(self, snapshot):
        snapshot.assert_match(MockFixedStaticSelectInput())

    @pytest.mark.parametrize(
        "field, value",
        [
            ("options", [Option("override", "override")]),
            ("initial_option", Option("override", "override")),
            ("placeholder", "override"),
            (
                "confirm",
                ConfirmationDialog(
                    text_object=PlainText("override"),
                    title="override",
                    confirm="confirm",
                    deny="deny",
                ),
            ),
        ],
    )
    def test_override(self, snapshot, field, value):
        snapshot.assert_match(MockFixedStaticSelectInput(**{field: value}))


class MockFixedPlainTextInput(FixedPlainTextInput):
    block_id = "test_block"
    action_id = "test_action"
    label = "label"
    optional = True
    hint = "hint"
    initial_value = "initial_value"
    multiline = False
    min_length = 1
    max_length = 20
    placeholder = "placeholder"


class TestFixedPlainTextInput:
    def test_fixed(self, snapshot):
        snapshot.assert_match(MockFixedPlainTextInput())

    @pytest.mark.parametrize(
        "field, value",
        [
            ("initial_value", "override"),
            ("multiline", True),
            ("min_length", 2),
            ("max_length", 3),
            ("placeholder", "override"),
        ],
    )
    def test_override(self, snapshot, field, value):
        snapshot.assert_match(MockFixedPlainTextInput(**{field: value}))


class MockFixedConversationsSelectInput(FixedConversationsSelectInput):
    block_id = "test_block"
    action_id = "test_action"
    label = "label"
    optional = True
    hint = "hint"
    initial_conversation = "1"
    placeholder = "placeholder"


class TestFixedConversationsSelectInput:
    def test_fixed(self, snapshot):
        snapshot.assert_match(MockFixedConversationsSelectInput())

    def test_override(self):
        obj = MockFixedConversationsSelectInput(initial_conversation="2")
        assert obj["element"]["initial_conversation"] == "2"
