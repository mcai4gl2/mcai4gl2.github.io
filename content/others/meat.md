---
title: "Meat Day Today!"
date: 2021-07-21T13:20:46+08:00
---

It may sound strange but I always found eating out by myself very weird. It maybe due to the fact that I couldn't order many dishes. Maybe it is just the loneness when seating down by myself. Maybe it is because I don't have a lot of things to watch on my phone. I have always prefer to cook myself at home or do takeaways. I even rarely do delivery until early this year during my two weeks' quarantine in Hongkong. The last time I eat out by myself this year would go back to my birthday in April, when I went to Outback Steakhouse in Olympian city for lunch.

I planed to go Gyu-Kaku for buffet for sometime. It sounds not that good an idea because Gyu-Kaku has always been busy with long queues. Also, I am kind of on diet for past several weeks and I skip dinner completely. But since I am on holiday this week, I feel I shall really go and take advantage of the discount on work day, haha.

I did exactly the kind of preparation needed for buffet, skipping dinner last night (as usual) and skipping breakfast this morning as well. So, I went to Gyu-Kaku quite early today at 11:30. Not only because there would be no queue at the time, but also because I am quite hungry at the time.

The no queue experience is good. I chose the US SRF Angus Wagyu Buffet, which is 338 HKD for early bird on work day (90 mins eating). I got my QR code and then ready to order with my phone. Like any software, the website doesn't open. I was cautious about my phone's reception in the restaurant so I took both my phones with me today, both of which don't work on the ordering website. Waiting for 5 mins, I managed to open the page but when submitting the order, the website gave me error connecting to the server. So, I had to get my order done manually with waiter. With another 5 mins waiting, my first round of food finally arrived:
![first](/meat/first.jpg)
The food is nice but it is already 20 mins since I set down!

The website is then up and down from time to time. I got a new QR code from the restaurant. I tired to order second round of food but got different errors. I stopped trying and waited for 5 mins. I did get the food but everything was doubled up since I submitted twice as it failed the first time around (apparently not failed):
![second](/meat/second.jpg)
I didn't mind doubling it up as I enjoyed the food anyway.

Finally, after I got my third QR code, the website is fully functional. I got some more meat:
![third](/meat/third.jpg)
and noodles:
![noodles](/meat/noodles.jpg)

Since I am eating by myself, I am very much concentrated on eating. So, 90 mins is more than enough to fill me up. I didn't ask for extension of my 90 mins because their technology doesn't work. In the end, I paid 371.8 with 10% service charge. I would argue the service is not that good given all the problems with their website on a grumpy day. But given all the meat I have today after 2 weeks of diet, I am happy enough to just pay and leave. 

Foods I enjoyed:
* The sauce is pretty good to mix with any kind of barbecue
* The beef tongues are good for me. It is not a thing I usually cook. So, very nice to have it when I am eating out
* Enoki mushroom is interesting idea
![mushroom](/meat/mushroom.jpg)

Foods I found a little bit strange:
* Tripe and intestine are a little bit strange for barbecue
* Oyster is not as good as I hoped

After I got home, I opened the website in my phone again as I would like to get a screenshot of all the foods I ordered. Unfortunately, instead of my orders, I got the next customer sitting at my table's order instead. Looking at the webpage URL, there is a token which I guess linked to the QR code, so I guess my QR code just had the wrong expiry. I don't particular mind to see other people's ordering, as it gave me several ideas on what I would like to try next time. But from a software developer perspective, a cross client incident is not good. The QR code should have expired as soon as I paid or it shall still show my orders until some house keeping.

The website's URL is: https://kabu-byod.azurewebsites.net/order?shopCode=GKK-OC&token=. I wonder how much penetration/security tests have been done. It is not something I am familiar with though. So, I won't randomly generate some tokens and try to hit the link.

A good lunch with some software failures. My diet continues tomorrow. I am not looking forward to weight myself tomorrow morning though ...