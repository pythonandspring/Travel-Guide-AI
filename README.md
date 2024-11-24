Travel Guide AI
===============

Module 01: Overview
--------------------

Frontend Team
-------------
Members:
1. Jayandhan Rajendran (Lead)
2. Rohan Mondal
3. Komal Kadu Pandit
4. Nithya Lakshmi
5. CharithaSree Vanamala

Team Contributions:

1. Jayandhan Rajendran:
   - Designed Admin Login, Dashboard, and Integration.
   - Created views and routes for related pages.
   - Added staff assignment functionality for admin CRUD operations on user profiles.
   - Developed a `base.html` template with reusable header and footer components.
   - Integrated Alertify.js for notification popups.

2. Rohan Mondal:
   - Implemented password update functionality for users who forgot passwords.
   - Added authentication features with strong password validation.

3. Nithya Lakshmi:
   - Designed and developed the following pages:
       * home.html
       * accommodations.html
       * contact.html
       * customer.html
       * edit_profile.html
       * edit_user.html
       * feedback.html
       * privacy_policy.html
       * profile.html
       * terms_conditions.html
   - Styled the pages with clean, user-friendly stylesheets.

4. Komal Kadu Pandit:
   - Designed Admin Login Page and Dashboard.
   - Created a Gallery Page.
   - Contributed to the `base.html` file design.

5. CharithaSree Vanamala:
   - Designed Customer Registration Page.
   - Added input validations for user registration.

Backend Team
------------
Members:
1. Rajeshwari Ch
2. Gaurav Desai
3. Hareesh J
4. Rama Tulasi Akula
5. Raunak Mishra
6. Kusuma

Team Contributions:

1. Rajeshwari Ch:
   - Implemented user registration and login functionality.
   - Created views for login, logout, and register.
   - Used Django's built-in forms to handle user changes.
   - Configured routing in `urls.py` within the `customer` folder.

2. Gaurav Desai:
   - Created views for `user_profile` and `edit_profile`.
   - Developed forms using the Profile model for editing user details.
   - Added password reset functionality with strong validations.
   - Configured paths in `urls.py` for routing views and forms.

3. Hareesh J:
   - Added a custom `myadmin` app.
   - Implemented admin login, logout, and staff toggle functionalities in `myadmin.views`.
   - Configured routing in the `myadmin` app and integrated with the frontend.

4. Rama Tulasi Akula, Raunak Mishra, and Kusuma:
   - Utilized the Speech Recognition library for converting speech to text.
   - Used PyAudio for microphone access.
   - Integrated the functionality with Django and the frontend.

Database Team
-------------
Members:
1. Iqbal

Team Contributions:

1. Iqbal:
   - Created user database using Django's inbuilt User model.
   - Extended the User model with a custom Profile model in `models.py`.
   - Established a `OneToOneField` relationship with the User model.
