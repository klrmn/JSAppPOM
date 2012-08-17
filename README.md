JSAppPOM
========

a (python) Page Object Model base class intended for use with sites that are JavaScript applications

In regular implementations of the POM, clicking on buttons and links often results in being sent to a new page. In websites that are designed more as JavaScript applications, clicking on things often results in a change to the page rather than going to a different page.

This class provides methods that wrap selenium's click(), send_keys(), text and get_attribute() methods to first wait for the locator to be present and displayed, then do the action, and, in the case of click() and send_keys(), wait for ajax to finish (as defined by jQuery.active == 0).

In this way, the Page Object writer is assured that the element they are trying to interact with will be there, and any processes that action triggers will be finished before the method returns.