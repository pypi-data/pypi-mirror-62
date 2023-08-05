# Contributing to PyCirkuit

You are here to help on PyCirkuit? Awesome! PyCirkuit is still at its infancy and needs a lot of love and work. If tou find this application useful, there are some areas where you can help, depending on your interests and level of expertise:

  - Writing documentation
  - Translating the app to your native language
  - Finding bugs and fixing issues
  - Contributing code


## Contributing guidelines

At present, PyCirkuit is a small project with little infrastructure around. Contributions are welcome and they don't have to adhere to any particular convention, but will be accepted or rejected at developer's discretion.

Meanwhile, you can ask questions or send contributions directly to me at [mailto:orestes@tsc.upc.edu](mailto:orestes@tsc.upc.edu).

**Thanks!**


## Contributing translations

The application is fully internationalized, so you can translate it to your language. If you want to do so, please follow these steps:

  1. Install the [Qt developping tools](https://www.qt.io/download), specially "Linguist". Unfortunately, Qt company does not offer you to download Linguist separately of the other developping tools. If you need/want install only QtLinguist, you can check [this project](https://github.com/lelegard/qtlinguist-installers).

  3. Locate the file [pycirkuit/L10n/pycirkuit_empty.ts](https://github.com/orestesmas/pycirkuit/blob/master/pycirkuit/L10n/pycirkuit_empty.ts) and copy it into a new file named "pycirkuit.LOCALE.ts" where LOCALE is the code/country of your language. For instance for french it can be "fr", "fr_CA", "fr_FR", etc. See [this Wikipedia entry](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for a complete list.
  4. Open the new file under Linguist and translate all the strings in it. The [Qt Linguist manual](http://doc.qt.io/qt-5/qtlinguist-index.html) can be helpful.
  5. Send the translated .TS file to the PyCirkuit developers or, if you know how to do it, create a pull/merge request.