# ai_framework
This is a speech recognition artificial intelligence framework that is aimed at being self programable (to the fullest extent), self learning, and fluid enough to where everything you want it to do, you can get it to do just by simply talking/typing to it.

## installation / basic usage

1. in a directory of your choosing, run command "git clone https://github.com/the-py-guy/ai_framework.git"
2. cd into ai_framework
3. run command "python main.py"
4. say hello

## basic information

since this is AI, your words do not need to be exact for any of the following commands we are about to go over. just say something similar and the AI will most likely know what you mean. If it doesn't, it will let you know it doesn't understand (try again but rephrase your sentence). with that being said, lets go into the advanced usage.

## advanced usage

* **predefined commands**
  - **saying "add a new action":** This will cause the AI to ask you what phrase should trigger this new action, lets respond: "tell me the weather" the AI has now remembered the phrase "tell me the weather". Now if you go into the "actions" directory, you will see a new python file that may look something like "Em0JckLXl77AvZFG6I6wkJ6ofmVItBw3.py" This is the script that the AI has created for this new action and will be ran everytime you say "tell me the weather". This file will contain a few predefined functions that you can take full advantage of when writing custom action scripts but other than that, it is up to you to actually program the part of this script that tells you the weather, or what ever it is you would like it to do.

  - **Saying variants of "yes":** Are interpreted as a confirmation.

  - **Saying variants of "no":** Are interpreted as a denial.

  - **Saying varients of "never mind":** Are interpreted as the user wanting to cancel dialog.
