const { PubSub, v1 } = require('@google-cloud/pubsub');

let topicName = null
let topicSubscriptionName = null

let pubSubClientV1 = new v1.SubscriberClient();

let GCP_PROJECT_ID = process.env.GCP_PROJECT_ID

class PubSubService {

    constructor() {
    }

    async createTopic() {

        topicName = 'LMS_chat_' + Date.now()
        let pubSubClient = new PubSub();

        // Creates a new topic
        await pubSubClient.createTopic(topicName);
        console.log(`Topic ${topicName} created.`);

        let subscriptionCreate = await this.createSubscription()
    }

    async createSubscription() {

        topicSubscriptionName = topicName + '_subsciption'

        const pubSubClient = new PubSub();
        
        // Creates a new subscription
        await pubSubClient.topic(topicName).createSubscription(topicSubscriptionName);
        console.log(`Subscription ${topicSubscriptionName} created.`);
    }

    async pushChatMessage(message) {
        if (topicName) {
            let pubSubClient = new PubSub();

            message = JSON.stringify(message)
            const dataBuffer = Buffer.from(message);

            const messageId = await pubSubClient.topic(topicName).publish(dataBuffer);
            console.log(`Message ${messageId} published.`);
        }
        else {
            console.log(`Topic does not exists for message to push.`);
        }

    }

    async subscribeMessagesSync() {
        if (topicName && topicSubscriptionName) {

            const subscription = pubSubClientV1.subscriptionPath(
                GCP_PROJECT_ID,
                topicSubscriptionName
            );

            const request = {
                subscription: subscription,
                maxMessages: 1000,
            };

            let [response] = await pubSubClientV1.pull(request)

            let messageHistory = []
            for (const message of response.receivedMessages) {
                console.log(`Received message: ${message.message.data}`);
                messageHistory.push(JSON.parse(message.message.data.toString()))
            }

            return messageHistory;

        } else {
            console.log(`Topic does not exists for subscription.`);
        }
    }
}

module.exports = PubSubService