# Not Just a Normal URL Shortener
---
**[https://viditagarwal.pythonanywhere.com/](https://viditagarwal.pythonanywhere.com/)**

This is a repo for a web app which can make short URL masks for long URLs.

**Disclaimer:** Currently, it has no database as such all the data is stored as python dictionary which is pickled and saved at certain frequency to disk. Thus shortened links can go away anytime.

# What does it do?
  - Creates short URL masks.
  - Prevents non-alphanumeric masks and long URLs without http or https.
  - *Number of time the short link was clicked.*
  - *List of IP Address that clicked the short link.*
  - *Count of which IP Address clicked the short link how many times.*

# TODO:
  - Add a database
  - Add a login system so the detailed view can only be accessed by the one made the short URL
  - Add ReCaptcha Verification based on IP Address that if excessive traffic is noticed from particular IP address then pass the user through Captcha Verification.
  - Based on the IP Address get the city, state and country of the visitor and show it in detailed view table for **better analytics**.
  - Create a data for malicious websites so no malicious sites can be shortened. If a site which has been shortened turns out to be malicious remove its mask.
  - Provide the user who created the mask a list of the masks they have produced and feature to delete them.

**If you want to contribute to any of above TODO then open a issue corresponding to it, I will assign you to that issue and then when feature gets implemented the pull request after review will be merged.**
