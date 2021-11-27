package com.muler;


import com.slack.api.Slack;
import com.slack.api.bolt.App;
import com.slack.api.bolt.response.Response;
import com.slack.api.bolt.socket_mode.SocketModeApp;
import com.slack.api.model.block.LayoutBlock;
import com.slack.api.model.block.SectionBlock;
import com.slack.api.model.block.composition.MarkdownTextObject;
import com.slack.api.model.block.composition.PlainTextObject;
import com.slack.api.model.block.element.BlockElement;
import com.slack.api.model.block.element.ButtonElement;
import com.slack.api.model.event.MessageEvent;
import com.slack.api.socket_mode.SocketModeClient;
import com.slack.api.webhook.Payload;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Slf4j
public class SlackApp {

  private final static String SLACK_APP_TOKEN = System.getenv("SLACK_APP_TOKEN");
  private final static String SLACK_BOT_TOKEN = System.getenv("SLACK_BOT_TOKEN");

  public static void main(String[] args) throws Exception {
    App app = new App();

    app.message("onboard", (message, context) -> {
      MessageEvent event = message.getEvent();

      String text = "Hello, <@" + event.getUser() + ">";
      BlockElement element = ButtonElement.builder().text(PlainTextObject.builder().text("Start Onboarding").build())
              .actionId("onboardClickAction")
              .style("primary")
              .build();
      SectionBlock block = SectionBlock.builder()
              .text(MarkdownTextObject.builder().text(text).build())
              .accessory(element)
              .build();

      List<LayoutBlock> layoutBlocks = new ArrayList<>();
      layoutBlocks.add(block);
      return Response.ok(context.say(chatPostMessageRequestBuilder ->
              chatPostMessageRequestBuilder.blocks(layoutBlocks)
                      .channel(event.getChannel())
      ));
    });

    app.blockAction("onboardClickAction", ((blockActionRequest, actionContext) -> {
      actionContext.ack();
      String responseUrl = actionContext.getResponseUrl();
      Slack slack = actionContext.getSlack();
      SectionBlock block = SectionBlock.builder()
              .text(MarkdownTextObject.builder().text("Processing..").build())
              .build();
      return Response.ok(slack.send(responseUrl, Payload.builder().blocks(Collections.singletonList(block)).build()));
    }));

    SocketModeApp socketModeApp = new SocketModeApp(SLACK_APP_TOKEN, SocketModeClient.Backend.JavaWebSocket, app);
    socketModeApp.start();
  }

}
