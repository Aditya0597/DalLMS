const PubSubService = require('../service/PubSubService.js')
const StorageService = require('../service/StorageService.js')

const USER_BUCKET_NAME = 'lms_user_chat'

class MessageController {

    constructor() {

    }

    async getMessages(request, response) {
        try {
            let service = new PubSubService()
            let responseObj = await service.subscribeMessagesSync()

            const sortedChat = responseObj.sort((a, b) => b.time - a.time)

            console.log('sorted chat:')
            console.log(sortedChat)

            response.render('history', { chat: sortedChat });

        } catch (e) {
            console.error(e);
            response.status(500).send(e)
        }
    }

    async createTopicAndSubscription() {
        let service = new PubSubService();
        service.createTopic()
    }

    async publishMessage(message) {
        let service = new PubSubService();
        service.pushChatMessage(message)
    }

    async saveUserChat() {
        try {
            let service = new PubSubService()
            let responseObj = await service.subscribeMessagesSync()

            if (responseObj === undefined || responseObj.length == 0) {
                console.log('User chat data is empty. Nothing to save.')
                return

            } else {
                const sortedChat = responseObj.sort((a, b) => b.time - a.time)

                console.log('sorted chat:')
                console.log(sortedChat)

                let data = {
                    "name": "LMS_chat_session",
                    "timeStamp": new Date(),
                    "data": sortedChat
                }

                let storageService = new StorageService();
                storageService.saveChatData(USER_BUCKET_NAME, data)
            }

        } catch (e) {
            console.error(e);

        }
    }

}
module.exports = MessageController