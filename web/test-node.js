import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Mock fetch
global.fetch = async (url) => {
    const filename = url.split('/').pop();
    const headers = new Headers();
    const filePath = path.join(process.cwd(), 'public', 'data', filename);
    const content = fs.readFileSync(filePath, 'utf8');

    return {
        json: async () => JSON.parse(content),
        text: async () => content,
    };
}

// Import logic
import * as SuitJob from './src/utils/logic.js';

async function run() {
    console.log("Initializing model...");
    await SuitJob.initModel();

    console.log("Generating words...");
    const words = SuitJob.generateWords();
    console.log("Like words count:", words.like.length);
    console.log("Cando words count:", words.cando.length);

    // Simulate selection
    const choices = {
        like: words.like.slice(0, 5),
        cando: words.cando.slice(0, 5)
    };

    console.log("Calculating score...");
    const res = SuitJob.calcScore(choices);
    console.log("Top Result:", res[0]);

    if (res.length > 0 && res[0].score > 0) {
        console.log("SUCCESS: Logic working.");
    } else {
        console.error("FAILURE: No results or zero score.");
        process.exit(1);
    }
}

run();
