const fs = require('fs');

const day = process.argv[2];
const regex = new RegExp('"fav_(.*?)"[.\\r\\n]*\\s*class="\\s*fas', 'gm');

fs.readFile(`./${day}.json`, 'utf8', (err, data) => {
    if(err) {
        console.error(err);
    } else {
        const matches = data.match(regex)
            .map(txt => txt
                .replace('"fav_', '')
                .replace(/"\n\s*class="\s*fas/, ''))
            .join(' ');
        console.log(matches);
    }
});