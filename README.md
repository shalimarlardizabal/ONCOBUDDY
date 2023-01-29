# ONCO BUDDY

Onco Buddy is a full-stack web application designed to assist cancer patients in becoming more active participants in managing their health. Going through chemotherapy can be very daunting, and the vast amount of information available about cancer can be hard to navigate. Onco Buddy provides personalized information based on the user’s diagnosis and treatments. The daily log feature allows users to keep track of their daily pain level, fatigue, sleep, and appetite. In addition, users can record symptoms and when they have administered treatments. The calendar feature allows visualization of treatment dates and the onset of symptoms. 

## About the Developer

Onco Buddy was created by Shalimar Lardizabal. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/shalimarlardizabal/).

## Tech Stack

* Python
* Flask
* PostgreSQL
* SQL Alchemy
* Jinja2
* HTML
* CSS
* Bootstrap
* Javascript
* AJAX/JSON
* Chart.js
* JS fullCalendar API
* Infermedica API

## Features

### User Authentication
![User Authentication](/static/Images/Readme-screenshots/Login.png)

Users log in on this page. User authentication checks database whether email and password matches. 
### Create an Account
![Create an Account](/static/Images/Readme-screenshots/Sign-Up.png)

If email exists, users will be asked to sign-in instead. 

### Intake Page
![Intake](/static/Images/Readme-screenshots/Intake.png)

### Add Diagnosis
![Add Diagnosis](/static/Images/Readme-screenshots/Add-Diagnosis.png)

### Add Treatments
![Add Treatments](/static/Images/Readme-screenshots/Add-Treatment.png)

### Add Other Conditions
![Add Other Conditions](/static/Images/Readme-screenshots/Add-other-conditions.png)

After creating an account, users are redirected to the intake page. Here, they will add diagnosis, treatment and other conditions. 

### Daily Log
![Daily Log](/static/Images/Readme-screenshots/DailyLog.png)

This is the page users will see every time they log in. They can enter their pain level, location of pain, fatigue level, sleep level, and appetite level. 

### Add Symptoms and Administered Treatments
![Symptoms and Treatments](/static/Images/Readme-screenshots/Symptoms-Treatment-Log.png)

If they are experiencing symptoms, they can log it here. If they got treatment the same day, they can also log it here. 

### User Health Profile
![Health Profile](/static/Images/Readme-screenshots/User-Profile.png)

This is the user health profile where they can see personalized information. 

### Diagnosis Information
![Diagnosis Information](/static/Images/Readme-screenshots/Diagnosis.png)

They can read and learn more about their diagnosis. 

### Treatment Information
![Treatment Information](/static/Images/Readme-screenshots/Treatment.png)

They can read and learn more about their treatments. 

### Daily Log Chart
![Daily Log Chart](/static/Images/Readme-screenshots/DailyLog-chart.png)

Data from daily log input will be reflected on this chart to see progression.

### Logged Symptoms and Administered Treatments
![Symptoms and Treatments](/static/Images/Readme-screenshots/Logged.png)

Users are able to see symptoms and administered treatments with dates. 

### Calendar
![Calendar](/static/Images/Readme-screenshots/Calendar.png)

Users can visualize date of treatment and onset of symptoms. 

## Version 2.0
* Implement a live-search for drop-down select
* Implement a "wall" section where users with the same diagnosis can share stories and experiences
* Implement comment feature for stories and experiences