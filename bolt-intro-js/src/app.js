"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const dotenv = require('dotenv');
const parsed = dotenv.config();
if (parsed.error)
    throw new Error('Error');
const { App } = require('@slack/bolt');
const { isGenericMessageEvent } = require('./utils/helper');
const credentials = {
    token: process.env.SLACK_BOT_TOKEN,
    signingSecret: process.env.SLACK_SIGNING_SECRET,
    socketMode: true,
    appToken: process.env.SLACK_APP_TOKEN,
    port: process.env.PORT || 3000
};
const app = new App(credentials);
app.message('hello', () => __awaiter(void 0, void 0, void 0, function* () {
    yield x.say({
        blocks: [
            {
                type: 'section',
                text: {
                    type: 'mrkdwn',
                    text: `Hi <@${x.message.user}>`
                }
            }
        ]
    });
}));
(() => __awaiter(void 0, void 0, void 0, function* () {
    // Start your app
    yield app.start();
    console.log('⚡️ Bolt app is running!');
}))();
//# sourceMappingURL=app.js.map