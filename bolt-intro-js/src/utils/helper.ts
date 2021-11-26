import {
    GenericMessageEvent,
    MessageEvent,
    ReactionAddedEvent,
    ReactionMessageItem
} from '@slack/bolt';

exports.isGenericMessageEvent = (
    msg: MessageEvent
): msg is GenericMessageEvent =>
    (msg as GenericMessageEvent).subtype === undefined;

exports.isMessageItem = (
    item: ReactionAddedEvent['item']
): item is ReactionMessageItem =>
    (item as ReactionMessageItem).type === 'message';
