import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

let MODEL = null;
let IGNORE_LIST = [];
let DEMAND_NF = 1;
let IS_INIT = false;

export async function initModel() {
    if (IS_INIT) return;
    try {
        const [modelRes, ignoreRes] = await Promise.all([
            fetch('/data/model.json'),
            fetch('/data/ignore.txt')
        ]);
        MODEL = await modelRes.json();
        const ignoreText = await ignoreRes.text();
        IGNORE_LIST = ignoreText.split('\n').map(s => s.trim()).filter(Boolean);

        // Calculate DEMAND_NF
        let csfs = [], ilfs = [];
        for (const cate in MODEL) {
            for (const post in MODEL[cate].posts) {
                const item = MODEL[cate].posts[post].demand;
                const csf = item.continuous_freq || 0;
                const ilf = item.interval_freq || 0;
                csfs.push(csf);
                ilfs.push(ilf);
            }
        }

        // Python: math.ceil(sum(csfs))
        const csfSum = Math.ceil(csfs.reduce((a, b) => a + b, 0));
        const ilfSum = Math.ceil(ilfs.reduce((a, b) => a + b, 0));
        DEMAND_NF = (csfSum + ilfSum) / 2;

        IS_INIT = true;
        console.log("SuitJOB logic initialized. DEMAND_NF:", DEMAND_NF);
    } catch (e) {
        console.error("Failed to init model", e);
    }
}

function randomPick(list, num) {
    const shuffled = [...list].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, num);
}

export function generateWords() {
    if (!MODEL) throw new Error("Model not initialized");
    let dutyList = [];
    let requireList = [];

    for (const key in MODEL) {
        const dutyWdict = MODEL[key].duty;
        const requireWdict = MODEL[key].require;

        const dutyKeys = Object.keys(dutyWdict);
        const requireKeys = Object.keys(requireWdict);

        const pickedDuty = randomPick(dutyKeys, 7).filter(w => !IGNORE_LIST.includes(w));
        const pickedRequire = randomPick(requireKeys, 7).filter(w => !IGNORE_LIST.includes(w));

        pickedDuty.forEach(w => dutyList.push({ word: w, category: key }));
        pickedRequire.forEach(w => requireList.push({ word: w, category: key }));
    }

    // Remove duplicates keeping last category (mimic python dict behavior)
    const dutyMap = new Map();
    dutyList.forEach(item => dutyMap.set(item.word, item.category));

    const requireMap = new Map();
    requireList.forEach(item => requireMap.set(item.word, item.category));

    const finalDuty = Array.from(dutyMap.entries()).map(([w, c]) => ({ word: w, category: c }));
    const finalRequire = Array.from(requireMap.entries()).map(([w, c]) => ({ word: w, category: c }));

    return {
        like: finalDuty.sort(() => 0.5 - Math.random()),
        cando: finalRequire.sort(() => 0.5 - Math.random())
    };
}

function getDutyCateScore(chosenDutyList) {
    const res = {};
    for (const { word: w, category: cate } of chosenDutyList) {
        if (MODEL[cate] && MODEL[cate].duty[w]) {
            const score = MODEL[cate].duty[w].prob;
            res[cate] = (res[cate] || 0) + score;
        }
    }
    return res;
}

function getRequirePostScore(chosenRequireList) {
    const res = {}; // {cate: {post: score}}
    for (const { word: w, category: cate } of chosenRequireList) {
        if (!MODEL[cate]) continue;
        const posts = MODEL[cate].posts;
        for (const post in posts) {
            if (posts[post].require[w]) {
                const score = posts[post].require[w].prob;
                if (!res[cate]) res[cate] = {};
                res[cate][post] = (res[cate][post] || 0) + score;
            }
        }
    }
    return res;
}

function getDemandPostScore(chosenRequireList) {
    const res = {};
    for (const { word: w, category: cate } of chosenRequireList) {
        if (!MODEL[cate]) continue;
        const posts = MODEL[cate].posts;
        for (const post in posts) {
            if (posts[post].require[w]) {
                if (res[cate] && res[cate][post] !== undefined) continue;

                const demand = posts[post].demand;
                const score = ((demand.continuous_freq + demand.interval_freq) / (2 * DEMAND_NF)) * demand.publish_freq;

                if (!res[cate]) res[cate] = {};
                res[cate][post] = score;
            }
        }
    }
    return res;
}

export function calcScore(userChosenDict, topk = 5) {
    if (!MODEL) throw new Error("Model not initialized");

    const dutyList = userChosenDict.like;
    const requireList = userChosenDict.cando;

    const dutyCateScore = getDutyCateScore(dutyList);
    const requirePostScore = getRequirePostScore(requireList);
    const demandPostScore = getDemandPostScore(requireList);

    const scores = [];

    for (const cate in requirePostScore) {
        const posts = requirePostScore[cate];
        const cateS = dutyCateScore[cate] || 0;

        for (const post in posts) {
            const postS = posts[post];
            const demandS = demandPostScore[cate]?.[post] || 0;

            // Adjusted Weights: Skills (postS) 50%, Interest (cateS) 30%, Demand 20%
            const score = cateS * 0.3 + postS * 0.5 + demandS * 0.2;

            // Simple breakdown to explain the score (debugging/user feedback)
            // Re-find which words contributed to this specific post match
            const matchedSkills = requireList.filter(item =>
                MODEL[cate].posts[post].require[item.word]
            ).map(item => item.word);

            const matchedInterests = dutyList.filter(item =>
                item.category === cate // Interest is category-level
            ).map(item => item.word);

            scores.push({
                name: `${cate}-${post}`,
                rawScore: score,
                category: cate,
                post: post,
                breakdown: {
                    skills: matchedSkills,
                    interests: matchedInterests
                }
            });
        }
    }

    // Sort descending
    scores.sort((a, b) => b.rawScore - a.rawScore);

    // Normalize: int(f * 100 / maxs)
    if (scores.length === 0) return [];

    const maxScore = scores[0].rawScore;
    const result = scores.slice(0, topk).map(item => ({
        ...item,
        score: maxScore === 0 ? 0 : Math.round((item.rawScore / maxScore) * 100)
    }));

    return result;
}
