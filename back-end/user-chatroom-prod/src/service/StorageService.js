const { Storage } = require('@google-cloud/storage');
const fs = require('fs');
var tmp = require('tmp');

const gcpStorage = new Storage();


class StorageService {

    constructor() {
    }

    async createBucket() {

        let bucketName = "lms_chat_" + Date.now()

        const [bucket] = await gcpStorage.createBucket(bucketName, {
            location: 'ASIA',
            storageClass: 'COLDLINE',
        });

        console.log(`Bucket ${bucket.name} created.`);

        return bucket.name;

    }

    async saveChatData(bucketName, data) {

        let fileName = 'LMS_chat_session'

        var tmpObj = tmp.fileSync({ prefix: fileName, postfix: '.json' });
        const content = JSON.stringify(data);

        fs.writeFileSync(tmpObj.name, content);

        console.log("File: ", tmpObj.name);

        // Uploads a local file to the bucket
        await gcpStorage.bucket(bucketName).upload(tmpObj.name, {
            gzip: true,
        });

        console.log(`${fileName} uploaded to ${bucketName}.`);
    }

}

module.exports = StorageService