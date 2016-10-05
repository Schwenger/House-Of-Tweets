# View:
The application's page is divided into three major parts.

### Center:

  On the center page there are control elements allowing to change the displayed tweets, used sounds, and displayed language. It also allows to re-play tweets.

### Left / Voices Lists:

  Two lists, one for the featured politicians, and one for the featured birds. Each entry in this list allows to open the respective profile page.

### Right / Citizen User: 

  A form allowing a citizen to register their twitter account temporarily.

-------------

# Logic:

### Connection:

All connections to the BackEnd are established using the [Connector](connector.coffee).
When tweets are received, the [Tweet Controller](tweet_controller.coffee) consumes it, adapts the DOM accordingly and notifies the [Sound Controller](sound_controller.coffee) such that the sound is played.

The FrontEnd itself sends information about newly registered Citizen Users to the BackEnd.

### Page Control:

The center page does not have a dedicated controller. 
It's control elements are indirectly vitalized by [Main](main.coffee), where is controller is set up. This especially includes:

* [Screensaver](screensaver.coffee) running as a time triggered daemon.

* [Display](display.coffee) controlling switches between pages triggered by user interactions.

* [Language Controller](language_controller.coffee) changing the language of all static elements and notifies all interested controllers.

* [Citizen User Controller](citizen_user.coffee) sets up the respective page and sends data to the BackEnd. 

* [Voices Lists Controller](voices_lists.coffee) sets up the respective pages and establishing a connection to the [Profiles Pages](profiles.coffee)

# Model:

The model consists of three components:

* [Language](model_messages.coffee): dictionary mapping a message id to the respective translations in all supported language.

* [Birds](model_birds.coffee): dictionary mapping an id based on the bird's German name to all interesting information, like a link to an image, the names, and a short description.

* [Politicians](model_polis.coffee): dictionary mapping a numeric id to all interesting information, like a link to an image, the party, and a short description.
