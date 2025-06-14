Front matter

Project Name: Sanare Soma

Version: 1.0

Author: Jane Aldakkour

Date: February 10, 2025



Introduction

This document outlines the requirements for the project titled Sanare Soma. This project aims to design and develop a software program which assists individuals in identifying ailments, connecting to professionals, and developing personalized and sustainable dietary and personal injury recovery plans to help them recover from said ailments. This software should address issues that individuals face when trying to identify effective exercise routines and diets that fit their individual needs, as well as identifying which professional will be able to best help them accomplish their goals. Users should be able to connect to reliable professionals, obtain information on their ailments, track nutritional and physical stats, and create their own personalized exercise and therapy routines that they will benefit from most. 


Table of contents

1. Introduction

    1.1 Table of Contents

3. Requirements Statements

    2.1 User Stories

    2.2 Use Cases

    2.3 Features

    2.4 Gherkin Validation

5. Specifications

     3.1 Concept

    3.2 Interfaces

    3.3 Behaviors

4.UML Diagram


2. Requirements statements

2.1 User Stories

   - As a user recovering from a knee injury, I want to create a personalized exercise program so that I can regain strength and mobility safely
   
   - As a professional nutritionist, I want to be able to contribute generalized advice and potentially offer to develop personalized plans for individual users
   
   - As a user with the goal to lose weight to help relieve joint pain, I want to track my macronutrient intake so that I can ensure I'm meeting my dietary needs.


2.2 User Cases
   
    User A has recently had a full knee replacement surgery and has undergone physical therapy. After the initial round of physical therapy, User A wishes to continue to build back leg strength. User A does this by signing up for the software and navigating to the exercises page, where they put together their own personalized program with exercises that focus on the quadraceps, hamstrings, and calf muscles. This will develop leg strength that will help support the knee and further their recovery. 

    User B has recently been suffering from sleep apnea and wishes to learn about how they can alieviate their symptoms by connecting to a professional. User B navigates to the connect page to find a professional who can help them learn that they can lose weight to help alieviate the symptoms. User B can then connect with a nutritionist to develop a personalized plan, or build their own by using the nutritional tracker, which they will then use to track their caloric intake and weight loss goals. 

    User C has recently had serious lower back pain. User C navigates to the exercises page and creates a personalized routine which stretches the lower back and opens up the hips as well to help allieviate lower back pain. Seeing as there are hundreds of different exercises offered, there are endless combinations for the user to create and personalize so that they are not limited to the same routine every day should they choose to want some variety. 


2.3 Features
  
    1. Nutritional Tracking: Allows users to log food intake, track macronutrients and calories, and monitor dietary progress.
    2. Personalized Therapy Program Development: Enables users to create customized exercise programs based on their injury type, goals, and available equipment.
    3. Professional Guidance & Information: Provides access to reliable information and advice from nutritionists, doctors, and physical therapists.
    4. Progress Tracking: Allows users to monitor their progress in terms of exercise adherence, nutritional intake, and goal achievement.
    5. Reviews Pages: Allows users to leave reviews and rate the professionals that they talk to. This way, the site will be able to offer only the best healthcare connections. 


2.4 Gherkin Validation 

Feature: Personalized Exercise Routine Creation

    Allows users the ability to search through hundreds of different exercises and stretches, select their own grouping of exercises based on their personal goals and arrange them into a routine. 

  
  Scenario: Leg Day Routine Creation
  
    Given The user has suffered from a knee injury   
    When The user is on the exercises page and the user has selected their exercises
    Then The user should be ablel to arrange the videos for those exercises in the order they wish and play them all consecutively in order to go through their own personalized workout routine


3. Specifications

   3.1 Concept

    The platform will be a mobile app and/or website that integrates nutritional tracking, personalized exercise program            development, and access to professional guidance. It will use an incremental development approach, focusing on core             features such as the exercise routine development, the nutritional tracker, and the professionals connections pages each initially and expanding the functionality of each over time. It will also allow me to integrate them later on. 

   3.2 Interfaces

    - input fields for food logging 

    - input fields for searching exercises

    - Option to rearrange exercises order

    - Buttons for navigation and action execution

    - Charts and graphs for data visualization on tracking nutritional stats

    - Search functionality for food database and exercise library

    - messaging forum to/from professionals


   3.3 Behaviors

    - The system should accurately calculate macronutrient and calorie intake

    - The system should provide personalized exercise suggestions based on user input

    - The system should allow users to customize thier nutrition and exercise plans

    - The system should allow users to connect to professionals 

    - The system should provide recommendations to highly rated professionals on the site and that are best suited to that individuals needs

    - The system should securely store user data

5. UML Diagram

![Diagram of Sanare Soma](https://github.com/jaldakkour/CIDM6330_FinalProject/blob/main/Assignment%201/Assignment1_for_final.png)

