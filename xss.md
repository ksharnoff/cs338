# Cookies and Cross-Site Scripting

Kezia Sharnoff

October 25, 2025

CS338 Computer Security


## Part 1: Cookies


Using Kali!!

### A

There is only one cookie, with the name `theme` and the value `default`. 

### B
The `theme` cookie changed its value to be `blue`. 

### C
The two relevant HTTP headers are `Cookie` and `Set-Cookie`. 

There are no cookies in the first GET request to the site, but the first HTTP response has the header `Set-Cookie: theme=default; Expires=Thu, 22 Jan 2026 22:38:02 GMT; Path=/`. After this, the GET requests to load the associated Javascript pages (`fdf.js` and `bootstrap.bundle.min.js`) have the header `Cookie: theme=default` included. After changing a cookie by the theme button and sending a GET request with the theme as a parameter (talked about in question F), the server responds with `Set-Cookie: theme=blue; Expires=Thu, 22 Jan 2026 22:38:31 GMT; Path=/`. All of this was figured out using Burp Suite. 

These are the same cookie values and names as with the inspector. 

### D
After quitting Firefox, the same theme is still selected. This means that these cookies are persistently stored until the date they expire and not on a per session basis. 

### E
The current theme is transmitted in each message from the browser to the server using the HTTP header `Cookie: theme=blue`. 

### F
A changed theme is sent from the browser to the server using a HTTP GET request with the new theme as a query, with the form `/fdf/?theme=blue`. The server responds with a `Set-Cookie` for theme blue. This can be seen using Burp Suite.

### G
Using the browser inspector, I can directly edit all fields of the cookies (name, value, domain, path, and expiration date). I changed the `value` to be `red` which did not change the page (because nothing was sent to the server to get the color). After reloading the page, it was red.

### H
Using Burp Suite's proxy tool, I can edit the HTTP that is being sent off. I easily could change the `Cookie: theme=default` to `Cookie: theme=red`. Then the server returned the `Set-Cookie` of a red theme and the website loaded red. I also tested setting this to a different color (green) but that showed up just as default, even though the server did return `Set-Cookie: theme=green`. 

### I
This is specific per the browser and the OS. 

I learned from [this UNIX stack exchange](https://unix.stackexchange.com/questions/82597/where-does-firefox-store-its-cookies-on-linux) that Firefox cookies in Linux are stored in `~/.mozzila/firefox/{profile}/cookies.sqlite`. I found that this path is correct, where my instillation of Kali Linux has my path as: `~/.mozilla/firefox/ybjm6ac6.default-esr/cookies.sqlite`. 

I found several files related to cookies for Burp Suite but was unable to find the location of the files. Burp Suite's [documentation](https://portswigger.net/burp/documentation/desktop/settings/sessions) does not specify where to find the cookies and just says that users should edit them in the application. The only cookie related files I could find were directories named `~/.BurpSuite/pre-wired-browser/OpenCookieDatabase` and `~/.BurpSuite/pre-wired-browser/CookieReadinessList` which were empty. 
 
## Part 2: Cross-Site Scripting

### A
According to [OWASP](https://owasp.org/www-community/Types_of_Cross-Site_Scripting), there are three types:
1. Reflected XSS:

    User inputted data is returned back (like in an error message) without checking that it is safe to display in the browser. For example, if someone submitted a query with HTML and then the server quoted the query to say it is not allowed while letting the HTML render. 
2. Stored XSS:

    User inputted data is stored and then returned back to other users without checking if it is safe. For example, if someone submitted a comment on an article with HTML and then the server displayed that comment to other visitors to the website, while letting the HTML render.
3. DOM Based XSS:
   
   This is similar to Reflected XSS, except the change is made to the DOM so the page loads differently than it should, without changing the HTTP response. An example of this would be to edit page contents using inspect element.

### B
Both evil posts are Stored XSS because the inputted data is returned by the server to other website visitors. 

The first evil post:
1. Moriarty figures out how to make text red using CSS
2. Moriarty logs into the discussion forum (with some back and forth from the server to verify)
3. Moriarty submits a post with red text tags included
4. The post information gets sent from Moriarty's computer to the server (using HTTP) where it is stored 
5. Later, another forum user clicks on the post
6. An HTTP GET request is sent to the server for the evil post, the server returns the exact contents that Moriarty had sent earlier (red text included)
7. The forum user's browser outputs the HTML and CSS for the page and makes the text red

The second evil post:
1. Moriarty figures out how to make a Javascript alert
2. Moriarty logs in to the forum
3. Moriarty submits a post with the alert script
4. The post information gets sent to and kept in the forum server
5. A different forum user clicks on the post, sending an HTTP GET request to the server
6. The server sends an HTTP response with the contents of the post
7. The browser reads through the HTML and compiles it. It notices that there is an alert so shows that first to the user
8. The user clicks out of the alert and can view the rest of the page 


### C

A virulent attack would be including the following in a post:

`<script> window.location.href = "http://fradulent-webpage.com" </script>`

When a victim clicks on the post, they will be redirect to `http://fradulent-webpage.com`. If `http://fradulent-webpage.com` looks exactly the same as the original website, the victim would not realize they had left the site. 

### D
A virulent attack would be the following script:

`<script> window.open("https://google.com"); window.open("https://microsoft.com"); window.open("https://wikipedia.org"); window.open("https://google.com"); window.open("https://microsoft.com"); window.open("https://wikipedia.org"); ... </script> `

This would open many tabs at once that all would need to do their own TLS handshake with the sites. This both acts as a DoS attack to the sites and slows down or crashes the victim's computer. In addition, if the victim's computer is marked as an IP address that does DoS attacks by a major website (Google) then they may have trouble accessing it in the future. I repeated this script for a total of 74 new tab opens on the forum page which slowed down my Kali VM, increased my total CPU usage by a factor of 4, and physically heated my laptop. If more tabs were to be opened this could guarantee a crash. Firefox automatically stops new tabs from opening, but this attack could be changed to redirecting to a bunch of different websites which would similarly lag and DoS them. 


### E
The server could prevent the inputted text from being read as valid scripting by searching for <> and </> and preventing them from being treated as language syntax, perhaps by using escape characters. I don't think there is much that the browser can do because it would be difficult/not worth it to differentiate between Moriarty's attacks and valid Javascript embedded in a HTML file. 

