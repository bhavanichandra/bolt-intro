import { LogLevel } from '@slack/bolt';

const dotenv = require('dotenv');
const parsed = dotenv.config();

if (parsed.error) throw new Error('Error');

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

// @ts-ignore
app.use(async ({ next }) => {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    await next!();
});
app.message('Onboard', async ({ message, say }) => {
    if (!isGenericMessageEvent(message)) return;

    await say({
        blocks: [
            {
                type: 'section',
                text: {
                    type: 'mrkdwn',
                    text: `Hi <@${message.user}>`
                },
                accessory: {
                    type: 'button',
                    text: {
                        type: 'plain_text',
                        text: 'Start Onboarding'
                    },
                    style: 'primary',
                    action_id: 'button_click'
                }
            }
        ],
        text: `Hi <@${message.user}>`
    });
});

app.action('button_click', async ({ body, ack, say }) => {
    await ack();
    await say(`<@${body.user.id}> Clicked the button`);
});

(async () => {
    // Start your app
    await app.start();

    console.log('⚡️ Bolt app is running!');
})();
