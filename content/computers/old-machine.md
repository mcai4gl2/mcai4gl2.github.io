---
title: "Salvaging My Old Desktop"
date: 2021-07-21T10:09:04+08:00
---

I have been using a [HP Pavilion 550-153na](https://support.hp.com/gb-en/document/c04835128) desktop for several years. Bought this computer back in 2015 winter as it was on close down sale from Currys. I went in last day after work and it is on 50% off, so I paid 250 pounds and got it.

I would admit that I bought it more because of the discount rather than the spec. Only when I got home, I really looked into the spec. It has i5-6400 CPU, 8 GB RAM, 2TB hard drive and a Radeon R5 330 graphic card. I have use it over years for writing code and game playing. Game playing is not very good given the spec, but I have to work with what I have and playing less demanding games.

I have been looking at how I could upgrade the machine from time to time. Getting a better graphic card would be an obvious starting point. But, I was worried that the power supply wouldn't be good enough and I need to buy another power supply. Power supply is the same reason I didn't upgrade the hard drive to SSD, as there is only one SATA power cable. So, I sticked with HDD for years. 

The machine is far from great but it kind of serves the purpose. So, when I moved from London to HongKong in 2019, I didn't throw it away but carried it over to HongKong. Over the years, the machine has definitely slowed down. I don't know the best way to clean up the hard drive so I installed ubuntu as an alternative operating system. 

This worked quite well until COVID hits. I didn't manage to get Citrix working on ubuntu so I had to switch back to Windows so I can remote login to work. I was getting more and more annoyed by the slow spinning disk. In the end, I unplugged the old HDD and bought a 1TB SanDisk SSD Plus. A SSD and a newly installed operating system definitely gave the old machine a second life. As I slowly getting into classic music, the machine's CD drive was also put into use a lot. 

Coming into 2021 and second year working from home, I desperately wanted a home PC upgrade. I have to admit that there was no particular reason for the upgrade as the old PC still works perfectly fine. Maybe not able to play games was the main pain point. But I knew that was just an excuse. Anyway, I had my eye on the new Intel NUC11 and put in order as soon as it was out. 

Now the old PC finally retired. I don't want to throw it away immediately as the parts could be useful somewhere else. The first usage case would be the 2TB hard drive it has. I put it into an [ORICO 2 bay hard drive enclosure](https://www.amazon.com/ORICO-Bay-Hard-Drive-Enclosure/dp/B0734CZSXL/ref=sr_1_6). This is now connected to my Raspberry Pi and used for downloading and storage for pictures. 

I took out the CPU and plan to buy a second hand HP 800 G2 mini barebone PC. The SanDisk SSD shall also fit there. I am planning to give this PC to my parents. It shall be powerful enough for their usages for next few years. I also took out the memory from the PC, but I don't know where they could be used for now.

I thought this was it and I could now throw the rest of the machine until I bought a Jetson Nano. Jetson Nano doesn't come with wifi. As my routers are in the living room and there is no wired connection to the study room, a wifi is must have if I want to use the Jetson Nano. I searched in old PC box and found that it has a removable Intel 3165 wifi card. So I moved the card and the antenna from the old box into Nano. With some googling, I managed to get the driver working as well. 

I have been using Nano for several days and didn't really like the fact that I had to unplug/replug the power cable every time I need to start the machine. So I started reading the option of having a power button. It looks quite simple as long as I have a button. Before ordering one from Amazon, I realised that the old PC has the same thing. So this time, I took out the power button and the light and plug it into Nano. Now I can turn on Nano without touching the power supply.

I decided to keep the old PC for some more time now given my journey of reusing things. The CPU and hard drive were obvious but the power button was definitely a surprise for me. 

It is also intriguing to see how little differences in my productivity when using the old machine vs new machine. I measure my productivity crudely by looking at codes I write after work. In 2020, I am writing all of these commits in my old PC:
![2020](/old-machine/2020.PNG)
In 2021, I got the new PC in late Mar:
![2021](/old-machine/2021.PNG)
In another word, it is very hard to justify the money I spent on buying the new NUC, haha.
