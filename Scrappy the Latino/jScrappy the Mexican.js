var jsdom = require("jsdom");
var fs = require("fs");

var dataFileIn = 'DailyMail_facebook_statuses_links.csv';
var dataFileOut = 'posts.json';

var outputArray = [];

function david (urls) {
	jsdom.env(urls.pop(), ["https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"], 
		(err, window) => {
			if (err) {
				console.log(err);
				return;
			}

			outputArray.push(window.$("div[itemprop='articleBody']").html());

			fs.writeFileSync(dataFileOut, JSON.stringify(outputArray));

			console.log(urls.length);

			if (urls.length > 0) {
				david(urls);
			}
		}
	);
}

var content = fs.readFileSync(dataFileIn).toString();

var lines = content.split("\n");
lines.pop();

var urls = [];

lines.forEach((line) => {
	urls.push(line.split(",")[1]);
});

david(urls.slice(0, 999));
david(urls.slice(1000, 1999));
david(urls.slice(2000, 2999));
david(urls.slice(3000, 3999));
david(urls.slice(4000, 4999));
david(urls.slice(5000, 5821));

//fs.writeFileSync(file, data[, options])


