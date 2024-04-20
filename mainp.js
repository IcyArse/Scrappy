const puppeteer = require('puppeteer');

async function runScript() {
    // Launch a headless browser
    const browser = await puppeteer.launch({ headless: true });

    // Create a new page
    const page = await browser.newPage();

    // Navigate to the login page
    await page.goto('https://www.turnitin.com/login_page.asp');

    // Enter email and password
    await page.type('input[name="email"]', 'amran@um.edu.my');
    await page.type('input[name="user_password"]', 'Superman@1000');

    // Click the submit button
    await page.click('input[name="submit"]');

    // Wait for navigation to complete
    await page.waitForNavigation();

    // Check if login was successful
    if (page.url().includes('t_home.asp')) {
        console.log('Login successful');

        // Find the <td> element with the given class ID
        const tdElement = await page.$x(`//td[@class='class_id' and contains(text(), '${class_id}')]`);

        if (tdElement.length > 0) {
            // Get the parent <tr> element
            const trElement = await tdElement[0].$x('./..');

            // Find the <a> tag within the <td> with class_name class
            const aTag = await trElement[0].$x(".//td[@class='class_name']/a");

            if (aTag.length > 0) {
                const hrefValue = await aTag[0].getProperty('href');
                const href = hrefValue._remoteObject.value;
                console.log(`The href value associated with class ID ${class_id} is: ${href}`);

                // Navigate to the href value URL
                await page.goto(href);

                // Wait for the assignment page to load
                await page.waitForNavigation();

                // Click on the link to open the assignment
                await page.click('a.similarity-open');

                // Wait for the assignment to open
                await page.waitForSelector('YOUR_SELECTOR_FOR_THE_BUTTON', { visible: true });

                // Click on the button to download the file
                await page.click('YOUR_SELECTOR_FOR_THE_BUTTON');

                console.log('File download initiated');
            } else {
                console.log(`No <a> tag found for class ID ${class_id}`);
            }
        } else {
            console.log(`Class ID ${class_id} not found in the HTML content.`);
        }
    } else {
        console.log('Login failed');
    }

    // Close the browser
    await browser.close();
}

// Call the function
runScript();
