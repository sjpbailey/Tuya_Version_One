# Universal Devices Tuya Product NodeServer

## Currently for Tuya TreatLife Dimmers, Switches, LED Bulbs and Strip Lights

* ![Tuya-Bulb-Control](<https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/main/images_go/Screenshot%202023-06-21%20at%202.35.55%20AM.png>)

* Device Model Numbers:
* LED Strip V1 - \u706f\u5e26\u63a7\u5236\u5668\uff08BK\uff09
* LED Bulb V2 - SL10
* Switch V0 - SS01S\uff08\u706b\u7ebf\u8d1f\u8f7d\u7ebf\u4e0d\u5206\u7248\u672c\uff09BK\u7248\u672c
* Switch V1 - SS01S(\u4e0d\u5206\u8d1f\u8f7d)\u4e50\u946b
* Switch V2 - \u5f00\u5173(\u84dd\u7259+Wi-Fi)
* Switch Dimmer - DS01C(\u91cf\u4ea7\uff09)
* Not Added Yet Need to add Asynchronous I/O to scan status and for Light Control

## Description

* This pulls Device Data from your configured Tuya API Account
* You must first create a Tuya Account and have your Devices functional on the Tuya Smart Phone App.

1. TUYA ACCOUNT - Set up a Tuya Account
2. Please watch quick video [From This Smart House](https://youtu.be/M9Q6de08QOI)

* Create a Tuya Developer account on [iot.tuya.com](https://iot.tuya.com/).
* [Tuya](https://en.tuya.com/) devices are designed to communicate with the TuyaCloud, allowing us to directly control the devices using the cloud. This python connector module authenticates your devices.
* [Tuya Instructions](https://developer.tuya.com/en/docs/iot/quick-start1?id=K95ztz9u9t89n)
* [PDF Instructions](<https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/ffbbf456fa85dbeebc11b04bc04ba75a73b49203/images_go/Tuya.IoT.API.Setup%20(3).pdf>)
* Click on "Cloud" icon -> "Create Cloud Project"
* 1. Remember the "Data Center" you select.([screenshot](https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/ffbbf456fa85dbeebc11b04bc04ba75a73b49203/images_go/Screenshot%202023-06-18%20at%2011.10.44%20PM.png)).
* 2. Skip the configuration wizard but remember the Authorization Key: *API ID* and *Secret* for below ([screenshot](https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/ffbbf456fa85dbeebc11b04bc04ba75a73b49203/images_go/Screenshot%202023-06-18%20at%2011.11.41%20PM.png)).
* Click on "Cloud" icon -> Select your project -> **Devices** -> **Link Tuya App Account** ([see screenshot](https://user-images.githubusercontent.com/836718/155827671-44d5fce4-0119-4d0e-a224-ef3715fafc24.png))
* Click **Add App Account** ([screenshot](https://user-images.githubusercontent.com/836718/155827671-44d5fce4-0119-4d0e-a224-ef3715fafc24.png)) and it will display a QR code. Scan the QR code with the *Tuya Smart app* on your Phone (see step 1 above) by going to the "Me" tab in the *Tuya Smart app* and clicking on the QR code button `[..]` in the upper right hand corner of the app. When you scan the QR code, it will link all of the devices registered in your *Tuya Smart app* into your Tuya IoT project.
* **NO DEVICES?** If no devices show up after scanning the QR code, you will need to select a different data center and edit your project (or create a new one) until you see your paired devices from the *Smart Life App* show up. ([screenshot](https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/ffbbf456fa85dbeebc11b04bc04ba75a73b49203/images_go/Screenshot%202023-06-18%20at%2011.13.45%20PM.png)). The data center may not be the most logical. As an example, some in the UK have reported needing to select "Central Europe" instead of "Western Europe".

* **SERVICE API:** Under "Service API" ensure these APIs are listed: `IoT Core`, `Authorization` and `Smart Home Scene Linkage`. To be sure, click subscribe again on every service.  Very important: **disable popup blockers** otherwise subscribing won't work without providing any indication of a failure. Make sure you authorize your Project to use those APIs:
* Click "Service API" tab
* Click "**Go to Authorize**" button
* Select the API Groups from the dropdown and click `Subscribe` [screenshot](<https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/ffbbf456fa85dbeebc11b04bc04ba75a73b49203/images_go/Screenshot%202023-06-18%20at%2011.14.31%20PM.png>)

## Requirements-

1. udi-interface
2. tuya-connector-python
3. tinytuya 1.12.7

### Release Notes

* Enter Your Access ID as apiAccessId = "Your API Access ID
* Enter your Access Secret as apiSecret = Your API Secret

* ![API ACCESS ID and SECRET Location](https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/main/images_go/Screenshot%202023-06-16%20at%203.57.31%20PM.png)

* API UID as apiUid = Your UID found Tuya Site key = baspi_ip Value = Your IP Address.

* ![UID Location](<https://github.com/sjpbailey/udi-tuya-poly-cloud-api-v3/blob/main/images_go/Screenshot%202023-06-16%20at%203.51.36%20PM.png>)

* API Endpoint as apiEndpoint = https:// openapi.tuyaus.com/
* API MQ Endpoint as apiMq = wss://mqe.tuyaus.com:8285/
* *Region* (cn, us, us-e, eu, eu-w, or in) So the (tuyaus) in the links above = us = USA, cn = Canada etc...

* 3.0.1 06/16/2023

* Initial version published to github
