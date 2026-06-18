```gherkin
Feature: Applicant login and start application

  Scenario: Applicant starts an application
    Given the applicant visits the portal
    When they submit the start form
    Then an application record is created with status "started"

```
