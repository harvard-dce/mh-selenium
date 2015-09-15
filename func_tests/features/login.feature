Feature: testing admin login
  Scenario: visting the admin site redirects to login
    Given we visit the admin site
     then we are redirected to the login page

  Scenario: successful login
    Given we are on the login page
     when we provide correct credentials
     then we see the recordings page

  Scenario: failed login
    Given we are on the login page
     when we provide incorrect credentials
     then we see a login error
